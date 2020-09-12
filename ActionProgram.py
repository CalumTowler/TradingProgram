
import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools

start_time = time.time()

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
    values={0:[3,0.8],1:[2.5,0.8],2:[2,0.8],3:[1.5,0.8],4:[1,0.8],5:[0.5,0.5]}
    listvalrsiu=[]
    listvalrsid=[]
    listvalbbpu=[]
    listvalbbpd=[]
    listvalrsimacdpu=[]
    listvalrsimacdpd=[]
    for x in range(len(values)):
        value=values[x][0]
        pmin=values[x][1]

        dfrsip = dfrsi[dfrsi["Value Change"] == value]
        dfrsipup = dfrsip[dfrsip["Probability Up"] > pmin]
        dfrsipup = dfrsipup.reset_index(drop=True)
        listtodrop = []

        for x in range(len(dfrsipup)):
            if float(dfrsipup.loc[dfrsipup.index[x],"Probability Up"])<float(dfrsipup.loc[dfrsipup.index[x],"Probability Down"]): # removes values where probup is less than down and vice versa
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

        dfrsimacdp = dfrsimacd[dfrsimacd["Value Change"] == value]
        dfrsimacdpup = dfrsimacdp[dfrsimacdp["Probability Up"] > pmin]
        dfrsimacdpup = dfrsimacdpup.reset_index(drop=True)
        listtodrop = []

        for x in range(len(dfrsimacdpup)):
            if float(dfrsimacdpup.loc[dfrsimacdpup.index[x], "Probability Up"]) < float(dfrsimacdpup.loc[dfrsimacdpup.index[x], "Probability Down"]):  # removes values where probup is less than down and vice versa
                listtodrop.append(x)  # makes list of rows to be removed (doing it in the loop would remvoe rows breaking for loop length
            else:
                pass
        dfrsimacdpup.drop(index=listtodrop, inplace=True)  # remvoes rows
        dfrsimacdpup = dfrsimacdpup.reset_index(drop=True)

        dfrsimacdpdown = dfrsimacdp[dfrsimacdp["Probability Down"] > pmin]
        dfrsimacdpdown = dfrsimacdpdown.reset_index(drop=True)
        listtodrop = []
        for x in range(len(dfrsimacdpdown)):
            if float(dfrsimacdpdown.loc[dfrsimacdpdown.index[x], "Probability Up"]) > float(dfrsimacdpdown.loc[dfrsimacdpdown.index[x], "Probability Down"]):
                listtodrop.append(x)
            else:
                pass
        dfrsimacdpdown.drop(index=listtodrop, inplace=True)
        dfrsimacdpdown = dfrsimacdpdown.reset_index(drop=True)
        listvalrsimacdpu.append(dfrsimacdpup)
        listvalrsimacdpd.append(dfrsimacdpdown)




    # dftickerfile = path + ticker + "short" + "60" + ".csv"
    # dfticker = pd.read_csv(dftickerfile)
    # dfticker['time'] = pd.to_datetime(dfticker['time'])
    dfcsv=excel1 = path2 + ticker + "short" + "full" +str(listdf[4])+ ".csv"
    dfticker = pd.read_csv(excel1)

    dfticker['time'] = pd.to_datetime(dfticker['time'])
    dfticker["timedate"]=0
    for x in range(len(dfticker)): #remove current day from experiment
        dfticker.loc[dfticker.index[x], "timedate"]=(dfticker.loc[dfticker.index[x], "time"].date()) #makes date only column
    currentdate = dfticker.loc[dfticker.index[0],"timedate"]
    dfticker=dfticker[dfticker["timedate"]!=currentdate] #removes current day to remove incomplete days
    dfticker = dfticker.reset_index(drop=True)

    n = 0
    bp=17500
    hj=0
    g=0
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
                    probhour={0:[0.0,"up"],1:[0.0,"down"],2:[0.0,"up"],3:[0.0,"down"],4:[0.0,"up"],5:[0.0,"down"]}
                    rsi = fval(dfcurrentday, "RSI", x)
                    rsigrad = float(fval(dfcurrentday, "rsigrad", x))
                    spreadgrad = dfcurrentday.loc[dfcurrentday.index[x], "Spread Grad"]
                    spreadratio = float(fval(dfcurrentday, "Spread Ratio", x))
                    histprofile = fval(dfcurrentday, "Histogram Profile",x)
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
                            dfrsimacdup=listvalrsimacdpu[x]
                            dfrsimacddown=listvalrsimacdpd[x]

                            while sellprice==0: #once trade attempted stop pricess on current day
                                value = (values[x][0]) / 100
                                updown=0
                                for y in range(len(dfrsipup)):
                                    t = dfrsipup.loc[dfrsipup.index[y], "RSI Range"].split(maxsplit=-1)
                                    z = dfrsipup.loc[dfrsipup.index[y], "RSI Gradient"].split(maxsplit=-1)

                                    if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]): #checks if within any column on probu for rsi

                                        probhour[0][0]=dfrsipup.loc[dfrsipup.index[y], "Probability Up"]
                                        break

                                    else:
                                        pass

                                for z in range(len(dfbbpup1)):
                                    y = dfbbpup1.loc[dfbbpup1.index[z], "bbprofile"].split(maxsplit=-1)

                                    if y[0]==breakbb and y[1]==stsq and float(y[2]) < spreadratio < float(y[3]):
                                        probhour[1][0] = float(dfbbpup1.loc[dfbbpup1.index[z], "Probability Up"])
                                        break
                                    else:
                                        pass

                                for y in range(len(dfrsipdown)):
                                    t = dfrsipdown.loc[dfrsipdown.index[y], "RSI Range"].split(maxsplit=-1)
                                    z = dfrsipdown.loc[dfrsipdown.index[y], "RSI Gradient"].split(maxsplit=-1)
                                    if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]):
                                        probhour[2][0] = dfrsipdown.loc[dfrsipdown.index[y], "Probability Down"]
                                        break
                                    else:
                                        pass

                                for z in range(len(dfbbpdown1)):
                                    y = dfbbpdown1.loc[dfbbpdown1.index[z], "bbprofile"].split(maxsplit=-1)

                                    if y[0]==breakbb and y[1]==stsq and float(y[2]) < spreadratio < float(y[3]):
                                        probhour[3][0] = dfbbpdown1.loc[dfbbpdown1.index[z], "Probability Down"]
                                        break
                                    else:
                                        pass
                                for y in range(len(dfrsimacdup)):
                                    t = dfrsimacdup.loc[dfrsimacdup.index[y], "RSI Range"].split(maxsplit=-1)
                                    z = dfrsimacdup.loc[dfrsimacdup.index[y], "RSI Gradient"].split(maxsplit=-1)
                                    k =  dfrsimacdup.loc[dfrsimacdup.index[y], "MACD Profile"]
                                    if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]) and k==histprofile: #checks if within any column on probu for rsi

                                        probhour[4][0]=dfrsimacdup.loc[dfrsimacdup.index[y], "Probability Up"]
                                        break

                                    else:
                                        pass

                                for y in range(len(dfrsimacddown)):
                                    t = dfrsimacddown.loc[dfrsimacddown.index[y], "RSI Range"].split(maxsplit=-1)
                                    z = dfrsimacddown.loc[dfrsimacddown.index[y], "RSI Gradient"].split(maxsplit=-1)
                                    k = dfrsimacddown.loc[dfrsimacddown.index[y], "MACD Profile"]
                                    if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]) and k==histprofile:
                                        probhour[5][0] = float(dfrsimacddown.loc[dfrsimacddown.index[y], "Probability Down"])
                                        break
                                    else:
                                        pass
                                listprobs=[]
                                for x in range(len(probhour)):
                                    listprobs.append(probhour[x][0])
                                for x in range(len(probhour)):
                                    if max(listprobs) == 0.0:
                                        break
                                    elif max(listprobs) == probhour[x][0]:

                                        updown = probhour[x][1]
                                    else:
                                        pass

                                if updown=="up": #need to sort if equal probabilities i.e. using 4 hour probs or other indicator probs

                                    buyprice = (fval(dfcurrentday, 'close', x))
                                    numbershares = bp / buyprice
                                    n=n+1

                                    for x in range((x + 1), len(dfcurrentday)):
                                        if fval(dfcurrentday, "high", x) > buyprice * (1 + value):
                                            bp = numbershares * buyprice * (1 + 2 * value)
                                            targethit = targethit + 1
                                            sellprice = buyprice * (1 + 2 * value)  # 2 x value to simulate etf
                                            break
                                        else:
                                            pass
                                    if sellprice != buyprice * (1 + 2 * value):
                                        bp = numbershares * buyprice*0.995
                                        sellprice = buyprice*0.995  # need to improve but for now assumes if cant find aimed sell price then sells at bought price
                                        break
                                    else:
                                        pass
                                    break
                                elif updown=="down":
                                    buyprice = (fval(dfcurrentday, 'close', x))
                                    numbershares = bp / buyprice
                                    n=n+1

                                    for x in range((x + 1), len(dfcurrentday)):
                                        if fval(dfcurrentday, "low", x) < buyprice * (1 - value):
                                            bp = numbershares * buyprice * (1 + 2 * value)
                                            targethit = targethit + 1
                                            sellprice = buyprice * (1 + 2 * value)

                                            break
                                        else:
                                            pass
                                    if sellprice != buyprice * ((1 + 2 * value)):
                                        bp = numbershares * buyprice*0.995
                                        sellprice = buyprice*0.995
                                        break
                                    else:
                                        pass
                                    break
                                elif updown == 0:
                                    pass
                                else:
                                    buyprice = (fval(dfcurrentday, 'close', x))
                                    numbershares = bp / buyprice
                                    n = n + 1
                                    g=g+1

                                    for x in range((x + 1), len(dfcurrentday)):
                                        if fval(dfcurrentday, "low", x) < buyprice * (1 - value):
                                            bp = numbershares * buyprice * (1 + 2 * value)
                                            targethit = targethit + 1
                                            sellprice = buyprice * (1 + 2 * value)

                                            break
                                        else:
                                            pass
                                    if sellprice != buyprice * ((1 + 2 * value)):
                                        bp = numbershares * buyprice
                                        sellprice = buyprice
                                        break
                                    else:
                                        pass
                                    break
                                break

                        break

                break
            else:
                weekends=weekends+1
                sellprice=1
                pass

        continue


    print(g)
    print("Number of attempted trades: "+str(n))
    print("Buying Power: "+str(bp))
    print("Total trading days: " +str(hj-weekends))
    print("Targets Hit: "+str(targethit))
    print("Days Traded:" + str(100*(n/(hj-weekends))) + "%")
    print("Target Hit Rate: " + str(100*(targethit/n))+ "%")
trader(tickerlist[0])

print("--- %s seconds ---" % (time.time() - start_time))
