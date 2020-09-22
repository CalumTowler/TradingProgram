
import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools
start_time = time.time()

# #
# # path = r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data\6 months prior'
# path2=r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data'
#
path = r'D:\OneDrive\Oracle\Trading Program\Stock Data\6 months prior'
path2=r'D:\OneDrive\Oracle\Trading Program\Stock Data'
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'}
tickerlist=["\TVC_USOIL, ","\SPCFD_S5INFT, "]
listindicator=["rsiprob","macdprob","maprob","bbprob"]
tplist=["60"]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
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

def fval(df,column,val):
    value = (df.loc[df.index[val], column])
    return value

df=dffix(listdf, 4, 0, tickerlist[0])
df['p1'] = 0  # columns for rsi probability of up or down within the number bars selected
df['p2'] = 0
df = priceprob(df, 6, 1.5)

df["rsigrad"]=0

df["timedate"] = 0
df["Support Fib"]=0
df["Resistance Fib"]=0
df["P Fib"]=0
for x in range(len(df)):  # remove current day from experiment
    df.loc[df.index[x], "timedate"] = (df.loc[df.index[x], "time"].date())  # makes date only column
interval=4
if interval<4:
    dffib=dffix(listdf,6,1,tickerlist[0])
else:
    dffib=dffix(listdf,7,1,tickerlist[0])
for x in range(len(df)):

    currentdate = df.loc[df.index[x], "timedate"]
    for y in range(len(df)):
        if df.loc[df.index[y], "timedate"]==currentdate:
            high = fval(dffib, 'high', 0)
            low = fval(dffib, 'low', 0)
            close = fval(dffib, 'close', 0)
            pp = round((high + low + close) / 3, 2)
            flevels = [0.382, 0.618, 1.0]
            SF = []
            RF = []
            for x in flevels:
                rf = round((pp + ((high - low) * x)), 2)
                RF.append(rf)

                sf = round((pp - ((high - low) * x)), 2)
                SF.append(sf)
            df.loc[df.index[y], "Support Fib"]=SF
            df.loc[df.index[y], "Resistance Fib"]=RF
            df.loc[df.index[y], "P Fib"]=pp


print(df)




rsigradnum={1:20,2:10,3:10,4:6,5:5,6:5}
rsigradn=rsigradnum[4]
for x in range(len(df)-rsigradn):
    df.loc[df.index[x], 'rsigrad']=(df.loc[df.index[x],'RSI']-df.loc[df.index[x+rsigradn],'RSI'])/rsigradn #rsigradient calc


df["Candlestick"]=0
candlesticks=["Green Hammer","Green Inverted Hammer","Red Hanging Man","Red Shooting Star"]
candlecolour=["Green","Green","Red","Red"]
bodysize=["0.15 0.8","0.15 0.8","0.15 0.8","0.15 0.8"]
lowershadow=["1 4","0 0.15","1 4","0 0.15"]
uppershadow=["0 0.15","1 4","0 0.15","1 4"]
priorcandle=["Open Higher","Open Higher","Open Lower","Open Lower"]
dfcandles=pd.DataFrame({'Candlestick':candlesticks,'Candle Colour': candlecolour, 'Body Size': bodysize, 'L Shadow': lowershadow, 'U Shadow':uppershadow, 'Prior Candle': priorcandle})
print(dfcandles)
dfcandles
for x in range(len(df)-1):
    high=fval(df,"high",x)
    low=fval(df,"low",x)
    close=fval(df,"close",x)
    open=fval(df,"open",x)
    phigh = fval(df, "high", (x+1))
    plow = fval(df, "low", (x+1))
    pclose = fval(df, "close", (x+1))
    popen = fval(df, "open", (x+1))
    bodysize=100*(abs(close-open)/open)

    if open>close:
        candlestickcolour = "Red"
        lshadow=(close-low)
        if lshadow!=0:
            lshadow=(lshadow/bodysize)
        else:
            lshadow=0
        ushadow=(high-open)
        if ushadow!=0:
            ushadow=(ushadow/bodysize)
        else:
            ushadow=0
        if open<=popen:
            priorcandle="Open Higher"
        elif open>=popen:
            priorcandle="Open Lower"
        else:
            pass


    elif close>open:
        candlestickcolour = "Green"
        lshadow = (open - low)
        if lshadow != 0:
            lshadow = (lshadow/bodysize)
        else:
            lshadow = 0
        ushadow = (high - close)
        if ushadow != 0:
            ushadow = (ushadow/bodysize)
        else:
            ushadow = 0
        if open <= popen:
            priorcandle = "Open Higher"
        elif open >= popen:
            priorcandle = "Open Lower"
        else:
            pass

    else:
        candlestick = "Doji"
    for y in range(len(dfcandles)):

        bodysizerange=fval(dfcandles,"Body Size",y).split(maxsplit=-1)
        lshadowrange=fval(dfcandles,"L Shadow",y).split(maxsplit=-1)
        ushadowrange=fval(dfcandles,"U Shadow",y).split(maxsplit=-1)

        if fval(dfcandles,"Candle Colour",y)==candlestickcolour and float(bodysizerange[0])<=bodysize<=float(bodysizerange[1]) and float(lshadowrange[0])<=lshadow<=float(lshadowrange[1])\
                and float(ushadowrange[0])<=ushadow<=float(ushadowrange[1]): #and fval(dfcandles, "Prior Candle",y)==priorcandle:
            df.loc[df.index[x], "Candlestick"] = fval(dfcandles,"Candlestick",y)
            break
        else:
            pass


df["Relative Volume"]=0
for x in range(len(df)):
    if df.loc[df.index[x], "Volume"]>df.loc[df.index[x], "VMA"]:
        df.loc[df.index[x], "Relative Volume"]="High Volume"
    else:
        df.loc[df.index[x], "Relative Volume"]="Low Volume"
listcandles=[]
print(dfcandles)
for x in range(len(dfcandles)):
    listcandles.append(dfcandles.loc[dfcandles.index[x], "Candlestick"])
print(listcandles)
rsigradrange = {0: -5,1: -2, 2: 0, 3: 2, 4: 5}
rsilist = {0: 10, 1: 30, 2: 40, 3: 60, 4: 70, 5: 90}
rsirange = []  # list of ranges to be used in df
rsigradcol = []
candlestickcolumn=[]
probu = []  # list of probability going up to be used
probd = []
nval=[]
maprofile=[]
df['MA Profile'] = 0
for x in range(len(df.index) - 3): #list of true false statements that comaprs to all comprarable possibilities
    y =(fval(df, '25MA', x))<(fval(df, '50MA', x))
    q =(fval(df, '25MA', x))<(fval(df, '100MA', x))



    df['MA Profile']=df['MA Profile'].astype('str') #had to convert to str to comapre lists as pandas makeslsit single values
    df.at[x,'MA Profile'] = [y,q]

maperms = []
l = [False, True]
for i in itertools.product(l, repeat=2):
    maperms.append(str(list(i)))  #converts lsit added as string
maprofile=[]

for x in maperms:
    dfma = df[(df['MA Profile'] == x)]

    maprofilestr = x
    for x in listcandles:
        dfcandle=df[(df["Candlestick"]==x)]
        dfcandle=dfcandle[(dfcandle["Relative Volume"]=="High Volume")]
        candlestring=x
        for x in range(len(rsigradrange) - 1):  # initialy sort sby gradient
            dfgrad = dfcandle[(dfcandle["rsigrad"] >= rsigradrange[x]) & (dfcandle["rsigrad"] >= rsigradrange[x + 1])]
            rsigradstr = " " + str(rsigradrange[x]) + " " + str(rsigradrange[x + 1])

            for x in range(len(rsilist) - 1):  # then sorts by rsi value
                df40 = dfgrad[(dfgrad['RSI'] >= rsilist[x]) & (dfgrad['RSI'] < rsilist[x + 1])]
                rsi40 = len(df40.index)  # has total number of rows within that rsi range
                if rsi40 != 0:  # incase that rsi range has no values
                    nval.append(rsi40)
                    df40u1 = df40[df40['p1'] > 0]  # new df of values within range selected that have probability of +1
                    rsi40u1 = len(df40u1.index)  # length of this df gives number of times it move sup within this rsi range
                    df40u2 = df40[df40['p2'] > 0]  # does the same withi p2
                    rsi40u2 = len(df40u2.index)
                    df40n1 = df40[df40['p1'] < 0]
                    rsi40n1 = len(df40n1.index)

                    probu40 = ((
                                           rsi40u1 + rsi40u2) / rsi40)  # number of times it moves up divided by number of times at this range gives probability
                    probd40 = (rsi40n1 / rsi40)
                    rsirange.append(" " + str(rsilist[x]) + " " + str(rsilist[x + 1]))
                    rsigradcol.append(rsigradstr)
                    candlestickcolumn.append(candlestring)
                    maprofile.append(maprofilestr)
                    probu.append(probu40)
                    probd.append(probd40)

                else:
                    pass

rsimacdprobs = pd.DataFrame({'Candlestick':[],'RSI Range': [], 'RSI Gradient': [], 'Probability Up': [],'Probability Down': []})  # makes df of probabilities at rsi ranges
rsimacdprobs['Candlestick'] = candlestickcolumn
rsimacdprobs['RSI Range'] = rsirange
rsimacdprobs['Probability Up'] = probu
rsimacdprobs['Probability Down'] = probd
rsimacdprobs['RSI Gradient'] = rsigradcol
rsimacdprobs['Nvalue']=nval
rsimacdprobs["MA Profile"]=maprofile

newdf = rsimacdprobs[rsimacdprobs["Nvalue"]>2]
print(newdf[newdf["Probability Up"]>=0.5])
print(newdf[newdf["Probability Down"]>=0.5])

candlestickcolumn=[]
probu = []  # list of probability going up to be used
probd = []
nval=[]

for x in listcandles:
    dfcandle=df[(df["Candlestick"]==x)]
    dfcandle=dfcandle[(dfcandle["Relative Volume"]=="High Volume")]
    candlestring=x
    numberof=len(dfcandle)
    if numberof != 0:  # incase that rsi range has no values
        nval.append(numberof)
        df40u1 = dfcandle[dfcandle['p1'] > 0]  # new df of values within range selected that have probability of +1
        rsi40u1 = len(df40u1.index)  # length of this df gives number of times it move sup within this rsi range
        df40u2 = dfcandle[dfcandle['p2'] > 0]  # does the same withi p2
        rsi40u2 = len(df40u2.index)
        df40n1 = dfcandle[dfcandle['p1'] < 0]
        rsi40n1 = len(df40n1.index)

        probu40 = ((rsi40u1 + rsi40u2) / numberof)  # number of times it moves up divided by number of times at this range gives probability
        probd40 = (rsi40n1 / numberof)
        candlestickcolumn.append(candlestring)
        probu.append(probu40)
        probd.append(probd40)
    else:
        pass

rsimacdprobs = pd.DataFrame({'Candlestick':[], 'Probability Up': [],'Probability Down': []})  # makes df of probabilities at rsi ranges
rsimacdprobs['Candlestick'] = candlestickcolumn
rsimacdprobs['Probability Up'] = probu
rsimacdprobs['Probability Down'] = probd
rsimacdprobs['Nvalue']=nval
print(rsimacdprobs)


