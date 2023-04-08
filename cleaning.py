# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 06:21:47 2023

@author: anggapark
"""

import pandas as pd
import numpy as np

path = "C:/Users/hi/LatihanData/Depok-houseprice-prediction/"
df = pd.read_csv(path + "raw_df.csv")

df = df.rename(
    columns={
        "rumah_url": "url",
        "rumah_nama": "nama",
        "rumah_lokasi": "lokasi",
        "rumah_harga": "harga",
        "rumah_kamar_tidur": "kamar_tidur",
        "rumah_kamar_mandi": "kamar_mandi",
        "rumah_luas_bangunan": "luas_bangunan",
        "rumah_luas_lahan": "luas_lahan",
        "rumah_fully_furnished": "fully_furnished",
        "rumah_keamanan": "keamanan24jam",
        "rumah_kolam_renang": "kolam_renang",
        "rumah_taman": "taman",
        "rumah_lahan_parkir": "lahan_parkir",
        "rumah_jumlah_lantai": "jumlah_lantai",
        "rumah_balcony": "balcony",
        "rumah_AC": "AC",
    }
)

# periksa missing value
df.isnull().sum().sort_values(ascending=0)

# pada hasil scraping, terdapat baris yang hanya terdapat url tanpa fitur rumah lainnya, baris tersebut dihapus
missing_idx = df[(df["harga"].isnull())].index
df = df.drop(index=missing_idx)

# fully_furnished, kolam_renang missing, dan jumlah_lantai memiliki missing data >90%,
df = df.drop(
    columns=["fully_furnished", "kolam_renang", "jumlah_lantai"], axis=1
).reset_index(drop=True)

# menyederhanakan lokasi
df["nama"] = df["nama"].apply(lambda x: x.lower())
df["lokasi"] = df["lokasi"].apply(lambda x: x.lower())


def simplified_location(df):
    """
    fungsi ini untuk mengambil nama kecamatan dari
    value lokasi untuk mempermudah analisis
    """
    if "beji" in df:
        return "beji"
    elif "tanah baru" in df:
        return "beji"
    elif "kukusan" in df:
        return "beji"
    elif "pondok cina" in df:
        return "beji"
    elif "kemiri" in df:
        return "beji"

    elif "bojongsari" in df:
        return "bojongsari"
    elif "pondok petir" in df:
        return "bojongsari"
    elif "curug" in df:
        return "bojongsari"
    elif "serua" in df:
        return "bojongsari"
    elif "duren" in df:
        return "bojongsari"

    elif "cilodong" in df:
        return "cilodong"
    elif "jatimulya" in df:
        return "cilodong"
    elif "kalimulya" in df:
        return "cilodong"
    elif "kalibaru" in df:
        return "cilodong"
    elif "sukamaju" in df:
        return "cilodong"
    elif "rajeg" in df:
        return "cilodong"
    elif "gani" in df:
        return "cilodong"
    elif "kemang" in df:
        return "cilodong"
    elif "boulevrd" in df:
        return "cilodong"

    elif "cimanggis" in df:
        return "cimanggis"
    elif "kelapa dua" in df:
        return "cimanggis"
    elif "tugu" in df:
        return "cimanggis"
    elif "cisalak" in df:
        return "cimanggis"
    elif "harjamukti" in df:
        return "cimanggis"
    elif "mekarsari" in df:
        return "cimanggis"
    elif "cibubur" in df:
        return "cimanggis"

    elif "cinere" in df:
        return "cinere"
    elif "pangkalan jati" in df:
        return "cinere"
    elif "gandul" in df:
        return "cinere"
    elif "andara" in df:
        return "cinere"

    elif "cipayung" in df:
        return "cipayung"
    elif "citayam" in df:
        return "cipayung"
    elif "bulak" in df:
        return "cipayung"
    elif "ratujaya" in df:
        return "cipayung"
    elif "serong" in df:
        return "cipayung"

    elif "limo" in df:
        return "limo"
    elif "krukut" in df:
        return "limo"
    elif "grogol" in df:
        return "limo"
    elif "maruyung" in df:
        return "limo"
    elif "meruyung" in df:
        return "limo"

    elif "pancoran mas" in df:
        return "pancoran mas"
    elif "rangkapan jaya" in df:
        return "pancoran mas"
    elif "margonda" in df:
        return "pancoran mas"
    elif "mampang" in df:
        return "pancoran mas"
    elif "nuvo" in df:
        return "pancoran mas"

    elif "sawangan" in df:
        return "sawangan"
    elif "bedahan" in df:
        return "sawangan"
    elif "pengasinan" in df:
        return "sawangan"
    elif "cinangka" in df:
        return "sawangan"
    elif "pasir putih" in df:
        return "sawangan"
    elif "desari" in df:
        return "sawangan"

    elif "sukmajaya" in df:
        return "sukmajaya"
    elif "baktijaya" in df:
        return "sukmajaya"
    elif "grand depok city" in df:
        return "sukmajaya"
    elif "gdc" in df:
        return "sukmajaya"
    elif "juanda" in df:
        return "sukmajaya"
    elif "tirtajaya" in df:
        return "sukmajaya"
    elif "abadi" in df:
        return "sukmajaya"
    elif "mekar" in df:
        return "sukmajaya"
    elif "japat" in df:
        return "sukmajaya"

    elif "tapos" in df:
        return "tapos"
    elif "cilangkap" in df:
        return "tapos"
    elif "sukatani" in df:
        return "tapos"
    elif "leuwi" in df:
        return "tapos"
    elif "cimpaeun" in df:
        return "tapos"
    elif "raffless" in df:
        return "tapos"

    elif "depok" in df:
        return "depok"

    else:
        return df


df["lokasi"] = df["lokasi"].apply(simplified_location)

# depok_idx = df[df['lokasi']=="depok"].index
# pick_name = df.iloc[depok_idx, ]
# df['lokasi'].iloc[depok_idx, ] = pick_name['nama']

# df['lokasi'] = df['lokasi'].apply(simplified_location)

# loc = df['lokasi'].value_counts()

# missing value diinput 'no' menandakan tidak adanya fasilitas
df["AC"] = df["AC"].fillna("no")
df["balcony"] = df["balcony"].fillna("no")
df["keamanan24jam"] = df["keamanan24jam"].fillna("no")
df["taman"] = df["taman"].fillna("no")

# input nilai mayoritas pada lahan parkir
df["lahan_parkir"] = df["lahan_parkir"].fillna(1.0)

# memperbaiki tipe data
df["kamar_tidur"] = df["kamar_tidur"].astype("int64")
df["kamar_mandi"] = df["kamar_mandi"].astype("int64")
df["lahan_parkir"] = df["lahan_parkir"].astype("int64")

# hapus row yang terdapat missing value
df = df.dropna()

# hapus kolom yang tidak dibutuhkan
df = df.drop(columns=["url", "nama"], axis=1)

# hapus Rp dan ubah tipe data pada harga
df["harga"] = df["harga"].str.split(" ", expand=True)[1]
df["harga"] = df["harga"].str.replace(".", "").astype("int64")

# periksa dan hapus row yang duplikat
var = df.drop(columns=["harga"], axis=1)
dup_idx = var[var.duplicated()].index

df = df.drop(index=dup_idx).reset_index(drop=True)

# ekspor data hasil cleaning
df.to_csv(path + "clean_df.csv", index=False)
