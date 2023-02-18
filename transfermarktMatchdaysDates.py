import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def getMatchdaysDates(seasons):
    # creating links
    matchday = list(np.arange(1, 41, 1))
    matchdayLinks = []

    for season in seasons:
        # creating links
        for day in matchday:
            matchdayLinks.append("https://www.transfermarkt.com/pko-ekstraklasa/spieltag/wettbewerb/PL1/"
                                 "saison_id/{}/spieltag/{}".format(season, day))


    for index, link in enumerate(matchdayLinks):
        # opening web page
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                    'Chrome/47.0.2526.106 Safari/537.36'})
        page = urlopen(req)
        soup = BeautifulSoup(page, 'lxml')

        # choosing tables tds with home and away team, scores and match date;
        # I'm not doing this in loop because table doesn't have any class, and it would be pointless trying to find
        # right tables
        teamHome = soup.select(".rechts.hauptlink.no-border-rechts.hide-for-small.spieltagsansicht-vereinsname")
        teamAway = soup.select(".hauptlink.no-border-links.no-border-rechts.hide-for-small.spieltagsansicht-vereinsname")

        result = soup.select(".zentriert.hauptlink.no-border-rechts.no-border-links.spieltagsansicht-ergebnis")
        matchDate = soup.select(".zentriert.no-border")[0::2]
        teamHomeList = []
        teamAwayList = []
        resultHomeList = []
        resultAwayList = []
        dateList = []
        for home, away, res, date in zip(teamHome, teamAway, result, matchDate):
            try:
                teamHomeList.append(home.text.split(")")[1].replace("\n", "").replace("\t", "").replace("\xa0", "")[0:-1])
                teamAwayList.append(away.text.split("(")[0].replace("\n", "").replace("\t", "").replace("\xa0", ""))
            except IndexError:
                teamHomeList.append(home.text.replace("\n", "")[0:-1])
                teamAwayList.append(away.text.replace("\n", "")[0:-1])

            try:
                resultHomeList.append(res.text.split(":")[0].replace("\n", ""))
                resultAwayList.append(res.text.split(":")[1].replace("\n", ""))
            except IndexError:
                resultHomeList.append("")
                resultAwayList.append("")

            dateList.append(date.text.split("\n")[2].replace("  ", ""))

        # creating dataframe, adding season and matchday
        allData = pd.DataFrame([teamHomeList, teamAwayList, resultHomeList, resultAwayList, dateList]).T
        allData.columns = ["Home Team", "Away Team", "Home Goals", "Away Goals", "Date"]

        matchdayList = []
        seasonList = []
        seasonValue = str(link).split("/")[8]
        for dfLen in range(len(allData)):
            matchdayList.append(str(link).split("/")[10])
            seasonList.append(str(seasonValue) + "/" + str(int(seasonValue) + 1))

        allData.insert(len(allData.columns), "Matchday No", matchdayList)
        allData.insert(len(allData.columns), "Season", seasonList)

        # saving to csv
        if index == 0:
            allData.to_csv('matchdaysDates.csv', mode='a', index=False, encoding='windows-1250', sep=";",
                           header=allData.columns)
        else:
            allData.to_csv('matchdaysDates.csv', mode='a', index=False, encoding='windows-1250', sep=";", header=False)

    print("Finished scraping matchdays dates")
