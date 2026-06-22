# Data Engineering Pipeline: Agentic AI Leadership

Ini adalah repository untuk Individual Project 2 (Data Engineering). Project ini membangun pipeline data end-to-end pakai PySpark dengan konsep Medallion Architecture (Bronze, Silver, Gold) untuk menganalisis impact Agentic AI terhadap produktivitas leadership di berbagai industri.

## Struktur Folder

- **01_Input**: Dataset mentah (CSV dari main dataset, JSON untuk benchmarks & OpenAlex papers, execution logs).
- **02_Scripts**: Kumpulan script Python & PySpark buat jalanin ETL, Machine Learning, dan generate report/diagram.
- **03_Output_Bronze**: Layer raw data yang di-ingest ke format Parquet.
- **04_Output_Silver**: Layer data yang udah dibersihin, deduplikasi, dan schema-enforced.
- **05_Output_Gold**: Layer agregasi siap pakai dan data hasil model Machine Learning.
- **06_Visualization**: Output grafik & diagram (ERD, Arsitektur ETL, K-Means profile).
- **07_Reports**: Laporan akhir format DOCX (Proposal, Paper, Final Report).
- **08_Logs**: Tracking execution log tiap kali pipeline jalan.
- **08_Reference**: Output HTML interaktif buat diagram.

## Tech Stack

- **Core**: Apache Spark (PySpark), Python.
- **Machine Learning**: K-Means Clustering, Logistic Regression.
- **Storage**: Parquet (Snappy compression).

## Model Performance

Pipeline ini juga melatih model ML di layer Gold:
- **K-Means Clustering**: Silhouette Score = 0.5276
- **Logistic Regression**: Accuracy = 55.44% (F1-Score = 46.59%)

## Cara Run

Untuk ngejalanin full pipeline dari Bronze sampai Gold, cukup run master script ini:

```bash
python 02_Scripts/run_spark_pipeline.py
```
