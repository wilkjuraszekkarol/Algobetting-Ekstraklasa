import pandas as pd
import requests
from bs4 import BeautifulSoup

def scraping(x):
    url = f"https://ekstrastats.pl/sezon-20{x[0]}-{x[0]+1}/#symple-tab-tabele-ligowe"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tabela = soup.find('table', id=f'tablepress-{x[1]}')
    return tabela

def parsing(x, tabela):
    list = []
    for mecz in tabela:
        mecz = str(mecz)   
        list.append(mecz)
    list = list[2:]
    list = [y for y in list if y != '\n']
    try:
        list[-1] = list[-1].split("""<tr class="row-""")
    finally:
        print(list)
    list = [x for xs in list for x in xs]
    list = list[1:]
    #print(len(list))
    for i in range(len(list)):
        list[i] = list[i][29:]
        for j in range(2,10):
            list[i] = list[i].replace(f"""</td><td class="column-{j}">""", ";")
        list[i] = list[i].replace("""</td><td class="column-10"> """, ";")
        list[i] = list[i].replace("""    </td><td class="column-11"> """, ";")
        list[i] = list[i].replace("""    </td><td class="column-12"> """, ";")
        list[i] = list[i].replace("""    </td>\n</tr>\n""", "")
        list[i] = list[i].split(";")
        if list[i][0].startswith(">") == True:
            list[i][0] = list[i][0][1:]
        elif list[i][0].startswith('"') == True:
            list[i][0] = list[i][0][2:]
        list[i] = list[i][:8]
        for j in range(1,8):
            list[i][j] = int(list[i][j])
        list[i].pop(1)
        
    df = pd.DataFrame(list, columns = ['Drużyna', 'Punkty', 'Zwycięstwa', 'Remisy', 'Porażki', 'Gole_zdobyte', 'Gole_stracone'])
    df.insert(1, 'Sezon', f"{x[0]}/{x[0]+1}")
    return df

if __name__ == '__main__':
    lista_dfow = []
    lista = [[23,896], [22,818], [21,718], [20,629], [19,533], [18,441], [17,348]]
    for x in lista:
        tabela = scraping(x)
        df = parsing(x, tabela)
        lista_dfow.append(df)
    pelne_dane = lista_dfow[0]
    for j in range(1, len(lista_dfow)):
        pelne_dane = pd.concat([pelne_dane, lista_dfow[j]])  
    pelne_dane = pelne_dane.reset_index(drop=True)
    pelne_dane.to_csv(f"PATH\\17-18_23-24_dane_ekstrastats.csv", sep=',', encoding='utf-8-sig')





