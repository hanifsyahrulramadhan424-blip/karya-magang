# 📊 SIMAK-KUNINGAN: Sistem Informasi & Dashboard Analitik Terpadu

**Sistem Informasi Terpadu Analisis PDRB dan Kesejahteraan Sosial Kabupaten Kuningan (2015–2025)**  
*Proyek Laporan & Evaluasi Magang — Badan Pusat Statistik (BPS) Kabupaten Kuningan*

---

## 🌟 Ringkasan Proyek
**SIMAK-KUNINGAN** adalah platform dashboard analitik interaktif berbasis Python dan Streamlit yang mengintegrasikan data makroekonomi, struktur sektoral 17 lapangan usaha, profil kemiskinan multidimensi, analisis korelasi ekonometrika, *Machine Learning Clustering*, dan peramalan (*forecasting*) deret waktu indikator pembangunan daerah.

---

## 🚀 Fitur Utama Dashboard

### 📈 1. Tab 1: Struktur Makroekonomi & Sektoral
- **Dual-Scale Macro Chart:** Tren pertumbuhan PDRB Riil (ADHK 2010), PDRB Nominal (ADHB), dan Laju Pertumbuhan Ekonomi (LPE).
- **17 Sektor Treemap & Interaktif:** Pemetaan visual kontribusi ekonomi sektoral dengan interpretasi statistik BPS.
- **Top 5 Sektor Donut Chart:** Ringkasan kontribusi lima lapangan usaha terbesar.
- **Pengeluaran Riil & ICVAR Metric:** Evaluasi komponen pengeluaran dan variabilitas kapital sektoral.

### 👥 2. Tab 2: Profil Kemiskinan & Sosial Ketenagakerjaan
- **Indeks FGT Foster-Greer-Thorbecke ($P_0, P_1, P_2$):** Analisis persentase kemiskinan, kedalaman, dan keparahan kemiskinan.
- **Dinamika Garis Kemiskinan:** Analisis inflasi kebutuhan pangan vs non-pangan.
- **Struktur Ketenagakerjaan:** Proporsi tenaga kerja formal vs informal (>62% sektor informal sebagai penyangga ekonomi).
- **Dimensi Indeks Pembangunan Manusia (IPM):** Evaluasi agregat kesehatan (UHH), pendidikan (HLS, RLS), dan daya beli riil.

### 🔬 3. Tab 3: Analisis Silang, Korelasi & Elastisitas
- **Heatmap Korelasi Pearson:** Matriks korelasi makro-sosial dengan tanda signifikansi ($^{***}p < 0.001$).
- **Dynamic OLS Regression Engine:** Model regresi linier bebas $\hat{Y} = \beta_0 + \beta_1 X$ dengan scatter plot dan uji signifikansi.
- **Kalkulator Elastisitas Kemiskinan:** Pembuktian empiris pertumbuhan inklusif (*Pro-Poor Growth* dengan $\bar{\varepsilon} \approx -0.62$).

### 🔮 4. Tab 4: Klasterisasi ML & Proyeksi 2026–2030
- **Machine Learning K-Means Clustering ($k=2,3,4$):** Pengelompokan 17 lapangan usaha berdasarkan pangsa PDRB dan CAGR pertumbuhan tahunan.
- **Peta Kuadran Tipologi Klassen:** Pemetaan sektor prima, akselerator (*rising stars*), penunjang, dan tertinggal.
- **Peramalan Deret Waktu (2026–2030):** Model *Holt's Linear Exponential Smoothing* & *OLS Trend Regression* dilengkapi pita batas toleransi *95% Confidence Interval* serta uji akurasi MAPE & RMSE.
- **Interpretasi Analitis Dinamis:** Narasi kebijakan yang beradaptasi otomatis sesuai jumlah klaster ($k$) dan variabel yang dipilih.

---

## 📁 Struktur Direktori Repositori

```text
├── .streamlit/
│   └── config.toml          # Konfigurasi UI/Theme Streamlit
├── assets/
│   └── logo_bps.png         # Aset Logo BPS Kab. Kuningan
├── modules/
│   ├── __init__.py          # Init modul Python
│   ├── data_loader.py       # Ingesti data Excel & kalkulasi agregat
│   ├── ui_components.py     # Desain Glassmorphism CSS, banner & KPI cards
│   ├── tab1_makro.py        # Logika Tab 1 (Makroekonomi & Sektoral)
│   ├── tab2_kemiskinan.py   # Logika Tab 2 (Kemiskinan & Sosial)
│   ├── tab3_inferensial.py  # Logika Tab 3 (Korelasi & Regresi OLS)
│   ├── tab4_proyeksi_klaster.py # Logika Tab 4 (K-Means & Forecasting)
│   └── data_explorer.py     # Penampil data tabular & download CSV
├── PDRB_dan_Indikator_Sosial_Ekonomi_Kuningan_2015_2025_Final.xlsx # Dataset Utama
├── app.py                   # File Utama Aplikasi (Main Entrypoint)
├── requirements.txt         # Daftar dependensi library Python
├── .gitignore               # File pengabaian Git
└── README.md                # Dokumentasi Proyek
```

---

## 💻 Panduan Instalasi & Menjalankan Lokal

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/username/SIMAK-KUNINGAN.git
   cd SIMAK-KUNINGAN
   ```

2. **Buat & aktifkan Virtual Environment (Opsional tapi disarankan):**
   ```bash
   python -m venv venv
   # Di Windows:
   venv\Scripts\activate
   # Di Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependensi library:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi dashboard:**
   ```bash
   streamlit run app.py
   ```
   Aplikasi akan terbuka otomatis pada browser di `http://localhost:8501`.

---

## 🛠️ Teknologi yang Digunakan
- **Bahasa:** Python 3.10+
- **Framework Web:** [Streamlit](https://streamlit.io/)
- **Visualisasi Data:** [Plotly Graph Objects & Express](https://plotly.com/python/)
- **Manipulasi Data:** Pandas & NumPy
- **Analisis Statistik & ML:** SciPy, Scikit-Learn, Statsmodels
- **Pengolah Dataset:** OpenPyXL

---

## 👨‍💻 Kontributor & Lisensi
Dikembangkan untuk keperluan **Laporan & Penilaian Magang di Badan Pusat Statistik (BPS) Kabupaten Kuningan**.  
Data bersumber dari publikasi resmi BPS Kabupaten Kuningan (2015–2025).
