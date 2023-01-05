# Depok City House Price Prediction


## Introduction
Rumah merupakan salah satu kebutuhan dasar yang berfungsi sebagai tempat tinggal, tempat melakukan suatu aktivitas, dan tempat berlindung, yang memberikan rasa aman dan nyaman. Alasan ini lah yang membuat rumah dianggap sebagai salah satu aset yang sangat penting bagi semua orang. Selain itu, rumah merupakan investasi yang menguntungkan karena merupakan salah satu aset yang mengalami kenaikan harga setiap tahunnya. 


Pertumbuhan penduduk yang terus meningkat setiap tahunnya mengakibatkan kebutuhan rumah yang terus meningkat. Setiap orang menginginkan rumah yang bagus dan nyaman dengan harga yang terjangkau. Sulitnya menemukan rumah ideal dengan harga yang terjangkau menjadi kendalah bagi sebagian orang. Berdasarkan permasalahan tersebut, dilakukan sebuah proyek di mana akan dibangun sebuah model yang dapat memprediksi harga rumah di kota Depok, Jawa Barat, dengan mempertimbangkan karakteristik rumah dan fasilitas yang tersedia.


## Goals
Proyek ini akan membangun sebuah model yang akan dapat memprediksi harga rumah di Kota Depok berdasarkan karakteristik dan fasilitas dari masing-masing rumah. Dan juga, proyek ini dapat memberikan insight terhadap hal-hal berikut: 
- Fitur/faktor yang paling berpengaruh terhadap penetapan harga rumah.
- Daerah pada Kota Depok yang memiliki harga rumah termahal.


## Web Scraping
Data didapatkan dengan melakukan web scraping pada website www.lamudi.co.id dengan menggunakan aplikasi Parsehub. Data hasil scraping terdiri dari 3000 rumah di Kota Depok, dari setiap data rumah, didapatkan fitur-fitur berikut:
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
- Fasilitas keamanan
- Fasilitas kolam renang
- Fasilitas taman
- Fasilitas balcony
- Fasilitas Pendingin ruangan (AC)