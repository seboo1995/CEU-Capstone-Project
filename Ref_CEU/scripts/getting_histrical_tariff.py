#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 15:10:06 2020
am using the spredsheet from national grid which can be found 
<a href = "https://www.nationalgrideso.com/document/5073 /download"> here </a>
@author: sebair
"""


import numpy as np
import pandas as pd
import re
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

