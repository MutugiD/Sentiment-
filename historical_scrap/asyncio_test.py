#https://www.youtube.com/watch?v=rc_Y6rdBqXM
#https://www.analyticsvidhya.com/blog/2020/08/analysing-streaming-tweets-with-python-and-postgresql/
import numpy as np 
import pandas as pd
from binance.client import Client
from binance import BinanceSocketManager
from datetime import datetime
import sqlalchemy
from datetime import datetime
import asyncio
import nest_asyncio
import time

API_KEY = 'jjfjfjejeh@keys'
API_SECRET = 'eyyrwwrtrtwtr@keys'
from binance.enums import *
client = Client(API_KEY, API_SECRET)
pair = "BTCUSDT"
bm= BinanceSocketManager(client)
# socket = bm.kline_socket(pair, interval=KLINE_INTERVAL_1MINUTE)
socket = bm.trade_socket(pair)
engine = sqlalchemy.create_engine('sqlite:///BTCUSDT_1minstream.db')
def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s', 'E', 'p']]
    df.columns = ['Symbol', 'Time', 'Price']
    df.Price= df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit = 'ms')
    return df 
async def main():
    while True:
        await socket.__aenter__()
        msg = await socket.recv()
        frame = createframe(msg)
        frame.to_sql(pair, engine, if_exists='append', index=False)
        print (frame)
        time.sleep(60)
nest_asyncio.apply()   
asyncio.run(main())




