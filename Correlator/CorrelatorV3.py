"""
CorrelatorV3.py

Calum
08/12/19
"""

import numpy as np
import pandas as pd
import sys

# import csv
# import datetime as dt
# from openpyxl import load_workbook

StockTickers = ['MSFT', 'MU', 'NEM']#, 'FB']

def correlator():

    path = r'C:\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\'
    i = 0
    j = 1
    c = len(StockTickers)
    NoCorrelation = {}
    PositiveCorrelation = {}
    NegativeCorrelation = {}
    
    while i < c:
        while j < c:
            Tkr1 = pd.read_csv(path + StockTickers[i] + '2019-10-25.csv')
            Tkr1_array = np.array(Tkr1)
            Tkr1_close = np.float_(Tkr1_array[:, 4])
            Tkr2 = pd.read_csv(path + StockTickers[j] + '2019-10-25.csv')
            Tkr2_array = np.array(Tkr2)
            Tkr2_close = np.float_(Tkr2_array[:, 4])
            PCorrCoef = np.corrcoef(Tkr1_close, Tkr2_close)
            Name = str(StockTickers[i]) + ' - ' + str(StockTickers[j])
            Value = str(PCorrCoef[0,1])
            print(Name + ' : ' + Value)
            if PCorrCoef[0,1] >= 0.8:
                PositiveCorrelation[Name] = PCorrCoef[0,1]
            elif PCorrCoef[0,1] <= -0.8:
                NegativeCorrelation[Name] = PCorrCoef[0,1]
            else:
                NoCorrelation[Name] = PCorrCoef[0,1]
            j += 1
        i += 1
        j = i + 1

    print('Positively Correlated Stocks: ')
    print(PositiveCorrelation)
    print('Negatively Correlated Stocks: ')
    print(NegativeCorrelation)
    print('Stocks With No Correlation: ')
    print(NoCorrelation)

correlator()