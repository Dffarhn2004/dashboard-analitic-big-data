Menurut saya, narasi terbaik bukan sekadar **“menampilkan kepuasan mahasiswa”**, tetapi:

> **Membantu rektorat mengidentifikasi kelompok mahasiswa yang memiliki tingkat kepuasan rendah serta menilai apakah kualitas pengajaran, fasilitas kampus, dan pengalaman pembelajaran berkaitan dengan kepuasan tersebut.**

Dengan narasi ini, dashboard punya alur yang jelas:

**kondisi umum → kelompok bermasalah → kemungkinan faktor penyebab → dasar tindakan.**

Ini sejalan dengan materi dosen bahwa dashboard bukan hanya kumpulan grafik, tetapi alat pendukung keputusan yang menampilkan KPI penting dan membantu pengguna bertindak. 

# 1. Penyesuaian konteks dataset

Dataset asli memuat banyak nama universitas. Namun, untuk proyek ini kita dapat menetapkan asumsi berikut:

> Seluruh responden dianggap sebagai mahasiswa dari satu universitas simulasi. Kolom `university` tidak digunakan dalam analisis karena nama universitas pada dataset hanya merupakan bagian dari data sintetis. Kolom `country` ditafsirkan sebagai negara asal mahasiswa, bukan lokasi universitas.

Ini lebih aman daripada mengganti kolom `university` menjadi fakultas, karena nilainya berupa nama universitas yang hampir semuanya berbeda dan tidak mewakili fakultas.

Dalam laporan, tuliskan secara transparan:

> Dataset yang digunakan merupakan data sintetis dari Kaggle. Untuk menyesuaikan dengan ruang lingkup proyek, seluruh responden diposisikan sebagai mahasiswa dalam satu universitas simulasi. Analisis difokuskan pada jenjang pendidikan, bidang studi, tahun studi, status beasiswa, kelas daring, penilaian fasilitas, kualitas pengajaran, dan kepuasan mahasiswa. Kolom nama universitas tidak digunakan.

---

# 2. Narasi utama dashboard

## Judul yang disarankan

> **Dashboard Evaluasi Pengalaman dan Kepuasan Mahasiswa**

Subjudul:

> Memantau tingkat kepuasan mahasiswa dan mengidentifikasi aspek layanan akademik yang memerlukan peningkatan.

Judul ini lebih kuat daripada “Dashboard Kepuasan Mahasiswa” karena dashboard kita tidak hanya menghitung kepuasan, tetapi juga mengevaluasi faktor-faktor yang mungkin berkaitan dengannya.

## Pengguna utama

> Pengguna utama dashboard adalah pihak rektorat, khususnya pimpinan universitas dan unit penjaminan mutu.

## Kebutuhan informasi pengguna

Narasi yang dapat langsung digunakan:

> Pihak rektorat membutuhkan informasi yang ringkas dan mudah dipahami mengenai pengalaman mahasiswa selama mengikuti pendidikan di universitas. Informasi tersebut diperlukan untuk mengetahui tingkat kepuasan mahasiswa secara keseluruhan, mengidentifikasi kelompok mahasiswa yang memiliki tingkat ketidakpuasan tinggi, serta mengevaluasi aspek layanan yang berpotensi memengaruhi pengalaman mahasiswa.
>
> Dashboard ini dirancang untuk membantu rektorat menjawab beberapa pertanyaan utama. Pertama, bagaimana kondisi kepuasan mahasiswa secara keseluruhan? Kedua, bidang studi atau jenjang pendidikan mana yang memiliki tingkat kepuasan relatif rendah? Ketiga, apakah mahasiswa yang memberikan penilaian rendah terhadap kualitas pengajaran dan fasilitas kampus juga cenderung memiliki tingkat kepuasan yang rendah? Keempat, apakah terdapat perbedaan pengalaman berdasarkan status beasiswa dan pelaksanaan kelas daring?
>
> Informasi tersebut dapat digunakan sebagai dasar awal untuk menentukan prioritas evaluasi. Sebagai contoh, apabila suatu bidang studi memiliki proporsi mahasiswa tidak puas yang tinggi dan pada saat yang sama memperoleh penilaian kualitas pengajaran yang rendah, rektorat dapat memprioritaskan evaluasi proses pembelajaran pada bidang studi tersebut. Namun, dashboard ini tidak digunakan untuk menyimpulkan hubungan sebab-akibat, melainkan untuk menemukan pola yang perlu diperiksa lebih lanjut.

Bagian terakhir penting. Dataset survei dapat menunjukkan **pola atau hubungan**, tetapi tidak cukup untuk membuktikan bahwa fasilitas buruk menyebabkan ketidakpuasan.

---

# 3. Cerita yang dibangun dashboard

Dashboard sebaiknya membawa rektorat melalui empat tahap.

## Tahap 1 — Bagaimana kondisi umum mahasiswa?

Pertanyaan:

* Berapa jumlah responden?
* Berapa persentase mahasiswa yang puas?
* Berapa persentase mahasiswa yang tidak puas?
* Bagaimana rata-rata kualitas pengajaran?
* Bagaimana rata-rata fasilitas kampus?

Tujuannya adalah memberikan gambaran umum dalam beberapa detik.

## Tahap 2 — Kelompok mana yang perlu diperhatikan?

Pertanyaan:

* Bidang studi mana yang memiliki kepuasan terendah?
* Jenjang Bachelor, Master, atau PhD mana yang menunjukkan ketidakpuasan lebih tinggi?
* Apakah mahasiswa pada tahun studi tertentu lebih tidak puas?
* Apakah ada perbedaan antara penerima dan nonpenerima beasiswa?

## Tahap 3 — Apa yang mungkin berkaitan dengan kepuasan?

Pertanyaan:

* Apakah kualitas pengajaran yang lebih tinggi diikuti kepuasan yang lebih baik?
* Apakah fasilitas kampus berkaitan dengan kepuasan?
* Mana yang tampak lebih kuat hubungannya dengan kepuasan: pengajaran atau fasilitas?
* Apakah pengalaman kelas daring menunjukkan pola yang berbeda?

## Tahap 4 — Apa tindakan awal yang dapat dilakukan?

Dashboard tidak perlu memberikan keputusan otomatis. Namun, dashboard dapat menampilkan kesimpulan seperti:

> Bidang studi dengan kepuasan rendah dan penilaian pengajaran di bawah rata-rata perlu menjadi prioritas evaluasi akademik.

Ini sesuai prinsip data storytelling: data, visualisasi, dan narasi perlu digabungkan agar audiens tidak hanya melihat angka, tetapi memahami maknanya dan dapat mengambil tindakan. 

---

# 4. Persiapan data kepuasan

Kolom `overall_satisfaction` masih berbentuk ordinal:

```text
Very Dissatisfied
Dissatisfied
Neutral
Satisfied
Very Satisfied
```

Kita perlu membuat versi numeriknya:

```python
satisfaction_score = {
    "Very Dissatisfied": 1,
    "Dissatisfied": 2,
    "Neutral": 3,
    "Satisfied": 4,
    "Very Satisfied": 5
}
```

Kemudian buat kategori ringkas:

```text
Puas:
- Satisfied
- Very Satisfied

Netral:
- Neutral

Tidak Puas:
- Dissatisfied
- Very Dissatisfied
```

Versi numerik digunakan untuk menghitung rata-rata, sedangkan kategori asli tetap digunakan untuk visualisasi distribusi.

Karena tingkat kepuasan merupakan data ordinal, urutan kategorinya harus dipertahankan. Materi visual encoding juga menjelaskan bahwa data ordinal sebaiknya disajikan dengan urutan visual atau skala warna berurutan, bukan warna acak. 

---

# 5. KPI utama

Bagian atas dashboard sebaiknya hanya berisi lima KPI.

### 1. Total responden

```text
1.000 mahasiswa
```

Menunjukkan cakupan data setelah filter diterapkan.

### 2. Persentase mahasiswa puas

Rumus:

```text
(Satisfied + Very Satisfied) / total responden × 100%
```

Lebih mudah dipahami rektorat daripada hanya menampilkan rata-rata skor.

### 3. Persentase mahasiswa tidak puas

Rumus:

```text
(Dissatisfied + Very Dissatisfied) / total responden × 100%
```

Ini menjadi indikator risiko utama.

### 4. Rata-rata kualitas pengajaran

Skala:

```text
1–5
```

### 5. Rata-rata fasilitas kampus

Skala:

```text
1–5
```

Saya tidak menyarankan menjadikan rata-rata biaya kuliah sebagai KPI utama karena dashboard berfokus pada kualitas pengalaman mahasiswa, bukan keuangan universitas.

---

# 6. Visualisasi yang mendukung narasi

## Visualisasi 1 — Distribusi kepuasan mahasiswa

**Jenis:** horizontal bar chart.

**Data:**

* Very Satisfied
* Satisfied
* Neutral
* Dissatisfied
* Very Dissatisfied

**Pertanyaan yang dijawab:**

> Bagaimana kondisi kepuasan mahasiswa secara keseluruhan?

Mengapa bar chart, bukan pie chart?

Karena bar chart lebih mudah digunakan untuk membandingkan jumlah atau persentase secara presisi. Materi dosen juga menjelaskan bahwa manusia lebih akurat membandingkan panjang batang daripada sudut atau luas pada pie chart. 

Urutkan dari positif ke negatif:

```text
Very Satisfied
Satisfied
Neutral
Dissatisfied
Very Dissatisfied
```

Gunakan warna ordinal yang konsisten:

```text
Hijau tua → hijau muda → abu-abu → jingga → merah
```

### Teks pendamping

> Grafik menunjukkan distribusi seluruh tingkat kepuasan, sehingga rektorat tidak hanya bergantung pada satu nilai rata-rata.

---

## Visualisasi 2 — Proporsi kepuasan berdasarkan bidang studi

**Jenis:** 100% stacked horizontal bar chart.

**Sumbu Y:**

```text
Field of study
```

**Bagian batang:**

```text
Puas
Netral
Tidak Puas
```

**Pertanyaan yang dijawab:**

> Bidang studi mana yang memiliki proporsi ketidakpuasan paling tinggi?

Mengapa 100% stacked bar?

Karena jumlah mahasiswa pada setiap bidang studi mungkin berbeda. Jika hanya menggunakan jumlah mentah, bidang dengan responden lebih banyak akan terlihat paling dominan. Persentase membuat perbandingan lebih adil.

Urutkan bidang studi berdasarkan persentase tidak puas dari yang tertinggi.

Contoh judul yang lebih naratif:

> **Bidang studi dengan proporsi mahasiswa tidak puas tertinggi**

Bukan sekadar:

> Kepuasan berdasarkan field of study

Materi tentang teks dashboard menunjukkan bahwa judul, subjudul, content block, anotasi, dan ringkasan angka membantu pengguna memahami fokus visual dan membaca dashboard sesuai urutan yang dimaksud. 

---

## Visualisasi 3 — Kualitas pengajaran dan fasilitas per bidang studi

**Jenis:** grouped horizontal bar chart.

Untuk setiap bidang studi, tampilkan:

* Rata-rata teaching quality
* Rata-rata campus facilities

**Pertanyaan yang dijawab:**

> Pada bidang studi dengan kepuasan rendah, apakah penilaian pengajaran atau fasilitas juga rendah?

Gunakan horizontal bar karena nama bidang studi relatif panjang. Materi visualisasi menyarankan horizontal bar ketika label kategori panjang agar lebih mudah dibaca. 

Namun, jangan menampilkan terlalu banyak kategori sekaligus. Delapan bidang studi masih cukup masuk akal.

Tambahkan garis referensi:

```text
Rata-rata universitas
```

Dengan begitu, rektorat dapat melihat bidang studi mana yang berada di bawah rata-rata.

---

## Visualisasi 4 — Hubungan kualitas pengajaran dengan kepuasan

Ada dua pilihan.

### Pilihan terbaik: heatmap

**Baris:**

```text
Teaching quality rating: 1–5
```

**Kolom:**

```text
Very Dissatisfied sampai Very Satisfied
```

**Isi warna:**

```text
Jumlah atau persentase mahasiswa
```

Pertanyaan:

> Ketika penilaian kualitas pengajaran meningkat, apakah distribusi kepuasan juga bergeser ke arah yang lebih positif?

Heatmap lebih cocok daripada scatter plot biasa karena kedua variabel hanya memiliki sedikit nilai diskrit. Jika dipaksakan menjadi scatter plot, banyak titik akan bertumpuk pada posisi yang sama.

Alternatifnya, gunakan **stacked bar chart** untuk setiap rating pengajaran.

### Teks pendamping

> Pola ini menunjukkan hubungan deskriptif antara kualitas pengajaran dan kepuasan. Pola tersebut tidak membuktikan hubungan sebab-akibat.

---

## Visualisasi 5 — Hubungan fasilitas dengan kepuasan

Gunakan bentuk yang sama dengan visualisasi pengajaran:

* Heatmap, atau
* 100% stacked bar chart

Pertanyaan:

> Apakah mahasiswa yang memberikan penilaian fasilitas rendah juga cenderung lebih tidak puas?

Dengan membandingkan visualisasi 4 dan 5, rektorat dapat memperoleh indikasi awal apakah pengajaran atau fasilitas tampak lebih berkaitan dengan kepuasan.

---

## Visualisasi 6 — Perbandingan berdasarkan kelas daring

**Jenis:** 100% stacked bar chart.

Dua kelompok:

```text
Online classes: Yes
Online classes: No
```

Bagian:

```text
Puas
Netral
Tidak Puas
```

Pertanyaan:

> Apakah mahasiswa yang mengikuti kelas daring menunjukkan distribusi kepuasan yang berbeda?

Ini lebih relevan daripada sekadar menghitung jumlah mahasiswa online dan offline.

---

## Visualisasi 7 — Beasiswa dan kepuasan

**Jenis:** grouped bar atau 100% stacked bar.

Kelompok:

```text
Scholarship: Yes
Scholarship: No
```

Metrik:

* Persentase puas
* Persentase tidak puas

Pertanyaan:

> Apakah pengalaman mahasiswa penerima beasiswa berbeda dari mahasiswa nonpenerima?

Jangan menyimpulkan beasiswa menyebabkan kepuasan. Cukup katakan:

> Terdapat atau tidak terdapat perbedaan pola kepuasan antara kedua kelompok.

---

## Visualisasi 8 — Biaya kuliah dan kepuasan

**Jenis:** box plot, bukan line chart.

Sumbu X:

```text
Overall satisfaction
```

Sumbu Y:

```text
Tuition USD
```

Pertanyaan:

> Apakah kelompok mahasiswa dengan tingkat kepuasan berbeda memiliki distribusi biaya kuliah yang berbeda?

Saya lebih menyarankan box plot daripada scatter plot karena `overall_satisfaction` adalah kategorikal ordinal. Box plot menunjukkan median, rentang, dan pencilan biaya kuliah pada tiap kategori kepuasan.

Namun, visualisasi ini bersifat **sekunder**, bukan inti dashboard.

---

# 7. Visualisasi yang tidak perlu digunakan

## Line chart

Dataset tidak mempunyai variabel waktu kalender seperti tanggal, bulan, atau tahun survei.

`year_of_study` berarti tingkat studi mahasiswa, bukan waktu pengamatan. Karena itu, menghubungkan tahun studi 1 sampai 5 dengan line chart dapat memberi kesan seolah-olah data merupakan tren waktu.

Gunakan bar chart untuk `year_of_study`, bukan line chart.

Materi dosen menjelaskan bahwa line chart tepat ketika sumbu X memiliki urutan bermakna, terutama waktu, untuk menunjukkan perubahan dari satu periode ke periode berikutnya. 

## Pie chart dengan lima tingkat kepuasan

Pie chart sebenarnya bisa digunakan, tetapi kurang efektif karena lima proporsi mungkin berdekatan. Horizontal bar chart akan lebih mudah dibandingkan.

## Peta negara

Kolom `country` merepresentasikan negara asal mahasiswa. Peta tidak terlalu mendukung narasi utama tentang kualitas pengajaran dan fasilitas. Negara lebih baik digunakan sebagai filter atau analisis tambahan.

## Grafik berdasarkan nama universitas

Karena kita menganggap data berasal dari satu universitas simulasi, kolom ini tidak digunakan.

---

# 8. Filter interaktif

Filter utama:

```text
Program level
Field of study
Year of study
Scholarship
Online classes
```

Filter tambahan:

```text
Gender
Country of origin
Age range
```

Urutan sidebar:

1. Program level
2. Field of study
3. Year of study
4. Scholarship
5. Online classes
6. Country
7. Gender

Semua KPI dan grafik harus berubah mengikuti filter.

Tambahkan tombol:

```text
Reset filter
```

Dan teks petunjuk:

> Gunakan filter untuk membandingkan pengalaman mahasiswa berdasarkan jenjang, bidang studi, tahun studi, beasiswa, dan kelas daring.

Ini sejalan dengan temuan paper bahwa interaction guidance, tooltip, judul, subjudul, dan content block memiliki peran penting dalam mengarahkan pengguna saat mengeksplorasi dashboard. 

---

# 9. Susunan dashboard

```text
=====================================================
DASHBOARD EVALUASI PENGALAMAN DAN KEPUASAN MAHASISWA
Memantau kualitas layanan akademik dan kelompok
mahasiswa yang memerlukan perhatian.
=====================================================

[Filter pada sidebar]

[Total Responden] [Puas] [Tidak Puas]
[Kualitas Pengajaran] [Fasilitas Kampus]

-----------------------------------------------------
1. KONDISI KEPUASAN MAHASISWA
Distribusi Tingkat Kepuasan
[Horizontal Bar Chart]
-----------------------------------------------------

2. KELOMPOK YANG MEMERLUKAN PERHATIAN

[100% Stacked Bar: Kepuasan per Bidang Studi]

[Grouped Bar:
 Kualitas Pengajaran vs Fasilitas per Bidang Studi]
-----------------------------------------------------

3. FAKTOR YANG BERKAITAN DENGAN KEPUASAN

[Heatmap: Teaching Quality vs Satisfaction]

[Heatmap: Facilities vs Satisfaction]
-----------------------------------------------------

4. PERBANDINGAN PENGALAMAN MAHASISWA

[Online vs Non-online]

[Scholarship vs Non-scholarship]
-----------------------------------------------------

5. DATA DETAIL DAN CATATAN

[Tabel Data]
[Download CSV]

Sumber: World University Student Survey Dataset, Kaggle
Catatan: data bersifat sintetis dan hasil bersifat deskriptif.
```

---

# 10. Narasi final untuk bagian kebutuhan

Berikut versi yang paling siap dimasukkan ke laporan:

## A. Penentuan Kebutuhan

### 1. Pengguna Utama Dashboard

Pengguna utama dashboard adalah pihak rektorat, khususnya pimpinan universitas dan unit penjaminan mutu. Rektorat membutuhkan informasi tingkat tinggi yang dapat membantu proses pemantauan kualitas layanan akademik dan pengalaman mahasiswa.

Dashboard ini menggunakan data survei sintetis mahasiswa. Untuk menyesuaikan ruang lingkup proyek, seluruh responden dianggap berasal dari satu universitas simulasi. Kolom negara digunakan untuk menggambarkan asal mahasiswa, sedangkan kolom nama universitas tidak digunakan dalam analisis.

### 2. Kebutuhan Informasi Pengguna

Pihak rektorat membutuhkan informasi mengenai kondisi kepuasan mahasiswa secara keseluruhan serta faktor-faktor yang berkaitan dengan pengalaman mahasiswa. Dashboard dirancang untuk membantu rektorat mengetahui proporsi mahasiswa yang puas, netral, dan tidak puas; mengevaluasi kualitas pengajaran dan fasilitas kampus; serta mengidentifikasi bidang studi, jenjang pendidikan, atau kelompok mahasiswa yang menunjukkan tingkat ketidakpuasan relatif tinggi.

Selain itu, rektorat membutuhkan perbandingan pengalaman berdasarkan status beasiswa dan pelaksanaan kelas daring. Dashboard juga membantu melihat pola hubungan antara kualitas pengajaran, fasilitas kampus, dan kepuasan mahasiswa.

Informasi tersebut digunakan sebagai dasar awal untuk menentukan area yang memerlukan evaluasi lebih lanjut. Sebagai contoh, apabila suatu bidang studi memiliki proporsi mahasiswa tidak puas yang tinggi serta penilaian kualitas pengajaran di bawah rata-rata, bidang studi tersebut dapat diprioritaskan dalam evaluasi akademik. Dashboard tidak dimaksudkan untuk membuktikan hubungan sebab-akibat, tetapi untuk memberikan gambaran deskriptif dan menemukan pola yang dapat mendukung pengambilan keputusan rektorat.

## Kesimpulan desain

Dashboard kita sebaiknya memiliki satu pesan utama:

> **Kepuasan mahasiswa perlu dilihat tidak hanya sebagai angka umum, tetapi ditelusuri berdasarkan kelompok mahasiswa dan kualitas pengalaman yang mereka terima.**

Dengan begitu, setiap visualisasi punya fungsi yang jelas dan tidak terasa seperti kumpulan grafik acak.
