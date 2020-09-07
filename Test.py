


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

def fval(df,column,val):
    value = (df.loc[df.index[val], column])
    return value


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
    dfrsip=dfrsip[dfrsip["Value Change"]==1]
    dfrsipup = dfrsip[dfrsip["Probability Up"]>0.7]
    dfrsipup = dfrsipup.reset_index(drop=True)

    dfrsipdown =dfrsip[dfrsip["Probability Down"]>0.7]
    dfrsipdown = dfrsipdown.reset_index(drop=True)

    print(dfrsipup)
    print(dfrsipdown)

    bbp = path + ticker + "short" + "Sep" + "bbprob" + "60" + ".csv"

    dfbbp = pd.read_csv(bbp)
    dfbbp = dfbbp[dfbbp["Value Change"] == 1]
    dfbbpup = dfbbp[dfbbp["Probability Up"] > 0.75]
    dfbbpup = dfbbpup.reset_index(drop=True)

    dfbbpdown = dfbbp[dfbbp["Probability Down"] > 0.75]
    dfbbpdown = dfbbpdown.reset_index(drop=True)

    print(dfbbpup)
    print(dfbbpdown)

    dftickerfile = path + ticker + "short" + "60" + ".csv"
    dfticker = pd.read_csv(dftickerfile)
    dfticker['time'] = pd.to_datetime(dfticker['time'])
    dfticker["timedate"]=0
    print(dfticker)
    for x in range(len(dfticker)): #remove current day from experiment
        dfticker.loc[dfticker.index[x], "timedate"]=(dfticker.loc[dfticker.index[x], "time"].date())
    currentdate = dfticker.loc[dfticker.index[0],"timedate"]
    dfticker=dfticker[dfticker["timedate"]!=currentdate]
    dfticker = dfticker.reset_index(drop=True)


    for x in reversed(range(1,50)):
        newdate=currentdate - timedelta(days=x)
        dfcurrentday = dfticker[dfticker["timedate"]==newdate]
        if len(dfcurrentday)!=0:
            dfcurrentday = dfcurrentday.reset_index(drop=True)
            for x in range(len(dfcurrentday)):
                rsi=dfcurrentday.loc[dfcurrentday.index[x], "RSI"]
                rsigrad=dfcurrentday.loc[dfcurrentday.index[x], "rsigrad"]
                spreadgrad = dfcurrentday.loc[dfcurrentday.index[x], "Spread Grad"]
                spreadratio=dfcurrentday.loc[dfcurrentday.index[x], "Spread Ratio"]
                if fval(dfcurrentday, 'Upper', x) < fval(dfcurrentday, 'close', x):
                    breakbb = "breakover"
                elif fval(dfcurrentday, 'Lower', x) > fval(dfcurrentday, 'close', x):
                    breakbb = "breakunder"
                else:
                    breakbb = "within"
                if spreadgrad<0:
                    stsq = "st"
                else:
                    stsq = "sq"
                for y in range(len(dfrsipup)):
                    y = dfrsipup.loc[dfrsipup.index[y], "RSI Range"].split(maxsplit=-1)
                    z = dfrsipup.loc[dfrsipup.index[y], "RSI Gradient"].split(maxsplit=-1)
                    if float(y[0]) < rsi < float(y[1]) and float(z[0]) < rsigrad < float(z[1]):
                        print(dfrsipup.loc[y])
                        print(fval(dfcurrentday, 'close', x))
                    else:
                        print("nope")
                for z in range(len(dfbbpup)):
                    y = dfbbpup.loc[dfbbpup.index[z], "bbprofile"].split(maxsplit=-1)
                    if y[0]==breakbb and y[1]==stsq and float(y[2]) < spreadratio < float(y[3]):
                        print(dfbbpup.loc[z])
                        print(fval(dfcurrentday, 'close', x))
                    else:
                        print("nope")



        else:
            continue
    print(dfcurrentday)
    for x in range(len(dfcurrentday)):
        rsi=dfcurrentday["RSI"]
        rsigrad=dfcurrentday["rsigrad"]
        spreadgrad = dfcurrentday['Spread Grad']
        spreadratio=dfcurrentday['Spread Ratio']

    bp=50000

    for x in range(len(dfrsipup)):
        y = dfrsipup.loc[dfrsipup.index[x], "RSI Range"].split(maxsplit=-1)
        z = dfrsipup.loc[dfrsipup.index[x], "RSI Gradient"].split(maxsplit=-1)
        if float(y[0]) < rsi < float(y[1]) and float(z[0]) < rsigrad < float(z[1]):
            print(rsip.loc[x])


        else:
            pass

trader(tickerlist[1])

