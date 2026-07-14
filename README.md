# Agentic AI Performance Evaluation Pipeline

Individual Project 2 (SECP3843-01) — Richard Clay (A23CS0342)
Supervisor: Dr. Aryati Binti Bakri

End-to-end analytics + machine learning pipeline built with **PySpark Medallion
Architecture** (Bronze → Silver → Gold). The full pipeline including K-Means
clustering and Logistic Regression classification runs in a single self-contained
notebook — no external modules required.

## Project Structure

```
├── data/                                   Raw multi-source datasets
│   ├── AgenticAI_Leadership_Dataset_v1.csv  Main leadership dataset
│   ├── agent_execution_logs.csv             Agent execution logs
│   ├── external_leadership_benchmarks.json  External benchmark data
│   └── openalex_ai_leadership_papers.json   Academic paper references
│
├── individual_project_pipeline.ipynb        SINGLE-FILE end-to-end pipeline
│                                             (Bronze → Silver → Gold + ML)
│
├── docs/
│   ├── Richard_Clay_Final_Report.docx       Final report (21 pages, EN)
│   ├── Richard_Clay_Proposal.docx           Project proposal (EN)
│   └── report_images/                       Figures used in the report
│
└── README.md
```

> Output directories (`03_Output_Bronze/`, `04_Output_Silver/`, `05_Output_Gold/`)
> are generated automatically when the notebook is executed.

## Data Sources

| Source | Format | Description |
|--------|--------|-------------|
| AgenticAI_Leadership_Dataset_v1.csv | CSV | Main agentic-AI leadership dataset |
| agent_execution_logs.csv | CSV | Per-agent execution / runtime logs |
| external_leadership_benchmarks.json | JSON | Industry benchmark scores |
| openalex_ai_leadership_papers.json | JSON | OpenAlex academic paper metadata |

## Pipeline Architecture

```
Raw Data (CSV / JSON / Logs)
        │
        ▼
   ┌─────────┐
   │ BRONZE  │  Ingest + schema validation → Parquet
   └────┬────┘
        │
        ▼
   ┌─────────┐
   │ SILVER  │  Dedup, median impute, join, NLP mapping → Enriched
   └────┬────┘
        │
        ▼
   ┌─────────┐
   │  GOLD   │  K-Means clustering + Logistic Regression + Star-Schema marts
   └─────────┘
```

## Star Schema (Gold Layer)

- **Fact table** — `ai_enriched_agentic_leadership` (one row per agent, all metrics)
- **Dimension table** — `ai_cluster_profile` (cluster-level aggregates + semantics)
- **Dimension table** — `industry_summary` (per-industry performance rollup)

## Machine Learning (Gold Layer)

- **K-Means** clustering (k=3) → semantic labels (Low / Average / High Performer)
  - Silhouette score: **0.5276**
- **Logistic Regression** (multiclass, 3-fold CrossValidator) on system-only
  features (no leakage) → performance-tier classification

## How to Run

1. Install dependencies: `pip install pyspark`
2. Open `individual_project_pipeline.ipynb` in Jupyter / VS Code
3. **Run All** — the notebook reads from `data/`, writes Parquet outputs to the
   `03/04/05_Output_*` folders, and prints layer timings + ML metrics.

> Spark is configured for low-memory machines (`driver.memory=1g`,
> `spark.sql.shuffle.partitions=4`, AQE enabled).

## Requirements

- Python 3.10+
- Apache Spark / PySpark
- Java 11+ (Spark dependency)

## Timeline

- **23–24 Jun 2026** — Proposal
- **9–10 Jul 2026** — Paper
- **13 Jul 2026** — Final report
- **15 Jul 2026** — Demo & presentation
