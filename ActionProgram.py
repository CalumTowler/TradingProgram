

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



excel1hr = path2 + tickerlist[0] + "short" + "full" + str(listdf[4]) + ".csv" #need to make into fucntion and for loop to make dfs
dfticker1hr = pd.read_csv(excel1hr)
dfticker1hr['time'] = pd.to_datetime(dfticker1hr['time'])
dfticker1hr["timedate"] = 0
for x in range(len(dfticker1hr)):  # remove current day from experiment
    dfticker1hr.loc[dfticker1hr.index[x], "timedate"] = (dfticker1hr.loc[dfticker1hr.index[x], "time"].date())  # makes date only column
currentdate = dfticker1hr.loc[dfticker1hr.index[0], "timedate"]
dfticker1hr = dfticker1hr[dfticker1hr["timedate"] != currentdate]  # removes current day to remove incomplete days
dfticker1hr = dfticker1hr.reset_index(drop=True)


# excel4hr = path2 + tickerlist[0] + "short" + "full" + str(listdf[5]) + ".csv"
# dfticker4hr = pd.read_csv(excel4hr)
# dfticker4hr['time'] = pd.to_datetime(dfticker4hr['time'])
# dfticker4hr["timedate"] = 0
# for x in range(len(dfticker4hr)):  # remove current day from experiment
#     dfticker4hr.loc[dfticker4hr.index[x], "timedate"] = (dfticker4hr.loc[dfticker4hr.index[x], "time"].date())  # makes date only column
# currentdate = dfticker4hr.loc[dfticker4hr.index[0], "timedate"]
# dfticker4hr = dfticker4hr[dfticker4hr["timedate"] != currentdate]  # removes current day to remove incomplete days
# dfticker4hr = dfticker4hr.reset_index(drop=True)

excel15min = path2 + tickerlist[0] + "short" + "full" + str(listdf[3]) + ".csv"
dfticker15m = pd.read_csv(excel15min)
dfticker15m['time'] = pd.to_datetime(dfticker15m['time'])
dfticker15m["timedate"] = 0
for x in range(len(dfticker15m)):  # remove current day from experiment
    dfticker15m.loc[dfticker15m.index[x], "timedate"] = (dfticker15m.loc[dfticker15m.index[x], "time"].date())  # makes date only column
currentdate = dfticker15m.loc[dfticker15m.index[0], "timedate"]
dfticker15m = dfticker15m[dfticker15m["timedate"] != currentdate]  # removes current day to remove incomplete days
dfticker15m = dfticker15m.reset_index(drop=True)

excel5min = path2 + tickerlist[0] + "short" + "full" + str(listdf[2]) + ".csv"
dfticker5m = pd.read_csv(excel5min)
dfticker5m['time'] = pd.to_datetime(dfticker5m['time'])
dfticker5m["timedate"] = 0
for x in range(len(dfticker5m)):  # remove current day from experiment
    dfticker5m.loc[dfticker5m.index[x], "timedate"] = (dfticker5m.loc[dfticker5m.index[x], "time"].date())  # makes date only column
currentdate = dfticker5m.loc[dfticker5m.index[0], "timedate"]
dfticker5m = dfticker5m[dfticker5m["timedate"] != currentdate]  # removes current day to remove incomplete days
dfticker5m = dfticker5m.reset_index(drop=True)

def dfcday(ticker,chartinterval,currentday):
    if chartinterval==4:
        dfticker=dfticker1hr
    # elif chartinterval==5:
    #     dfticker=dfticker4hr
    elif chartinterval == 3:
        dfticker=dfticker15m
    elif chartinterval ==2:
        dfticker=dfticker5m
    else:
        pass
    newdate = currentdate - timedelta(days=currentday)  # makes current date going back x number days
    dfcurrentday = dfticker[dfticker["timedate"] == newdate]  # makes dataframe of current day
    dfcurrentday = dfcurrentday.iloc[::-1]  # so that time moves forward with index value
    dfcurrentday = dfcurrentday.reset_index(drop=True)

    return dfcurrentday


listcsvpull = ["rsip", "bbp", "rsimacdp", "maratiop", "marsip"]
dfindicators5 = []
for x in listcsvpull:
    pcsv = path + tickerlist[0] + "short" + "Sep" + x + str(listdf[2]) + ".csv"
    dfp = pd.read_csv(pcsv)
    dfindicators5.append(dfp)

dfindicators15=[]
for x in listcsvpull:
    pcsv = path + tickerlist[0] + "short" + "Sep" + x + str(listdf[3]) + ".csv"
    dfp = pd.read_csv(pcsv)
    dfindicators15.append(dfp)

dfindicators60=[]
for x in listcsvpull:
    pcsv = path + tickerlist[0] + "short" + "Sep" + x + str(listdf[4]) + ".csv"
    dfp = pd.read_csv(pcsv)
    dfindicators60.append(dfp)




def probpull(ticker,chartinterval,q1,q2,q3):

    if chartinterval==2:
        dfindicators=dfindicators5
    elif chartinterval==3:
        dfindicators=dfindicators15
    elif chartinterval==4:
        dfindicators=dfindicators60
    else:
        pass

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
        values = [3, 2.5, 2, 1.5, 1.25, 1, 0.75, 0.5]

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
            if y==2 or 1.5:
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Enough Values"]=inddf1.loc[inddf1.index[x],"Nvalue"]>=10
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Up"]=inddf1.loc[inddf1.index[x],"Probability Up"]>=float((probu.quantile([q1])))
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Down"]=inddf1.loc[inddf1.index[x],"Probability Down"]>=float((probd.quantile([q1])))
            elif y==3 or 2.5:
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Enough Values"]=inddf1.loc[inddf1.index[x],"Nvalue"]>=6
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Up"]=inddf1.loc[inddf1.index[x],"Probability Up"]>=float((probu.quantile([q2]))) and inddf1.loc[inddf1.index[x],"Probability Up"]>=inddf1.loc[inddf1.index[x],"Probability Down"]
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Down"]=inddf1.loc[inddf1.index[x],"Probability Down"]>=float((probd.quantile([q2]))) and inddf1.loc[inddf1.index[x],"Probability Down"]>=inddf1.loc[inddf1.index[x],"Probability Up"]
            elif y==1.25 or 1 or 0.75 or 0.5:
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Enough Values"]=inddf1.loc[inddf1.index[x],"Nvalue"]>=10
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Up"]=inddf1.loc[inddf1.index[x],"Probability Up"]>=float((probu.quantile([q3])))
                for x in range(len(inddf1)):
                    inddf1.loc[inddf1.index[x],"Good Probability Down"]=inddf1.loc[inddf1.index[x],"Probability Down"]>=float((probd.quantile([q3])))


            else:
                pass

            indvalues.append(inddf1)
            if y == 0.5:
                df1 = pd.concat(indvalues)
                inds[ind][0]=df1
            else:
                pass

    return inds





# allindval4hr=probpull(tickerlist[0],5)




def proboutcome(ticker,chartinterval,currentday,indexval): #sort out currentday caller so that currentday only occurs on dfs that arent weekends






    if chartinterval==4:
        allindval=allindval1hr
        dfticker=dfticker1hr
    # elif chartinterval==5:
    #     allindval = allindval4hr
    #     dfticker=dfticker4hr
    elif chartinterval == 3:
        allindval = allindval15m
        dfticker=dfticker15m
    elif chartinterval==2:
        allindval = allindval5m
        dfticker=dfticker5m
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
    results = {}

    values=[3,2.5,2,1.5,1.25,1,0.75,0.5]
    for x in values:
        updown = 0
        valueval=x
        probhour = {0: [0.0, "up"], 1: [0.0, "down"], 2: [0.0, "up"], 3: [0.0, "down"], 4: [0.0, "up"],
                    5: [0.0, "down"], 6: [0.0, "up"], 7: [0.0, "down"],8:[0.0, "up"],9:[0.0,"down"]}

        dfrsi = allindval[0][0]
        dfbb = allindval[1][0]
        dfrsimacd = allindval[2][0]
        dfmaratio = allindval[3][0]
        dfmarsi = allindval[4][0]

        dfrsi=dfrsi[dfrsi["Value Change"]==x]
        dfbb = dfbb[dfbb["Value Change"] == x]
        dfrsimacd = dfrsimacd[dfrsimacd["Value Change"] == x]
        dfmaratio = dfmaratio[dfmaratio["Value Change"] == x]
        dfmarsi = dfmarsi[dfmarsi["Value Change"] == x]



        for y in range(len(dfrsi)):
            t = dfrsi.loc[dfrsi.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfrsi.loc[dfrsi.index[y], "RSI Gradient"].split(maxsplit=-1)

            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(
                    z[1]) and dfrsi.loc[dfrsi.index[y], "Enough Values"]==True and dfrsi.loc[dfrsi.index[y], "Good Probability Up"]==True:  # checks if within any column on probu for rsi

                probhour[0][0] = dfrsi.loc[dfrsi.index[y], "Probability Up"]
                break

            else:
                pass

        for z in range(len(dfbb)):
            y = dfbb.loc[dfbb.index[z], "bbprofile"].split(maxsplit=-1)

            if y[0] == breakbb and y[1] == stsq and float(y[2]) < spreadratio < float(y[3]) and dfbb.loc[dfbb.index[z], "Enough Values"]==True and dfbb.loc[dfbb.index[z], "Good Probability Up"]==True:
                probhour[2][0] = float(dfbb.loc[dfbb.index[z], "Probability Up"])
                break
            else:
                pass

        for y in range(len(dfrsi)):
            t = dfrsi.loc[dfrsi.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfrsi.loc[dfrsi.index[y], "RSI Gradient"].split(maxsplit=-1)
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]) and dfrsi.loc[dfrsi.index[y], "Enough Values"]==True and dfrsi.loc[dfrsi.index[y], "Good Probability Down"]==True:
                probhour[1][0] = dfrsi.loc[dfrsi.index[y], "Probability Down"]
                break
            else:
                pass

        for z in range(len(dfbb)):
            y = dfbb.loc[dfbb.index[z], "bbprofile"].split(maxsplit=-1)

            if y[0] == breakbb and y[1] == stsq and float(y[2]) < spreadratio < float(y[3]) and dfbb.loc[dfbb.index[z], "Enough Values"]==True and dfbb.loc[dfbb.index[z], "Good Probability Down"]==True:
                probhour[3][0] = dfbb.loc[dfbb.index[z], "Probability Down"]
                break
            else:
                pass
        for y in range(len(dfrsimacd)):
            t = dfrsimacd.loc[dfrsimacd.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfrsimacd.loc[dfrsimacd.index[y], "RSI Gradient"].split(maxsplit=-1)
            k = dfrsimacd.loc[dfrsimacd.index[y], "MACD Profile"]
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(
                    z[1]) and k == histprofile and dfrsimacd.loc[dfrsimacd.index[y], "Enough Values"]==True and dfrsimacd.loc[dfrsimacd.index[y], "Good Probability Up"]==True:  # checks if within any column on probu for rsi

                probhour[4][0] = dfrsimacd.loc[dfrsimacd.index[y], "Probability Up"]
                break

            else:
                pass

        for y in range(len(dfrsimacd)):
            t = dfrsimacd.loc[dfrsimacd.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfrsimacd.loc[dfrsimacd.index[y], "RSI Gradient"].split(maxsplit=-1)
            k = dfrsimacd.loc[dfrsimacd.index[y], "MACD Profile"]
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]) and k == histprofile and dfrsimacd.loc[dfrsimacd.index[y], "Enough Values"]==True and dfrsimacd.loc[dfrsimacd.index[y], "Good Probability Down"]==True:
                probhour[5][0] = float(dfrsimacd.loc[dfrsimacd.index[y], "Probability Down"])
                break
            else:
                pass
        for y in range(len(dfmaratio)):
            t = dfmaratio.loc[dfmaratio.index[y], "MA Ratio Range"].split(maxsplit=-1)
            if int(t[0]) < marat < int(t[1]) and dfmaratio.loc[dfmaratio.index[y], "Enough Values"]==True and dfmaratio.loc[dfmaratio.index[y], "Good Probability Up"]==True:
                probhour[6][0] = dfmaratio.loc[dfmaratio.index[y], "Probability Up"]
                break
            else:
                pass

        for y in range(len(dfmaratio)):
            t = dfmaratio.loc[dfmaratio.index[y], "MA Ratio Range"].split(maxsplit=-1)
            if int(t[0]) < marat < int(t[1]) and dfmaratio.loc[dfmaratio.index[y], "Enough Values"]==True and dfmaratio.loc[dfmaratio.index[y], "Good Probability Down"]==True:
                probhour[7][0] = dfmaratio.loc[dfmaratio.index[y], "Probability Down"]
                break
            else:
                pass

        for y in range(len(dfmarsi)):
            t = dfmarsi.loc[dfmarsi.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfmarsi.loc[dfmarsi.index[y], "RSI Gradient"].split(maxsplit=-1)
            k = dfmarsi.loc[dfmarsi.index[y], "MA Profile"]
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(
                    z[1]) and k == histprofile and dfmarsi.loc[dfmarsi.index[y], "Enough Values"]==True and dfmarsi.loc[dfmarsi.index[y], "Good Probability Up"]==True:  # checks if within any column on probu for rsi

                probhour[8][0] = dfmarsi.loc[dfmarsi.index[y], "Probability Up"]
                break

            else:
                pass

        for y in range(len(dfmarsi)):
            t = dfmarsi.loc[dfmarsi.index[y], "RSI Range"].split(maxsplit=-1)
            z = dfmarsi.loc[dfmarsi.index[y], "RSI Gradient"].split(maxsplit=-1)
            k = dfmarsi.loc[dfmarsi.index[y], "MA Profile"]
            if int(t[0]) < rsi < int(t[1]) and int(z[0]) < rsigrad < int(z[1]) and k == histprofile and dfmarsi.loc[dfmarsi.index[y], "Enough Values"]==True and dfmarsi.loc[dfmarsi.index[y], "Good Probability Down"]==True:
                probhour[9][0] = float(dfmarsi.loc[dfmarsi.index[y], "Probability Down"])
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
            updown=0
            if aveup > (avedown*1) and chartinterval==5:
                updown="up"

            elif avedown > (aveup*1) and chartinterval==5:
                updown="down"
            elif maxup > maxdown and aveup > (avedown) and chartinterval == 4 or 3:
                updown = "up"

            elif maxdown > maxup and avedown > (aveup) and chartinterval == 4 or 3:
                updown = "down"

            elif aveup > (avedown) and chartinterval== 2:
                updown="up"

            elif avedown > (aveup)  and chartinterval== 2:
                updown="down"
            else:
                pass
        elif len(listprobsup)>0 and len(listprobsdown)==0:
            updown="up"

        elif len(listprobsdown)>0 and len(listprobsup)==0:
            updown="down"

        else:
            continue

        results.update({valueval:[valueval,updown]})

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


    for x in reversed(range(2,20)):
        currentday = x
        dfbuy = dfcday(tickerlist[0], 2, currentday)
        hj = hj + 1
        if len(dfbuy)>200:
            timebuy = 0





            hr1list = {2: [10, 11, 12, 13], 3: [14, 15, 16, 17, 18], 4: [18]}

            m15list = {10: [39, 40, 41, 42], 11: [43, 44, 45, 46], 12: [47, 48, 49, 50], 13: [51, 52, 53, 54], 14: [55, 56, 57, 58], 15: [59, 60, 61, 62],
                       16: [63, 64, 65, 66], 17: [67, 68, 69, 70], 18: [71, 72, 73, 74], 19: [75, 76]}

            m5list={39: [120, 121, 122], 40: [123, 124, 125], 41: [126, 127, 128], 42: [129, 130, 131], 43: [132, 133, 134], 44: [135, 136, 137], 45: [138, 139, 140], 46: [141, 142, 143], 47: [144, 145, 146],
                    48: [147, 148, 149], 49: [150, 151, 152], 50: [153, 154, 155], 51: [156, 157, 158], 52: [159, 160, 161], 53: [162, 163, 164], 54: [165, 166, 167], 55: [168, 169, 170], 56: [171, 172, 173],
                    57: [174, 175, 176], 58: [177, 178, 179], 59: [180, 181, 182], 60: [183, 184, 185], 61: [186, 187, 188], 62: [189, 190, 191], 63: [192, 193, 194], 64: [195, 196, 197], 65: [198, 199, 200],
                    66: [201, 202, 203], 67: [204, 205, 206], 68: [207, 208, 209], 69: [210, 211, 212], 70: [213, 214, 215], 71: [216, 217, 218], 72: [219, 220, 221], 73: [222, 223, 224], 74: [225, 226, 227],
                    75: [228, 229, 230], 76: [231, 232, 233], 77: [234, 235, 236], 78: [237, 238, 239], 79: [240, 241, 242], 80: [243, 244, 245], 81: [246, 247, 248]}



            valueaim=0
            tradetimehour=0
            tradetime15min=0
            tradetime5min=0
            direction=0


            chrlist=hr1list[2]
            for hr1time in chrlist:
                if tradetime15min == 0:

                    hr1 = proboutcome(tickerlist[0], 4, currentday, hr1time)
                    for y in hr1:
                        if hr1[y][0] >= 1:

                            valueaim = hr1[y][0]
                            tradetime15min = hr1time + 1
                            direction = hr1[y][1]

                            break
                        else:
                            continue
                else:
                    break




            if tradetime15min!=0:
                c15mlist=m15list[tradetime15min]
                for y in range(tradetime15min+1, chrlist[-1]):
                    c15mlist = c15mlist + m15list[y]
                for m15time in c15mlist:
                    if tradetime5min==0:

                        m15=proboutcome(tickerlist[0],3,currentday,m15time)
                        for y in m15:
                            if m15[y][0] >= 1 and m15[y][1] == direction and tradetime5min==0:

                                valueaim = m15[y][0]
                                tradetime5min = m15time + 1
                                direction = m15[y][1]



                                break
                            else:
                                continue
                    else:
                        break
            else:
                pass

            if tradetime5min!=0:
                c5mlist = m5list[tradetime5min]
                for y in range(tradetime5min + 1, c15mlist[-1]):
                    c5mlist = c5mlist + m5list[y]
                for m5time in c5mlist:
                    if timebuy==0:
                        m5 = proboutcome(tickerlist[0], 2, currentday, m5time)
                        for y in m5:
                            if m5[y][0] >= (valueaim-0.5) and m5[y][1] == direction:

                                timebuy = m5time
                                direction = m5[y][1]
                                endtrade=164

                                break

                            else:
                                continue
                    else:
                        break
            else:
                pass


            if timebuy==0:
                timebuy=0
                valueaim = 0
                tradetimehour = 0
                tradetime15min = 0
                tradetime5min = 0
                direction = 0



                chrlist = hr1list[3]


                for hr1time in chrlist:
                    if tradetime15min==0:
                        hr1 = proboutcome(tickerlist[0], 4, currentday, hr1time)


                        for y in hr1:
                            if hr1[y][0] >= 1 and tradetime15min==0:
                                valueaim = hr1[y][0]
                                tradetime15min = hr1time + 1
                                direction = hr1[y][1]


                                break
                            else:
                                continue
                    else:
                        break



                else:
                    pass
                if tradetime15min != 0:
                    # print("15 2")

                    c15mlist = m15list[tradetime15min]
                    for y in range(tradetime15min + 1, chrlist[-1]):
                        c15mlist = c15mlist + m15list[y]
                    for m15time in c15mlist:
                        if tradetime5min==0:
                            m15 = proboutcome(tickerlist[0], 3, currentday, m15time)
                            for y in m15:
                                if m15[y][0] >= 1 and m15[y][1] == direction and tradetime5min==0:
                                    valueaim = m15[y][0]
                                    tradetime5min = m15time + 1
                                    direction = m15[y][1]


                                    break
                                else:
                                    continue
                        else:
                            break

                else:
                    pass
                if tradetime5min != 0:
                    # print("5 2")
                    c5mlist = m5list[tradetime5min]
                    for y in range(tradetime5min + 1, c15mlist[-1]):
                        c5mlist = c5mlist + m5list[y]

                    for m5time in c5mlist:
                        if timebuy==0:

                            m5 = proboutcome(tickerlist[0], 2, currentday, m5time)
                            for y in m5:
                                if m5[y][0] >= (valueaim-0.5) and m5[y][1] == direction and timebuy==0:
                                    timebuy = m5time
                                    direction = m5[y][1]
                                    endtrade=240

                                    break

                                else:
                                    continue
                        else:
                            break

                else:
                    pass








            sellprice=0
            value=(valueaim-0.25)/100
            dfcurrentday=dfbuy
            currenthour=timebuy


            if direction=="up" and timebuy!=0: #need to sort if equal probabilities i.e. using 4 hour probs or other indicator probs
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
                        bp = numbershares * buyprice * (0.97)
                        sellprice = buyprice
                        stoploss = stoploss + 1
                        break
                    elif x>=(endtrade-10) and fval(dfcurrentday, "high", x)>(buyprice*(1+value/2)):
                        bp = numbershares * buyprice*((((fval(dfcurrentday, "high", x)-buyprice)/buyprice)*2)+1)
                        sellprice = buyprice
                        nohitnoloss = nohitnoloss + 1
                        break
                    elif x>endtrade and fval(dfcurrentday,"high",x)>(buyprice):
                        bp = numbershares * buyprice
                        nohitnogain=nohitnogain+1
                        break
                    elif x > endtrade and fval(dfcurrentday, "low", x) > (buyprice*0.995):
                        bp = numbershares * buyprice*0.995
                        nohitnogain = nohitnogain + 1
                        break
                    elif x > endtrade and fval(dfcurrentday, "low", x) > (buyprice*0.99):
                        bp = numbershares * buyprice*0.99
                        nohitnogain = nohitnogain + 1
                        break
                    elif x > endtrade and fval(dfcurrentday, "low", x) > (buyprice*0.987):
                        bp = numbershares * buyprice*0.987
                        nohitnogain = nohitnogain + 1
                        break
                    else:
                        continue
                continue


            elif direction=="down" and timebuy!=0:

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
                        bp = numbershares * buyprice * (0.97)
                        sellprice = buyprice
                        stoploss=stoploss+1


                        break
                    elif x>=(endtrade-10) and fval(dfcurrentday, "low", x)<(buyprice*(1-value/2)):
                        bp = numbershares * buyprice*((((buyprice-fval(dfcurrentday, "low", x))/buyprice)*2)+1)
                        sellprice = buyprice
                        nohitnoloss = nohitnoloss + 1

                        break
                    elif x>endtrade and fval(dfcurrentday,"low",x)<(buyprice):
                        bp = numbershares * buyprice
                        nohitnogain=nohitnogain+1
                        break
                    elif x > endtrade and fval(dfcurrentday, "high", x) < (buyprice*1.005):
                        bp = numbershares * buyprice*0.995
                        nohitnogain = nohitnogain + 1
                        break
                    elif x > endtrade and fval(dfcurrentday, "high", x) < (buyprice*1.01):
                        bp = numbershares * buyprice*0.99
                        nohitnogain = nohitnogain + 1
                        break
                    elif x > endtrade and fval(dfcurrentday, "high", x) < (buyprice*1.013):
                        bp = numbershares * buyprice*0.987
                        nohitnogain = nohitnogain + 1
                        break


                    else:
                        continue
                continue





            else:
                continue






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
    return bp, stoploss, n, targethit,nohitnogain,nohitnoloss

q1=0.7
q2=0.7
q3=0.6

q4=0.85
q5=0.85
q6=0.8

q7=0.85
q8=0.85
q9=0.85







allindval1hr = probpull(tickerlist[0], 4,q1,q2,q3)
allindval15m = probpull(tickerlist[0], 3,q4,q5,q6)
allindval5m = probpull(tickerlist[0], 2,q7,q8,q9)
listreturned = trader(tickerlist[0])
# bp = listreturned[0]
# stoploss = listreturned[1]
# n = listreturned[2]
# targethit = listreturned[3]
# nohitnogain = listreturned[4]
# nohitnoloss = listreturned[5]



            # for x in range(2,5):
            #     chartinterval=x
            #     listcsvpull = ["rsip", "bbp", "rsimacdp", "maratiop", "marsip"]
            #     dfindicators = []
            #     for x in listcsvpull:
            #         pcsv = path + tickerlist[0] + "short" + "Sep" + x + str(listdf[chartinterval]) + ".csv"
            #         dfp = pd.read_csv(pcsv)
            #         dfindicators.append(dfp)
            #
            #     dfrsi = dfindicators[0]
            #     dfbb = dfindicators[1]
            #     dfrsimacd = dfindicators[2]
            #     dfmaratio = dfindicators[3]
            #     dfmarsi = dfindicators[4]
            #     inds = {0: [dfrsi, "rsip"], 1: [dfbb, "bbp"], 2: [dfrsimacd, "rsimacdp"], 3: [dfmaratio, "maratiop"],
            #             4: [dfmarsi, "marsip"]}
            #
            #     for x in range(len(inds)):
            #         inddf = inds[x][0]
            #         ind=x
            #         indvalues=[]
            #
            #         for y in values:
            #
            #
            #             inddf1 = inddf[inddf["Value Change"]==y]
            #             inddf1= inddf1[inddf1["Probability Up"]!=0]
            #             inddf1 = inddf1[inddf1["Probability Down"] != 0]
            #             nvalue=inddf1["Nvalue"]
            #             probu=inddf1["Probability Up"]
            #             probd = inddf1["Probability Down"]
            #             inddf1["Enough Values"] = 0
            #             inddf1["Good Probability Up"] = 0
            #             inddf1["Good Probability Down"] = 0
            #             if y==2 or 1.5:
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Enough Values"]=inddf1.loc[inddf1.index[x],"Nvalue"]>=10
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Good Probability Up"]=inddf1.loc[inddf1.index[x],"Probability Up"]>=float((probu.quantile([q1])))
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Good Probability Down"]=inddf1.loc[inddf1.index[x],"Probability Down"]>=float((probd.quantile([q1])))
            #             elif y==3 or 2.5:
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Enough Values"]=inddf1.loc[inddf1.index[x],"Nvalue"]>=6
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Good Probability Up"]=inddf1.loc[inddf1.index[x],"Probability Up"]>=float((probu.quantile([q2]))) and inddf1.loc[inddf1.index[x],"Probability Up"]>=inddf1.loc[inddf1.index[x],"Probability Down"]
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Good Probability Down"]=inddf1.loc[inddf1.index[x],"Probability Down"]>=float((probd.quantile([q2]))) and inddf1.loc[inddf1.index[x],"Probability Down"]>=inddf1.loc[inddf1.index[x],"Probability Up"]
            #             elif y==1.25 or 1 or 0.75 or 0.5:
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Enough Values"]=inddf1.loc[inddf1.index[x],"Nvalue"]>=10
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Good Probability Up"]=inddf1.loc[inddf1.index[x],"Probability Up"]>=float((probu.quantile([q3])))
            #                 for x in range(len(inddf1)):
            #                     inddf1.loc[inddf1.index[x],"Good Probability Down"]=inddf1.loc[inddf1.index[x],"Probability Down"]>=float((probd.quantile([q3])))
            #
            #
            #             else:
            #                 pass
            #
            #
            #
            #             indvalues.append(inddf1)
            #             df1 = pd.concat(indvalues)
            #             if y==0.5:
            #
            #                 df1.to_csv(path + tickerlist[0] + "short" + inds[ind][1] + str(listdf[chartinterval]) + ".csv",index=False)
            #             else:
            #                 pass








print("--- %s seconds ---" % (time.time() - start_time))
