#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 23:48:34 2022

@author: kruthic
"""

import yfinance as yf
import pandas as pd
import datetime as dt

stocks = ["AXISBANK.NS", "HDFC.NS", "INFY.NS", "ONGC.NS"]

start = dt.datetime.today() - dt.timedelta(3650)
end   = dt.datetime.today()
cl_price = pd.DataFrame()

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end) ["Adj Close"]

cl_price.dropna(how = 'any', axis = 0,  inplace = True)

daily_return = cl_price.pct_change()

daily_return.plot(subplots = True, layout = (2, 2), sharex = False, sharey = True, grid = True)

dic = {}
for ticker in stocks:
    arr = cl_price[ticker]
    dic[ticker] = []
    for x in arr:
        dic[ticker].append(x/arr[0])
    
new_data = pd.DataFrame(dic).plot()


returns = (1+daily_return).cumprod().plot()

# cl_price.plot(kind = 'line', subplots = True, layout = (2, 2), sharey = False, title = "close prices")