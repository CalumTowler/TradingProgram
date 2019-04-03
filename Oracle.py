# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 21:53:55 2019
@author: Calum
"""
from Stock import Stock
import time
import glob

StockTickers = ['SPX', 'TVC', 'FB', 'TWTR', 'NEM', 'WMT', 'XOM', 'SRCL', 'COP', 'SBUX', 'PFE', 'MSFT', 'NVDA', 'EOG', 'AES', 'PPL', 'BAC']

for i in StockTickers:   
    Stocks = Stock(i)
    Stocks.collect_intraday_data()
    Stocks.collect_daily_data()
    time.sleep(10)
    print("Done with "+str(i))

#Ticker = Stock('TVC')
#Path = 'WebExtract/StockData/'+Ticker.ticker+'/*.csv'
#List = glob.glob(Path)
#for i in List:
#    Data = pd.read_csv(i)

