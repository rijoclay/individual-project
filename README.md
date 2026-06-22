# Individual Project: AI Customer Support Agent

An end-to-end Data Engineering pipeline and AI integration project for my university coursework. This project builds an intelligent conversational agent that understands product data and answers customer inquiries dynamically.

## Overview

This system ingests raw product data and customer logs, processes them through a Medallion Architecture (Bronze → Silver → Gold), and leverages an AI model to handle customer queries based on the refined dataset. The goal is to automate customer support while maintaining accurate, context-aware responses.

## Architecture

- **Bronze Layer**: Raw data ingestion (JSON/CSV) into Parquet format.
- **Silver Layer**: Data cleaning, schema enforcement, and deduplication.
- **Gold Layer**: Aggregated business-level data and ML features ready for the AI agent.

## Tech Stack

- **Core Engine**: Apache Spark (PySpark)
- **Language**: Python
- **Storage**: Parquet (Snappy compressed)
- **ML & AI**: K-Means Clustering (User Profiling) & Logistic Regression

## Execution

To run the entire pipeline from raw data to Gold layer:

```bash
python 02_Scripts/run_spark_pipeline.py
```
