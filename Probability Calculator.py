
import pandas as pd
import datetime
import time
import math




#function to fix and subsequently call correct df

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)
start_time = time.time()
path = r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data'
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D',7:'1W'}



def dffix(list,x,tp):
    excel1 = path + "\TVC_USOIL, " + str(list[x]) + ".csv"
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
    #print('Current time is ' + str(df.loc[df.index[0], 'time']))

    return df



def fval(df,column,val):
    value = (df.loc[df.index[val], column])
    return value

def rsiprob(valuechange, chartinterval):

    numberbars={1:180,2:36,3:12,4:3,5:1,6:1} #for various chart intervals the number of bars forward that are to be looked at varies
    #i.e. This is because i would want a trade to have a time range of about 30mins-4 hours e.g. for minute bars 120 is required for hour bars 3 is required
    nb=numberbars[chartinterval]

    df=dffix(listdf,chartinterval,0)
    df['RSIp1']=0 #columns for rsi probability of up or down within the number bars selected
    df['RSIp2']=0

    for x in range((len(df.index) - nb)): #this itterates over every row in the dataframe except the top rows where forward data is not available
        cprice = fval(df, 'close', x + nb) #current price
        xlst = range(nb) #gives forward bar indexes as list
        p1list = [] #list of probabilities for range of forward bars
        p2list=[] #this list is for probabilities if the value change is both up and down by the required amount i.e. moves 1% up and down in net 3 hours
        for y in xlst:
            npriced = fval(df, 'low', x) #low of bar
            npriceu = fval(df, 'high', x) #high of bar
            percent = (cprice / 100)*valuechange

            d = cprice - npriced #different between forward price and current price being exaimned
            u = npriceu - cprice
            if u > percent and d > percent: #for conditions where both up and down value changes occur
                p1 = 1
                p2 = -1
            else:
                p2 = 0
                if d > percent: #down by value occurs
                    p1 = -1

                elif u > percent: #up by value occurs
                    p1 = 1

                else:
                    p1 = 0
            p1list.append(p1) #list of values
            p2list.append(p2)
        pu1 = [x for x in p1list if x > 0] #list of positive value moves
        pd1 = [x for x in p1list if x < 0] #lsit of neg value moves
        pd2 = [x for x in p2list if x < 0] #list of neg value moves if both neg and pos occur
        if len(pd2) > 0: #if both occur then 2 probabilities are entered
            p11 = -1
            p22 = 1
        else:
            p22 = 0 #if only one value change occurs
            if len(pu1) > 0: #if list has any values in it then a value chnage up occured thus rsi has preceded an upwards movement
                p11 = 1

            elif len(pd1) > 0:
                p11 = -1

            else:
                p11 = 0

        df.loc[df.index[x + nb], 'RSIp1'] = p11 #assign these values to df column
        df.loc[df.index[x + nb], 'RSIp2'] = p22


    #print(df[['time','RSI','RSIp1','RSIp2','close','high','low']])


    rsilist=[10,20,30,40,50,60,70,80] #ranges of rsis

    rsirange=[] #list of ranges to be used in df
    probu=[] #list of probability going up to be used
    probd=[]

    for x in rsilist:
        df40=df[(df['RSI']>=x) & (df['RSI']< x+10)] #makes new df with selcted rsi range that already has probability of that rsi range moving up
        rsi40 = len(df40.index) #has total number of rows within that rsi range
        if rsi40 != 0: #incase that rsi range has no values

            df40u1=df40[df40['RSIp1']>0] #new df of values within range selected that have probability of +1
            rsi40u1 = len(df40u1.index) #length of this df gives number of times it move sup within this rsi range
            df40u2=df40[df40['RSIp2']>0] #does the same withi p2
            rsi40u2 = len(df40u2.index)
            df40n1=df40[df40['RSIp1']<0]
            rsi40n1 = len(df40n1.index)

            probu40=((rsi40u1+rsi40u2)/rsi40) #number of times it moves up divided by number of times at this range gives probability
            probd40=(rsi40n1/rsi40)
            rsirange.append(" "+str(x) + "-" + str(x + 10))
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

# change = [0.5,1 ,1.5,2,2.5,3]
# charttime=[1,2,3,4,5,6]
# chartime={}
# for x in charttime:
#     values={}
#     print('Curent chart period is '+str(listdf[x]))
#     for y in change:
#         print('value change is ' + str(y))
#         df=rsiprob(y,x)
#         df['Value Change']=y
#         #print(df)
#         values[y]=df
#         #print(values[y])
#
#     df1=(values[0.5])
#     df2=pd.DataFrame(values[1])
#     df3=values[1.5]
#     #df1=pd.concat([df1,df2,df3],axis=0)
#     df1=pd.concat([values[0.5],values[1],values[1.5],values[2],values[2.5],values[3]],axis=0)
#     df1 = df1.reset_index(drop=True)  # reset index
#     print(df1)
#     df1.to_csv(path + "\TVC_USOIL, " + "RSI Probabilities" + str(x)+".csv", index=False)
# print ("time elapsed: {:.2f}s".format(time.time() - start_time))

# df.to_csv(path + "\TVC_USOIL, " + "RSI Probabilities" + ".csv", index=False)

def MACDprob(chartinterval, valuechange):
    numberbars = {1: 180, 2: 36, 3: 12, 4: 3, 5: 1, 6: 1}  # for various chart intervals the number of bars forward that are to be looked at varies
    # i.e. This is because i would want a trade to have a time range of about 30mins-4 hours e.g. for minute bars 120 is required for hour bars 3 is required
    nb = numberbars[chartinterval]

    df=dffix(listdf,chartinterval,0)
    print(df['time'])
    df['Histogram Gradient']=0
    for x in range(len(df.index)-3):
        df.loc[df.index[x], 'Histogram Gradient'] = (fval(df, 'Histogram', x) - fval(df, 'Histogram', (x+3))) / 4

        # (df.loc[df.index[x], 'Histogram Gradient'])

    df=df[df['Histogram Gradient']!=0]

    df['MACDp1']=0
    df['MACDp2']=0



    for x in range((len(df.index) - nb)):  # this itterates over every row in the dataframe except the top rows where forward data is not available
        cprice = fval(df, 'close', x + nb)  # current price
        xlst = range(nb)  # gives forward bar indexes as list
        p1list = []  # list of probabilities for range of forward bars
        p2list = []  # this list is for probabilities if the value change is both up and down by the required amount i.e. moves 1% up and down in net 3 hours
        for y in xlst:
            npriced = fval(df, 'low', x)  # low of bar
            npriceu = fval(df, 'high', x)  # high of bar
            percent = (cprice / 100) * valuechange

            d = cprice - npriced  # different between forward price and current price being exaimned
            u = npriceu - cprice
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
        df.loc[df.index[x + nb], 'MACDp1'] = p11  # assign these values to df column
        df.loc[df.index[x + nb], 'MACDp2'] = p22

        dfup=df[df['Histogram']>0]
        dfdown=df[df['Histogram']<0]


        histgrad=[#different gradient ranges based on ]
        #     rsirange = []  # list of ranges to be used in df
        # probu = []  # list of probability going up to be used
        # probd = []
        #
        # for x in rsilist:
        #     df40 = df[(df['RSI'] >= x) & (df[
        #                                       'RSI'] < x + 10)]  # makes new df with selcted rsi range that already has probability of that rsi range moving up
        # rsi40 = len(df40.index)  # has total number of rows within that rsi range
        # if rsi40 != 0:  # incase that rsi range has no values
        #
        #     df40u1 = df40[df40['RSIp1'] > 0]  # new df of values within range selected that have probability of +1
        # rsi40u1 = len(df40u1.index)  # length of this df gives number of times it move sup within this rsi range
        # df40u2 = df40[df40['RSIp2'] > 0]  # does the same withi p2
        # rsi40u2 = len(df40u2.index)
        # df40n1 = df40[df40['RSIp1'] < 0]
        # rsi40n1 = len(df40n1.index)
        #
        # probu40 = ((
        #                        rsi40u1 + rsi40u2) / rsi40)  # number of times it moves up divided by number of times at this range gives probability
        # probd40 = (rsi40n1 / rsi40)
        # rsirange.append(str(x) + "-" + str(x + 10))
        # probu.append(probu40)
        # probd.append(probd40)
        #
        # else:
        # pass
        #
        # rsiprobs = pd.DataFrame(
        #     {'RSI Range': [], 'Probability Up': [], 'Probability Down': []})  # makes df of probabilities at rsi ranges
        # rsiprobs['RSI Range'] = rsirange
        # rsiprobs['Probability Up'] = probu
        # rsiprobs['Probability Down'] = probd


    return

MACDprob(2,1)