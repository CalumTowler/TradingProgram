# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 16:37:03 2019

@author: Alex
"""

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import datetime
import sched  
import schedule 
from datetime import timedelta
import time

MyKey = '28M2VQTADUQ0HSCP'
ts = TimeSeries(key=MyKey, output_format='pandas')


def day_checker():

    today = datetime.datetime.now()
    todayday = datetime.datetime.weekday(Today)

    if todayday==0:
        n=3
        today_str = today.strftime("%Y-%m-%d")
        yesterday = today - timedelta(n)
        yesterday_str =yesterday.strftime("%Y-%m-%d")
    else:
        n=2
        today_str = today.strftime("%Y-%m-%d")
        yesterday = today - timedelta(n)
        yesterday_str = yesterday.strftime("%Y-%m-%d")

    return todayday, today_str, yesterday_str


class Stock:



    def __init__(self, ticker, path, dataframe_name, temp_df_name):
        self.dataframe_name=dataframe_name
        self.temp_df_name = temp_df_name
        self.ticker = ticker
        self.path = path
        #first pull of full 5 day 1min data to create primary library

    def initial_pull(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker, '1min', 'full')
        filename = str(self.ticker) + str(day_checker()[2])+'.csv'
        filePath = str(self.path)
        stockdata.to_csv(filepath+filename)

    def prilib(self):
        for i in stock_ticker_names
            global i
        #make dataframe of 5 day file, change data type from float64 to float 32 to substantially
        #save memory (standard is float64)
            M1PL = pd.read_csv(str(self.path) + str(self.ticker)+str(day_checker()[2])+'.csv',
                         dtype={'1. open':np.float32,'2. high':np.float32, '3. low':np.float32, '4. close':np.float32, '5. volume':np.int})
        #remove days that are not today (to save 80% od data as each full pull gives 5 days )
        M1PL = M1PL[M1PL['date'].str.contains(Day_Checker()[2])]#makes primary library of only yesterdays data
        #make usable primary library of today and make excel file whcih replaces old file 
        M1PL = M1PL.sort_values(by='date',ascending=False) #changes date order
        M1PL = M1PL.set_index('date')
        M1PL.to_csv(str(self.path)+str(self.ticker)+str(Day_Checker()[2])+'.csv')
        print(M1PL)
        return M1PL
    
        #this newdata pull will pull data every min and update the primary library with this new data
    def update_pull(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min', 'compact')#compact extracts only 100 data points 
        Filename = str(self.ticker)+str(Day_Checker()[1])+'1minc'+'.csv'
        FilePath = str(self.path)
        stockdata.to_csv(FilePath+Filename)

    def update_prilib(self):
        global M1PL
        upM1PL=pd.read_csv(str(self.path)+str(self.ticker)+str(Day_Checker()[1])+'1minc'+'.csv',
                           dtype={'1. open':np.float32,'2. high':np.float32, '3. low':np.float32, '4. close':np.float32, '5. volume':np.int},
                           skiprows=range(1,100)) #only takes single newest data point 
        upM1PL.set_index('date', inplace=True) # sets index as date
        M1PL=M1PL.append(upM1PL) # adds new datat point to prilib
        M1PL=M1PL.sort_values(by='date',ascending=False) #to make sure list has newest values first
        print(M1PL)
        return M1PL

