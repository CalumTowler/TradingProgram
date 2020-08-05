import pandas as pd
import numpy as np


path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'
listdf = {1:1,2:5,3:15,4:60,5:240,6:'1D'}
excel1 = path + "\TVC_USOIL, " + str(listdf[6]) + ".csv"
df = pd.read_csv(excel1)
df.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
                  'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
                  ,'MOMMACD','MOMSignal']
df['time'] = pd.to_datetime(df['time'])

df['time']=df['time'].shift(-1)
df['weekday']=df['time'].dt.dayofweek


value = (df.loc[df.index[-2], 'time'])

if (df.loc[df.index[-2], 'weekday']) == 4.0:
    currentday=value+pd.Timedelta(days=3)
else:
    currentday = value + pd.Timedelta(days=1)
print(currentday)

(df.loc[df.index[-1], 'time'])=currentday

df = df.drop(['weekday'], axis=1)
df.to_csv(path + "\TVC_USOIL, " + str(listdf[6]) + ".csv", index=False)
print(df)