


import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools
path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'

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

def topp(ticker, valuechange, indicator, direction,tp,length,type):

    excel1 = path + ticker + length + type + indicator + tp + ".csv"
    df = pd.read_csv(excel1)
    df=df[df["Value Change"]==valuechange]
    if direction=="Up":
        print(df.nlargest(4, "Probability Up"))
    elif direction=="Down":
        print(df.nlargest(4, "Probability Down"))

    return

tickerlist=["\TVC_USOIL, ","\SPCFD_S5INFT, "]
listindicator=["rsiprob","macdprob","maprob","bbprob"]
tplist=["60"]
# for x in tickerlist:
#     print(x)
#     for y in tplist:
#         print(y)
#         for z in listindicator:
#             topp(x,2,z,"Up",y,"short","Sep")
#             topp(x,2,z,"Down",y,"short","Sep")

def trader(ticker):

    rsip = path + ticker + "short" + "Sep" + "rsiprob" + "60" + ".csv"

    dfrsip = pd.read_csv(rsip)
    dfrsip=dfrsip[dfrsip["Value Change"]==1.5]
    dfrsipup = dfrsip[dfrsip["Probability Up"]>0.75]
    dfrsipdown =dfrsip[dfrsip["Probability Down"]>0.75]
    print(dfrsipup)
    print(dfrsipdown)

    bbp = path + ticker + "short" + "Sep" + "bbprob" + "60" + ".csv"

    dfbbp = pd.read_csv(bbp)
    dfbbp = dfbbp[dfbbp["Value Change"] == 1.5]
    dfbbpup = dfbbp[dfbbp["Probability Up"] > 0.75]
    dfbbpdown = dfbbp[dfbbp["Probability Down"] > 0.75]
    print(dfbbpup)
    print(dfbbpdown)

    dfticker=dffix(listdf, 4, 0, ticker)
    dfticker["timedate"]=0
    for x in range(len(dfticker)): #remove current day from experiment
        dfticker.loc[dfticker.index[x], "timedate"]=(dfticker.loc[dfticker.index[x], "time"].date())
    currentdate = dfticker.loc[dfticker.index[0],"timedate"]
    dfticker=dfticker[dfticker["timedate"]!=currentdate]
    dfticker = dfticker.reset_index(drop=True)

    newdate=currentdate - timedelta(days=6)
    print(newdate)

    dfcurrentday = dfticker[dfticker["timedate"]==newdate]
    dfcurrentday = dfcurrentday.reset_index(drop=True)
    print(dfcurrentday)
    for x in range(len(dfcurrentday)):
        rsi=dfcurrentday["RSI"]
        rsigrad=dfcurrentday["rsigrad"]
        spreadgrad = dfcurrentday['Spread Grad']
        spreadratio=dfcurrentday['Spread Ratio']


trader(tickerlist[1])

