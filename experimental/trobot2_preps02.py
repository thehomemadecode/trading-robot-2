import trobot2 as tr
import sqlite3

# read config.ini
def read_config(filename):
    config = {}
    current_section = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.split('#')[0].strip()
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            elif '=' in line and current_section and not line.startswith('#'):
                key, value = line.split('=')
                config[current_section][key.strip()] = value.strip()
    return config

filename = 'config.ini'
config = read_config(filename)

fx = config['trobot Inputs']['fx']
graphtimeperiod = config['trobot Inputs']['graphtimeperiod']

dbfilename = config['database settings']['dbfilename']
prefix = config['database settings']['prefix']

allrules = []
for getrule in config['rules']:
    ruleitem = []
    allrules.append(ruleitem)
    ruleitem.append(getrule)
    ruleitem.append(config['rules'][f'{getrule}'])

# convert OHLC letters to numbers, default:C
def letter_to_number(arg):
    switcher = {
        "O": 1,
        "H": 2,
        "L": 3,
        "C": 4,
        "V": 5
    }
    return switcher.get(arg, 4)

def dbconnect(dbfilename):
    dbconnection = sqlite3.connect(dbfilename)
    return dbconnection

dbconnection = dbconnect(dbfilename)
dbcursor = dbconnection.cursor()
dbcursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ;")
dbtables = [row[0] for row in dbcursor.fetchall()]
for dbtable in dbtables:
    temp = [x for x in dbtable.split("_")]
    if (graphtimeperiod==temp[2]):
        dbcursor.execute(f"SELECT * FROM {dbtable}")
        data = dbcursor.fetchall()
        print(f"[{dbtable}]:")
        count = 0
        for row in reversed(data):
            print(row[2], row[3], row[4], row[5], row[6])
            count += 1
            if (count == 5):break

dbconnection.close()

# call c++ functions
def check1(data):
    data2 = tr.check(data)
    return data2

def check2(data):
    data2 = tr.check(data)
    return data2

def check3(data):
    data2 = tr.check(data)
    return data2

function_map = {
    'check1': check1,
    'check2': check2,
    'check3': check3
}

def execute_function(func_name, *args):
    if func_name in function_map:
        # Retrieve the function from the dictionary and call it with parameters
        return function_map[func_name](*args)
    else:
        return "Function not found"

for getrule in allrules:
    result = execute_function(getrule[0], int(getrule[1]))
    print(getrule,result)
