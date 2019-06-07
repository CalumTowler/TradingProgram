from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import datetime
import sched
import schedule
from datetime import timedelta
import time
import Dataframe
from LearningData import day_checker
from LearningData import Stock
import threading
import timeit


def timing():

    n = 1
    x = 1
    y = 45

    start_time = datetime.time(x, y, 00)
    end_time = datetime.time(x, y+10, 30)
    pre_time = datetime.time(x, (y - n), 30)  # time before market opens to get initial pull

    market_open = start_time.isoformat(timespec='seconds')
    market_close = end_time.isoformat(timespec='seconds')
    pre_market = pre_time.isoformat(timespec='seconds')

    market_open1 = datetime.datetime.combine(datetime.date.today(), start_time)
    sleep = market_open1 - (datetime.datetime.now())
    sleep = sleep.total_seconds()
    time_now = (datetime.datetime.now().time().isoformat(timespec='seconds'))
    return pre_market, market_open, market_close, sleep, time_now

def Oracle_Run():

    # creating names of unique dataframe names
    stock_ticker1 = ['NVDA', 'AMD', 'MSFT', 'AMZN', 'AAPL', 'GOOGL', 'GOOG', 'FB', 'CSCO', 'INTC', 'CMCSA',
                    'PEP', 'NFLX', 'ADBE', 'PYPL', 'COST', 'AMGN', 'AVGO', 'TXN', 'SBUX', 'NVDA', 'CHTR',
                    'GILD', 'QCOM', 'BKNG']

    while True:
        while (day_checker()[0] in range(5)):
          while (timing()[0]<timing()[4]<timing()[1]):



              for i in stock_ticker1:
                  Stocks = Stock(i,'D:\Dream\Oracle\Program\TradingProgram\WebExtract\StockData')
                  Stocks.initial_pull()#need to change M1PL variable name to a unique one for stocks
                  time.sleep(12)