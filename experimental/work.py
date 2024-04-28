import random
import trobot2 as tr

# read config.ini
def init_config(filename):
    config = {}
    current_section = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            elif ':' in line and current_section and not line.startswith('#'):
                key, value = line.split(':')
                config[current_section][key.strip()] = value.strip()
    file.close()
    return config

# read rules from config.ini
def init_rules(config_rules):
    allrules = []
    for item in config_rules:
        items = []
        allrules.append(items)
        items.append(item)
        items.append(config_rules[f'{item}'])
    return allrules

filename = "config.ini"
config = init_config(filename)
allrules = init_rules(config['rules'])
#print(allrules)


alpha = 1
beta = 1.5
wbvnum = random.weibullvariate(alpha, beta)
#print(round(wbvnum,4))

datasend = []
for d in range(0,30):
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

cd = 0
for d in datasend:
    print(d)
    cd += 1 

cols = [0,1,2,3,4,5]

analysisrule = allrules[0][1]







res = tr.receptionP(datasend,cols[3],analysisrule)
print(res)
'''
for r in res:
    print("tr0:",round(r,4))
'''
