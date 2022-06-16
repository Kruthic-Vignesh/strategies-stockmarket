#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 23:48:34 2022

@author: kruthic
"""

import yfinance as yf
import numpy as np
import pandas as pd

def CAGR(DF):       # Compound annual growth rate
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_ret'] = (1+df['return']).cumprod()
    n = len(df)/249
    CAGR = (df['cum_ret'][-1])**(1/n) - 1
    return CAGR

def MACD(DF, fast = 12, slow = 26, signal = 9, st = 'Adj Close'):
    df = DF.copy()
    df['ma_fast'] = df[st].ewm(span = fast, min_periods = fast).mean()
    df['ma_slow'] = df[st].ewm(span = slow, min_periods = slow).mean()
    df['MACD']    = df['ma_fast'] - df['ma_slow']
    df['Signal']  = df['MACD'].ewm(span = signal, min_periods = signal).mean()
    df['Histogram'] = df['MACD'] - df['Signal']
    return df['MACD'], df['Signal'], df['Histogram']

def RSI(DF, length = 14):
    df = DF.copy()
    df['change'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['change'] > 0, df['change'], 0)
    df['loss'] = np.where(df['change'] < 0, -df['change'], 0)
    df['avggain'] = df['gain'].ewm(alpha = 1/length, min_periods = length).mean()
    df['avgloss'] = df['loss'].ewm(alpha = 1/length, min_periods = length).mean()
    df['rs'] = df['avggain']/df['avgloss']
    df['rsi'] = 100 - 100/(1+df['rs'])
    return df['rsi']
 
def BB(DF, period = 20, offset = 2, st = 'Adj Close'):
    df = DF.copy()
    df['20avg'] = df[st].rolling(period).mean()
    df['std']   = df[st].rolling(period).std(ddof = 0)
    return df['20avg'] - offset*df['std'], df['20avg'] + offset*df['std'], df['20avg']   

stocks = ["AXISBANK.NS", "HDFC.NS", "INFY.NS", "ONGC.NS"]

ohlcv_data = {} # collecting daily data, past 1 year
period = '1y'
interval = '1d'

for ticker in stocks:
    tem = yf.download(ticker, period = period, interval = interval)
    tem.dropna(how = 'any', axis = 0, inplace = True)
    ohlcv_data[ticker] = tem
    
for ticker in stocks:
    ohlcv_data[ticker]['MACD'], ohlcv_data[ticker]['Signal'], ohlcv_data[ticker]['Histogram'] = MACD(ohlcv_data[ticker])
    ohlcv_data[ticker]['BB_low'], ohlcv_data[ticker]['BB_high'], ohlcv_data[ticker]['BB_mid'] = BB(ohlcv_data[ticker])
    ohlcv_data[ticker]['RSI'] = RSI(ohlcv_data[ticker])
    
# handling data
for ticker in stocks:
    ohlcv_data[ticker].dropna(how = 'any', axis = 0, inplace = True)
    
class live:
    def __init__(self, type, price):
        self.type = type
        self.price = price
    
    def set_val(self, type, price):
        self.type = type
        self.price = price

bought_at = []
sold_at = []
cur_cash = []
def strat2(ticker, max_count = 1):
    profit = 0
    run = live("none", 0)
    n = max_count
    cash = 700
    count = 0
    margin = 700
    for i in range(0, len(ohlcv_data[ticker])):
        rsi = ohlcv_data[ticker].iloc[i]['RSI']
        price = ohlcv_data[ticker].iloc[i]['Adj Close']
        low = ohlcv_data[ticker].iloc[i]['BB_low']
        high = ohlcv_data[ticker].iloc[i]['BB_high']
        min_quota = low + 0.1*(high-low)
        max_quota = high - 0.1*(high-low)
        if price <= min_quota and rsi < 40:
            count += 1
            if run.type == 'buy':
                continue
            elif run.type == 'sell':    # short
                ch = price - run.price
                profit -= ch
                cash -= price
                margin += run.price - ch
                run.type = 'none'
                bought_at.append(price)
                cur_cash.append(margin)
            elif run.type == 'none' and margin > price:
                run.set_val('buy', price)
                cash -= price
                margin -= price
                bought_at.append(price)
                
        elif price >= max_quota and rsi > 60:
            count += 1
            if run.type == 'sell':
                continue
            elif run.type == 'buy':     # long
                ch = price - run.price
                profit += ch
                cash += price
                margin += run.price + ch
                run.type = 'none'
                sold_at.append(price)
                cur_cash.append(margin)
            elif run.type == 'none' and margin > price:
                run.set_val('sell', price)
                margin -= price
                cash += price
                sold_at.append(price)
    
    print("current cash ", margin)
    print("total profit ", profit)
    print("count ", count)


strat2('AXISBANK.NS')
    
backtest = {}
ohlcv_data = {}
for ticker in stocks:
    tem = yf.download(ticker, period = '2y', interval = '1h')
    tem.dropna(how = 'any', axis = 0, inplace = True)
    ohlcv_data[ticker] = tem
    
for ticker in stocks:
    ohlcv_data[ticker]['MACD'], ohlcv_data[ticker]['Signal'], ohlcv_data[ticker]['Histogram'] = MACD(ohlcv_data[ticker])
    ohlcv_data[ticker]['BB_low'], ohlcv_data[ticker]['BB_high'], ohlcv_data[ticker]['BB_mid'] = BB(ohlcv_data[ticker])
    ohlcv_data[ticker]['RSI'] = RSI(ohlcv_data[ticker])
    
# handling data
for ticker in stocks:
    ohlcv_data[ticker].dropna(how = 'any', axis = 0, inplace = True)  

    
