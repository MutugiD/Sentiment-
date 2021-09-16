import pandas as pd
import numpy as np
import csv
import snscrape.modules.twitter as sntwitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime as dt
import time
from timeit import default_timer as timer
from platform import python_version
from datetime import datetime, timedelta
##################
keyword = "bitcoin"
##################

start = timer()
maxTweets = 1000000

look_back = 30
now = datetime.now()
now = now.strftime('%Y-%m-%d')
days_count = datetime.now() - timedelta(days = look_back)
days_count = days_count.strftime('%Y-%m-%d')


csvFile = open(keyword + '-sentiment-' + now + '.csv', 'a', newline='', encoding='utf8')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['id','Date','tweet',])
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' lang:en since:' +  days_count + ' until:' + now + ' -filter:links -filter:replies').get_items()):
        if i > maxTweets :
            break
        csvWriter.writerow([tweet.id, tweet.date, tweet.content])
csvFile.close()

df = pd.read_csv(keyword +'-sentiment-{}'.format(look_back) + now + '.csv', parse_dates=True, index_col=0)
analyzer = SentimentIntensityAnalyzer()
df['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df['tweet']]
df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df['tweet']]
df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df['tweet']]
df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df['tweet']]
avg_compound = np.average(df['compound'])
avg_neg = np.average(df['neg']) * -1  # Change neg value to negative number for clarity
avg_neu = np.average(df['neu'])
avg_pos = np.average(df['pos'])
count = len(df.index)
print("Since yesterday there has been", count ,  "tweets on " + keyword, end='\n*')
print("Positive Sentiment:", '%.2f' % avg_pos, end='\n*')
print("Neutral Sentiment:", '%.2f' % avg_neu, end='\n*')
print("Negative Sentiment:", '%.2f' % avg_neg, end='\n*')
print("Compound Sentiment:", '%.2f' % avg_compound, end='\n')

elapsed_time = (timer() - start) / 60 # in seconds
print("Program Executed in", '%.2f' % elapsed_time, "minutes")
