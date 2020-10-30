import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta
from statistics import mean

import time
import math
import itertools
path = r'D:\OneDrive\Oracle\Trading Program\Stock Data\Probability Results'


values=["80.4 hour", "80.4", "120.7 hour", "120.7", "161 hour", "161"]

for x in values:

    df = pd.read_csv(path+r"\current dayshortmomentum" + x +".csv")

    df.columns=['5 Min RSI', '15 Min RSI', '15 Min MOM2LEAD', '15 Min MOM2Histogram', 'Min MOM2LEAD' , 'Min MOM2Histogram',
            'Probability Up', 'Probability Down', "Probability Difference", 'Nvalue', 'Nvalue Up','Nvalue Down']

    print(x)
    # dfpos=df[(df["Probability Up"]>0.7) & (df["Probability Difference"]>0.4)]
    dfpos = df[(df["Probability Up"] > 0.5)]
    j=(dfpos["Nvalue Up"].sum())

    # dfneg=df[(df["Probability Down"]>0.7) & (df["Probability Difference"]<(-0.4))]
    dfneg = df[(df["Probability Down"] > 0.5)]
    h=(dfneg["Nvalue Down"].sum())

    print(j)
    print(h)
    print(j+h)
