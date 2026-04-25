# Sistem Intelijen Kepolisian: Fuzzy Logic dan Expert System

Repositori ini berisi implementasi dua sistem kecerdasan buatan untuk memenuhi tugas Responsi Praktikum Kecerdasan Buatan. Sistem ini dirancang untuk membantu pengambilan keputusan taktis kepolisian menggunakan paradigma Fuzzy Logic dan Expert System berbasis Web (Streamlit).

## Identitas Mahasiswa
* Nama: Hafizh Naufal Raditya
* NIM: H1D024061

---

## Ringkasan Proyek

Proyek ini terdiri dari dua aplikasi utama yang diintegrasikan dalam antarmuka web interaktif:

### 1. Sistem Fuzzy: Kalkulator Eskalasi Taktis (Rules of Engagement)
Sistem ini menggunakan logika fuzzy untuk menentukan tingkat respon petugas kepolisian di lapangan.
* Variabel Input: Agresivitas Tersangka (0-100), Jarak Fisik (0-50m), dan Kepadatan Warga Sipil (0-100).
* Variabel Output: Skor Tingkat Tindakan (0-100).
* Logika: Menentukan kapan petugas harus menggunakan negosiasi verbal, senjata less-lethal (Taser/Gas), atau lethal force (Senjata Api) sesuai standar SOP dan keamanan publik.

### 2. Sistem Pakar: Rekomendasi Tactical Loadout SWAT/Brimob
Sistem pakar berbasis aturan (Rule-Based System) untuk menentukan perlengkapan personel sebelum menjalankan operasi.
* Fakta Input: Jenis Operasi, Kondisi Medan, Pencahayaan, dan Tingkat Ancaman.
* Output: Rekomendasi Senjata Utama, Senjata Cadangan, Pelindung Tubuh, dan Tactical Gear secara spesifik.
* Logika: Menggunakan Forward Chaining untuk mencocokkan intelijen lapangan dengan database logistik persenjataan.

---

## Cara Menjalankan Aplikasi

Aplikasi ini dibangun menggunakan framework Streamlit. Ikuti langkah berikut untuk menjalankan di lingkungan lokal:

1. Klik New Terminal di menu Terminal
2. Ketikkan "streamlit run responsi.py" untuk fuzzy, untuk pakar "streamlit run responsi2.py
