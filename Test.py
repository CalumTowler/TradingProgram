
import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools
start_time = time.time()

#
# path = r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data\3 months prior'
# path2=r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data\current day'

path = r'D:\OneDrive\Oracle\Trading Program\Stock Data\3 months prior'
path2=r'D:\OneDrive\Oracle\Trading Program\Stock Data\current day'
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'}
tickerlist=["\TVC_USOIL, ","\SPCFD_S5INFT, "]
listindicator=["rsiprob","macdprob","maprob","bbprob"]
tplist=["60"]

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def dffix(list,x,tp,ticker):

    excel1 = path + ticker + str(list[x]) + ".csv"
    df = pd.read_csv(excel1)
    #print('Chart Interval is '+(str(list[x])))
    # puts column headers in
    df.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
                  'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
                  ,'MOMMACD','MOMSignal']
    df['time'] = pd.to_datetime(df['time'])  # changes time column format to datetime
    df = df.iloc[::-1] # revereses index
    df = df.reset_index(drop=True)  # reset so newest data is at index 0
    if tp >= 0: # if 0 is selected as start then removing rows will be skipped
        df = df.drop(df.index[:tp]) #drops range of rows not wanted to make new df starting from point selected
        df = df.reset_index(drop=True) #reset index
    else:
        pass

    return df

def fval(df,column,val):
    value = (df.loc[df.index[val], column])
    return value

df=dffix(listdf, 4, 0, tickerlist[0])

candlesticklist={"Hammer":[]}

df["Candlestick Colour"]=0

for x in range(len(df)):
    high=fval(df,"high",x)
    low=fval(df,"low",x)
    close=fval(df,"close",x)
    open=fval(df,"open",x)
    if open>close:
        df.loc[df.index[x],"Candlestick Colour"] = "Red"
    elif close>open:
        df.loc[df.index[x], "Candlestick Colour"] = "Green"
    else:
        df.loc[df.index[x], "Candlestick Colour"] = "Doji"


print(df)