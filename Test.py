import pandas as pd
import numpy as np
import itertools



# if ma25<ma50:
#     if ma25<ma100:
#         if ma25<ma200:
#             if ma50<ma100:
#                 if ma50<ma200:
#                     if ma100<ma200:
#                         maval=1
#                     elif ma100>ma200:
#                         maval=0.95
#                     else:
#                         pass
#                 if ma50>ma200:
#                     if ma100<ma200:
#                         maval=0.9
#                     elif ma100>ma200:
#                         maval=0.85
#                     else:
#                         pass
#             elif ma50>ma100:
#                 if ma50<ma200:
#                     if ma100<ma200:
#                         maval=0.8
#                     elif ma100>ma200:
#                         maval=0.75
#                     else:
#                         pass
#                 if ma50>ma200:
#                     if ma100<ma200:
#                         maval=0.7
#                     elif ma100>ma200:
#                         maval=0.65
#                     else:
#                         pass
#         elif ma25>ma200:
#              if ma50 < ma100:
#                  if ma50 < ma200:
#                      if ma100 < ma200:
#                          maval = 0.6
#                      elif ma100 > ma200:
#                          maval = 0.55
#                      else:
#                          pass
#                  if ma50 > ma200:
#                      if ma100 < ma200:
#                          maval = 0.5
#                      elif ma100 > ma200:
#                          maval = 0.45
#                      else:
#                          pass
#              elif ma50 > ma100:
#                  if ma50 < ma200:
#                      if ma100 < ma200:
#                          maval = 0.4
#                      elif ma100 > ma200:
#                          maval = 0.35
#                      else:
#                          pass
#                  if ma50 > ma200:
#                      if ma100 < ma200:
#                          maval = 0.3
#                      elif ma100 > ma200:
#                          maval = 0.25
#                      else:
#                          pass
#              if ma25 < ma200:
#                  if ma50 < ma100:
#                      if ma50 < ma200:
#                          if ma100 < ma200:
#                              maval = 1
#                          elif ma100 > ma200:
#                              maval = 0.95
#                          else:
#                              pass
#                      if ma50 > ma200:
#                          if ma100 < ma200:
#                              maval = 0.9
#                          elif ma100 > ma200:
#                              maval = 0.85
#                          else:
#                              pass
#                  elif ma50 > ma100:
#                      if ma50 < ma200:
#                          if ma100 < ma200:
#                              maval = 0.8
#                          elif ma100 > ma200:
#                              maval = 0.75
#                          else:
#                              pass
#                      if ma50 > ma200:
#                          if ma100 < ma200:
#                              maval = 0.7
#                          elif ma100 > ma200:
#                              maval = 0.65
#                          else:
#                              pass
#              elif ma25 > ma200:
#                  if ma50 < ma100:
#                      if ma50 < ma200:
#                          if ma100 < ma200:
#                              maval = 0.6
#                          elif ma100 > ma200:
#                              maval = 0.55
#                          else:
#                              pass
#                      if ma50 > ma200:
#                          if ma100 < ma200:
#                              maval = 0.5
#                          elif ma100 > ma200:
#                              maval = 0.45
#                          else:
#                              pass
#                  elif ma50 > ma100:
#                      if ma50 < ma200:
#                          if ma100 < ma200:
#                              maval = 0.4
#                          elif ma100 > ma200:
#                              maval = 0.35
#                          else:
#                              pass
#                      if ma50 > ma200:
#                          if ma100 < ma200:
#                              maval = 0.3
#                          elif ma100 > ma200:
#                              maval = 0.25
#                          else:
#                              pass
#
#
#
#                 if ma100<ma200
#                     maval=0.9
#                 elif ma100>ma200
#                     maval=0.85
# else: pass


ma25=1.1
ma50=1.3
ma100=0.9
ma200=1.0

x = ma25<ma50
y=ma25<ma100
q=ma25<ma200
r=ma50<ma100
s=ma50<ma200
z=ma100<ma200 #binary manipulation of true false ma cases

mas=[x,y,q,r,s,z]
print(mas)


maperms=[]
l=[False,True]
for i in itertools.product(l,repeat=6):
    maperms.append(list(i))
print(maperms)
dfmas = pd.DataFrame({'MA Profile':[],'Probability Up':[], 'Probability Down':[]})
dfmas['MA Profile']=maperms
print(dfmas)



# mapermsdict={}
# for x in range(64):
#     a={x:(x/10)}
#     mapermsdict.update(a)
# for i in maperms and mapermsdict:
#     a=maperms[i]
#     mapermsdict[i]= a
# print(mapermsdict)
#
# for i in mapermsdict:
#     if mas==mapermsdict[i]:
#         print(mapermsdict[i])
#     else:
#         pass


def priceprob(df,nb,valuechange):
    for x in range((len(df.index) - nb)):  # this itterates over every row in the dataframe except the top rows where forward data is not available
        cprice = fval(df, 'close', x + nb)  # current price
        xlst = range(nb)  # gives forward bar indexes as list
        p1list = []  # list of probabilities for range of forward bars
        p2list = []  # this list is for probabilities if the value change is both up and down by the required amount i.e. moves 1% up and down in net 3 hours
        for y in xlst:
            npriced = fval(df, 'low', x)  # low of bar
            npriceu = fval(df, 'high', x)  # high of bar
            percent = (cprice / 100) * valuechange

            d = cprice - npriced  # different between forward price and current price being exaimned
            u = npriceu - cprice
            if u > percent and d > percent:  # for conditions where both up and down value changes occur
                p1 = 1
                p2 = -1
            else:
                p2 = 0
                if d > percent:  # down by value occurs
                    p1 = -1

                elif u > percent:  # up by value occurs
                    p1 = 1

                else:
                    p1 = 0
            p1list.append(p1)  # list of values
            p2list.append(p2)
        pu1 = [x for x in p1list if x > 0]  # list of positive value moves
        pd1 = [x for x in p1list if x < 0]  # lsit of neg value moves
        pd2 = [x for x in p2list if x < 0]  # list of neg value moves if both neg and pos occur
        if len(pd2) > 0:  # if both occur then 2 probabilities are entered
            p11 = -1
            p22 = 1
        else:
            p22 = 0  # if only one value change occurs
            if len(
                    pu1) > 0:  # if list has any values in it then a value chnage up occured thus rsi has preceded an upwards movement
                p11 = 1

            elif len(pd1) > 0:
                p11 = -1

            else:
                p11 = 0
        df.loc[df.index[x + nb], 'p1'] = p11  # assign these values to df column
        df.loc[df.index[x + nb], 'p2'] = p22
    return(df)

priceprob(df,nb,valuechange)

