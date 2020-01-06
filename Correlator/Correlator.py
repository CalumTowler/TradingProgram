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
import sys

path = r'C:\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\'
StockTickers = ['MSFT', 'MU', 'NEM']

def correlator():

    path = r'C:\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\'
    StockTickers = ['MSFT', 'MU', 'NEM']

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
    
    return correlation[0,1]

correlator()
