"""
First trial of alpha vantage. (It works, were sticking with this for the moment!)

23/03/19: initial commit
25/03/19: Finally did something! Program can call intraday data for a tickr, and pull out the values. This is the
          beginning of manipulatable data.
25/03/19: Introducing Stock class. Overarching class that calls intraday data from stocks in list.
26/03/19: Removed unnecessary bracketing so extracting from Procstockdata is simpler. Added user input for data call.
27/03/19: Added functionality to write data to files to build library to train neural network.
Author: Calum Towler
"""
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

#List of Stocks. Implement later once functions work.

class Stock():
    
    def __init__(self):
        self.Stocks = {'MSFT':'Microsoft','GOOGL':'Google','NKE':'Nike'}
        self.StockIndexes = []
        for i in self.Stocks.keys():
            self.StockIndexes.append(i)

    def collect_intraday_data(self):
        MyKey ='28M2VQTADUQ0HSCP'
        ts = TimeSeries(key=MyKey)
        Procstockdata = []
#       InputTime = input("Which time interval? Options are '1min', '5min', '15min', '30min', '60min'")
#       InputLength = input("Which time interval? Options are 'compact'or'full'.")
        for i in self.StockIndexes:
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
    
    def write_stockdata_library(self):
       Datetime = datetime.now()
       Datetime_str = Datetime.strftime("%m-%d-%Y_%H-%M-%S")
       Test_Filename = 'StockData_'+str(Datetime_str)+'.txt'
       with open('C:\\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\'+Test_Filename, 'w') as f:
           for item in StockData:
               f.write("%s\n" % item)
    
Stocks = Stock()
StockData = Stocks.collect_intraday_data()
Stocks.write_stockdata_library()
#print(StockData)

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