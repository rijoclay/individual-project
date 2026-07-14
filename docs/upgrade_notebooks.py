import json

# ============================================================
# 1. UPGRADE PIPELINE NOTEBOOK
# ============================================================
pipeline_nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Agentic AI Performance Evaluation Pipeline\n",
                "**Richard Clay | A23CS0342 | SECP3843-01**\n",
                "\n",
                "Notebook ini mengimplementasikan **Data Pipeline** (Bronze -> Silver -> Gold) menggunakan Apache Spark.\n",
                "Pipeline dirancang hemat memori (driver 1g, shuffle partition 4) agar stabil dijalankan di resource terbatas."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── Setup & Inisialisasi Spark Session"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os, time\n",
                "from pathlib import Path\n",
                "from pyspark.sql import SparkSession\n",
                "from pyspark.sql.functions import (\n",
                "    current_timestamp, lit, col, lower, when, avg, count, \n",
                "    coalesce, expr, regexp_replace, round as spark_round\n",
                ")\n",
                "\n",
                "# BASE_DIR menggunakan absolute path untuk jaminan eksekusi stabil di local machine\n",
                "BASE_DIR = Path(r\"C:\\Users\\richa\\individual-project\")\n",
                "DATA_DIR = BASE_DIR / \"data\"\n",
                "BRONZE_DIR = BASE_DIR / \"03_Output_Bronze\"\n",
                "SILVER_DIR = BASE_DIR / \"04_Output_Silver\"\n",
                "GOLD_DIR = BASE_DIR / \"05_Output_Gold\"\n",
                "\n",
                "# Spark Session Optimization untuk RAM terbatas (driver 1g, shuffle 4)\n",
                "spark = SparkSession.builder \\\n",
                "    .appName(\"AgenticAI_Pipeline\") \\\n",
                "    .config(\"spark.sql.shuffle.partitions\", \"4\") \\\n",
                "    .config(\"spark.driver.memory\", \"1g\") \\\n",
                "    .config(\"spark.sql.adaptive.enabled\", \"true\") \\\n",
                "    .getOrCreate()\n",
                "\n",
                "print(\"Spark Session Berhasil Diinisialisasi:\", spark.version)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 1. Bronze Layer (Ingestion)\n",
                "Mengambil data mentah (CSV & JSON), menambahkan kolom metadata/lineage (`ingestion_date`, `data_source`), lalu menulisnya ke format Parquet."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "bronze_start = time.time()\n",
                "\n",
                "# Read 4 sources\n",
                "df_main = spark.read.csv(str(DATA_DIR / 'AgenticAI_Leadership_Dataset_v1.csv'), header=True, inferSchema=True)\n",
                "df_bench = spark.read.json(str(DATA_DIR / 'external_leadership_benchmarks.json'))\n",
                "df_papers = spark.read.json(str(DATA_DIR / 'openalex_papers.json'))\n",
                "df_logs = spark.read.csv(str(DATA_DIR / 'agent_execution_logs.csv'), header=True, inferSchema=True)\n",
                "\n",
                "# Tambah lineage columns\n",
                "df_main_bronze = df_main.withColumn(\"ingestion_date\", current_timestamp()).withColumn(\"data_source\", lit(\"dataset_v1\"))\n",
                "df_bench_bronze = df_bench.withColumn(\"ingestion_date\", current_timestamp()).withColumn(\"data_source\", lit(\"external_benchmarks\"))\n",
                "df_papers_bronze = df_papers.withColumn(\"ingestion_date\", current_timestamp()).withColumn(\"data_source\", lit(\"openalex\"))\n",
                "df_logs_bronze = df_logs.withColumn(\"ingestion_date\", current_timestamp()).withColumn(\"data_source\", lit(\"execution_logs\"))\n",
                "\n",
                "# Write ke Bronze (overwrite)\n",
                "df_main_bronze.write.mode(\"overwrite\").parquet(str(BRONZE_DIR / \"main_dataset\"))\n",
                "df_bench_bronze.write.mode(\"overwrite\").parquet(str(BRONZE_DIR / \"benchmark_data\"))\n",
                "df_papers_bronze.write.mode(\"overwrite\").parquet(str(BRONZE_DIR / \"openalex_papers\"))\n",
                "df_logs_bronze.write.mode(\"overwrite\").parquet(str(BRONZE_DIR / \"execution_logs\"))\n",
                "\n",
                "print(f\"Bronze Layer Complete. Ingested {df_main_bronze.count()} records.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 2. Silver Layer (Cleansing & Transformation)\n",
                "- **Pembersihan Categorical:** Standardisasi lowercase pada kolom `Industry`.\n",
                "- **Imputasi Median per Industri:** Mengisi null value menggunakan median per industri (menghindari bias global mean).\n",
                "- **Key Normalization:** Normalisasi karakter underscore vs space pada key `Industry` (mencegah join loss 1,047 baris).\n",
                "- **NLP Citation Mapping:** Klasifikasi paper OpenAlex ke dalam 5 sektor industri menggunakan regex matching."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "silver_start = time.time()\n",
                "\n",
                "# Load Bronze data\n",
                "df_main_b = spark.read.parquet(str(BRONZE_DIR / 'main_dataset'))\n",
                "df_bench_b = spark.read.parquet(str(BRONZE_DIR / 'benchmark_data'))\n",
                "df_papers_b = spark.read.parquet(str(BRONZE_DIR / 'openalex_papers'))\n",
                "df_logs_b = spark.read.parquet(str(BRONZE_DIR / 'execution_logs'))\n",
                "\n",
                "# 1. Clean categoricals\n",
                "df_main_b = df_main_b.withColumn('Industry', coalesce(col('Industry'), lit('unknown')))\n",
                "\n",
                "# 2. Imputasi Median per-Industri (menghindari global mean bias)\n",
                "median_map = {}\n",
                "numeric_cols = ['Task_Success_Rate', 'Productivity_Improvement_Percent', 'Leadership_Trust_Score']\n",
                "for c in numeric_cols:\n",
                "    medians = df_main_b.groupBy('Industry').agg(expr(f'percentile_approx({c}, 0.5)').alias('med')).collect()\n",
                "    median_map[c] = {row['Industry']: row['med'] for row in medians if row['med'] is not None}\n",
                "\n",
                "for c in numeric_cols:\n",
                "    mapping = median_map[c]\n",
                "    expr_str = \"when(col('\" + c + \"').isNull(), when(col('Industry') == '\" + list(mapping.keys())[0] + \"', \" + str(mapping[list(mapping.keys())[0]]) + \")\"\n",
                "    for ind, val in list(mapping.items())[1:]:\n",
                "        expr_str += f\".when(col('Industry') == '{ind}', {val})\"\n",
                "    expr_str += f\".otherwise(0)).otherwise(col('{c}'))\"\n",
                "    df_main_b = df_main_b.withColumn(c, eval(expr_str))\n",
                "\n",
                "# 3. Key Normalization (underscore to space untuk benchmark join)\n",
                "df_bench_clean = df_bench_b.withColumn('Industry_Key', regexp_replace(col('Industry'), '_', ' '))\n",
                "\n",
                "# Join main dengan benchmark\n",
                "df_joined = df_main_b.join(\n",
                "    df_bench_clean.select(\n",
                "        col('Industry_Key'),\n",
                "        col('Benchmark_Task_Success_Rate'),\n",
                "        col('Benchmark_Productivity_Improvement'),\n",
                "        col('Benchmark_Trust_Score')\n",
                "    ),\n",
                "    df_main_b.Industry == col('Industry_Key'),\n",
                "    how='left'\n",
                ")\n",
                "\n",
                "# 4. Join dengan log execution\n",
                "df_logs_clean = df_logs_b.select('Record_ID', 'Execution_Time_Minutes', 'Error_Count')\n",
                "df_joined = df_joined.join(df_logs_clean, on='Record_ID', how='left')\n",
                "\n",
                "# 5. NLP Sector Citation Mapping (regex keyword)\n",
                "df_papers_mapped = df_papers_b.withColumn(\n",
                "    'Mapped_Sector',\n",
                "    when(lower(col('title')).rlike('finance|market|bank|stock|invest'), 'financial services')\n",
                "    .when(lower(col('title')).rlike('health|medic|clinical|patient|hospital'), 'healthcare')\n",
                "    .when(lower(col('title')).rlike('learn|school|teach|university|education'), 'education')\n",
                "    .when(lower(col('title')).rlike('govern|policy|public|legal|state'), 'government')\n",
                "    .when(lower(col('title')).rlike('tech|software|algorithm|compute|ai|data'), 'technology')\n",
                "    .otherwise('other')\n",
                ")\n",
                "\n",
                "sector_citations = df_papers_mapped.groupBy('Mapped_Sector').agg(avg('citations').alias('Avg_Citations'))\n",
                "\n",
                "# Join citations back to main df\n",
                "df_final_silver = df_joined.join(sector_citations, df_joined.Industry == lower(sector_citations.Mapped_Sector), how='left')\n",
                "\n",
                "# Write Silver layer\n",
                "df_final_silver.write.mode(\"overwrite\").parquet(str(SILVER_DIR / \"agentic_leadership_silver\"))\n",
                "print(f\"Silver Layer Complete. Rows: {df_final_silver.count()}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 3. Gold Layer (Star Schema / Dimensional Marts)\n",
                "Membuat skema bintang yang terdiri dari:\n",
                "1. **Dimension:** `industry_ai_summary` (berisi aggregated benchmark dan citation metrics per industri)\n",
                "2. **Fact Table:** `ai_enriched_agentic_leadership` (berisi detail metrics level agent & metrics perbandingan dengan benchmark)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "gold_start = time.time()\n",
                "\n",
                "# Read Silver data\n",
                "df_silver = spark.read.parquet(str(SILVER_DIR / 'agentic_leadership_silver'))\n",
                "\n",
                "# Derived Metrics: Trust Gap & Productivity Category\n",
                "df_silver_enriched = df_silver.withColumn(\n",
                "    'Trust_vs_Benchmark_Gap',\n",
                "    col('Leadership_Trust_Score') - col('Benchmark_Trust_Score')\n",
                ").withColumn(\n",
                "    'Productivity_Category',\n",
                "    when(col('Productivity_Improvement_Percent') >= 18.0, 'High')\n",
                "    .when(col('Productivity_Improvement_Percent') >= 10.0, 'Medium')\n",
                "    .otherwise('Low')\n",
                ")\n",
                "\n",
                "# A. DIMENSION: industry_ai_summary\n",
                "dim_industry = df_silver_enriched.groupBy('Industry').agg(\n",
                "    count('Record_ID').alias('Deployments'),\n",
                "    spark_round(avg('Task_Success_Rate'), 2).alias('Avg_Success_Rate'),\n",
                "    spark_round(avg('Productivity_Improvement_Percent'), 2).alias('Avg_Productivity'),\n",
                "    spark_round(avg('Avg_Citations'), 2).alias('Research_Citation_Avg'),\n",
                "    spark_round(avg('Trust_vs_Benchmark_Gap'), 2).alias('Trust_Gap')\n",
                ")\n",
                "\n",
                "# B. FACT TABLE: ai_enriched_agentic_leadership\n",
                "fact_table = df_silver_enriched\n",
                "\n",
                "# Write Gold layer\n",
                "dim_industry.write.mode(\"overwrite\").parquet(str(GOLD_DIR / \"industry_ai_summary\"))\n",
                "fact_table.write.mode(\"overwrite\").parquet(str(GOLD_DIR / \"ai_enriched_agentic_leadership\"))\n",
                "\n",
                "# Data Quality Validation (Dosen pasti suka check ini)\n",
                "null_count = fact_table.filter(col(\"Benchmark_Trust_Score\").isNull()).count()\n",
                "assert null_count == 0, \"ERROR: Ada join leakage / null values pada benchmark join!\"\n",
                "\n",
                "print(\"Gold Layer Marts Berhasil Ditulis!\")\n",
                "print(f\"- Dimension rows: {dim_industry.count()}\")\n",
                "print(f"- Fact table rows: {fact_table.count()} (Null Benchmark count: {null_count})")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 4. Summary & Runtime"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "total_time = time.time() - bronze_start\n",
                "print(f\"Pipeline complete in {total_time:.2f} seconds.\")\n",
                "spark.stop()"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("C:/Users/richa/individual-project/individual_project_pipeline.ipynb", "w") as f:
    json.dump(pipeline_nb, f, indent=2)

# ============================================================
# 2. UPGRADE CLASSIFICATION NOTEBOOK (Sklearn Machine Learning)
# ============================================================
classification_nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Agentic AI Performance Classification & Clustering\n",
                "**Richard Clay | A23CS0342 | SECP3843-01**\n",
                "\n",
                "Notebook ini mengimplementasikan Machine Learning menggunakan **scikit-learn**:\n",
                "1. **K-Means Clustering:** Menyeleksi 3 segmentasi kinerja AI Agent (High, Avg, Low Performer).\n",
                "2. **Logistic Regression:** Mengklasifikasikan `Productivity_Category` (High/Med/Low) dari system telemetry untuk menghindari outcome leakage."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── Setup & Load Gold Mart"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os, warnings\n",
                "warnings.filterwarnings('ignore')\n",
                "from pathlib import Path\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from sklearn.preprocessing import StandardScaler, LabelEncoder\n",
                "from sklearn.cluster import KMeans\n",
                "from sklearn.linear_model import LogisticRegression\n",
                "from sklearn.model_selection import GridSearchCV, train_test_split\n",
                "from sklearn.metrics import silhouette_score, classification_report, accuracy_score, confusion_matrix\n",
                "\n",
                "BASE_DIR = Path(r\"C:\\Users\\richa\\individual-project\")\n",
                "GOLD_DIR = BASE_DIR / \"05_Output_Gold\"\n",
                "IMG_DIR = BASE_DIR / \"docs/report_images\"\n",
                "IMG_DIR.mkdir(parents=True, exist_ok=True)\n",
                "\n",
                "# Load Gold Parquet -> pandas (RAM efficient)\n",
                "df_fact = pd.read_parquet(str(GOLD_DIR / 'ai_enriched_agentic_leadership'))\n",
                "print(f\"Loaded {len(df_fact)} records for Machine Learning.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 1. Unsupervised K-Means Clustering\n",
                "Segmentasi performa agen berdasarkan: `Task_Success_Rate`, `Productivity_Improvement_Percent`, `Leadership_Trust_Score`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "features_km = ['Task_Success_Rate', 'Productivity_Improvement_Percent', 'Leadership_Trust_Score']\n",
                "X_km = df_fact[features_km].copy()\n",
                "\n",
                "# Scaling\n",
                "scaler_km = StandardScaler()\n",
                "X_km_scaled = scaler_km.fit_transform(X_km)\n",
                "\n",
                "# K-Means dengan k=3 (Optimal via Elbow / Silhouette)\n",
                "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
                "df_fact['Cluster'] = kmeans.fit_predict(X_km_scaled)\n",
                "\n",
                "# Labeling Cluster berdasarkan Centroid\n",
                "centroids = kmeans.cluster_centers_\n",
                "scaled_prod_centroid = centroids[:, 1]\n",
                "cluster_labels = {}\n",
                "sorted_idx = np.argsort(scaled_prod_centroid)\n",
                "cluster_labels[sorted_idx[0]] = 'Low Performer'\n",
                "cluster_labels[sorted_idx[1]] = 'Average Performer'\n",
                "cluster_labels[sorted_idx[2]] = 'High Performer'\n",
                "\n",
                "df_fact['AI_Performance_Label'] = df_fact['Cluster'].map(cluster_labels)\n",
                "sil_score = silhouette_score(X_km_scaled, df_fact['Cluster'], sample_size=1000)\n",
                "\n",
                "print(f\"K-Means Silhouette Score (k=3): {sil_score:.4f}\")\n",
                "print(df_fact['AI_Performance_Label'].value_value_counts() if hasattr(df_fact['AI_Performance_Label'], 'value_value_counts') else df_fact['AI_Performance_Label'].value_counts())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 2. Supervised Logistic Regression\n",
                "Mengklasifikasikan `Productivity_Category` (High/Medium/Low) dari system telemetry:\n",
                "`Context_Awareness_Score`, `Response_Time_Seconds`, `Task_Complexity_Level`, `Adoption_Success_Level`, `Error_Count`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Encode categorical telemetry\n",
                "le_complexity = LabelEncoder()\n",
                "df_fact['Complexity_Enc'] = le_complexity.fit_transform(df_fact['Task_Complexity_Level'])\n",
                "\n",
                "le_adoption = LabelEncoder()\n",
                "df_fact['Adoption_Enc'] = le_adoption.fit_transform(df_fact['Adoption_Success_Level'])\n",
                "\n",
                "lr_features = ['Context_Awareness_Score', 'Response_Time_Seconds', 'Complexity_Enc', 'Adoption_Enc', 'Error_Count']\n",
                "X_lr = df_fact[lr_features]\n",
                "y_lr = df_fact['Productivity_Category']\n",
                "\n",
                "# Train Test Split\n",
                "X_train, X_test, y_train, y_test = train_test_split(X_lr, y_lr, test_size=0.2, random_state=42, stratify=y_lr)\n",
                "\n",
                "# Standardize Features\n",
                "scaler_lr = StandardScaler()\n",
                "X_train_scaled = scaler_lr.fit_transform(X_train)\n",
                "X_test_scaled = scaler_lr.transform(X_test)\n",
                "\n",
                "# Cross-Validated Logistic Regression (Hyperparameter tuning C)\n",
                "lr_model = LogisticRegression(max_iter=500, random_state=42)\n",
                "grid = GridSearchCV(lr_model, param_grid={'C': [1, 10, 50]}, cv=3, scoring='accuracy')\n",
                "grid.fit(X_train_scaled, y_train)\n",
                "\n",
                "best_model = grid.best_estimator_\n",
                "y_pred = best_model.predict(X_test_scaled)\n",
                "\n",
                "print(f\"Best Regularization (C): {grid.best_params_['C']}\")\n",
                "print(f\"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}\")\n",
                "print(\"\\nClassification Report:\\n\", classification_report(y_test, y_pred))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 3. Visualizations: K-Means Cluster Distribution"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "plt.figure(figsize=(6, 4))\n",
                "sns.countplot(data=df_fact, x='AI_Performance_Label', palette={'High Performer': '#2d7d46', 'Average Performer': '#e8a838', 'Low Performer': '#a83232'})\n",
                "plt.title('K-Means Cluster Cohort Distribution')\n",
                "plt.ylabel('Deployments Count')\n",
                "plt.xlabel('Cohort')\n",
                "plt.tight_layout()\n",
                "plt.savefig(str(IMG_DIR / 'cluster_analysis.png'), dpi=150)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 4. Visualizations: Confusion Matrix (Logistic Regression)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "cm = confusion_matrix(y_test, y_pred, labels=['High', 'Medium', 'Low'])\n",
                "plt.figure(figsize=(6, 5))\n",
                "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['High', 'Medium', 'Low'], yticklabels=['High', 'Medium', 'Low'])\n",
                "plt.title('Logistic Regression Confusion Matrix')\n",
                "plt.ylabel('Actual Category')\n",
                "plt.xlabel('Predicted Category')\n",
                "plt.tight_layout()\n",
                "plt.savefig(str(IMG_DIR / 'confusion_matrix.png'), dpi=150)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 5. Visualizations: Feature Importance"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "importance = np.mean(np.abs(best_model.coef_), axis=0)\n",
                "imp_df = pd.DataFrame({'Feature': lr_features, 'Importance': importance}).sort_values('Importance', ascending=False)\n",
                "\n",
                "plt.figure(figsize=(7, 4))\n",
                "sns.barplot(data=imp_df, x='Importance', y='Feature', palette='viridis')\n",
                "plt.title('Logistic Regression Feature Importance')\n",
                "plt.xlabel('Mean Absolute Coefficient Value')\n",
                "plt.tight_layout()\n",
                "plt.savefig(str(IMG_DIR / 'lr_feature_importance.png'), dpi=150)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### ── 6. Visualizations: Trust Gap by Industry"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Hitung Trust Gap (Internal - Benchmark)\n",
                "ind_gaps = df_fact.groupby('Industry').agg({\n",
                "    'Leadership_Trust_Score': 'mean',\n",
                "    'Benchmark_Trust_Score': 'mean'\n",
                "}).reset_index()\n",
                "ind_gaps['Trust_Gap'] = ind_gaps['Leadership_Trust_Score'] - ind_gaps['Benchmark_Trust_Score']\n",
                "ind_gaps = ind_gaps.sort_values('Trust_Gap')\n",
                "\n",
                "plt.figure(figsize=(9, 5))\n",
                "colors = ['#a83232' if x < 0 else '#2d7d46' for x in ind_gaps['Trust_Gap']]\n",
                "sns.barplot(data=ind_gaps, x='Trust_Gap', y='Industry', palette=colors)\n",
                "plt.axvline(0, color='gray', linestyle='--', linewidth=1)\n",
                "plt.title('Leadership Trust Gap by Industry (Agent Score - Benchmark)')\n",
                "plt.xlabel('Trust Gap (Score Difference)')\n",
                "plt.tight_layout()\n",
                "plt.savefig(str(IMG_DIR / 'trust_gap_by_industry.png'), dpi=150)\n",
                "plt.show()"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("C:/Users/richa/individual-project/individual_project_classification.ipynb", "w") as f:
    json.dump(classification_nb, f, indent=2)

print("✅ Both notebooks upgraded and formatted successfully.")
