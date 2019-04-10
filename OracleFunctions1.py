"""
Testing out Classes

24/03/19: initial commit
Author: Calum Towler
"""
#from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import itertools
from itertools import islice
import sched
import time 
from sched import scheduler
from datetime import timedelta
#MyKey ='28M2VQTADUQ0HSCP'
#ts = TimeSeries(key=MyKey, output_format='pandas')

class Stock():
    
    #def __init__(self, ticker):
        #self.ticker = ticker
        
    #def collect_intraday_data(self):
        #stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min','full')
        #Datetime = datetime.now()
        #Datetime_str = Datetime.strftime("%m-%d-%Y_%H-%M-%S")
        #Filename = str(self.ticker)+str(Datetime_str)+'.csv'
        #FilePath = 'C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData' + '\\' + str(self.ticker) 
        #stockdata.to_csv(FilePath+Filename)
        #stockdata['4. close'].plot()
        #Title = 'Intraday Times Series for the '+str(self.ticker)+' stock (1 min)'
        #plt.title(Title)
        #plt.show()
        #return stockdata
    
   # def collect_daily_data(self):
        #stockdata, meta_stockdata = ts.get_daily(self.ticker,'full')
        #Datetime = datetime.now()
        #Datetime_str = Datetime.strftime("%m-%d-%Y_%H-%M-%S")
        #Filename = str(self.ticker)+str(Datetime_str)+'Daily20Year.csv'
        #FilePath = 'C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData' + '\\' + str(self.ticker) 
        #stockdata.to_csv(FilePath+Filename)
        #stockdata['4. close'].plot()
        #Title = 'Daily Times Series for the '+str(self.ticker)+' stock'
        #plt.title(Title)
        #plt.show()
        #return stockdata)
    
    #z=data_extract('C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData\FBFB04-05-2019_21-49-12.csv')
    
    def data_extract(filepath):
        

            with open(filepath) as xfile:
                for row in islice(csv.reader(xfile), 2, 3):
           
                    return(row)
                    
    
    bank = (list('0'))*50
    #print(bank)
    
    with open('C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData\FBFB04-05-2019_21-49-12.csv') as z:
            for row in islice(csv.reader(z), 1, 2):
                t=row
    x=50
    bank.insert(0,t)
    #print(bank)
    time.sleep(1) #60 seconds in real life
              
    
   
   
        
        

    scheduler = sched.scheduler(timefunc=time.time)
    
    def data_store(store):
        
        x=50
        
        if len(store) < x+1:
        
            with open('C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData\FBFB04-05-2019_21-49-12.csv') as z:
                for row in islice(csv.reader(z), 2, 3):
                    z=row
            store.insert(0,z)
            print (store)
        else:
            del store [x]
            print(store)             
            return store
        
        print(store)
    
   
    
        scheduler.enter(5, priority=0, action=data_store(bank))
    
    data_store(bank)
    
    try:
        scheduler.run(blocking=True)
    except KeyboardInterrupt:
        print('stopped')
    
    
    
   
    
   
    
    

        
        
        
    #data=z  
   # print('data')
  # def data_storage(data)   
  #  for n in range(1,)
   # q=0
 #   n=q+1
   # 2d1m = {n:data} #2d=2 day time period, 1m=1 minute data
   # print(2d1m)
        
    #del 2d1m(3)   
        
        
        
    
    
        

        
    