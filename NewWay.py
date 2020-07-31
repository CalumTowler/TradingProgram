import pandas as pd

path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'

x='1'
excel1 = path + "\TVC_USOIL, "+x +".csv"

df1 = pd.read_csv(excel1)
print(df1)

df1.columns = ['time','open','high','low','close','15VMA','VWMA','25MA','50MA','100MA','200MA','Basis','Upper','Lower',
               'Volume','VMA','RSI','Histogram','MACD','Signal','%K','%D','Aroon Up','Aroon Down','MOM','MOMHistogram'
               ,'MOMMACD','MOMSignal']

print(df1)