#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:55 2019

@author: ubuntu
"""

#As 21-10-2019, 
#min_vol of 50 generate 56 markets
#min_vol of 40 generate 65 markets

from pandas import Series, DataFrame
import time
from timeit import default_timer as timer
from datetime import timedelta


def get_markets_list(symbol='BTC', min_vol=50, max_markets=50):
    stable_coins_list = ['BUSD', 'TUSD', 'USDT', 'USDC', 'PAX', 'GUSD', 'USDAP', 'USDS']
    f_markets = []
    
    tickers = client.get_ticker()
    for ticker in tickers:
        if float(ticker['quoteVolume']) > min_vol and not(any(coin in ticker['symbol'] for coin in stable_coins_list)) and symbol in ticker['symbol']:
            f_markets.append(ticker)
    
    #if market['MarketName'][:3] == "BTC" and market['BaseVolume'] > min_vol:

    f_markets = sorted(f_markets, key=lambda i: float(i['quoteVolume']), reverse=True)
    if len(f_markets) > max_markets:
        return f_markets[:max_markets]
    else:
        return f_markets
    
#Get trading info in a dataframe


def get_markets_bs_balance(markets, limit=100, reach=0.025):
    cost = 0
    df_markets = DataFrame(columns=('Market Name', 'bs_balance %', 'Volume', 'Last price', 'Mid price', 'Nb buy', \
                                    'Buy sum', 'Nb sell', 'Sell sum', 'Limit reach'))
    start = timer()
    
    for market in markets:
        book = market_book(symbol=market['symbol'], limit=limit, reach=reach)
        book.get_bs_balance()
        cost += 1
        
        if book.nb_buy_orders == 0 or book.nb_sell_orders == 0:
            continue
        if (book.buy_out + book.sell_out) > 0 and limit==100:
            book = market_book(market['symbol'], limit=500, reach=reach)
            book.get_bs_balance()
            cost += 5
            time.sleep(0.7)
            if (book.buy_out + book.sell_out) > 0:
                book = market_book(market['symbol'], limit=1000, reach=reach)
                book.get_bs_balance()
                cost += 10
                time.sleep(1)
        
        try:
            df_markets = df_markets.append(Series([market['symbol'], round(book.bs_balance_pour, 2), round(float(market['quoteVolume']), 2), \
                                        market['lastPrice'], book.mid_price, book.nb_buy_orders, book.buy_sum, book.nb_sell_orders, \
                                        book.sell_sum, (book.buy_out + book.sell_out)], index=df_markets.columns), ignore_index=True)
        except:
            print('Error with :', market['symbol'])
           
    df_markets = df_markets.sort_values(by=['bs_balance %', 'Volume'], ascending=False)
    end = timer()
    print("API cost :", cost, " in", timedelta(seconds=end-start), " sec")
    return df_markets

class market_book:
    buy_sum = 0
    sell_sum = 0
    nb_buy_orders = 0
    nb_sell_orders = 0
    #To determine if the orders in book is out of reach for the bs_balance %
    buy_out = True
    sell_out = True
    
    def __init__(self, symbol, limit=100, reach=0.025):
        self.book = client.get_order_book(symbol=symbol, limit=limit)
        if self.book['bids'] != [] and self.book['asks'] != []:
            self.mid_price = float(self.book['bids'][0][0]) + (float(self.book['asks'][0][0]) - float(self.book['bids'][0][0])) / 2
        else:
            self.mid_price = 0
        self.buy_limit = self.mid_price*(1-reach)
        self.sell_limit = self.mid_price*(1+reach)
        
        #self.btc_price = client.get_symbol_ticker(symbol='BTCUSDT')
        #self.btc_price = float(self.btc_price['price'])
    
    def get_bs_balance(self):
        val = 0
       
        for order in self.book['bids']:
            val = float(order[0]) * float(order[1])
            if float(order[0]) > self.buy_limit:
                self.buy_sum += val
                self.nb_buy_orders += 1
            else:
                self.buy_out = False
                break

        for order in self.book['asks']:
            val = float(order[0]) * float(order[1])
            if float(order[0]) < self.sell_limit:
                self.sell_sum += val
                self.nb_sell_orders += 1
            else:
                self.sell_out = False
                break

        self.bs_balance_dif = self.buy_sum - self.sell_sum
        if self.bs_balance_dif != 0:
            self.bs_balance_pour = (self.buy_sum - self.sell_sum)/(self.buy_sum + self.sell_sum)
        else:
            self.bs_balance_pour = 0
        return self.bs_balance_pour