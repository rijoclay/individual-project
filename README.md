# Individual Project — Agentic AI Leadership

A Data Engineering project analyzing **Agentic AI in Leadership** using PySpark medallion architecture (Bronze → Silver → Gold).

## Overview

This project builds an end-to-end data pipeline to explore how Agentic AI transforms leadership across industries. The pipeline ingests data from multiple sources, cleans and enriches it, then generates analytics-ready outputs for clustering and industry analysis.

## Project Structure

```
├── 01_Input/                        Raw datasets
│   ├── AgenticAI_Leadership_Dataset_v1.csv
│   ├── agent_execution_logs.csv
│   ├── external_leadership_benchmarks.json
│   └── openalex_ai_leadership_papers.json
│
├── 02_Scripts/                      PySpark pipeline scripts
│   ├── bronze_layer.py              Raw → Cleaned data
│   ├── silver_layer.py              Cleaned → Enriched data
│   ├── gold_layer.py                Enriched → Analytics-ready data
│   ├── run_spark_pipeline.py        Pipeline runner
│   └── test_pipeline.py             Pipeline tests
│
├── 08_Reference/                    Planned architecture diagrams
│   ├── architecture_diagram.html    Full system architecture
│   ├── etl_architecture.png         ETL flow diagram
│   └── gantt_chart.png              Project timeline
│
├── 07_Reports/
│   └── Richard_Clay_Proposal.docx   Project proposal (EN)
│
└── README.md
```

## Data Sources

| Source | Format | Description |
|--------|--------|-------------|
| AgenticAI_Leadership_Dataset_v1.csv | CSV | Main dataset (1,500+ records, 11 industries) |
| agent_execution_logs.csv | CSV | AI agent execution logs |
| external_leadership_benchmarks.json | JSON | External leadership benchmark data |
| openalex_ai_leadership_papers.json | JSON | OpenAlex research papers on AI leadership |

## Pipeline Architecture

```
Raw Data (CSV/JSON/Logs)
       │
       ▼
   ┌─────────┐
   │ BRONZE  │  Clean, validate, deduplicate
   └────┬────┘
        │
        ▼
   ┌─────────┐
   │ SILVER  │  Enrich, transform, standardize
   └────┬────┘
        │
        ▼
   ┌─────────┐
   │  GOLD   │  Analytics-ready outputs, ML models
   └─────────┘
```

## Methodology

1. **Data Collection** — Ingest multi-source data (CSV, JSON, logs, OpenAlex API)
2. **Bronze Layer** — Remove duplicates, handle missing values, validate schema
3. **Silver Layer** — Enrich with industry tags, standardize columns, join datasets
4. **Gold Layer** — Generate analytics outputs, train clustering models (K-Means, Logistic Regression)

## Requirements

- Python 3.10+
- Apache Spark / PySpark
- Java 11+ (Spark dependency)

## Timeline

- **23–24 Jun 2026** — Proposal submission
- **9–10 Jul 2026** — Paper submission
- **13 Jul 2026** — Final report
- **15 Jul 2026** — Demo & presentation
