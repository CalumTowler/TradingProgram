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

MyKey = '28M2VQTADUQ0HSCP'
ts = TimeSeries(key=MyKey, output_format='pandas')


def day_checker():
    today = datetime.datetime.now()
    todayday = datetime.datetime.weekday(today)

    if todayday == 0:
        n = 3
        today_str = today.strftime("%Y-%m-%d")
        yesterday = today - timedelta(n)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
    else:
        n = 1
        today_str = today.strftime("%Y-%m-%d")
        yesterday = today - timedelta(n)
        yesterday_str = yesterday.strftime("%Y-%m-%d")

    return todayday, today_str, yesterday_str


class Stock:


    def __init__(self, ticker, path):
        self.ticker = ticker
        self.path = path
        # first pull of full 5 day 1min data to create primary library

    def pull_min(self):
        stockdata, meta_stockdata = ts.get_intraday(self.ticker, '1min', 'full')
        filename = str(self.ticker) + str(day_checker()[2]) + '.csv'
        filepath = str(self.path) + '\\' + str(self.ticker) + '\\' + 'min'
        stockdata.to_csv(filepath + filename)
        return

    def pull_day(self):
        Datetime = datetime.now()
        Datetime_str = Datetime.strftime("%d-%m-%Y")
        stockdata, meta_stockdata = ts.get_daily(self.ticker, 'full')
        filename = str(self.ticker) + Datetime_str + '.csv'
        filepath = str(self.path) + '\\' + str(self.ticker) + '\\' + 'day'
        stockdata.to_csv(filepath + filename)
        return



