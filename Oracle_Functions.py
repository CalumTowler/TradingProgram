from alpha_vantage.timeseries import TimeSeries
import datetime as dt
import pandas as pd
import os
import matplotlib.pyplot as plt
import time

class Oracle_Functions:

    def __init__(self, ticker_list = ['MSFT'], key = '28M2VQTADUQ0HSCP', repository_path = r'C:\Users\Calum\Trading Program\TradingProgram\StockData'):
        self.ticker_list = ticker_list
        self.key = key
        self.repository_path = repository_path

        self.M1PrimLib = {}
        self.M5PrimLib = {}
        self.M10PrimLib = {}
        self.M15PrimLib = {}
        self.M30PrimLib = {}
        self.M60PrimLib = {}
        self.Lengths = {}

        os.chdir(self.repository_path)

    def check_day(self):
        Today = dt.datetime.now()
        Todayday = dt.datetime.weekday(Today)
        if Todayday == 0:  # Monday
            Day = 3
            self.today_str = Today.strftime("%Y-%m-%d")
            yesterday = Today - dt.timedelta(Day)
            self.yesterday_str = yesterday.strftime("%Y-%m-%d")
        else:
            Day = 2
            self.today_str = Today.strftime("%Y-%m-%d")
            Yesterday = Today - dt.timedelta(Day)
            self.yesterday_str = Yesterday.strftime("%Y-%m-%d")

        return self.today_str, self.yesterday_str

    def check_dirs(self):
        for ticker in self.ticker_list:
            if os.path.isdir(ticker) == True:
                print('Directory exists')
            else:
                print('Making Directory')
                os.mkdir(ticker)

    def call_data(self):
        ts = TimeSeries(key=self.key, output_format='pandas')
        for ticker in self.ticker_list:
            # Call Starting Data
            stockdata, meta_stockdata = ts.get_intraday(ticker, '1min', 'full')
            # Save to csv file
            filename = str(ticker) + str(self.today_str) + '.csv'
            filepath = str(self.repository_path + '\\' + str(ticker) + '\\')
            stockdata.to_csv(filepath + filename)
            # Set index to DateTimeIndex for re-sampling
            time_index = pd.DatetimeIndex(stockdata.index)
            stockdata_2 = stockdata.set_index(time_index)
            # Save to dictionary for manipulation
            self.M1PrimLib[ticker] = stockdata_2
            time.sleep(12)

        return self.M1PrimLib

    def resample_primary_libraries(self):
        for ticker in self.ticker_list:
            # Re-sample Minute data and add to other dictionaries
            self.M5PrimLib[ticker] = self.M1PrimLib[ticker].resample('5min').mean()
            self.M10PrimLib[ticker] = self.M1PrimLib[ticker].resample('10min').mean()
            self.M15PrimLib[ticker] = self.M1PrimLib[ticker].resample('15min').mean()
            self.M30PrimLib[ticker] = self.M1PrimLib[ticker].resample('30min').mean()
            self.M60PrimLib[ticker] = self.M1PrimLib[ticker].resample('60min').mean()

        return self.M5PrimLib, self.M10PrimLib, self.M15PrimLib, self.M30PrimLib, self.M60PrimLib

    def plot_primary_libraries(self, ticker):
        self.M1PrimLib[ticker]['4. close'].plot()
        self.M5PrimLib[ticker]['4. close'].plot()
        self.M10PrimLib[ticker]['4. close'].plot()
        self.M15PrimLib[ticker]['4. close'].plot()
        self.M30PrimLib[ticker]['4. close'].plot()
        self.M60PrimLib[ticker]['4. close'].plot()
        plt.title('Intraday ' + str(ticker))
        plt.show()