



import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta
import time
import math
import itertools



path = r'D:\OneDrive\Oracle\Trading Program\Stock Data\current day'
path2=r'D:\OneDrive\Oracle\Trading Program\Stock Data\current day'

def fullframe():
    print('Select y for full df display')
    x=input()
    if x == 'y':
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
    else:
        pass

def priceprob(df,nb,valuechange):
    for x in range((len(df.index) - nb)):  # this itterates over every row in the dataframe except the top rows where forward data is not available
        cprice = fval(df, 'close', x + nb)  # current price
        p1list = []  # list of probabilities for range of forward bars
        p2list = []  # this list is for probabilities if the value change is both up and down by the required amount i.e. moves 1% up and down in net 3 hours
        y=(x+nb-1)
        npriceddf=(df.loc[df.index[x:y],'low'])
        npriced= npriceddf.min()
        npriceudf =(df.loc[df.index[x:y],'high'])
        npriceu = npriceudf.max()

        d = cprice - npriced  # different between forward price and current price being exaimned
        u = npriceu - cprice
        percent = (cprice / 100) * valuechange

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
        if len(pd2) > 0:  # if both occur then 2 probabilities are entered
            p11 = -1
            p22 = 1
        else:
            p22 = 0  # if only one value change occurs
            if len(
                    pu1) > 0:  # if list has any values in it then a value chnage up occured thus rsi has preceded an upwards movement
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


def seperatevar(ticker,chartinterval,valuechange,nb):
    start_time = time.time()

    nb=nb
    df=dffix(listdf, chartinterval, 0, ticker,path)
    df['p1'] = 0  # columns for rsi probability of up or down within the number bars selected
    df['p2'] = 0
    df = priceprob(df, nb, valuechange)

    if chartinterval<4:
        dffib=dffix(listdf,6,1,tickerlist[0],path)
    else:
        dffib=dffix(listdf,7,1,tickerlist[0],path)

    for x in range(len(dffib)):
        dffib.loc[dffib.index[x], "timedate"] = (dffib.loc[dffib.index[x], "time"].date())

    for x in range(len(df)):

        bodysize=100*(abs((fval(df,"close",x))-(fval(df,"open",x)))/(fval(df,"open",x)))
        df.loc[df.index[x], "Body Size"]=bodysize

    medianbody = df["Body Size"].median()

    df["Body Size Ratio"] = df["Body Size"] / medianbody

    rsigradnum = {1: 20, 2: 10, 3: 10, 4: 6, 5: 5, 6: 5}
    rsigradn = rsigradnum[chartinterval]
    df['Spread'] = df["Upper"] - df['Lower']


    df["MA Spread"] = 0
    for x in range(len(df)-10):

        # MASPREAD
        df.loc[df.index[x], "MA Spread"] = ((fval(df, 'close', x) - fval(df, "25MA", x)) / fval(df, 'close',x)) * 100  # calculates as a percentage of price above or below ma25

        # RSIGRADIENT
        df.loc[df.index[x], 'rsigrad'] = (df.loc[df.index[x], 'RSI'] - df.loc[df.index[x + rsigradn], 'RSI']) / rsigradn

        # HISTOGRAM GRADIENT
        df.loc[df.index[x], 'Histogram Gradient'] = (fval(df, 'Histogram', x) - fval(df, 'Histogram', (x + 3))) / 4
        if df.loc[df.index[x], 'Histogram'] > 0:
            if df.loc[df.index[x], 'Histogram Gradient'] > 0:
                df.loc[df.index[x], 'Histogram Profile'] = "upup"
            else:
                df.loc[df.index[x], 'Histogram Profile'] = "updown"
        else:
            if df.loc[df.index[x], 'Histogram Gradient'] > 0:
                df.loc[df.index[x], 'Histogram Profile'] = "downup"
            else:
                df.loc[df.index[x], 'Histogram Profile'] = "downdown"

        #MA Profile

        y = (fval(df, '25MA', x)) < (fval(df, '50MA', x))
        q = (fval(df, '25MA', x)) < (fval(df, '100MA', x))
        r = (fval(df, '25MA', x)) < (fval(df, '200MA', x))
        s = (fval(df, '50MA', x)) < (fval(df, '100MA', x))

        # had to convert to str to comapre lists as pandas makeslsit single values
        df.at[x, 'MA Profile'] = str([y, q, r, s])  # list of true false statements that comaprs to all comprarable possibilities

        #Bollinger Bands

        df.loc[df.index[x], 'Spread Grad'] = (fval(df, 'Spread', x) - fval(df, 'Spread', (x + 2))) / 3
        df.loc[df.index[x], 'Spread Grad Ratio'] = (fval(df, 'Spread Grad', x) / fval(df, 'close', x))*1000


        cspread = fval(df, 'Spread', x)
        df.loc[df.index[x], 'Spread Ratio'] = (cspread / (df['Spread']).median())

        if fval(df, 'close', x) > fval(df, 'Upper', x):
            df['BB Profile'] = "Breakover"
        elif fval(df, 'close', x) > fval(df, 'Lower', x):
            df['BB Profile'] = "Breakunder"
        elif fval(df, 'Lower', x)<=fval(df, 'close', x)<=fval(df, 'Upper', x) and fval(df, 'close', x)>fval(df, 'Basis', x):
            df['BB Profile'] = "Within Upper Bound"
        elif fval(df, 'Lower', x)<=fval(df, 'close', x)<=fval(df, 'Upper', x) and fval(df, 'close', x)<=fval(df, 'Basis', x):
            df['BB Profile'] = "Within Lower Bound"
        else:
            pass

        if fval(df, 'Spread Grad Ratio', x)>=1.9:
            df.loc[df.index[x], 'Squeeze Spread']="Strong Spread"
        elif 1.9>fval(df, 'Spread Grad Ratio', x)>=0.9:
            df.loc[df.index[x], 'Squeeze Spread'] = "Weak Spread"
        elif 0.9>fval(df, 'Spread Grad Ratio', x)>-0.9:
            df.loc[df.index[x], 'Squeeze Spread'] = "Flat"
        elif -0.9>=fval(df, 'Spread Grad Ratio', x)>-1.9:
            df.loc[df.index[x], 'Squeeze Spread'] = "Weak Squeze"
        elif -1.9>=fval(df, 'Spread Grad Ratio', x):
            df.loc[df.index[x], 'Squeeze Spread'] = "Strong Squeeze"
        else:
            pass

        #Fibbonaci

        df.loc[df.index[x], "timedate"] = (df.loc[df.index[x], "time"].date())  # makes date only column

        currentdate = df.loc[df.index[x], "timedate"]
        day = datetime.weekday(currentdate)
        if day != 6 and chartinterval > 3:
            week = currentdate - timedelta(days=(8 + day))
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
            priorday = currentdate - timedelta(days=1)
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
            df.loc[df.index[x], "First Whole Resistance"] = one
            df.loc[df.index[x], "First Whole Support"] = (one - 1)
            df.loc[df.index[x], "First Half Resistance"] = (one + 0.5)
            df.loc[df.index[x], "First Half Support"] = (one - 0.5)
            df.loc[df.index[x], "Second Whole Resistance"] = (one + 1)
            df.loc[df.index[x], "Second Whole Support"] = (one - 2)
            df.loc[df.index[x], "Second Half Resistance"] = (one + 1.5)
            df.loc[df.index[x], "Second Half Support"] = (one - 1.5)
        elif one < cprice:
            df.loc[df.index[x], "First Whole Resistance"] = one + 1
            df.loc[df.index[x], "First Whole Support"] = one
            df.loc[df.index[x], "First Half Resistance"] = (one + 0.5)
            df.loc[df.index[x], "First Half Support"] = (one - 0.5)
            df.loc[df.index[x], "Second Whole Resistance"] = (one + 2)
            df.loc[df.index[x], "Second Whole Support"] = (one - 2)
            df.loc[df.index[x], "Second Half Resistance"] = (one + 1.5)
            df.loc[df.index[x], "Second Half Support"] = (one - 1.5)
        else:
            df.loc[df.index[x], "First Whole Resistance"] = one + 1
            df.loc[df.index[x], "First Whole Support"] = one
            df.loc[df.index[x], "First Half Resistance"] = (one + 0.5)
            df.loc[df.index[x], "First Half Support"] = (one - 0.5)
            df.loc[df.index[x], "Second Whole Resistance"] = (one + 2)
            df.loc[df.index[x], "Second Whole Support"] = (one - 2)
            df.loc[df.index[x], "Second Half Resistance"] = (one + 1.5)
            df.loc[df.index[x], "Second Half Support"] = (one - 1.5)

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

        df.loc[df.index[x], "Low Whick"] = lshadow
        df.loc[df.index[x], "Upper Whick"] = ushadow




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

    #Bollinger Bands









    if valuechange == 1:

        df.to_csv(path + ticker + "short" + "newfull" + str(listdf[chartinterval])+".csv", index=False)
    else:
        pass

    print("time elapsed: {:.2f}s".format(time.time() - start_time))
    return df








    # for x in range(df):
    #     cprice=fval(df,"close",x)
    #     rten = float(round(cprice, -1))  # founds rounded multiple of 10
    #     cr = float(math.ceil(fval(df, 'close', 0)))  # finds cloeset dollar value above
    #     cs = float(math.floor(fval(df, 'close', 0)))  # closest dolar value below
    #
    #     if rten > cprice:  # founded other multiple of 10 and 5 depending if first rounded number was a support or resistance
    #         rfive = rten - 5
    #         sten = rten - 10
    #     else:
    #         rfive = rten + 5
    #         sten = rten + 10
    #
    #     RS.extend((cr, cs, rten, rfive, sten))
    #     RS = list(dict.fromkeys(RS))  # removes any duplicates from inputs
    #     R = [x for x in RS if x > cprice]  # seperates into R and s and reorders lists
    #     S = [x for x in RS if x < cprice]
    #
    #
    # high = fval(df, 'high', 0)
    # low = fval(df, 'low',0)
    # close = fval(df, 'close',0)
    # pp=round((high+low+close)/3,2)
    #
    # flevels=[0.382,0.618,1.0]
    # SF = []
    # RF=[]
    # for x in flevels:
    #
    #     rf=round((pp+((high-low)*x)),2)
    #     RF.append(rf)
    #
    #     sf = round((pp-((high-low)*x)),2)
    #     SF.append(sf)
    #
    # print(pp, RF,SF)



#     maratio = {0: -7, 1: -5, 2: -3, 3: -2, 4: -1, 5: 0, 6: 1, 7: 2, 8: 3,9:5,10:7,11:11}
#
#
#     probu=[]
#     probd=[]
#     dfmarange=[]
#     nval = []
#     for x in range(len(maratio)-1):
#         dfmaspread = df[(df["MA Spread"] >= maratio[x]) & (df["MA Spread"] < maratio[x+1])]  # makes new df with selcted rsi range that already has probability of that rsi range moving up
#         dfma = len(dfmaspread.index)  # has total number of rows within that rsi range
#
#
#         if dfma != 0:  # incase that rsi range has no values
#             nval.append(dfma)
#
#             dfmaspreadu1 = dfmaspread[dfmaspread['p1'] > 0]  # new df of values within range selected that have probability of +1
#             dfmau1 = len(dfmaspreadu1.index)  # length of this df gives number of times it move sup within this rsi range
#             dfmaspreadu2 = dfmaspread[dfmaspread['p2'] > 0]  # does the same withi p2
#             dfmau2 = len(dfmaspreadu2.index)
#             dfmaspreadn1 = dfmaspread[dfmaspread['p1'] < 0]
#             dfman1 = len(dfmaspreadn1.index)
#
#             probu40 = ((dfmau1 + dfmau2) / dfma)  # number of times it moves up divided by number of times at this range gives probability
#             probd40 = (dfman1 / dfma)
#             dfmarange.append(" " + str(maratio[x]) + " " + str(maratio[x + 1]))
#
#             probu.append(probu40)
#             probd.append(probd40)
#
#         else:
#             pass
#
#     maratioprobs = pd.DataFrame({'MA Ratio Range': [], 'Probability Up': [],'Probability Down': []})  # makes df of probabilities at rsi ranges
#     maratioprobs['MA Ratio Range'] = dfmarange
#     maratioprobs['Probability Up'] = probu
#     maratioprobs['Probability Down'] = probd
#     maratioprobs['Nvalue'] = nval
#
#
#     rsigradrange={0:-4,1:-3,2:-2,3:-1,4:0,5:1,6:2,7:3,8:4}
#
#
#     rsilist = {0:10, 1:20, 2:30, 3:40, 4:60, 5:70, 6:80,7:85,8:90} #ranges of rsis
#     rsirange=[] #list of ranges to be used in df
#     rsigradcol=[]
#     probu=[] #list of probability going up to be used
#     probd=[]
#     nval = []
#
#     for x in range(len(rsigradrange)-1): #initialy sort sby gradient
#         dfgrad=df[(df["rsigrad"] >=rsigradrange[x]) & (df["rsigrad"] >=rsigradrange[x+1])]
#         rsigradstr=" "+str(rsigradrange[x]) + " " + str(rsigradrange[x+1])
#         for x in range(len(rsilist)-1): #then sorts by rsi value
#             df40=dfgrad[(dfgrad['RSI'] >= rsilist[x]) & (dfgrad['RSI'] <rsilist[x+1])] #makes new df with selcted rsi range that already has probability of that rsi range moving up
#             rsi40 = len(df40.index) #has total number of rows within that rsi range
#             if rsi40 != 0: #incase that rsi range has no values
#                 nval.append(rsi40)
#
#                 df40u1=df40[df40['p1']>0] #new df of values within range selected that have probability of +1
#                 rsi40u1 = len(df40u1.index) #length of this df gives number of times it move sup within this rsi range
#                 df40u2=df40[df40['p2']>0] #does the same withi p2
#                 rsi40u2 = len(df40u2.index)
#                 df40n1=df40[df40['p1']<0]
#                 rsi40n1 = len(df40n1.index)
#
#                 probu40=((rsi40u1+rsi40u2)/rsi40) #number of times it moves up divided by number of times at this range gives probability
#                 probd40=(rsi40n1/rsi40)
#                 rsirange.append(" "+str(rsilist[x]) + " " + str(rsilist[x+1]))
#                 rsigradcol.append(rsigradstr)
#                 probu.append(probu40)
#                 probd.append(probd40)
#
#             else:
#                 pass
#
#
#     rsiprobs = pd.DataFrame({'RSI Range':[],'RSI Gradient':[], 'Probability Up':[],'Probability Down':[]}) #makes df of probabilities at rsi ranges
#     rsiprobs['RSI Range']=rsirange
#     rsiprobs['Probability Up']=probu
#     rsiprobs['Probability Down']=probd
#     rsiprobs['RSI Gradient']=rsigradcol
#     rsiprobs['Nvalue'] = nval
#
#
#
#
#     df=df[df['Histogram Gradient']!=0]
#     dfup=df[df['Histogram']>0]
#     dfdown=df[df['Histogram']<0]
#
#     upup=dfup[dfup['Histogram Gradient']>0]
#     updown=dfup[dfup['Histogram Gradient']<0]
#     downup = dfdown[dfdown['Histogram Gradient'] > 0]
#     downdown = dfdown[dfdown['Histogram Gradient'] < 0]
#     listdfmacd=[upup,updown,downup,downdown]
#     macdlist=['upup','updown','downup','downdown']
#     probu=[]
#     probd=[]
#
#     for x in listdfmacd:
#         dftotal = len(x.index)
#         dfup1 = x[x['p1'] > 0]
#         macdup1 = len(dfup1.index)
#         dfup2 = x[x['p2'] > 0]
#         macdup2 = len(dfup2.index)
#         dfdown1 = x[x['p1'] < 0]
#         macddown1 = len(dfdown1.index)
#         probu1 = ((macdup1 + macdup2) / dftotal)
#         probd1 = (macddown1 / dftotal)
#         probu.append(probu1)
#         probd.append(probd1)
#
#     dfmacdprob = pd.DataFrame( {'MACD':[], 'Probability Up':[], 'Probability Down':[]})
#     dfmacdprob['MACD']=macdlist
#     dfmacdprob['Probability Up']=probu
#     dfmacdprob['Probability Down']=probd
#
#
#     # df['MOM Histogram Gradient'] = 0
#     # for x in range(len(df.index) - 3):
#     #     df.loc[df.index[x], 'MOM Histogram Gradient'] = (fval(df, 'MOMHistogram', x) - fval(df, 'MOMHistogram', (x + 3))) / 4
#     #
#     #
#     # df = df[df['Histogram Gradient'] != 0]
#     # dfup = df[df['MOMHistogram'] > 0]
#     # dfdown = df[df['MOMHistogram'] < 0]
#     #
#     # upup = dfup[dfup['MOM Histogram Gradient'] > 0]
#     # updown = dfup[dfup['MOM Histogram Gradient'] < 0]
#     # downup = dfdown[dfdown['MOM Histogram Gradient'] > 0]
#     # downdown = dfdown[dfdown['MOM Histogram Gradient'] < 0]
#     # listdfmacd = [upup, updown, downup, downdown]
#     # macdlist = ['MOMupup', 'MOMupdown', 'MOMdownup', 'MOMdowndown','MOMupupup']
#     # probu = []
#     # probd = []
#     #
#     # for x in listdfmacd:
#     #     dftotal = len(x.index)
#     #     dfup1 = x[x['p1'] > 0]
#     #     macdup1 = len(dfup1.index)
#     #     dfup2 = x[x['p2'] > 0]
#     #     macdup2 = len(dfup2.index)
#     #     dfdown1 = x[x['p1'] < 0]
#     #     macddown1 = len(dfdown1.index)
#     #     probu1 = ((macdup1 + macdup2) / dftotal)
#     #     probd1 = (macddown1 / dftotal)
#     #     probu.append(probu1)
#     #     probd.append(probd1)
#     #
#     # dfMOMmacdprob = pd.DataFrame({'MOMMACD': [], 'Probability Up': [], 'Probability Down': []})
#     # dfMOMmacdprob['MOMMACD'] = macdlist
#     # dfMOMmacdprob['Probability Up'] = probu
#     # dfMOMmacdprob['Probability Down'] = probd
#
#
#
#
#     maperms = []
#     l = [False, True]
#     for i in itertools.product(l, repeat=4):
#         maperms.append(str(list(i)))  #converts lsit added as string
#     maprofile=[]
#     probu=[]
#     probd=[]
#     rsigradrange = {0: -5, 1: -3, 2: -1, 3: 0, 4: 1, 5: 3, 6: 5}
#     rsilist = {0: 10, 1: 20, 2: 30, 3: 40, 4: 60, 5: 70, 6: 80, 7: 90}  # ranges of rsis
#     rsirange = []  # list of ranges to be used in df
#     rsigradcol = []
#     nval = []
#
#
#     for x in maperms:
#         dfma=df[(df['MA Profile']==x)]
#         mal=len(dfma.index)
#         maprofilestr=x
#         for x in range(len(rsigradrange) - 1):  # initialy sort sby gradient
#             dfgrad = dfma[(dfma["rsigrad"] >= rsigradrange[x]) & (dfma["rsigrad"] >= rsigradrange[x + 1])]
#             rsigradstr = " " + str(rsigradrange[x]) + " " + str(rsigradrange[x + 1])
#
#             for x in range(len(rsilist) - 1):  # then sorts by rsi value
#                 df40 = dfgrad[(dfgrad['RSI'] >= rsilist[x]) & (dfgrad['RSI'] < rsilist[x + 1])]
#                 rsi40 = len(df40.index)  # has total number of rows within that rsi range
#                 if rsi40 != 0:  # incase that rsi range has no values
#                     nval.append(rsi40)
#
#                     df40u1 = df40[df40['p1'] > 0]  # new df of values within range selected that have probability of +1
#                     rsi40u1 = len(df40u1.index)  # length of this df gives number of times it move sup within this rsi range
#                     df40u2 = df40[df40['p2'] > 0]  # does the same withi p2
#                     rsi40u2 = len(df40u2.index)
#                     df40n1 = df40[df40['p1'] < 0]
#                     rsi40n1 = len(df40n1.index)
#
#                     probu40 = ((
#                                            rsi40u1 + rsi40u2) / rsi40)  # number of times it moves up divided by number of times at this range gives probability
#                     probd40 = (rsi40n1 / rsi40)
#                     rsirange.append(" " + str(rsilist[x]) + " " + str(rsilist[x + 1]))
#                     rsigradcol.append(rsigradstr)
#                     maprofile.append(maprofilestr)
#                     probu.append(probu40)
#                     probd.append(probd40)
#
#                 else:
#                     pass
#
#         else:
#             pass
#
#     dfmas = pd.DataFrame({'MA Profile': [], 'RSI Range': [], 'RSI Gradient' :[], 'Probability Up': [], 'Probability Down': []})
#     dfmas['MA Profile'] = maprofile
#     dfmas['Probability Up']=probu
#     dfmas['Probability Down'] = probd
#     dfmas['RSI Range']=rsirange
#     dfmas['RSI Gradient']=rsigradcol
#     dfmas['Nvalue'] = nval
#
#
#
#
#
#
#
#
#     probu = []
#     probd = []
#     nval = []
#
#
#
#     spreadratios = {1: 0.25, 2: 0.75, 3: 1.25, 4: 2.0, 5: 3.0, 6: 4.0, 7: 5.0,8:8.0}
#
#     for x in range(1,4):
#         dfb=dfbreak[x][0]
#         nb=dfbreak[x][1]
#         st = dfb[dfb['Spread Grad'] < 0]
#         sq = dfb[dfb['Spread Grad'] > 0]
#         dflist = {1: [st, "st"], 2: [sq, "sq"]}
#         for x in range(1,3):
#             dfstsq=dflist[x][0]
#             n=dflist[x][1]
#
#             for x in range(1,8):
#                 dfnew = dfstsq[(dfstsq['Spread Ratio'] >= (spreadratios[x])) & (dfstsq['Spread Ratio'] < (spreadratios[x + 1]))]  # makes new df with selcted rsi range that already has probability of that rsi range moving up
#                 dfnewl = len(dfnew.index)  # has total number of rows within that rsi range
#                 if dfnewl != 0: #incase that rsi range has no values
#                     nval.append(dfnewl)
#
#                     dfnewu1=dfnew[dfnew['p1']>0] #new df of values within range selected that have probability of +1
#                     dfnewlu1 = len(dfnewu1.index) #length of this df gives number of times it move sup within this rsi range
#                     dfnewu2=dfnew[dfnew['p2']>0] #does the same withi p2
#                     dfnewlu2 = len(dfnewu2.index)
#                     dfnewn1=dfnew[dfnew['p1']<0]
#                     dfnewln1 = len(dfnewn1.index)
#
#                     probunow=((dfnewlu1+dfnewlu2)/dfnewl) #number of times it moves up divided by number of times at this range gives probability
#                     probdnow=(dfnewln1/dfnewl)
#                     bbprofile.append(nb+" "+n+" "+str(spreadratios[x]) + " " + str(spreadratios[x+1]))
#                     probu.append(probunow)
#                     probd.append(probdnow)
#
#                 else:
#                     pass
#
#
#     bbprobs = pd.DataFrame({'bbprofile': [], 'Probability Up': [], 'Probability Down': []})  # makes df of probabilities at rsi ranges
#     bbprobs['bbprofile'] = bbprofile
#     bbprobs['Probability Up'] = probu
#     bbprobs['Probability Down'] = probd
#     bbprobs['Nvalue'] = nval
#
#     dfup = df[df['Histogram'] > 0]
#     dfdown = df[df['Histogram'] < 0]
#
#     upup = dfup[dfup['Histogram Gradient'] > 0]
#     updown = dfup[dfup['Histogram Gradient'] < 0]
#     downup = dfdown[dfdown['Histogram Gradient'] > 0]
#     downdown = dfdown[dfdown['Histogram Gradient'] < 0]
#     listdfmacd = [upup, updown, downup, downdown]
#     macdlist = ['upup', 'updown', 'downup', 'downdown']
#     rsigradrange = {0: -5, 1: -3, 2: -1, 3: 0, 4: 1, 5: 3, 6: 5}
#     rsilist = {0: 10, 1: 20, 2: 30, 3: 40, 4: 60, 5: 70, 6: 80, 7: 90}  # ranges of rsis
#     rsirange = []  # list of ranges to be used in df
#     rsigradcol = []
#     macdcol=[]
#     probu = []  # list of probability going up to be used
#     probd = []
#     nval = []
#
#     for x in range(len(listdfmacd)):
#         dfuse=listdfmacd[x]
#         macdstr=macdlist[x]
#         for x in range(len(rsigradrange) - 1):  # initialy sort sby gradient
#             dfgrad = dfuse[(dfuse["rsigrad"] >= rsigradrange[x]) & (dfuse["rsigrad"] >= rsigradrange[x + 1])]
#             rsigradstr = " " + str(rsigradrange[x]) + " " + str(rsigradrange[x + 1])
#
#             for x in range(len(rsilist) - 1):  # then sorts by rsi value
#                 df40 = dfgrad[(dfgrad['RSI'] >= rsilist[x]) & (dfgrad['RSI'] < rsilist[x + 1])]
#                 rsi40 = len(df40.index)  # has total number of rows within that rsi range
#                 if rsi40 != 0:  # incase that rsi range has no values
#                     nval.append(rsi40)
#
#                     df40u1 = df40[df40['p1'] > 0]  # new df of values within range selected that have probability of +1
#                     rsi40u1 = len(df40u1.index)  # length of this df gives number of times it move sup within this rsi range
#                     df40u2 = df40[df40['p2'] > 0]  # does the same withi p2
#                     rsi40u2 = len(df40u2.index)
#                     df40n1 = df40[df40['p1'] < 0]
#                     rsi40n1 = len(df40n1.index)
#
#                     probu40 = ((
#                                            rsi40u1 + rsi40u2) / rsi40)  # number of times it moves up divided by number of times at this range gives probability
#                     probd40 = (rsi40n1 / rsi40)
#                     rsirange.append(" " + str(rsilist[x]) + " " + str(rsilist[x + 1]))
#                     rsigradcol.append(rsigradstr)
#                     macdcol.append(macdstr)
#                     probu.append(probu40)
#                     probd.append(probd40)
#
#                 else:
#                     pass
#
#     rsimacdprobs = pd.DataFrame({'MACD Profile':[],'RSI Range': [], 'RSI Gradient': [], 'Probability Up': [],
#                              'Probability Down': []})  # makes df of probabilities at rsi ranges
#     rsimacdprobs['MACD Profile'] = macdcol
#     rsimacdprobs['RSI Range'] = rsirange
#     rsimacdprobs['Probability Up'] = probu
#     rsimacdprobs['Probability Down'] = probd
#     rsimacdprobs['RSI Gradient'] = rsigradcol
#     rsimacdprobs['Nvalue'] = nval
#
#     if valuechange==1:
#
#         df.to_csv(path + ticker + "short" + "full" + str(listdf[chartinterval])+".csv", index=False)
#     else:
#         pass
#     print("done")
#     return rsiprobs,bbprobs,maratioprobs,rsimacdprobs,dfmas
#
# def cprofile(ticker,chartinterval):
#
#     rsigradnum = {1: 20, 2: 10, 3: 10, 4: 6, 5: 5, 6: 5}
#     rsigradn = rsigradnum[chartinterval]
#     df = dffix(listdf, chartinterval, 0, ticker,path2)
#     rsi=fval(df,'RSI',0)
#     rsigradient=(df.loc[df.index[0], 'RSI'] - df.loc[df.index[0 + rsigradn], 'RSI']) / rsigradn
#
#     histgrad=(fval(df, 'Histogram', 0) - fval(df, 'Histogram', (3))) / 4
#     histo=fval(df,'Histogram',0)
#     if histo >0 and histgrad >0:
#         macd="upup"
#     elif histo >0 and histgrad <0:
#         macd="updown"
#     elif histo <0 and histgrad >0:
#         macd="downup"
#     elif histo <0 and histgrad <0:
#         macd="downdown"
#     else:
#         print("No MACD specification")
#
#     y = (fval(df, '25MA', 0)) < (fval(df, '50MA', 0))
#     q = (fval(df, '25MA', 0)) < (fval(df, '100MA', 0))
#     r = (fval(df, '25MA', 0)) < (fval(df, '200MA', 0))
#     s = (fval(df, '50MA', 0)) < (fval(df, '100MA', 0))
#
#
#     maprofile=str([y, q, r, s])
#     spreadgrad = (fval(df, 'Upper', 20) - fval(df, 'Lower', 20)) - (fval(df, 'Upper', 0) - fval(df, 'Lower', (0)))
#     if spreadgrad<0:
#         stsq="st"
#     else:
#         stsq="sq"
#     df['Spread'] = df["Upper"] - df['Lower']
#     spreadratio= fval(df, 'Spread',0) / (df['Spread']).median()
#
#     if fval(df, 'Upper', 0) < fval(df, 'close', 0):
#         breakbb="breakover"
#     elif fval(df, 'Lower', 0) > fval(df, 'close', 0):
#         breakbb="breakunder"
#     else:
#         breakbb="within"
#     maratio=((fval(df,'close',0)-fval(df,"25MA",0))/fval(df,'close',0))*100
#     return rsi,rsigradient, macd,maprofile, breakbb, spreadratio, stsq, maratio,





charttime=[1,2,3,4,5,6]
tickerlist={0:"\TVC_USOIL, ",1:r'\NASDAQ_MSFT, ',2:r"\NASDAQ_AAPL, ",3:"\SPCFD_S5INFT, ",4:"\SPCFD_SPX, ",5:"\TVC_NDX, "}
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'}
change = [0.5,0.75,1,1.25,1.5,2,2.5,3]
zex = {1:[0,"rsiprob"],2:[1,"macdprob"],3:[2,"maprob"],4:[3,"bbprob"],5:[4,"maratioprob"]}
numberbarss={1:120,2:48,3:20,4:6,5:4,6:2} #for various chart intervals the number of bars forward that are to be looked at varies
    #i.e. This is because i would want a trade to have a time range of about 30mins-4 hours e.g. for minute bars 120 is required for hour bars 3 is required
numberbarsl={1:240,2:60,3:24,4:8,5:8,6:4}
fullframe()



def selector():

    shlo=input("Would you like to see short term or longterm?: s/l")
    if shlo=="s":
        numberbars=numberbarss
        print("These are the selected data ranges" + str(numberbars))
    elif shlo == "l":
        numberbars=numberbarsl
        print("These are the selected data ranges" + str(numberbars))
    else:
        print("No type selected returning to start")
        return

    auto=input("Would you like to automate save to excel: y/n")
    if auto=="y":
        typeprob=input("What Methodology would you like to use: s(Seperate), i(integrated), b(Both)")
        if typeprob=="s":
            typeprobname="Sep"
            for x in range(len(tickerlist)):
                ticker=tickerlist[3]
                for y in range(5,6):
                    values={}
                    chartinterval=y
                    nb = numberbars[y]
                    rsiplist=[]
                    maratioplist=[]
                    bbplist=[]
                    rsimacdlist=[]
                    marsilist=[]
                    for z in change:
                        listp=seperatevar(ticker,chartinterval,z,nb)
                        for x in listp:
                            x['Value Change'] = z
                        rsip = listp[0]
                        bbp = listp[1]
                        maratiop = listp[2]
                        rsimacd = listp[3]
                        marsi = listp[4]
                        rsiplist.append(rsip)
                        maratioplist.append(maratiop)
                        bbplist.append(bbp)
                        rsimacdlist.append(rsimacd)
                        marsilist.append(marsi)
                    allindicators={0:[rsiplist,"rsip"],1:[maratioplist,"maratiop"],2:[bbplist,"bbp"],3:[rsimacdlist,"rsimacdp"],4:[marsilist,"marsip"]}
                    for x in range(len(allindicators)):

                        df1=pd.concat(allindicators[x][0])
                        df1.to_csv(path + ticker + "short" +typeprobname + str(allindicators[x][1]) + str(listdf[chartinterval])+".csv", index=False)
                    print("done")

        else:
            print("No type selected")
    elif auto=="n":
        print(tickerlist)
        tickersel=int(input("What ticker would you like to select? "))
        ticker=tickerlist[tickersel]
        timep=int(input("What time period would you like to view for?: {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'} "))

        valuec=float(input("What value change?"))
        nb= numberbars[timep]
        typeprob = input("What Methodology would you like to use: s(Seperate), i(integrated), b(Both)")

        if typeprob=="s":
            listp=seperatevar(ticker,timep, valuec, nb)
            rsip=listp[0]
            bbp=listp[1]
            maratiop=listp[2]
            rsimacd=listp[3]
            marsip=listp[4]

            print(rsip)

            print(marsip)
            print(bbp)

            print(maratiop)

            print(rsimacd)





            # for loops to comapre current values to those in probability tables
            rsips = []
            for x in range(len(rsip)):
                y = rsip.loc[rsip.index[x], "RSI Range"].split(maxsplit=-1)
                z = rsip.loc[rsip.index[x], "RSI Gradient"].split(maxsplit=-1)
                if float(y[0]) < listc[0] < float(y[1]) and float(z[0]) < listc[1] < float(z[1]):
                    print(rsip.loc[x])


                else:
                    pass
            for x in range(len(bbp)):
                y = bbp.loc[bbp.index[x], "bbprofile"].split(maxsplit=-1)

                if y[0] == listc[4] and y[1] == listc[6] and float(y[2]) <= listc[5] < float(y[3]):
                    print(bbp.loc[bbp.index[x]])
                else:
                    pass

            for x in range(len(maratiop)):
                y = maratiop.loc[maratiop.index[x], "MA Ratio Range"].split(maxsplit=-1)
                if float(y[0]) <= listc[7] < float(y[1]):
                    print(maratiop.loc[x])


                else:
                    pass

            for x in range(len(rsimacd)):
                y = rsimacd.loc[rsimacd.index[x], "RSI Range"].split(maxsplit=-1)
                z = rsimacd.loc[rsimacd.index[x], "RSI Gradient"].split(maxsplit=-1)

                if float(y[0]) < listc[0] < float(y[1]) and float(z[0]) < listc[1] < float(z[1]) and rsimacd.loc[rsimacd.index[x], "MACD Profile"]==listc[2]:
                    print(rsimacd.loc[x])


                else:
                    pass

            for x in range(len(marsip)):
                y = marsip.loc[marsip.index[x], "RSI Range"].split(maxsplit=-1)
                z = marsip.loc[marsip.index[x], "RSI Gradient"].split(maxsplit=-1)

                if float(y[0]) < listc[0] < float(y[1]) and float(z[0]) < listc[1] < float(z[1]) and marsip.loc[marsip.index[x], "MA Profile"]==listc[3]:
                    print(marsip.loc[x])


                else:
                    pass






        else:
            print("Try Again")
        start_time = time.time()


    return

# numberbarss={1:120,2:24,3:8,4:8,5:2,6:2} #for various chart intervals the number of bars forward that are to be looked at varies
#     #i.e. This is because i would want a trade to have a time range of about 30mins-4 hours e.g. for minute bars 120 is required for hour bars 3 is required
# numberbarsl={1:240,2:60,3:24,4:20,5:8,6:4}

x=input("Would you like to stop program?y/n")

while x != "y":
    selector()
    x = input("Would you like to stop program?y/n")











print ("time elapsed: {:.2f}s".format(time.time() - start_time))