"""
First trial of alpha vantage. (It works, were sticking with this for the moment!)

23/03/19: initial commit
25/03/19: Finally did something! Program can call intraday data for a tickr, and pull out the values. This is the
          beginning of manipulatable data.
Author: Calum Towler
"""
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas
from datetime import datetime

class Stock:
    def __init__(self, ticker, open_time, open_value, close_value, low, high, volume):
        self.ticker = ticker
        self.open_time = open_time
        self.open_value = open_value
        self.close_value = close_value
        self.low = low
        self.high = high
        self.volume = volume

Class StockData:   
    def __init__(Stock,)
    def direction_increasing(self):
        if self.open_value < self.close_value:
            return "Up"
        else:
            return "Down"

    def spike(self):
        if self.volume >= 100000:
            return "Spike"
        else:
            return "No Spike"
    def intraday_data(self):
        MyKey ='28M2VQTADUQ0HSCP'
        ts = TimeSeries(key=MyKey)
        stockdata, meta_stockdata = ts.get_intraday(Stock.ticker)
        Indexes = []
        Procstockdata = []
        for i in stockdata.keys():
            Indexes.append(i)
        for item in Indexes:
            get_interval = stockdata.get(item)
            interval_data = Stock(meta_stockdata.get('2. Symbol'), item, float(get_interval.get('1. open')), float(get_interval.get('4. close')), float(get_interval.get('3. low')), float(get_interval.get('2. high')), int(get_interval.get('5. volume')))
            Procstockdata.append([interval_data.open_time, interval_data.open_value, interval_data.close_value, interval_data.low, interval_data.high, interval_data.volume, interval_data.direction_increasing(), interval_data.spike()])
        print(Procstockdata)
        
#MyKey ='28M2VQTADUQ0HSCP'
#ts = TimeSeries(key=MyKey)
#stockdata, meta_stockdata = ts.get_intraday(Stock.ticker)

#Indexes = []
#Procstockdata = []
#for i in stockdata.keys():
#    Indexes.append(i)
#for item in Indexes:
#    get_interval = stockdata.get(item)
#    interval_data = Stock(meta_stockdata.get('2. Symbol'), item, float(get_interval.get('1. open')), float(get_interval.get('4. close')), float(get_interval.get('3. low')), float(get_interval.get('2. high')), int(get_interval.get('5. volume')))
#    Procstockdata.append([interval_data.open_time, interval_data.open_value, interval_data.close_value, interval_data.low, interval_data.high, interval_data.volume, interval_data.direction_increasing(), interval_data.spike()])
#print(Procstockdata)

#ts = TimeSeries(key=MyKey, output_format='pandas')
#data, meta_data = ts.get_intraday(symbol='MSFT',get_interval='1min', outputsize='full')
#data['4. close'].plot()
#plt.title('Intraday Times Series for the MSFT stock (1 min)')
#plt.show()

# str to datetime conversion. Might not be neeeded so leaving here just in case.
#interval_opentime = []
#    dateint = datetime.strptime(i, '%Y-%m-%d %X')
#    print(dateint)
#    interval_opentime.append(dateint)
#print(interval_opentime)