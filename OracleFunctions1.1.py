# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 00:50:17 2019

@author: Alex
"""
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import itertools
from itertools import islice


MyKey ='28M2VQTADUQ0HSCP'
ts = TimeSeries(key=MyKey, output_format='pandas')

class Stock():
    
    def __init__(self, ticker):
        self.ticker = ticker
        
    #def collect_intraday_data(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min','full')
        Datetime = datetime.now()
        Datetime_str = Datetime.strftime("%m-%d-%Y_%H-%M-%S")
        Filename = str(self.ticker)+str(Datetime_str)+'.csv'
        FilePath = 'C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData' + '\\' + str(self.ticker) 
        stockdata.to_csv(FilePath+Filename)
        stockdata['4. close'].plot()
        Title = 'Intraday Times Series for the '+str(self.ticker)+' stock (1 min)'
        plt.title(Title)
        plt.show()
        return stockdata
    
   # def collect_daily_data(self):
        stockdata, meta_stockdata = ts.get_daily(self.ticker,'full')
        Datetime = datetime.now()
        Datetime_str = Datetime.strftime("%m-%d-%Y_%H-%M-%S")
        Filename = str(self.ticker)+str(Datetime_str)+'Daily20Year.csv'
        FilePath = 'C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData' + '\\' + str(self.ticker) 
        stockdata.to_csv(FilePath+Filename)
        stockdata['4. close'].plot()
        Title = 'Daily Times Series for the '+str(self.ticker)+' stock'
        plt.title(Title)
        plt.show()
        return stockdata

     def data_extract(filepath, x, y):
        n, y = 1,2
        
        with open(filepath) as xfile:
            for row in islice(csv.reader(xfile), x, y):
           
                return(row)
                
                def data_store(filepath):
                    
                    while y <10:
                        z=data_extract('filepath', n, y )
                        n, y = y, y+1
                        k=n-1
                        return z
            
  
                p=data_store(filepath)
                print(p)
    z=data_extract(C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData\FBFB04-05-2019_21-49-12.csv, )
      