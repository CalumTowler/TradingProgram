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
    x=18
    y=8
    
    
    start_time = datetime.time(x,y, 00) 
    end_time = datetime.time(x, y, 30) 
    pre_time = datetime.time(x,(y-n),30)
    
    Market_Open = start_time.isoformat(timespec='seconds')
    Market_Close  = end_time.isoformat(timespec='seconds')
    Initial_Pull = pre_time.isoformat(timespec='seconds')

    StockTickers = ['SPX','AMD']
    
    while True:
        while (Day_Checker()[0] in range(6)):
          while ((datetime.datetime.now().time().isoformat(timespec='seconds'))>Initial_Pull and 
                 (datetime.datetime.now().time().isoformat(timespec='seconds'))< Market_Open):
                  
               

                  for i in StockTickers:   #need to pause loop during loop
                      Stocks = Stock(i, 'C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\\') 
                      Stocks.initial_pull()#need to change M1PL variable name to a unique one for stocks 
                      Stocks.prilib()
                      Stocks.update_pull()
                      Stocks.update_prilib()
                      time.sleep(10)
                  
  
          while ((datetime.datetime.now().time().isoformat(timespec='seconds'))>Market_Open and 
                 (datetime.datetime.now().time().isoformat(timespec='seconds')) < Market_Close): 
                  
                  for i in StockTickers:   
                      Stocks = Stock(i, 'D:\\Dream\Oracle\Program\TradingProgram\WebExtract\StockData\\')
                      Stocks.update_pull()
                      Stocks.update_prilib()
                      time.sleep(5)
            
            
          
        else:
            print('The Market is Closed')
            time.sleep(2)

Oracle_Run()


    
    
    
            