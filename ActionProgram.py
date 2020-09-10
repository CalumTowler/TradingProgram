
import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools
path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data\3 months prior'
path2=r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data\current day'
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

    rsip = path + ticker + "short" + "Sep" + "rsip" + "60" + ".csv"
    bbp = path + ticker + "short" + "Sep" + "bbp" + "60" + ".csv"
    maratio = path + ticker + "short" + "Sep" + "maratiop" + "60" + ".csv"
    rsimacd = path + ticker + "short" + "Sep" + "rsimacdp" + "60" + ".csv"
    dfrsi = pd.read_csv(rsip)
    dfbb = pd.read_csv(bbp)
    dfrsimacd=pd.read_csv(rsimacd)
    values={0:[3,0.4],1:[2.5,0.4],2:[2,0.4],3:[1.5,0.4],4:[1,0.4]}#,5:[0.5,0.7]}
    listvalrsiu=[]
    listvalrsid=[]
    listvalbbpu=[]
    listvalbbpd=[]
    listvalrsimacdu=[]
    listvalrsimacdd=[]
    for x in range(len(values)):
        value=values[x][0]
        pmin=values[x][1]

        dfrsip = dfrsi[dfrsi["Value Change"] == value]
        dfrsipup = dfrsip[dfrsip["Probability Up"] > pmin]
        dfrsipup = dfrsipup.reset_index(drop=True)
        listtodrop = []

        for x in range(len(dfrsipup)):
            if float(dfrsipup.loc[dfrsipup.index[x],"Probability Up"])<float(dfrsipup.loc[dfrsipup.index[x],"Probability Down"]+0.1): # removes values where probup is less than down and vice versa
                listtodrop.append(x) #makes list of rows to be removed (doing it in the loop would remvoe rows breaking for loop length
            else:
                pass
        dfrsipup.drop(index=listtodrop, inplace=True) #remvoes rows
        dfrsipup = dfrsipup.reset_index(drop=True)

        dfrsipdown = dfrsip[dfrsip["Probability Down"] > pmin]
        dfrsipdown = dfrsipdown.reset_index(drop=True)
        listtodrop = []
        for x in range(len(dfrsipdown)):
            if float(dfrsipdown.loc[dfrsipdown.index[x],"Probability Up"])>float(dfrsipdown.loc[dfrsipdown.index[x],"Probability Down"]):
                listtodrop.append(x)
            else:
                pass
        dfrsipdown.drop(index=listtodrop, inplace=True)
        dfrsipdown = dfrsipdown.reset_index(drop=True)
        listvalrsiu.append(dfrsipup)
        listvalrsid.append(dfrsipdown)

        dfbbp = dfbb[dfbb["Value Change"] == value]
        dfbbpup1 = dfbbp[dfbbp["Probability Up"] > pmin]
        dfbbpup1 = dfbbpup1.reset_index(drop=True)
        listtodrop = []

        for x in range(len(dfbbpup1)):
            if float(dfbbpup1.loc[dfbbpup1.index[x], "Probability Up"]) < float(dfbbpup1.loc[dfbbpup1.index[x], "Probability Down"]):
                listtodrop.append(x)
            else:
                pass
        dfbbpup1.drop(index=listtodrop, inplace=True)
        dfbbpup1 = dfbbpup1.reset_index(drop=True)

        dfbbpdown1 = dfbbp[dfbbp["Probability Down"] > pmin]
        dfbbpdown1 = dfbbpdown1.reset_index(drop=True)
        listtodrop = []

        for x in range(len(dfbbpdown1)):
            if float(dfbbpdown1.loc[dfbbpdown1.index[x], "Probability Up"]) > float(dfbbpdown1.loc[dfbbpdown1.index[x], "Probability Down"]):
                listtodrop.append(x)
            else:
                pass
        dfbbpdown1.drop(index=listtodrop, inplace=True)
        dfbbpdown1 = dfbbpdown1.reset_index(drop=True)
        listvalbbpu.append(dfbbpup1)
        listvalbbpd.append(dfbbpdown1)






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
        dfticker.loc[dfticker.index[x], "timedate"]=(dfticker.loc[dfticker.index[x], "time"].date()) #makes date only column
    currentdate = dfticker.loc[dfticker.index[0],"timedate"]
    dfticker=dfticker[dfticker["timedate"]!=currentdate] #removes current day to remove incomplete days
    dfticker = dfticker.reset_index(drop=True)

    n = 0
    bp=17500
    hj=0
    weekends=0
    targethit=0
    for x in reversed(range(1,90)):
        newdate=currentdate - timedelta(days=x) #makes current date going back x number days
        dfcurrentday = dfticker[dfticker["timedate"]==newdate] #makes dataframe of current day
        dfcurrentday = dfcurrentday.iloc[::-1] #so that time moves forward with index value
        dfcurrentday = dfcurrentday.reset_index(drop=True)

        dfcurrentday = dfcurrentday[dfcurrentday.index>8] # removes morning trade where trading on us market not availble
        dfcurrentday = dfcurrentday.reset_index(drop=True)


        hj=hj+1
        sellprice=0
        while sellprice == 0:
            if len(dfcurrentday)>5:
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
                        for x in range(len(listvalrsiu)):
                            dfrsipup=listvalrsiu[x]
                            dfrsipdown=listvalrsid[x]
                            dfbbpup1=listvalbbpu[x]
                            dfbbpdown1=listvalbbpd[x]
                            while sellprice==0: #once trade attempted stop pricess on current day
                                value = (values[x][0]) / 100

                                for y in range(len(dfrsipup)):
                                    t = dfrsipup.loc[dfrsipup.index[y], "RSI Range"].split(maxsplit=-1)
                                    z = dfrsipup.loc[dfrsipup.index[y], "RSI Gradient"].split(maxsplit=-1)

                                    if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]): #checks if within any column on probu for rsi
                                        n=n+1
                                        buyprice=(fval(dfcurrentday, 'close', x))
                                        numbershares=bp/buyprice
                                        for x in range((x+1),len(dfcurrentday)):
                                            if fval(dfcurrentday,"high",x)> buyprice*(1+value):
                                                bp=numbershares*buyprice*(1+2*value)
                                                targethit=targethit+1
                                                sellprice=buyprice*(1+2*value) #2 x value to simulate etf
                                                break
                                            else:
                                                pass
                                        if sellprice!=buyprice*(1+2*value):
                                            bp = numbershares * buyprice
                                            sellprice = buyprice #need to improve but for now assumes if cant find aimed sell price then sells at bought price
                                            break
                                        else:
                                            pass
                                        break

                                    else:
                                        pass
                                break

                            while sellprice == 0:
                                value = (values[x][0]) / 100
                                for z in range(len(dfbbpup1)):
                                    y = dfbbpup1.loc[dfbbpup1.index[z], "bbprofile"].split(maxsplit=-1)

                                    if y[0]==breakbb and y[1]==stsq and float(y[2]) < spreadratio < float(y[3]):

                                        buyprice=(fval(dfcurrentday, 'close', x))
                                        numbershares = bp / buyprice

                                        n = n + 1

                                        for x in range((x+1),len(dfcurrentday)):
                                            if fval(dfcurrentday,"high",x)> buyprice*(1+value):
                                                targethit = targethit + 1
                                                bp = numbershares * (buyprice*(1+2*value))
                                                sellprice = buyprice * (1+2*value)

                                                break
                                            else:
                                                pass
                                        if sellprice!=buyprice*((1+2*value)):

                                            bp = numbershares * buyprice
                                            sellprice = buyprice

                                            break
                                        else:
                                            pass
                                        break
                                    else:
                                        pass
                                break
                            while sellprice == 0:
                                value = (values[x][0]) / 100

                                for y in range(len(dfrsipdown)):

                                    t = dfrsipdown.loc[dfrsipdown.index[y], "RSI Range"].split(maxsplit=-1)
                                    z = dfrsipdown.loc[dfrsipdown.index[y], "RSI Gradient"].split(maxsplit=-1)
                                    if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]):
                                        n = n + 1

                                        buyprice = (fval(dfcurrentday, 'close', x))
                                        numbershares = bp / buyprice
                                        for x in range((x + 1), len(dfcurrentday)):
                                            if fval(dfcurrentday, "low", x) < buyprice * (1-value):
                                                bp = numbershares * buyprice * (1+2*value)
                                                targethit = targethit + 1
                                                sellprice = buyprice * (1+2*value)

                                                break
                                            else:
                                                pass
                                        if sellprice != buyprice * ((1+2*value)):
                                            bp = numbershares * buyprice
                                            sellprice = buyprice
                                            break
                                        else:
                                            pass
                                        break

                                    else:
                                        pass
                                break
                            while sellprice == 0:
                                value = (values[x][0]) / 100

                                for z in range(len(dfbbpdown1)):

                                    y = dfbbpdown1.loc[dfbbpdown1.index[z], "bbprofile"].split(maxsplit=-1)

                                    if y[0]==breakbb and y[1]==stsq and float(y[2]) < spreadratio < float(y[3]):

                                        buyprice=(fval(dfcurrentday, 'close', x))
                                        numbershares = bp / buyprice

                                        n = n + 1

                                        for x in range((x+1),len(dfcurrentday)):
                                            if fval(dfcurrentday,"low",x)< buyprice * (1-value):
                                                targethit = targethit + 1
                                                bp = numbershares * buyprice*(1+2*value)
                                                sellprice = buyprice * (1+2*value)

                                                break
                                            else:
                                                pass
                                        if sellprice!=buyprice*((1+2*value)):

                                            bp = numbershares * buyprice
                                            sellprice = buyprice

                                            break
                                        else:
                                            pass
                                        break
                                    else:
                                        pass
                                break

                        break

                break
            else:
                weekends=weekends+1
                sellprice=1
                pass

        continue



    print("Number of attempted trades: "+str(n))
    print("Buying Power: "+str(bp))
    print("Total trading days: " +str(hj-weekends))
    print("Targets Hit: "+str(targethit))
    print("Days Traded:" + str(100*(n/(hj-weekends))) + "%")
    print("Target Hit Rate: " + str(100*(targethit/n))+ "%")
trader(tickerlist[0])
