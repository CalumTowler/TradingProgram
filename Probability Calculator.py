
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
path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'
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

df1h=dffix(listdf,4,0)

df1h['RSIp1']=0
df1h['RSIp2']=0



for x in range((len(df1h.index)-3)):
    cprice = fval(df1h, 'close', x+3)
    crsi = fval(df1h, 'RSI', x+3)
    npriced = fval(df1h, 'low', x)
    npriceu=fval(df1h,'high',x)
    percent = cprice / 100

    d = cprice - npriced
    u = npriceu- cprice
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


    df1h.loc[df1h.index[x+3], 'RSIp1']=p1
    df1h.loc[df1h.index[x + 3], 'RSIp2'] = p2

print(df1h[['time','RSI','RSIp1','RSIp2','close','high','low']])

#df1h40=df1h[df1h['RSI'].between(10,20,inclusive=True)]

rsilist=[10,20,30,40,50,60,70,80]

rsirange=[]
probu=[]
probd=[]

for x in rsilist:
    df1h40=df1h[(df1h['RSI']>=x) & (df1h['RSI']< x+10)]
    rsi40 = len(df1h40.index)
    if rsi40 != 0:

        df1h40u1=df1h40[df1h40['RSIp1']>0]
        rsi40u1 = len(df1h40u1.index)
        df1h40n1=df1h40[df1h40['RSIp1']<0]
        rsi40n1 = len(df1h40n1.index)

        probu40=(rsi40u1/rsi40)
        probd40=(rsi40n1/rsi40)


    else:
        pass
    rsirange.append(str(x)+"-"+str(x+10))
    probu.append(probu40)
    probd.append(probd40)



rsiprobs = pd.DataFrame({'RSI Range':[],'Probability Up':[],'Probability Down':[]})
rsiprobs['RSI Range']=rsirange
rsiprobs['Probability Up']=probu
rsiprobs['Probability Down']=probd
print(rsiprobs)

print ("time elapsed: {:.2f}s".format(time.time() - start_time))