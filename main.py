#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import json
import os
import sys
import datetime
import requests
import pandas as pd
import ConfigParser

def read_price():
    df = pd.read_csv('mona_jpy_2017.csv')
    return df
    #print df['A']  # show 'A' column


def get_transactions(url, key):
    print("loading transactions from pool...")

    start_date = datetime.datetime(2017,  1, 1, 00, 00, 00)
    end_date   = datetime.datetime(2017, 12,31, 23, 59, 59)

    payload={'page': "api", 'action': "getusertransactions", 'api_key' : key, 'limit' : -1}
    r = requests.get(url+"/index.php", params=payload)
    j = r.json()
    #print(j["getusertransactions"])
    transactions = j["getusertransactions"]["data"]["transactions"]
    res = []
    for d in transactions:
        timestamp = d["timestamp"]
        amount =float(d["amount"])

        formatted_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        if(start_date <= formatted_date and formatted_date <= end_date ):
            res.append((formatted_date, amount))

        #print("{0}, {1}".format(timestamp, amount))
    return res

def main():
    # read ini
    inifile = ConfigParser.SafeConfigParser()
    inifile.read("./pool.ini")

    url     = inifile.get("info", "pool_url")
    api_key = inifile.get("info", "api_key")

    # get transaction from pool
    trans= get_transactions(url, api_key)

    prices = read_price()
    
    data_frame = pd.DataFrame(index=[], columns=['timestamp', 'amount', 'closing_price', 'acquisition_value'])
    total_value = 0.0
    total_mona  = 0.0

    for t in reversed(trans):
        price = prices[prices.date == t[0].strftime("%Y/%m/%d") ].end_price.values[0]     
        acc_value = t[1] * float(price) 
        total_value += acc_value
        total_mona  += t[1]
        print("{0}, {1}, {2}, {3}".format(t[0], t[1], price, str(acc_value)))

        series = pd.Series([t[0], t[1], price, acc_value], index=data_frame.columns)
        data_frame = data_frame.append(series, ignore_index = True)

    print("result in 2017")
    print("number of transactions: {0}".format(len(trans)))
    print("total value: {0}".format(str(total_value)))
    print("total acquisition mona: {0}".format(str(total_mona)))
    print("average acquisition value: {0}".format(str(total_value/total_mona)))

    data_frame.to_csv('./output.csv') 
main()
