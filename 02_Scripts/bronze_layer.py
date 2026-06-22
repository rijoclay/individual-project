"""
bronze_layer.py - Data Ingestion Layer (Bronze)
Reads 4 data sources: CSV (main dataset), JSON (benchmarks), CSV (execution logs), and JSON API (OpenAlex Papers).
Adds metadata (ingestion_date, data_source) and writes to Parquet format.
"""

import os
import sys

# Set Spark Home
os.environ['SPARK_HOME'] = r'C:\Users\richa\spark'
os.environ['HADOOP_HOME'] = r'C:\Users\richa\hadoop'
os.environ['PYSPARK_PYTHON'] = r'C:\Users\richa\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe'
os.environ['PYSPARK_DRIVER_PYTHON'] = r'C:\Users\richa\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe'
if os.environ['SPARK_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['SPARK_HOME'] + r'\bin'
if os.environ['HADOOP_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['HADOOP_HOME'] + r'\bin'

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
import json
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_DIR = os.path.join(BASE_DIR, '01_Input')
OUTPUT_DIR = os.path.join(BASE_DIR, '03_Output_Bronze')
LOG_DIR = os.path.join(BASE_DIR, '08_Logs')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Initialize Spark
spark = SparkSession.builder \
    .appName("IP2_Bronze_Ingestion") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
log = {"run_id": run_id, "layer": "bronze", "status": "started", "details": {}}

try:
    # --- Source 1: Main CSV Dataset ---
    csv_path = os.path.join(INPUT_DIR, 'AgenticAI_Leadership_Dataset_v1.csv')
    df_main = spark.read.option("header", "true").option("inferSchema", "true").csv(csv_path)
    df_main = df_main.withColumn("ingestion_date", current_timestamp()) \
                     .withColumn("data_source", lit("kaggle_csv"))
    
    main_count = df_main.count()
    log["details"]["main_csv_records"] = main_count
    print(f"[BRONZE] Main CSV loaded: {main_count} records")

    # --- Source 2: JSON Benchmark Data ---
    json_path = os.path.join(INPUT_DIR, 'external_leadership_benchmarks.json')
    df_bench = spark.read.option("multiLine", "true").json(json_path)
    df_bench = df_bench.withColumn("ingestion_date", current_timestamp()) \
                       .withColumn("data_source", lit("api_benchmark_json"))
    
    bench_count = df_bench.count()
    log["details"]["benchmark_json_records"] = bench_count
    print(f"[BRONZE] Benchmark JSON loaded: {bench_count} records")

    # --- Source 3: Execution Logs CSV ---
    logs_path = os.path.join(INPUT_DIR, 'agent_execution_logs.csv')
    df_logs = spark.read.option("header", "true").option("inferSchema", "true").csv(logs_path)
    df_logs = df_logs.withColumn("ingestion_date", current_timestamp()) \
                     .withColumn("data_source", lit("execution_logs_csv"))
    
    logs_count = df_logs.count()
    log["details"]["execution_logs_records"] = logs_count
    print(f"[BRONZE] Execution Logs loaded: {logs_count} records")

    # --- Source 4: OpenAlex API Papers JSON ---
    openalex_path = os.path.join(INPUT_DIR, 'openalex_ai_leadership_papers.json')
    df_papers = spark.read.option("multiLine", "true").json(openalex_path)
    df_papers = df_papers.withColumn("ingestion_date", current_timestamp()) \
                         .withColumn("data_source", lit("openalex_api_json"))
    
    papers_count = df_papers.count()
    log["details"]["openalex_papers_records"] = papers_count
    print(f"[BRONZE] OpenAlex API Papers loaded: {papers_count} records")

    # --- Write to Bronze Layer (Parquet) ---
    main_out = os.path.join(OUTPUT_DIR, 'main_dataset')
    df_main.write.mode("overwrite").partitionBy("Industry").parquet(main_out)

    bench_out = os.path.join(OUTPUT_DIR, 'benchmark_data')
    df_bench.write.mode("overwrite").parquet(bench_out)

    logs_out = os.path.join(OUTPUT_DIR, 'execution_logs')
    df_logs.write.mode("overwrite").parquet(logs_out)

    papers_out = os.path.join(OUTPUT_DIR, 'openalex_papers')
    df_papers.write.mode("overwrite").parquet(papers_out)

    log["status"] = "completed"
    log["output_paths"] = {
        "main_dataset": main_out,
        "benchmark_data": bench_out,
        "execution_logs": logs_out,
        "openalex_papers": papers_out
    }

except Exception as e:
    log["status"] = "failed"
    log["error"] = str(e)
    print(f"[BRONZE] ERROR: {e}")
    raise

finally:
    log_path = os.path.join(LOG_DIR, f'bronze_run_{run_id}.json')
    with open(log_path, 'w') as f:
        json.dump(log, f, indent=2, default=str)
    spark.stop()