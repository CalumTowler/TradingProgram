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
from Dataframe import day_checker
from Dataframe import Stock
import threading
import timeit

def day_checker():

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


def timing():

    n = 1
    x = 1
    y = 45

    start_time = datetime.time(x, y, 00)
    end_time = datetime.time(x, y+10, 30)
    pre_time = datetime.time(x, (y - n), 30)  # time before market opens to get initial pull

    market_open = start_time.isoformat(timespec='seconds')
    market_close = end_time.isoformat(timespec='seconds')
    pre_market = pre_time.isoformat(timespec='seconds')

    market_open1 = datetime.datetime.combine(datetime.date.today(), start_time)
    sleep = market_open1 - (datetime.datetime.now())
    sleep = sleep.total_seconds()
    time_now = (datetime.datetime.now().time().isoformat(timespec='seconds'))
    return pre_market, market_open, market_close, sleep, time_now

def Oracle_Run():

    # creating names of unique dataframe names
    stock_ticker = ['NVDA','AMD']

    while True:
        while (day_checker()[0] in range(5)):
          while (timing()[0]<timing()[4]<timing()[1]):



              for i in stock_ticker:
                  Stocks = Stock(i,'D:\Dream\Oracle\Program\TradingProgram\WebExtract\StockData')
                  Stocks.initial_pull()#need to change M1PL variable name to a unique one for stocks
                  Stocks.prilib()
                  if (i==stock_ticker[-1]):
                      time.sleep(timing()[3])





                  
  
          while (timing()[1]<timing()[4]<timing()[2]):

              for i in stock_ticker:
                  tic=timeit.default_timer()
                  Stocks = Stock(i, 'D:\Dream\Oracle\Program\TradingProgram\WebExtract\StockData')
                  Stocks.update_pull()  # need to change M1PL variable name to a unique one for stocks
                  Stocks.update_prilib()
                  if (i==stock_ticker[-1]):
                      toc = timeit.default_timer()
                      quick_sleep = toc - tic
                      time.sleep(60-2*quick_sleep)








            
            
          
        else:
            print('The Market is Closed')
            time.sleep(2)

Oracle_Run()


    
    
    
            