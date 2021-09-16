import settings
import pandas as pd
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import re
import matplotlib.pyplot as plt 


consumer_key= ' '
consumer_secret= '  '
access_token='  '
access_token_secret='  '

auth = tweepy.OAuthHandler(consumer_key, consumer_secret )
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

search_term = '#bitcoin -filter:retweets' 
tweets = tweepy.Cursor(api.search, q=search_term, 
                       lang ='en', since ='2021-08-01', tweet_mode ='extended').items(2000)
all_tweets =[tweet.full_text for tweet in tweets]

df = pd.DataFrame(all_tweets, columns =['Tweets'])

def CleanTwt(twt): 
    twt = re.sub('#bitcoin', 'bitcoin', twt)
    twt = re.sub('#Bitcoin', 'Bitcoin', twt)
    twt = re.sub('#BTC', 'BTC', twt)
    twt = re.sub('#btc', 'btc', twt)
    twt = re.sub('#[A-Za-z0-9]+', '', twt)
    twt = re.sub('\\n', '', twt)
    twt = re.sub('https?:\/\/\S+', '', twt)
    return twt

df['Tweets_cleaned'] = df["Tweets"].apply(CleanTwt)

def getSubjectivity(twt): 
    return TextBlob(twt).sentiment.subjectivity 
def getPolarity(twt): 
    return TextBlob(twt).sentiment.polarity 

df['Subjectivity'] = df["Tweets_cleaned"].apply(getSubjectivity)
df['Polarity'] = df["Tweets_cleaned"].apply(getPolarity)

def getSentiment(score): 
    if score < 0: 
        return 'Negative'
    elif score == 0: 
        return "Neutral"
    else: 
        return "Positve"
    
df['Sentiment'] = df['Polarity'].apply(getSentiment)


# plt.figure(figsize=(8.6))
for i in range(0, df.shape[0]): 
    plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color ='purple')
plt.title("Sentiment Analysis")
plt.xlabel('Polarity')
plt.xlabel("Subjectivity")
plt.show()


df['Sentiment'].value_counts().plot(kind='bar')
plt.title("Sentiment Bar Chart")
plt.xlabel('Polarity')
plt.ylabel("Subjectivity")
plt.show()
