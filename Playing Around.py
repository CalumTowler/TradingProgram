"""
Testing out Classes

24/03/19: initial commit
Author: Calum Towler
"""

from Dataframe import Stock

global M1PL

Stocks = Stock('SPX', 'C:\\Users\Alex\Documents\Stocks\Oracle\Program\TradingProgram\WebExtract\StockData\\')
#Stocks.initial_pull()
M1PL=Stocks.prilib()



M1PL.columns =['Open', 'High', 'Low', 'Close', 'Volume']
M1PL=M1PL.sort_values(by='date',ascending=True)
print(M1PL)


M1PL['MA'] = M1PL.Close.rolling(25).mean()
print(M1PL)
