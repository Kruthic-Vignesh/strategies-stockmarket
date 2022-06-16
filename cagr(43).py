    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 23:48:34 2022

@author: kruthic
"""

import yfinance as yf
import pandas as pd
import numpy as np
# from stocktrends import Renko
# import math

def CAGR(DF):       # Compound annual growth rate
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_ret'] = (1+df['return']).cumprod()
    n = len(df)/249
    CAGR = (df['cum_ret'][-1])**(1/n) - 1
    return CAGR

def VOL(DF):        # Volatility
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    vol = df['return'].std()*np.sqrt(252)
    return vol

def SHARPE(DF):     # positive -> invest in this stock, negative -> invest in govt bonds instead, (0.07 -> govt interest rate)
    df = DF.copy()
    return (CAGR(df)-0.07)/VOL(df)
    
def SORTINO(DF):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    neg_ret = np.where(df['return'] > 0, 0, df['return'])
    neg_vol = pd.Series(neg_ret[neg_ret != 0]).std()
    return (CAGR(df)-0.07)/neg_vol

def DRAWDOWN(DF): # calmar ratio
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_ret'] = (1+df['return']).cumprod()
    df['rolling_max'] = df['cum_ret'].cummax()
    df['drawdown'] = df['rolling_max'] - df['cum_ret']      # trying the find the largest drop in asset value
    return (df['drawdown']/df['rolling_max']).max()         # max of (high-low)/high is max_drawdown

def CALMAR(DF):
    df = DF.copy()
    return CAGR(df)/DRAWDOWN(df)        # Sense of risk in our portfolio, how big of a dropdown vs the annual increase rate
    
stocks = ["AXISBANK.NS", "HDFC.NS", "INFY.NS", "ONGC.NS"]

ohlcv_data = {}
cagr = {}
volt = {}
sharpe = {}
sortino = {}
drawdown = {}
calmar = {}
    
for ticker in stocks:
    tem = yf.download(ticker, period = '1y', interval = '1d')
    tem.dropna(how = 'any', axis = 0, inplace = True)
    ohlcv_data[ticker] = tem

for ticker in stocks:
    cagr[ticker] = CAGR(ohlcv_data[ticker])
    volt[ticker] = VOL(ohlcv_data[ticker])
    sharpe[ticker] = SHARPE(ohlcv_data[ticker])
    sortino[ticker] = SORTINO(ohlcv_data[ticker])
    drawdown[ticker] = DRAWDOWN(ohlcv_data[ticker])
    calmar[ticker] = CALMAR(ohlcv_data[ticker])