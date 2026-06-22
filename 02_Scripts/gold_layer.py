import os
import sys
import json
from datetime import datetime

if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = r'C:\Users\richa\spark'
if 'HADOOP_HOME' not in os.environ:
    os.environ['HADOOP_HOME'] = r'C:\Users\richa\hadoop'

if os.environ['SPARK_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['SPARK_HOME'] + r'\bin'
if os.environ['HADOOP_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['HADOOP_HOME'] + r'\bin'

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, round as spark_round, when
from pyspark.ml.feature import VectorAssembler, StandardScaler, StringIndexer
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_DIR = os.path.join(BASE_DIR, '04_Output_Silver', 'agentic_leadership_silver')
OUTPUT_DIR = os.path.join(BASE_DIR, '05_Output_Gold')
LOG_DIR = os.path.join(BASE_DIR, '08_Logs')
MODEL_DIR = os.path.join(OUTPUT_DIR, 'models')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

spark = SparkSession.builder \
    .appName("IP2_Gold_AI_Analytics_Advanced") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
log = {"run_id": run_id, "layer": "gold", "status": "started", "details": {}}

try:
    df_silver = spark.read.parquet(INPUT_DIR)
    print(f"[GOLD] Silver data loaded: {df_silver.count()} records.")

    # =========================================================================
    # 1. Unsupervised: K-Means Clustering (Performance Profiles)
    # =========================================================================
    features_km = ["Task_Success_Rate", "Productivity_Improvement_Percent", "Leadership_Trust_Score"]
    
    assembler_km = VectorAssembler(inputCols=features_km, outputCol="km_raw_features")
    df_km_vec = assembler_km.transform(df_silver)
    
    scaler_km = StandardScaler(inputCol="km_raw_features", outputCol="km_scaled_features", withStd=True, withMean=True)
    df_km_scaled = scaler_km.fit(df_km_vec).transform(df_km_vec)
    
    kmeans = KMeans(featuresCol="km_scaled_features", predictionCol="AI_Performance_Cluster", k=3, seed=42)
    model_km = kmeans.fit(df_km_scaled)
    df_km_out = model_km.transform(df_km_scaled)
    
    evaluator_km = ClusteringEvaluator(featuresCol="km_scaled_features", predictionCol="AI_Performance_Cluster")
    silhouette = evaluator_km.evaluate(df_km_out)
    print(f"[GOLD] K-Means Silhouette Score: {silhouette:.4f}")
    log["details"]["kmeans_silhouette_score"] = silhouette

    # Semantic Label Mapping
    centers = model_km.clusterCenters()
    cluster_prod = [(i, centers[i][1]) for i in range(3)]
    cluster_prod.sort(key=lambda x: x[1])
    c0, c1, c2 = cluster_prod[0][0], cluster_prod[1][0], cluster_prod[2][0]
    
    df_km_mapped = df_km_out.withColumn(
        "AI_Performance_Label",
        when(col("AI_Performance_Cluster") == c0, "Low Performer")
        .when(col("AI_Performance_Cluster") == c1, "Average Performer")
        .when(col("AI_Performance_Cluster") == c2, "High Performer")
        .otherwise("Unknown")
    )

    # =========================================================================
    # 2. Supervised: Logistic Regression (Hyperparameter Tuned + Full Metrics)
    # =========================================================================
    indexer = StringIndexer(inputCol="Productivity_Category", outputCol="label")
    df_lr_prep = indexer.fit(df_km_mapped).transform(df_km_mapped)
    
    # Safe features (No Data Leakage from Clustering)
    features_lr = [
        "Context_Awareness_Score", "Response_Time_Seconds", 
        "Task_Complexity_Score", "Memory_Per_Message_MB", "CPU_Utilization_Percent"
    ]
    df_lr_prep = df_lr_prep.fillna(0.0, subset=features_lr)
    
    assembler_lr = VectorAssembler(inputCols=features_lr, outputCol="lr_features")
    df_lr_vec = assembler_lr.transform(df_lr_prep)
    
    train_df, test_df = df_lr_vec.randomSplit([0.8, 0.2], seed=42)
    
    lr = LogisticRegression(featuresCol="lr_features", labelCol="label")
    paramGrid = ParamGridBuilder() \
        .addGrid(lr.regParam, [0.1, 0.05]) \
        .addGrid(lr.elasticNetParam, [0.0, 0.5]) \
        .build()
        
    evaluator_acc = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
    cv = CrossValidator(estimator=lr, estimatorParamMaps=paramGrid, evaluator=evaluator_acc, numFolds=3)
    cv_model = cv.fit(train_df)
    
    predictions = cv_model.transform(test_df)
    
    # Comprehensive Evaluation Metrics
    accuracy = evaluator_acc.evaluate(predictions)
    f1 = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1").evaluate(predictions)
    precision = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedPrecision").evaluate(predictions)
    recall = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedRecall").evaluate(predictions)
    
    print(f"[GOLD] LR Metrics -> Accuracy: {accuracy:.4f} | F1: {f1:.4f} | Precision: {precision:.4f} | Recall: {recall:.4f}")
    log["details"]["lr_metrics"] = {"accuracy": accuracy, "f1_score": f1, "precision": precision, "recall": recall}

    # Save Best Model Artifact
    best_model_path = os.path.join(MODEL_DIR, "lr_productivity_model")
    cv_model.bestModel.write().overwrite().save(best_model_path)
    print(f"[GOLD] Best LR model exported to {best_model_path}")

    # =========================================================================
    # 3. Save Final Analytical Marts
    # =========================================================================
    enriched_out = os.path.join(OUTPUT_DIR, 'ai_enriched_agentic_leadership')
    df_km_mapped.drop("km_raw_features", "km_scaled_features").write.mode("overwrite").parquet(enriched_out)
    
    df_industry = df_km_mapped.groupBy("Industry").agg(
        spark_round(avg("Task_Success_Rate"), 2).alias("Avg_Success_Rate"),
        spark_round(avg("Productivity_Improvement_Percent"), 2).alias("Avg_Productivity_Imprv"),
        spark_round(avg("Industry_Citation_Avg"), 2).alias("Research_Citation_Avg"), # NEW
        spark_round(avg("Trust_vs_Benchmark_Gap"), 2).alias("Trust_Gap"),
        count("Record_ID").alias("Total_Deployments")
    ).orderBy(col("Avg_Productivity_Imprv").desc())
    df_industry.write.mode("overwrite").parquet(os.path.join(OUTPUT_DIR, 'industry_ai_summary'))
    
    log["status"] = "completed"

except Exception as e:
    log["status"] = "failed"
    log["error"] = str(e)
    raise

finally:
    log_path = os.path.join(LOG_DIR, f'gold_run_{run_id}.json')
    with open(log_path, 'w') as f:
        json.dump(log, f, indent=2, default=str)
    spark.stop()
