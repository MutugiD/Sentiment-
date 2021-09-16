import pandas as pd
import numpy as np
import sqlalchemy
import sqlite3
from datetime import datetime
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import math
from itertools import product
import datetime as dt
from platform import python_version
from datetime import datetime, timedelta
import pandas as pd
import tweepy
import settings 
import dataset
from datafreeze import freeze

##coin processing
coin_pair = "BTCUSDT"
coin_engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')
df_coin = pd.read_sql(coin_pair, coin_engine)
df_coin = df_coin.set_index("Time")
df_coin.index = pd.to_datetime(df_coin.index, errors='coerce',format='%Y-%m-%d %H:%M:%S')
df_coin_re = df_coin.resample('1min').mean()

####twitter processing
# twitter_engine = dataset.connect("sqlite:///tweets.db")
# result = twitter_engine["tweets"].all()
# freeze(result, format='csv', filename=settings.CSV_NAME)
df_twitter = pd.read_csv(r'E:\Python Projects\Logan\Sentiment\config\tweets.csv')
analyzer = SentimentIntensityAnalyzer()
df_twitter= df_twitter.rename(columns ={'created':'Time'})
df_twitter['Time'] = pd.to_datetime(df_twitter['Time'], errors='coerce',format='%Y-%m-%d %H:%M:%S')
df_twitter = df_twitter.set_index('Time')
df_twitter_re = df_twitter.resample('1min').mean()

###polarity 
df_twitter['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df_twitter['text']] 
df_twitter['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df_twitter['text']]
df_twitter['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df_twitter['text']]
df_twitter['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df_twitter['text']]


"""
"""
combined_df = df_twitter_re.merge(df_coin_re, on ='Time', how='outer').dropna()
# Calculating Log Returns Column
combined_df['returns'] = np.log(combined_df['Price'] / combined_df['Price'].shift(1))
# Long when the sentiment[pos > neg] and short otherwise
combined_df['position'] = np.where(combined_df['pos'] > combined_df['neg'], 1, -1)
# Create Strategy column & by multiplying SHIFTED position to avoid hindsight bias
combined_df['strategy'] = combined_df['position'].shift(1) * combined_df['returns']
combined_df.dropna(inplace=True)
combined_df.head()
np.exp(combined_df[['returns','strategy']].sum())

retl = combined_df['returns'].cumsum()
stratl = combined_df['strategy'].cumsum()
pnn = combined_df['pos'] - combined_df['neg']
plt.figure(figsize=(8,4))
plt.style.use('seaborn')
plt.plot(retl, linestyle=':', label='Return Benchmark')
plt.plot(stratl, label='Strategy')
plt.plot(pnn, linestyle='-',label='Sentiment Line')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend(loc='upper right')






