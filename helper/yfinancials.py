#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:19:49 2022

@author: kruthic
"""

import pandas as pd
from yahoofinancials import YahooFinancials
import datetime as dt

stocks = ["AXISBANK.NS", "HDFC.NS", "INFY.NS", "ONGC.NS"]
close_prices = pd.DataFrame()
end_date = dt.datetime.today().strftime('%Y-%m-%d')
beg_date = (dt.datetime.today()-dt.timedelta(200)).strftime('%Y-%m-%d')

for ticker in stocks:  
    yahoo_financials = YahooFinancials(ticker)
    json_obj = yahoo_financials.get_historical_price_data(beg_date, end_date, "daily")
    ohlv = json_obj[ticker]['prices']
    temp = pd.DataFrame(ohlv)[["formatted_date", "adjclose"]]
    temp.set_index("formatted_date", inplace = True)
    temp.dropna(inplace = True)
    close_prices[ticker] = temp["adjclose"]