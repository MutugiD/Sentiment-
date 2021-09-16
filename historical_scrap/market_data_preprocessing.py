import pandas as pd
from binance.client import Client
from binance import BinanceSocketManager
from datetime import datetime
import sqlalchemy
from datetime import datetime


pair = "BTCUSDT"
engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')

df = pd.read_sql("BTCUSDT", engine)
df= df.set_index("Time")
df.index = pd.to_datetime(df.index, errors='coerce',format='%Y-%m-%d %H:%M:%S')
df_resampled = df.resample('1min').mean()

