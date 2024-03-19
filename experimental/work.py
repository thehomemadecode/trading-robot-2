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

analysisrule = "sma(10)>ema(9)<hma(30)"
#analysisrule = "hma(20)<ema(7)"


#print(datasend)
#print(cols)
#print(analysisrules)

res = tr.receptionP(datasend,cols,analysisrule)
for r in res:
    print("tr0:",round(r,4))

