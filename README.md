# Data Engineering Individual Project

A Data Engineering project proposal outlining an end-to-end analytics pipeline using PySpark medallion architecture (Bronze → Silver → Gold).

## Overview

This repository contains the proposal phase of the project. The planned data pipeline will ingest multi-source data, clean and enrich it, and ultimately generate analytics-ready outputs.

## Project Structure

```
├── data/                            Sample & raw datasets (for proposal context)
│   ├── AgenticAI_Leadership_Dataset_v1.csv
│   ├── agent_execution_logs.csv
│   ├── external_leadership_benchmarks.json
│   └── openalex_ai_leadership_papers.json
│
├── src/                             Planned PySpark pipeline structure
│   ├── bronze_layer.py              Raw → Cleaned data
│   ├── silver_layer.py              Cleaned → Enriched data
│   ├── gold_layer.py                Enriched → Analytics-ready data
│   ├── run_spark_pipeline.py        Pipeline runner
│   └── test_pipeline.py             Pipeline tests
│
├── reference/                       Proposed Architecture & Timelines
│   ├── architecture_diagram.html    Proposed full system architecture
│   ├── etl_architecture.png         Proposed ETL flow diagram
│   └── gantt_chart.png              Proposed project timeline
│
├── docs/
│   └── Richard_Clay_Proposal.docx   Project proposal (EN)
│
└── README.md
```

## Planned Data Sources

| Source | Format | Description |
|--------|--------|-------------|
| AgenticAI_Leadership_Dataset_v1.csv | CSV | Main dataset for analysis |
| agent_execution_logs.csv | CSV | Execution log dataset |
| external_leadership_benchmarks.json | JSON | Benchmark dataset |
| openalex_ai_leadership_papers.json | JSON | Academic reference dataset |

## Planned Pipeline Architecture

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

## Proposed Methodology

1. **Data Collection** — Ingest multi-source data (CSV, JSON, logs, API references).
2. **Bronze Layer** — Remove duplicates, handle missing values, and validate schemas.
3. **Silver Layer** — Enrich and transform data, standardize columns, and join datasets.
4. **Gold Layer** — Generate analytics-ready outputs and evaluate models.

## Requirements

- Python 3.10+
- Apache Spark / PySpark
- Java 11+ (Spark dependency)

## Timeline

- **23–24 Jun 2026** — Proposal submission *(Current Phase)*
- **9–10 Jul 2026** — Paper submission
- **13 Jul 2026** — Final report
- **15 Jul 2026** — Demo & presentation
