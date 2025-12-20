import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scraping(url, x, megalista):
    service = Service(executable_path="C:\\Users\\Karol\\Desktop\\Algobetting\\projekty-i-w-ogóle\\Scraping i nie tylko\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(url)
    css_selector = "div.eventRow.flex.w-full.flex-col.text-xs"
    try:
        login_modal = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    finally:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    tabela = driver.find_elements(By.CSS_SELECTOR, css_selector)

    stringi = []
    list = []
    if x[0] in (13, 14, 15, 16, 17, 18, 19):
        for mecz in tabela:
            stringi.append(mecz.text)
            stringi[-1] = stringi[-1].replace("1\nX\n2\nB","")
            if stringi[-1].count(f"20{x[0]}") == 1 or stringi[-1].count(f"20{x[0]+1}") == 1:
                lista = stringi[-1].splitlines(keepends=False)
                if lista[0].count(" - Grupa mistrzowska") == 1:
                    lista[0] = lista[0].replace(" - Grupa mistrzowska", "")
                elif lista[0].count(" - Grupa spadkowa") == 1:
                    lista[0] = lista[0].replace(" - Grupa spadkowa", "")
                else:
                    pass
                lista.remove("")
                lista.pop(-1)
                list.append(lista)
            else:
                lista = ["Data jak powyżej"]
                lista2 = stringi[-1].splitlines(keepends=False)
                lista = lista + lista2
                lista.pop(-1)
                list.append(lista)
            if lista.count('przyz.') == 1:
                lista.remove('przyz.')
            elif lista.count("Dodaj do mojego kuponu") == 1:
                lista.remove("Dodaj do mojego kuponu")
            else:
                pass
    else:
        for mecz in tabela:
            stringi.append(mecz.text)
            stringi[-1] = stringi[-1].replace("1\nX\n2\nB","")
            if stringi[-1].count(f"20{x[0]}") == 1 or stringi[-1].count(f"20{x[0]+1}") == 1:
                lista = stringi[-1].splitlines(keepends=False)
                lista.remove("")
                lista.pop(-1)
                list.append(lista)
            else:
                lista = ["Data jak powyżej"]
                lista2 = stringi[-1].splitlines(keepends=False)
                lista = lista + lista2
                lista.pop(-1)
                list.append(lista)
            if lista.count('przyz.') == 1:
                lista.remove('przyz.')
            elif lista.count("Dodaj do mojego kuponu") == 1:
                lista.remove("Dodaj do mojego kuponu")
            else:
                pass

    list[0] = list[0][5:] #Czyści pierwszy wiersz z niepotrzebnych elementów

    for mecz in list:
        try:
            if int(mecz[3]) > int(mecz[5]):
                mecz.append("Wygrali gospodarze")
            elif int(mecz[3]) < int(mecz[5]):
                mecz.append("Wygrali goście")
            else:
                mecz.append("Remis")
        except ValueError:
            list.remove(mecz)

    print(len(list)) #Sprawdza czy wszystko się wczytało. Wartość powinna wynosić 50 dla każdej strony oprócz ostatniej
    megalista.append(list)
    driver.close()
    return tabela

def tworzenie_tabeli(x, megalista):
    j = 1
    while j <= x[1]:
        if x[0] == 16:
            url = f"https://www.oddsportal.com/pl/football/poland/lotto-ekstraklasa-2016-2017/results/#/page/{j}"
        elif x[0] in (12,13,14,15,17,18):
            url = f"https://www.oddsportal.com/pl/football/poland/ekstraklasa-20{x[0]}-20{x[0]+1}/results/#/page/{j}"
        elif x[0] in (19,20,21,22,23,24):
            url = f"https://www.oddsportal.com/pl/football/poland/pko-bp-ekstraklasa-20{x[0]}-20{x[0]+1}/results/#/page/{j}"
        scraping(url, x, megalista)
        j = j+1
    megalista = [x for xs in megalista for x in xs]
    print(megalista)

    for i in range(len(megalista)):
        megalista[i].pop(4)
        if megalista[i][0] == "Data jak powyżej":
            megalista[i][0] = megalista[i-1][0]
        else:
            pass

    df = pd.DataFrame(megalista, columns = ['Data', 'Godzina', 'Gospodarze', 'Gole_gospodarze', 'Gole_goście', 'Goście', 'Oddsy_gospodarze', 'Oddsy_remis', 'Oddsy_goście', 'Kto_wygrał'])
    df.insert(2, 'Sezon', f'{x[0]}/{x[0]+1}')
    #df.to_csv(f'Sezon_{x}_{x+1}.csv', sep=',', encoding='utf-8-sig')
    print(df.to_string())
    return df


if __name__ == '__main__':
    lista = [[12, 5], [13,6], [14,6], [15,6], [16,6], [17,6], [18,6], [19,6], [20,5], [21,7], [22,7], [23,7], [24,7]]
    for i in lista:
        megalista = []
        tworzenie_tabeli(i, megalista).to_csv(f'C:\\Users\\Karol\\Desktop\\Algobetting\\projekty-i-w-ogóle\\Scraping i nie tylko\\Dane per sezon TEST\\Sezon_{i[0]}_{i[0]+1}.csv', sep=',', encoding='utf-8-sig')













