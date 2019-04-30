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


def Oracle_Run():
    start_time = datetime.time(23,46, 50)#would be 14:30:00 (9:30am(EST) US Market open)
    endtime = datetime.time(23, 47, 10)#would be 21:00:00 (4:00pm(EST) US Market Close)

    Market_Open = start_time.isoformat(timespec='seconds')
    Market_Close  = endtime.isoformat(timespec='seconds')

    while True:
        if Day_Checker()[0]==range(0,5) :#first checks that the day is mon-fri
            if ((datetime.datetime.now().time().isoformat(timespec='seconds'))>Market_Open and #then checks the time is during market hours 
                (datetime.datetime.now().time().isoformat(timespec='seconds')) < Market_Close): 
                print('The Market is Open')
                time.sleep(2)
            else:
                
                print('The Market is Closed')
                time.sleep(2)
                #this elif statement checks whether the market is open    
        else:
            print('The Market is Closed')
            time.sleep(2)

Oracle_Run()
            