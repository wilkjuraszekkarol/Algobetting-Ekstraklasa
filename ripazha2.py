import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

path_oddsportal = "/home/pwj/Desktop/aezakmi/Pełne_dane_Oddsportal.csv" 
path_ekstrastats = "/home/pwj/Desktop/aezakmi/merged_data_ekstrastats.csv"
df1 = pd.read_csv(path_oddsportal, encoding='utf-8', index_col=[0])
df2 = pd.read_csv(path_ekstrastats, encoding='utf-8', index_col=[0])
df1 = df1[(df1["Sezon"] != "11/12") & (df1["Sezon"] != "Dec-13") & (df1["Sezon"] != "13/14") & (df1["Sezon"] != "14/15")]

w_przed = ["Jagiellonia Białystok", "Bruk-Bet T.", "Podbeskidzie B-B"]
w_po = ["Jagiellonia", "Termalica Bruk-Bet Nieciecza", "Podbeskidzie Bielsko-Biała"]
for i in range(3):
    df1["Gospodarze"] = df1["Gospodarze"].replace(w_przed[i], w_po[i])
    df1["Goście"] = df1["Goście"].replace(w_przed[i], w_po[i])

for i in reversed(range(14,24)):
    df2["Sezon"] = df2["Sezon"].replace(f"{i}/{i+1}", f"{i+1}/{i+2}")

df2["Avg._posiadanie"] = [i[:-1] for i in df2["Avg._posiadanie"]]
df2["%_SFG"] = [i[:-1] for i in df2["%_SFG"]]
temp1 = df2.copy()
temp2 = df2.copy()
temp1.columns = temp1.columns.str.replace('Drużyna', 'Gospodarze')
lista1 = list(temp1.columns)
for i in range(2, len(lista1)):
    lista1[i] = lista1[i] + "_Gospodarze"
temp1.columns = lista1
temp2.columns = temp2.columns.str.replace('Drużyna', 'Goście')
lista2 = list(temp2.columns)
for i in range(2, len(lista2)):
    lista2[i] = lista2[i] + "_Goście"
temp2.columns = lista2

temp3 = df1.merge(temp1, on=["Gospodarze", "Sezon"], how='left')
temp3.to_csv("temp3.csv", index=True, encoding='utf-8')
df = temp3.merge(temp2, on=["Goście", "Sezon"], how='left')
print(df.tail(20))

mean1 = round(df[df['Avg.spalone_Gospodarze'] != "Brak danych"] & df[df['Avg.spalone_Gospodarze'] != np.nan]['Avg.spalone_Gospodarze'].mean(), 3)
mean2 = round(df[df['Avg.spalone_Goście'] != "Brak danych"] & df[df['Avg.spalone_Goście'] != np.nan]['Avg.spalone_Goście'].mean(), 3)
df['Avg.spalone_Gospodarze'] = np.where(df['Avg.spalone_Gospodarze'] == "Brak danych", mean1, df['Avg.spalone_Gospodarze'])
df['Avg.spalone_Goście'] = np.where(df['Avg.spalone_Goście'] == "Brak danych", mean1, df['Avg.spalone_Goście'])
df.to_csv("wszystko1.csv", index=True, encoding='utf-8')







