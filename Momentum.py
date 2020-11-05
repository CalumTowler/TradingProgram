

import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta
from statistics import mean

import time
import math
import itertools
path = r'D:\OneDrive\Oracle\Trading Program\Stock Data\New Analysis'
tickerlist={0:"\TVC_USOIL, ",1:r'\NASDAQ_MSFT, ',2:r"\NASDAQ_AAPL, ",3:"\SPCFD_S5INFT, ",4:"\SPCFD_SPX, ",5:"\TVC_NDX, "}
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'}

pd.set_option('display.max_rows', 700)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
def dffix(list,x,tp,ticker,path,dropcols=None):
    print(dropcols)

    excel1 = path + ticker + str(list[x])  + ".csv"
    df = pd.read_csv(excel1)
    #print('Chart Interval is '+(str(list[x])))
    # puts column headers in
    df.columns = ['time','open','high','low','close','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
                  'Volume','VMA','RSI','Histogram','MACD','Signal','Aroon Up','Aroon Down',"MOM2 LAG", "Plot", "MOM2 LEAD"]
    for x in dropcols:
        df = df.drop(columns=[x])
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

def priceprob(df,nb,valuechange): #this function calculates whether the value at each point increases by the "valuechange" in nb points


    for x in range((len(df.index) - nb)):  # this itterates over every row in the dataframe except the top rows where forward data is not available
        cprice = fval(df, 'close', x)  # current close price
        currentday=fval(df,"timedate",x)
        p1list = []  # list of probabilities for range of forward bars
        p2list = []  # this list is for probabilities if the value change is both up and down by the required amount i.e. moves 1% up and 1% down in net 3 hours
        y=(x-nb) #point in future
        dfexam=(df[df["timedate"] == currentday])
        intlist=(dfexam.index)


        if x==int(intlist[0]):
            y=int(int(intlist[0]))
            x=int(int(intlist[1]))
        elif y<int(intlist[0]):
            y=int(intlist[0])
        else:
            pass



        npriceddf=(dfexam.loc[df.index[y:x],'low'])
        npriced= npriceddf.min() #finds lowest value between now and future

        npriceudf =(dfexam.loc[df.index[y:x],'high'])
        npriceu = npriceudf.max() #finds highest value

        d = cprice-npriced # different between forward price and current price being examined
        u = npriceu - cprice
        percent = (cprice / 100) * valuechange #looks for values where change is equal to or greater than desired value change
        if len(npriceddf)>(nb-4):
            if u > percent and d > percent:  # for conditions where both up and down value changes occur
                p1 = 1
                p2 = -1
            else:
                p2 = 0
                if d > percent:  # down by value occurs
                    p1 = -1

                elif u > percent:  # up by value occurs
                    p1 = 1

                else:
                    p1 = 0
            p1list.append(p1)  # list of values
            p2list.append(p2)

            pu1 = [x for x in p1list if x > 0]  # list of positive value moves
            pd1 = [x for x in p1list if x < 0]  # lsit of neg value moves
            pd2 = [x for x in p2list if x < 0]  # list of neg value moves if both neg and pos occur
            if len(pd2) > 0:  # if both up and down occur in time period then 2 probabilities are entered
                p11 = -1
                p22 = 1
            else:
                p22 = 0  # if only one value change occurs
                if len(
                        pu1) > 0:
                    p11 = 1

                elif len(pd1) > 0:
                    p11 = -1

                else:
                    p11 = 0
            df.loc[df.index[x], 'p1'] = p11  # assign these values to df column
            df.loc[df.index[x], 'p2'] = p22
        else:
            df.loc[df.index[x], 'p1'] = 2
    return(df)

def seperatevar(ticker,chartinterval):

    chartintervals=[2,3,4,6]


    for chartinterval in chartintervals:

        rsigradnum = {1: 20, 2: 8, 3: 6, 4: 6, 5: 5,6: 5}  # list of range of vlaues to calucalte RSI gradient over
        rsigradn = rsigradnum[chartinterval]
        df = dffix(listdf, chartinterval, 0, ticker, path,dropcols=["Aroon Up", "Aroon Down", "Plot", "Histogram", "MACD", "Signal", "Basis", "Upper", "Lower","VWMA"])

        if chartinterval>4:
            pass
        else:
            df['hour'] = pd.to_datetime(df['time'], format='%H:%M').dt.hour
            df['minute'] = df['time'].dt.strftime('%M')

        if chartinterval < 4:
            dffib = dffix(listdf, 6, 0, ticker, path)  # dataframe used for fibonacci retracement (day chart for 1,5,15 min and week for hour, 4hr and day)
        else:
            dffib = dffix(listdf, 7, 0, ticker, path)

        for x in range(len(dffib)):
            dffib.loc[dffib.index[x], "timedate"] = (dffib.loc[dffib.index[x], "time"].date())  # makes date only time column for fibonacci calcs

        df["MOM2 Histogram"]=df["MOM2 LEAD"]-df["MOM2 LAG"]
        df["RSI Gradient"]=0
        df["MOM2 Lead Gradient"]=0
        df["MOM2 Histogram Gradient"]=0
        for x in range(len(df)):
            if fval(df,"hour",x)==9 and fval(df,"minute",x)==30 or fval(df,"minute",x)==35 or fval(df,"minute",x)==40 and chartinterval == 2:
                df = df.drop(df.index[x])
            else:
                pass
        df = df.reset_index(drop=True)
        for x in range(len(df)-rsigradn):

            df.loc[df.index[x], "timedate"] = (df.loc[df.index[x], "time"].date())
            df.loc[df.index[x], "MOM2 Histogram Gradient"] = (fval(df, "MOM2 Histogram", x) - fval(df, "MOM2 Histogram",x + 2)) / 3
            df.loc[df.index[x], "MOM2 Lead Gradient"] = (fval(df, "MOM2 Lead", x) - fval(df, "MOM2 Lead",x + 2)) / 3

            df.loc[df.index[x], 'RSI Gradient'] = (df.loc[df.index[x], 'RSI'] - df.loc[df.index[x + rsigradn], 'RSI']) / rsigradn

            df.loc[df.index[x], "25 MA Spread"] = ((fval(df, 'close', x) - fval(df, "25MA", x)) / fval(df, 'close',x)) * 100
            df.loc[df.index[x], "50 MA Spread"] = ((fval(df, 'close', x) - fval(df, "50MA", x)) / fval(df, 'close',x)) * 100
            df.loc[df.index[x], "100 MA Spread"] = ((fval(df, 'close', x) - fval(df, "100MA", x)) / fval(df, 'close',x)) * 100

            currentdate = df.loc[df.index[x], "timedate"]
            day = datetime.weekday(currentdate)
            if day != 6 and chartinterval == 2:
                week = currentdate - Timedelta(days=(8 + day))
                for t in range(len(dffib)):
                    if dffib.loc[dffib.index[t], "timedate"] == week:
                        day = t
                        break
                    else:
                        pass

                high = fval(dffib, 'high', day)
                low = fval(dffib, 'low', day)
                close = fval(dffib, 'close', day)
                pp = round((high + low + close) / 3, 2)
                flevels = [0.382, 0.618, 1.0]
                SF = []
                RF = []
                for z in flevels:
                    rf = round((pp + ((high - low) * z)), 2)
                    RF.append(rf)

                    sf = round((pp - ((high - low) * z)), 2)
                    SF.append(sf)

                df.loc[df.index[x], "Support Fib 1"] = SF[0]
                df.loc[df.index[x], "Resistance Fib 1"] = RF[0]
                df.loc[df.index[x], "Support Fib 2"] = SF[1]
                df.loc[df.index[x], "Resistance Fib 2"] = RF[1]
                df.loc[df.index[x], "Support Fib 3"] = SF[2]
                df.loc[df.index[x], "Resistance Fib 3"] = RF[2]
                df.loc[df.index[x], "P Fib"] = pp

            elif day != 6 and chartinterval == 4:
                currentdate = df.loc[df.index[x], "timedate"]
                priorday = currentdate - Timedelta(days=1)
                for y in range(len(dffib)):
                    if dffib.loc[dffib.index[y], "timedate"] == priorday:
                        day = y
                        break
                    else:
                        pass
                high = fval(dffib, 'high', day)
                low = fval(dffib, 'low', day)
                close = fval(dffib, 'close', day)
                pp = round((high + low + close) / 3, 2)
                flevels = [0.382, 0.618, 1.0]
                SF = []
                RF = []
                for z in flevels:
                    rf = round((pp + ((high - low) * z)), 2)
                    RF.append(rf)

                    sf = round((pp - ((high - low) * z)), 2)
                    SF.append(sf)

                df.loc[df.index[x], "Support Fib 1"] = SF[0]
                df.loc[df.index[x], "Resistance Fib 1"] = RF[0]
                df.loc[df.index[x], "Support Fib 2"] = SF[1]
                df.loc[df.index[x], "Resistance Fib 2"] = RF[1]
                df.loc[df.index[x], "Support Fib 3"] = SF[2]
                df.loc[df.index[x], "Resistance Fib 3"] = RF[2]
                df.loc[df.index[x], "P Fib"] = pp

            else:
                pass

            RFIBList=["Resistance Fib 1", "Resistance Fib 2", "Resistance Fib 3"]
            FSUPList=[ "Support Fib 1"]

            cprice = fval(df, "close", x)
            ten = float(round(cprice, -1))  # founds rounded multiple of 10
            one = float(round(cprice))

            if one > cprice:
                if one == ten:
                    df.loc[df.index[x], "First Whole Resistance"] = one + 1
                    df.loc[df.index[x], "Second Whole Resistance"] = (one + 2)
                    df.loc[df.index[x], "First Whole Support"] = (one - 1)
                    df.loc[df.index[x], "Second Whole Support"] = (one - 2)
                elif one == (ten - 1):
                    df.loc[df.index[x], "First Whole Resistance"] = one
                    df.loc[df.index[x], "Second Whole Resistance"] = one + 2
                    df.loc[df.index[x], "First Whole Support"] = (one - 1)
                    df.loc[df.index[x], "Second Whole Support"] = (one - 2)
                elif one == (ten + 1):
                    df.loc[df.index[x], "First Whole Resistance"] = one
                    df.loc[df.index[x], "Second Whole Resistance"] = one + 1
                    df.loc[df.index[x], "First Whole Support"] = (one - 2)
                    df.loc[df.index[x], "Second Whole Support"] = (one - 3)

                df.loc[df.index[x], "First Half Resistance"] = (one + 0.5)
                df.loc[df.index[x], "First Half Support"] = (one - 0.5)
                df.loc[df.index[x], "Second Half Resistance"] = (one + 1.5)
                df.loc[df.index[x], "Second Half Support"] = (one - 1.5)

            elif one <= cprice:
                if one == ten:
                    df.loc[df.index[x], "First Whole Support"] = one - 1
                    df.loc[df.index[x], "Second Whole Support"] = (one - 2)
                    df.loc[df.index[x], "First Whole Resistance"] = one + 1
                    df.loc[df.index[x], "Second Whole Resistance"] = (one + 2)
                elif one == (ten - 1):
                    df.loc[df.index[x], "First Whole Support"] = one
                    df.loc[df.index[x], "Second Whole Support"] = one - 1
                    df.loc[df.index[x], "First Whole Resistance"] = one + 2
                    df.loc[df.index[x], "Second Whole Resistance"] = (one + 3)
                elif one == (ten + 1):
                    df.loc[df.index[x], "First Whole Support"] = one
                    df.loc[df.index[x], "Second Whole Support"] = one - 2
                    df.loc[df.index[x], "First Whole Resistance"] = one + 1
                    df.loc[df.index[x], "Second Whole Resistance"] = (one + 2)

                df.loc[df.index[x], "First Half Resistance"] = (one + 0.5)
                df.loc[df.index[x], "First Half Support"] = (one - 0.5)
                df.loc[df.index[x], "Second Half Resistance"] = (one + 1.5)
                df.loc[df.index[x], "Second Half Support"] = (one - 1.5)

            else:
                pass

            if ten > cprice:
                df.loc[df.index[x], "Ten Resistance"] = ten
                df.loc[df.index[x], "Ten Support"] = (ten - 10)
                df.loc[df.index[x], "Five Resistance"] = (ten + 5)
                df.loc[df.index[x], "Five Support"] = (ten - 5)
            elif ten < cprice:
                df.loc[df.index[x], "Ten Support"] = ten
                df.loc[df.index[x], "Ten Resistance"] = (ten + 10)
                df.loc[df.index[x], "Five Resistance"] = (ten + 5)
                df.loc[df.index[x], "Five Support"] = (ten - 5)
            else:
                df.loc[df.index[x], "Ten Support"] = ten
                df.loc[df.index[x], "Ten Resistance"] = (ten + 10)
                df.loc[df.index[x], "Five Resistance"] = (ten + 5)
                df.loc[df.index[x], "Five Support"] = (ten - 5)
            Resistancelist = ["First Whole Resistance", "Second Whole Resistance", "Ten Resistance", "Five Resistance"]
            Supportlist = ["First Whole Support", "Second Whole Support", "Ten Support", "Five Support"]

        for x in range(len(df) - 2):


            if df.loc[df.index[x], "Volume"] > df.loc[df.index[x], "VMA"]:
                df.loc[df.index[x], "Relative Volume"] = "High Volume"
            else:
                df.loc[df.index[x], "Relative Volume"] = "Low Volume"
            RSbreak = []
            open = fval(df, "open", x)
            close = fval(df, "close", x)
            low = fval(df, "low", x)
            high = fval(df, "high", x)

            # breaksthough resistance
            # make if both whole support and ten/five resistance is the same to assign the value to ten and
            if chartinterval = 2:
                for resistance in Resistancelist:
                    if open <= df.loc[df.index[x + 1], resistance] and close > df.loc[df.index[x + 1], resistance]:
                        RSbreak.append(1)
                    else:
                        RSbreak.append(0)
                for support in Supportlist:
                    if open >= df.loc[df.index[x + 1], support] and close < df.loc[df.index[x + 1], support]:
                        RSbreak.append(1)

                    else:
                        RSbreak.append(0)
                for fibsupport in FibResis


            else:
                pass
            RSbreak = str(tuple(RSbreak))
            df.loc[df.index[x], "RS Break"] = RSbreak



    return df



def houradder():
    df=seperatevar(tickerlist[3],2)
    df15=seperatevar(tickerlist[3],3)

    for x in range(len(df)-5):
        currentdate=fval(df,'timedate',x)
        currenthour=int(fval(df,'hour',x))
        currentminute=int(fval(df,'minute',x))
        df15current=df15[df15["timedate"]==currentdate]
        df15current = df15current.reset_index(drop=True)
        for y in range(len(df15current)):
            m15time = int(fval(df15, 'minute', y))
            m15hour = int(fval(df15, 'hour', y))

            if currentminute<15 and currenthour==(m15hour+1) and m15time==45:
                df.loc[df.index[x], 'm15rsi']=fval(df15current, 'RSI', y)

                df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
                df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
                break
            elif 14<currentminute<30 and currenthour==(m15hour) and m15time ==0:
                df.loc[df.index[x], 'm15rsi'] = fval(df15current, 'RSI', y)

                df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
                df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
                break

            elif 29<currentminute<45 and currenthour==(m15hour) and m15time ==15:
                df.loc[df.index[x], 'm15rsi'] = fval(df15current, 'RSI', y)

                df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
                df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
                break

            elif 44<currentminute and currenthour==(m15hour) and m15time ==30:
                df.loc[df.index[x], 'm15rsi'] = fval(df15current, 'RSI', y)

                df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
                df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
                break

            else:
                pass




    df.to_csv(path + tickerlist[3] + "15added" + "momentum" + ".csv", index=False)

    return



def timeremover(prob, chartinterval):
    timestodrop = []
    if 3 > len(prob) > 1:
        for k in range(1, len(prob)):
            timenow = prob.loc[prob.index[k], 'time']
            timeminus = prob.loc[prob.index[k - 1], 'time']

            timedelta = timeminus - timenow

            timeclose = (pd.Timedelta("0 days" + (str(listdf[chartinterval]) + " min")))
            if timedelta == timeclose:
                timestodrop.append(k - 1)

            else:
                pass
        prob = prob.drop(prob.index[timestodrop])
    elif len(prob) > 2:

        for k in range(2, len(prob)):
            timenow = prob.loc[prob.index[k], 'time']
            timeminus = prob.loc[prob.index[k - 1], 'time']
            timeplus = prob.loc[prob.index[k - 2], 'time']
            timedelta = timeminus - timenow
            timedelta2 = timeplus - timenow

            timeclose = (pd.Timedelta("0 days" + (str(listdf[chartinterval]) + " min")))
            timeclose2 = (pd.Timedelta("0 days" + (str(2 * (listdf[chartinterval])) + " min")))
            if timedelta == timeclose or timedelta == timeclose2:
                timestodrop.append(k - 1)
            elif timedelta == timeclose2:
                timestodrop.append(k - 2)

            else:
                pass
        prob = prob.drop(prob.index[timestodrop])

    else:
        pass

    return prob, timestodrop




def probanalyser(tp,value):


    df15=pd.read_csv((path + tickerlist[3] + str(listdf[3]) + "momentum" + ".csv"))
    df15.columns = ['time', 'open', 'high', 'low', 'close', 'VWMA', '25MA', '50MA', '100MA', '200MA', 'Basis', 'Upper',
                  'Lower',
                  'Volume', 'VMA', 'RSI', 'Histogram', 'MACD', 'Signal', '%K', '%D', 'Aroon Up', 'Aroon Down', 'MOM',
                  'MOMHistogram'
        , 'MOMMACD', 'MOMSignal', "MOM2 LAG", "MOM2 LEAD","hour", 'minute', "MOM2 Histogram", "MOM2 Cross", "MOM2 Cross Gradient", "MOM2 Histogram Gradient","timedate"]
    df15['time'] = pd.to_datetime(df15['time'])

    df=pd.read_csv(path + tickerlist[3] + "15added" + "momentum" + ".csv")
    df.columns = ['time', 'open', 'high', 'low', 'close', 'VWMA', '25MA', '50MA', '100MA', '200MA', 'Basis', 'Upper',
                  'Lower',
                  'Volume', 'VMA', 'RSI', 'Histogram', 'MACD', 'Signal', '%K', '%D', 'Aroon Up', 'Aroon Down', 'MOM',
                  'MOMHistogram'
        , 'MOMMACD', 'MOMSignal', "MOM2 LAG", "MOM2 LEAD","hour", 'minute', "MOM2 Histogram", "MOM2 Cross", "MOM2 Cross Gradient", "MOM2 Histogram Gradient","timedate", "m15rsi", 'm15 MOM2LEAD', 'm15 MOM2 Histogram Gradient']
    df['time'] = pd.to_datetime(df['time'])  # changes time column format to datetime

    df=priceprob(df,tp,value)

    dfpos = df[df["MOM2 LEAD"] > 0]
    positivelead = []
    listq = [0.05, 0.3, 0.7, 0.95]
    for q in listq:
        positivelead.append(float((dfpos["MOM2 LEAD"].quantile([q]))))

    dfneg = df[df["MOM2 LEAD"] < 0]
    negativelead = []
    listq = [0.05, 0.3, 0.7, 0.95]
    for q in listq:
        negativelead.append(float((dfneg["MOM2 LEAD"].quantile([q]))))

    dfpos = df[df["MOM2 Histogram Gradient"] > 0]
    positivehist = []
    listq = [0.05, 0.3, 0.7, 0.95]
    for q in listq:
        positivehist.append(float((dfpos["MOM2 Histogram Gradient"].quantile([q]))))

    dfneg = df[df["MOM2 Histogram Gradient"] < 0]
    negativehist = []
    listq = [0.05, 0.3, 0.7, 0.95]
    for q in listq:
        negativehist.append(float((dfneg["MOM2 Histogram Gradient"].quantile([q]))))

    lead = negativelead + positivelead
    hist = negativehist + positivehist

    dfpos = df15[df15["MOM2 LEAD"] > 0]
    positiveleaddf15 = []
    listq = [0.05, 0.3, 0.7, 0.95]
    for q in listq:
        positiveleaddf15.append(float((dfpos["MOM2 LEAD"].quantile([q]))))

    dfneg = df15[df15["MOM2 LEAD"] < 0]
    negativeleaddf15 = []
    listq = [0.05, 0.3, 0.7, 0.95]
    for q in listq:
        negativeleaddf15.append(float((dfneg["MOM2 LEAD"].quantile([q]))))

    dfpos = df15[df15["MOM2 Histogram Gradient"] > 0]
    positivehistdf15 = []
    listq = [0.05, 0.3, 0.7, 0.95]
    for q in listq:
        positivehistdf15.append(float((dfpos["MOM2 Histogram Gradient"].quantile([q]))))

    dfneg = df15[df15["MOM2 Histogram Gradient"] < 0]
    negativehistdf15 = []
    listq = [0.05, 0.3, 0.7, 0.95]
    for q in listq:
        negativehistdf15.append(float((dfneg["MOM2 Histogram Gradient"].quantile([q]))))

    leaddf15 = negativeleaddf15 + positiveleaddf15
    histdf15 = negativehistdf15 + positivehistdf15





    rsilist = [0, 20,30, 50, 70, 80,100]
    probu = []
    probd = []
    nval = []
    nvalup = []
    nvaldown = []
    min5RSI=[]
    m15RSI=[]
    m15MOM2LEAD=[]
    m15MOM2Hist=[]
    min5MOM2LEAD=[]
    min5MOM2Hist=[]
    probdiff=[]
    df=df[df["p1"]!=2]

    for k in range(len(leaddf15)-1):
        dfprobs5 = df[(df['m15 MOM2LEAD'] >= leaddf15[k]) & (df['m15 MOM2LEAD'] < leaddf15[k + 1])]
        for i in range(len(histdf15)-1):
            dfprobs4 = dfprobs5[(dfprobs5['m15 MOM2 Histogram Gradient'] >= histdf15[i]) & (dfprobs5['m15 MOM2 Histogram Gradient'] < histdf15[i + 1])]
            for h in range(len(lead)-1):
                dfprobs3= dfprobs4[(dfprobs4['MOM2 LEAD'] >= lead[h]) & (dfprobs4['MOM2 LEAD'] < lead[h + 1])]
                for j in range(len(hist) - 1):
                    dfprobs2 = dfprobs3[(dfprobs3['MOM2 Histogram Gradient'] >= hist[j]) & (dfprobs3['MOM2 Histogram Gradient'] < hist[j + 1])]
                    for q in range(len(rsilist) - 1):
                        dfprobs1 = dfprobs2[(dfprobs2['m15rsi'] >= rsilist[q]) & (dfprobs2['m15rsi'] < rsilist[q + 1])]
                        for b in range(len(rsilist) - 1):  # then sorts by rsi value
                            dfprobs = dfprobs1[(dfprobs1['RSI'] >= rsilist[b]) & (dfprobs1['RSI'] < rsilist[b + 1])]
                            dfprobs = dfprobs.reset_index(drop=True)
                            if len(dfprobs)>1:
                                dfup1 = dfprobs[dfprobs["p1"]>0]
                                dfup1list=timeremover(dfup1,2)
                                up1len=len(dfup1list[0])

                                dfup2=dfprobs[dfprobs["p2"]>0]
                                dfup2list=timeremover(dfup2,2)
                                up2len = len(dfup2list[0])

                                dfdo1=dfprobs[dfprobs["p1"]<0]
                                dfdo1list=timeremover(dfdo1,2)
                                do1len = len(dfdo1list[0])

                                probup=(up1len + up2len)/(len(dfprobs)-(len(dfup1list[1])+len(dfup2list[1])))
                                probdown=do1len/(len(dfprobs)-len(dfdo1list[1]))
                                probu.append(probup)
                                probd.append(probdown)
                                min5RSI.append((str(rsilist[b])+" - "+str(rsilist[b+1])))
                                m15RSI.append((str(rsilist[q])+" - "+str(rsilist[q+1])))
                                m15MOM2LEAD.append((str(leaddf15[k]) + " : " + str(leaddf15[k+1])))
                                m15MOM2Hist.append((str(histdf15[i]) + " : " + str(histdf15[i+1])))
                                min5MOM2LEAD.append((str(lead[h]) + " : " +str(lead[h+1])))
                                min5MOM2Hist.append((str(hist[j]) + " : " + str(hist[j+1])))
                                nvalup.append(up1len + up2len)
                                nvaldown.append(do1len)
                                probdiff.append(probup-probdown)
                                nval.append(len(dfprobs)-(len(dfup1list[1])+len(dfdo1list[1])))

                                continue
                            else:
                                continue


    probs = pd.DataFrame(
        {'5 Min RSI': [], '15 Min RSI': [], '15 Min MOM2LEAD' : [], '15 Min MOM2Histogram' : [], 'Min MOM2LEAD' : [], 'Min MOM2Histogram' : [],
         'Probability Up': [], 'Probability Down': [], "Probability Difference":[], 'Nvalue': [], 'Nvalue Up': [],
         'Nvalue Down': []})  # makes df of probabilities at rsi ranges
    probs['5 Min RSI'] = min5RSI
    probs['15 Min RSI'] = m15RSI
    probs['15 Min MOM2LEAD'] = m15MOM2LEAD
    probs['15 Min MOM2Histogram'] = m15MOM2Hist
    probs['Min MOM2LEAD'] = min5MOM2LEAD
    probs['Min MOM2Histogram'] = min5MOM2Hist


    probs['Probability Up'] = probu
    probs['Probability Down'] = probd
    probs['Nvalue'] = nval
    probs["Nvalue Up"] = nvalup
    probs["Nvalue Down"] = nvaldown
    probs["Probability Difference"] = probdiff



    probs.to_csv(path + "short" + "momentum" + str(tp) + str(value)+ ".csv", index=False)

    return

# listvalues=[[8,0.4],[12,0.7],[16,1]]
#
# for x in listvalues:
#     probanalyser(x[0],x[1])

def compare():

    df = pd.read_csv((path + tickerlist[3] + str(listdf[2]) + " use" + ".csv"))
    df.columns = ['time', 'open', 'high', 'low', 'close', 'VWMA', '25MA', '50MA', '100MA', '200MA', 'Basis', 'Upper','Lower',
                  'Volume', 'VMA', 'RSI', 'Histogram', 'MACD', 'Signal', '%K', '%D', 'Aroon Up', 'Aroon Down', 'MOM',
                  'MOMHistogram' , 'MOMMACD', 'MOMSignal', "MOM2 LAG", "MOM2 LEAD"]
    df['time'] = pd.to_datetime(df['time'])
    df = df.iloc[::-1]  # revereses index
    df = df.reset_index(drop=True)  # reset so newest data is at index 0
      # if 0 is selected as start then removing rows will be skipped
    df = df.drop(df.index[468:])  # drops range of rows not wanted to make new df starting from point selected
    df = df.reset_index(drop=True)
    df['hour'] = (df['time']).dt.hour
    df['minute'] = df['time'].dt.strftime('%M')
    df["MOM2 Histogram"] = df["MOM2 LEAD"] - df["MOM2 LAG"]
    df["MOM2 Histogram Gradient"] = 0


    for x in range(len(df) - 3):
        df.loc[df.index[x], "MOM2 Histogram Gradient"] = (fval(df, "MOM2 Histogram", x) - fval(df, "MOM2 Histogram",
                                                                                           x + 2)) / 3
        df.loc[df.index[x], "timedate"] = (df.loc[df.index[x], "time"].date())

    df15 = pd.read_csv((path + tickerlist[3] + str(listdf[4])  + " use" +".csv"))
    df15.columns = ['time', 'open', 'high', 'low', 'close', 'VWMA', '25MA', '50MA', '100MA', '200MA', 'Basis', 'Upper',
                  'Lower',
                  'Volume', 'VMA', 'RSI', 'Histogram', 'MACD', 'Signal', '%K', '%D', 'Aroon Up', 'Aroon Down', 'MOM',
                  'MOMHistogram', 'MOMMACD', 'MOMSignal', "MOM2 LAG", "MOM2 LEAD"]
    df15['time'] = pd.to_datetime(df15['time'])
    df15 = df15.iloc[::-1]  # revereses index
    df15 = df15.reset_index(drop=True)  # reset so newest data is at index 0
    # if 0 is selected as start then removing rows will be skipped
    df15 = df15.drop(df15.index[200:])  # drops range of rows not wanted to make new df60 starting from point selected
    df15 = df15.reset_index(drop=True)
    df15['hour'] = (df15['time']).dt.hour

    df15['minute'] = df15['time'].dt.strftime('%M')
    df15["MOM2 Histogram"] = df15["MOM2 LEAD"] - df15["MOM2 LAG"]
    df15["MOM2 Histogram Gradient"] = 0



    for x in range(len(df15) - 3):
        df15.loc[df15.index[x], "MOM2 Histogram Gradient"] = (fval(df15, "MOM2 Histogram", x) - fval(df15, "MOM2 Histogram",
                                                                                               x + 2)) / 3
        df15.loc[df15.index[x], "timedate"] = (df15.loc[df.index[x], "time"].date())

    for x in range(len(df) - 5):
        currentdate = fval(df, 'timedate', x)
        currenthour = int(fval(df, 'hour', x))
        currentminute = int(fval(df, 'minute', x))
        df15current = df15[df15["timedate"] == currentdate]
        df15current = df15current.reset_index(drop=True)
        for y in range(len(df15current)):
            m15time = int(fval(df15, 'minute', y))
            m15hour = int(fval(df15, 'hour', y))

            if currenthour ==(m15hour+1):
                df.loc[df.index[x], 'm15rsi'] = fval(df15current, 'RSI', y)
                df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
                df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
                break
            else:
                pass

            # if currentminute < 15 and currenthour == (m15hour + 1) and m15time == 45:
            #     df.loc[df.index[x], 'm15rsi'] = fval(df15current, 'RSI', y)
            #
            #     df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
            #     df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
            #     break
            # elif 14 < currentminute < 30 and currenthour == (m15hour) and m15time == 0:
            #     df.loc[df.index[x], 'm15rsi'] = fval(df15current, 'RSI', y)
            #
            #     df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
            #     df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
            #     break
            #
            # elif 29 < currentminute < 45 and currenthour == (m15hour) and m15time == 15:
            #     df.loc[df.index[x], 'm15rsi'] = fval(df15current, 'RSI', y)
            #
            #     df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
            #     df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
            #     break
            #
            # elif 44 < currentminute and currenthour == (m15hour) and m15time == 30:
            #     df.loc[df.index[x], 'm15rsi'] = fval(df15current, 'RSI', y)
            #
            #     df.loc[df.index[x], 'm15 MOM2LEAD'] = fval(df15current, 'MOM2 LEAD', y)
            #     df.loc[df.index[x], 'm15 MOM2 Histogram Gradient'] = fval(df15current, 'MOM2 Histogram Gradient', y)
            #     break
            #
            # else:
            #     pass

    path2 = r'D:\OneDrive\Oracle\Trading Program\Stock Data\Probability Results'
    df804=pd.read_csv(path2 + r"\current dayshortmomentum" + "80.4 hour" + ".csv")
    df1207=pd.read_csv(path2 + r"\current dayshortmomentum" + "120.7 hour" + ".csv")
    df161 = pd.read_csv(path2 + r"\current dayshortmomentum" + "161 hour" + ".csv")
    dflist=[df804,df1207,df161]

    for dfs in dflist:



        dfs.columns = ["5 Min RSI", "15 Min RSI", "15 Min MOM2LEAD", "15 Min MOM2Histogram", "Min MOM2LEAD",
                           "Min MOM2Histogram", "Probability Up", "Probability Down", "Probability Difference",
                           "Nvalue",
                           "Nvalue Up", "Nvalue Down"]

    rsilist = [0, 20, 30, 50, 70, 80, 100]
    # m15mom2leadlist = [-33.826459822, -12.051567574000002, -3.0914118569, -0.43391146435000005, 0.61020714275,
    #                    3.7496264285, 10.86615857, 26.755033575]
    # m15mom2histolist = [-1.5873991666666658, -0.5668340473333341, -0.17104547599999995, -0.02464321416666667,
    #                     0.02765620351666663, 0.1658073570000002, 0.5377366207666668, 1.5153366550666667]

    m15mom2leadlist = [-54.899753356000005, -18.915704214999998,-5.783795357000001, -0.8428125360000004,1.1448153567500001,7.0448980712000004,18.395932289,41.181286926 ]
    m15mom2histolist= [-2.603473573133333, -0.885222190933334, -0.2800862384000008, -0.05000247560000011, 0.046099881200000165,0.273493478, 0.8856727631000013,2.4437043494999973]
    minmom2leadlist = [-20.52251, -6.6333335710000005, -1.651266429, -0.248025, 0.29513032140000006, 1.8868959286999996,
                       6.1706808569, 17.947602963999998]
    minmom2histolist = [-1.0470922393500002, -0.3325977151666668, -0.0132719760333333, -0.09231878579999996,
                        0.09402076193333328, 0.014120226033333273, 0.3336800234999999, 1.0542217258666657]

    probabilities=[]
    timesdown=[]
    timesup=[]
    for x in range(len(df) - 5):
        dfprobs=dflist[0]

        time=(fval(df,"time",x))
        rsi5=fval(df,"RSI",x)
        rsi15=fval(df,"m15rsi",x)
        mom2lead5=fval(df,"MOM2 LEAD",x)
        mom2lead15 = fval(df, "m15 MOM2LEAD", x)
        mom2hist5=fval(df,"MOM2 Histogram Gradient",x)
        mom2hist15=fval(df,"m15 MOM2 Histogram Gradient",x)


        for rsi in range(len(rsilist) - 1):
            if rsilist[rsi] <= rsi5 < rsilist[rsi + 1]:
                rsirange5 = (str(rsilist[rsi]) + " - " + str(rsilist[rsi + 1]))
            else:
                pass

        for rsi in range(len(rsilist) - 1):
            if rsilist[rsi] <= rsi15 < rsilist[rsi + 1]:
                rsirange15 = (str(rsilist[rsi]) + " - " + str(rsilist[rsi + 1]))

            else:
                pass

        for mom2lead in range(len(m15mom2leadlist) - 1):
            if m15mom2leadlist[mom2lead] <= mom2lead15 < m15mom2leadlist[mom2lead + 1]:
                mom2leadrange15 = (str(m15mom2leadlist[mom2lead]) + " : " + str(m15mom2leadlist[mom2lead + 1]))
            else:
                pass

        for mom2hist in range(len(m15mom2histolist) - 1):
            if m15mom2histolist[mom2hist] <= mom2hist15 < m15mom2histolist[mom2hist + 1]:
                mom2histrange15 = (str(m15mom2histolist[mom2hist]) + " : " + str(m15mom2histolist[mom2hist + 1]))

            else:
                pass
        for mom2lead in range(len(minmom2leadlist) - 1):
            if minmom2leadlist[mom2lead] <= mom2lead5 < minmom2leadlist[mom2lead + 1]:
                mom2leadrange5 = (str(minmom2leadlist[mom2lead]) + " : " + str(minmom2leadlist[mom2lead + 1]))
            else:
                pass

        for mom2hist in range(len(minmom2histolist) - 1):
            if minmom2histolist[mom2hist] <= mom2hist5 < minmom2histolist[mom2hist + 1]:
                mom2histrange5 = (str(minmom2histolist[mom2hist]) + " : " + str(minmom2histolist[mom2hist + 1]))
            else:
                continue











            dfmatch=dfprobs[(dfprobs["5 Min RSI"]==rsirange5) & (dfprobs["15 Min RSI"]==rsirange15) & (dfprobs["15 Min MOM2LEAD"]==mom2leadrange15) & (dfprobs["15 Min MOM2Histogram"]==mom2histrange15) &
                        (dfprobs["Min MOM2LEAD"]==mom2leadrange5) & (dfprobs["Min MOM2Histogram"]==mom2histrange5)]

            if len(dfmatch)>0 and float(fval(dfmatch,"Probability Down",0))>0.7 and float(fval(dfmatch,"Probability Difference",0))<-0.5 :
                timesdown.append(time)
            elif len(dfmatch)>0 and float(fval(dfmatch,"Probability Up",0))>0.7 and float(fval(dfmatch,"Probability Difference",0))>0.5 :
                timesup.append(time)
            else:
                pass



    print(timesdown)
    print(timesup)
    return

compare()
