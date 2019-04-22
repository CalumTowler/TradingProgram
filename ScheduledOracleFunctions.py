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




MyKey ='28M2VQTADUQ0HSCP'
ts = TimeSeries(key=MyKey, output_format='pandas')

class Stock():
    Today = datetime.datetime(2019, 4, 13)
    
    def __init__(self, ticker):
        self.ticker = ticker
    #first pull of full 5 day data to create primary library 
    def initial_pull(self):
        
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min', 'full')
        
        print(Today)
        Today_str = Today.strftime("%Y-%m-%d")
        print(Today_str)
        Filename = str(self.ticker)+str(Today_str)+'1min'+'.csv'
        FilePath = 'C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData' + '\\' + str(self.ticker) 
        stockdata.to_csv(FilePath+Filename)

        def prilib(Today):
            #make dataframe of 5 day file, change data type from float64 to float 32 to substantially save memory (standard is float64)
            Yesterday = Today - timedelta(1)
            Yesterday_str = Yesterday.strftime("%d/%m/%Y")
            print(Yesterday_str)
            M1PL=pd.read_csv('C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData\SPXSPX'
                             + '1minf' +'.csv',
                             dtype={'1. open':np.float32,'2. high':np.float32, '3. low':np.float32, '4. close':np.float32, '5. volume':np.int})
           
            
            #remove days that are not today (to save 80% od data as each full pull gives 5 days )
            M1PL=M1PL[M1PL['date'].str.match(Yesterday_str)]#makes primary library of only yesterdays data 
            print(M1PL)
            #make usable primary library of today and make excel file whcih replaces old file 
            M1PL=M1PL.sort_values(by='date',ascending=False) #changes date order
            M1PL=M1PL.set_index('date')
            print(M1PL)
            Yesterday_str = Yesterday.strftime("%d-%m-%Y") #cant accept date formart as d/m/y for file name obvs
            M1PL.to_csv('C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData\SPXSPX'+ str(Yesterday_str) + '1min' +'.csv')
            return M1PL          
        prilib=prilib(Today)
        return prilib
    prilib=initial_pull()
             
        #this newdata pull will pull data every min and update the primary library with this new data
    def update_pull(self):
        
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min', 'compact')#compact extracts only 100 data points 
        Today_str = Today.strftime("%Y-%m-%d")
        print(Today_str)
        Filename = str(self.ticker)+str(Today_str)+'1minc'+'.csv'
        FilePath = 'C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData' + '\\' + str(self.ticker) 
        stockdata.to_csv(FilePath+Filename)

        def update_prilib(prilib):
            upM1PL=pd.read_csv('C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData\SPXSPX1minc.csv',
                               dtype={'1. open':np.float32,'2. high':np.float32, '3. low':np.float32, '4. close':np.float32, '5. volume':np.int},
                               skiprows=range(1,100)) #only takes newest data point 

            upM1PL.set_index('date', inplace=True) # sets index as date
            prilib=prilib.append(upM1PL) # adds new datat point to prilib
            prilib=prilib.sort_values(by='date',ascending=False) #to make sure list has newest values first
            return prilib
        prilib=update_pull(prilib)
        return prilib
    prilib=update_pull()
    



#schedullllerrrr

start_time = datetime.time(2,11, 30)#would be 14:30:00 (9:30am(EST) US Market open)
endtime = datetime.time(2, 11, 40)#would be 21:00:00 (4:00pm(EST) US Market Close)

Market_Open = start_time.isoformat(timespec='seconds')
Market_Close  = endtime.isoformat(timespec='seconds')

    


schedule.every().day.at(Market_Open).do(initial_pull) 
schedule.every(60).seconds.do(update_pull)


while True:
   #first if statement checks whether the market is clsoed
    if ((datetime.datetime.now().time().isoformat(timespec='seconds'))<Market_Open or 
        (datetime.datetime.now().time().isoformat(timespec='seconds')) > Market_Close):
        time.sleep(1)
        print('The Market is Closed')
        #this elif statement checks whether the market is open
    elif ((datetime.datetime.now().time().isoformat(timespec='seconds'))>Market_Open and 
          (datetime.datetime.now().time().isoformat(timespec='seconds')) < Market_Close):
        
        schedule.run_pending()
        time.sleep(1)
    
    


    
    





    


    







