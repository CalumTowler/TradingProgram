import math

list=[]
x=56.54
list.append(x)
t=(round(x,-1))
list.append(t)
d=math.ceil(x)
list.append(d)
g=math.floor(x)
list.append(g)
print(list)

if t>x:
    a=t-5
    print(a)
else:
    a=t+5
    print(a)