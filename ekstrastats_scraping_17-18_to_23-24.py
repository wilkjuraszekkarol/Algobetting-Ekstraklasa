import pandas as pd
import requests
from bs4 import BeautifulSoup


def scraping(x):
    url = f"https://ekstrastats.pl/sezon-20{x[0]}-{x[0]+1}/#symple-tab-tabele-ligowe"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id=f'tablepress-{x[1]}')
    return table


def parsing(x, table): #Parses and creates a dataframe, for each season that is
    list = []
    for game in table:
        game = str(game)   
        list.append(game)
    list = list[2:]
    list = [y for y in list if y != '\n']
    try:
        list[-1] = list[-1].split("""<tr class="row-""")
    finally:
        pass
        #print(list)
    list = [x for xs in list for x in xs]
    list = list[1:]
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



def creating_full_df(list): #Merges all collected data into a single spreadsheet
    dfs = []
    for x in list:
        table = scraping(x)
        df = parsing(x, table)
        dfs.append(df)
    full_data = dfs[0]
    for j in range(1, len(dfs)):
        full_data = pd.concat([full_data, dfs[j]])  
    full_data = full_data.reset_index(drop=True)
    return full_data



if __name__ == '__main__':
    values = [[23,896], [22,818], [21,718], [20,629], [19,533], [18,441], [17,348]]
    full_data = creating_full_df(values)
    #print(full_data.to_string()) #Uncomment if you just want to see if code does what it's meant to do
    full_data.to_csv(f"PATH\\17-18_23-24_data_ekstrastats.csv", sep=',', encoding='utf-8-sig') #----CHANGE PATH----
    #Comment this line if you don't want to save any data





