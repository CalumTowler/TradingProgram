
import pandas as pd
import datetime
import time

start_time = time.time()

# df1.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
#                'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
#                ,'MOMMACD','MOMSignal']
#
# df1['time'] = pd.to_datetime(df1['time']) #changes time column format to datetime
# df1 = df1.iloc[::-1]
# df1=df1.reset_index(drop=True) # reset so newest data is at index 0
#
# dn = (df1.loc[df1.index[0],'time']) # newest time

path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'

#brings excel file from documents
#intervals={1:['1','1min'],5:['5','5min'],15:['15','15min'],60:['60','60min'],240:['240','240min'],1440:['D','Day']}
# excel1 = path + "\TVC_USOIL, "+ '1' +".csv"
# df1 = pd.read_csv(excel1)
#
# excel1 = path + "\TVC_USOIL, "+ '5' +".csv"
# df5 = pd.read_csv(excel1)
#
# excel1 = path + "\TVC_USOIL, "+ '15' +".csv"
# df15 = pd.read_csv(excel1)
#
# excel1 = path + "\TVC_USOIL, "+ '60' +".csv"
# df60 = pd.read_csv(excel1)
#
# excel1 = path + "\TVC_USOIL, "+ '240' +".csv"
# df240 = pd.read_csv(excel1)
#
# excel1 = path + "\TVC_USOIL, "+ '1D' +".csv"
# dfd = pd.read_csv(excel1)

listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D'}
#print(listdf)

#function to fix and subsequently call correct df

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

def dffix(list,x):
    excel1 = path + "\TVC_USOIL, " + str(list[x]) + ".csv"
    df = pd.read_csv(excel1)
    print('Chart Interval is '+(str(list[x])))
    # puts column headers in
    df.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
                  'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
                  ,'MOMMACD','MOMSignal']
    df['time'] = pd.to_datetime(df['time'])  # changes time column format to datetime
    df = df.iloc[::-1] # revereses index
    df = df.reset_index(drop=True)  # reset so newest data is at index 0
    print('Current time is ' + str(df.loc[df.index[0], 'time']))
    return df

#rsi checker where p = probability of upwards movement

def fval(df,column,val):
    value = (df.loc[df.index[val], column])
    return value


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



def macd_checker(Histogram,df,time):
    #use histogram value to determine if macd is crossed up or down
    #checking when last macd cross was

    if Histogram>0:
        print('MACD is crossed up')
        p=0.5
        rslt_df = df[df[
                         'Histogram'] < 0]  # finds positive histogram values to determine cross time (need to make it so it finds first value only and not make
        # massive df of all positive values  )

        # print(rslt_df)
        dt = (rslt_df.loc[rslt_df.index[0], 'time'])  # selects only first value
        # need to put this as outside function returns msot recent timestamp
        timed = dn - dt
        print('MACD cross occured ' + str(timed) + ' minutes ago')

        rslt_df = df[df['Histogram']<0]



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
#find max/min value bb spread to calc prob of increasing decreasing
def bb_checker(df):
    dfspread = df["Upper"]-df['Lower'] #dataframe of spread between upper lower bb
    print(dfspread)
    gradientU = (fval(df,'Upper',0) - fval(df,'Upper',20))/20
    gradientL = (fval(df, 'Lower', 0) - fval(df, 'Lower', 20))/20
    spread = gradientU-gradientL #calcs current greadient of bands to determine if bands aer stretching or decreasing
    print('The spread is decreading at a rate of ' + str(spread))
    print('med' +str(dfspread.median()))
    print(dfspread.mean())
    print((fval(df,'Upper',0) - fval(df,'Lower',0))) # tells if spread is stretching/squeezing
    if spread < 0:
        print('Bollinger Band is Squeezing')
    else:
        print('Bollinger Band is Stretching')

    p=0
    return p

for x in listdf:
    df=dffix(listdf,x)
    dn = fval(df,'time',0)
    print('Current price is ' + str(fval(df,'close',0)))
    # takes most recent data point
    currentrsi = fval(df,'RSI',0)
    cMA25 = fval(df,'25MA',0)
    cMA50 = fval(df,'50MA',0)
    cMA100 =fval(df,'100MA',0)
    cMA200 =fval(df,'200MA',0)
    chistogram = fval(df,'Histogram',0)
    p=rsi_checker(currentrsi)+trend_strength(cMA25, cMA50, cMA100, cMA200)+macd_checker(chistogram, df, dn)+bb_checker(df)
    print('Trend probability is ' + str(p))
    print(''
          )

#calculation of  probabilities
#print('The date and time is ' + str(dn))
#p=(trend_strength(cMA25, cMA50, cMA100, cMA200)+rsi_checker(currentrsi)+macd_checker(currenthistogram,df1,dn))
#('Trend probability is ' + str(p))

print ("time elapsed: {:.2f}s".format(time.time() - start_time))
