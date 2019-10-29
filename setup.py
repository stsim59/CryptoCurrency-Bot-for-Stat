#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:36 2019

@author: ubuntu
"""

import binance as bi
import markets_op as mo
import trade as tr
#from pandas import Series, DataFrame

api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)

wallet1 = tr.simple_wallet(ETH=10, BTC=0)
wallet2 = tr.simple_wallet(ETH=10, BTC=0)
tr.trade(client, wallet1)

def get_markets_to_dataframe():
    markets = mo.get_markets_list(client)
    df_market = mo.balances_to_dataframe(client, markets)
    print(df_market)
