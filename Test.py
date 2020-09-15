
import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools
start_time = time.time()

path = r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data\3 months prior'
path2=r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data\current day'
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

values = {0: [3, 0.8], 1: [2.5, 0.65], 2: [2, 0.65], 3: [1.5, 0.65], 4: [1, 0.6], 5: [0.5, 0.5]}

def probresults(ticker,chartinterval):

    listcsvpull=["rsip","bbp","rsimacdp","maratiop"]
    dfindicators=[]
    for x in listcsvpull:
        pcsv=path + ticker + "short" + "Sep" + x + str(listdf[chartinterval]) + ".csv"
        dfp=pd.read_csv(pcsv)
        dfindicators.append(dfp)


    dfrsi = dfindicators[0]
    dfbb = dfindicators[1]
    dfrsimacd = dfindicators[2]
    dfmaratio = dfindicators[3]



    listvalind = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [],7:[],8:[]}

    inds = {1: dfrsi, 2: dfbb, 3: dfrsimacd,4:dfmaratio}


    for x in range(1, len(inds) + 1):
        inddf = inds[x]

        for y in range(0, len(values), 2):
            value1 = values[y][0]
            pmin1 = values[y][1]
            inddf1 = inddf[inddf["Value Change"]==value1]
            inddf1up = inddf1[inddf1["Probability Up"] > pmin1]
            inddf1up = inddf1up.reset_index(drop=True)

            listtodrop = []

            for q in range(len(inddf1up)):
                if float(inddf1up.loc[inddf1up.index[q], "Probability Up"]) < float(inddf1up.loc[inddf1up.index[q], "Probability Down"]):  # removes values where probup is less than down and vice versa
                    listtodrop.append(q)  # makes list of rows to be removed (doing it in the loop would remvoe rows breaking for loop length
                else:
                    pass
            inddf1up.drop(index=listtodrop, inplace=True)  # remvoes rows
            inddf1up = inddf1up.reset_index(drop=True)

            inddf1down = inddf1[inddf1["Probability Down"] > pmin1]
            inddf1down = inddf1down.reset_index(drop=True)

            listtodrop = []
            for q in range(len(inddf1down)):
                if float(inddf1down.loc[inddf1down.index[q], "Probability Up"]) > float(inddf1down.loc[inddf1down.index[q], "Probability Down"]):
                    listtodrop.append(q)
                else:
                    pass
            inddf1down.drop(index=listtodrop, inplace=True)
            inddf1down = inddf1down.reset_index(drop=True)
            listvalind[2 * x - 1].append(inddf1up)
            listvalind[2 * x].append(inddf1down)

            value2 = values[y+1][0]
            pmin2 = values[y+1][1]
            inddf2 = inddf[inddf["Value Change"] == value2]
            inddf2up = inddf2[inddf2["Probability Up"] > pmin2]
            inddf2up = inddf2up.reset_index(drop=True)

            listtodrop = []

            for q in range(len(inddf2up)):
                if float(inddf2up.loc[inddf2up.index[q], "Probability Up"]) < float(inddf2up.loc[inddf2up.index[q], "Probability Down"]):  # removes values where probup is less than down and vice versa
                    listtodrop.append(q)  # makes list of rows to be removed (doing it in the loop would remvoe rows breaking for loop length
                else:
                    pass
            inddf2up.drop(index=listtodrop, inplace=True)  # remvoes rows
            inddf2up = inddf2up.reset_index(drop=True)

            inddf2down = inddf2[inddf2["Probability Down"] > pmin2]
            inddf2down = inddf2down.reset_index(drop=True)

            listtodrop = []
            for q in range(len(inddf2down)):
                if float(inddf2down.loc[inddf2down.index[q], "Probability Up"]) > float(
                        inddf2down.loc[inddf2down.index[q], "Probability Down"]):
                    listtodrop.append(q)
                else:
                    pass
            inddf2down.drop(index=listtodrop, inplace=True)
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

    return listvalrsiu,listvalrsid,listvalbbpu,listvalbbpd,listvalrsimacdpu,listvalrsimacdpd,listvalmaratiopu,listvalmaratiopd

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


def proboutcome(ticker,chartinterval,currentday,indexval): #sort out currentday caller so that currentday only occurs on dfs that arent weekends

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


    if chartinterval==3:
        lengthmin=20
    elif chartinterval==4:
        lengthmin=5
    elif chartinterval ==5:
        lengthmin=3
    else:
        pass
    results = {}
    if len(dfcurrentday) > lengthmin:




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
                        5: [0.0, "down"], 6: [0.0, "up"], 7: [0.0, "down"]}

            dfrsipup = listallindval[0][x]
            dfrsipdown = listallindval[1][x]
            dfbbpup1 = listallindval[2][x]
            dfbbpdown1 = listallindval[3][x]
            dfrsimacdup = listallindval[4][x]
            dfrsimacddown = listallindval[5][x]
            dfrsimaratioup = listallindval[6][x]
            dfrsimaratiodown = listallindval[7][x]

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

            listprobs = []
            for x in range(len(probhour)):
                listprobs.append(probhour[x][0])

            for x in range(len(probhour)):
                if max(listprobs) == 0.0:
                    break
                elif max(listprobs) == probhour[x][0]:
                    updown = probhour[x][1]
                    break
                else:
                    pass
            results.update({x:[values[valueval][0],updown]})
            continue
    return results,dfcurrentday


for x in range(1,90):


    for x in reversed(range(1,90)):
        currentday=25

        hr4list=[2,3]
        hr4list2=[4,5]

        hr1list={2:[10,11,12,13],3:[14,15,16,17],4:[18,19,20,21],}
        y = 37
        t = 10
        m15list={}
        for x in range(hr1list[2][0],hr1list[3][3]):

            m15list.update({t:[y,y+1,y+2,y+3]})
            y=y+4
            t=t+1


        tradetime=0
        valueaim=0
        timebuy="non"
        for x in hr4list:
            print(x)
            list4hrval=x
            hr4 = proboutcome(tickerlist[0], 5, currentday, x)

            for y in hr4:
                print(y)
                if y[0]== 3 or 2.5 or 2 or 1.5 and y[1]!=0:
                    valueaim=y[0]
                    tradetime=list4hrval
                    print("hey")
                    break
                else:
                    print("four")
        if tradetime==0:
            for x in hr4list2:
                hr4 = proboutcome(tickerlist[0],5,currentday,x)

                for y in hr4:
                    if hr4[y][1]!=0:
                        valueaim=y[0]
                        tradetime=5

                    else:
                        pass

        else:
            pass
        print(tradetime, valueaim, "yoyo")
        chrlist = hr1list[3]
        for x in chrlist:
            hr1=proboutcome(tickerlist[0],4,currentday,x)
            for y in hr1:
                if y[0] ==valueaim or (valueaim-0.5):
                    valueaim=hr1[y][0]
                    tradetime=x
                    break
                else:
                    print("one")
        c15mlist=m15list[tradetime]
        for x in c15mlist:
            m15=proboutcome(tickerlist[0],3,currentday,x)
            for y in m15:
                if y[0]==valueaim:
                    timebuy=x

                    break
                else:
                    print("fifteen")
        print(timebuy)



def trader(ticker):

    n = 0
    bp=17500
    hj=0
    g=0
    weekends=0
    targethit=0
    nohitnoloss=0
    stoploss=0

    for x in reversed(range(1,90)):
        currentday=x

        hr4list=[2,3,4]

        hr1list={2:[10,11,12,13],3:[14,15,16,17],4:[18,19,20,21]}
        y = 37
        t = 10
        m15list={}
        for x in range(hr1list[1][0],hr1list[3][3]):

            m15list.update({t:[y,y+1,y+2,y+3]})
            y=y+4
            t=t+1

        for x in hr4list:
            hr4 = proboutcome(tickerlist[0], 5, j, x)
            for x in hr4:
                print(hr4[x])


        hj=hj+1
        sellprice=0
        while sellprice == 0:


            if updown=="up": #need to sort if equal probabilities i.e. using 4 hour probs or other indicator probs
                print(value * 100)
                sellprice = 1
                buyprice = (fval(dfcurrentday, 'close', currenthour))
                numbershares = bp / buyprice
                n=n+1

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
                        print(value * 100)
                        break
                    elif x>=5 and fval(dfcurrentday, "high", x)>buyprice  :
                        bp = numbershares * fval(dfcurrentday, "high", x)
                        sellprice = buyprice
                        nohitnoloss = nohitnoloss + 1
                        break
                    else:
                        continue
                break

            elif updown=="down":
                print(value * 100)

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
                        print(value * 100)

                        break
                    elif x>=5 and fval(dfcurrentday, "low", x)<buyprice:
                        bp = numbershares * buyprice*(buyprice/fval(dfcurrentday, "low", x))
                        sellprice = buyprice
                        nohitnoloss = nohitnoloss + 1
                        break
                    else:
                        continue

                break



            else:
                pass

            break




        else:
            weekends=weekends+1
            sellprice=1
            pass

        continue
    print("stoploss: " + str(stoploss))
    print(nohitnoloss)
    print(g)
    print("Number of attempted trades: "+str(n))
    print("Buying Power: "+str(bp))
    print("Total trading days: " +str(hj-weekends))
    print("Targets Hit: "+str(targethit))
    print("Days Traded:" + str(100*(n/(hj-weekends))) + "%")
    print("Target Hit Rate: " + str(100*(targethit/n))+ "%")
#trader(tickerlist[0])

print("--- %s seconds ---" % (time.time() - start_time))

