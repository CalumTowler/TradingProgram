

import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta
from statistics import mean

import time
import math
import itertools
start_time = time.time()

#
# path = r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data\3 months prior'
# path2=r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data\current day'

path = r'D:\OneDrive\Oracle\Trading Program\Stock Data\6 months prior'
path2=r'D:\OneDrive\Oracle\Trading Program\Stock Data\current day'
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'}
tickerlist=["\TVC_USOIL, ","\SPCFD_S5INFT, "]


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def fval(df,column,val):
    value = (df.loc[df.index[val], column])
    return value


def dffix(list,x,tp,ticker):

    excel1 = path2 + ticker + str(list[x]) + ".csv"
    df = pd.read_csv(excel1)
    #print('Chart Interval is '+(str(list[x])))
    # puts column headers in
    df.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
                  'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
                  ,'MOMMACD','MOMSignal']
    df['time'] = pd.to_datetime(df['time'])  # changes time column format to datetime
    df = df.iloc[::-1]# revereses index
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






values=[3,2.5,2,1.5,1.25,1,0.75,0.5]

for x in range(2,6):
    chartinterval=x
    listcsvpull = ["rsip", "bbp", "rsimacdp", "maratiop", "marsip"]
    dfindicators = []
    for x in listcsvpull:
        pcsv = path + tickerlist[0] + "short" + "Sep" + x + str(listdf[chartinterval]) + ".csv"
        dfp = pd.read_csv(pcsv)
        dfindicators.append(dfp)

    dfrsi = dfindicators[0]
    dfbb = dfindicators[1]
    dfrsimacd = dfindicators[2]
    dfmaratio = dfindicators[3]
    dfmarsi = dfindicators[4]
    inds = {0: [dfrsi, "rsip"], 1: [dfbb, "bbp"], 2: [dfrsimacd, "rsimacdp"], 3: [dfmaratio, "maratiop"],
            4: [dfmarsi, "marsip"]}

    for x in range(len(inds)):
        inddf = inds[x][0]
        ind=x
        indvalues=[]

        for y in values:


            inddf1 = inddf[inddf["Value Change"]==y]
            inddf1= inddf1[inddf1["Probability Up"]!=0]
            inddf1 = inddf1[inddf1["Probability Down"] != 0]
            nvalue=inddf1["Nvalue"]
            probu=inddf1["Probability Up"]
            probd = inddf1["Probability Down"]
            inddf1["Enough Values"] = 0
            inddf1["Good Probability Up"] = 0
            inddf1["Good Probability Down"] = 0
            if y==1.5 or 1.25 or 1 or 0.75 or 0.5:
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Enough Values"]=inddf1.loc[inddf1.index[x],"Nvalue"]>=10
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Up"]=inddf1.loc[inddf1.index[x],"Probability Up"]>=(probu.median())
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Down"]=inddf1.loc[inddf1.index[x],"Probability Down"]>=(probd.median())
            elif y==3 or 2.5 or 2:
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Enough Values"]=inddf1.loc[inddf1.index[x],"Nvalue"]>=10
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Up"]=inddf1.loc[inddf1.index[x],"Probability Up"]>=(probu.median()) and inddf1.loc[inddf1.index[x],"Probability Up"]>=inddf1.loc[inddf1.index[x],"Probability Down"]
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Down"]=inddf1.loc[inddf1.index[x],"Probability Down"]>=(probd.median()) and inddf1.loc[inddf1.index[x],"Probability Down"]>=inddf1.loc[inddf1.index[x],"Probability Up"]
            else:
                pass



            indvalues.append(inddf1)

            if y==0.5:
                df1 = pd.concat(indvalues)
                df1.to_csv(path + tickerlist[0] + "short" + inds[ind][1] + str(listdf[chartinterval]) + ".csv",index=False)
            else:
                pass


