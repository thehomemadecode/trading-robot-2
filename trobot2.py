import sqlite3
import trobot2 as tr
from binance.spot import Spot
import time

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
            elif '=' in line and current_section and not line.startswith('#'):
                key, value = line.split('=')
                config[current_section][key.strip()] = value.strip()
    file.close()
    return config

def init_rules(config_rules):
    allrules = []
    for item in config_rules:
        items = []
        allrules.append(items)
        items.append(item)
        items.append(config_rules[f'{item}'])
    return allrules

# date conversion: human readable to machine
def dateconvert(date):
    date = time.strptime(date, "%d/%m/%y-%H:%M")
    date = time.mktime(date)
    date = int(date*1000)
    return date

timetable = {
    "1m" :1,
    "5m" :5,
    "15m":15,
    "1h" :60,
    "4h" :240,
    "1d" :1440
}

# convert OHLC letters to numbers, default:C
def letter_to_number(arg):
    switcher = {
        "O": 0, # open
        "H": 1, # high
        "L": 2, # low
        "C": 3, # close
        "V": 4, # volume
        "Q": 5  # quote assest volume
    }
    return switcher.get(arg, 3)

def dbconnect(dbfilename):
    dbcon = sqlite3.connect(dbfilename)
    return dbcon

def db_read(dbcon,prefix,fx,status,graphtimeperiod,alldatafilename):
    alldatafile = open(alldatafilename, "r")
    for line in alldatafile:
        content = line
    alldatafile.close()
    alldata = eval(content)
    symbollist = []
    for i in alldata['symbols']:
        if fx == "ALL" and status == "ALL":
            symbollist.append(i['symbol'])
        elif fx == "ALL" and status != "ALL":
            if status == i['status']:
                symbollist.append(i['symbol'])
        elif fx != "ALL" and status == "ALL":
            if fx == i['symbol'][-(len(fx)):]:
                symbollist.append(i['symbol'])
        elif fx == i['symbol'][-(len(fx)):] and status == i['status']:
            symbollist.append(i['symbol'])

    selecteddata = []
    for symbol in symbollist:
        try:
            dbcur = dbcon.cursor()
            dbcur.execute(f"SELECT * FROM {prefix}_{symbol}_{graphtimeperiod}")
            data = dbcur.fetchall()
            #count = 0
            timetemp = data[len(data)-1][1]
            timedata = str(timetemp)
            timedata = timedata[:-4]
            rowdata = [symbol,graphtimeperiod,timedata]
            subrow = []
            for row in reversed(data):
                subrow += [[row[2], row[3], row[4], row[5], row[6], row[8]]]
                #count += 1
                #if (count == 2):break
            rowdata.append(subrow)
            selecteddata.append(rowdata)
        except Exception as err:
            pass
            #import sys
            #print('An error has occurred. Line number: {}'.format(sys.exc_info()[-1].tb_lineno))
            #print(type(err).__name__, err)
    return selecteddata

def db_check(dbcon,client):
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ;")
    dbtables = [row[0] for row in dbcur.fetchall()]
    count = 0
    for dbtable in dbtables:
        dbcur.execute(f"SELECT open_time FROM {dbtable} ORDER BY id DESC LIMIT 1")
        timedata = dbcur.fetchone()
        time1 = int(timedata[0]/1000)
        temp = [x for x in dbtable.split("_")]
        bars = client.klines(temp[1], temp[2], limit = 1)   
        time2 = int((bars[0][0])/1000)
        fark = time2-time1
        if (fark != 0):
            outdatedbarnumber = fark / timetable[temp[2]]
            outdatedbarnumber = int(outdatedbarnumber / 60)
            if (outdatedbarnumber>200):outdatedbarnumber=200
            print(time.strftime("%Y-%m-%d %H:%M:%S"),end=": ")
            print(temp[1],temp[2],end=": ")
            print(time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(time1)),end=" ")
            print(int(time1),end=" ")
            print(int(time2),end=" ")
            print(fark,outdatedbarnumber)
            
            dbcur.execute(f"SELECT * FROM {dbtable} ORDER BY open_time DESC LIMIT 1;")
            last_records = dbcur.fetchall()
            for record in last_records:
                sql = f"DELETE FROM {dbtable} WHERE open_time={record[1]}"
                print(sql)
                dbcur.execute(sql)
            dbcon.commit()
            
            sql1 = f"INSERT INTO {dbtable} "
            sql2 = f"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_base_volume, taker_quote_volume, unused) "
            klimit = outdatedbarnumber + 1
            bars = client.klines(temp[1], temp[2], limit = klimit)
            for b in range(0,len(bars)):
                arrayb = bars[b]
                print("arrayb",arrayb)
                # reshape arrayb
                sql3 = ",".join(str(x) for x in arrayb)
                #print(sql3)
                sql = sql1+sql2+f"VALUES({sql3})"
                time3 = int(bars[b][0]/1000)
                #print(time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(time3)),end=" ")
                dbcur.execute(sql)
            dbcon.commit()
            #print("")
            
        count += 1
        #if (count == 6):break
    return 0

def consistency_db_check(dbcon):
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ;")
    dbtables = [row[0] for row in dbcur.fetchall()]
    for dbtable in dbtables:
        temp = [x for x in dbtable.split("_")]
        chkval = int(timetable[temp[2]]*60000)
        dbcur.execute(f"SELECT id, open_time FROM {dbtable} ORDER BY open_time DESC;")
        opentimes = dbcur.fetchall()
        before = int(opentimes[0][1])
        opentimes.pop(0)
        print(dbtable,"--> Check value:",chkval,"-->\t",end="")
        passcounter = len(opentimes)
        for ot in opentimes:
            after = int(ot[1])
            val = before - after
            br = False
            if (chkval != val):
                print("Consistency check: FAILED ",dbtable,"\t id@",ot[0],after,before,chkval,val)
                br = True
            else:
                passcounter -= 1
                if (passcounter == 0):print("Consistency check: PASSED")
            if (br):break
            before = after
    return 0

def main():
    # read configs
    filename = "config.ini"
    config = init_config(filename)

    fxtypes = eval(config['trobot Inputs']['fxtypes'])
    statustypes = eval(config['trobot Inputs']['statustypes'])
    graphtimeperiodlist = eval(config['trobot Inputs']['graphtimeperiodlist'])

    alldatafilename = config['trobot Inputs']['alldatafilename']
    dbfilename = config['trobot Inputs']['dbfilename']
    prefix = config['trobot Inputs']['prefix']
    ohlvcq = config['trobot Inputs']['ohlvcq']

    fx = fxtypes[1]
    status = statustypes[1]
    graphtimeperiod = graphtimeperiodlist[2]
    
    allrules = init_rules(config['rules'])

    dbcon = dbconnect(dbfilename)
    selecteddata = db_read(dbcon,prefix,fx,status,graphtimeperiod,alldatafilename)
    
    client = Spot()
    temp = db_check(dbcon,client)
    temp = consistency_db_check(dbcon)
    dbcon.close()
    
    #print(selecteddata)
    '''
    col = letter_to_number(ohlvcq)
    for rowdata in selecteddata:
        for datagroup in rowdata[3:]:
            for data in datagroup:
                print(data[col])
    #print(bar,end=" ")
    #print("")
    '''
    '''
    col = letter_to_number(ohlvcq)
    result = tr.cryptocurrencyGate(selecteddata,col,allrules)
    print(result,len(result))
    '''

# most probably main
if __name__ == '__main__':
    main()
#test2
