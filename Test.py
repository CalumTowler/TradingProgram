


import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools
path = r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data'

hey={0:[0.5,3],1:[0.6,5]}

hey[0][0] = 0.6
print(hey)
y=0

listp=[]
for x in range(len(hey)):
    listp.append(hey[x][0])
for x in range(len(hey)):
    if max(listp)==0.0:
        print(2)
        break
    elif max(listp)==hey[x][0]:
        print(x)
        y=hey[x][1]
    else:
        pass

print(y)