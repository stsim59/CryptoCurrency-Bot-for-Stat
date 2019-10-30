#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:36 2019

@author: ubuntu
"""

import binance as bi
import markets_op as mo
import trade as tr
import time, datetime
#from pandas import Series, DataFrame

api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)
log_path = 'logETH_' + str(datetime.datetime.now()) + '.txt'

#Trading tests
wallet1 = tr.simple_wallet('Wallet 1.02-0.98', ETH=10, BTC=0)
wallet2 = tr.simple_wallet('Wallet 1.04-0.96', ETH=10, BTC=0)
wallet3 = tr.simple_wallet('Wallet 1.10-1', ETH=10, BTC=0)

def get_markets_to_dataframe():
    markets = mo.get_markets_list(client)
    df_market = mo.balances_to_dataframe(client, markets)
    print(df_market)

def log_balance(text):
    file = open(log_path, 'a')
    file.write(text + '\n')
    file.close
    
while True:
    book = mo.market_book(client, symbol='ETHUSDT', limit=1000)
    eth_price = mo.get_price(client, 'ETHUSDT')
    print(f'Looking {book.symbol}, last price is : {eth_price} and balances are {book.balance_pc}')
    log_balance(f'{datetime.datetime.now()},{book.symbol},{eth_price},{book.balance_pc[0]},{book.balance_pc[1]},{book.balance_pc[2]},{book.balance_pc[3]},{book.balance_pc[4]}')
    tr.trade(client, book, wallet1, buy_pc=1.02, sell_pc=0.98)
    tr.trade(client, book, wallet2, buy_pc=1.04, sell_pc=0.96)
    tr.trade(client, book, wallet3, buy_pc=1.1, sell_pc=1)
    time.sleep(30)


