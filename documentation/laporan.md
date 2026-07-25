# Laporan: Perancangan dan Implementasi Dashboard Universitas

## A. Penentuan Kebutuhan

### 1. Pengguna Utama

Pengguna utama dashboard adalah **pihak rektorat**, khususnya pimpinan universitas dan unit penjaminan mutu. Rektorat membutuhkan informasi tingkat tinggi untuk memantau kualitas layanan akademik dan pengalaman mahasiswa.

Dalam proyek ini, seluruh responden diposisikan sebagai mahasiswa dari satu universitas simulasi. Kolom negara menggambarkan asal mahasiswa; nama universitas pada dataset tidak digunakan dalam analisis.

### 2. Kebutuhan Informasi

Pihak rektorat membutuhkan informasi yang dapat membantu evaluasi pengalaman dan tingkat kepuasan mahasiswa, antara lain:

1. Jumlah mahasiswa yang menjadi responden survei.
2. Distribusi tingkat kepuasan (sangat puas hingga sangat tidak puas) serta proporsi Puas / Netral / Tidak Puas.
3. Rata-rata penilaian kualitas pengajaran dan fasilitas kampus (skala 1–5).
4. Perbandingan kepuasan antar bidang studi untuk menemukan kelompok yang perlu perhatian.
5. Perbandingan pengalaman berdasarkan jenjang pendidikan, status beasiswa, dan kelas daring.
6. Gambaran proporsi ketidakpuasan menurut negara asal mahasiswa.
7. Pola deskriptif antara rating pengajaran/fasilitas dengan kepuasan keseluruhan.

Informasi tersebut digunakan sebagai dasar awal pengambilan keputusan strategis, bukan sebagai bukti hubungan sebab-akibat.

## B. Perancangan Dashboard

### 1. Indikator yang Ditampilkan

| Indikator | Bentuk tampilan |
|-----------|-----------------|
| Total responden | KPI |
| Proporsi mahasiswa Puas / Netral / Tidak Puas | KPI |
| Rata-rata kualitas pengajaran | KPI |
| Rata-rata fasilitas kampus | KPI |
| Distribusi lima tingkat kepuasan | Bar chart |
| Proporsi tidak puas per negara asal | Choropleth map + bar chart |
| Distribusi kepuasan per bidang studi | Stacked bar chart |
| Rating pengajaran & fasilitas per bidang studi | Grouped bar chart |
| Pengajaran / fasilitas vs kepuasan | Heatmap |
| Kelas daring vs non-daring | Stacked bar chart |
| Beasiswa vs non-beasiswa | Stacked bar chart |
| Data detail responden | Tabel + unduh CSV |

Alur dashboard: **kondisi umum → kelompok bermasalah → faktor terkait → perbandingan pengalaman → data detail**.

### 2. Sumber Data

Data berasal dari **World University Student Survey Dataset** (Kaggle). Dataset bersifat sintetis dan dipilih agar proyek tetap realistis tanpa memakai data internal universitas yang bersifat rahasia.

File data:

```text
data/world_university_survey_dataset.csv
```

## C. Implementasi Teknis

Dashboard dikembangkan dengan **Python** dan **Streamlit**. Pandas digunakan untuk pengolahan data; Plotly untuk visualisasi interaktif.

### Komponen utama

- **≥2 jenis visualisasi:** bar chart, stacked bar, heatmap, dan peta (choropleth).
- **≥1 komponen interaktif:** filter multiselect untuk bidang studi, tahun studi, kelas daring, beasiswa, jenjang pendidikan, negara asal, dan jenis kelamin; tombol reset filter.
- KPI ringkasan yang ikut berubah mengikuti filter.
- Tabel detail dan unduh CSV hasil filter.

### Cara menjalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

## D. Publikasi Proyek

Kode program, dataset, `requirements.txt`, dan `README.md` diunggah ke GitHub. README menjelaskan cara menjalankan proyek, struktur folder, sumber data, dan fitur dashboard.

Dokumentasi lengkap kebutuhan dan narasi desain tersedia di folder `documentation/`.

### Tautan dashboard online

https://25917045-analyticbigdata.streamlit.app/

### Tautan repository

https://github.com/Dffarhn2004/dashboard-analitic-big-data
