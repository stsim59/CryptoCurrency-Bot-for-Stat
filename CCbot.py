#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:36 2019

@author: ubuntu
"""

import binance as bi
import markets_op as ma

api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)

markets = ma.get_markets_list()
df_market = ma.get_markets_bs_balance(markets)

print(df_market)