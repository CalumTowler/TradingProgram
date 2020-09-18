

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

values4hr = {0: [3, 0.1], 1: [2.5, 0.1], 2: [2, 0.2], 3: [1.5, 0.3], 4: [1, 0.5], 5: [0.5, 0.7]}
values1hr = {0: [3, 0.1], 1: [2.5, 0.3], 2: [2, 0.5], 3: [1.5, 0.5], 4: [1, 0.75], 5: [0.5, 0.75]}
values15m = {0: [3, 0.1], 1: [2.5, 0.2], 2: [2, 0.4], 3: [1.5, 0.4], 4: [1, 0.5], 5: [0.5, 0.75]}


def probresults(ticker,chartinterval):
    if chartinterval==5:
        values=values4hr
    elif chartinterval==4:
        values=values1hr
    elif chartinterval==3:
        values=values15m
    else:
        pass



    listcsvpull=["rsip","bbp","rsimacdp","maratiop","marsip"]
    dfindicators=[]
    for x in listcsvpull:
        pcsv=path + ticker + "short" + "Sep" + x + str(listdf[chartinterval]) + ".csv"
        dfp=pd.read_csv(pcsv)
        dfindicators.append(dfp)


    dfrsi = dfindicators[0]
    dfbb = dfindicators[1]
    dfrsimacd = dfindicators[2]
    dfmaratio = dfindicators[3]
    dfmarsi = dfindicators[4]



    listvalind = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [],7:[],8:[],9:[],10:[]}

    inds = {1: dfrsi, 2: dfbb, 3: dfrsimacd,4:dfmaratio,5:dfmarsi}


    for x in range(1, len(inds) + 1):
        inddf = inds[x]

        for y in range(0, len(values), 2):
            value1 = values[y][0]
            pmin1 = values[y][1]
            inddf1 = inddf[inddf["Value Change"]==value1]
            inddf1up = inddf1[inddf1["Probability Up"] > pmin1]
            inddf1up = inddf1up.reset_index(drop=True)



            inddf1down = inddf1[inddf1["Probability Down"] > pmin1]
            inddf1down = inddf1down.reset_index(drop=True)


            listvalind[2 * x - 1].append(inddf1up)
            listvalind[2 * x].append(inddf1down)

            value2 = values[y+1][0]
            pmin2 = values[y+1][1]
            inddf2 = inddf[inddf["Value Change"] == value2]
            inddf2up = inddf2[inddf2["Probability Up"] > pmin2]
            inddf2up = inddf2up.reset_index(drop=True)



            inddf2down = inddf2[inddf2["Probability Down"] > pmin2]
            inddf2down = inddf2down.reset_index(drop=True)


            listvalind[2 * x - 1].append(inddf2up)
            listvalind[2 * x].append(inddf2down)

    listvalrsiu = listvalind[1]
    listvalrsid = listvalind[2]
    listvalbbpu = listvalind[3]
    listvalbbpd = listvalind[4]
    listvalrsimacdpu = listvalind[5]
    listvalrsimacdpd = listvalind[6]
    listvalmaratiopu = listvalind[7]
    listvalmaratiopd = listvalind[8]
    listvalmarsipu = listvalind[9]
    listvalmarsipd = listvalind[10]

    return listvalrsiu,listvalrsid,listvalbbpu,listvalbbpd,listvalrsimacdpu,listvalrsimacdpd,listvalmaratiopu,listvalmaratiopd,listvalmarsipu, listvalmarsipd


#probability and df maker

listallindval15m = probresults(tickerlist[0], 3)
listallindval4hr = probresults(tickerlist[0], 5)
listallindval1hr = probresults(tickerlist[0], 4)

excel1hr = path2 + tickerlist[0] + "short" + "full" + str(listdf[4]) + ".csv" #need to make into fucntion and for loop to make dfs
dfticker1hr = pd.read_csv(excel1hr)
dfticker1hr['time'] = pd.to_datetime(dfticker1hr['time'])
dfticker1hr["timedate"] = 0
for x in range(len(dfticker1hr)):  # remove current day from experiment
    dfticker1hr.loc[dfticker1hr.index[x], "timedate"] = (dfticker1hr.loc[dfticker1hr.index[x], "time"].date())  # makes date only column
currentdate = dfticker1hr.loc[dfticker1hr.index[0], "timedate"]
dfticker1hr = dfticker1hr[dfticker1hr["timedate"] != currentdate]  # removes current day to remove incomplete days
dfticker1hr = dfticker1hr.reset_index(drop=True)


excel4hr = path2 + tickerlist[0] + "short" + "full" + str(listdf[5]) + ".csv"
dfticker4hr = pd.read_csv(excel4hr)
dfticker4hr['time'] = pd.to_datetime(dfticker4hr['time'])
dfticker4hr["timedate"] = 0
for x in range(len(dfticker4hr)):  # remove current day from experiment
    dfticker4hr.loc[dfticker4hr.index[x], "timedate"] = (dfticker4hr.loc[dfticker4hr.index[x], "time"].date())  # makes date only column
currentdate = dfticker4hr.loc[dfticker4hr.index[0], "timedate"]
dfticker4hr = dfticker4hr[dfticker4hr["timedate"] != currentdate]  # removes current day to remove incomplete days
dfticker4hr = dfticker4hr.reset_index(drop=True)

excel15min = path2 + tickerlist[0] + "short" + "full" + str(listdf[3]) + ".csv"
dfticker15m = pd.read_csv(excel15min)
dfticker15m['time'] = pd.to_datetime(dfticker15m['time'])
dfticker15m["timedate"] = 0
for x in range(len(dfticker15m)):  # remove current day from experiment
    dfticker15m.loc[dfticker15m.index[x], "timedate"] = (dfticker15m.loc[dfticker15m.index[x], "time"].date())  # makes date only column
currentdate = dfticker15m.loc[dfticker15m.index[0], "timedate"]
dfticker15m = dfticker15m[dfticker15m["timedate"] != currentdate]  # removes current day to remove incomplete days
dfticker15m = dfticker15m.reset_index(drop=True)

def dfcday(ticker,chartinterval,currentday):
    if chartinterval==4:
        dfticker=dfticker1hr
    elif chartinterval==5:
        dfticker=dfticker4hr
    elif chartinterval == 3:
        dfticker=dfticker15m
    else:
        pass
    newdate = currentdate - timedelta(days=currentday)  # makes current date going back x number days
    dfcurrentday = dfticker[dfticker["timedate"] == newdate]  # makes dataframe of current day
    dfcurrentday = dfcurrentday.iloc[::-1]  # so that time moves forward with index value
    dfcurrentday = dfcurrentday.reset_index(drop=True)

    return dfcurrentday



def proboutcome(ticker,chartinterval,currentday,indexval): #sort out currentday caller so that currentday only occurs on dfs that arent weekends
    if chartinterval==5:
        values=values4hr
    elif chartinterval==4:
        values=values1hr
    elif chartinterval==3:
        values=values15m
    else:
        pass

    if chartinterval==4:
        listallindval=listallindval1hr
        dfticker=dfticker1hr
    elif chartinterval==5:
        listallindval = listallindval4hr
        dfticker=dfticker4hr
    elif chartinterval == 3:
        listallindval = listallindval15m
        dfticker=dfticker15m
    else:
        pass


    newdate = currentdate - timedelta(days=currentday)  # makes current date going back x number days
    dfcurrentday = dfticker[dfticker["timedate"] == newdate]  # makes dataframe of current day
    dfcurrentday = dfcurrentday.iloc[::-1]  # so that time moves forward with index value
    dfcurrentday = dfcurrentday.reset_index(drop=True)



    results = {}






    probhour = {0: [0.0, "up"], 1: [0.0, "down"], 2: [0.0, "up"], 3: [0.0, "down"], 4: [0.0, "up"],5: [0.0, "down"], 6: [0.0, "up"], 7: [0.0, "down"]}
    rsi = fval(dfcurrentday, "RSI", indexval)
    rsigrad = float(fval(dfcurrentday, "rsigrad", indexval))
    spreadgrad = dfcurrentday.loc[dfcurrentday.index[indexval], "Spread Grad"]
    spreadratio = float(fval(dfcurrentday, "Spread Ratio", indexval))
    histprofile = fval(dfcurrentday, "Histogram Profile", indexval)
    marat = fval(dfcurrentday, "MA Spread", indexval)
    if fval(dfcurrentday, 'Upper', indexval) < fval(dfcurrentday, 'close', indexval):
        breakbb = "breakover"
    elif fval(dfcurrentday, 'Lower', indexval) > fval(dfcurrentday, 'close', indexval):
        breakbb = "breakunder"
    else:
        breakbb = "within"
    if spreadgrad < 0:
        stsq = "st"
    else:
        stsq = "sq"


    for x in range(len(values)):
        updown = 0
        valueval=x
        probhour = {0: [0.0, "up"], 1: [0.0, "down"], 2: [0.0, "up"], 3: [0.0, "down"], 4: [0.0, "up"],
                    5: [0.0, "down"], 6: [0.0, "up"], 7: [0.0, "down"],8:[0.0, "up"],9:[0.0,"down"]}

        dfrsipup = listallindval[0][x]
        dfrsipdown = listallindval[1][x]
        dfbbpup1 = listallindval[2][x]
        dfbbpdown1 = listallindval[3][x]
        dfrsimacdup = listallindval[4][x]
        dfrsimacddown = listallindval[5][x]
        dfrsimaratioup = listallindval[6][x]
        dfrsimaratiodown = listallindval[7][x]
        dfmarsiup = listallindval[8][x]
        dfmarsidown = listallindval[9][x]




        for y in range(len(dfrsipup)):
            t = dfrsipup.loc[dfrsipup.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfrsipup.loc[dfrsipup.index[y], "RSI Gradient"].split(maxsplit=-1)

            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(
                    z[1]):  # checks if within any column on probu for rsi

                probhour[0][0] = dfrsipup.loc[dfrsipup.index[y], "Probability Up"]
                break

            else:
                pass

        for z in range(len(dfbbpup1)):
            y = dfbbpup1.loc[dfbbpup1.index[z], "bbprofile"].split(maxsplit=-1)

            if y[0] == breakbb and y[1] == stsq and float(y[2]) < spreadratio < float(y[3]):
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

            if y[0] == breakbb and y[1] == stsq and float(y[2]) < spreadratio < float(y[3]):
                probhour[3][0] = dfbbpdown1.loc[dfbbpdown1.index[z], "Probability Down"]
                break
            else:
                pass
        for y in range(len(dfrsimacdup)):
            t = dfrsimacdup.loc[dfrsimacdup.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfrsimacdup.loc[dfrsimacdup.index[y], "RSI Gradient"].split(maxsplit=-1)
            k = dfrsimacdup.loc[dfrsimacdup.index[y], "MACD Profile"]
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(
                    z[1]) and k == histprofile:  # checks if within any column on probu for rsi

                probhour[4][0] = dfrsimacdup.loc[dfrsimacdup.index[y], "Probability Up"]
                break

            else:
                pass

        for y in range(len(dfrsimacddown)):
            t = dfrsimacddown.loc[dfrsimacddown.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfrsimacddown.loc[dfrsimacddown.index[y], "RSI Gradient"].split(maxsplit=-1)
            k = dfrsimacddown.loc[dfrsimacddown.index[y], "MACD Profile"]
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]) and k == histprofile:
                probhour[5][0] = float(dfrsimacddown.loc[dfrsimacddown.index[y], "Probability Down"])
                break
            else:
                pass
        for y in range(len(dfrsimaratioup)):
            t = dfrsimaratioup.loc[dfrsimaratioup.index[y], "MA Ratio Range"].split(maxsplit=-1)
            if int(t[0]) < marat < int(t[1]):
                probhour[6][0] = dfrsimaratioup.loc[dfrsimaratioup.index[y], "Probability Up"]
                break
            else:
                pass

        for y in range(len(dfrsimaratiodown)):
            t = dfrsimaratiodown.loc[dfrsimaratiodown.index[y], "MA Ratio Range"].split(maxsplit=-1)
            if int(t[0]) < marat < int(t[1]):
                probhour[7][0] = dfrsimaratiodown.loc[dfrsimaratiodown.index[y], "Probability Down"]
                break
            else:
                pass

        for y in range(len(dfmarsiup)):
            t = dfmarsiup.loc[dfmarsiup.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfmarsiup.loc[dfmarsiup.index[y], "RSI Gradient"].split(maxsplit=-1)
            k = dfmarsiup.loc[dfmarsiup.index[y], "MA Profile"]
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(
                    z[1]) and k == histprofile:  # checks if within any column on probu for rsi

                probhour[8][0] = dfmarsiup.loc[dfmarsiup.index[y], "Probability Up"]
                break

            else:
                pass

        for y in range(len(dfmarsidown)):
            t = dfmarsidown.loc[dfmarsidown.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfmarsidown.loc[dfmarsidown.index[y], "RSI Gradient"].split(maxsplit=-1)
            k = dfmarsidown.loc[dfmarsidown.index[y], "MA Profile"]
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]) and k == histprofile:
                probhour[9][0] = float(dfmarsidown.loc[dfmarsidown.index[y], "Probability Down"])
                break
            else:
                pass

        listprobs = []
        listprobsup =[]
        listprobsdown=[]
        for x in range(len(probhour)):
            if probhour[x][0]!=0 and probhour[x][1]=="up":
                listprobsup.append(probhour[x][0])
            elif probhour[x][0]!=0 and probhour[x][1]=="down":
                listprobsdown.append(probhour[x][0])

            else:
                pass
        if len(listprobsup)>0 and len(listprobsdown)>0:
            maxup=max(listprobsup)
            maxdown=max(listprobsdown)
            aveup=mean(listprobsup)
            avedown=mean(listprobsdown)
            if maxup>maxdown and chartinterval==5:
                updown="up"

            elif maxdown>maxup and chartinterval==5:
                updown="down"
            elif maxup>maxdown and aveup>(avedown) and chartinterval==4 or 3:
                updown="up"

            elif maxdown>maxup and avedown>(aveup) and chartinterval==4 or 3:
                updown="down"
            else:
                pass
        elif len(listprobsup)>0 and len(listprobsdown)==0:
            updown="up"

        elif len(listprobsdown)>0 and len(listprobsup)==0:
            updown="down"

        else:
            continue


        results.update({x:[values[valueval][0],updown]})

        continue
    return results







def trader(ticker):

    n = 0
    bp=17500
    hj=0
    g=0
    weekends=0
    targethit=0
    nohitnoloss=0
    nohitnogain=0
    stoploss=0
    timebuy=0

    for x in reversed(range(1,120)):
        currentday = x
        dfbuy = dfcday(tickerlist[0], 3, currentday)
        hj = hj + 1

        if len(dfbuy)>70:


            hr4list = [2]
            hr4list2 = [3,4]

            hr1list = {2: [10, 11, 12, 13], 3: [14, 15, 16, 17], 4: [18, 19, 20, 21]}
            y = 39
            t = 10
            m15list = {}
            for x in range(hr1list[2][0], hr1list[4][3]):
                m15list.update({t: [y, y + 1, y + 2, y + 3]})
                y = y + 4
                t = t + 1
            tradetime = 0
            valueaim = 0
            timebuy = 0
            direction=0
            for x in hr4list:

                list4hrval = x
                hr4 = proboutcome(tickerlist[0], 5, currentday, x)


                for y in hr4:
                    if hr4[y][0] >=1 and hr4[y][1] != 0:
                        valueaim = hr4[y][0]
                        tradetime = list4hrval
                        direction=hr4[y][1]
                        chrlist = hr1list[tradetime]
                        for y in range(tradetime + 1, len(hr4list) + 1):
                            chrlist = chrlist + chrlist[y]
                        for x in chrlist:
                            hr1 = proboutcome(tickerlist[0], 4, currentday, x)
                            for y in hr1:
                                if hr1[y][0] >= valueaim and hr1[y][1] == direction:
                                    valueaim = hr1[y][0]
                                    tradetime = x
                                    direction = hr1[y][1]
                                    c15mlist = m15list[tradetime]
                                    for y in range(tradetime + 1, chrlist[-1]+1):
                                        c15mlist = c15mlist + m15list[y]
                                    for x in c15mlist:
                                        m15 = proboutcome(tickerlist[0], 3, currentday, x)
                                        for y in m15:
                                            if m15[y][0] == valueaim and m15[y][1] == direction:
                                                timebuy = x
                                                direction = m15[y][1]
                                                break
                                            else:
                                                pass
                                        break
                                    break
                                else:
                                    pass

                            break
                        break
                    else:
                        pass
                break
            if timebuy==0:
                for x in hr4list2:
                    list4hrval = x
                    hr4 = proboutcome(tickerlist[0], 5, currentday, x)

                    for y in hr4:
                        if hr4[y][0] >=0.5 and hr4[y][1] != 0:
                            valueaim = hr4[y][0]
                            tradetime = list4hrval
                            direction=hr4[y][1]
                            chrlist = hr1list[tradetime]
                            for y in range(tradetime + 1, len(hr4list) + 1):
                                chrlist = chrlist + chrlist[y]
                            for x in chrlist:
                                hr1 = proboutcome(tickerlist[0], 4, currentday, x)
                                for y in hr1:
                                    if hr1[y][0] >= valueaim and hr1[y][1] == direction:
                                        valueaim = hr1[y][0]
                                        tradetime = x
                                        direction = hr1[y][1]
                                        c15mlist = m15list[tradetime]
                                        for y in range(tradetime + 1, chrlist[-1]):
                                            c15mlist = c15mlist + m15list[y]
                                        for x in c15mlist:
                                            m15 = proboutcome(tickerlist[0], 3, currentday, x)
                                            for y in m15:
                                                if m15[y][0] == valueaim and m15[y][1] == direction:
                                                    timebuy = x
                                                    direction = m15[y][1]
                                                    break
                                                else:
                                                    pass
                                            break
                                        break
                                    else:
                                        pass

                                break
                            break
                        else:
                            pass
                    break
            else:
                print("nope")

            sellprice=0
            value=valueaim/100
            dfcurrentday=dfbuy
            currenthour=timebuy

            if direction=="up": #need to sort if equal probabilities i.e. using 4 hour probs or other indicator probs
                sellprice = 1
                buyprice = (fval(dfcurrentday, 'close', currenthour))
                numbershares = bp / buyprice
                n=n+1
                print(value)

                for x in range((currenthour + 1), len(dfcurrentday)):
                    if fval(dfcurrentday, "high", x) > buyprice * (1 + value):
                        bp = numbershares * buyprice * (1 + 2 * value)
                        targethit = targethit + 1
                        sellprice = buyprice * (1 + 2 * value)  # 2 x value to simulate etf
                        break
                    elif fval(dfcurrentday, "low", x) < buyprice * (0.985):
                        bp = numbershares * buyprice * (0.99)
                        sellprice = buyprice
                        stoploss = stoploss + 1
                        print("loss")
                        break
                    elif x>=(75) and fval(dfcurrentday, "high", x)>(buyprice*1.005):
                        bp = numbershares * buyprice*((((fval(dfcurrentday, "high", x)-buyprice)/buyprice)*2)+1)
                        sellprice = buyprice
                        nohitnoloss = nohitnoloss + 1
                        break
                    elif x>84 and fval(dfcurrentday,"high",x)>(buyprice):
                        bp = numbershares * buyprice
                        nohitnogain=nohitnogain+1
                        break
                    elif x > 84 and fval(dfcurrentday, "low", x) > (buyprice*0.995):
                        bp = numbershares * buyprice*0.995
                        nohitnogain = nohitnogain + 1
                        break
                    elif x > 84 and fval(dfcurrentday, "low", x) > (buyprice*0.99):
                        bp = numbershares * buyprice*0.99
                        nohitnogain = nohitnogain + 1
                        break
                    elif x > 84 and fval(dfcurrentday, "low", x) > (buyprice*0.987):
                        bp = numbershares * buyprice*0.987
                        nohitnogain = nohitnogain + 1
                        break
                    else:
                        continue


            elif direction=="down":
                print(value)

                sellprice=1
                buyprice = (fval(dfcurrentday, 'close', currenthour))
                numbershares = bp / buyprice
                n=n+1
                for x in range((currenthour + 1), len(dfcurrentday)):
                    if fval(dfcurrentday, "low", x) < buyprice * (1 - value):
                        bp = numbershares * buyprice * (1 + 2 * value)
                        targethit = targethit + 1
                        sellprice = buyprice * (1 + 2 * value)


                        break
                    elif fval(dfcurrentday, "high", x) > buyprice * (1.015):
                        bp = numbershares * buyprice * (0.99)
                        sellprice = buyprice
                        stoploss=stoploss+1
                        print("loss")


                        break
                    elif x>=(75) and fval(dfcurrentday, "low", x)<(buyprice*0.995):
                        bp = numbershares * buyprice*((((buyprice-fval(dfcurrentday, "low", x))/buyprice)*2)+1)
                        sellprice = buyprice
                        nohitnoloss = nohitnoloss + 1

                        break
                    elif x>84 and fval(dfcurrentday,"low",x)<(buyprice):
                        bp = numbershares * buyprice
                        nohitnogain=nohitnogain+1
                        break
                    elif x > 84 and fval(dfcurrentday, "high", x) < (buyprice*1.005):
                        bp = numbershares * buyprice*0.995
                        nohitnogain = nohitnogain + 1
                        break
                    elif x > 84 and fval(dfcurrentday, "high", x) < (buyprice*1.01):
                        bp = numbershares * buyprice*0.99
                        nohitnogain = nohitnogain + 1
                        break
                    elif x > 84 and fval(dfcurrentday, "high", x) < (buyprice*1.013):
                        bp = numbershares * buyprice*0.987
                        nohitnogain = nohitnogain + 1
                        break


                    else:
                        continue





            else:
                pass






        else:
            weekends=weekends+1
            sellprice=1
            continue



    print("stoploss: " + str(stoploss))
    print("nohitnsomegain" +str(nohitnoloss))
    print("nohitnoloss"+str(nohitnogain))
    print(hj)
    print("Number of attempted trades: "+str(n))
    print("Buying Power: "+str(bp))
    print("Total trading days: " +str(hj-weekends))
    print("Targets Hit: "+str(targethit))
    print("Days Traded:" + str(100*(n/(hj-weekends))) + "%")
    print("Target Hit Rate: " + str(100*(targethit/n))+ "%")

trader(tickerlist[0])

print("--- %s seconds ---" % (time.time() - start_time))
