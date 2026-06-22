import unittest
import os
import json
import warnings
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

warnings.simplefilter('ignore', ResourceWarning)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = r'C:\Users\richa\spark'
if 'HADOOP_HOME' not in os.environ:
    os.environ['HADOOP_HOME'] = r'C:\Users\richa\hadoop'
if os.environ['SPARK_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['SPARK_HOME'] + r'\bin'

class TestIP2Pipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.appName("IP2_DQ_Testing").master("local[2]").getOrCreate()
            
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_01_input_files_exist(self):
        inputs = ['AgenticAI_Leadership_Dataset_v1.csv', 'external_leadership_benchmarks.json', 
                  'agent_execution_logs.csv', 'openalex_ai_leadership_papers.json']
        for f in inputs:
            self.assertTrue(os.path.exists(os.path.join(BASE_DIR, '01_Input', f)), f"Missing: {f}")

    def test_02_silver_data_quality_nulls(self):
        """10/10 Metric: Ensure zero null values in critical numerical columns after cleansing."""
        silver_path = os.path.join(BASE_DIR, '04_Output_Silver', 'agentic_leadership_silver')
        df = self.spark.read.parquet(silver_path)
        
        # Strict DQ Assertions
        null_tsr = df.filter(col("Task_Success_Rate").isNull()).count()
        null_lts = df.filter(col("Leadership_Trust_Score").isNull()).count()
        
        self.assertEqual(null_tsr, 0, f"Found {null_tsr} nulls in Task_Success_Rate (Imputation Failed)")
        self.assertEqual(null_lts, 0, f"Found {null_lts} nulls in Leadership_Trust_Score (Imputation Failed)")
        
        # NLP Feature verification
        self.assertTrue("Industry_Citation_Avg" in df.columns, "NLP Contextual Citation column missing")

    def test_03_gold_record_strict_count(self):
        """10/10 Metric: No records dropped during ML processing."""
        gold_enriched = os.path.join(BASE_DIR, '05_Output_Gold', 'ai_enriched_agentic_leadership')
        df = self.spark.read.parquet(gold_enriched)
        count = df.count()
        self.assertEqual(count, 5500, f"Data loss detected in Gold layer. Expected 5500, got {count}")

    def test_04_model_artifact_exported(self):
        """10/10 Metric: Ensure ML model is saved for production deployment."""
        model_path = os.path.join(BASE_DIR, '05_Output_Gold', 'models', 'lr_productivity_model')
        self.assertTrue(os.path.exists(model_path), "Logistic Regression model artifact not exported!")

if __name__ == '__main__':
    unittest.main()
