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


def log_balance(text):
    file = open(log_path, 'a')
    file.write(text + '\n')
    file.close


def trading():    
    #Trading tests
    log_balance('time,symbol,price,volume,bal1,bal2,bal3,bal4,bal5')

    wallet1 = tr.simple_wallet('Wallet 1.02-0.98', ETH=10, BTC=0)
    wallet2 = tr.simple_wallet('Wallet 1.04-0.96', ETH=10, BTC=0)
    wallet3 = tr.simple_wallet('Wallet 1.06-0.94', ETH=10, BTC=0)
    wallet4 = tr.simple_wallet('Wallet 1.08-0.92', ETH=10, BTC=0)
    
    wallet5 = tr.simple_wallet('Wallet 1.02-0.98-b', ETH=10, BTC=0)
    wallet6 = tr.simple_wallet('Wallet 1.04-0.96-b', ETH=10, BTC=0)
    wallet7 = tr.simple_wallet('Wallet 1.06-0.94-b', ETH=10, BTC=0)
    wallet8 = tr.simple_wallet('Wallet 1.08-0.92-b', ETH=10, BTC=0)
    
    wallet9 = tr.simple_wallet('Wallet 1.02-0.98-c', ETH=10, BTC=0)
    wallet10 = tr.simple_wallet('Wallet 1.04-0.96-c', ETH=10, BTC=0)
    wallet11 = tr.simple_wallet('Wallet 1.06-0.94-c', ETH=10, BTC=0)
    wallet12 = tr.simple_wallet('Wallet 1.08-0.92-c', ETH=10, BTC=0)
    
    wallet21 = tr.simple_wallet('Wallet 1.02-0.98', ETH=10, BTC=0)
    wallet22 = tr.simple_wallet('Wallet 1.04-0.96', ETH=10, BTC=0)
    wallet23 = tr.simple_wallet('Wallet 1.06-0.94', ETH=10, BTC=0)
    wallet24 = tr.simple_wallet('Wallet 1.08-0.92', ETH=10, BTC=0)

    while True:
        book = mo.market_book(client, symbol='ETHUSDT', limit=1000)
        info = client.get_ticker(symbol='ETHUSDT')
        eth_price = info['lastPrice']
        eth_volume = info['quoteVolume']
        print(f'Looking {book.symbol}, last price is : {eth_price}, vol:{eth_volume} and balances are {book.balance_pc}')
        
        log_balance(f'{datetime.datetime.now()},{book.symbol},{eth_price},{book.balance_pc[0]},{book.balance_pc[1]},{book.balance_pc[2]},{book.balance_pc[3]},{book.balance_pc[4]}')
        
        tr.trade(book, wallet1, buy_pc=1.02, sell_pc=0.98)
        tr.trade(book, wallet2, buy_pc=1.04, sell_pc=0.96)
        tr.trade(book, wallet3, buy_pc=1.06, sell_pc=0.94)
        tr.trade(book, wallet4, buy_pc=1.08, sell_pc=0.92)

        tr.trade(book, wallet5, buy_pc=1.02, sell_pc=0.98, balance_index=1)
        tr.trade(book, wallet6, buy_pc=1.04, sell_pc=0.96, balance_index=1)
        tr.trade(book, wallet7, buy_pc=1.06, sell_pc=0.94, balance_index=1)
        tr.trade(book, wallet8, buy_pc=1.08, sell_pc=0.92, balance_index=1)

        tr.trade(book, wallet9, buy_pc=1.02, sell_pc=0.98, balance_index=2)
        tr.trade(book, wallet10, buy_pc=1.04, sell_pc=0.96, balance_index=2)
        tr.trade(book, wallet11, buy_pc=1.06, sell_pc=0.94, balance_index=2)
        tr.trade(book, wallet12, buy_pc=1.08, sell_pc=0.92, balance_index=2)

        tr.trade(book, wallet21, buy_pc=1.02, sell_pc=0.98)
        tr.trade(book, wallet22, buy_pc=1.04, sell_pc=1)
        tr.trade(book, wallet23, buy_pc=1.06, sell_pc=1.02)
        tr.trade(book, wallet24, buy_pc=1.08, sell_pc=1.04)

        time.sleep(30)

api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)
log_path = 'logETH_' + str(datetime.datetime.now()) + '.txt'

trading()
