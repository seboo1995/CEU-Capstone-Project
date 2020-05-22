#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
This script is for the functions that I will use in the notebook in order not to
polute the envioroment


"""






#####################################################################
"""
Created on Thu May  7 11:21:15 2020

This is how I will get the national data csv files to dataframe

The csv files are downloaded from national grid(https://www.nationalgrideso.com/balancing-data/data-finder-and-explorer)


@author: sebair"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import os
import re
import warnings
warnings.filterwarnings("ignore")


def demand_data_to_dataframe(aggregate = "Y"):
    """ This function is just to get the csv files from /data/national_demand to one pandas dataframe
    Input: aggregate: -> how to aggregate the data(in python: resample)
    
    """
    
    #path to data
    file_path =  "../data/demand_data/"
    
    print("Getting data from",file_path)
    
    print("Files are: ",os.listdir(file_path))
    
    
    
    #the names of the csv files are in the list   
    csv_files = os.listdir(file_path)
    #dictionary for temporary holding the data
    temp = {}
    
    #looping through the names of the folder /data/demand_data and puttig the 
    #dataframes in dictionary
    for i in csv_files:
        # the try blcok is because there is one docx file, the descriptor
        try:
            year = i.split("_")[1]
            print("Reading the file",i)
             
            temp_df = pd.read_csv(file_path+i)
                
                
            print("For",year)
            
            temp_df["SETTLEMENT_DATE"] = pd.to_datetime(temp_df["SETTLEMENT_DATE"])
            #print("+++++++++++++++++++++++++++++++")
            ##print(temp["SETTLEMENT_DATE"].year)
            #print("________________________________")
            
            temp_df["log_ND"] = temp_df.apply(make_log_ND,axis=1)
            print(temp_df.head())
            
            #doesnt worl
            #temp_df.set_index("SETTLEMENT_DATE",inplace = True)
            
            
            temp_df.index = temp_df.SETTLEMENT_DATE
            
            #temp_df["year"] = year
              
            #the data is daily, and this is tp aggreagate and its the sum
            temp_df = temp_df.resample(aggregate).sum()
            
            #putting it to the dict
            temp[year] = temp_df[["log_ND"]]
                        
            
            
    
        except Exception as e:
            print("Exception",e)
            pass
    #creating empty dataframe to be filled with the resampled data
    final_df = pd.DataFrame(columns = ["log_ND"])
   
    for i,d in temp.items():
        final_df = pd.concat([final_df,d
                              ])
        
    
    return final_df




##########################################################################

"""
Created on Fri May  8 18:45:56 2020
I also try to get stock data from national grid and see if it works


@author: sebair
"""


def get_stock_data():
    
    """
    This function gets the national grid stock data from yahoo finance and
    aggregate to yearly data
    
    
    """
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



###########################################################
"""
Created on Thu May  7 11:21:15 2020

This is how I will get the national data csv files to dataframe

The csv files are downloaded from national grid(https://www.nationalgrideso.com/balancing-data/data-finder-and-explorer)


@author: sebair"""


#import matplotlib.pyplot as plt

def make_log_ND(j):
    """ 
    Just to make function that makes log10 of National Demand
    """
    return np.log10(j.ND)


###############################################################





"""
Created on Thu May  7 15:10:06 2020
am using the spredsheet from national grid which can be found 
<a href = "https://www.nationalgrideso.com/document/5073 /download"> here </a>
@author: sebair
"""


import warnings
warnings.filterwarnings("ignore")

def get_historical_tariff():
    
    data_path = "../data/historical_TNUoS_tariff_data/TNUoS Tariffs 2005-06 to 2019-20.xlsx"
    
    #there is one xlsx file wiht multiple sheet, and for pandas I
    #need to create names for the sheet(to read only demand tariffs)
    
    years = ["Dem "+ str(i)+"-"+str(i%100 + 1) for i in range(2005,2020)]
    
    ## The names are very strange until 2008, the names of the sheets are:
    ## 2006-07 format, and after 2008, they are Dem 2009-10. Thay are also Generators
    ## tariffs
    for i in range(len(years)):
    #last two digits of the years list
        temp = years[i].split("-")
    #the sheet names are of the form 2005-06
        if int(temp[1]) < 10:
        #the sheet for the years between 2005 and 2008 they
        #do not have the string "Dem"
            new_sheet_name = temp[0].split(" ")[1] + "-0" + temp[1]
            years[i] = new_sheet_name
    #reading the sheets that have the names as the var years
    sheets = pd.read_excel(data_path,sheet_name = years,skiprows = 5)

    print("Done with reading the data")
    print("Sheets read:",sheets)
    
    for i,j in sheets.items():
        try:
            if int(i.split("-")[0]) <= 2008:
              #  print("This is for",i)
     
                temp = sheets[i][sheets[i].columns[2:]][0:35]
                sheets[i] = temp
                #new columns as year
                sheets[i]["year"] = i.split("-")[0]
    
                if  int(i.split("-")[0]) == 2005:
                    sheets[i]["residual"] = sheets[i].loc[sheets[i].shape[0]-1,"Zonal Tariff (£/kW)"]
                else:
                    sheets[i]["residual"] = sheets[i].loc[sheets[i].shape[0]-1,"Zone No..1"]
                
                sheets[i] = sheets[i][sheets[i].columns[3:]][1:14]
    
        #this acts as the embeded else, because it gets me the error
        #for invalid itteral(meaning that I have strings and I see
        #it as number)
        except Exception as e:
            #print("excepption")
            #year = i.split(" ")[0]
            #print(e)
            pass
        
        if i.startswith("Dem"):
            year= i.split(" ")[1].split("-")[0]
          #  print("year",year)
           # print("For sheet",i,"the shape is",sheets[i].shape)
            #Until 2012 its fine
            if(int(year) <= 2012 ):
            #    print("The residual demand tariff is  ", sheets[i].iloc[18,4])
                res_demand = sheets[i].iloc[18,4]
                sheets[i]["residual_demand"] = res_demand
                
             #   print("__________________________________")
            elif int(year) >= 2013 and int(year) <= 2016:
              #  print("The residual demand tariff is  ", sheets[i].iloc[18,4])
                sheets[i]["residual_demand"] = sheets[i].iloc[18,4]
               # print("__________________________________")
            else:
                #it contains characters, but I excluded the pound sign
                sheets[i]["residual_demand"] = re.sub('[^0-9,.]', '', str(sheets[i].iloc[18,4]))
                #print("__________________________________")
                
        sheets[i] = sheets[i][:14]
        #print(sheets["Dem 2009-10"])
    
    for sheet in sheets:
        for col in sheets[sheet]: 
            if col.startswith("Unnamed"):
         #       print("For sheet",sheet,"the column",col,"will be dropped")
                sheets[sheet].drop([col],axis=1,inplace=True)
    for sheet in sheets:
        if sheet.startswith("Dem"):
          #  print("Adding year column to sheet",sheet)
            temp = sheet.split("-")
            year = ''.join(filter(lambda i: i.isdigit(), temp[0]))
            sheets[sheet]['year'] = year
           # print("Finished with sheet",sheet)
    for i,j in sheets.items():
       for col in j.columns:
             if(re.search("Zone No.",col)):
                    j.drop(col,axis=1,inplace=True)
                    
    columns = ["zone_name","hh_zonal","nhh_zonal","residual","year"]
    for i,j in sheets.items():
        zone_name = (j.filter(regex = "Zone.").columns[0])
        
        hh_zonal = j.filter(regex = "^HH").columns[0]
        #print(hh_zonal)
        
        nhh_zonal  = j.filter(regex = "^NHH").columns[0]
        #print(nhh_zonal)
        
        res = (j.filter(regex = "^res").columns[0])
        #print(res)
        
        year = (j.filter(regex = "^year").columns[0])
        #print(year)
        
        j.rename(columns = {
            zone_name:"zone_name",
            hh_zonal:"hh_zonal",
            nhh_zonal:"nhh_zonal",
            res:"residual",
            year:'year'
            
            
        },inplace=True)
    final_df = pd.DataFrame(columns=columns)

    for i,j in sheets.items():
        final_df = pd.concat([final_df,j[columns]])
    
    return final_df

##################################################

"""
Created on Thu May  7 14:56:31 2020

This script is for getting the inflation data. This data is downloaded from OECD,
and on this link(https://data.oecd.org/price/inflation-cpi.htm#indicator-chart)


@author: sebair
"""
#data = pd.read_csv("../data/inflation_cpi_data/inflation.csv")
#print(data[data.LOCATION == "GBR"])

def get_inflation_data():
    
    file_path = "../data/inflation_cpi_data/inflation.csv"
    
    infl_data = pd.read_csv(file_path) 
    
    #filtering for GBR(Great Britain)

    
    #returning the data 
    return infl_data[infl_data.LOCATION == "GBR"][["TIME","Value"]]



"""
Created on Fri May  8 17:37:00 2020

@author: sebair
"""

### NEED TO FIND A WAY TO READ THE REPORTS, BUT FOR NOW I WILL READ THEM 
### MANUALLY. There is a csv file



def get_op_cost():
    file_paths = "../data/reports_from_nget/op_cost.csv"

    df = pd.read_csv(file_paths)

    return df
### adfuller_test

from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic

def adfuller_test(series, signif=0.05, name='', verbose=False):
    """Perform ADFuller to test for Stationarity of given series and print report"""
    r = adfuller(series, autolag='AIC')
    output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
    p_value = output['pvalue'] 
    def adjust(val, length= 6): return str(val).ljust(length)

    # Print Summary
    print(f'    Augmented Dickey-Fuller Test on "{name}"', "\n   ", '-'*47)
    print(f' Null Hypothesis: Data has unit root. Non-Stationary.')
    print(f' Significance Level    = {signif}')
    print(f' Test Statistic        = {output["test_statistic"]}')
    print(f' No. Lags Chosen       = {output["n_lags"]}')

    for key,val in r[4].items():
        print(f' Critical value {adjust(key)} = {round(val, 3)}')

    if p_value <= signif:
        print(f" => P-Value = {p_value}. Rejecting Null Hypothesis.")
        print(f" => Series is Stationary.")
    else:
        print(f" => P-Value = {p_value}. Weak evidence to reject the Null Hypothesis.")
        print(f" => Series is Non-Stationary.")
    return p_value    



















