#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:08:36 2019

@author: ubuntu
"""

import binance as bi
import markets_op as mo
from pandas import Series, DataFrame

api_key = ''
api_secret = ''
client = bi.Client(api_key, api_secret)

markets = mo.get_markets_list(client)
df_market = mo.balances_to_dataframe(client, markets)

print(df_market)
