
import pandas as pd
import datetime
import time
import math
import itertools

start_time = time.time()

numberbars={1:180,2:36,3:12,4:3,5:6,6:3} #for various chart intervals the number of bars forward that are to be looked at varies
    #i.e. This is because i would want a trade to have a time range of about 30mins-4 hours e.g. for minute bars 120 is required for hour bars 3 is required
path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'


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


def seperatevar(ticker,chartinterval,valuechange):

    nb = numberbars[chartinterval]
    df=dffix(listdf, chartinterval, 0, ticker)
    df['p1'] = 0  # columns for rsi probability of up or down within the number bars selected
    df['p2'] = 0
    df = priceprob(df, nb, valuechange)
    def rsiprob(df):



        rsilist=[10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85] #ranges of rsis
        rsirange=[] #list of ranges to be used in df
        probu=[] #list of probability going up to be used
        probd=[]

        for x in rsilist:
            df40=df[(df['RSI']>=x) & (df['RSI']< x+5)] #makes new df with selcted rsi range that already has probability of that rsi range moving up
            rsi40 = len(df40.index) #has total number of rows within that rsi range
            if rsi40 != 0: #incase that rsi range has no values

                df40u1=df40[df40['p1']>0] #new df of values within range selected that have probability of +1
                rsi40u1 = len(df40u1.index) #length of this df gives number of times it move sup within this rsi range
                df40u2=df40[df40['p2']>0] #does the same withi p2
                rsi40u2 = len(df40u2.index)
                df40n1=df40[df40['p1']<0]
                rsi40n1 = len(df40n1.index)

                probu40=((rsi40u1+rsi40u2)/rsi40) #number of times it moves up divided by number of times at this range gives probability
                probd40=(rsi40n1/rsi40)
                rsirange.append(" "+str(x) + "-" + str(x + 5))
                probu.append(probu40)
                probd.append(probd40)

            else:
                pass

        rsiprobs = pd.DataFrame({'RSI Range':[],'Probability Up':[],'Probability Down':[]}) #makes df of probabilities at rsi ranges
        rsiprobs['RSI Range']=rsirange
        rsiprobs['Probability Up']=probu
        rsiprobs['Probability Down']=probd
        #df.to_csv(path + "\TVC_USOIL, " + "RSI Probabilities" + ".csv", index=False)
        return rsiprobs

    def MACDprob(df):

        df['Histogram Gradient']=0
        for x in range(len(df.index)-3):
            df.loc[df.index[x], 'Histogram Gradient'] = (fval(df, 'Histogram', x) - fval(df, 'Histogram', (x+3))) / 4

            # (df.loc[df.index[x], 'Histogram Gradient'])

        df=df[df['Histogram Gradient']!=0]
        dfup=df[df['Histogram']>0]
        dfdown=df[df['Histogram']<0]

        upup=dfup[dfup['Histogram Gradient']>0]
        updown=dfup[dfup['Histogram Gradient']<0]
        downup = dfdown[dfdown['Histogram Gradient'] > 0]
        downdown = dfdown[dfdown['Histogram Gradient'] < 0]
        listdfmacd=[upup,updown,downup,downdown]
        macdlist=['upup','updown','downup','downdown']
        probu=[]
        probd=[]

        for x in listdfmacd:
            dftotal = len(x.index)
            dfup1 = x[x['p1'] > 0]
            macdup1 = len(dfup1.index)
            dfup2 = x[x['p2'] > 0]
            macdup2 = len(dfup2.index)
            dfdown1 = x[x['p1'] < 0]
            macddown1 = len(dfdown1.index)
            probu1 = ((macdup1 + macdup2) / dftotal)
            probd1 = (macddown1 / dftotal)
            probu.append(probu1)
            probd.append(probd1)

        dfmacdprob = pd.DataFrame( {'MACD':[], 'Probability Up':[], 'Probability Down':[]})
        dfmacdprob['MACD']=macdlist
        dfmacdprob['Probability Up']=probu
        dfmacdprob['Probability Down']=probd
        return dfmacdprob


    def MAprob(df):

        df['MA Profile'] = 0
        for x in range(len(df.index) - 3): #list of true false statements that comaprs to all comprarable possibilities
            y =(fval(df, '25MA', x))<(fval(df, '50MA', x))
            q =(fval(df, '25MA', x))<(fval(df, '100MA', x))
            r =(fval(df, '25MA', x))<(fval(df, '200MA', x))
            s =(fval(df, '50MA', x))<(fval(df, '100MA', x))
            z =(fval(df, '50MA', x))<(fval(df, '200MA', x))
            p =(fval(df, '100MA', x))<(fval(df, '200MA', x))

            df['MA Profile']=df['MA Profile'].astype('str') #had to convert to str to comapre lists as pandas makeslsit single values
            df.at[x,'MA Profile'] = [y,q,r,s,z,p]

        maperms = []
        l = [False, True]
        for i in itertools.product(l, repeat=6):
            maperms.append(str(list(i)))  #converts lsit added as string
        maprofile=[]
        probu=[]
        probd=[]
        for x in maperms:
            dfma=df[(df['MA Profile']==x)]
            mal=len(dfma.index)
            if mal !=0:
                dfmau1=dfma[dfma['p1']>0]
                malu1 = len(dfmau1.index)
                dfmau2 = dfma[dfma['p2'] > 0]
                malu2 = len(dfmau2.index)
                dfman1 = dfma[dfma['p1'] < 0]
                maln1 = len(dfman1.index)
                probu1=((malu1+malu2)/mal)
                probd1=(maln1/mal)
                maprofile.append(str(x))
                probu.append(probu1)
                probd.append(probd1)
            else:
                pass

        dfmas = pd.DataFrame({'MA Profile': [], 'Probability Up': [], 'Probability Down': []})
        dfmas['MA Profile'] = maprofile
        dfmas['Probability Up']=probu
        dfmas['Probability Down'] = probd
        return dfmas

    def BBprob(df):

        df['Spread'] = df["Upper"]-df['Lower']
        df['Spread Grad']=0
        df['Spread Ratio']=0
        for x in range(len(df.index) - 20):

            df.loc[df.index[x],'Spread Grad'] = (fval(df, 'Upper', x+20) - fval(df, 'Lower', (x+20)))-(fval(df, 'Upper', x) - fval(df, 'Lower', (x)))
            cspread = fval(df, 'Spread', x)
            df.loc[df.index[x],'Spread Ratio']=(cspread / (df['Spread']).median())




        probu = []
        probd = []
        bbprofile=[]
        breakover=df[df['close']>df['Upper']]
        breakunder=df[df['close']<df['Lower']]
        within=df[df['Lower']<df['close']]
        within=within[within['Upper']>within['close']]
        dfbreak={1:[breakover,"breakover"], 2:[breakunder,"breakunder"],3:[within,"within"]}

        spreadratios = {1:0.25, 2:0.5, 3:0.75, 4:1.25, 5:2, 6:3, 7:4, 8:5}

        for x in range(1,4):
            dfb=dfbreak[x][0]
            nb=dfbreak[x][1]
            st = dfb[dfb['Spread Grad'] > 0]
            sq = dfb[dfb['Spread Grad'] < 0]
            dflist = {1: [st, "st"], 2: [sq, "sq"]}
            for x in range(1,3):
                df=dflist[x][0]
                n=dflist[x][1]

                for x in range(1,8):
                    dfnew = df[(df['Spread Ratio'] >= (spreadratios[x])) & (df['Spread Ratio'] < (spreadratios[x + 1]))]  # makes new df with selcted rsi range that already has probability of that rsi range moving up
                    dfnewl = len(dfnew.index)  # has total number of rows within that rsi range
                    if dfnewl != 0: #incase that rsi range has no values

                        dfnewu1=dfnew[dfnew['p1']>0] #new df of values within range selected that have probability of +1
                        dfnewlu1 = len(dfnewu1.index) #length of this df gives number of times it move sup within this rsi range
                        dfnewu2=dfnew[dfnew['p2']>0] #does the same withi p2
                        dfnewlu2 = len(dfnewu2.index)
                        dfnewn1=dfnew[dfnew['p1']<0]
                        dfnewln1 = len(dfnewn1.index)

                        probunow=((dfnewlu1+dfnewlu2)/dfnewl) #number of times it moves up divided by number of times at this range gives probability
                        probdnow=(dfnewln1/dfnewl)
                        bbprofile.append(nb+" "+n+" "+str(spreadratios[x]) + "-" + str(spreadratios[x+1]))
                        probu.append(probunow)
                        probd.append(probdnow)

                    else:
                        pass


            bbprobs = pd.DataFrame({'bbprofile': [], 'Probability Up': [], 'Probability Down': []})  # makes df of probabilities at rsi ranges
            bbprobs['bbprofile'] = bbprofile
            bbprobs['Probability Up'] = probu
            bbprobs['Probability Down'] = probd
        return bbprobs

    dfrsi=rsiprob(df)
    dfmacd=MACDprob(df)
    dfma=MAprob(df)
    dfbb=BBprob(df)
    return dfrsi,dfmacd,dfma,dfbb

# "\SPCFD_S5INFT, ",

charttime=[1,2,3,4,5,6]
tickerlist=["\TVC_USOIL, "]
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'}
change = [0.5,1 ,1.5,2,2.5,3]
zex = {1:[0,"rsiprob"],2:[1,"macdprob"],3:[2,"maprob"],4:[3,"bbprob"]}
fullframe()

for x in tickerlist:
    ticker=x
    for y in range(1,7):
        values={}
        chartinterval=y
        for t in range(1, 5):
            g = zex[t][0]
            name = zex[t][1]
            for z in change:
                df=seperatevar(ticker,chartinterval,z)[g]
                df['Value Change'] = z
                values[z]=df
            df1=pd.concat([values[0.5],values[1],values[1.5],values[2],values[2.5],values[3]])
            df1.to_csv(path+ticker+name+str(listdf[y])+".csv", index=False)

def integratedvar(ticker,chartinterval,valuechange):

    nb = numberbars[chartinterval]
    df = dffix(listdf, chartinterval, 0, ticker)
    df['p1'] = 0  # columns for rsi probability of up or down within the number bars selected
    df['p2'] = 0
    df = priceprob(df, nb, valuechange)


print ("time elapsed: {:.2f}s".format(time.time() - start_time))
