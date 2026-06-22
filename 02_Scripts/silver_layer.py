import os
import sys
import json
from datetime import datetime

# Dynamic Config (No hardcoded paths if env exists)
if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = r'C:\Users\richa\spark'
if 'HADOOP_HOME' not in os.environ:
    os.environ['HADOOP_HOME'] = r'C:\Users\richa\hadoop'

if os.environ['SPARK_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['SPARK_HOME'] + r'\bin'
if os.environ['HADOOP_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['HADOOP_HOME'] + r'\bin'

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    current_timestamp, lit, col, lower, when, round as spark_round, coalesce, expr, avg, count
)
from pyspark.sql.types import DoubleType

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_DIR = os.path.join(BASE_DIR, '03_Output_Bronze')
OUTPUT_DIR = os.path.join(BASE_DIR, '04_Output_Silver')
LOG_DIR = os.path.join(BASE_DIR, '08_Logs')

os.makedirs(OUTPUT_DIR, exist_ok=True)

spark = SparkSession.builder \
    .appName("IP2_Silver_Cleansing_Advanced") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
log = {"run_id": run_id, "layer": "silver", "status": "started", "details": {}}

try:
    # 1. Read Bronze
    df_main = spark.read.parquet(os.path.join(INPUT_DIR, 'main_dataset'))
    df_bench = spark.read.parquet(os.path.join(INPUT_DIR, 'benchmark_data'))
    df_logs = spark.read.parquet(os.path.join(INPUT_DIR, 'execution_logs'))
    df_papers = spark.read.parquet(os.path.join(INPUT_DIR, 'openalex_papers'))

    initial_count = df_main.count()
    log["details"]["input_records"] = initial_count

    # 2. Deduplication
    df_main_dedup = df_main.dropDuplicates(["Record_ID"])
    log["details"]["duplicates_removed"] = initial_count - df_main_dedup.count()

    # 3. Standardize Categorical
    cat_cols = ['Organization_Size', 'Leadership_Function', 'AI_Maturity_Level', 'Agent_Type', 
                'Use_Case_Area', 'Agent_Autonomy_Level', 'Decision_Making_Type', 'Task_Complexity_Level', 
                'Human_Oversight_Level', 'Explainability_Level', 'Data_Privacy_Compliance', 'Integration_Level', 'Adoption_Success_Level']
    
    df_std = df_main_dedup
    for c in cat_cols:
        if c in df_std.columns:
            df_std = df_std.withColumn(c, lower(col(c)))
    
    # 4. Numerics & Robust Median Imputation
    numeric_cols = ['Context_Awareness_Score', 'Task_Success_Rate', 'Response_Time_Seconds', 
                    'Productivity_Improvement_Percent', 'Leadership_Trust_Score']
    for c in numeric_cols:
        df_std = df_std.withColumn(c, col(c).cast(DoubleType()))

    df_imputed = df_std
    for c in numeric_cols:
        medians = df_imputed.groupBy("Industry").agg(expr(f"percentile_approx({c}, 0.5)").alias(f"median_{c}"))
        global_median = df_imputed.approxQuantile(c, [0.5], 0.01)
        global_val = global_median[0] if global_median else 0.0
        
        df_imputed = df_imputed.join(medians, on="Industry", how="left")
        df_imputed = df_imputed.withColumn(c, coalesce(col(c), col(f"median_{c}"), lit(global_val))).drop(f"median_{c}")

    # 5. Benchmarks Join
    df_bench_clean = df_bench.select(
        col("Industry"),
        col("Benchmark_Task_Success_Rate").cast(DoubleType()),
        col("Benchmark_Productivity_Improvement").cast(DoubleType()),
        col("Benchmark_Trust_Score").cast(DoubleType())
    )
    df_joined = df_imputed.join(df_bench_clean, on="Industry", how="left")

    # 6. Logs & Derived Efficiency Feature
    df_logs_clean = df_logs.select(['Record_ID', 'Execution_Time_Minutes', 'Messages_Sent', 'Memory_Usage_MB', 'CPU_Utilization_Percent', 'Error_Count'])
    df_logs_enhanced = df_logs_clean.withColumn(
        "Memory_Per_Message_MB", 
        when(col("Messages_Sent") > 0, spark_round(col("Memory_Usage_MB") / col("Messages_Sent"), 2)).otherwise(0.0)
    )
    df_integrated = df_joined.join(df_logs_enhanced, on="Record_ID", how="left")

    # 7. Advanced OpenAlex Contextual NLP Mapping
    # Extracts keywords from title to map research citations directly to specific Industries
    df_papers_mapped = df_papers.withColumn("title_lower", lower(col("title"))).withColumn(
        "Mapped_Industry",
        when(col("title_lower").rlike("financ|bank|account"), "Financial Services")
        .when(col("title_lower").rlike("educat|student|teach|learn"), "Education")
        .when(col("title_lower").rlike("health|medic|care|patient"), "Healthcare")
        .when(col("title_lower").rlike("manufact|supply|logist|industry 4.0"), "Manufacturing")
        .when(col("title_lower").rlike("retail|commerce|market"), "Retail")
        .when(col("title_lower").rlike("tech|software|data|cyber|digital"), "Technology")
        .when(col("title_lower").rlike("govern|polic|public"), "Government")
        .otherwise("General_Research")
    )
    
    paper_agg = df_papers_mapped.filter(col("Mapped_Industry") != "General_Research") \
        .groupBy("Mapped_Industry").agg(
            spark_round(avg("citations"), 2).alias("Industry_Citation_Avg"),
            spark_round(avg("relevance"), 2).alias("Industry_Relevance_Avg"),
            count("paper_id").alias("Mapped_Paper_Count")
        )
        
    df_integrated = df_integrated.join(paper_agg, df_integrated["Industry"] == paper_agg["Mapped_Industry"], "left")
    df_integrated = df_integrated.fillna({
        "Industry_Citation_Avg": 0.0,
        "Industry_Relevance_Avg": 0.0,
        "Mapped_Paper_Count": 0
    }).drop("Mapped_Industry")

    # 8. Derived Final Columns (Business Logic)
    df_silver = df_integrated.withColumn(
        "Response_Time_Category", 
        when(col("Response_Time_Seconds") <= 3.0, "fast")
        .when(col("Response_Time_Seconds") <= 7.0, "moderate")
        .otherwise("slow")
    ).withColumn(
        "Productivity_Category", 
        when(col("Productivity_Improvement_Percent") < 10.0, "low")
        .when(col("Productivity_Improvement_Percent") < 15.0, "medium")
        .otherwise("high")
    ).withColumn(
        "Task_Complexity_Score", 
        when(col("Task_Complexity_Level") == "simple", 1)
        .when(col("Task_Complexity_Level") == "moderate", 2)
        .otherwise(3)
    ).withColumn(
        "Trust_vs_Benchmark_Gap", 
        spark_round(col("Leadership_Trust_Score") - col("Benchmark_Trust_Score"), 2)
    ).withColumn("processing_timestamp", current_timestamp())

    final_count = df_silver.count()
    log["details"]["output_records"] = final_count

    # 9. Output to Parquet
    silver_out = os.path.join(OUTPUT_DIR, 'agentic_leadership_silver')
    df_silver.write.mode("overwrite").partitionBy("Industry").parquet(silver_out)
    print(f"[SILVER] Success. Records: {final_count}. Contextual NLP mapped OpenAlex papers to Industries.")

    log["status"] = "completed"

except Exception as e:
    log["status"] = "failed"
    log["error"] = str(e)
    import traceback
    traceback.print_exc()
    raise

finally:
    log_path = os.path.join(LOG_DIR, f'silver_run_{run_id}.json')
    with open(log_path, 'w') as f:
        json.dump(log, f, indent=2, default=str)
    spark.stop()
