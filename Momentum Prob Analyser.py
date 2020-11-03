import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta
from statistics import mean

import time
import math
import itertools
# path = r'D:\OneDrive\Oracle\Trading Program\Stock Data\Probability Results'
#
#
# values=["80.4 hour", "80.4", "120.7 hour", "120.7", "161 hour", "161"]
#
# for x in values:
#
#     df = pd.read_csv(path+r"\current dayshortmomentum" + x +".csv")
#
#     df.columns=['5 Min RSI', '15 Min RSI', '15 Min MOM2LEAD', '15 Min MOM2Histogram', 'Min MOM2LEAD' , 'Min MOM2Histogram',
#             'Probability Up', 'Probability Down', "Probability Difference", 'Nvalue', 'Nvalue Up','Nvalue Down']
#
#     print(x)
#     # dfpos=df[(df["Probability Up"]>0.7) & (df["Probability Difference"]>0.4)]
#     dfpos = df[(df["Probability Up"] > 0.5)]
#     j=(dfpos["Nvalue Up"].sum())
#
#     # dfneg=df[(df["Probability Down"]>0.7) & (df["Probability Difference"]<(-0.4))]
#     dfneg = df[(df["Probability Down"] > 0.5)]
#     h=(dfneg["Nvalue Down"].sum())
#
#     print(j)
#     print(h)
#     print(j+h)
pd.set_option('display.max_rows', 700)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

variables=["MOM Lead, MOM Histogram Gradient, MOM Histogram", "MOM Lead Gradient", "RSI, RSI Gradient", "25MA Orbit", "50MA Orbit", "100MA Orbit"]
timeperiods=["15Min", "60Min", "Day" ]

tplist=[]
essentials=["5MinMOM Lead, MOM Histogram Gradient, MOM Histogram","5MinMOM Lead Gradient" "5MinRSI", "5MinRSI Gradient", "5Min50MA Orbit",  "5Min Fibonacci", "5Min50MA Orbit","60MinRSI, RSI Gradient",
            "DayRSI, RSI Gradient","Day25MA Orbit", "Day50MA Orbit", "DayMOM Lead, MOM Histogram Gradient, MOM Histogram", "Day Fibonacci"]
notneeded=[]
for x in timeperiods:
    for y in variables:
        timeadapted=(x+y)

        tplist.append(timeadapted)

tpslist = [x for x in tplist if x not in essentials]
tpsslist= [x for x in tpslist if x not in notneeded]
print(tpsslist)
master=[]
for x in range(1,14):

    master.extend((list(itertools.combinations(tpsslist, x))))
master2=[]
for x in master:
    x=list(x)
    x=[x]
    master2.extend(x)

master3=[]

for y in master2:
    d=dict()

    inlist=[x for x in tpsslist if x in y]
    outlist=[x for x in tpsslist if x not in y]

    for variables in inlist:
        d.update({variables:True})
    for variables in outlist:
        d.update({variables:False})
    master3.append(d)

df=pd.DataFrame()
for x in tpsslist:
    df[x]=[]
print(len(master3))

for z in range(len(master3)):
    df=df.append(master3[z], ignore_index=True)



print(df.iloc[1].tolist())
