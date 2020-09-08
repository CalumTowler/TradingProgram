
import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools
path = r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data'

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
    dfbbp1 = dfbbp[dfbbp["Value Change"] == 1]
    dfbbpup1 = dfbbp1[dfbbp1["Probability Up"] > 0.7]
    dfbbpup1 = dfbbpup1.reset_index(drop=True)

    dfbbpdown1 = dfbbp1[dfbbp1["Probability Down"] > 0.7]
    dfbbpdown1 = dfbbpdown1.reset_index(drop=True)
    print(dfbbpup1)
    print(dfbbpdown1)




    # dftickerfile = path + ticker + "short" + "60" + ".csv"
    # dfticker = pd.read_csv(dftickerfile)
    # dfticker['time'] = pd.to_datetime(dfticker['time'])
    dfticker=dffix(listdf,4,0,ticker)

    dfticker["rsigrad"] = 0

    rsigradnum = {1: 20, 2: 10, 3: 10, 4: 6, 5: 5, 6: 5}
    rsigradn = rsigradnum[4]
    for x in range(len(dfticker) - rsigradn):
        dfticker.loc[dfticker.index[x], 'rsigrad'] = (dfticker.loc[dfticker.index[x], 'RSI'] - dfticker.loc[dfticker.index[x + rsigradn], 'RSI']) / rsigradn  # rsigradient calc

    dfticker['Spread'] = dfticker["Upper"] - dfticker['Lower']
    dfticker['Spread Grad'] = 0
    dfticker['Spread Ratio'] = 0
    for x in range(len(dfticker.index) - 20):
        dfticker.loc[dfticker.index[x], 'Spread Grad'] = (fval(dfticker, 'Upper', x + 20) - fval(dfticker, 'Lower', (x + 20))) - (
                    fval(dfticker, 'Upper', x) - fval(dfticker, 'Lower', (x)))
    for x in range(len(dfticker.index)):
        cspread = fval(dfticker, 'Spread', x)
        dfticker.loc[dfticker.index[x], 'Spread Ratio'] = (cspread / (dfticker['Spread']).median())


    dfticker["timedate"]=0
    for x in range(len(dfticker)): #remove current day from experiment
        dfticker.loc[dfticker.index[x], "timedate"]=(dfticker.loc[dfticker.index[x], "time"].date())
    currentdate = dfticker.loc[dfticker.index[0],"timedate"]
    dfticker=dfticker[dfticker["timedate"]!=currentdate]
    dfticker = dfticker.reset_index(drop=True)

    n = 0
    bp=50000

    for x in reversed(range(1,200)):
        newdate=currentdate - timedelta(days=x)
        dfcurrentday = dfticker[dfticker["timedate"]==newdate]
        dfcurrentday = dfcurrentday.reset_index(drop=True)
        sellprice=0
        if len(dfcurrentday)!=0:
            for x in range(len(dfcurrentday)):
                rsi = fval(dfcurrentday, "RSI", x)
                rsigrad = float(fval(dfcurrentday, "rsigrad", x))
                spreadgrad = dfcurrentday.loc[dfcurrentday.index[x], "Spread Grad"]
                spreadratio = float(fval(dfcurrentday, "Spread Ratio", x))
                if fval(dfcurrentday, 'Upper', x) < fval(dfcurrentday, 'close', x):
                    breakbb = "breakover"
                elif fval(dfcurrentday, 'Lower', x) > fval(dfcurrentday, 'close', x):
                    breakbb = "breakunder"
                else:
                    breakbb = "within"
                if spreadgrad < 0:
                    stsq = "st"
                else:
                    stsq = "sq"
                while sellprice==0:
                    for y in range(len(dfrsipup)):
                        t = dfrsipup.loc[dfrsipup.index[y], "RSI Range"].split(maxsplit=-1)
                        z = dfrsipup.loc[dfrsipup.index[y], "RSI Gradient"].split(maxsplit=-1)
                        if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]):
                            print(dfrsipup.loc[y])
                            n=n+1

                            buyprice=(fval(dfcurrentday, 'close', x))
                            numbershares=bp/buyprice
                            for x in range((x+1),len(dfcurrentday)):
                                if fval(dfcurrentday,"high",x)> buyprice*1.01:
                                    bp=numbershares*buyprice*1.01
                                    sellprice=buyprice*1.01

                                    break
                                else:
                                    pass
                            if sellprice!=buyprice*1.01:
                                y = len(dfcurrentday) - 1
                                bp = numbershares * buyprice
                                sellprice = buyprice
                                break
                            else:
                                pass
                            break

                        else:
                            continue
                    for z in range(len(dfbbpup1)):
                        y = dfbbpup1.loc[dfbbpup1.index[z], "bbprofile"].split(maxsplit=-1)

                        if y[0]==breakbb and y[1]==stsq and float(y[2]) < spreadratio < float(y[3]):
                            print(dfbbpup1.loc[z])

                            buyprice=(fval(dfcurrentday, 'close', x))
                            numbershares = bp / buyprice

                            n = n + 1

                            for x in range((x+1),len(dfcurrentday)):
                                if fval(dfcurrentday,"high",x)> buyprice*1.01:

                                    bp = numbershares * buyprice*1.01
                                    sellprice = buyprice * 1.01

                                    break
                                else:
                                    pass
                            if sellprice!=buyprice*1.01:
                                y = len(dfcurrentday) - 1

                                bp = numbershares * buyprice
                                sellprice = buyprice

                                break
                            else:
                                pass
                            break
                        else:
                            continue
                    break

    print(n)
    print(bp)


trader(tickerlist[0])
