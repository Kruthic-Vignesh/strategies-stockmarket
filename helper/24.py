#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 23:48:34 2022

@author: kruthic
"""

import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

stocks = ["AXISBANK.NS", "HDFC.NS", "INFY.NS", "ONGC.NS"]

start = dt.datetime.today() - dt.timedelta(3650)
end   = dt.datetime.today()
cl_price = pd.DataFrame()

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end) ["Adj Close"]

cl_price.dropna(how = 'any', axis = 0,  inplace = True)

daily_return = cl_price.pct_change()

flg, ax = plt.subplots()
ax.set(title = 'Mean daily return of stocks', xlabel = 'stocks', ylabel = 'mean daily return')
plt.bar(x = stocks, height = daily_return.mean(axis = 0))

# ax.set(title = 'tits')
# plt.bar(x = stocks, height = daily_return.ewm(com = 25, min_periods = 25).mean())