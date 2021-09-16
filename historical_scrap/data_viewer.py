import pandas as pd
import settings
import tweepy
import dataset
from datafreeze import freeze
db = dataset.connect("sqlite:///tweets.db")
result = db["tweets"].all()
freeze(result, format='csv', filename=settings.CSV_NAME)

df  = pd.read_csv(settings.CSV_NAME)