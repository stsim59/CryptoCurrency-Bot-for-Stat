#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 11:25:28 2019

@author: pi

1200 requests per minute
10 orders per second
100,000 orders per 24hrs : 70 calls per minutes

"""

import binance as bi
import markets_op as mo
import datetime
import time

def get_markets_btc():
    btc_markets = mo.get_markets_list(client, min_vol=1, max_markets=0)
    
    df_btc_market = mo.balances_to_dataframe(client, btc_markets)
    print(df_btc_market)
    path = 'Markets/btc_markets-' + str(datetime.datetime.now()) + '.csv'
    #df_btc_market.to_csv(path)


def get_markets_usd():
    usd_markets = mo.get_markets_list(client, min_vol=100000, symbol='USDT', max_markets=0)
    
    df_usd_markets = mo.balances_to_dataframe(client, usd_markets)
    print(df_usd_markets)
    path = 'Markets/usd_markets-' + str(datetime.datetime.now()) + '.csv'
    #df_usd_markets.to_csv(path)


api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)

while True:
    usd_markets = mo.get_markets_list(client, min_vol=0, symbol='USDT', max_markets=0)
    mo.log_data(client, usd_markets)
    print('Log at :', datetime.datetime.now())
    time.sleep(210)

#get_markets_usd()
#get_markets_btc()
#mo.get_market(client, 'HBARUSDT')
#mo.get_market(client, 'BEAMUSDT')