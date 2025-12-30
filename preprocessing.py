import pandas as pd
import numpy as np


def beniaminki(df1, x): #Returns a list of new teams during each season
    a = set(df1[df1['Sezon'] == f"{x}/{x+1}"]['Drużyna'].unique())
    b = set(df1[df1['Sezon'] == f"{x-1}/{x}"]['Drużyna'].unique())
    c = a - b
    d = list(c)
    return d


def merging(df1, df2):
    df2 = df2[(df2["Sezon"] != "Dec-13") & (df2["Sezon"] != "13/14") & (df2["Sezon"] != "14/15")] #It's because df1 begins at Season 15/16
    """print(np.sort(df1['Drużyna'].unique()))
    print(np.sort(df2['Gospodarze'].unique()))
    print(np.sort(df2['Goście'].unique()))"""
    wektor_1 = ["Sandecja", "Jagiellonia Białystok", "Zawisza", "Bruk-Bet", "Termalica", "Nieciecza", "Bruk-Bet T.", "Podbeskidzie", "Podbeskidzie B-B"]
    wektor_2 = ["Sandecja Nowy Sącz", "Jagiellonia", "Zawisza Bydgoszcz", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Termalica Bruk-Bet Nieciecza", "Podbeskidzie Bielsko-Biała", "Podbeskidzie Bielsko-Biała"]
    for i in range(len(wektor_1)): 
        df1["Drużyna"].replace(wektor_1[i], wektor_2[i])
        df2["Gospodarze"].replace(wektor_1[i], wektor_2[i])
        df2["Goście"].replace(wektor_1[i], wektor_2[i])

    for i in reversed(range(14,24)): 
        df1["Sezon"] = df1["Sezon"].replace(f"{i}/{i+1}", f"{i+1}/{i+2}")

    temp1 = df1.copy()
    temp2 = df1.copy()
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

    temp3 = df2.merge(temp1, on=["Gospodarze", "Sezon"], how='left')
    df = temp3.merge(temp2, on=["Goście", "Sezon"], how='left')
    
    return df


def filling_nans(df1, df):
    temp = pd.DataFrame()
    for i in range(15,24):
        x = df1[df1["Sezon"] == f"{i}/{i+1}"]
        y = x[x["Drużyna"].isin(beniaminki(df1,i)) == True]
        temp = pd.concat([temp,y], axis=0)
    temp = temp[list(temp.columns)[2:]]
    srednie = list(temp.mean())
    wektor = []
    for i in range(len(srednie)):
        wektor.append(round(srednie[i], 3))
    print(wektor)
    #wektor = contains average values of all significant stats that every new team achieved in their first season
    #--------------------------------------
    #now we append this wektor to all new teams (to fill NaN values), column by column
    for i in range(6):
        df[list(df.columns)[i+11]] = np.where(df[list(df.columns)[i+11]].isna() == True, wektor[i], df[list(df.columns)[i+11]])
        df[list(df.columns)[i+17]] = np.where(df[list(df.columns)[i+17]].isna() == True, wektor[i], df[list(df.columns)[i+17]])

    for kolumna in list(df.columns)[7:10]: #Bugfix
        df[kolumna] = df[kolumna].astype(str)
        df[kolumna] = df[kolumna].str.replace("-", "3.33")
        df[kolumna] = [float(s) for s in df[kolumna]]
    
    return df


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    df1 = pd.read_csv("PATH\\pełne_dane_ekstrastats.csv", encoding='utf-8', index_col=[0])
    df2 = pd.read_csv("PATH\\pelne_dane_oddsportal.csv", encoding='utf-8', index_col=[0])
    df = merging(df1,df2) #This merges these two tables, while accounting for whether a team is playing at home or away
    #However, it leaves us with NaN values for where a team did not play in the previous season. Let's change that.
    df = filling_nans(df1, df)
    df.to_csv("PATH\\merged_data.csv", encoding='utf-8-sig', index=True)
    max_scaled = df.copy()
    for column in list(max_scaled.columns)[11:]:
        max_scaled[column] = round(max_scaled[column] / max_scaled[column].max(), 3)
    max_scaled.to_csv("PATH\\merged_normalized.csv", encoding='utf-8-sig', index=True)
    #Some models require us to normalize our data, better to keep both copies


