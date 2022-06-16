#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 23:48:34 2022

@author: kruthic
"""

import yfinance as yf
import pandas as pd
import numpy as np
from stocktrends import Renko
import math


def MACD(DF, fast = 12, slow = 26, signal = 9, st = 'Adj Close'):
    df = DF.copy()
    df['ma_fast'] = df[st].ewm(span = fast, min_periods = fast).mean()
    df['ma_slow'] = df[st].ewm(span = slow, min_periods = slow).mean()
    df['MACD']    = df['ma_fast'] - df['ma_slow']
    df['Signal']  = df['MACD'].ewm(span = signal, min_periods = signal).mean()
    df['Histogram'] = df['MACD'] - df['Signal']
    return df['MACD'], df['Signal'], df['Histogram']

def ATR(DF, period = 14):
    df = DF.copy()
    df['hl'] = df['High'] - df['Low']
    df['hc'] = abs(df['High'] - df['Close'].shift(1))
    df['lc'] = abs(df['Low'] - df['Close'].shift(1))
    df['ar'] = df[['hl', 'hc', 'lc']].max(axis = 1, skipna = False)
    df['atr'] = df['ar'].ewm(span = period, min_periods = period).mean()
    return df['atr']

def BB(DF, period = 20, offset = 2, st = 'Adj Close'):
    df = DF.copy()
    df['20avg'] = df[st].rolling(period).mean()
    df['std']   = df[st].rolling(period).std(ddof = 0)
    return df['20avg'] - offset*df['std'], df['20avg'] + offset*df['std'], df['20avg']  

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

def ADX(DF, period = 20):
    df = DF.copy()
    df['atr'] = ATR(df)
    df['upmove'] = df['High'] - df['High'].shift(1)
    df['downmove'] = df['Low'] - df['Low'].shift(1)
    df['+dm'] = np.where(df['upmove'] > df['downmove'], np.where(df['upmove'] > 0, df['upmove'], 0), 0)
    df['-dm'] = np.where(df['downmove'] > df['upmove'], np.where(df['downmove'] > 0, df['downmove'], 0), 0)
    df['+di'] = 100 * (df['+dm']/df['atr']).ewm(com = period, min_periods = period).mean()
    df['-di'] = 100 * (df['-dm']/df['atr']).ewm(com = period, min_periods = period).mean()
    df['adx'] = 100 * (abs(df['+di']-df['-di']) / abs(df['+di'] + df['-di'])).ewm(com = period, min_periods = period).mean()
    return df[['adx', '+di', '-di']]

renko_data = {}

def renko(DF, hour):
    df = DF.copy()
    df.drop("Close", axis = 1, inplace = True)
    df.reset_index(inplace = True)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df2 = Renko(df)
    df2.brick_size = 3*round(ATR(DF = hour, period = 120).iloc[-1], 0)
    renko_df = df2.get_ohlc_data()
    return renko_df
    

stocks = ["AXISBANK.NS", "HDFC.NS", "INFY.NS", "ONGC.NS"]

ohlcv_data = {}
hour_data = {}
    
for ticker in stocks:
    tem = yf.download(ticker, period = '1mo', interval = '5m')
    tem.dropna(how = 'any', axis = 0, inplace = True)
    ohlcv_data[ticker] = tem
    
    tem = yf.download(ticker, period = '1y', interval = '1h')
    tem.dropna(how = 'any', axis = 0, inplace = True)
    hour_data[ticker] = tem

for ticker in stocks:
    renko_data[ticker] = renko(ohlcv_data[ticker], hour_data[ticker])
    
for ticker in stocks:
    ohlcv_data[ticker]['MACD'], ohlcv_data[ticker]['Signal'], ohlcv_data['Histogram'] = MACD(ohlcv_data[ticker])
    ohlcv_data[ticker]['ATR'] = ATR(ohlcv_data[ticker])
    ohlcv_data[ticker]['BB_low'], ohlcv_data[ticker]['BB_high'], ohlcv_data[ticker]['BB_mid'] = BB(ohlcv_data[ticker])
    ohlcv_data[ticker]['RSI'] = RSI(ohlcv_data[ticker])
    ohlcv_data[ticker][['ADX', '+DI', '-DI']] = ADX(ohlcv_data[ticker])
