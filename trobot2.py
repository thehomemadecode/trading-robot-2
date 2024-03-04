import sqlite3
import trobot2 as tr
from binance.spot import Spot
import time
import asyncio
import websockets
import json
from datetime import datetime
import multiprocessing
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
import random

FORES = [ Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

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
            timedata = timedata[:-3]
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
    dbcur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name ASC;")
    dbtables = [row[0] for row in dbcur.fetchall()]
    count = 0
    progress = (len(dbtables))
    progressc = 0
    for dbtable in dbtables:
        dbcur.execute(f"SELECT open_time FROM {dbtable} ORDER BY id DESC LIMIT 1")
        timedata = dbcur.fetchone()
        time1 = int(timedata[0]/1000)
        temp = [x for x in dbtable.split("_")]
        bars = client.klines(temp[1], temp[2], limit = 1)   
        time2 = int((bars[0][0])/1000)
        fark = time2-time1
        progressc += 1
        if (fark != 0):
            outdatedbarnumber = fark / timetable[temp[2]]
            outdatedbarnumber = int(outdatedbarnumber / 60)
            if (outdatedbarnumber>500):outdatedbarnumber=500 # write a function delete older than kline500.
            '''
            print(time.strftime("%Y-%m-%d %H:%M:%S"),end=": ")
            print(temp[1],temp[2],end=": ")
            print(time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(time1)),end=" ")
            print(int(time1),end=" ")
            print(int(time2),end=" ")
            print(fark,outdatedbarnumber)
            '''
            dbcur.execute(f"SELECT * FROM {dbtable} ORDER BY open_time DESC LIMIT 1;")
            last_records = dbcur.fetchall()
            for record in last_records:
                sql = f"DELETE FROM {dbtable} WHERE open_time={record[1]}"
                #print(sql)
                dbcur.execute(sql)
            #dbcon.commit()

            sql1 = f"INSERT INTO {dbtable} "
            sql2 = f"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_base_volume, taker_quote_volume, unused) "
            klimit = outdatedbarnumber + 1
            bars = client.klines(temp[1], temp[2], limit = klimit)
            for b in range(0,len(bars)):
                arrayb = bars[b]
                #print("arrayb",arrayb)
                # reshape arrayb
                sql3 = ",".join(str(x) for x in arrayb)
                #print(sql3)
                sql = sql1+sql2+f"VALUES({sql3})"
                time3 = int(bars[b][0]/1000)
                #print(time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(time3)),end=" ")
                dbcur.execute(sql)
            dbcon.commit()
            #print("")
        comp = round((100 * (progressc/progress)),1)
        print(f"db_check: {comp}%\r",end="")
        count += 1
        #if (count == 6):break
    print("")
    return 0

def consistency_db_check(dbcon):
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ;")
    dbtables = [row[0] for row in dbcur.fetchall()]
    failedtables = []
    for dbtable in dbtables:
        temp = [x for x in dbtable.split("_")]
        chkval = int(timetable[temp[2]]*60000)
        dbcur.execute(f"SELECT id, open_time FROM {dbtable} ORDER BY open_time DESC;")
        opentimes = dbcur.fetchall()
        before = int(opentimes[0][1])
        opentimes.pop(0)
        #print(dbtable,"--> Check value:",chkval,"-->\t",end="\n")
        passcounter = len(opentimes)
        for ot in opentimes:
            after = int(ot[1])
            val = before - after
            br = False
            if (chkval != val):
                print("Consistency check: FAILED ",dbtable,"\t id@",ot[0],after,before,chkval,val)
                failedtables.append(dbtable)
                br = True
            else:
                passcounter -= 1
                #if (passcounter == 0):print("Consistency check: PASSED")
            if (br):break
            before = after
    return failedtables

def refresh_failedtables(dbcon,failedtables,client):
    dbcur = dbcon.cursor()
    cols1 = "(id INTEGER PRIMARY KEY AUTOINCREMENT, open_time INTEGER, open TEXT, high TEXT, low TEXT, close TEXT, volume TEXT, close_time INTEGER, "    
    cols2 = "quote_asset_volume TEXT, number_of_trades INTEGER, taker_base_volume TEXT, taker_quote_volume TEXT, unused TEXT)"    
    sql2 = f"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_base_volume, taker_quote_volume, unused) "
    for dbtable in failedtables:
        dbcur.execute("DROP TABLE IF EXISTS " + dbtable)
        dbcon.commit()
        dbcur.execute(f"CREATE TABLE IF NOT EXISTS {dbtable} {cols1}{cols2}")
        temp = [x for x in dbtable.split("_")]
        bars = client.klines(temp[1], temp[2], limit = 200)
        sql1 = f"INSERT INTO {dbtable} "
        for b in bars:
            arrayb = b
            # reshape arrayb
            sql3 = ",".join(str(x) for x in arrayb)
            sql = sql1+sql2+f"VALUES({sql3})"
            dbcur.execute(sql)
        dbcon.commit()
        print(dbtable,"refreshed.")
    return 0

# ----------------------------------------------------------------------------------------------
async def get_data(data):
    symbol = data[0].lower()
    klinestarttimedata = int(data[2])
    graphtimeperiod = data[1]
    url = f"wss://data-stream.binance.vision:443/ws/{symbol}@kline_{graphtimeperiod}"
    async with websockets.connect(url) as websocket:
        renk = random.sample(FORES,k=1)
        stil = random.sample(STYLES,k=1)
        renk = renk[0]
        stil = stil[0]
        data2 = ""
        sayac = 0
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            closeprice = data['k']['c']
            klinestarttime = data['k']['t']
            klinestarttime = int(klinestarttime/1000)
            if (data2 != closeprice):
                data2 = closeprice
                timediff = klinestarttime-klinestarttimedata
                print(renk+stil+f"{sayac}: [{datetime.now().isoformat()}] {symbol}: {closeprice} {klinestarttimedata} {klinestarttime} {timediff}")
                sayac += 1
                if (timediff != 0):
                    print(f"{symbol} <-----------------------------------> break")
                    break

async def worker(selecteddata,s,f):
    partedselecteddata = []
    for i in range(s,f):
        partedselecteddata.append(selecteddata[i])
    tasks = [get_data(data) for data in partedselecteddata]
    await asyncio.gather(*tasks)

def dowork(selecteddata,s,f):
    asyncio.run(worker(selecteddata,s,f))
# ----------------------------------------------------------------------------------------------

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
    graphtimeperiod = graphtimeperiodlist[0]
    
    allrules = init_rules(config['rules'])

    dbcon = dbconnect(dbfilename)
    client = Spot()
    temp = db_check(dbcon,client)
    failedtables = consistency_db_check(dbcon)
    temp = refresh_failedtables(dbcon,failedtables,client)
    selecteddata = db_read(dbcon,prefix,fx,status,graphtimeperiod,alldatafilename)
    dbcon.close()

    '''
    for rowdata in selecteddata:
        print(rowdata[0],rowdata[1],rowdata[2],rowdata[3][0])
    exit()
    '''
    just_fix_windows_console()
    p1 = multiprocessing.Process(target=dowork, args=(selecteddata,0,10))
    p2 = multiprocessing.Process(target=dowork, args=(selecteddata,10,20))
    p3 = multiprocessing.Process(target=dowork, args=(selecteddata,20,30))
    p4 = multiprocessing.Process(target=dowork, args=(selecteddata,30,40))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p1.terminate()
    p2.terminate()
    p3.terminate()
    p4.terminate()
    
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
