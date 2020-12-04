#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:36 2019

@author: ubuntu
"""

import binance as bi
import markets_op as mo
#import trade as tr
import time, datetime
#from pandas import Series, DataFrame


def get_markets_to_dataframe():
    usd_markets_list = mo.get_markets_list(client, min_vol=500000, symbol='USDT', max_markets=0)
    df_usd_markets = mo.balances_to_dataframe(client, usd_markets_list)
    print(df_usd_markets)
    path = 'Markets/usd_markets.csv'
    df_usd_markets.to_csv(path)

def log_balance(text):
    file = open(log_path, 'a')
    file.write(text + '\n')
    file.close


api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)
#log_path = 'logETH_' + str(datetime.datetime.now()) + '.txt'
log_path = 'log.txt'

#trading()
while True:
    usd_markets_list = mo.get_markets_list(client, min_vol=500000, symbol='USDT', max_markets=0)
    mo.log_data(client, usd_markets_list)
    time.sleep(900)     #au 15 min