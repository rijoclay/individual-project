# Individual Project 2 — Data Engineering Pipeline

Tugas individu mata kuliah Data Engineering — proposal data pipeline yang menganalisis peran **Agentic AI** dalam mendukung kepemimpinan dan pengambilan keputusan di organisasi modern.

## Soal & Poin-Poin

### Task 1: Problem Identification
**Domain:** AI Agents for Business Leadership  
**Problem:** Agentic AI (sistem otonom yang mampu beradaptasi tanpa intervensi manusia) semakin digunakan untuk mendukung fungsi kepemimpinan. Perlu dipahami bagaimana efektivitasnya dalam decision-making, faktor yang mempengaruhi performa, dan kontribusinya terhadap produktivitas organisasi.

### Task 2: Objectives
1. Mengukur efektivitas AI agents dalam decision-making
2. Mengidentifikasi faktor kunci yang mempengaruhi performa AI agents
3. Menganalisis kontribusi AI agents terhadap leadership efficiency & organizational productivity

### Task 3: Methodology
- **Data Source:** Public dataset dari Kaggle (5,500 records)
- **Bronze Layer:** Raw data ingestion (CSV, JSON, logs) via PyArrow, + metadata (ingestion_date, data_source)
- **Silver Layer:** Cleaning, deduplikasi, imputasi missing values, standardisasi kategorikal, derived columns
- **Gold Layer:** Agregasi + ML (K-Means, Logistic Regression)
- **Storage:** Data Lakehouse (Parquet + Snappy)

### Task 4: System Architecture
ETL pipeline — Bronze → Silver → Gold. Setiap layer diproses dengan PySpark di lingkungan local.

### Task 5: Project Timeline
20 May 2026 – 10 July 2026

### Task 6: Documentation
Proposal, Paper, Final Report, dan Presentasi.

## Struktur Folder

- `01_Input/` — Dataset mentah (CSV, JSON, logs)
- `02_Scripts/` — Script ETL, ML, generate report
- `03_Output_Bronze/` — Data mentah dalam Parquet
- `04_Output_Silver/` — Data bersih, siap analisis
- `05_Output_Gold/` — Agregasi + model ML
- `06_Visualization/` — Grafik & diagram
- `07_Reports/` — Proposal, Paper, Final Report (.docx)
- `08_Logs/` — Execution logs
- `08_Reference/` — Diagram arsitektur

## Run Pipeline

```bash
python 02_Scripts/run_spark_pipeline.py
```
