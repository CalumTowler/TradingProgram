"""
First trial of alpha vantage. (It works, were sticking with this for the moment!)

23/03/19: initial commit
25/03/19: Finally did something! Program can call intraday data for a tickr, and pull out the values. This is the
          beginning of manipulatable data.
25/03/19: Introducing Stock class. Overarching class that calls intraday data from stocks in list.
26/03/19: Removed unnecessary bracketing so extracting from Procstockdata is simpler. Added user input for data call.
27/03/19: Added functionality to write data to files to build library to train neural network.
30/03/19: Added plot as Stock function. Reorganised init file. Misc testing.
Author: Calum Towler
"""
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
import matplotlib.pyplot as plt
import pandas
MyKey ='28M2VQTADUQ0HSCP'
ts = TimeSeries(key=MyKey)
#List of Stocks. Implement later once functions work.

class Stock():
    
    def __init__(self):
        self.StockTickers = ['AGMpB']#'MSFT','GOOGL','NKE','DJI','NFLX', 'A', 'AA', 'AAC', 'AAN', 'AAP', 'AAT', 'AB', 'ABB', 'ABBV', 'ABC', 'ABEV']

    def collect_intraday_data(self):
        MyKey ='28M2VQTADUQ0HSCP'
        ts = TimeSeries(key=MyKey)
        Procstockdata = []
#       InputTime = input("Which time interval? Options are '1min', '5min', '15min', '30min', '60min'")
#       InputLength = input("Which time interval? Options are 'compact'or'full'.")
        for i in self.StockTickers:
            stockdata, meta_stockdata = ts.get_intraday(i,'1min','full')
            Indexes = []
            Procstockdata.append(i)
            for i in stockdata.keys():
                Indexes.append(i)
            for item in Indexes:
                get_interval = stockdata.get(item)
                interval_data = [item, float(get_interval.get('1. open')), float(get_interval.get('4. close')), float(get_interval.get('3. low')), float(get_interval.get('2. high')), int(get_interval.get('5. volume'))]
                Procstockdata.append([interval_data[0], interval_data[1], interval_data[2], interval_data[3], interval_data[4], interval_data[5]]) 
        return Procstockdata 
    
    def collect_daily_data(self):
        MyKey ='28M2VQTADUQ0HSCP'
        ts = TimeSeries(key=MyKey)
        Procstockdata = []
#       InputTime = input("Which time interval? Options are '1min', '5min', '15min', '30min', '60min'")
#       InputLength = input("Which time interval? Options are 'compact'or'full'.")
        for i in self.StockTickers:
            stockdata, meta_stockdata = ts.get_daily(i,'full')
            Indexes = []
            Procstockdata.append(i)
            for i in stockdata.keys():
                Indexes.append(i)
            for item in Indexes:
                get_interval = stockdata.get(item)
                interval_data = [item, float(get_interval.get('1. open')), float(get_interval.get('4. close')), float(get_interval.get('3. low')), float(get_interval.get('2. high')), int(get_interval.get('5. volume'))]
                Procstockdata.append([interval_data[0], interval_data[1], interval_data[2], interval_data[3], interval_data[4], interval_data[5]]) 
        return Procstockdata
    
    def write_stockdata_library(self):
       Datetime = datetime.now()
       Datetime_str = Datetime.strftime("%m-%d-%Y_%H-%M-%S")
       Test_Filename = 'StockData_'+str(Datetime_str)+'.txt'
       with open('C:\\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\'+Test_Filename, 'w') as f:
           for item in StockData:
               f.write("%s\n" % item)
               
    def plot_stockdata(self):
        for i in self.StockTickers:
            ts = TimeSeries(key=MyKey, output_format='pandas')
            data, meta_data = ts.get_intraday(i,'1min', outputsize='full')
            data['4. close'].plot()
            Title = 'Intraday Times Series for the '+str(i)+' stock (1 min)'
            plt.title(Title)
            plt.show()
            
#data, meta_data = ts.get_daily('MSFT',outputsize='full')
#Indexes = []
#Procstockdata = []
#for i in data.keys():
#    Indexes.append(i)
#    for item in Indexes:
#        get_interval = data.get(item)
#        interval_data = [item, float(get_interval.get('1. open')), float(get_interval.get('4. close')), float(get_interval.get('3. low')), float(get_interval.get('2. high')), int(get_interval.get('5. volume'))]
#        Procstockdata.append([interval_data[0], interval_data[1], interval_data[2], interval_data[3], interval_data[4], interval_data[5]])
#        print(Procstockdata)
#Test_Filename = 'MSFT_Daily_20Years.txt'
#with open('C:\\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\Daily20Year\\'+Test_Filename, 'w') as f:
#    for item in Procstockdata:
#        f.write("%s\n" % item)
    
Stocks = Stock()
StockData = Stocks.collect_intraday_data()
#print(len(StockData))
#Stocks.write_stockdata_library()
#Stocks.plot_stockdata()
#print(StockData)


#        self.Stocks = {'A':'A','MSFT':'Microsoft','GOOGL':'Google','NKE':'Nike'}
#        self.StockIndexes = []
#        for i in self.Stocks.keys():
#            self.StockIndexes.append(i)

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



# str to datetime conversion. Might not be neeeded so leaving here just in case.
#interval_opentime = []
#    dateint = datetime.strptime(i, '%Y-%m-%d %X')
#    print(dateint)
#    interval_opentime.append(dateint)
#print(interval_opentime)