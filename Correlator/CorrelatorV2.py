"""
CorrelatorV2.py

Calum
05/12/19
"""

import numpy as np
import pandas as pd
import sys

# import csv
# import datetime as dt
# from openpyxl import load_workbook

# StockTickers = ['MSFT', 'MU', 'NEM']

def correlator(*Tkrs):

    path = r'C:\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\'

    Tkr1 = pd.read_csv(path + Tkrs[0] + '2019-10-25.csv')
    Tkr1_array = np.array(Tkr1)
    Tkr1_close = np.float_(Tkr1_array[:, 4])

    Tkr2 = pd.read_csv(path + Tkrs[1] + '2019-10-25.csv')
    Tkr2_array = np.array(Tkr2)
    Tkr2_close = np.float_(Tkr2_array[:, 4])


    PCorrCoef = np.corrcoef(Tkr1_close, Tkr2_close)
    
    return PCorrCoef[0,1]