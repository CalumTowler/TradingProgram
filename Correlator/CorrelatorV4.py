"""
CorrelatorV4.py

Calum
03/01/20
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
            Tkr1_close = Tkr1['4. close']
            Tkr2 = pd.read_csv(path + StockTickers[j] + '2019-10-25.csv')
            Tkr2_close = Tkr2['4. close']
            PCorrCoef = Tkr1_close.corr(Tkr2_close)
            
            Name = str(StockTickers[i]) + ' - ' + str(StockTickers[j])
            Value = str(PCorrCoef)
            
            if PCorrCoef >= 0.8:
                PositiveCorrelation[Name] = PCorrCoef
            elif PCorrCoef <= -0.8:
                NegativeCorrelation[Name] = PCorrCoef
            else:
                NoCorrelation[Name] = PCorrCoef
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