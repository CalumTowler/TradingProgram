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


MA=[25,50,100,200] 


M1PL['MA25'] = M1PL.Close.rolling(25).mean()
M1PL['MA50'] = M1PL.Close.rolling(50).mean()
M1PL['MA100'] = M1PL.Close.rolling(100).mean()
M1PL['MA200'] = M1PL.Close.rolling(200).mean()
print(M1PL)
