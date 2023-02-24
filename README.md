# Ekstraklasa - tweets and position.
Analyse if there is any correlation between place in polish Ekstraklasa and amount of clubs posts on Twitter.


## How does it work?
All football data (e.g. points, positions, number of won and lost matches, etc.) are scraped from Transfermarkt using Python scripts.
Tweets are downloaded using [snscrape](https://github.com/JustAnotherArchivist/snscrape) and then I'm analysing their sentiment using [sentimentPL](https://github.com/philvec/sentimentPL). Links to Twitter accounts are gathered manually - I tried to scrap them from Ekstraklasa webpage, but unfortunately not all clubs had links included.
Report is prepared in Power BI and consists of 3 pages:
- summarization - position of clubs in table, avarage value of sentiment with anomalies and amount of tweets in each  of 5 classes (very positive, positvie, neutal, negative, very negative)
- tweets - list of tweets with class and sentiment value (by analysing value and class can there be spotted tweets which were wrongly classified), percent of tweets in each class and daily amount of tweets
- correlation - correlation between place at the end of the season and number of tweets (there is option to view all tweets and from specific class), number of won and lost matches 


![page1](https://user-images.githubusercontent.com/56642926/221175700-00e8c1ee-3127-4d46-8663-1fd51222216c.png)
![page2](https://user-images.githubusercontent.com/56642926/221175709-0f4063f3-0e48-48a9-a225-0186c0f199ad.png)
![page3](https://user-images.githubusercontent.com/56642926/221176073-46691d4a-b109-4e7d-a20d-400a760fc6cd.png)
