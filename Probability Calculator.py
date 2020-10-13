





import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta
import time
from pandas import Timedelta
import math
import itertools


# path=r"C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data\current day"
path = r'D:\OneDrive\Oracle\Trading Program\Stock Data\current day'
path2=r'D:\OneDrive\Oracle\Trading Program\Stock Data\current day'
charttime=[1,2,3,4,5,6]
tickerlist={0:"\TVC_USOIL, ",1:r'\NASDAQ_MSFT, ',2:r"\NASDAQ_AAPL, ",3:"\SPCFD_S5INFT, ",4:"\SPCFD_SPX, ",5:"\TVC_NDX, "}
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'}
change = [0.5,0.75,1,1.25,1.5,2,2.5,3]
zex = {1:[0,"rsiprob"],2:[1,"macdprob"],3:[2,"maprob"],4:[3,"bbprob"],5:[4,"maratioprob"]}
numberbarss={1:120,2:30,3:10,4:4,5:4,6:2} #for various chart intervals the number of bars forward that are to be looked at varies
    #i.e. This is because i would want a trade to have a time range of about 30mins-4 hours e.g. for minute bars 120 is required for hour bars 3 is required
numberbarsl={1:240,2:60,3:24,4:8,5:8,6:4}


def fullframe(): #simple function which displays full dataframe
    print('Select y for full df display')
    x=input()
    if x == 'y':
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
    else:
        pass

def priceprob(df,nb,valuechange): #this function calculates whether the value at each point increases by the "valuechange" in nb points


    for x in range((len(df.index) - nb)):  # this itterates over every row in the dataframe except the top rows where forward data is not available
        cprice = fval(df, 'close', x)  # current close price
        p1list = []  # list of probabilities for range of forward bars
        p2list = []  # this list is for probabilities if the value change is both up and down by the required amount i.e. moves 1% up and 1% down in net 3 hours
        y=(x+nb-1) #point in future
        npriceddf=(df.loc[df.index[x:y],'low'])
        npriced= npriceddf.min() #finds lowest value between now and future
        npriceudf =(df.loc[df.index[x:y],'high'])
        npriceu = npriceudf.max() #finds highest value

        d = cprice - npriced  # different between forward price and current price being examined
        u = npriceu - cprice
        percent = (cprice / 100) * valuechange #looks for values where change is equal to or greater than desired value change

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
        df.loc[df.index[x + nb], 'p1'] = p11  # assign these values to df column
        df.loc[df.index[x + nb], 'p2'] = p22
    return(df)

def dffix(list,x,tp,ticker,path):

    excel1 = path + ticker + str(list[x]) + ".csv"
    df = pd.read_csv(excel1)
    #print('Chart Interval is '+(str(list[x])))
    # puts column headers in
    df.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
                  'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
                  ,'MOMMACD','MOMSignal']
    df['time'] = pd.to_datetime(df['time'])  # changes time column format to datetime
    df = df.iloc[::-1] # revereses index so that newest values are on top for easier calculations
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


def seperatevar(ticker,chartinterval):
    start_time = time.time()


    df=dffix(listdf, chartinterval, 0, ticker,path) #makes dataframe


    if chartinterval<4:
        dffib=dffix(listdf,6,1,tickerlist[0],path) #dataframe used for fibonacci retracement (day chart for 1,5,15 min and week for hour, 4hr and day)
    else:
        dffib=dffix(listdf,7,1,tickerlist[0],path)

    for x in range(len(dffib)):
        dffib.loc[dffib.index[x], "timedate"] = (dffib.loc[dffib.index[x], "time"].date()) #makes date only time column for fibonacci calcs

    for x in range(len(df)):

        bodysize=100*(abs((fval(df,"close",x))-(fval(df,"open",x)))/(fval(df,"open",x))) #calculates body size of candle
        df.loc[df.index[x], "Body Size"]=bodysize

    medianbody = df["Body Size"].median() #median size of body

    df["Body Size Ratio"] = df["Body Size"] / medianbody #to provide a relative body size

    rsigradnum = {1: 20, 2: 10, 3: 10, 4: 6, 5: 5, 6: 5} #list of range of vlaues to calucalte RSI gradient over
    rsigradn = rsigradnum[chartinterval] #rsi gradient number is dependant on chartinterval
    df['Spread'] = df["Upper"] - df['Lower'] #spread of bollinger bands
    for x in range(len(df)):
        df.loc[df.index[x], "Spread"]=fval(df,'Spread',x)/fval(df,'close',x)  #makes spread value relative to price


    df["MA Spread"] = 0
    for x in range(len(df)-10):

        # MASPREAD
        df.loc[df.index[x], "MA Spread"] = ((fval(df, 'close', x) - fval(df, "50MA", x)) / fval(df, 'close',x)) * 100  # calculates as a percentage of price how much above or below ma25

        # RSIGRADIENT
        df.loc[df.index[x], 'rsigrad'] = (df.loc[df.index[x], 'RSI'] - df.loc[df.index[x + rsigradn], 'RSI']) / rsigradn #calculates gradient of rsi

        # HISTOGRAM Profile
        df.loc[df.index[x], 'Histogram Gradient'] = (fval(df, 'Histogram', x) - fval(df, 'Histogram', (x + 3))) / 4 #calcuates histogram gradient
        if df.loc[df.index[x], 'Histogram'] > 0:
            if df.loc[df.index[x], 'Histogram Gradient'] > 0:
                df.loc[df.index[x], 'Histogram Profile'] = "upup"
            else:
                df.loc[df.index[x], 'Histogram Profile'] = "updown"
        else:
            if df.loc[df.index[x], 'Histogram Gradient'] > 0:
                df.loc[df.index[x], 'Histogram Profile'] = "downup"
            else:
                df.loc[df.index[x], 'Histogram Profile'] = "downdown" #defines 4 different MACD profiles

        #MA Profile

        y = (fval(df, '25MA', x)) < (fval(df, '50MA', x))
        q = (fval(df, '25MA', x)) < (fval(df, '100MA', x))
        s = (fval(df, '50MA', x)) < (fval(df, '100MA', x)) #determines whether MAs are crossed over each other

        # had to convert to str to comapre lists as pandas makeslsit single values
        df.at[x, 'MA Profile'] = str([y, q, s])  # list of true false statements that comaprs to all comprarable possibilities

        #Bollinger Bands

         #calulates whether bollinger bands are squeezing or stretching based on gradient

        df.loc[df.index[x], 'Spread Grad Ratio'] = ((fval(df, 'Spread', x) - fval(df, 'Spread', (x + 1))) / 2) *10000 #x1000 so number is more easily understandable



        cspread = fval(df, 'Spread', x)
        df.loc[df.index[x], 'Spread Ratio'] = ((cspread)/ (df['Spread']).median()) #makes spread ratio realtive to average spread
        if fval(df, 'close', x) > fval(df, 'Upper', x): #set of if statements that determines whether price is inside or outside bollinger bands
            df.loc[df.index[x], 'BB Profile'] = "Breakover"
        elif fval(df, 'close', x) < fval(df, 'Lower', x):
            df.loc[df.index[x], 'BB Profile'] = "Breakunder"
        elif fval(df, 'Lower', x)<=fval(df, 'close', x)<=fval(df, 'Upper', x) and fval(df, 'close', x)>fval(df, 'Basis', x):
            df.loc[df.index[x], 'BB Profile'] = "Within Upper Bound"
        elif fval(df, 'Lower', x)<=fval(df, 'close', x)<=fval(df, 'Upper', x) and fval(df, 'close', x)<=fval(df, 'Basis', x):
            df.loc[df.index[x], 'BB Profile'] = "Within Lower Bound"
        else:
            pass

    #determines strength of spread or squeeze by examing the gradient of lines
        spreadgradlist={2:[10,4],3:[12,6],4:[15,8],5:[60,20]}
        sgrad=spreadgradlist[chartinterval]
        if fval(df, 'Spread Grad Ratio', x)>=sgrad[0]:
            df.loc[df.index[x], 'Squeeze Spread']="Strong Spread"
        elif sgrad[0]>fval(df, 'Spread Grad Ratio', x)>=sgrad[1]:
            df.loc[df.index[x], 'Squeeze Spread'] = "Weak Spread"
        elif sgrad[1]>fval(df, 'Spread Grad Ratio', x)>-sgrad[1]:
            df.loc[df.index[x], 'Squeeze Spread'] = "Flat"
        elif -sgrad[1]>=fval(df, 'Spread Grad Ratio', x)>-sgrad[0]:
            df.loc[df.index[x], 'Squeeze Spread'] = "Weak Squeze"
        elif -sgrad[0]>=fval(df, 'Spread Grad Ratio', x):
            df.loc[df.index[x], 'Squeeze Spread'] = "Strong Squeeze"
        else:
            pass

        # Fibbonaci

        df.loc[df.index[x], "timedate"] = (df.loc[df.index[x], "time"].date())  # makes date only column
        df['hour'] = pd.to_datetime(df['time'], format='%H:%M').dt.hour



        currentdate = df.loc[df.index[x], "timedate"]
        day = datetime.weekday(currentdate)
        if day != 6 and chartinterval > 3:
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

        elif day != 6 and chartinterval < 4:
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

        #Resistance and Support

        # when calculating probabilities make sure to know whether price is in upper half of dolalr range as this will determine use of half support resistance i.e. at 37.7 37.5 acts as better supp than at 38.3

        cprice = fval(df, "close", x)
        ten = float(round(cprice, -1))  # founds rounded multiple of 10
        one = float(round(cprice))


        if one > cprice:
            if one==ten:
                df.loc[df.index[x], "First Whole Resistance"] = one+1
                df.loc[df.index[x], "Second Whole Resistance"] = (one + 2)
                df.loc[df.index[x], "First Whole Support"] = (one - 1)
                df.loc[df.index[x], "Second Whole Support"] = (one - 2)
            elif one==(ten-1):
                df.loc[df.index[x], "First Whole Resistance"] = one
                df.loc[df.index[x], "Second Whole Resistance"] = one+2
                df.loc[df.index[x], "First Whole Support"] = (one - 1)
                df.loc[df.index[x], "Second Whole Support"] = (one - 2)
            elif one==(ten+1):
                df.loc[df.index[x], "First Whole Resistance"] = one
                df.loc[df.index[x], "Second Whole Resistance"] = one + 1
                df.loc[df.index[x], "First Whole Support"] = (one - 2)
                df.loc[df.index[x], "Second Whole Support"] = (one - 3)



            df.loc[df.index[x], "First Half Resistance"] = (one + 0.5)
            df.loc[df.index[x], "First Half Support"] = (one - 0.5)
            df.loc[df.index[x], "Second Half Resistance"] = (one + 1.5)
            df.loc[df.index[x], "Second Half Support"] = (one - 1.5)

        elif one <= cprice:
            if one==ten:
                df.loc[df.index[x], "First Whole Support"] = one-1
                df.loc[df.index[x], "Second Whole Support"] = (one - 2)
                df.loc[df.index[x], "First Whole Resistance"] = one + 1
                df.loc[df.index[x], "Second Whole Resistance"] = (one + 2)
            elif one==(ten-1):
                df.loc[df.index[x], "First Whole Support"] = one
                df.loc[df.index[x], "Second Whole Support"] = one-1
                df.loc[df.index[x], "First Whole Resistance"] = one + 2
                df.loc[df.index[x], "Second Whole Resistance"] = (one + 3)
            elif one==(ten+1):
                df.loc[df.index[x], "First Whole Support"] = one
                df.loc[df.index[x], "Second Whole Support"] = one-2
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

        #Candle Stick Analysis

        open = fval(df, "open", x)
        close = fval(df, "close", x)
        low = fval(df, "low", x)
        high = fval(df, "high", x)

        if open > close:
            df.loc[df.index[x], "CandleStick Colour"] = "Red"
            lshadow = (close - low) / open
            if lshadow != 0:
                lshadow = (lshadow / medianbody)
            else:
                lshadow = 0
            ushadow = (high - open) / open
            if ushadow != 0:
                ushadow = (ushadow / medianbody)
            else:
                ushadow = 0



        elif close > open:
            df.loc[df.index[x], "CandleStick Colour"] = "Green"
            lshadow = (open - low) / open
            if lshadow != 0:
                lshadow = (lshadow / medianbody)
            else:
                lshadow = 0
            ushadow = (high - close) / open
            if ushadow != 0:
                ushadow = (ushadow / medianbody)
            else:
                ushadow = 0


        else:
            candlestick = "Doji"

        df.loc[df.index[x], "Low Whick"] = (lshadow*100)
        df.loc[df.index[x], "Upper Whick"] = (ushadow*100)

    Resistancelist = ["First Whole Resistance", "Second Whole Resistance", "Ten Resistance", "Five Resistance"]

    supportlist = ["First Whole Support", "Second Whole Support", "Ten Support", "Five Support"]
    df["Relative Volume"] = 0

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
        if chartinterval > 2:
            for resistance in Resistancelist:
                if open <= df.loc[df.index[x + 1], resistance] and close > df.loc[df.index[x + 1], resistance]:
                    RSbreak.append(1)
                else:
                    RSbreak.append(0)
            for support in supportlist:
                if open >= df.loc[df.index[x + 1], support] and close < df.loc[df.index[x + 1], support]:
                    RSbreak.append(1)

                else:
                    RSbreak.append(0)
        elif chartinterval >= 2:
            for resistance in Resistancelist:
                if open >= df.loc[df.index[x + 1], resistance] and close > df.loc[df.index[x + 1], resistance]:
                    RSbreak.append(1)
                else:
                    RSbreak.append(0)
            for support in supportlist:
                if open <= df.loc[df.index[x + 1], support] and close < df.loc[df.index[x + 1], support]:
                    RSbreak.append(1)

                else:
                    RSbreak.append(0)

        else:
            pass
        RSbreak = str(tuple(RSbreak))
        df.loc[df.index[x], "RS Break"] = RSbreak





    #Trend Line Analysis
    #
    # for x in range(len(df-20)):
    #     closeprices={}
    #     openprices={}
    #     for z in range(x,(x-5)):
    #         closeprices.update({z:[z,fval(df,"close",z)]})
    #         openprices.update({z: [z, fval(df, "open", z)]})
    #
    #     if df.loc[df.index[x], "CandleStick Colour"]=="Green" and currentopen>startopen:
    #         trendlbotg=(fval("open",df,x)-fval(df,"open",(x+3)))/4
    #         for z in range(x+1,0):
    #             trendline=(z*trendlbotg+startopen)
    #             if fval(df,"open",(z))>trendline and (df,"close",(z))>trendline:
    #











    #MAX AND MIN PRICE CHANGE
    # df['Price ChangeUp'] = 0
    # df['Price ChangeDown'] = 0
    # for x in range(len(df.index) - 1):
    #     df.loc[df.index[x], 'Price Change Up'] = (fval(df, 'high', x) - fval(df, 'close', (x + 1))) / fval(df, 'close',
    #                                                                                                        (
    #                                                                                                                    x + 1)) * 100
    #     df.loc[df.index[x], 'Price Change Down'] = (fval(df, 'low', x) - fval(df, 'close', (x + 1))) / fval(df, 'close',
    #                                                                                                         (
    #                                                                                                                     x + 1)) * 100
    #
    # maxmoveup = df["Price Change Up"].max()
    # maxmovedown = df["Price Change Down"].min()




    df.to_csv(path + ticker + "short" + "newfull" + str(listdf[chartinterval]) + ".csv", index=False)



    return
for x in range(2,7):
    seperatevar(tickerlist[0],x)


def probcalculator(valuechange):

    df15=pd.read_csv((path + tickerlist[0] + "short" + "newfull" + "15" + ".csv"))
    df60 = pd.read_csv((path + tickerlist[0] + "short" + "newfull" + "60" + ".csv"))
    df15['time'] = pd.to_datetime(df15['time'])
    df60['time'] = pd.to_datetime(df60['time'])

    df15['p1'] = 0  # columns for probability of up or down within the number bars selected
    df15['p2'] = 0
    df15 = priceprob(df15, 8, valuechange)

    for x in range(len(df15)):
        currentdate=fval(df15,'timedate',x)
        currenthour=int(fval(df15,'hour',x))
        for y in range(len(df60)):
            hourdate = fval(df60, 'timedate', y)
            hourhour = int(fval(df60, 'hour', y))

            if hourdate==currentdate and currenthour==(hourhour+1):
                df15.loc[df15.index[x], 'hourrsi']=fval(df60, 'RSI', y)
                df15.loc[df15.index[x], 'hourrsigrad'] = fval(df60, 'rsigrad', y)
                df15.loc[df15.index[x], 'hourmacdprofile'] = fval(df60, 'Histogram Profile', y)
                df15.loc[df15.index[x], 'hourMAProfile'] = fval(df60, 'MA Profile', y)
                df15.loc[df15.index[x], 'hourSqueezeSpread'] = fval(df60, 'Squeeze Spread', y)
                df15.loc[df15.index[x], 'hourBBProfile'] = fval(df60, 'BB Profile', y)
                df15.loc[df15.index[x], 'hourRelativeVolume'] = fval(df60, 'Relative Volume', y)






    listq=[0,0.15,0.3,0.6,0.75,1]
    listqmaspread=[]
    listqrsigrad=[]
    listqspreadratio=[]
    for q in listq:
        # print(df["Body Size Ratio"].quantile([q]))
        # print(df["Low Whick"].quantile([q]))
        # print(df["Upper Whick"].quantile([q]))
        listqmaspread.append(float(df["MA Spread"].quantile([q])))
        listqrsigrad.append(float(df["rsigrad"].quantile([q])))
        listqspreadratio.append(float(df["Spread Ratio"].quantile([q])))
    print(listqmaspread)
    print(listqrsigrad)
    print(listqspreadratio)
    listqmaspread = [-6,-2,0,2,4]
    listqrsigrad = [-5,-2,0,2,5]
    listqspreadratio = [0,0.5,1,2,6]


    probu = []
    probd=[]
    nval=[]
    nvalup=[]
    nvaldown=[]
    rsilist=[0,20,30,50,70,80,100]
    RSlist=["FWR, SWR, TR, FR, FWS, SWS, TS, FS"]

    rsmove=(list(itertools.product([0,1],repeat=8)))

    profile=[]
    bblist1 = ["Breakover", "Breakunder", "Within Upper Bound", "Within Lower Bound"]
    bblist2 = ["Strong Spread", "Weak Spread", "Flat", "Weak Squeze", "Strong Squeeze"]

    # dfmove=df[df["p1"]!=0]
    # dfmove = dfmove.reset_index(drop=True)
    # print(len(dfmove))
    # for h in range(len(listq) - 1):
    #     dfmove1= dfmove[(dfmove["rsigrad"] >= float(listqrsigrad[h])) & (dfmove["rsigrad"] < float(listqrsigrad[h+1]))]
    #     for b in range(len(rsilist)-1):
    #         dfmove2 = dfmove1[(dfmove['RSI'] >= rsilist[b]) & (dfmove1['RSI'] < rsilist[b + 1])]
    #         print(len(dfmove2))



    for movethrough in rsmove:

        dfprobs0=df[(df["RS Break"]==str(movethrough))]
        if len(dfprobs0)>0:
            for x in range(len(listqmaspread)-1):
                dfprobs1= dfprobs0[(dfprobs0["MA Spread"] >= float(listqmaspread[x])) & (dfprobs0["MA Spread"] < float(listqmaspread[x+1]))]
                dfprobs1 = dfprobs1.reset_index(drop=True)
                for h in range(len(listqrsigrad) - 1):
                    dfprobs2= dfprobs1[(dfprobs1["rsigrad"] >= float(listqrsigrad[h])) & (dfprobs1["rsigrad"] < float(listqrsigrad[h+1]))]
                    dfprobs2 = dfprobs2.reset_index(drop=True)

                    for a in range(len(listqspreadratio) - 1):
                        dfprobs3 = dfprobs2[(dfprobs2["Spread Ratio"] >= float(listqspreadratio[a])) & (dfprobs2["Spread Ratio"] < float(listqspreadratio[a + 1]))]
                        dfprobs3 = dfprobs3.reset_index(drop=True)



                        for b in range(len(rsilist) - 1):  # then sorts by rsi value
                            dfprobs4=dfprobs3[(dfprobs3['RSI'] >= rsilist[b]) & (dfprobs3['RSI'] <rsilist[b+1])]
                            dfprobs4 = dfprobs4.reset_index(drop=True)


                            for c in bblist1:
                                dfprobs5=dfprobs4[dfprobs4["BB Profile"]==c]
                                dfprobs5 = dfprobs5.reset_index(drop=True)
                                for d in bblist2:
                                    dfprobs6 = dfprobs5[dfprobs5["Squeeze Spread"] == d]
                                    dfprobs6 = dfprobs6.reset_index(drop=True)

                                    dfprobslength=len(dfprobs6)

                                    if dfprobslength > 1:  # incase that rsi range has no values


                                        dfprobsu1 = dfprobs6[dfprobs6['p1'] > 0]  # new df of values within range selected that have probability of +1
                                        timesdrop1 = []
                                        if 3>len(dfprobsu1)>1:
                                            for k in range(1,len(dfprobsu1)):
                                                timenow = dfprobsu1.loc[dfprobsu1.index[k], 'time']
                                                timeminus = dfprobsu1.loc[dfprobsu1.index[k - 1], 'time']

                                                timedelta = timeminus-timenow

                                                timeclose=(pd.Timedelta("0 days" + (str(listdf[chartinterval]) + " min")))
                                                if timedelta==timeclose:
                                                    timesdrop1.append(k-1)

                                                else:
                                                    pass
                                            dfprobsu1=dfprobsu1.drop(dfprobsu1.index[timesdrop1])
                                        elif len(dfprobsu1)>2:

                                            for k in range(2,len(dfprobsu1)):
                                                timenow = dfprobsu1.loc[dfprobsu1.index[k], 'time']
                                                timeminus = dfprobsu1.loc[dfprobsu1.index[k - 1], 'time']
                                                timeplus = dfprobsu1.loc[dfprobsu1.index[k - 2], 'time']
                                                timedelta = timeminus-timenow
                                                timedelta2 = timeplus-timenow

                                                timeclose=(pd.Timedelta("0 days" + (str(listdf[chartinterval]) + " min")))
                                                timeclose2=(pd.Timedelta("0 days" + (str(2*(listdf[chartinterval])) + " min")))
                                                if timedelta==timeclose or timedelta==timeclose2:
                                                    timesdrop1.append(k-1)
                                                elif timedelta==timeclose2:
                                                    timesdrop1.append(k - 2)

                                                else:
                                                    pass
                                            dfprobsu1=dfprobsu1.drop(dfprobsu1.index[timesdrop1])

                                        else:
                                            pass



                                        dfmau1 = len(dfprobsu1.index)  # length of this df gives number of times it move sup within this rsi range
                                        dfprobsu2 = dfprobs6[dfprobs6['p2'] > 0]  # does the same withi p2

                                        timesdrop3 = []
                                        if 3 > len(dfprobsu2) > 1:
                                            for k in range(1, len(dfprobsu2)):
                                                timenow = dfprobsu2.loc[dfprobsu2.index[k], 'time']
                                                timeminus = dfprobsu2.loc[dfprobsu2.index[k - 1], 'time']

                                                timedelta = timeminus - timenow

                                                timeclose = (pd.Timedelta("0 days" + (str(listdf[chartinterval]) + " min")))
                                                if timedelta == timeclose:
                                                    timesdrop1.append(k - 1)

                                                else:
                                                    pass
                                            dfprobsu2 = dfprobsu2.drop(dfprobsu2.index[timesdrop3])
                                        elif len(dfprobsu2) > 2:

                                            for k in range(2, len(dfprobsu2)):
                                                timenow = dfprobsu2.loc[dfprobsu2.index[k], 'time']
                                                timeminus = dfprobsu2.loc[dfprobsu2.index[k - 1], 'time']
                                                timeplus = dfprobsu2.loc[dfprobsu2.index[k - 2], 'time']
                                                timedelta = timeminus - timenow
                                                timedelta2 = timeplus - timenow

                                                timeclose = (pd.Timedelta("0 days" + (str(listdf[chartinterval]) + " min")))
                                                timeclose2 = (
                                                    pd.Timedelta("0 days" + (str(2 * (listdf[chartinterval])) + " min")))
                                                if timedelta == timeclose or timedelta == timeclose2:
                                                    timesdrop1.append(k - 1)
                                                elif timedelta == timeclose2:
                                                    timesdrop1.append(k - 2)

                                                else:
                                                    pass
                                            dfprobsu2 = dfprobsu2.drop(dfprobsu2.index[timesdrop3])

                                        else:
                                            pass

                                        dfmau2 = len(dfprobsu2.index)

                                        dfprobsd1 = dfprobs6[dfprobs6['p1'] < 0]
                                        timesdrop2 = []
                                        if 3>len(dfprobsd1)>1:
                                            for j in range(2,len(dfprobsd1)):
                                                timenow = dfprobsd1.loc[dfprobsd1.index[j], 'time']
                                                timeminus = dfprobsd1.loc[dfprobsd1.index[j - 1], 'time']
                                                timedelta = timeminus-timenow

                                                timeclose=(pd.Timedelta("0 days" + (str(listdf[chartinterval]) + " min")))
                                                if timedelta==timeclose:
                                                    timesdrop2.append(j-1)

                                                else:
                                                    pass
                                            dfprobsd1 = dfprobsd1.drop(dfprobsd1.index[timesdrop2])
                                        elif len(dfprobsd1)>2:

                                            for j in range(2,len(dfprobsd1)):
                                                timenow = dfprobsd1.loc[dfprobsd1.index[j], 'time']
                                                timeminus = dfprobsd1.loc[dfprobsd1.index[j - 1], 'time']
                                                timeplus = dfprobsd1.loc[dfprobsd1.index[j - 2], 'time']
                                                timedelta = timeminus-timenow
                                                timedelta2 = timeplus-timenow

                                                timeclose=(pd.Timedelta("0 days" + (str(listdf[chartinterval]) + " min")))
                                                timeclose2=(pd.Timedelta("0 days" + (str(2*(listdf[chartinterval])) + " min")))
                                                if timedelta==timeclose or timedelta==timeclose2:
                                                    timesdrop2.append(j-1)
                                                elif timedelta==timeclose2:
                                                    timesdrop2.append(j - 2)
                                                else:
                                                    pass
                                            dfprobsd1 = dfprobsd1.drop(dfprobsd1.index[timesdrop2])


                                        else:
                                            pass
                                        dfprobsn1l = len(dfprobsd1.index)

                                        probu40 = ((dfmau1 + dfmau2) / (dfprobslength-(len(timesdrop1)+len(timesdrop3)))) # number of times it moves up divided by number of times at this range gives probability
                                        probd40 = (dfprobsn1l / (dfprobslength-(len(timesdrop2))))
                                        profilestr=("MA Spread: "+str(listqmaspread[x])+"-"+str(listqmaspread[x+1])+" "+ "RSI: "+ str(rsilist[b])+"-"+str(rsilist[b+1])+" "+
                                                    "RSI Grad: "+str(listqrsigrad[h])+"-"+str(listqrsigrad[h+1])+" "+"SpreadRatio: "+str(listqspreadratio[a])+"-"+str(listqspreadratio[a+1])+" "+str(c)+str(d)+" "+
                                                    str(RSlist) +str(movethrough))
                                        if probu40>0 or probd40>0:
                                            probu.append(probu40)
                                            probd.append(probd40)
                                            profile.append(profilestr)
                                            nval.append(dfprobslength)
                                            nvaldown.append((dfprobsn1l + 0))
                                            nvalup.append((dfmau1 + dfmau2 + 0))
                                        else:
                                            pass

                                    else:
                                        pass
        else:
            pass

    probs = pd.DataFrame(
    {'Profile': [], 'Probability Up': [], 'Probability Down': [],'Nvalue':[],'Nvalue Up':[],'Nvalue Down':[]})  # makes df of probabilities at rsi ranges
    probs['Profile'] = profile
    probs['Probability Up'] = probu
    probs['Probability Down'] = probd
    probs['Nvalue'] = nval
    probs["Nvalue Up"]=nvalup
    probs["Nvalue Down"]=nvaldown


    print(probs)
    probs.to_csv(path + ticker + "short" + "fullprobs" + str(listdf[chartinterval]) + ".csv", index=False)


    print("time elapsed: {:.2f}s".format(time.time() - start_time))
    return







df['p1'] = 0  # columns for probability of up or down within the number bars selected
df['p2'] = 0
df = priceprob(df, nb, valuechange)














print ("time elapsed: {:.2f}s".format(time.time() - start_time))