#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:55 2019

@author: ubuntu

1200 requests per minute
10 orders per second
100,000 orders per 24hrs

"""

#As 21-10-2019, 
#min_vol of 50 generate 56 markets
#min_vol of 40 generate 65 markets

from pandas import Series, DataFrame
import time
from timeit import default_timer as timer
from datetime import timedelta


def get_markets_list(client, symbol='BTC', min_vol=50, max_markets=50):
    stable_coins_list = ['BUSD', 'TUSD', 'USDC', 'PAX', 'GUSD', 'USDAP', 'USDS', 'BTC']
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



def balances_to_dataframe(client, markets):
    cost = 0
    df_markets = DataFrame(columns=('Market Name', '1', '2', '3', '4', '5', 'Volume', 'Last price'))
    start = timer()
    
    for market in markets:
        book = market_book(client, symbol=market['symbol'], limit=100)
        cost += 1
        if book.oo_reach == True:
            time.sleep(0.6)
            book = market_book(client, market['symbol'], limit=500)
            cost += 5
            if book.oo_reach == True:
                time.sleep(1)
                book = market_book(client, market['symbol'], limit=1000)
                cost += 10
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
                                        round(float(market['quoteVolume']), 2), \
                                        market['lastPrice']], \
                                        index=df_markets.columns), ignore_index=True)
        '''
        print(market['symbol'], \
                                        book.balance_pc[0], \
                                        book.balance_pc[1], \
                                        book.balance_pc[2], \
                                        book.balance_pc[3], \
                                        book.balance_pc[4], \
                                        max(book.balance_pc), \
                                        round(float(market['quoteVolume']), 2), \
                                        market['lastPrice'])
        '''
        del book
        
    df_markets = df_markets.sort_values(by=['5', 'Volume'], ascending=False)
    end = timer()
    print("API cost :", cost, " in", timedelta(seconds=end-start), " sec")
    return df_markets




#MARKET BOOK _____________________
class market_book:
    
    def __init__(self, client, symbol, limit=100):
        self.buy_price, self.sell_price = [0,0,0,0,0], [0,0,0,0,0]
        self.buy_sum, self.sell_sum = [0,0,0,0,0], [0,0,0,0,0]
        self.nb_buy_orders, self.nb_sell_orders = [0,0,0,0,0], [0,0,0,0,0]
        self.balance_pc = [0,0,0,0,0]
        #To determine if the orders in book is out of reach for the number of orders(def __init__ limit var)
        self.oo_reach = False
        self.symbol = symbol
        self.book = client.get_order_book(symbol=symbol, limit=limit)
        if self.book['bids'] != [] and self.book['asks'] != []:
            self.mid_price = float(self.book['bids'][0][0]) + (float(self.book['asks'][0][0]) - float(self.book['bids'][0][0])) / 2
            self.buy_price[0] = self.mid_price*0.995
            self.buy_price[1] = self.mid_price*0.99
            self.buy_price[2] = self.mid_price*0.98
            self.buy_price[3] = self.mid_price*0.97
            self.buy_price[4] = self.mid_price*0.95
            self.sell_price[0] = self.mid_price*1.005
            self.sell_price[1] = self.mid_price*1.01
            self.sell_price[2] = self.mid_price*1.02
            self.sell_price[3] = self.mid_price*1.03
            self.sell_price[4] = self.mid_price*1.05
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
            if self.buy_sum[i] != 0 and self.sell_sum[i] != 0:
                self.balance_pc[i] = round(self.buy_sum[i]/self.sell_sum[i], 2)
            else:
                self.balance_pc[i] = 0


def get_price(client, symbol='BTCUSDT'):
    info = client.get_symbol_ticker(symbol=symbol)
    price = float(info['price'])
    return price

def get_market(client, symbol='BTCUSDT', limit=100):
    market = market_book(client, symbol, limit)
    info = client.get_ticker(symbol=symbol)
    print('------------\nMARKET : ', market.symbol)
    print('Out of reach :', market.oo_reach)
    print('Mid price :', market.mid_price)
    print('Last price :', info['lastPrice'])
    print('C-Volume :', round(float(info['volume'])))
    if symbol[-4:] == "USDT":
        print('Q-Volume :', round(float(info['volume']) * float(info['lastPrice'])), '$')
    elif symbol[-3:] == "BTC":
        print('Q-Volume :', round(float(info['volume']) * float(info['lastPrice']), 2), 'BTC')        
    print('Price buy :', market.buy_price)
    print('Price buy sum :', market.buy_sum)
    print('Nb of buy :', market.nb_buy_orders)
    print('Price sell :', market.sell_price)
    print('Price sell sum :', market.sell_sum)
    print('Nb of sell :', market.nb_sell_orders)
    print('% range :', market.balance_pc)
    print('% max :', max(market.balance_pc))