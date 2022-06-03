#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 20:41:09 2022

@author: kruthic
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

income_st_dict = {}
balance_st_dict = {}
cashflow_st_dict = {}

stocks = ["AXISBANK.NS", "HDFC.NS", "INFY.NS", "ONGC.NS"]

for ticker in stocks:
    url_income = "https://finance.yahoo.com/quote/{}/financials?p={}".format(ticker, ticker)
    headers = {"User-Agent": "Chrome/101.0.4951.54"}
    page = requests.get(url_income, headers = headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find_all("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    income_stmt = {}
    table_title = {}
    for tabl in table:
        heading = tabl.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split('|')[0]] = top_row.get_text(separator='|').split('|')[1:]
        
        
        rows = tabl.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            income_stmt[row.get_text(separator="|").split('|')[0]] = row.get_text(separator='|').split('|')[1:]
            
    income_data = pd.DataFrame(income_stmt)
    indices = table_title["Breakdown"]
    income_data.index = indices
    income_data = income_data.T
    
    income_st_dict[ticker] = income_data
    
for ticker in stocks:
    balance_url = "https://finance.yahoo.com/quote/{}/balance-sheet?p={}".format(ticker, ticker)
    headers = {"User-Agent": "Chrome/101.0.4951.54"}
    page = requests.get(balance_url, headers = headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find_all("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    balance_stmt = {}
    table_tit = {}
    for tabl in table:
        heading = tabl.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_tit[top_row.get_text(separator="|").split('|')[0]] = top_row.get_text(separator='|').split('|')[1:]
        
        
        rows = tabl.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            balance_stmt[row.get_text(separator="|").split('|')[0]] = row.get_text(separator='|').split('|')[1:]
            
    bal_data = pd.DataFrame(balance_stmt)
    indices = table_tit["Breakdown"]
    bal_data.index = indices
    bal_data = bal_data.T
    
    balance_st_dict[ticker] = bal_data
    
for ticker in stocks:
    cash_url = "https://finance.yahoo.com/quote/{}/cash-flow?p={}".format(ticker, ticker)
    headers = {"User-Agent": "Chrome/101.0.4951.54"}
    page = requests.get(cash_url, headers = headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find_all("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    cash_stmt = {}
    table_titl = {}
    for tabl in table:
        heading = tabl.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_titl[top_row.get_text(separator="|").split('|')[0]] = top_row.get_text(separator='|').split('|')[1:]
        
        
        rows = tabl.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            cash_stmt[row.get_text(separator="|").split('|')[0]] = row.get_text(separator='|').split('|')[1:]
            
    cash_data = pd.DataFrame(cash_stmt)
    indices = table_titl["Breakdown"]
    cash_data.index = indices
    cash_data = cash_data.T
    
    cashflow_st_dict[ticker] = cash_data

for ticker in stocks:
    for col in income_st_dict[ticker].columns:
        income_st_dict[ticker][col] = income_st_dict[ticker][col].str.replace(',|-', '')
        income_st_dict[ticker][col] = pd.to_numeric(income_st_dict[ticker][col], errors = "coerce")
        
for ticker in stocks:
    for col in balance_st_dict[ticker].columns:
        balance_st_dict[ticker][col] = balance_st_dict[ticker][col].str.replace(',|-', '')
        balance_st_dict[ticker][col] = pd.to_numeric(balance_st_dict[ticker][col], errors = "coerce")
        
for ticker in stocks:
    for col in cashflow_st_dict[ticker].columns:
        cashflow_st_dict[ticker][col] = cashflow_st_dict[ticker][col].str.replace(',|-', '')
        cashflow_st_dict[ticker][col] = pd.to_numeric(cashflow_st_dict[ticker][col], errors = "coerce")