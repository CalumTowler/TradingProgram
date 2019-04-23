# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 20:29:23 2019

@author: Alex
"""

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import sched  
import schedule 
from datetime import timedelta
import time




MyKey ='28M2VQTADUQ0HSCP'
ts = TimeSeries(key=MyKey, output_format='pandas')
Today = datetime.now()
Yesterday = Today - timedelta(1)
Yesterday_str = Yesterday.strftime("%Y-%m-%d")

class Stock():
    
    def __init__(self, ticker, path):
        self.ticker = ticker
        self.path = path
    #first pull of full 5 day 1min data to create primary library 
    def initial_pull(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min','full')
        Filename = str(self.ticker) + str(Yesterday_str)+'.csv'
        FilePath = str(self.path)
        stockdata.to_csv(FilePath+Filename)
        
    def prilib(self):
        #make dataframe of 5 day file, change data type from float64 to float 32 to substantially save memory (standard is float64)
        M1PL=pd.read_csv(str(self.path) + str(self.ticker)+str(Yesterday_str)+'.csv',
                         dtype={'1. open':np.float32,'2. high':np.float32, '3. low':np.float32, '4. close':np.float32, '5. volume':np.int})
        #remove days that are not today (to save 80% od data as each full pull gives 5 days )
        M1PL=M1PL[M1PL['date'].str.contains(Yesterday_str)]#makes primary library of only yesterdays data 
        print(M1PL)
        #make usable primary library of today and make excel file whcih replaces old file 
        M1PL=M1PL.sort_values(by='date',ascending=False) #changes date order
        M1PL=M1PL.set_index('date')
        print(M1PL)
        M1PL.to_csv(str(self.path)+str(self.ticker)+str(Yesterday_str)+'.csv')
        return M1PL      
    
        #this newdata pull will pull data every min and update the primary library with this new data
    def update_pull(self):
        
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min', 'compact')#compact extracts only 100 data points 
        Today_str = Today.strftime("%d-%m-%Y")
        Filename = str(self.ticker)+str(Today_str)+'1minc'+'.csv'
        FilePath = str(self.path) + '\\' + str(self.ticker) + '\\'
        stockdata.to_csv(FilePath+Filename)

    def update_prilib(self, prilib, update_pull):
        Today_str = Today.strftime("%d-%m-%Y")
        upM1PL=pd.read_csv(str(self.path)+str(self.ticker)+str(Today_str)+'1minc'+'.csv',
                           dtype={'1. open':np.float32,'2. high':np.float32, '3. low':np.float32, '4. close':np.float32, '5. volume':np.int},
                           skiprows=range(1,100)) #only takes single newest data point 
        upM1PL.set_index('date', inplace=True) # sets index as date
        prilib=prilib.append(upM1PL) # adds new datat point to prilib
        prilib=prilib.sort_values(by='date',ascending=False) #to make sure list has newest values first
        prilib=update_pull(prilib)
        return prilib