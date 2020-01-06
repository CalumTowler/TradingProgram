"""
Created on Sun Mar 31 21:53:55 2019
@author: Calum
"""
from DataFrame import Stock
import time
import glob

StockTickers = ['MU', 'MSFT', 'NEM', 'FB']#, 'FB', 'TWTR', 'NEM', 'WMT', 'XOM', 'SRCL', 'COP', 'SBUX', 'PFE', 'MSFT', 'NVDA', 'EOG', 'AES', 'PPL', 'BAC']
Lengths = []
Counter = 1

for i in StockTickers:
    Stocks = Stock(i, r'C:\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData')
    Stocks.check_dir()
    #Stocks.initial_pull()
    #Length = Stocks.length_checker()
    #Lengths.append(Length)f
    # Stocks.prilib()
    # Stocks.update_pull()
    # Stocks.update_prilib()
    # Stocks.collect_daily_data()
    #print(Lengths)
    print('Done with ' + str(i))
    print(r'Waiting...')
    #time.sleep(15)
print('Finished with stock list.')

#while Lengths[0] != Lengths[1] or Lengths[1] != Lengths[2] or Lengths[2] != Lengths[3]:
 #       Lengths = []
  #      print(Counter)
   #     for i in StockTickers:
    #        Stocks = Stock(i, r'C:\Users\Calum\Trading Program\TradingProgram\WebExtract\StockData\\')
     #       Stocks.initial_pull()
      #      Length = Stocks.length_checker()
       #     Lengths.append(Length)
         #   print('Done with ' + str(i))
        #    print(r'Waiting...')
          #  time.sleep(15)
         #   print(Lengths)
        #Counter += 1
#else:
 #   print("All datasets are equal size")

