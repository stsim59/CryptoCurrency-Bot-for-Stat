#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:36 2019

@author: ubuntu
"""

import binance as bi
import markets_op as mo
import trade as tr
import time
#from pandas import Series, DataFrame

api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)
wallet1 = tr.simple_wallet(ETH=10, BTC=0)
wallet2 = tr.simple_wallet(ETH=10, BTC=0)
wallet3 = tr.simple_wallet(ETH=10, BTC=0)


while True:
    book = mo.market_book(client, symbol='ETHUSDT', limit=1000)
    print('Looking', book.symbol, ', balance are', book.balance_pc)
    
    tr.trade(client, book, wallet1)
    tr.trade(client, book, wallet2, buy_pc=0.95, sell_pc=1.05)
    tr.trade(client, book, wallet3, buy_pc=0.92, sell_pc=1.08)
    time.sleep(30)


def get_markets_to_dataframe():
    markets = mo.get_markets_list(client)
    df_market = mo.balances_to_dataframe(client, markets)
    print(df_market)
