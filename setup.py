#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:36 2019

@author: ubuntu
"""

import binance as bi
import markets_op as ma
from pandas import Series, DataFrame

api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)

markets = ma.get_markets_list(client)
df_market = ma.market_book(markets, symbol='BTC')

print(df_market)
