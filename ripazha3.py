import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
path = "/home/pwj/Desktop/aezakmi/wszystko1.csv"
df = pd.read_csv(path, encoding='utf-8', index_col=[0])

def beniaminki(df, x):
    a = set(df[df['Sezon'] == f"{x}/{x+1}"]['Drużyna'].unique())
    b = set(df[df['Sezon'] == f"{x-1}/{x}"]['Drużyna'].unique())
    c = a - b
    d = list(c)
    return d

path2 = "/home/pwj/Desktop/aezakmi/merged_data_ekstrastats.csv"
staty = pd.read_csv(path2, encoding='utf-8', index_col=[0])
temp = pd.DataFrame()

for i in range(15,24):
    x = staty[staty["Sezon"] == f"{i}/{i+1}"]
    y = x[x["Drużyna"].isin(beniaminki(staty,i)) == True]
    temp = pd.concat([temp,y], axis=0)

temp["Avg._posiadanie"] = [i[:-1] for i in temp["Avg._posiadanie"]]
temp["%_SFG"] = [i[:-1] for i in temp["%_SFG"]]
temp = temp[list(temp.columns)[2:]]
for kolumna in list(temp.columns)[6:]:
    temp[kolumna] = [float(s.replace(",", ".")) for s in temp[kolumna]]
srednie = list(temp.mean())
wektor = []
for i in range(len(srednie)):
    wektor.append(round(srednie[i], 3))

#--------------------------------------------------------------------------------------------------

for kolumna in list(df.columns)[18:29]:
    df[kolumna] = df[kolumna].astype(str)
    df[kolumna] = [float(s.replace(",", ".")) for s in df[kolumna]]
for kolumna in list(df.columns)[36:]:
    df[kolumna] = df[kolumna].astype(str)
    df[kolumna] = [float(s.replace(",", ".")) for s in df[kolumna]]
for kolumna in list(df.columns)[7:10]:
    df[kolumna] = df[kolumna].astype(str)
    df[kolumna] = df[kolumna].str.replace("-", "3.33")
    df[kolumna] = [float(s) for s in df[kolumna]]

for i in range(18):
    df[list(df.columns)[i+11]] = np.where(df[list(df.columns)[i+11]].isna() == True, wektor[i], df[list(df.columns)[i+11]])
for i in range(18):
    df[list(df.columns)[i+29]] = np.where(df[list(df.columns)[i+29]].isna() == True, wektor[i], df[list(df.columns)[i+29]])
print(df.head(20))
print(df.tail(20))
df.to_csv("wszystko2.csv", index=True)

max_scaled = df.copy()
print(max_scaled.info())
for column in list(max_scaled.columns)[11:]:
    max_scaled[column] = round(max_scaled[column] / max_scaled[column].abs().max(), 3)
print(max_scaled.head(20))

max_scaled.to_csv("znormalizowane.csv", encoding='utf-8', index=True)