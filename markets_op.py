#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:55 2019

@author: ubuntu
"""

#As 21-10-2019, 
#min_vol of 50 generate 56 markets
#min_vol of 40 generate 65 markets

import pandas as pd
from pandas import Series, DataFrame
import time
from timeit import default_timer as timer
from datetime import timedelta
import statistics


def get_markets_list(client, symbol='BTC', min_vol=50, max_markets=50):
    stable_coins_list = ['BUSD', 'TUSD', 'USDC', 'PAX', 'GUSD', 'USDAP', 'USDS']
    f_markets = []
    
    tickers = client.get_ticker()
    for ticker in tickers:
        if float(ticker['quoteVolume']) > min_vol and not(any(coin in ticker['symbol'] for coin in stable_coins_list)) and ticker['symbol'][-len(symbol):] == symbol:
            f_markets.append(ticker)
    
    f_markets = sorted(f_markets, key=lambda i: float(i['quoteVolume']), reverse=True)
    if len(f_markets) > max_markets and max_markets != 0:
        return f_markets[:max_markets]
    else:
        return f_markets



def balances_to_dataframe(markets):
    cost = 0
    df_markets = DataFrame(columns=('Market Name', '1%', '2%', '3%', '4%', '5%', 'Balance % mean', 'Volume', 'Last price', \
                                    'Mid price', 'Nb buy 5%', 'Nb sell 5%', 'Limit reach'))
    start = timer()
    
    for market in markets:
        #if market['symbol'] == 'USDTBTC':
        #    continue
        
        book = market_book(symbol=market['symbol'], limit=100)
        cost += 1
        if book.oo_reach == True:
            book = market_book(market['symbol'], limit=500)
            cost += 5
            time.sleep(0.5)
            if book.oo_reach == True:
                book = market_book(market['symbol'], limit=1000)
                cost += 10
                time.sleep(1)
                if book.oo_reach == True:
                    print('Limit out of reach with', market['symbol'])
        
        #Adding data to dataframe
        #print(book.symbol, book.balance_pc, round(statistics.mean(book.balance_pc), 2))
        df_markets = df_markets.append(Series([market['symbol'], \
                                        book.balance_pc[0], \
                                        book.balance_pc[1], \
                                        book.balance_pc[2], \
                                        book.balance_pc[3], \
                                        book.balance_pc[4], \
                                        round(statistics.mean(book.balance_pc), 2), \
                                        round(float(market['quoteVolume']), 2), \
                                        market['lastPrice'], \
                                        book.mid_price, \
                                        round(book.nb_buy_orders[4], 2), \
                                        round(book.nb_sell_orders[4], 2), \
                                        book.oo_reach], index=df_markets.columns), ignore_index=True)
           
    df_markets = df_markets.sort_values(by=['Balance % mean', 'Volume'], ascending=False)
    end = timer()
    print("API cost :", cost, " in", timedelta(seconds=end-start), " sec")
    return df_markets



#MARKET BOOK _____________________
class market_book:
    buy_price, sell_price = [0,0,0,0,0], [0,0,0,0,0]
    buy_sum, sell_sum = [0,0,0,0,0], [0,0,0,0,0]
    nb_buy_orders, nb_sell_orders = [0,0,0,0,0], [0,0,0,0,0]
    balance_pc = [0,0,0,0,0]

    #To determine if the orders in book is out of reach for the number of orders(def __init__ limit var)
    oo_reach = False
 
                       
    def __init__(self, client, symbol, limit=100):
        self.symbol = symbol
        self.book = client.get_order_book(symbol=symbol, limit=limit)
        if self.book['bids'] != [] and self.book['asks'] != []:
            self.mid_price = float(self.book['bids'][0][0]) + (float(self.book['asks'][0][0]) - float(self.book['bids'][0][0])) / 2
            for i in range(1, 6):
                self.buy_price[i-1] = self.mid_price*(100-i)/100
                self.sell_price[i-1] = self.mid_price*(100+i)/100
            self.get_balances()
        else:
            self.mid_price = 0
    
    
    def get_balances(self):
        if float(self.book['bids'][len(self.book['bids'])-1][0]) > self.buy_price[4] or \
            float(self.book['asks'][len(self.book['asks'])-1][0]) < self.sell_price[4]:                
            self.oo_reach = True
            #return "limit out of reach"

        for order in self.book['bids']:
            val = float(order[0]) * float(order[1])      #order[0] == price, order[1] == qte
            for i in range(5):
                if float(order[0]) > self.buy_price[i]:
                    self.buy_sum[i] += val
                    self.nb_buy_orders[i] += 1 #float(order[1])

        for order in self.book['asks']:
            val = float(order[0]) * float(order[1])      #order[0] == price, order[1] == qte
            for i in range(5):
                if float(order[0]) < self.sell_price[i]:
                    self.sell_sum[i] += val
                    self.nb_sell_orders[i] += 1 #float(order[1])
        
        for i in range(5):
            self.balance_pc[i] = round(self.buy_sum[i]/self.sell_sum[i], 2)
