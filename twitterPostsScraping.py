import os
import pandas as pd
import glob
from sentimentpl.models import SentimentPLModel

# declaring date from which download posts and accounts names
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

# scracping tweets using command line
# for account in accounts:
#     os.system("chcp 65001")
#     os.system("snscrape --jsonl --since {} twitter-search 'from:{}'> tweets{}.json"
#               .format(tweetsSince, account, account))
#     tweets = pd.read_json('tweets' + account + '.json', lines=True)
#     tweets.to_csv('tweets' + account + '.csv', sep=';', index=False)
#     os.remove('tweets' + account + '.json')
#     print("Finished scraping", account, "account.")


#joining csv files
# files = os.listdir("./tweets/")
# csvList = []
# for file in files:
#     csvList.append(pd.read_csv("./tweets/" + file, sep=";"))
# csv = pd.concat(csvList, ignore_index=True)
# csv.to_csv("./tweets/" + 'tweetsAll.csv', index=False, sep=";")


#sentiment
df = pd.read_csv("./tweets/tweetsALL.csv", sep=';', low_memory=False)
model = SentimentPLModel(from_pretrained='latest')
sentimentList = []
sentimentClass = []

for row in range(len(df)):
    sentimentList.append(model(df['rawContent'][row]).item())

    # assign text class for tweet
    # neutral
    if -0.25 < model(df['rawContent'][row]).item() < 0.25:
        sentimentClass.append("Neutral")

    # positive
    if 0.25 <= model(df['rawContent'][row]).item() < 0.75:
        sentimentClass.append("Positive")

    # very positive
    if 0.75 <= model(df['rawContent'][row]).item() < 1:
        sentimentClass.append("Very positive")

    # negative
    if -0.25 <= model(df['rawContent'][row]).item() < -0.75:
        sentimentClass.append("Negative")

    # very negative
    if -0.75 <= model(df['rawContent'][row]).item() < -1:
        sentimentClass.append("Very negative")

df.insert(len(df.columns), "Sentiment", sentimentList)
df.insert(len(df.columns), "Sentiment Class", sentimentClass)
df.to_csv("./tweets/" + 'tweetsAllWithSentiment.csv', index=False, sep=";")

