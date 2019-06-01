# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:19:31 2019

@author: Alex
"""
    
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import datetime
import sched  
import schedule 
from datetime import timedelta
import time
from timeloop import Timeloop
from datetime import timedelta
import threading 
from Dataframe import Stock

class test():
    

    def test():
        global g
        g=1+3
        print(g)
        time.sleep(6)
        print(g)
        return g
        
    def test1():
        time.sleep(1)
        global g
        g=g+1
        print(g)
        return g
        
    
targets=[test.test, test.test1]    

for i in targets:     
    t=threading.Thread(target=i, name = 'test')

#t=threading.Thread(target=test.test1, name ='test1')
    t.start()  



print('hello')



  


    
    





    


    







