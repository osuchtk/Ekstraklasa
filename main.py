import os

import pandas as pd
import numpy as np

from transfermarktMatchdaysDates import getMatchdaysDates
from transfermarktMatchdaysStandings import getMatchdaysStandings
from twitterPostsScraping import scrapTwitter, joinCsv, analyseSentiment


# set up scrapers
os.mkdir("./tweets")
os.mkdir("./tweetsSentiment")
seasons = ["2017", "2018", "2019", "2020", "2021"]
tweetsSince = "2017-07-14"
accounts = ["ArkaGdyniaSA", #Arka Gdynia
            "MKSCracoviaSSA", #Cracovia
            "zielono_czarni", #Gornik Leczna
            "GornikZabrzeSSA", #Górnik Zabrze
            "Jagiellonia1920", #Jagiellonia
            "Korona_Kielce", #Korona Kielce
            "LechPoznan", #Lech Poznan
            "LechiaGdanskSA", #Lechia Gdansk
            "LegiaWarszawa", #Legia Warszawa
            "LKS_Lodz", #LKS Lodz
            "MiedzLegnica", #Miedz Legnica
            "PiastGliwiceSA", #Piast Gliwice
            "TSP_SA", #Podbeskidzie
            "PogonSzczecin", #Pogon Szczecin
            "1910radomiak", #Radomiak
            "Rakow1921", #Rakow
            "SandecjaNS", #Sandecja
            "SlaskWroclawPl", #Slask Wroclaw
            "FksStalMielec", #Stal Mielec
            "BB_Termalica", #Termalica
            "WartaPoznan", #Warta Poznan
            "WislaKrakowSA", #Wisla Krakow
            "WislaPlockSA", #Wisla Plock
            "zaglebie_eu", #Zaglebie Sosnowiec
            "ZaglebieLubin" #Zaglebie Lubin
            ]
teamNames = ["Arka Gdynia",
             "Cracovia",
             "Gornik Leczna",
             "Górnik Zabrze",
             "Jagiellonia",
             "Korona Kielce",
             "Lech Poznan",
             "Lechia Gdansk",
             "Legia Warszawa",
             "LKS Lodz",
             "Miedz Legnica",
             "Piast Gliwice",
             "Podbeskidzie",
             "Pogon Szczecin",
             "Radomiak",
             "Rakow",
             "Sandecja",
             "Slask Wroclaw",
             "Stal Mielec",
             "Termalica",
             "Warta Poznan",
             "Wisla Krakow",
             "Wisla Plock",
             "Zaglebie Sosnowiec",
             "Zaglebie Lubin"]
pathToTweets = "./tweets/"
pathToTweetsWithSentiment = "./tweetsSentiment"
pathToSaveTweetsWithSenitment = "./"
tweetsWithSentimentFilename = "tweetsWithSentimentAll"

# scrap transfermarkt
getMatchdaysDates()
getMatchdaysStandings()

# scrap tweets
scrapTwitter(accounts, tweetsSince, pathToTweets)

# analyse sentiment
files = os.listdir(pathToTweets)
for file in files:
    analyseSentiment(file, pathToTweetsWithSentiment)

# join csv files
joinCsv(pathToTweetsWithSentiment, pathToSaveTweetsWithSenitment, tweetsWithSentimentFilename)

# join team names and twitter account names
arr = np.array([accounts, teamNames]).T
TeamAccount = pd.DataFrame(arr, columns=["TwitterName", "TeamName"])
TeamAccount.to_csv("TeamNameWithAccount.csv", sep=";", index=False)
