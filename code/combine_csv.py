# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 18:34:30 2023

@author: anggapark
"""

import os
import pandas as pd

print(os.listdir("dataset/"))

df1 = pd.read_csv("dataset/hp1to6.csv")
df2 = pd.read_csv("dataset/hp7to12.csv")
df3 = pd.read_csv("dataset/hp13to18.csv")
df4 = pd.read_csv("dataset/hp19to24.csv")
df5 = pd.read_csv("dataset/hp25to30.csv")
df6 = pd.read_csv("dataset/hp31to36.csv")
df7 = pd.read_csv("dataset/hp37to42.csv")
df8 = pd.read_csv("dataset/hp43to48.csv")
df9 = pd.read_csv("dataset/hp49to54.csv")
df10 = pd.read_csv("dataset/hp55to60.csv")
df11 = pd.read_csv("dataset/hp61to66.csv")
df12 = pd.read_csv("dataset/hp67to72.csv")
df13 = pd.read_csv("dataset/hp73to78.csv")
df14 = pd.read_csv("dataset/hp79to84.csv")
df15 = pd.read_csv("dataset/hp85to90.csv")
df16 = pd.read_csv("dataset/hp91to96.csv")
df17 = pd.read_csv("dataset/hp97to100.csv")

df = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15,df16,df17])

df.to_csv("raw_df.csv", index=False)
