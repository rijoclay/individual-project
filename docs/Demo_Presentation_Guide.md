# Dokumentasi Code Cell — Persiapan Demo Presentasi
**Individual Project 2: Agentic AI Performance Evaluation Pipeline**
**Richard Clay | A23CS0342 | SECP3843-01**

---

## 📘 NOTEBOOK 1: `individual_project_pipeline.ipynb`
**Fokus:** Medallion Architecture (Bronze → Silver → Gold) — Data Engineering murni.

### Cell 1 — Title & Identitas
- Heading notebook, nama mahasiswa, supervisor, course code.

### Cell 2 — Setup & Inisialisasi Spark
- **Import library:** PySpark SQL, fungsi transformasi, Path handling.
- **Path config:** `BASE_DIR` di-hardcode ke `C:\Users\richa\individual-project` (biar gak error di environment manapun).
- **Buat folder output:** `03_Output_Bronze/`, `04_Output_Silver/`, `05_Output_Gold/`.
- **SparkSession:** `local[*]`, driver memory 1GB, shuffle partition 4, AQE on (hemat RAM di VPS 1.9GB).

### Cell 3 — BRONZE LAYER (Ingestion)
- Baca 4 sumber: Kaggle CSV (5,500 rows), OpenAlex JSON (paper), Benchmark JSON, Telemetry CSV.
- Tambah kolom `ingestion_date` & `data_source` buat tracking lineage.
- Simpan masing-masing ke Parquet di Bronze.
- **Output:** 4 folder Parquet.

### Cell 4 — SILVER LAYER (Cleansing & Integration)
- **Dedup:** `dropDuplicates(['Record_ID'])`.
- **Lowercase** semua kolom kategorikal (Industry, Agent_Type, dll) biar join gak case-sensitive.
- **Cast numerik** ke DoubleType.
- **Median imputation per-Industry:** kolom numerik yang null diisi median per sektor (bukan global mean → lebih akurat).
- **Join Benchmark:** FIX — `regexp_replace(Industry, '_', ' ')` buat normalisasi key (Financial_Services vs Financial Services). Ini nylametin 1,047 rows (19%) yang tadinya null.
- **Join Logs:** gabung execution telemetry (Execution_Time_Minutes, Error_Count).
- **NLP Mapping:** OpenAlex papers di-map ke 4 sektor (Financial, Healthcare, Education, Government, Technology) pakai regex title.
- **Derived columns:** `Productivity_Category` (low/medium/high), `Trust_vs_Benchmark_Gap`.
- **Write Silver:** 1 Parquet `agentic_leadership_silver` (5,500 records, 0 nulls di kolom kritis).

### Cell 5 — GOLD LAYER (Analytical Marts)
- **Dimension `industry_ai_summary`:** Agregasi per Industry (avg success, productivity, trust, trust gap, jumlah deployment) → 11 rows.
- **Fact `ai_enriched_agentic_leadership`:** Full dataset enriched → 5,500 rows.
- **Write Gold:** 2 Parquet. (Ini Star Schema: Dim + Fact).

### Cell 6 — Pipeline Summary
- Print total runtime (Bronze + Silver + Gold).
- `spark.stop()` — tutup session.

---

## 📗 NOTEBOOK 2: `individual_project_classification.ipynb`
**Fokus:** Machine Learning (Unsupervised + Supervised) — di-file terpisah biar dosen gampang nanya ML part.

### Cell 1 — Title & Identitas
- Heading, nama, supervisor, course.

### Cell 2 — Setup
- **Import:** pandas, numpy, matplotlib, seaborn, scikit-learn (KMeans, LogisticRegression, metrics, GridSearchCV), pyarrow.
- **Why sklearn?** PySpark ML di RAM 1.9GB sering OOM (Python worker crash). Scikit-learn di pandas jauh lebih ringan & stabil buat dataset 5,500 rows.
- **Path:** `GOLD_DIR` → baca dari `05_Output_Gold/`.

### Cell 3 — Load Gold Data
- Baca `ai_enriched_agentic_leadership.parquet` via `pyarrow` → pandas DataFrame.
- Print shape & columns buat verifikasi.

### Cell 4 — K-MEANS CLUSTERING (Unsupervised)
- **Features:** Task_Success_Rate, Productivity_Improvement_Percent, Leadership_Trust_Score.
- **StandardScaler:** normalize biar K-Means gak bias ke fitur dengan skala besar.
- **K-Means (k=3, seed=42):** bagi data jadi 3 cluster.
- **Silhouette Score:** 0.5218 (ukur kualitas cluster —semakin dekat 1, makin padat & terpisah).
- **Labeling:** cluster dikasih nama **Low / Average / High Performer** berdasarkan centroid productivity.
- **Centroid summary:** High Performer (Success 76.4, Prod 25.4, Trust 61.2), Average (73.8, 14.1, 57.6), Low (70.9, 7.3, 53.9).

### Cell 5 — LOGISTIC REGRESSION (Supervised)
- **Target:** `Productivity_Category` (low/medium/high) — 3-class classification.
- **Features (strict: system telemetry only):** Context_Awareness_Score, Response_Time_Seconds, Task_Complexity_Level, Adoption_Success_Level, Error_Count.
- **NO data leakage:** gak pakai kolom hasil (Task_Success_Rate) atau cluster label sebagai fitur.
- **LabelEncoder:** ubah kategori jadi angka.
- **Train/Test split:** 80/20 (seed=42).
- **GridSearchCV (3-fold):** cari `C` terbaik (regularization).
- **Metrics:**
  - Accuracy: **59.30%**
  - F1 (macro): **52.60%**
  - Precision (weighted): 40.34%
  - Recall (weighted): 52.60%
- **Confusion Matrix:** medium class paling susah diprediksi (F1=0.39).

### Cell 6 — VISUAL ANALYTICS (4 Charts)
- **Chart 1 — Cluster Distribution + Centroids:** Pie chart (43% High, 33% Low, 24% Avg) + bar centroids.
- **Chart 2 — Confusion Matrix:** Heatmap prediksi vs aktual.
- **Chart 3 — Trust Gap by Industry:** Bar horizontal, merah = gap negatif (trust < benchmark), hijau = positif.
  - Terburuk: Technology (-16.23), Logistics (-11.30), Financial Services (-11.39).
  - Terbaik: Government (+3.92, satu-satunya positif).
- **Chart 4 — LR Coefficients:** Bar per fitur per kelas. Context_Awareness & Task_Complexity paling dominan.
- **Save:** semua ke `docs/report_images/*.png` untuk dilampirkan di report.

---

## 🎤 TIPS PRESENTASI (Q&A Antisipasi)
| Pertanyaan Dosen | Jawaban Singkat |
|------------------|-----------------|
| "Kenapa pisah pipeline & classification?" | "Biobr data engineering (Spark) dari ML (sklearn) — arsitektur bersih, gampang di-debug, dan ML gak butuh Spark di RAM kecil." |
| "Akurasi 59% kok rendah?" | "Ini multiclass (3 kelas) dengan fitur sistem-saja (no leakage). Baseline random = 33%. Model capture pola nyata, bukan noise. Medium class yang sulit karena overlap." |
| "Benchmark join fix itu apa?" | "Awalnya Industry pakai underscore (Financial_Services) vs benchmark pakai spasi (Financial Services) → 19% rows ga ke-join. Diperbaiki pakai `regexp_replace` → 0 nulls." |
| "Kenapa sklearn bukan PySpark ML?" | "VPS RAM 1.9GB. PySpark Python worker sering OOM. Sklearn di pandas jauh lebih stabil untuk 5,500 rows." |
| "Trust gap negatif itu artinya?" | "Trust internal perusahaan LEBIH RENDAH dari benchmark industri → ada deficit kepercayaan terhadap AI agent." |

---

**File siap demo.** Jalankan urut: (1) pipeline dulu → (2) classification. Output visual otomatis masuk `docs/report_images/`.
