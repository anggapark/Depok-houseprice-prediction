# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 06:21:47 2023

@author: anggapark
"""

import pandas as pd
import numpy as np

path = "../ML-project-Depok-houseprice-prediction/"
df = pd.read_csv(path + "raw_df.csv")

df = df.rename(
        columns={
                'rumah_url': 'url', 'rumah_nama': 'nama', 'rumah_lokasi': 'lokasi', 
                'rumah_harga': 'harga', 'rumah_kamar_tidur': 'kamar_tidur', 
                'rumah_kamar_mandi': 'kamar_mandi', 'rumah_luas_bangunan': 'luas_bangunan', 
                'rumah_fully_furnished': 'fully_furnished','rumah_keamanan': 'keamanan24jam', 
                'rumah_kolam_renang': 'kolam_renang', 'rumah_taman': 'taman',
                'rumah_lahan_parkir': 'lahan_parkir', 'rumah_jumlah_lantai': 'jumlah_lantai', 
                'rumah_balcony': 'balcony', 'rumah_AC': 'AC'
                }
              )

# periksa missing value
df.isnull().sum().sort_values(ascending=0)

# pada hasil scraping, terdapat baris yang hanya terdapat url tanpa fitur rumah lainnya, baris tersebut dihapus
missing_idx = df[(df['harga'].isnull())].index
df = df.drop(index=missing_idx)

# fully_furnished, kolam_renang missing, dan jumlah_lantai memiliki missing data >90%, 
df = df.drop(columns=["fully_furnished", "kolam_renang", "jumlah_lantai"], axis=1)

# menyederhanakan lokasi
df["nama"] = df["nama"].apply(lambda x: x.lower())
df["lokasi"] = df["lokasi"].apply(lambda x: x.lower())

def simplified_location(df):
    """
    fungsi ini untuk menyederhanakan nilai pada kolom lokasi
    dengan mengambil nama kecamatan
    """
    if "beji" in df:
        return "beji"
    elif "tanah baru" in df:
        return "beji"
    elif "bojongsari" in df:
        return "bojongsari"
    elif "pondokpetir" in df:
        return "bojongsari"
    elif "curug" in df:
        return "bojongsari"
    elif "cilodong" in df:
        return "cilodong"
    elif "jatimulya" in df:
        return "cilodong"
    elif "kalimulya" in df:
        return "cilodong"
    elif "kalibaru" in df:
        return "cilodong"
    elif "cimanggis" in df:
        return "cimanggis"
    elif "cimanggis" in df:
        return "cimanggis"
    elif "tugu" in df:
        return "cimanggis"
    elif "cinere" in df:
        return "cinere"
    elif "cipayung" in df:
        return "cipayung"
    elif "citayam" in df:
        return "cipayung"
    elif "limo" in df:
        return "limo"
    elif "pancoran mas" in df:
        return "pancoran mas"
    elif "rangkapan jaya" in df:
        return "pancoran mas"
    elif "margonda" in df:
        return "pancoran mas"
    elif "mampang" in df:
        return "pancoran mas"
    elif "sawangan" in df:
        return "sawangan"
    elif "bedahan" in df:
        return "sawangan"
    elif "pengasinan" in df:
        return "sawangan"
    elif "cinangka" in df:
        return "sawangan"
    elif "sukmajaya" in df:
        return "sukmajaya"
    elif "baktijaya" in df:
        return "sukmajaya"
    elif "tapos" in df:
        return "tapos"
    elif "cilangkap" in df:
        return "tapos"
    
    else:
        return df
    
df['lokasi'] = df['lokasi'].apply(simplified_location)
    
df['lokasi'].value_counts()
    
    
    
    
    
    
    