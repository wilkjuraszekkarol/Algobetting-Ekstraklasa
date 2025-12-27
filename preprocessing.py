import pandas as pd
import numpy as np

def preprocessing0(df2,df3):
    wektor_1 = ["Jagiellonia Białystok", "Bruk-Bet", "Podbeskidzie", "Sandecja", "Sandecja Nowy", "Termalica Nieciecza", "Termalica", "Bruk-Bet Nieciecza", "Zawisza"]
    wektor_2 = ["Jagiellonia", "Termalica Bruk-Bet Nieciecza", "Podbeskidzie Bielsko-Biała", "Sandecja Nowy Sącz", "Sandecja Nowy Sącz", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Zawisza Bydgoszcz"]
    for i in range(len(wektor_1)):
        df3["Drużyna"] = df3["Drużyna"].replace(wektor_1[i], wektor_2[i])
        df2["Drużyna"] = df2["Drużyna"].replace(wektor_1[i], wektor_2[i])
    df23 = df2.merge(df3, on=['Drużyna', 'Sezon'], how='left')
    srednia = round((np.array([float(s.replace(",", ".")) for s in df23[df23['Avg.spalone'] != "Brak danych"]['Avg.spalone']])).mean(), 3)
    df23['Avg.spalone'] = np.where(df23['Avg.spalone'] == "Brak danych", str(srednia).replace(".", ","), df23['Avg.spalone'])
    return df23


def preprocessing1(df1, df2):
    wektor_1 = ["Sandecja", "Zawisza", "Bruk-Bet", "Termalica", "Nieciecza", "Podbeskidzie"]
    wektor_2 = ["Sandecja Nowy Sącz", "Zawisza Bydgoszcz", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Podbeskidzie Bielsko-Biała"]
    for i in range(len(wektor_1)):
        df2["Drużyna"] = df2["Drużyna"].replace(wektor_1[i], wektor_2[i])
        df1["Drużyna"] = df1["Drużyna"].replace(wektor_1[i], wektor_2[i])
    merged = df1.merge(df2, on=['Drużyna','Sezon'], how='left')
    return merged


def preprocessing2(df1,df2):
    df1 = df1[(df1["Sezon"] != "11/12") & (df1["Sezon"] != "Dec-13") & (df1["Sezon"] != "13/14") & (df1["Sezon"] != "14/15")]
    w_przed = ["Jagiellonia Białystok", "Bruk-Bet T.", "Podbeskidzie B-B"]
    w_po = ["Jagiellonia", "Termalica Bruk-Bet Nieciecza", "Podbeskidzie Bielsko-Biała"]
    for i in range(len(w_przed)):
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
    df = temp3.merge(temp2, on=["Goście", "Sezon"], how='left')
    return df

def beniaminki(df, x):
    a = set(df[df['Sezon'] == f"{x}/{x+1}"]['Drużyna'].unique())
    b = set(df[df['Sezon'] == f"{x-1}/{x}"]['Drużyna'].unique())
    c = a - b
    d = list(c)
    return d

def preprocessing3(staty, df):
    temp = pd.DataFrame()
    for i in range(15,24):
        x = staty[staty["Sezon"] == f"{i}/{i+1}"]
        y = x[x["Drużyna"].isin(beniaminki(staty,i)) == True]
        temp = pd.concat([temp,y], axis=0)

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
    df['Avg._posiadanie_Gospodarze'] = df['Avg._posiadanie_Gospodarze'].astype(float)
    df['Avg._posiadanie_Goście'] = df['Avg._posiadanie_Goście'].astype(float)

    for i in range(18):
        df[list(df.columns)[i+11]] = np.where(df[list(df.columns)[i+11]].isna() == True, wektor[i], df[list(df.columns)[i+11]])
    for i in range(18):
        df[list(df.columns)[i+29]] = np.where(df[list(df.columns)[i+29]].isna() == True, wektor[i], df[list(df.columns)[i+29]])
    
    return df





if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    path1 = "C:\\Users\\Karol\\Desktop\\Projekty do CV\\pełne_dane_Ekstrastats1.csv"
    path2 = "C:\\Users\\Karol\\Desktop\\Projekty do CV\\pełne_dane_Ekstrastats2.csv"
    path3 = "C:\\Users\\Karol\\Desktop\\Projekty do CV\\pełne_dane_Ekstrastats3.csv"
    path_oddsportal = "C:\\Users\\Karol\\Desktop\\Projekty do CV\\Pełne_dane_Oddsportal.csv"
    df1 = pd.read_csv(path1, encoding='utf-8', index_col=[0])
    df2 = pd.read_csv(path2, encoding='utf-8', index_col=[0])
    df3 = pd.read_csv(path3, encoding='utf-8', index_col=[0])
    df4 = pd.read_csv(path_oddsportal, encoding='utf-8', index_col=[0])
    df23 = preprocessing0(df2, df3)
    merged_staty_ekstrastats = preprocessing1(df1, df23)
    merged = preprocessing2(df4, merged_staty_ekstrastats)
    df = preprocessing3(merged_staty_ekstrastats, merged)

    df.to_csv("C:\\Users\\Karol\\Desktop\\Projekty do CV\\wszystko.csv", index=True, encoding='utf-8-sig')
    max_scaled = df.copy()
    
    for column in list(max_scaled.columns)[11:]:
        max_scaled[column] = round(max_scaled[column] / max_scaled[column].max(), 3)
    max_scaled.to_csv("C:\\Users\\Karol\\Desktop\\Projekty do CV\\wszystko_znormalizowane.csv", encoding='utf-8-sig', index=True)

