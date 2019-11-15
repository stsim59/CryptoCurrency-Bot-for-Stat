# -*- coding: utf-8 -*-

#import time
#import markets_op

def log(text):
    file = open('log.txt', 'a')
    file.write(text + '\n')
    file.close()

def trade(book, wallet, buy_pc=1.02, sell_pc=0.98, balance_index=0):
    
    #Selling order
    if wallet.balance['ETH'] > 0 and book.balance_pc[balance_index] < sell_pc:
        ETH_balance = wallet.balance['ETH']
        print(f'{wallet.name} : selling with balance ({book.balance_pc[balance_index]}) below {sell_pc}, \
              selling ETH with {ETH_balance} ETH, at {book.mid_price} ETH')
        wallet.new_order('ETHUSDT', 'sell', wallet.balance['ETH'], book.mid_price)
        log(f'{wallet.name} : selling with balance ({book.balance_pc[balance_index]}) below {sell_pc}, selling ETH with {ETH_balance} ETH, at {book.mid_price} ETH')
        log(f'{wallet.name} : balance is {wallet.get_balance()}')
    
    #Buying order
    if wallet.balance['ETH'] == 0 and book.balance_pc[balance_index] > buy_pc:
        USDT_balance = wallet.balance['USDT']
        print(f'{wallet.name} : buying with balance ({book.balance_pc[balance_index]}) above {buy_pc}, \
              buying ETH with {USDT_balance} USDT, at {book.mid_price} ETH')
        wallet.new_order('ETHUSDT', 'buy', wallet.balance['USDT'], book.mid_price)
        log(f'{wallet.name} : buying with balance ({book.balance_pc[balance_index]}) above {buy_pc}, buying ETH with {USDT_balance} USDT, at {book.mid_price} ETH')
        log(f'{wallet.name} : balance is {wallet.get_balance()}')
    

        
        
class simple_wallet:
   
    def __init__(self, name, BTC=10, USDT=0, stoploss=0.05, **tickers):
        self.name = name
        self.balance = {}
        self.balance["BTC"] = BTC
        self.balance["USDT"] = USDT
        for ticker, value in tickers.items():
            self.balance[ticker] = value
        self.stoploss = stoploss
        self.total_fees = 0
            
    def get_balance(self):
        return self.balance
    
    def new_order(self, symbol, side, quantity, price):
        #full list : (self, symbol, side, order_type, price, quantity, timestamp):
        #timestamp : number of millisecond before the server reject the request. Serious trading is about timing. It's 
        #recommanded to use a small windows (5000 or less), max is 60 000.
        self.total_fees += quantity*price*0.001
        if side == "buy":
            self.balance[symbol[:3]] += quantity/price*0.999   #currency
            self.balance[symbol[-4:]] -= quantity   #USDT
        
        
        elif side == "sell":
            self.balance[symbol[:3]] -= quantity   #currency
            self.balance[symbol[-4:]] += quantity*price*0.999   #USDT
                
        else:
            raise "Buy or sell non-defined"
    
    def total_value_btc(self):
        total = 0
        for ticker, value in self.balance.items():
            if ticker == 'BTC':
                total += value
            else:
                ticker_info = client.get_symbol_ticker(symbol=(ticker + 'BTC'))
                total += float(ticker_info['price'])*value
        return total
    
    def total_value_usd(self):
        return get_btc_usd() * self.total_value_btc()
