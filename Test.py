

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


#rsi checker where p = probability of upwards movement

def fval(df,column,val):
    value = (df.loc[df.index[val], column])
    return value

def bb_checker(df,tp):
    df['Spread'] = df["Upper"]-df['Lower'] #column of spread between upper lower bb
    gradientU = (fval(df,'Upper',tp) - fval(df,'Upper',(tp+20)))/20
    gradientL = (fval(df, 'Lower', tp) - fval(df, 'Lower', (tp+20)))/20
    spreadgrad = gradientU-gradientL #calcs current greadient of up/low bands to determine if bands aer stretching or squeezing
    #print('The spread is decreading at a rate of ' + str(spreadgrad))
    cspread=fval(df,'Spread',tp)
    print('Median')
    print((cspread)/(df['Spread']).median())
    print('Average')
    print((cspread)/(df['Spread']).mean())
    print('Current Spread')
    print("")
    # if spreadgrad < 0:
    #     print('Bollinger Band is Squeezing')
    # else:
    #     print('Bollinger Band is Stretching')
df = dffix(listdf, 3, 0)


for x in range(0,100):
    print(fval(df,'time',x))
    bb_checker(df,x)


print('Done')
