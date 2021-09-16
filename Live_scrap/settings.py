TRACK_TERMS = ["Bitcoin", "BTC", "$BTC"]
CONNECTION_STRING = "sqlite:///tweets_1min.db"
CSV_NAME = "tweets_1min.csv"
TABLE_NAME = "tweets_1min"

try:
    from private import *
except Exception:
    pass
