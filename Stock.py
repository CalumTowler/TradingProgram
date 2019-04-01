"""
Testing out Classes

24/03/19: initial commit
Author: Calum Towler
"""
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
import matplotlib.pyplot as plt
import time

MyKey ='28M2VQTADUQ0HSCP'
ts = TimeSeries(key=MyKey, output_format='pandas')

class Stock():
    
    def __init__(self, ticker):
        self.ticker = ticker
        
    def collect_intraday_data(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker,'1min','full')
        Datetime = datetime.now()
        Datetime_str = Datetime.strftime("%m-%d-%Y_%H-%M-%S")
        Filename = str(self.ticker)+str(Datetime_str)+'.csv'
        FilePath = 'C:\\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData' + '\\' + str(self.ticker) + '\\'
        stockdata.to_csv(FilePath+Filename)
        stockdata['4. close'].plot()
        Title = 'Intraday Times Series for the '+str(self.ticker)+' stock (1 min)'
        plt.title(Title)
        plt.show()
        return stockdata
    
    def collect_daily_data(self):
        stockdata, meta_stockdata = ts.get_daily(self.ticker,'1min','full')
        Datetime = datetime.now()
        Datetime_str = Datetime.strftime("%m-%d-%Y_%H-%M-%S")
        Filename = str(self.ticker)+str(Datetime_str)+'Daily20Year.csv'
        FilePath = 'C:\\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData' + '\\' + str(self.ticker) + '\\'
        stockdata.to_csv(FilePath+Filename)
        stockdata['4. close'].plot()
        Title = 'Daily Times Series for the '+str(self.ticker)+' stock (1 min)'
        plt.title(Title)
        plt.show()
        return stockdata
                       
        