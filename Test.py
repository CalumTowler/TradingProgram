


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


for x in reversed(range(1,3)):

    for x in range(6):
        listtodrop.append(x)


print(listtodrop)


