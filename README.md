# Depok City House Price Prediction

## Introduction

Rumah merupakan salah satu kebutuhan dasar yang berfungsi sebagai tempat tinggal, tempat melakukan suatu aktivitas, dan tempat berlindung, yang memberikan rasa aman dan nyaman. Alasan ini lah yang membuat rumah dianggap sebagai salah satu aset yang sangat penting bagi semua orang. Selain itu, rumah merupakan investasi yang menguntungkan karena merupakan salah satu aset yang mengalami kenaikan harga setiap tahunnya.

Pertumbuhan penduduk yang terus meningkat setiap tahunnya mengakibatkan kebutuhan rumah yang terus meningkat. Setiap orang menginginkan rumah yang bagus dan nyaman dengan harga yang terjangkau. Sulitnya menemukan rumah ideal dengan harga yang terjangkau menjadi kendalah bagi sebagian orang. Berdasarkan permasalahan tersebut, dilakukan sebuah proyek di mana akan dibangun sebuah model yang dapat memprediksi harga rumah di kota Depok, Jawa Barat, dengan mempertimbangkan karakteristik rumah dan fasilitas yang tersedia.

## Goals

Proyek ini akan membangun sebuah model yang akan dapat memprediksi harga rumah di Kota Depok berdasarkan karakteristik dan fasilitas dari masing-masing rumah. Dan juga, proyek ini dapat memberikan insight terhadap hal-hal berikut:

- Fitur/faktor yang paling berpengaruh terhadap penetapan harga rumah.
- Daerah pada Kota Depok yang memiliki harga rumah termahal.

## Web Scraping

Data didapatkan dengan melakukan web scraping pada website www.lamudi.co.id pada bulan Januari 2023 dengan menggunakan aplikasi Parsehub. Data hasil scraping terdiri dari 3000 rumah di Kota Depok, dari setiap data rumah, didapatkan fitur-fitur berikut:

- URL
- Nama
- Lokasi
- Harga
- Jumlah kamar tidur
- Jumlah kamar mandi
- Luas bangunan
- Luas lahan
- jumlah lahan parkir
- jumlah lantai
- Fully Furnished
- Fasilitas keamanan24jam
- Fasilitas kolam renang
- Fasilitas taman
- Fasilitas balcony
- Fasilitas Pendingin ruangan (AC)

## Data Preprocessing

Setelah di scraping, data perlu dibersihkan agar dapat dianalisis dan dilakukan prediksi, yaitu:

- Rename nama kolom agar mudah dibaca
- Menghilangkan baris yang hanya terdapat URL
- Menghilangkan kolom fully_furnished, kolam_renang, jumlah lahan parkir, dan jumlah_lantai
- Menyederhanakan nama lokasi menjadi kecamatan
- Memperbaiki tipe data pada kamar dan kamar_mandi
- Input missing value pada fitur fasilitas menjadi 'no'
- Input missing value pada fitur numerik menggunakan nilai rata-rata (mean)
- Menghilangkan 'Rp' dan mengganti tipe data pada harga (ex: Rp 130.000.000 menjadi 130000000)
- Menghilangkan baris duplikat
- Sebelum pemeriksaan outlier, data dibagi menjadi dua, yaitu train dan test dengan persentase 80 % dan 20 %
- Ditemukannya outlier pada fitur kamar tidur, kamar mandi, luas bangunan, dan luas lahan.

  - Mayoritas outlier diakibatkan oleh kesalahan input pada sumber data. Metode untuk mengatasi outlier ini pada projek ini adalah dengan menganggap nilai tersebut sebagai missing value, sehingga diganti dengan nilai median. Nilai median digunakan karena tahan terhadap outlier dibanding dengan menggunakan mean.
  - Terdapat outlier lainnya yang bukan hasil kesalahan input. Outlier jenis ini akan dibiarkan

- Semua fitur numerik memiliki distribusi yang cenderung skew ke kanan karena adanya outlier.
- Fitur kamar mandi dihilangkan karena berkorelasi tinggi dengan kamar tidur

## Data Analysis

Berdasarkan hasil analisis:

- Terdapat rumah di daerah Sawangan dengan harga 40 milyar dengan luas lahan 9000 m^2
- Cinere merupakan daerah yang memiliki rata-rata harga rumah termahal di Kota Depok, diikuti oleh Limo dan Beji

  ![alt text](https://github.com/anggapark/Depok-houseprice-prediction/blob/main/asset/rata2_harga_lokasi.png?raw=true)

- Rumah dengan harga di atas sama dengan 20 milyar memiliki luas lahan di atas 2000 m^2
- Luas lahan memiliki korelasi yang cukup tinggi dengan harga rumah, diikuti oleh luas bangunan
- Kamar tidur memiliki korelasi yang tinggi dengan kamar tidur

  ![alt text](https://github.com/anggapark/Depok-houseprice-prediction/blob/main/asset/korelasi.png?raw=true)

- Mayoritas rumah tidak memiliki salah satu atau semua fitur tambahan

  ![alt text](https://github.com/anggapark/Depok-houseprice-prediction/blob/main/asset/fitur_lain.png?raw=true)

## Modelling

- Pada tahap data preprocessing:

  - Fitur dengan nilai yes dan no dilakukan label encoding menjadi yes: 1 dan no: 0.
  - Fitur kategorik dengan kelas yang banyak seperti lokasi diterapkan One Hot Encoding
  - Fitur yang distribusinya skew dilakukan transformasi data menggunakan log transformation
  - Fitur numerik di scale menggunakan StandardScaler

- Pada tahap modelling, algoritma yang digunakan adalah:

  - Linear Regression,
  - Ridge Regression,
  - Lasso Regression,
  - RANSAC Regression, dan
  - Random Forest Regression

- Metric yang digunakan sebagai evaluasi model adalah Root Mean Squared Error (RMSE) dan Mean Absolute Error (MAE)

## Evaluation

| Model                    | RMSE     | MAE      |
| ------------------------ | -------- | -------- |
| Linear Regression        | 0.288594 | 0.209811 |
| Ridge Regression         | 0.288735 | 0.209920 |
| Lasso Regression         | 0.610469 | 0.451481 |
| RANSAC Regression        | 0.318648 | 0.227697 |
| Random forest Regression | 0.254087 | 0.174959 |

Dapat dilihat, model dengan nilai RMSE dan MAE terbaik adalah Random Forest Regression dengan nilai RMSE 0.254087 dan MAE 0.174959.

Setelah itu dilakukan parameter tuning pada model Random Forest Regression untuk mencari hasil yang lebih baik menggunakan GridSearchCV.

Hasil dari tuning adalah:

| Tuning | RMSE | MAE |
| Sebelum | 0.254087 | 0.174959 |
| Setelah | 0.253440 | 0.174139 |

## Future Plan

- [x] Melakukan parameter tuning pada model untuk mencari nilai RMSE dan MAE yang lebih baik.
- [ ] Deploy machine learning model dengan streamlit.
- [ ] Membuat API untuk siapa saja yang ingin membuat aplikasi dengan machine learning model.
