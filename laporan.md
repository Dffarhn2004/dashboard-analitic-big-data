# Rancangan Laporan Dashboard Universitas

## A. Penentuan Kebutuhan

### 1. Pengguna Utama

Pengguna utama dashboard adalah pihak rektorat dan pimpinan universitas. Pengguna tersebut membutuhkan informasi ringkas yang dapat membantu proses pemantauan, evaluasi, dan pengambilan keputusan strategis di tingkat universitas.

### 2. Kebutuhan Informasi

Informasi yang dibutuhkan meliputi jumlah mahasiswa aktif, jumlah mahasiswa baru, jumlah lulusan, publikasi dosen, rata-rata IPK, persentase kelulusan tepat waktu, persentase lulusan yang telah bekerja, serta status akreditasi masing-masing fakultas.

Dashboard juga perlu menyediakan fasilitas untuk membandingkan kinerja antar-fakultas dan melihat perkembangan indikator berdasarkan tahun.

## B. Perancangan Dashboard

### 1. Indikator yang Ditampilkan

Indikator utama yang ditampilkan adalah:

1. Jumlah mahasiswa aktif.
2. Jumlah mahasiswa baru.
3. Jumlah lulusan.
4. Jumlah publikasi dosen.
5. Rata-rata IPK mahasiswa.
6. Persentase kelulusan tepat waktu.
7. Persentase lulusan yang telah bekerja.
8. Status akreditasi.

### 2. Sumber Data

Data yang digunakan merupakan data simulasi periode 2021–2026. Data simulasi dipilih karena dapat menggambarkan kebutuhan dashboard tanpa menggunakan data internal universitas yang bersifat rahasia.

## C. Implementasi Teknis

Dashboard dikembangkan menggunakan Python dan Streamlit. Library Pandas digunakan untuk membaca dan mengolah data, sedangkan Plotly digunakan untuk membuat visualisasi interaktif.

Dashboard memiliki beberapa komponen berikut:

- KPI card untuk menampilkan ringkasan indikator.
- Bar chart mahasiswa aktif per fakultas.
- Line chart tren publikasi dosen.
- Bar chart persentase kelulusan tepat waktu.
- Pie chart distribusi akreditasi.
- Filter tahun dan fakultas.
- Tabel detail dan fitur unduh CSV.

## D. Publikasi Proyek

Kode program, dataset simulasi, file requirements, dan README diunggah ke GitHub. README menjelaskan struktur proyek, fitur dashboard, dependency, dan langkah menjalankan aplikasi.

Tautan repository:

https://github.com/USERNAME/dashboard-universitas
