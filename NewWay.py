import pandas as pd

path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'

#brings excel file from documents
interval='1'
excel1 = path + "\TVC_USOIL, "+interval +".csv"

df1 = pd.read_csv(excel1)
print(df1)
#puts column headers in

df1.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
               'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
               ,'MOMMACD','MOMSignal']


#takes most recent data point

currentrsi = float(df1.loc[df1.index[-1:],'RSI'])
print(currentrsi)
#rsi checker where p = probability of upwards movement

def rsi_checker(currentrsi):

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
    print(p)

    prsi=p
    return prsi

rsi_checker(currentrsi)

MA25 = float(df1.loc[df1.index[-1:],'25MA'])
MA50 = float(df1.loc[df1.index[-1:],'50MA'])
MA100 = float(df1.loc[df1.index[-1:],'100MA'])
MA200 = float(df1.loc[df1.index[-1:],'200MA'])

#establishes current trend by determining MA crosses

def trend_strength(MA25, MA50, MA100, MA200):

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

    print(p)
    pma=p
    return pma

trend_strength(MA25, MA50, MA100, MA200)

p=(trend_strength(MA25, MA50, MA100, MA200)*rsi_checker(currentrsi))
print(p)