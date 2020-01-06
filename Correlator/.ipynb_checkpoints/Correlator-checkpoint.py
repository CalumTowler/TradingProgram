"""
Correlator.py

Calum
26/10/19 1800
"""

import numpy as np
import pandas as pd
from openpyxl import load_workbook
import csv
import datetime as dt

path = r'C:\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\'
StockTickers = ['MSFT', 'MU', 'NEM']
counter1 = 0
counter2 = 0

def correlator():

    path = r'C:\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\'
    StockTickers = ['MSFT', 'MU', 'NEM']
    # counter1 = 0
    # counter2 = 0

    # for counter1 in StockTickers:
    #     data = pd.read_csv(path + counter1 + '2019-10-25.csv')
    #     counter1_array = np.array(data)
    #     counter1_date_close = np.column_stack((counter1_array[:, 0], counter1_array[:, 4]))
    #     # while counter2 < len(counter1_close):
    #     #     print(counter1_close[counter2])
    #     #     counter2 += 1

    msft = pd.read_csv(path + StockTickers[0] + '2019-10-25.csv')
    msft_array = np.array(msft)
    msft_close = np.float_(msft_array[:, 4])
    # print(len(msft_close))
    # print(msft)

    mu = pd.read_csv(path + StockTickers[1] + '2019-10-25.csv')
    mu_array = np.array(mu)
    mu_close = np.float_(mu_array[:, 4])
    # print(len(mu_close))
    # print(mu_close)
    # print(mu)

    nem = pd.read_csv(path + StockTickers[2] + '2019-10-25.csv')
    nem_array = np.array(nem)
    nem_close = np.float_(nem_array[:, 4])
    # print(len(nem_close))

    correlation = np.corrcoef(msft_close, mu_close)
    # correlation2 = np.corrcoef(msft_close, nem_close)
    # correlation3 = np.corrcoef(mu_close, nem_close)
    #
    print(correlation)
    # print(correlation2)
    # print(correlation3)

    #from alpha_vantage.foreignexchange import ForeignExchange
    #from pprint import pprint
    #cc = ForeignExchange(key='28M2VQTADUQ0HSCP',output_format='pandas')
    ## There is no metadata in this call
    #data, _ = cc.get_currency_exchange_intraday(from_symbol='XAU', to_symbol='USD', interval='1min', outputsize='full')
    #pprint(data)
    
    return correlation

#correlator()
