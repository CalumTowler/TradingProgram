
from alpha_vantage.timeseries import TimeSeries
import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
import time
import matplotlib.pyplot as plt
import csv
import sched
import schedule


MyKey ='28M2VQTADUQ0HSCP'
ts = TimeSeries(key=MyKey, output_format='pandas')

def Day_Checker():

    Today = datetime.datetime.now()
    Todayday = datetime.datetime.weekday(Today)

    if Todayday==0:    
        n=3
        Today_str = Today.strftime("%Y-%m-%d")
        Yesterday = Today - timedelta(n)    
        Yesterday_str = Yesterday.strftime("%Y-%m-%d")
    else:
        n=2
        Today_str = Today.strftime("%Y-%m-%d")
        Yesterday = Today - timedelta(n)
        Yesterday_str = Yesterday.strftime("%Y-%m-%d")
    
    
    return Todayday, Today_str, Yesterday_str 

class Stock():
    
    def __init__(self, ticker, path):
        self.ticker = ticker
        self.path = path
        #first pull of full 5 day 1min data to create primary library 
        
    def initial_pull(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min','full')
        print(len(stockdata))
        #print(stockdata)
        i = 1
        while len(stockdata) < 1938:
            stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min','full')
            print(len(stockdata))
            time.sleep(20)
            Filename = str(self.ticker) + str(Day_Checker()[2]) + 'No' + str(i) + '.csv'
            FilePath = str(self.path)
            stockdata.to_csv(FilePath+Filename)
            i+=1