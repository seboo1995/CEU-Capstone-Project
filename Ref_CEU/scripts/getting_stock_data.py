#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 18:45:56 2020
I also try to get stock data from national grid and see if it works


@author: sebair
"""

import pandas as pd

def get_stock_data():
    file_path = "../data/stock/stock.csv"
    #reading the data
    df = pd.read_csv(file_path)        
    
    #setting the index to resample it to yearly data
    # I will get the mean of the aggregation
    df.Date = pd.to_datetime(df.Date)
    df.set_index("Date",inplace=True)
    df = df.resample("y").mean()
    
    df = df[df.index.year >= 2007]
    
    
    df = df[["Adj Close","Volume"]]
    

        
    return(df)
