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
    todayday = datetime.datetime.weekday(today)

    if todayday==0:
        n=3
        today_str = today.strftime("%Y-%m-%d")
        yesterday = today - timedelta(n)
        yesterday_str =yesterday.strftime("%Y-%m-%d")
    else:
        n=1
        today_str = today.strftime("%Y-%m-%d")
        yesterday = today - timedelta(n)
        yesterday_str = yesterday.strftime("%Y-%m-%d")

    return todayday, today_str, yesterday_str

class Stock:
    global df_names
    df_names = {'NVDA': 'NVDAdf', 'AMD': 'AMDdf'}

    global temp_df_names
    temp_df_names = {'SPX': 'SPXtdf', 'AMD': 'AMDtdf'}

    def __init__(self, ticker, path):
        self.ticker = ticker
        self.path = path
        #first pull of full 5 day 1min data to create primary library

    def initial_pull(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker, '1min', 'full')
        filename = str(self.ticker) + str(day_checker()[2])+'.csv'
        filepath = str(self.path)
        stockdata.to_csv(filepath+filename)

    def prilib(self):

        #make dataframe of 5 day file, change data type from float64 to float 32 to substantially
        #save memory (standard is float64)
        df_names[str(self.ticker)] = pd.read_csv(str(self.path) + str(self.ticker)+str(day_checker()[2])+'.csv', dtype={'1. open':np.float32,'2. high':np.float32, '3. low':np.float32, '4. close':np.float32, '5. volume':np.int})
        #remove days that are not today (to save 80% od data as each full pull gives 5 days )
        df_names[str(self.ticker)] = df_names[str(self.ticker)]\
                                     [df_names[str(self.ticker)]['date'].str.contains(day_checker()[2])]
        #makes primary library of only yesterdays data
        df_names[str(self.ticker)] = df_names[str(self.ticker)].sort_values(by='date',ascending=False) #changes date order
        df_names[str(self.ticker)] = df_names[str(self.ticker)].set_index('date')
        df_names[str(self.ticker)].to_csv(str(self.path)+str(self.ticker)+str(day_checker()[2])+'.csv')
        #make usable primary library of today and make excel file whcih replaces old file
        print(df_names[str(self.ticker)])
        return df_names[str(self.ticker)]
    
        #this newdata pull will pull data every min and update the primary library with this new data

    def update_pull(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min', 'compact')#compact extracts only 100 data points 
        filename = str(self.ticker)+str(day_checker()[1])+'1minc'+'.csv'
        filePath = str(self.path)
        stockdata.to_csv(filePath+filename)

    def update_prilib(self):
        temp_df_names[str(self.ticker)]=pd.read_csv(str(self.path)+str(self.ticker)+str(day_checker()[1])+'1minc'+'.csv',
                           dtype={'1. open':np.float32,'2. high':np.float32, '3. low':np.float32, '4. close':np.float32, '5. volume':np.int},
                           skiprows=range(1,100)) #only takes single newest data point 
        temp_df_names[str(self.ticker)].set_index('date', inplace=True) # sets index as date
        df_names[str(self.ticker)]=df_names[str(self.ticker)].append(temp_df_names[str(self.ticker)]) # adds new datat point to prilib
        df_names[str(self.ticker)]=df_names[str(self.ticker)].sort_values(by='date',ascending=False) #to make sure list has newest values first
        print(df_names[str(self.ticker)])
        return df_names[str(self.ticker)]

