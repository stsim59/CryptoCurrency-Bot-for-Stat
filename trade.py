# -*- coding: utf-8 -*-

import binance as bi
import pandas as pd
import time
import markets_op as mo
from collections import defaultdict


def log(file, text):
    file = open(file, 'a')
    file.write(text + '\n')
    file.close()

        
        
class simple_wallet:
    def __init__(self, name, USDT=1000, **tickers):
        self.name = name
        self.balance = defaultdict(float)
        self.balance["USDT"] = USDT
        for ticker, value in tickers.items():
            self.balance[ticker] = value
        self.total_fees = 0
     

    def sell_market(self, symbol, quantity):
        #full list : (self, symbol, side, order_type, price, quantity, timestamp):
        #timestamp : number of millisecond before the server reject the request. Serious trading is about timing. It's 
        #recommanded to use a small windows (5000 or less), max is 60 000.
        book = client.get_order_book(symbol=symbol, limit=100)
        amount_left = quantity 
        average_p = 0
        i = 0
                
        while amount_left > 0:
            #print('Selling order :', i, book['asks'][i][1], book['asks'][i][0])
            qte = float(book['bids'][i][1])
            price = float(book['bids'][i][0])
            if amount_left >= qte:     #get the full offer
                self.balance[symbol[:-4]] -= qte                  #currency
                self.balance[symbol[-4:]] += qte * price * 0.999  #USDT
                self.total_fees += qte * price * 0.001            #fees
                i += 1            
                average_p += qte * price
            else:
                self.balance[symbol[:-4]] -= amount_left           #currency
                self.balance[symbol[-4:]] += amount_left * price * 0.999   #USDT
                self.total_fees +=  amount_left * price * 0.001    #fees
                average_p += amount_left * price
            amount_left -= qte
            i += 1            
        average_p /= quantity
        print('Selling {} {} at an average price of {} ({} order(s) get)'.format(quantity, symbol, average_p, i))


    def buy_market(self, symbol, q_usd):
        #quantity in USD
        book = client.get_order_book(symbol=symbol, limit=100)
        usd_left = q_usd
        amount_bought = 0
        average_p = 0
        i = 0
                        
        while usd_left > 0:
            #print('Buying order :', i, book['asks'][i][1], book['asks'][i][0])
            qte = float(book['asks'][i][1])
            price = float(book['asks'][i][0])
            if usd_left >= qte * price:     #get the full offer
                self.balance[symbol[:-4]] += qte                     #currency
                self.balance[symbol[-4:]] -= qte * price * 1.001   #USDT
                usd_left -= qte * price * 1.001
                self.total_fees += qte * price * 0.001    #fees
                average_p += qte * price
                amount_bought += qte
            else:
                unit_left = usd_left / (price  * 1.001)
                self.balance[symbol[:-4]] += unit_left                      #currency
                self.balance[symbol[-4:]] -= unit_left * price   #USDT
                self.total_fees +=  unit_left * price * 0.001    #fees
                average_p += unit_left * price
                amount_bought += unit_left
                usd_left = 0
            i += 1            
        average_p /= amount_bought
        print('Buying {} with {} USD {} at an average price of {} ({} order(s) get)'.format(amount_bought, q_usd, symbol, average_p, i))
    

    def sell_all(self):
        for ticker, qte in self.balance.items():
            if ticker == 'USDT' or qte == 0:
                continue
            self.sell_market(ticker + 'USDT', qte)
    
    
    def total_value_usd(self):
        total = 0
        for ticker, qte in self.balance.items():
            if ticker == 'USDT':
                continue
            ticker_info = client.get_symbol_ticker(symbol=(ticker + 'USDT'))
            total += float(ticker_info['price']) * qte
        return total
   
    
    
    
#Program ...............................
api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)

wallet1 = simple_wallet('wallet1')
wallet2 = simple_wallet('wallet2')
wallet3 = simple_wallet('wallet3')
wallet4 = simple_wallet('wallet4')
wallet5 = simple_wallet('wallet5')

while True:
    usd_markets = mo.get_markets_list(client, min_vol=100000, symbol='USDT', max_markets=0)
    df = mo.balances_to_dataframe(client, usd_markets)
#    df.to_csv('data')
#    df = pd.read_csv('data')

    #Trading
    best_market = df.loc[df['1'].idxmax(), 'Market Name']
    print('For 1% bal,', best_market, 'is the best option, with a value of', df.loc[df['1'].idxmax(), '1'])
    if wallet1.balance[best_market[:-4]] < 1:
        wallet1.sell_all()
        wallet1.buy_market(df.loc[df['1'].idxmax(), 'Market Name'], wallet1.balance['USDT'])        
        print('New balance for', wallet1.name, 'is', wallet1.balance, '\n')
        log(wallet1.name, str(wallet1.balance) + ', total value : ' + str(wallet1.total_value_usd()))
    
    best_market = df.loc[df['2'].idxmax(), 'Market Name']
    print('For 2% bal,', best_market, 'is the best option, with a value of', df.loc[df['2'].idxmax(), '2'])
    if wallet2.balance[best_market[:-4]] < 1:
        wallet2.sell_all()
        wallet2.buy_market(df.loc[df['2'].idxmax(), 'Market Name'], wallet2.balance['USDT'])        
        print('New balance for', wallet2.name, 'is', wallet2.balance, '\n')
        log(wallet2.name, str(wallet2.balance) + ', total value : ' + str(wallet2.total_value_usd()))
        
    best_market = df.loc[df['3'].idxmax(), 'Market Name']
    print('For 3% bal,', best_market, 'is the best option, with a value of', df.loc[df['3'].idxmax(), '3'])
    if wallet3.balance[best_market[:-4]] < 1:
        wallet3.sell_all()
        wallet3.buy_market(df.loc[df['3'].idxmax(), 'Market Name'], wallet3.balance['USDT'])        
        print('New balance for', wallet3.name, 'is', wallet3.balance, '\n')
        log(wallet3.name, str(wallet3.balance) + ', total value : ' + str(wallet3.total_value_usd()))
        
    best_market = df.loc[df['4'].idxmax(), 'Market Name']
    print('For 4% bal,', best_market, 'is the best option, with a value of', df.loc[df['4'].idxmax(), '4'])
    if wallet4.balance[best_market[:-4]] < 1:
        wallet4.sell_all()
        wallet4.buy_market(df.loc[df['4'].idxmax(), 'Market Name'], wallet4.balance['USDT'])        
        print('New balance for', wallet4.name, 'is', wallet4.balance, '\n')
        log(wallet4.name, str(wallet4.balance) + ', total value : ' + str(wallet4.total_value_usd()))
        
    best_market = df.loc[df['5'].idxmax(), 'Market Name']
    print('For 5% bal,', best_market, 'is the best option, with a value of', df.loc[df['5'].idxmax(), '5'])
    if wallet5.balance[best_market[:-4]] < 1:
        wallet5.sell_all()
        wallet5.buy_market(df.loc[df['5'].idxmax(), 'Market Name'], wallet5.balance['USDT'])        
        print('New balance for', wallet5.name, 'is', wallet5.balance, '\n')
        log(wallet5.name, str(wallet5.balance) + ', total value : ' + str(wallet5.total_value_usd()))
    
    print('------------------------------------------------\n')
    time.sleep(240)


#wallet = simple_wallet('test')
#wallet.buy_market('ETHUSDT', 1000)
#wallet.buy_market('BEAMUSDT', 1000)
#wallet.sell_all()
#
##wallet.sell_market('ETHUSDT', wallet.balance['ETH'])
##wallet.buy_market('ETHUSDT', wallet.balance['USDT'])
##wallet.sell_market('ETHUSDT', wallet.balance['ETH'])
##wallet.buy_market('ETHUSDT', wallet.balance['USDT'])
##wallet.sell_market('ETHUSDT', wallet.balance['ETH'])
#print(wallet.get_balance())
