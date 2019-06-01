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
import datetime
import sched  
import schedule 
from datetime import timedelta
import time
import Dataframe
from Dataframe import Day_Checker
from Dataframe import Stock
import threading 

def first():
    global x
    x=1
    print(x)
    return x

def repeat():
    global x
    x=x+1
    print(x)
    return x

def Day_Checker():

    Today = datetime.datetime.now()
    Todayday = datetime.datetime.weekday(Today)

    if Todayday==0:    
        n=3
        Today_str = Today.strftime("%Y-%m-%d")
        Yesterday = Today - timedelta(n)    
        Yesterday_str = Yesterday.strftime("%Y-%m-%d")
    else:
        n=1
        Today_str = Today.strftime("%Y-%m-%d")
        Yesterday = Today - timedelta(n)
        Yesterday_str = Yesterday.strftime("%Y-%m-%d")
    
    
    return Todayday, Today_str, Yesterday_str 



def Oracle_Run():
    
    n=1
    start_time = datetime.time(2,13, 00) 
    end_time = datetime.time(2, 13, 30) 
    pre_time = datetime.time(2,(13-n),30)
    
    Market_Open = start_time.isoformat(timespec='seconds')
    Market_Close  = end_time.isoformat(timespec='seconds')
    Initial_Pull = pre_time.isoformat(timespec='seconds')

    StockTickers = ['SPX','AMD']
    
    while True:
        while (Day_Checker()[0] in range(6)):
          while ((datetime.datetime.now().time().isoformat(timespec='seconds'))>Initial_Pull and 
                 (datetime.datetime.now().time().isoformat(timespec='seconds'))< Market_Open):
                  
               

                  for i in StockTickers:   
                      Stocks = Stock(i, 'D:\\Dream\Oracle\Program\TradingProgram\WebExtract\StockData\\')
                      Stocks.initial_pull()
                      Stocks.prilib()
                  
                  
                  time.sleep(5)
  
          while ((datetime.datetime.now().time().isoformat(timespec='seconds'))>Market_Open and 
                 (datetime.datetime.now().time().isoformat(timespec='seconds')) < Market_Close): 
                  
                  b = threading.Thread(target=repeat(), )
                  time.sleep(1)
            
            
          
        else:
            print('The Market is Closed')
            time.sleep(2)

Oracle_Run()


    
    
    
            