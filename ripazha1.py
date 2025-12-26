import pandas as pd
import numpy as np

path1 = "/home/pwj/Desktop/aezakmi/pełne_dane_Ekstrastats1.csv"
path23 = "/home/pwj/Desktop/aezakmi/pełne_dane_Ekstrastats23.csv"
df1 = pd.read_csv(path1, encoding='utf-8', index_col=[0])
df23 = pd.read_csv(path23, encoding='utf-8', index_col=[0])

"""
print(df1["Drużyna"].unique())
print(len(df1["Drużyna"].unique()))
print("----------")
print(len(df23["Drużyna"].unique()))
print(df23["Drużyna"].unique())"""

wektor23_1 = ["Sandecja", "Zawisza", "Bruk-Bet", "Termalica", "Nieciecza", "Podbeskidzie"]
wektor23_2 = ["Sandecja Nowy Sącz", "Zawisza Bydgoszcz", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Podbeskidzie Bielsko-Biała"]
for i in range(6):
    df23["Drużyna"] = df23["Drużyna"].replace(wektor23_1[i], wektor23_2[i])
    df1["Drużyna"] = df1["Drużyna"].replace(wektor23_1[i], wektor23_2[i])

merged = df1.merge(df23, on=['Drużyna','Sezon'], how='left')
#merged = merged.drop(0)
#merged = merged.drop('Unnamed: 0_x')
print(merged.head(20))

merged.to_csv("merged_data_ekstrastats.csv", index=True)





