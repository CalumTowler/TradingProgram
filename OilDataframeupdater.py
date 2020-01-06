

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
import OilDataframe
from OilDataframe import day_checker
from OilDataframe import Stock
import threading


def day_checker():
    Today = datetime.datetime.now()
    Todayday = datetime.datetime.weekday(Today)

    if Todayday == 0:
        n = 3
        Today_str = Today.strftime("%Y-%m-%d")
        Yesterday = Today - timedelta(n)
        Yesterday_str = Yesterday.strftime("%Y-%m-%d")
    else:
        n = 1
        Today_str = Today.strftime("%Y-%m-%d")
        Yesterday = Today - timedelta(n)
        Yesterday_str = Yesterday.strftime("%Y-%m-%d")

    return Todayday, Today_str, Yesterday_str


def Oracle_Run():
    n = 1
    x = 21
    y = 28

    start_time = datetime.time(x, y, 00)
    end_time = datetime.time(x, y, 30)
    pre_time = datetime.time(x, (y - n), 20)  # time before market opens to get initial pull

    Market_Open = start_time.isoformat(timespec='seconds')
    Market_Close = end_time.isoformat(timespec='seconds')
    pre_market = pre_time.isoformat(timespec='seconds')



    while True:
        while (day_checker()[0] in range(5)):
            while ((datetime.datetime.now().time().isoformat(timespec='seconds')) > pre_market and
                   (datetime.datetime.now().time().isoformat(timespec='seconds')) < Market_Open):


                Stocks = Stock("EIA/PET_RWTC_D", 'D:\Dream\Oracle\Program\TradingProgram\WebExtract\StockData')
                Stocks.initial_pull()  # need to change M1PL variable name to a unique one for stocks
                Stocks.prilib()
                Stocks.test()
                time.sleep(40)

            while ((datetime.datetime.now().time().isoformat(timespec='seconds')) > Market_Open and
                   (datetime.datetime.now().time().isoformat(timespec='seconds')) < Market_Close):
                print('next')



        else:
            print('The Market is Closed')
            time.sleep(2)


Oracle_Run()
