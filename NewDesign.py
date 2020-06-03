"""
04/01/2020

@author: Calum
"""

from alpha_vantage.timeseries import TimeSeries
import datetime as dt
import pandas as pd
import os
import matplotlib.pyplot as plt
import time

# Variables + Dictionary Initialisation
Key = '28M2VQTADUQ0HSCP'
ts = TimeSeries(key=Key, output_format='pandas')
StockTickers = ['MSFT']#, 'MU']#, 'NEM', 'FB']  # , 'FB', 'TWTR', 'NEM', 'WMT', 'XOM', 'SRCL', 'COP', 'SBUX', 'PFE', 'MSFT',
                                            # 'NVDA', 'EOG', 'AES', 'PPL', 'BAC']
User = 'Calum'
if User == 'Calum':
    Path = r'C:\Users\Calum\Trading Program\TradingProgram\StockData'
else:
    Path = r'C:\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\StockData'
M1PrimLib = {}
M5PrimLibM = {}
M5PrimLibO = {}
M10PrimLib = {}
M15PrimLib = {}
M30PrimLib = {}
M60PrimLib = {}
Lengths = {}

# Flags
HaveData = False
CheckLength = False

# Ensure in Path
os.chdir(Path)

# Set Day - Needs Explanation
Today = dt.datetime.now()
Todayday = dt.datetime.weekday(Today)
if Todayday == 0: # Monday
    Day = 3
    Today_str = Today.strftime("%Y-%m-%d")
    Yesterday = Today - dt.timedelta(Day)
    Yesterday_str = Yesterday.strftime("%Y-%m-%d")
else:
    Day = 2
    Today_str = Today.strftime("%Y-%m-%d")
    Yesterday = Today - dt.timedelta(Day)
    Yesterday_str = Yesterday.strftime("%Y-%m-%d")

if HaveData == False and CheckLength == False:
# Ensure Directories Exist
    for ticker in StockTickers:
        if os.path.isdir(ticker) == True:
            print('Directory exists')
        else:
            print('Making Directory')
            os.mkdir(ticker)

# Call Starting Data
        stockdata, meta_stockdata = ts.get_intraday(ticker, '1min', 'full')
# Save to csv file
        Filename = str(ticker) + str(Today_str) + '.csv'
        Filepath = str(Path + '\\' + str(ticker) + '\\')
        stockdata.to_csv(Filepath + Filename)
# Set index to DateTimeIndex for re-sampling
        time_index = pd.DatetimeIndex(stockdata.index)
        stockdata_2 = stockdata.set_index(time_index)
# Save to dictionary for manipulation
        M1PrimLib[ticker] = stockdata_2

# Check Length - Hopefully can delete
        print(len(stockdata_2.index))

# Re-sample Minute data and add to other dictionaries
#         M5PrimLib[ticker] = stockdata_2.resample('5min').mean()
        M10PrimLib[ticker] = stockdata_2.resample('10min').mean()
        M15PrimLib[ticker] = stockdata_2.resample('15min').mean()
        M30PrimLib[ticker] = stockdata_2.resample('30min').mean()
        M60PrimLib[ticker] = stockdata_2.resample('60min').mean()

# Sleep to ensure no more than 5 calls in 60s
        time.sleep(12)

elif CheckLength == True:
    print('Checking stockdata lengths')
    for ticker in StockTickers:
        stockdata, meta_stockdata = ts.get_intraday(ticker, '1min', 'full')
        print(ticker + ' - ' + str(len(stockdata)))
        if len(stockdata) < 1950:
            time.sleep(12)
        while len(stockdata) < 1950:
            stockdata, meta_stockdata = ts.get_intraday(ticker, '1min', 'full')
            print(ticker + ' - ' + str(len(stockdata)))
            if len(stockdata) < 1950:
                time.sleep(12)

else:
    for ticker in StockTickers:
        Filename = str(ticker) + str(Today_str) + '.csv'
        Filepath = str(Path + '\\' + str(ticker) + '\\')
        stockdata = pd.read_csv(Filepath + Filename)
        time_index = pd.DatetimeIndex(stockdata['date'])
        stockdata_2 = stockdata.set_index(time_index)
        M1PrimLib[ticker] = stockdata_2
        M5PrimLibM[ticker] = stockdata_2.resample('5min').mean()
        M5PrimLibO[ticker] = stockdata_2['4. close'].resample('5min').ohlc()
        M10PrimLib[ticker] = stockdata_2.resample('10min').mean()
        M15PrimLib[ticker] = stockdata_2.resample('15min').mean()
        M30PrimLib[ticker] = stockdata_2.resample('30min').mean()
        M60PrimLib[ticker] = stockdata_2.resample('60min').mean()

        stockdata, meta_stockdata = ts.get_intraday(ticker, '5min', 'full')

# M1PrimLib['MSFT']['4. close'].plot()
# M5PrimLib['MSFT']['4. close'].plot()
# M10PrimLib['MSFT']['4. close'].plot()
# M15PrimLib['MSFT']['4. close'].plot()
# M30PrimLib['MSFT']['4. close'].plot()
# M60PrimLib['MSFT']['4. close'].plot()
# plt.title('Intraday MSFT')
# plt.show()

# print(M5PrimLibM['MSFT'])
# print(M5PrimLibO['MSFT'])
# print(stockdata)