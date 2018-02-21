#!/usr/bin/env python
# 
import json
import os
import sys
import datetime
import requests

def main():
    payload={'fsym': "MONA", 'tsym': "JPY", 'limit':365}
    r = requests.get("https://min-api.cryptocompare.com/data/histoday", params=payload)
    j = r.json()
    print(j["Response"])
    if j["Response"] == "Success":
        for d in j["Data"]:
            timestamp = d["time"]
            open_price = d["open"]

            textualdate = datetime.datetime.fromtimestamp(timestamp)
            print("{0}, {1}, open = {2}".format(timestamp, textualdate, open_price))

main()
