import re

SCRIPT = r"C:\Users\richa\Documents\Sem.6\DatEng_Individual_Project\individual_project_2\02_Scripts\generate_template_proposal.py"

with open(SCRIPT, 'r', encoding='utf-8') as f:
    code = f.read()

# =================== EN ABSTRACT ===================
old_abstract_en = '''add_normal_para(doc,
        "This proposal outlines the engineering of a distributed and scalable data pipeline designed to evaluate "
        "the performance and trustworthiness of Agentic AI systems within modern enterprises. As organizations "
        "in the professional services sector increasingly rely on autonomous AI agents for mission-critical tasks, "
        "a critical gap has emerged: decision-makers lack reliable, unified metrics to assess the reliability and "
        "productivity of these systems. The proposed solution addresses this challenge by constructing a Medallion "
        "architecture pipeline within the Data Lakehouse paradigm using Apache Spark. Four heterogeneous data "
        "sources are integrated: a primary operational dataset stored in CSV format containing 5,500 organizational "
        "records, external industry benchmarks in JSON, system execution logs in CSV, and academic citation data "
        "sourced via the OpenAlex API. Each source undergoes rigorous schema mapping, data quality checks, and "
        "industry-specific imputation in the Silver processing layer. A regex-based Natural Language Processing "
        "classifier contextualizes OpenAlex paper citations by mapping them directly to relevant business "
        "sectors. Advanced machine learning models are deployed in the Gold layer, comprising an unsupervised "
        "K-Means clustering algorithm validated with a Silhouette score of 0.5276, and a tuned multiclass "
        "Logistic Regression classifier producing an accuracy of 56.01%. Data leakage is prevented by "
        "isolating clustering features from classification inputs. The final optimized model is serialised "
        "and exported as a production-ready artifact. This fully automated pipeline delivers meaningful "
        "performance profiles that enable leadership teams to base strategic AI adoption decisions on "
        "quantitative, validated data rather than subjective assessments.")'''

new_abstract_en = '''add_normal_para(doc,
        "We built a data pipeline to measure how well Agentic AI systems perform in real companies. "
        "Decision-makers need hard numbers to trust AI agents, but existing data is scattered and inconsistent. "
        "Using Apache Spark, we constructed a Medallion pipeline (Bronze, Silver, Gold) that integrates four "
        "data sources: a CSV dataset (5,500 company records), industry benchmarks (JSON), system logs (CSV), "
        "and academic data from the OpenAlex API. The Silver layer runs schema validation, median-based imputation "
        "per industry, and a regex NLP classifier that maps OpenAlex papers to business sectors. The Gold layer "
        "deploys two ML models: unsupervised K-Means clustering (Silhouette score 0.5276) and a tuned multiclass "
        "Logistic Regression (accuracy 56.01%, F1 50.29%). We isolated clustering features from classification "
        "features to prevent data leakage. The final model is exported as a production-ready artifact. The pipeline "
        "gives leadership teams quantitative, validated performance profiles instead of subjective estimates.")'''

assert old_abstract_en in code, "Abstract EN not found"
code = code.replace(old_abstract_en, new_abstract_en)

# =================== EN INTRODUCTION - paragraph 1 ===================
old_p1 = '''add_normal_para(doc,
        "The rapid advancement of artificial intelligence over the past decade has fundamentally changed the "
        "way businesses operate across nearly every industrial sector. One of the most transformative developments "
        "in this area is the emergence of Agentic AI\u2014autonomous software systems that can independently plan, "
        "execute, and adapt while carrying out complex, multi-step tasks in dynamic environments. Unlike "
        "traditional rule-based automation, which strictly follows predefined scripts, Agentic AI agents "
        "leverage large language models and reinforcement learning to reason about their tasks, interact "
        "with external systems and application programming interfaces, and adjust their behaviour based on "
        "real-time feedback and contextual signals. These systems are now being deployed in high-stakes "
        "environments such as customer service management, supply chain coordination, financial auditing, "
        "and enterprise IT operations. Their ability to operate autonomously and at scale makes them "
        "extremely valuable assets for organisations seeking to reduce operational costs, accelerate "
        "decision-making, and maintain competitive advantage.")'''

new_p1 = '''add_normal_para(doc,
        "Agentic AI is changing how businesses operate. Unlike rule-based bots that just follow scripts, "
        "these systems plan, use tools, and adapt on their own. Companies deploy them for customer service, "
        "supply chains, and IT operations\u2014cutting costs and speeding up decisions. But here\u2019s the catch: "
        "nobody has a solid way to measure if they are actually delivering.")'''

assert old_p1 in code, "Intro P1 EN not found"
code = code.replace(old_p1, new_p1)

# =================== EN INTRODUCTION - paragraph 2 ===================
old_p2 = '''add_normal_para(doc,
        "However, the adoption of Agentic AI also presents significant governance and measurement "
        "challenges. Business leaders and technical managers need reliable, quantitative evidence to "
        "evaluate whether these autonomous agents are performing as expected, operating within safety "
        "parameters, and delivering measurable productivity gains. Unfortunately, the operational "
        "telemetry generated by these agents is usually fragmented across multiple heterogeneous systems. "
        "Performance metrics exist in isolated application logs stored as unstructured text files, "
        "organizational metadata is held in structured CSV exports from enterprise portals, and "
        "additional contextual data\u2014such as industry benchmarks and academic research\u2014resides in "
        "external databases and public APIs. Without a centralised data engineering pipeline that can "
        "ingest, clean, integrate, and analyse these disparate sources, organisations are forced to "
        "evaluate AI systems based on incomplete, siloed, and often inconsistent information. This "
        "limits the ability of decision-makers to compare results, detect anomalies, and understand "
        "the full picture of AI performance across their organisation.")'''

new_p2 = '''add_normal_para(doc,
        "The problem is the data is scattered. System logs live in text files. Company metrics are in "
        "CSVs sitting on someone\u2019s laptop. Industry benchmarks are behind APIs. Academic research is "
        "on OpenAlex. Without a pipeline that actually combines these sources, managers end up making "
        "decisions on gut feeling\u2014not real numbers. That is the gap this project addresses.")'''

assert old_p2 in code, "Intro P2 EN not found"
code = code.replace(old_p2, new_p2)

# =================== EN INTRODUCTION - paragraph 3 (closing) ===================
old_p3 = '''add_normal_para(doc,
        "This project directly addresses the measurement gap described above. The primary contribution "
        "is the design and implementation of an automated, end-to-end data pipeline that transforms raw, "
        "fragmented telemetry data into structured, analysable performance profiles for Agentic AI "
        "leadership. Built on Apache Spark and following the Medallion data architecture pattern, "
        "the pipeline processes four distinct data sources through a three-layer transformation "
        "workflow. The Bronze layer ingests raw files in their native formats while preserving audit "
        "metadata. The Silver layer performs cleansing operations\u2014including deduplication, type casting, "
        "industry-specific null imputation, efficiency metric derivation, and NLP-based contextual "
        "mapping of scientific citations\u2014to produce a clean, unified dataset. The Gold layer applies "
        "advanced machine learning algorithms to generate predictive insights and performance "
        "classifications. The final outcomes are designed to provide business leaders with reliable, "
        "data-backed profiles that support strategic decisions regarding AI adoption and investment.")'''

new_p3 = '''add_normal_para(doc,
        "This project closes that gap. We built a Spark-based Medallion pipeline that turns messy, "
        "scattered logs into clean performance profiles. Bronze layer stores raw data as-is. Silver "
        "layer cleans it\u2014drops duplicates, fills missing values per industry, maps academic papers "
        "to business sectors using NLP. Gold layer runs the ML: K-Means to find performance clusters, "
        "Logistic Regression to predict productivity. The output? Actionable numbers leadership can "
        "actually trust.")'''

assert old_p3 in code, "Intro P3 EN not found"
code = code.replace(old_p3, new_p3)

# =================== EN LITERATURE REVIEW ===================
old_lr1 = '''add_normal_para(doc,
        "A data pipeline is the foundational architecture that automates the end-to-end process of "
        "extracting data from source systems, transforming it through cleansing and enrichment "
        "operations, and loading it into target storage repositories for analysis. In enterprise "
        "environments, data pipelines are essential for handling the diversity, volume, and velocity "
        "of operational data generated by modern applications. Historically, organisations relied on "
        "relational Data Warehouses, which offer strong transactional guarantees and query performance "
        "but are expensive to scale and poorly suited for semi-structured or unstructured data. On the "
        "other end of the spectrum, Data Lakes provide cost-effective storage for raw data in its "
        "native format but lack ACID transaction support and suffer from performance degradation when "
        "queried directly. The Data Lakehouse architecture emerged as a response to these limitations, "
        "combining the schema enforcement and transaction management of a warehouse with the flexible "
        "storage model of a data lake. Lakehouse implementations typically use open columnar formats "
        "such as Apache Parquet to store data on cloud object storage, while leveraging query engines "
        "like Apache Spark to provide transactional operations, schema evolution, and direct machine "
        "learning capabilities on the stored data [1].")'''

new_lr1 = '''add_normal_para(doc,
        "Data pipelines are the backbone of enterprise analytics. They move data from source systems, "
        "clean it, and load it into storage for analysis. Old-school Data Warehouses enforce schemas "
        "and support transactions but cost a fortune to scale and choke on unstructured data. Data Lakes "
        "are cheap and flexible but lack ACID guarantees and query performance. The Data Lakehouse "
        "splits the difference: Parquet-formatted data on cheap storage, queried by Spark for both "
        "SQL and ML workloads. It is the model this project follows [1].")'''

assert old_lr1 in code, "LR P1 EN not found"
code = code.replace(old_lr1, new_lr1)

old_lr2 = '''add_normal_para(doc,
        "Three previous studies provide the theoretical foundation and methodological guidance for "
        "this project. First, the seminal work by Armbrust et al. (2021) introduced the Lakehouse "
        "concept and demonstrated through empirical analysis that organisations adopting this "
        "architecture can significantly reduce data duplication and pipeline complexity while "
        "maintaining a single source of truth for both business intelligence dashboards and advanced "
        "machine learning workloads [1]. Second, Zaharia et al. (2016) established Apache Spark as "
        "a unified analytics engine for large-scale data processing, showing that its distributed "
        "in-memory computation model achieves high throughput and low latency for complex join "
        "operations on massive datasets\u2014exactly the requirement for integrating heterogeneous "
        "telemetry logs from multiple Agentic AI sources [2]. Third, recent research in AI governance "
        "and trustworthiness has highlighted the need for empirical frameworks that combine operational "
        "execution telemetry with external validation baselines, including scientific citation metrics "
        "from databases such as OpenAlex, to establish confidence in autonomous agent decision-making "
        "processes [3]. These studies collectively justify the architectural choices and methodological "
        "approach adopted in this project.")'''

new_lr2 = '''add_normal_para(doc,
        "Three key studies frame this work. Armbrust et al. (2021) showed that Lakehouse architecture "
        "cuts data duplication and keeps a single source of truth for both dashboards and ML [1]. "
        "Zaharia et al. (2016) proved that Spark\u2019s in-memory processing handles complex joins across "
        "massive datasets\u2014exactly what we need for integrating scattered Agentic AI logs [2]. Recent "
        "AI governance research stresses that combining system logs with external baselines (like "
        "OpenAlex citations) is essential for measuring trust in autonomous agents [3]. These three "
        "papers define our architectural choices.")'''

assert old_lr2 in code, "LR P2 EN not found"
code = code.replace(old_lr2, new_lr2)

# =================== EN METHODOLOGY INTRO ===================
old_meth1 = '''add_normal_para(doc,
        "The methodology section describes the systematic approach used to design, develop, and validate "
        "the proposed data engineering pipeline. A well-defined methodology is essential for ensuring "
        "that the project deliverables align with the stated objectives, meet academic and professional "
        "standards, and are reproducible in other organisational contexts. This chapter covers the "
        "selection and justification of the overall project framework, the identification and description "
        "of the four data sources used as inputs, the procedures for data ingestion and cleansing, the "
        "storage architecture and rationale, and the integration of artificial intelligence algorithms "
        "within the processing workflow. Each component is explained with sufficient technical depth "
        "to allow a reader to understand both the high-level design decisions and the specific "
        "implementation details that make the pipeline robust, scalable, and production-ready.")'''

new_meth1 = '''add_normal_para(doc,
        "This section explains how we designed, built, and validated the pipeline. A clear methodology "
        "keeps the project focused, replicable, and aligned with the objectives. We cover the project "
        "framework, four data sources, how data is ingested and cleaned, our storage choices, and the "
        "ML models that run in the Gold layer.")'''

assert old_meth1 in code, "Meth intro P1 EN not found"
code = code.replace(old_meth1, new_meth1)

old_meth2 = '''add_normal_para(doc,
        "The engineering approach follows the Medallion Architecture pattern, which organises data "
        "processing into three progressively refined layers. The Bronze layer serves as the landing "
        "zone where raw data is ingested with full fidelity and minimal transformation. The Silver "
        "layer performs cleansing, quality assurance, and integration operations to produce a "
        "consistent and reliable dataset. The Gold layer aggregates the cleansed data and applies "
        "analytical and machine learning models to generate business-level insights and predictions. "
        "This architectural pattern is widely adopted in industry because it provides clear separation "
        "of concerns, enables incremental data quality improvement, and supports both batch and "
        "streaming ingestion patterns within a single framework. The following subsections detail "
        "each aspect of the methodology, beginning with the selection of CRISP-DM as the overarching "
        "project management framework.")'''

new_meth2 = '''add_normal_para(doc,
        "We use the Medallion pattern: Bronze stores raw data unchanged, Silver cleans and integrates, "
        "Gold runs analysis and ML. It is the industry standard\u2014clean separation, incremental "
        "improvements, and batch or streaming support. The overall project is managed using CRISP-DM.")'''

assert old_meth2 in code, "Meth intro P2 EN not found"
code = code.replace(old_meth2, new_meth2)


# ================== INDONESIAN VERSIONS ==================

# =================== ID ABSTRACT ===================
old_abstrak = '''add_normal_para(doc,
        "Proposal ini menguraikan rekayasa pipeline data terdistribusi dan terukur yang dirancang "
        "untuk mengevaluasi kinerja dan kepercayaan sistem Agentic AI di perusahaan modern. Seiring "
        "dengan semakin bergantungnya organisasi di sektor jasa profesional pada agen AI otonom "
        "untuk tugas-tugas kritikal, telah muncul kesenjangan kritis: para pengambil keputusan tidak "
        "memiliki metrik terpadu yang andal untuk menilai keandalan dan produktivitas sistem ini. "
        "Solusi yang diusulkan mengatasi tantangan ini dengan membangun pipeline arsitektur Medallion "
        "dalam paradigma Data Lakehouse menggunakan Apache Spark. Empat sumber data heterogen "
        "diintegrasikan: dataset operasional utama dalam format CSV berisi 5.500 catatan organisasi, "
        "tolok ukur industri eksternal dalam JSON, log eksekusi sistem dalam CSV, dan data kutipan "
        "akademik dari API OpenAlex. Setiap sumber mengalami pemetaan skema yang ketat, pemeriksaan "
        "kualitas data, dan imputasi spesifik industri di lapisan pemrosesan Silver. Classifier "
        "NLP berbasis regex mengontekstualisasikan kutipan makalah OpenAlex dengan memetakannya "
        "langsung ke sektor bisnis yang relevan. Model pembelajaran mesin canggih diterapkan di "
        "lapisan Gold, terdiri dari algoritma klasterisasi K-Means tanpa pengawasan yang divalidasi "
        "dengan skor Silhouette 0,5276, dan classifier Regresi Logistik multikelas yang di-tune "
        "dengan akurasi 56,01%. Data leakage dicegah dengan mengisolasi fitur klasterisasi dari "
        "input klasifikasi. Model akhir yang dioptimalkan diserialisasi dan diekspor sebagai "
        "artefak siap produksi. Pipeline otomatis ini memberikan profil kinerja yang bermakna "
        "yang memungkinkan tim kepemimpinan mendasarkan keputusan strategis adopsi AI pada data "
        "kuantitatif yang tervalidasi.")'''

new_abstrak = '''add_normal_para(doc,
        "Kami membangun pipeline data untuk mengukur kinerja sistem Agentic AI di perusahaan. "
        "Pengambil keputusan butuh angka pasti, tapi data yang ada tersebar dan tidak konsisten. "
        "Dengan Apache Spark, kami membuat pipeline Medallion (Bronze, Silver, Gold) yang "
        "mengintegrasikan 4 sumber: dataset CSV (5.500 data perusahaan), tolok ukur industri "
        "(JSON), log sistem (CSV), dan data akademik dari API OpenAlex. Layer Silver menjalankan "
        "validasi skema, imputasi median per industri, dan classifier NLP berbasis regex yang "
        "memetakan paper OpenAlex ke sektor bisnis. Layer Gold menggunakan dua model ML: K-Means "
        "clustering (skor Silhouette 0,5276) dan Regresi Logistik (akurasi 56,01%, F1 50,29%). "
        "Kami memisahkan fitur clustering dari fitur klasifikasi untuk mencegah data leakage. "
        "Model akhir diekspor sebagai artefak siap produksi, memberikan profil kinerja kuantitatif "
        "bagi tim kepemimpinan.")'''

assert old_abstrak in code, "Abstrak ID not found"
code = code.replace(old_abstrak, new_abstrak)

# =================== ID INTRODUCTION ===================
old_id_p1 = '''add_normal_para(doc,
        "Kemajuan pesat kecerdasan buatan selama satu dekade terakhir telah mengubah secara fundamental "
        "cara bisnis beroperasi di hampir setiap sektor industri. Salah satu perkembangan paling "
        "transformasional di bidang ini adalah munculnya Agentic AI\u2014sistem perangkat lunak otonom "
        "yang dapat secara mandiri merencanakan, mengeksekusi, dan beradaptasi sambil menjalankan "
        "tugas kompleks multi-langkah di lingkungan dinamis. Tidak seperti otomatisasi berbasis aturan "
        "tradisional yang mengikuti skrip yang telah ditentukan secara ketat, agen Agentic AI "
        "memanfaatkan model bahasa besar dan pembelajaran penguatan untuk bernalar tentang tugas "
        "mereka, berinteraksi dengan sistem eksternal dan API, serta menyesuaikan perilaku mereka "
        "berdasarkan umpan balik real-time dan sinyal kontekstual. Sistem ini kini diterapkan di "
        "lingkungan berisiko tinggi seperti manajemen layanan pelanggan, koordinasi rantai pasok, "
        "audit keuangan, dan operasi TI perusahaan. Kemampuan mereka untuk beroperasi secara otonom "
        "dan dalam skala besar menjadikannya aset yang sangat berharga bagi organisasi yang ingin "
        "mengurangi biaya operasional, mempercepat pengambilan keputusan, dan mempertahankan "
        "keunggulan kompetitif.")'''

new_id_p1 = '''add_normal_para(doc,
        "Agentic AI mengubah cara perusahaan bekerja. Berbeda dengan bot berbasis aturan yang cuma "
        "ngikutin skrip, sistem ini bisa merencanakan, pakai tools, dan beradaptasi sendiri. "
        "Perusahaan sekarang pakai Agentic AI untuk layanan pelanggan, rantai pasok, dan operasi TI\u2014"
        "ngurangin biaya dan mempercepat keputusan. Tapi masalahnya: belum ada cara yang solid untuk "
        "ngukur apakah mereka benar-benar bekerja.")'''

assert old_id_p1 in code, "Intro P1 ID not found"
code = code.replace(old_id_p1, new_id_p1)

old_id_p2 = '''add_normal_para(doc,
        "Namun, adopsi Agentic AI juga menghadirkan tantangan tata kelola dan pengukuran yang "
        "signifikan. Pemimpin bisnis dan manajer teknis membutuhkan bukti kuantitatif yang andal "
        "untuk mengevaluasi apakah agen otonom ini berkinerja sesuai harapan, beroperasi dalam "
        "parameter keamanan, dan memberikan peningkatan produktivitas yang terukur. Sayangnya, "
        "telemetri operasional yang dihasilkan oleh agen-agen ini biasanya terfragmentasi di "
        "berbagai sistem yang heterogen. Metrik kinerja ada dalam log aplikasi terisolasi yang "
        "disimpan sebagai file teks tidak terstruktur, metadata organisasi disimpan dalam ekspor "
        "CSV terstruktur dari portal perusahaan, dan data kontekstual tambahan\u2014seperti tolok ukur "
        "industri dan penelitian akademis\u2014berada di database eksternal dan API publik. Tanpa "
        "pipeline rekayasa data terpusat yang dapat mengumpulkan, membersihkan, mengintegrasikan, "
        "dan menganalisis sumber-sumber yang berbeda ini, organisasi terpaksa mengevaluasi sistem "
        "AI berdasarkan informasi yang tidak lengkap, terisolasi, dan seringkali tidak konsisten. "
        "Hal ini membatasi kemampuan pengambil keputusan untuk membandingkan hasil, mendeteksi "
        "anomali, dan memahami gambaran lengkap kinerja AI di seluruh organisasi mereka.")'''

new_id_p2 = '''add_normal_para(doc,
        "Masalahnya ada di data yang berserakan. Log sistem ada di file teks. Metrik perusahaan "
        "ada di CSV. Tolok ukur industri ada di API. Riset akademik ada di OpenAlex. Tanpa pipeline "
        "yang benar-benar menggabungkan sumber-sumber ini, manajer terpaksa membuat keputusan "
        "berdasarkan feeling\u2014bukan data. Itulah celah yang diperbaiki oleh proyek ini.")'''

assert old_id_p2 in code, "Intro P2 ID not found"
code = code.replace(old_id_p2, new_id_p2)

old_id_p3 = '''add_normal_para(doc,
        "Proyek ini secara langsung mengatasi kesenjangan pengukuran yang dijelaskan di atas. "
        "Kontribusi utama adalah desain dan implementasi pipeline data otomatis ujung-ke-ujung "
        "yang mengubah data telemetri mentah dan terfragmentasi menjadi profil kinerja terstruktur "
        "dan dapat dianalisis untuk kepemimpinan Agentic AI. Dibangun di atas Apache Spark dan "
        "mengikuti pola arsitektur data Medallion, pipeline ini memproses empat sumber data yang "
        "berbeda melalui alur kerja transformasi tiga lapis. Lapisan Bronze mengumpulkan file "
        "mentah dalam format aslinya sambil mempertahankan metadata audit. Lapisan Silver "
        "melakukan operasi pembersihan\u2014termasuk deduplikasi, konversi tipe, imputasi null spesifik "
        "industri, derivasi metrik efisiensi, dan pemetaan kontekstual kutipan ilmiah berbasis "
        "NLP\u2014untuk menghasilkan dataset yang bersih dan terpadu. Lapisan Gold menerapkan algoritma "
        "pembelajaran mesin canggih untuk menghasilkan wawasan prediktif dan klasifikasi kinerja. "
        "Hasil akhir dirancang untuk memberikan para pemimpin bisnis profil yang andal dan "
        "berbasis data yang mendukung keputusan strategis mengenai adopsi dan investasi AI.")'''

new_id_p3 = '''add_normal_para(doc,
        "Proyek ini menutup celah itu. Kami membangun pipeline Medallion berbasis Spark yang "
        "mengubah data kotor dan berserakan jadi profil kinerja yang rapi. Layer Bronze nyimpen "
        "data mentah. Layer Silver bersihin\u2014buang duplikat, isi nilai kosong per industri, "
        "petakan paper akademik ke sektor bisnis pakai NLP. Layer Gold jalanin ML: K-Means buat "
        "cari klaster kinerja, Regresi Logistik buat prediksi produktivitas. Hasilnya? Angka "
        "nyata yang bisa dipercaya sama pimpinan.")'''

assert old_id_p3 in code, "Intro P3 ID not found"
code = code.replace(old_id_p3, new_id_p3)

# =================== ID LITERATURE REVIEW ===================
old_id_lr1 = '''add_normal_para(doc,
        "Pipeline data adalah arsitektur dasar yang mengotomatiskan proses ujung-ke-ujung dari "
        "ekstraksi data dari sistem sumber, transformasi melalui operasi pembersihan dan "
        "pengayaan, dan pemuatan ke repositori penyimpanan target untuk analisis. Di lingkungan "
        "perusahaan, pipeline data sangat penting untuk menangani keragaman, volume, dan kecepatan "
        "data operasional yang dihasilkan oleh aplikasi modern. Secara historis, organisasi "
        "mengandalkan Gudang Data relasional, yang menawarkan jaminan transaksional yang kuat "
        "dan kinerja kueri tetapi mahal untuk diskalakan dan kurang cocok untuk data "
        "semi-terstruktur atau tidak terstruktur. Di sisi lain, Danau Data menyediakan "
        "penyimpanan hemat biaya untuk data mentah dalam format aslinya tetapi tidak memiliki "
        "dukungan transaksi ACID dan mengalami penurunan kinerja saat di-kueri secara langsung. "
        "Arsitektur Data Lakehouse muncul sebagai respons terhadap keterbatasan ini, menggabungkan "
        "penegakan skema dan manajemen transaksi gudang data dengan model penyimpanan fleksibel "
        "danau data. Implementasi Lakehouse biasanya menggunakan format kolom terbuka seperti "
        "Apache Parquet untuk menyimpan data di penyimpanan objek cloud, sambil memanfaatkan "
        "mesin kueri seperti Apache Spark untuk menyediakan operasi transaksional, evolusi skema, "
        "dan kemampuan pembelajaran mesin langsung pada data yang disimpan [1].")'''

new_id_lr1 = '''add_normal_para(doc,
        "Pipeline data adalah tulang punggung analitik perusahaan. Data dipindahkan dari sumber, "
        "dibersihkan, lalu dimuat ke penyimpanan untuk dianalisis. Data Warehouse lama punya skema "
        "ketat dan transaksi kuat tapi mahal dan sulit dipakai buat data tidak terstruktur. "
        "Data Lake murah dan fleksibel tapi tidak punya jaminan transaksi ACID. Data Lakehouse "
        "menggabungkan keduanya: data disimpan di Parquet di atas penyimpanan murah, lalu "
        "di-query pakai Spark baik untuk SQL maupun ML. Itulah model yang dipakai proyek ini [1].")'''

assert old_id_lr1 in code, "LR P1 ID not found"
code = code.replace(old_id_lr1, new_id_lr1)

old_id_lr2 = '''add_normal_para(doc,
        "Tiga penelitian sebelumnya memberikan landasan teoretis dan panduan metodologis untuk "
        "proyek ini. Pertama, karya seminal oleh Armbrust et al. (2021) memperkenalkan konsep "
        "Lakehouse dan menunjukkan melalui analisis empiris bahwa organisasi yang mengadopsi "
        "arsitektur ini dapat secara signifikan mengurangi duplikasi data dan kompleksitas "
        "pipeline sambil mempertahankan satu sumber kebenaran untuk dasbor intelijen bisnis "
        "dan beban kerja pembelajaran mesin canggih [1]. Kedua, Zaharia et al. (2016) menetapkan "
        "Apache Spark sebagai mesin analitik terpadu untuk pemrosesan data skala besar, "
        "menunjukkan bahwa model komputasi memori terdistribusinya mencapai throughput tinggi "
        "dan latensi rendah untuk operasi join kompleks pada dataset besar\u2014persis seperti yang "
        "dibutuhkan untuk mengintegrasikan log telemetri heterogen dari beberapa sumber Agentic "
        "AI [2]. Ketiga, penelitian terbaru dalam tata kelola AI dan kepercayaan telah menyoroti "
        "kebutuhan akan kerangka empiris yang menggabungkan telemetri eksekusi operasional dengan "
        "tolok ukur validasi eksternal, termasuk metrik kutipan ilmiah dari database seperti "
        "OpenAlex, untuk membangun keyakinan dalam proses pengambilan keputusan agen otonom [3]. "
        "Studi-studi ini secara kolektif membenarkan pilihan arsitektural dan pendekatan "
        "metodologis yang diadopsi dalam proyek ini.")'''

new_id_lr2 = '''add_normal_para(doc,
        "Tiga studi utama jadi acuan kami. Armbrust et al. (2021) menunjukkan bahwa arsitektur "
        "Lakehouse mengurangi duplikasi data dan menjaga satu sumber kebenaran untuk dasbor "
        "dan ML [1]. Zaharia et al. (2016) membuktikan bahwa pemrosesan in-memory Spark "
        "menangani join kompleks di dataset besar\u2014tepat yang kami butuhkan untuk menyatukan "
        "log Agentic AI yang tersebar [2]. Riset tata kelola AI terbaru menekankan bahwa "
        "menggabungkan log sistem dengan data eksternal (seperti kutipan OpenAlex) sangat "
        "penting untuk mengukur kepercayaan pada agen otonom [3]. Ketiga paper ini mendefinisikan "
        "pilihan arsitektural kami.")'''

assert old_id_lr2 in code, "LR P2 ID not found"
code = code.replace(old_id_lr2, new_id_lr2)

# =================== ID METHODOLOGY INTRO ===================
old_id_meth1 = '''add_normal_para(doc,
        "Bagian metodologi menjelaskan pendekatan sistematis yang digunakan untuk merancang, "
        "mengembangkan, dan memvalidasi pipeline rekayasa data yang diusulkan. Metodologi yang "
        "terdefinisi dengan baik sangat penting untuk memastikan bahwa hasil proyek selaras "
        "dengan tujuan yang dinyatakan, memenuhi standar akademik dan profesional, serta dapat "
        "direproduksi dalam konteks organisasi lain. Bab ini mencakup pemilihan dan justifikasi "
        "kerangka kerja proyek secara keseluruhan, identifikasi dan deskripsi empat sumber data "
        "yang digunakan sebagai input, prosedur untuk ingesti dan pembersihan data, arsitektur "
        "penyimpanan dan alasannya, serta integrasi algoritma kecerdasan buatan dalam alur kerja "
        "pemrosesan. Setiap komponen dijelaskan dengan kedalaman teknis yang cukup untuk "
        "memungkinkan pembaca memahami baik keputusan desain tingkat tinggi maupun detail "
        "implementasi spesifik yang membuat pipeline ini tangguh, terukur, dan siap produksi.")'''

new_id_meth1 = '''add_normal_para(doc,
        "Bagian ini menjelaskan bagaimana kami merancang, membangun, dan memvalidasi pipeline. "
        "Metodologi yang jelas membuat proyek tetap fokus, bisa direproduksi, dan selaras dengan "
        "tujuan. Kami bahas kerangka proyek, empat sumber data, cara data diingesti dan "
        "dibersihkan, pilihan penyimpanan, dan model ML yang berjalan di layer Gold.")'''

assert old_id_meth1 in code, "Meth intro P1 ID not found"
code = code.replace(old_id_meth1, new_id_meth1)

old_id_meth2 = '''add_normal_para(doc,
        "Pendekatan rekayasa mengikuti pola Arsitektur Medallion, yang mengatur pemrosesan "
        "data ke dalam tiga lapisan yang disempurnakan secara progresif. Lapisan Bronze berfungsi "
        "sebagai zona pendaratan di mana data mentah diingesti dengan fidelitas penuh dan "
        "transformasi minimal. Lapisan Silver melakukan pembersihan, jaminan kualitas, dan "
        "operasi integrasi untuk menghasilkan dataset yang konsisten dan andal. Lapisan Gold "
        "mengagregasi data yang telah dibersihkan dan menerapkan model analitis dan pembelajaran "
        "mesin untuk menghasilkan wawasan dan prediksi tingkat bisnis. Pola arsitektural ini "
        "diadopsi secara luas di industri karena menyediakan pemisahan kepentingan yang jelas, "
        "memungkinkan peningkatan kualitas data secara bertahap, dan mendukung pola ingesti "
        "batch dan streaming dalam satu kerangka kerja. Sub-bagian berikut merinci setiap "
        "aspek metodologi, dimulai dengan pemilihan CRISP-DM sebagai kerangka manajemen proyek "
        "secara keseluruhan.")'''

new_id_meth2 = '''add_normal_para(doc,
        "Kami pakai pola Medallion: Bronze nyimpen data mentah apa adanya, Silver membersihkan "
        "dan mengintegrasikan, Gold menjalankan analisis dan ML. Ini standar industri\u2014pisah "
        "bersih, perbaikan bertahap, bisa batch maupun streaming. Proyek dikelola pakai CRISP-DM.")'''

assert old_id_meth2 in code, "Meth intro P2 ID not found"
code = code.replace(old_id_meth2, new_id_meth2)

# Write back
with open(SCRIPT, 'w', encoding='utf-8') as f:
    f.write(code)

print("All humanize rewrites applied successfully.")
print(f"File size: {len(code)} chars")
