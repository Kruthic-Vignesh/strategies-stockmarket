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
ohlcv_data = {}

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end) ["Adj Close"]
    
for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker, start, end)
    
# filling nan values
cl_price.fillna(method = 'bfill', axis = 1,  inplace = True)