    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 23:48:34 2022

@author: kruthic
"""

import yfinance as yf
import pandas as pd
import numpy as np

backtest_data = {}

divide = {"m": 12, "d": 250, "y": 1}

def CAGR(DF, period = 'm'):       # Compound annual growth rate
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change() 
    df['cum_ret'] = (1+df['return']).cumprod()  
    n = len(df)/divide[period]       # effective number of years
    if df['cum_ret'].tolist()[-1] < 0:
        return -2
    CAGR = (df['cum_ret'].tolist()[-1])**(1/n) - 1
    return CAGR

def VOL(DF, period = 'm'):        # Volatility
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    vol = df['return'].std()*np.sqrt(divide['m'])
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

def DRAWDOWN(DF): 
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_ret'] = (1+df['return']).cumprod()
    df['rolling_max'] = df['cum_ret'].cummax()
    df['drawdown'] = df['rolling_max'] - df['cum_ret']      # trying the find the largest drop in asset value
    return (df['drawdown']/df['rolling_max']).max()         # max of (high-low)/high is max_drawdown

def CALMAR(DF):  # calmar ratio
    df = DF.copy()
    return CAGR(df)/DRAWDOWN(df)        # Sense of risk in our portfolio, how big of a dropdown vs the annual increase rate


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
    

### Collecting stock info ###

''' Do not recompile everytime '''
stocks = []
f = open('lc.txt', 'r')
for word in f:
    stocks.append(word[:-1] + '.NS')

ohlcv_data_store = {}
    
for ticker in stocks:
    tem = yf.download(ticker, period = 'max', interval = '1mo')
    tem.dropna(how = 'any', axis = 0, inplace = True)
    ohlcv_data_store[ticker] = tem

backtest_data['max_1mo'] = ohlcv_data_store
    
cagr = {}
volt = {}
sharpe = {}
sortino = {}
drawdown = {}
calmar = {}

stock_list_dont = []
ohlcv_data_dont = {}
for ticker in stocks:
    if ohlcv_data_store[ticker]['Adj Close'][-1] <= 5000:
        ohlcv_data_dont[ticker] = ohlcv_data_store[ticker]
        stock_list_dont.append(ticker)
        
''' Change stuff from this area '''

### REBALANCING BASED ON RSI ###

ohlcv_data = ohlcv_data_dont
stock_list = stock_list_dont

return_df = pd.DataFrame()
rsi_df = pd.DataFrame()

# collecting returns per month
for ticker in stock_list:
    return_df[ticker] = ohlcv_data[ticker]['Adj Close'].pct_change()    # monthly close rates
    return_df[ticker][0] = 0
    
# collecting rsi month-wise
for ticker in stock_list:
    rsi_df[ticker] = RSI(ohlcv_data[ticker])
    
rsi_df.fillna(50, inplace = True) # filling na to 50 -> neutral rsi value

return_df.fillna(0, inplace = True)
    
def rsi_strat1(DF, count, rem):
    df = return_df.copy()
    rs = rsi_df.copy()
    portfolio = []
    monthly_ret = [0]
    monthly_port = []
    money = 100
   # print("money start ", money)
    for i in range(1, len(df)): # no of months
        if len(portfolio) > 0:
            selected_stocks = df[portfolio].iloc[i,:]
            monthly_ret.append(selected_stocks.mean())
            
            money *= monthly_ret[-1]+1
            
            find_stocks = rs[portfolio].iloc[i, :]
            remove_stocks = find_stocks.sort_values(ascending = False)[:rem].index.values.tolist()
            portfolio = [x for x in portfolio if x not in remove_stocks]
        add_co = count - len(portfolio)
        distinct = [x for x in stock_list if x not in portfolio]  # change if you want to allow multiple stocks
        # repeat = stock_list
        new_picks = rs[distinct].iloc[i,:].sort_values(ascending = True)[:add_co].index.values.tolist()
        portfolio += new_picks
        monthly_port.append(portfolio)
        
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret), columns = ['Adj Close'])
    return monthly_ret_df, money


def test_different_rsize(limit = 10):
    money_max = -2
    count_max = -2
    
    for i in range(2, limit, 2):
        returned = pd.DataFrame()
        returned, money = rsi_strat1(return_df, i, i//2)
        
        returned = returned[1:]
        
        if money > money_max:
            money_max = money
            count_max = i
        
    return money_max, count_max

dif_rsize_money, dif_rsize_count = test_different_rsize(limit = 20)

### END OF RSI REBALANCING ###