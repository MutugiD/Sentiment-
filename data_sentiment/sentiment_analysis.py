import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import math
from itertools import product
import datetime as dt
from platform import python_version
import pandas as pd 
from datetime import datetime, timedelta
import yfinance as yf

df = pd.read_csv('bitcoin-sentiment-2021-09-10.csv', parse_dates=True, index_col=0)
analyzer = SentimentIntensityAnalyzer()
df = df.set_index('date')

df['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df['tweet']] 
df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df['tweet']]
df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df['tweet']]
df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df['tweet']]


df.index = pd.to_datetime(df.index, errors='coerce',format='%Y-%m-%d %H:%M:%S')
df_resampled = df.resample('1h').mean()

df_resampled.tz_localize(None)
# df_resampled.to_csv('tweets_resampled_mean_no_weekends.csv')

"""
"""

def download_data(sign=None, start=None, interval=None, end=None):
  data = yf.download(sign, start=start, interval=interval,  end=end ,progress=False)[["Close"]]
  return data
symbol = 'BTC-USD'
start = '2021-08-27'
end = '2021-09-10'
interval = '1h'
df_coin = download_data(symbol, start=start, interval=interval,  end=end)
df_coin = df_coin.rename_axis("date")

"""
"""

combined_df = df_resampled.merge(df_coin, on ='date', how='outer').dropna()
# Calculating Log Returns Column
combined_df['returns'] = np.log(combined_df['Close'] / combined_df['Close'].shift(1))
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




