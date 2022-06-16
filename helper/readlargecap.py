#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 29 16:22:02 2022

@author: kruthic
"""

import csv

large_cap = []

file = open('largecap.csv')
csvreader = csv.reader(file)

for row in csvreader:
    large_cap.append(row[2])
    
large_cap = large_cap[1:]

large_cap = [x+".NS" for x in large_cap]