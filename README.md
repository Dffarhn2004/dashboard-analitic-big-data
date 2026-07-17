# Dashboard Kinerja Universitas

Dashboard interaktif berbasis **Streamlit** untuk membantu pihak rektorat memantau indikator utama universitas, seperti jumlah mahasiswa aktif, jumlah lulusan, publikasi dosen, kelulusan tepat waktu, tingkat penyerapan lulusan, dan status akreditasi.

## Pengguna Utama

Pengguna utama dashboard adalah **pihak rektorat dan pimpinan universitas**.

Dashboard digunakan untuk:

- Memantau perkembangan jumlah mahasiswa.
- Membandingkan performa antar-fakultas.
- Melihat tren publikasi dosen.
- Mengevaluasi kelulusan tepat waktu.
- Memantau persentase lulusan yang telah bekerja.
- Melihat distribusi status akreditasi.

## Fitur

- Filter berdasarkan tahun.
- Filter berdasarkan fakultas.
- KPI jumlah mahasiswa, lulusan, publikasi, dan penyerapan lulusan.
- Bar chart mahasiswa aktif per fakultas.
- Line chart tren publikasi dosen.
- Grafik kelulusan tepat waktu.
- Pie chart distribusi akreditasi.
- Tabel data detail.
- Unduh data hasil filter dalam format CSV.

## Sumber Data

Proyek ini menggunakan **data simulasi** untuk tahun 2021–2026. Data disimpan pada:

```text
data/university_data.csv
```

## Struktur Proyek

```text
dashboard-universitas/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── university_data.csv
```

## Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/USERNAME/dashboard-universitas.git
cd dashboard-universitas
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

Dashboard dapat dipublikasikan melalui Streamlit Community Cloud setelah kode diunggah ke GitHub.

## Tautan Repository

Ganti bagian berikut dengan tautan repository GitHub Anda:

```text
https://github.com/USERNAME/dashboard-universitas
```
