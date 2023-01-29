import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib import error

# crate matchdayLinks
seasons = ["2021"]
matchday = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
matchdayLinks = []

for season in seasons:
    for day in matchday:
        matchdayLinks.append("https://www.transfermarkt.com/pko-ekstraklasa/spieltagtabelle/wettbewerb/"
                     "PL1?saison_id={}&spieltag={}".format(season, day))



for index, link in enumerate(matchdayLinks):
    tableHeaders = []

    # opening web page
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                'Chrome/47.0.2526.106 Safari/537.36'})
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')

    # choosing table with standings
    matchdayStandingTable = soup.select(".items")[0]

    # get headers from table
    for columnName in matchdayStandingTable.find_all('th'):
        title = columnName.text
        tableHeaders.append(title)

    # add one addidtional item to header for club logo;
    # if it's not there table will not be scrapped -> mismatched columns error
    tableHeaders.insert(1, "Logo")

    # add headers to dataframes
    df = pd.DataFrame(columns = tableHeaders)
    allData = pd.DataFrame(columns = tableHeaders)

    # scrap body of table
    for j in matchdayStandingTable.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [k.text for k in row_data]
        length = len(df)
        df.loc[length] = row
        allData.loc[length] = row

    # managing columns in df
    allData.rename({"#": "Position", " ": "Matches Played", "W": "Won", "D": "Draw", "L": "Lost"},
                   inplace=True, axis='columns')

    matchdayList = []
    for dfLen in range(len(allData)):
        matchdayList.append(str(link).split("=")[2])

    allData.insert(len(allData.columns), "Matchday No", matchdayList)

    # removing characters
    allData = allData.replace('\n', '', regex=True)
    allData = allData.replace('\xa0', '', regex=True)

    # saving to csv
    if index == 0:
        allData.to_csv('test.csv', mode='a', index=False, encoding='windows-1250', sep=";", header=allData.columns)
    else:
        allData.to_csv('test.csv', mode='a', index=False, encoding='windows-1250', sep=";", header=False)


    print(1)
