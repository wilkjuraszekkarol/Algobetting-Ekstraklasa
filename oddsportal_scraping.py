import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd



def scraping(url, x, megalist):
    service = Service(executable_path="PATH\\chromedriver.exe") #Ensure that you have a working chromedriver and that its' PATH is correct
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(url)
    css_selector = "div.eventRow.flex.w-full.flex-col.text-xs"
    try:
        login_modal = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))) #Ensures that we wait exactly as long as we have to, no more no less
    finally:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #Ensures that we actually load the entire site
    time.sleep(2)
    table = driver.find_elements(By.CSS_SELECTOR, css_selector)
    #-------------
    strings = []
    list = []
    if x[0] in (13, 14, 15, 16, 17, 18, 19): #A lot of parsing
        for game in table:
            strings.append(game.text)
            strings[-1] = strings[-1].replace("1\nX\n2\nB","")
            if strings[-1].count(f"20{x[0]}") == 1 or strings[-1].count(f"20{x[0]+1}") == 1:
                small_list = strings[-1].splitlines(keepends=False)
                if small_list[0].count(" - Grupa mistrzowska") == 1:
                    small_list[0] = small_list[0].replace(" - Grupa mistrzowska", "")
                elif small_list[0].count(" - Grupa spadkowa") == 1:
                    small_list[0] = small_list[0].replace(" - Grupa spadkowa", "")
                else:
                    pass
                small_list.remove("")
                small_list.pop(-1)
                list.append(small_list)
            else:
                small_list = ["Data jak powyżej"]
                small_list2 = strings[-1].splitlines(keepends=False)
                small_list = small_list + small_list2
                small_list.pop(-1)
                list.append(small_list)
            if small_list.count('przyz.') == 1:
                small_list.remove('przyz.')
            elif small_list.count("Dodaj do mojego kuponu") == 1:
                small_list.remove("Dodaj do mojego kuponu")
            else:
                pass
    else:
        for game in table:
            strings.append(game.text)
            strings[-1] = strings[-1].replace("1\nX\n2\nB","")
            if strings[-1].count(f"20{x[0]}") == 1 or strings[-1].count(f"20{x[0]+1}") == 1:
                small_list = strings[-1].splitlines(keepends=False)
                small_list.remove("")
                small_list.pop(-1)
                list.append(small_list)
            else:
                small_list = ["Data jak powyżej"]
                small_list2 = strings[-1].splitlines(keepends=False)
                small_list = small_list + small_list2
                small_list.pop(-1)
                list.append(small_list)
            if small_list.count('przyz.') == 1:
                small_list.remove('przyz.')
            elif small_list.count("Dodaj do mojego kuponu") == 1:
                small_list.remove("Dodaj do mojego kuponu")
            else:
                pass

    list[0] = list[0][5:] #Cleans the first row from unnecessary scraps

    for game in list:
        try:
            if int(game[3]) > int(game[5]):
                game.append("Wygrali gospodarze")
            elif int(game[3]) < int(game[5]):
                game.append("Wygrali goście")
            else:
                game.append("Remis")
        except ValueError:
            list.remove(game)

    print(len(list)) #Checks if everything actually loaded. Value should be exactly 50 for every page except the last one (for each season)
    megalist.append(list)
    driver.close()
    return table



def creating_df(x, megalist): #Creates a dataframe for each season
    j = 1
    while j <= x[1]:
        if x[0] == 16:
            url = f"https://www.oddsportal.com/pl/football/poland/lotto-ekstraklasa-2016-2017/results/#/page/{j}"
        elif x[0] in (12,13,14,15,17,18):
            url = f"https://www.oddsportal.com/pl/football/poland/ekstraklasa-20{x[0]}-20{x[0]+1}/results/#/page/{j}"
        elif x[0] in (19,20,21,22,23,24):
            url = f"https://www.oddsportal.com/pl/football/poland/pko-bp-ekstraklasa-20{x[0]}-20{x[0]+1}/results/#/page/{j}"
        scraping(url, x, megalist)
        j = j+1
    megalist = [x for xs in megalist for x in xs]
    print(megalist)

    for i in range(len(megalist)):
        megalist[i].pop(4)
        if megalist[i][0] == "Data jak powyżej":
            megalist[i][0] = megalist[i-1][0]
        else:
            pass

    df = pd.DataFrame(megalist, columns = ['Data', 'Godzina', 'Gospodarze', 'Gole_gospodarze', 'Gole_goście', 'Goście', 'Oddsy_gospodarze', 'Oddsy_remis', 'Oddsy_goście', 'Kto_wygrał'])
    df.insert(2, 'Sezon', f'{x[0]}/{x[0]+1}')
    print(df.to_string())
    return df


def creating_full_df(list): #Merges all collected data into a single spreadsheet
    dfs = []
    for i in list:
        megalist = []
        df = creating_df(i, megalist)
        dfs.append(df)
    full_data = dfs[0]
    for j in range(1, len(dfs)):
        full_data = pd.concat([full_data, dfs[j]])
    full_data = full_data.reset_index(drop=True)
    return full_data


if __name__ == '__main__':
    values = [[24,7], [23,7], [22,7], [21,7], [20,5], [19,6], [18,6], [17,6], [16,6], [15,6], [14,6], [13,6], [12,5]]
    full_data = creating_full_df(values)
    #print(full_data.to_string()) Uncomment if you only want to see how the spreadsheet presents itself
    full_data.to_csv(f"PATH\\pelne_dane_oddsportal.csv", sep=',', encoding='utf-8-sig') #Set up a PATH if you want to save this dataframe on your device













