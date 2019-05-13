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


print(Day_Checker()[0])

def Oracle_Run():
    
    start_time = datetime.time(1,14, 10)#would be 14:30:00 (9:30am(EST) US Market open)
    endtime = datetime.time(1, 14, 30)#would be 21:00:00 (4:00pm(EST) US Market Close)

    Market_Open = start_time.isoformat(timespec='seconds')
    Market_Close  = endtime.isoformat(timespec='seconds')

    while True:
        if Day_Checker()[0]==range(5):#first checks that the day is mon-fri
          print('m')
          f=threading.Thread(target=first(), name ='t') 
           
          while ((datetime.datetime.now().time().isoformat(timespec='seconds'))>Market_Open and #then checks the time is during market hours 
              (datetime.datetime.now().time().isoformat(timespec='seconds')) < Market_Close): 
              repeat()
              print("Moneytime")
              r=threading.Thread(target=repeat(), name = 'test')
              time.sleep(1)
          
        else:
            print('The Market is Closed')
            time.sleep(2)

Oracle_Run()
            