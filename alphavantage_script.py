#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:19:49 2022

@author: kruthic
"""

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

key_path = "/home/kruthic/proj_algo/alphavantage_key"

stocks = ["INFY", "HDFC", "AXISBANK", "ONGC"]
close_prices = pd.DataFrame()
for ticker in stocks:
    ts = TimeSeries(key = open(key_path, 'r').read(), output_format='pandas')
    data = ts.get_intraday(symbol = ticker, interval = '1min', outputsize = 'compact')[0]
    data.columns = ['open', 'high', 'low', 'close', 'volume']
    close_prices[ticker] = data['close']