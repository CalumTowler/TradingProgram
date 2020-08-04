
import pandas as pd
import datetime
import time
import math




#function to fix and subsequently call correct df

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D'}

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
    tp = (tp-1) # tp is time period back selected -1 is used because index begins at 0
    if tp >= 0: # if 0 is selected as start then removing rows will be skipped
        df = df.drop(df.index[:tp]) #drops range of rows not wanted to make new df starting from point selected
        df = df.reset_index(drop=True) #reset index
    else:
        pass
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
    df['Spread'] = df["Upper"]-df['Lower'] #column of spread between upper lower bb
    gradientU = (fval(df,'Upper',0) - fval(df,'Upper',(20)))/20
    gradientL = (fval(df, 'Lower', 0) - fval(df, 'Lower', (20)))/20
    spreadgrad = gradientU-gradientL #calcs current greadient of up/low bands to determine if bands aer stretching or squeezing
    print('The spread is decreading at a rate of ' + str(spreadgrad))
    print('med' +str(df['Spread'].median()))
    print(df['Spread'].mean())
    print(fval(df,'Spread',0)) # current spread
    if spreadgrad < 0:
        print('Bollinger Band is Squeezing')
    else:
        print('Bollinger Band is Stretching')

    p=0
    return p

#INPUT AND ACTIONS

tp = int(input('How many periods ago would you like to start from?'))
print(tp)
print(''
      '')
df=dffix(listdf,1,tp)
cprice = (fval(df,'close',0))
print('Current price is ' + str(cprice))



#inputting resistance and support points

RS = [] #empty resistance point list
RS1 = (input('What are the Resistance and support points'))
while RS1 !="": #if no input given then question is skipped
    RS.append(RS1)
    RS1 = (input('What are the Resistance and Support points'))

print('Resistance and Support points selected are' + str([RS]))

rten = round(cprice,-1)
if rten>cprice:
    rfive = rten-5
    sten = rten-10
else:
    rfive =rten+5
    sten = rten+10


print((math.ceil(fval(df,'close',0))))
print((math.floor(fval(df,'close',0))))






t = input('Would you like to see all time periods? y/n')
print(''
      '')

start_time = time.time()

if t == 'y':

    for x in listdf:
        start_time = time.time()
        df=dffix(listdf,x,tp)
        dn = fval(df,'time',0)
        print('Chart Interval is ' + (str(listdf[x])))
        #print('Current price is ' + str(fval(df,'close',0)))
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
else:

    t = int(input('What time period would you like? 1min(1), 5min(2), 15min(3), 60min(4), 240min(5), 1Day(6)'))
    start_time = time.time()
    listdf = {1: 1, 2: 5, 3: 15, 4: 60, 5: 240, 6: '1D'}
    print(''
          )
    df = dffix(listdf, t, tp)
    dn = fval(df, 'time', 0)
    print('Chart Interval is ' + (str(listdf[t])))
    print('Current price is ' + str(fval(df, 'close', 0)))
    # takes most recent data point
    currentrsi = fval(df, 'RSI', 0)
    cMA25 = fval(df, '25MA', 0)
    cMA50 = fval(df, '50MA', 0)
    cMA100 = fval(df, '100MA', 0)
    cMA200 = fval(df, '200MA', 0)
    chistogram = fval(df, 'Histogram', 0)
    p = rsi_checker(currentrsi) + trend_strength(cMA25, cMA50, cMA100, cMA200) + macd_checker(chistogram, df,
                                                                                              dn) + bb_checker(df)
    print('Trend probability is ' + str(p))
    print(''
          )

print ("time elapsed: {:.2f}s".format(time.time() - start_time))
