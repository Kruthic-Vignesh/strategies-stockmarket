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

cl_price.fillna(method = 'bfill', axis = 1,  inplace = True)

cl_price.mean()     # mean of each column
cl_price.std()      # standard deviation of each column
cl_price.median()   # median of each column
cl_price.describe() # count, mean, std, ... of each column as a table
cl_price.head(7)    # cl_price, first 7 rows
cl_price.tail(8)    # cl_price, last 8 rows

# daily_return = cl_price.pct_change()
shift_one = cl_price.shift(1)           # shifts all row by 1
daily_return = cl_price/shift_one - 1

daily_return.mean()
daily_return.std()

d1 = daily_return.rolling(window = 25).mean()
d2 = daily_return.rolling(window = 25).std()
d3 = daily_return.rolling(window = 25).max()
d4 = daily_return.rolling(window = 25).min()
d5 = daily_return.rolling(window = 25).sum()
d6 = daily_return.rolling(window = 25, min_periods = 16).median()

exp1 = daily_return.ewm(com = 25, min_periods = 25).mean()  

# infy_price = pd.DataFrame()
# infy_price["INFY.NS"] = yf.download("INFY.NS", start, end-dt.timedelta(45)) ["Adj Close"]
# dal_ret = infy_price/infy_price.shift(1) - 1
# dal_ret.mean()