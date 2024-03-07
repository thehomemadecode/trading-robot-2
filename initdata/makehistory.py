from binance.spot import Spot
import time
import sqlite3

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

# date conversion: human readable to machine
def dateconvert(date):
    date = time.strptime(date, "%d/%m/%y-%H:%M")
    date = time.mktime(date)
    date = int(date*1000)
    return date

def dbconnect(dbfilename):
    dbconnection = sqlite3.connect(dbfilename)
    return dbconnection

def main():
    # read configs
    filename = "config.ini"
    config = init_config(filename)
    
    # settings const
    fxtypes = eval(config['trobot Inputs']['fxtypes'])
    statustypes = eval(config['trobot Inputs']['statustypes'])
    # settings vars
    alldatafilename = config['trobot Inputs']['alldatafilename']
    fx = fxtypes[1]
    status = statustypes[1]
    maxklines = int(config['trobot Inputs']['maxklines'])
    graphtimeperiodlist = eval(config['trobot Inputs']['graphtimeperiodlist'])
    prefix = config['trobot Inputs']['prefix']
    dbfilename = config['trobot Inputs']['dbfilename']

    # connect binance
    client = Spot()

    # show infos
    file = open(alldatafilename, "r")
    for content in file:
        temp = content
    file.close()
    alldata = eval(temp)
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

    # get selected symbol's OHLCV & data
    dbconnection = dbconnect(dbfilename)
    dbcursor = dbconnection.cursor()
    s = 0 # temporary counter for symbol limiter
    say = 0
    symbolTable = []
    for symbol in symbollist:
        #symbolTable.append(symbol)
        #symbolTable.append([])
        #i = 0
        for graphtimeperiod in graphtimeperiodlist:
            print(symbol,graphtimeperiod)
            #symbolTable[1].append([graphtimeperiod])
            bars = client.klines(symbol, graphtimeperiod, limit = maxklines)
            say += 1
            sql1 = f"INSERT INTO {prefix}_{symbol}_{graphtimeperiod} "
            sql2 = f"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_base_volume, taker_quote_volume, unused) "
            for b in bars:
                arrayb = b
                # reshape arrayb
                sql3 = ",".join(str(x) for x in arrayb)
                #print(sql3)
                sql = sql1+sql2+f"VALUES({sql3})"
                dbcursor.execute(sql)
            #symbolTable[1][i].append(bars)
            #i += 1
        s += 1
        print("----",s,say,"-----------------------")
        #time.sleep(1)
        if s==40:break # temporary limiter
    print(s)
    print(say)
    dbconnection.commit()
    dbconnection.close()
    '''
    print(symbolTable)
    print("*********************************************")
    print(symbolTable[0])
    print("---------------")
    table = symbolTable[1]
    for per in table:
        print(per[0])
        print("------------------------------")
        for data in per[1]:
            print(data)
        print("*********************************************")
    '''
# most probably main
if __name__ == '__main__':
    main()
