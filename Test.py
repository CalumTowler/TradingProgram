


import pandas as pd
import datetime
import time
import math
import itertools
path = r'C:\Users\Admin\OneDrive\Oracle\Trading Program\Stock Data'

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def topp(ticker, valuechange, indicator, direction,tp,length,type):

    excel1 = path + ticker + length + type + indicator + tp + ".csv"
    df = pd.read_csv(excel1)
    df=df[df["Value Change"]==valuechange]
    if direction=="Up":
        print(df.nlargest(4, "Probability Up"))
    elif direction=="Down":
        print(df.nlargest(4, "Probability Down"))

    return

tickerlist=["\TVC_USOIL, ","\SPCFD_S5INFT, "]
listindicator=["rsiprob","macdprob","maprob","bbprob"]
tplist=["60"]
for x in tickerlist:
    print(x)
    for y in tplist:
        print(y)
        for z in listindicator:
            topp(x,2,z,"Up",y,"short","Sep")
            topp(x,2,z,"Down",y,"short","Sep")