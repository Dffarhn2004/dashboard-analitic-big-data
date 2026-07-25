# Dashboard Evaluasi Pengalaman dan Kepuasan Mahasiswa

Dashboard interaktif berbasis **Streamlit** untuk membantu pihak rektorat memantau tingkat kepuasan mahasiswa, menilai kualitas pengajaran dan fasilitas kampus, serta mengidentifikasi kelompok mahasiswa yang memerlukan perhatian.

## Pengguna Utama

Pengguna utama dashboard adalah **pihak rektorat dan pimpinan universitas**.

Dashboard digunakan untuk:

- Memantau distribusi tingkat kepuasan mahasiswa.
- Membandingkan proporsi ketidakpuasan antar bidang studi.
- Melihat penilaian kualitas pengajaran dan fasilitas kampus.
- Membandingkan pengalaman kelas daring vs non-daring.
- Membandingkan pengalaman penerima vs nonpenerima beasiswa.
- Melihat proporsi ketidakpuasan berdasarkan negara asal mahasiswa.

## Fitur

- Filter interaktif (bidang studi, tahun studi, kelas daring, beasiswa, jenjang, negara, gender).
- KPI total responden, proporsi puas/netral/tidak puas, serta rata-rata rating.
- Bar chart distribusi tingkat kepuasan.
- Peta proporsi mahasiswa tidak puas menurut negara asal.
- Stacked bar kepuasan per bidang studi.
- Heatmap kualitas pengajaran / fasilitas vs kepuasan.
- Perbandingan pengalaman kelas daring dan status beasiswa.
- Tabel data detail.
- Unduh data hasil filter dalam format CSV.

## Sumber Data

Proyek ini menggunakan **World University Student Survey Dataset** (Kaggle, data sintetis). Seluruh responden diperlakukan sebagai mahasiswa dari satu universitas simulasi. Data disimpan pada:

```text
data/world_university_survey_dataset.csv
```

## Struktur Proyek

```text
dashboard-universitas/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── world_university_survey_dataset.csv
└── documentation/
    ├── laporan.md
    ├── prd.md
    └── narasi.md
```

## Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/Dffarhn2004/dashboard-analitic-big-data.git
cd dashboard-analitic-big-data
```

### 2. Buat virtual environment

```bash
python -m venv venv
```

Aktifkan virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependency

```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka melalui browser pada alamat:

```text
http://localhost:8501
```

## Publikasi

Dashboard dipublikasikan melalui Streamlit Community Cloud. Dokumentasi laporan (bagian A–D tugas) tersedia di folder `documentation/`.

### Dashboard online

```text
https://25917045-analyticbigdata.streamlit.app/
```

## Tautan Repository

```text
https://github.com/Dffarhn2004/dashboard-analitic-big-data
```
