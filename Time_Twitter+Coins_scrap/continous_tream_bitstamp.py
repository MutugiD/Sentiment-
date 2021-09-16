import requests
import time
import datetime

f_name = "live_bitcoin_cap.csv"
f = open(f_name,"a")
keys = ["price_usd","24h_volume_usd","market_cap_usd","available_supply","total_supply","percent_change_1h","percent_change_24h","percent_change_7d"]
vals = [0]*len(keys)


while True:
    i=1
    data = requests.get(f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?id={i}").json()
   
    # bstamp = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/").json() 
    bkc = requests.get("https://blockchain.info/ticker").json()
    for d in data.keys():
        if d in keys:
            indx = keys.index(d)
            vals[indx] = data[d]
    for val in vals:
        f.write(str(val))
      
    # f.write("{},{},".format(bstamp["volume"],bstamp["vwap"]))
    f.write("{},{},{}".format(bkc["USD"]["sell"],bkc["USD"]["buy"],bkc["USD"]["15m"]))
    f.write(","+datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
    f.write("\n")
    f.flush()
    time.sleep(60)