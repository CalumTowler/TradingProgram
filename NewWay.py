
import pandas as pd
import datetime



path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'

#brings excel file from documents
interval='1'
excel1 = path + "\TVC_USOIL, "+interval +".csv"

df1 = pd.read_csv(excel1)

#puts column headers in

df1.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
               'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
               ,'MOMMACD','MOMSignal']

df1['time'] = pd.to_datetime(df1['time']) #changes time column format to datetime
df1 = df1.iloc[::-1]
df1=df1.reset_index(drop=True) # reset so newest data is at index 0

dn = (df1.loc[df1.index[0],'time']) # newest time

#takes most recent data point

currentrsi = float(df1.loc[df1.index[1],'RSI'])


#rsi checker where p = probability of upwards movement

def rsi_checker(rsi):

    if currentrsi > 70:
        print("RSI is overbought at " + str(currentrsi))
        p=-0.75
    else:
        if currentrsi < 30:
            print("RSI is oversold at " + str(currentrsi))
            p=0.75
        else:
            print("RSi is " + str(currentrsi))
            if currentrsi>=50:
                p=((currentrsi-25)/100)
            else:
                p=((currentrsi+25)/100)
    #print(p)

    return p

#rsi_checker(currentrsi)

cMA25 = float(df1.loc[df1.index[1],'25MA'])
cMA50 = float(df1.loc[df1.index[1],'50MA'])
cMA100 = float(df1.loc[df1.index[1],'100MA'])
cMA200 = float(df1.loc[df1.index[1],'200MA'])

#establishes current trend by determining MA crosses

def trend_strength(MA25, MA50, MA100, MA200):
    print('MAs point to')
    if MA25>MA50:
        if MA50>MA100:
            if MA100>MA200:
                print('Strong Uptrend')
                p=0.75
            else:
                print('Medium Uptrend')
                p=0.5
        else:
            print('Weak Uptrend')
            p=0.25
    else:
        if MA50<MA100:
            if MA100<MA200:
                print('Strong Downtrend')
                p=-0.75
            else:
                print('Medium Downtrend')
                p=-0.75
        else:
            print('Weak Downtrend')
            p=-0.75

    #print(p)
    return p

#trend_strength(cMA25, cMA50, cMA100, cMA200)

#macd stuff

currenthistogram = float(df1.loc[df1.index[1],'Histogram'])

def macd_checker(Histogram,df,time):
    #use histogram value to determine if macd is crossed up or down
    #checking when last macd cross was

    if Histogram>0:
        print('MACD is crossed up')
        p=0.5

        rslt_df = df[df['Histogram']<0]
        print(rslt_df)


    else:
        print('MACD is crossed down')
        p=-0.5
        rslt_df = df[df['Histogram'] > 0] # finds positive histogram values to determine cross time (need to make it so it finds first value only and not make
        #massive df of all positive values  )

        #print(rslt_df)
        dt = (rslt_df.loc[rslt_df.index[0],'time']) #selects only first value
         # need to put this as outside function returns msot recent timestamp
        timed = dn-dt
        print('MACD cross occured '+ str(timed) + ' minutes ago')


    return p

#macd_checker(currenthistogram,df1)

#calculation of  probabilities
print('The date and time is ' + str(dn))
p=(trend_strength(cMA25, cMA50, cMA100, cMA200)+rsi_checker(currentrsi)+macd_checker(currenthistogram,df1,dn))
print('Trend probability is ' + str(p))