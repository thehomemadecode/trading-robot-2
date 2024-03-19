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

analysisrules = [["close>sma(2)"],["sma(2)>ema(3)"],["sma(2)>open>ema(3)"]]



for i in range(0,len(datasend)):
    res = (datasend[i][0]+datasend[i][1])/2
    res = round(res,4)
    print("datasend2:",res)
for i in range(0,len(datasend)):
    res = (datasend[i][0]+datasend[i][1]+datasend[i][2])/3
    res = round(res,4)
    print("datasend3:",res)
#print(datasend)
#print(cols)
#print(analysisrules)
res = tr.receptionP(datasend,cols,analysisrules)
r0 = res[0]
r1 = res[1]
r0 = round(r0,4)
r1 = round(r1,4)
print("tr0:",r0)
print("tr1:",r1)

