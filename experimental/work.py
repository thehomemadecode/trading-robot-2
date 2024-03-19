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
print(datasend)

cols = [0,1,2,3,4,5]

analysisrule = "sma(2)>open>ema(3)"



#print(datasend)
#print(cols)
#print(analysisrules)

res = tr.receptionP(datasend,cols,analysisrule)
r0 = res[0]
r1 = res[1]
r0 = round(r0,4)
r1 = round(r1,4)
print("tr0:",r0)
print("tr1:",r1)
