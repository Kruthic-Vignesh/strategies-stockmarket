#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 16:54:24 2022

@author: kruthic
"""

pct_change()    :   cur_price/prev_day_price - 1
shift(x)        :   if x > 0: pushes down rows by x
                    else    : pushes up rows by x
ewm             :   exponential weighting
cumprod         :   cumulaive product       (entry(x) *= entry(1) * (2) * (3) .. * (x-1))