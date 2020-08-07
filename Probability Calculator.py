
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
    print('Current time is ' + str(df.loc[df.index[0], 'time']))

    return df



def fval(df,column,val):
    value = (df.loc[df.index[val], column])
    return value

def rsiprob(valuechange, chartinterval):

    numberbars={1:180,2:36,3:12,4:3,5:1,6:1}
    nb=numberbars[chartinterval]

    df=dffix(listdf,chartinterval,0)
    df['RSIp1']=0
    df['RSIp2']=0



    for x in range((len(df.index)-nb)):
        cprice = fval(df, 'close', x+nb)
        crsi = fval(df, 'RSI', x+nb)

        npriced = fval(df, 'low', x)
        npriceu=fval(df,'high',x)
        percent = (cprice / 100) * valuechange
        xlst=range(nb)
        for x in xlst:
            npriced = fval(df, 'low', x)

        d = cprice - npriced
        u = npriceu - cprice
        if u>percent and d >percent:
            p1=1
            p2=-1
        else:
            p2=0
            if d > percent:
                p1 = -1

            elif u > percent:
                p1 = 1

            else:
                p1 = 0


        df.loc[df.index[x+nb], 'RSIp1']=p1
        df.loc[df.index[x + nb], 'RSIp2'] = p2

    print(df[['time','RSI','RSIp1','RSIp2','close','high','low']])


    rsilist=[10,20,30,40,50,60,70,80]

    rsirange=[]
    probu=[]
    probd=[]

    for x in rsilist:
        df40=df[(df['RSI']>=x) & (df['RSI']< x+10)]
        rsi40 = len(df40.index)
        if rsi40 != 0:

            df40u1=df40[df40['RSIp1']>0]
            rsi40u1 = len(df40u1.index)
            df40n1=df40[df40['RSIp1']<0]
            rsi40n1 = len(df40n1.index)

            probu40=(rsi40u1/rsi40)
            probd40=(rsi40n1/rsi40)
            rsirange.append(str(x) + "-" + str(x + 10))
            probu.append(probu40)
            probd.append(probd40)

        else:
            pass




    rsiprobs = pd.DataFrame({'RSI Range':[],'Probability Up':[],'Probability Down':[]})
    rsiprobs['RSI Range']=rsirange
    rsiprobs['Probability Up']=probu
    rsiprobs['Probability Down']=probd
    print(rsiprobs)
    return rsiprobs

rsiprob(1.5,5)

print ("time elapsed: {:.2f}s".format(time.time() - start_time))