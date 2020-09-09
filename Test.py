


import pandas as pd
import datetime
from datetime import datetime
import numpy as np
from datetime import timedelta

import time
import math
import itertools
path = r'C:\Users\Alex\OneDrive\Oracle\Trading Program\Stock Data'

df = pd.DataFrame(np.arange(12).reshape(3, 4),
                  columns=['A', 'B', 'C', 'D'])
print(df)
listtodrop=[]
for x in range(len(df)):
    if df.loc[df.index[x],"C"]/df.loc[df.index[x],"B"]==1.2:
        listtodrop.append(x)
        print("hello")
    else:
        pass

df.drop(index=listtodrop,inplace=True)
df = df.reset_index(drop=True)

print(df)


