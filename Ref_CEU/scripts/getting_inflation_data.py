#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 14:56:31 2020

This script is for getting the inflation data. This data is downloaded from OECD,
and on this link(https://data.oecd.org/price/inflation-cpi.htm#indicator-chart)


@author: sebair
"""


import pandas as pd
import  numpy as np

#data = pd.read_csv("../data/inflation_cpi_data/inflation.csv")
#print(data[data.LOCATION == "GBR"])

def get_inflation_data():
    
    file_path = "../data/inflation_cpi_data/inflation.csv"
    
    infl_data = pd.read_csv(file_path) 
    
    #filtering for GBR(Great Britain)

    
    #returning the data 
    return infl_data[infl_data.LOCATION == "GBR"][["TIME","Value"]]