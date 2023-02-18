import os
import pandas as pd
import glob
from sentimentpl.models import SentimentPLModel


# scracping tweets using command line
def scrapTwitter(accounts, tweetsSince, pathToSave):
    for account in accounts:
        os.system("chcp 65001")
        os.system("snscrape --jsonl --since {} twitter-search 'from:{}'> ./{}/tweets{}.json"
                  .format(tweetsSince, account, pathToSave, account))
        tweets = pd.read_json('./tweets/tweets' + account + '.json', lines=True)
        tweets.to_csv('./tweets/tweets' + account + '.csv', sep=';', index=False)
        os.remove('tweets' + account + '.json')
        print("Finished scraping", account, "account.")


#joining csv files
def joinCsv(pathToReadFrom, pathToSave, filename):
    files = os.listdir(pathToReadFrom)
    csvList = []
    for file in files:
        csvList.append(pd.read_csv(pathToReadFrom + file, sep=";", low_memory=False))
    csv = pd.concat(csvList, ignore_index=True)
    csv.to_csv(pathToSave + filename + '.csv', index=False, sep=";")
    print("Finished merging csv files.")


#sentiment
def analyseSentiment(filename, pathToSave):
    print("Starting... " + filename)
    df = pd.read_csv("./tweets/" + filename, sep=';', low_memory=False)
    model = SentimentPLModel(from_pretrained='latest')

    sentimentList = []
    sentimentClass = []
    for index, row in enumerate(range(len(df))):
        # check sentiment
        sentimentList.append(model(df['rawContent'][row]).item())

        # assign text class for tweet
        # neutral
        if -0.25 < model(df['rawContent'][row]).item() < 0.25:
            sentimentClass.append("Neutral")

        # positive
        elif 0.25 <= model(df['rawContent'][row]).item() < 0.75:
            sentimentClass.append("Positive")

        # very positive
        elif 0.75 <= model(df['rawContent'][row]).item() <= 1:
            sentimentClass.append("Very positive")

        # negative
        elif -0.75 < model(df['rawContent'][row]).item() <= -0.25:
            sentimentClass.append("Negative")

        # very negative
        elif -1 <= model(df['rawContent'][row]).item() <= -0.75:
            sentimentClass.append("Very negative")

        else:
            print(model(df['rawContent'][row]).item())
            print(1)

        # index printing
        if index % 1000 == 0:
            print(str(index) + "/" + str(len(df)))

    df.insert(len(df.columns), "Sentiment", sentimentList)
    df.insert(len(df.columns), "Sentiment Class", sentimentClass)
    df.to_csv(pathToSave + filename + "WithSentiment.csv", index=False, sep=";")
