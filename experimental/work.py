import random
import trobot2 as tr

alpha = 1
beta = 1.5
wbvnum = random.weibullvariate(alpha, beta)
#print(round(wbvnum,4))

datasend = []
for d in range(0,3):
    row = []
    for i in range(0,6):
        wbvnum = random.weibullvariate(alpha, beta)
        row.append(round(wbvnum,4))
    datasend.append(row)
#print(datasend)

row = []
for i in range(0,6):
    wbvnum = random.weibullvariate(alpha, beta)
    row.append(round(wbvnum,4))
datasend[0] = row
#print(datasend)

row = []
for i in range(0,6):
    wbvnum = random.weibullvariate(alpha, beta)
    row.append(round(wbvnum,4))
datasend = [row] + datasend
#print(datasend)

cols = [0,1,2,3,4,5]
analysisrules = [["sma",2],["ema",3]]



for i in range(0,len(datasend)):
    res = (datasend[i][0]+datasend[i][1])/2
    res = round(res,4)
    print(res)
for i in range(0,len(datasend)):
    res = (datasend[i][0]+datasend[i][1]+datasend[i][2])/3
    res = round(res,4)
    print(res)
#print(datasend)
#print(cols)
#print(analysisrules)
res = tr.receptionP(datasend,cols,analysisrules)
#print(res[0])
#print(res[1])

