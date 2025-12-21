import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scraping(url):
    service = Service(executable_path="C:\\Users\\Karol\\Desktop\\Algobetting\\projekty-i-w-ogóle\\Scraping i nie tylko\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(url)
    id = "tablepress-249_wrapper" #Has to be changed by hand, for each season of course
    try:
        login_modal = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, id)))
    finally:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    tabela = driver.find_elements(By.ID, id)
    
    stringi = []
    list = []
    for mecz in tabela:
        stringi.append(mecz.text)
        lista = stringi[-1].splitlines(keepends=False)
        list.append(lista)
        
    megalista.append(list)
    driver.close()
    return tabela

def parsing(megalista):
    tabela = []

    for drużyna in megalista:
        tabela.append(drużyna.split(" "))
        try:
            a = int(tabela[-1][1])
            tabela[-1] = tabela[-1][0:1] + tabela[-1][2:8]  
        except ValueError:
            tabela[-1][0] = tabela[-1][0] + " " + tabela[-1][1]
            tabela[-1] = tabela[-1][0:1] + tabela[-1][3:9]
    
    print(tabela[1:])
    tabela = tabela[1:]
    return tabela
    

if __name__ == '__main__':
    megalista = []
    url = f"https://ekstrastats.pl/sezon-2023-24/#symple-tab-tabele-ligowe" #Change for each season
    scraping(url)
    megalista = [x for xs in megalista for x in xs]
    megalista = megalista[0][1:]
    print(megalista)
    tabela = parsing(megalista)
    print(tabela)
    df = pd.DataFrame(tabela, columns = ['Drużyna', 'Punkty', 'Zwycięstwa', 'Remisy', 'Porażki', 'Gole_zdobyte', 'Gole_stracone'])
    df.insert(1, 'Sezon', '23/24') #Change for each season
    df.to_csv('C:\\Users\Karol\\Desktop\\Projekty do CV\\Dane per sezon Ekstrastats\\Ekstrastats_1_23_24.csv', sep=',', encoding='utf-8-sig') #Change for each season
    print(df.to_string())







