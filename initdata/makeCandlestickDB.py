# trobot2 makeCandlestickDB (28 Mar)
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
            elif ':' in line and current_section and not line.startswith('#'):
                key, value = line.split(':')
                config[current_section][key.strip()] = value.strip()
    file.close()
    return config

def dbconnect(dbfilename):
    dbconnection = sqlite3.connect(dbfilename)
    return dbconnection

# Be careful, all data will be ERASED if present.
def sqlite3ClearCreate(dbfilename):
    dbconnection = sqlite3.connect(dbfilename)
    dbcursor = dbconnection.cursor()
    dbcursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ;")
    dbtables = [row[0] for row in dbcursor.fetchall()]
    for dbtable in dbtables:
        print("deleting",dbtable)
        dbcursor.execute("DROP TABLE IF EXISTS " + dbtable)
    dbconnection.commit()
    dbconnection.close()

def makeTables(dbconnection,symbollist,graphtimeperiodlist,prefix,limit):
    cols1 = "(id INTEGER PRIMARY KEY AUTOINCREMENT, open_time INTEGER, open TEXT, high TEXT, low TEXT, close TEXT, volume TEXT, close_time INTEGER, "
    cols2 = "quote_asset_volume TEXT, number_of_trades INTEGER, taker_base_volume TEXT, taker_quote_volume TEXT, unused TEXT)"
    for symbol in symbollist:
        for graphtimeperiod in graphtimeperiodlist:
            print(f"creating {prefix}_{symbol}_{graphtimeperiod}")
            dbconnection.execute(f"CREATE TABLE IF NOT EXISTS {prefix}_{symbol}_{graphtimeperiod} {cols1}{cols2}")
        limit -= 1
        if (limit == 0):break
    dbconnection.commit()
    dbconnection.close()

def main():
    # read configs
    filename = "config.ini"
    config = init_config(filename)
    # settings const
    fxtypes = eval(config['trobot Inputs']['fxtypes'])
    statustypes = eval(config['trobot Inputs']['statustypes'])
    # settings vars
    exclusions = eval(config['trobot Inputs']['exclusions'])
    inclusions = eval(config['trobot Inputs']['inclusions'])
    alldatafilename = config['trobot Inputs']['alldatafilename']
    fx = fxtypes[int(config['trobot Inputs']['fx'])]
    status = statustypes[int(config['trobot Inputs']['status'])]
    isMarginTradingAllowed = config['trobot Inputs']['isMarginTradingAllowed']
    graphtimeperiodlist = eval(config['trobot Inputs']['graphtimeperiodlist'])
    prefix = config['trobot Inputs']['prefix']
    dbfilename = config['trobot Inputs']['dbfilename']
    limit = int(config['trobot Inputs']['assetlimit'])

    # get alldata content
    file = open(alldatafilename, "r")
    for content in file:
        temp = content
    file.close()
    alldata = eval(temp)
    symbollist = []
    
    # isMarginTradingAllowed & fx & status: populate symbollist
    if isMarginTradingAllowed == "BOTH":
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

    elif isMarginTradingAllowed == "TRUE":
        for i in alldata['symbols']:
            if i['isMarginTradingAllowed']:
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

    elif isMarginTradingAllowed == "FALSE":
        for i in alldata['symbols']:
            if not i['isMarginTradingAllowed']:
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

    symbollist = symbollist[:limit]
    
    '''
    print("exclusions:")
    for e in exclusions:
        print(e)
    print("-----------------------")
    print("inclusions:")
    for i in inclusions:
        print(i)
    print("-----------------------")
    print("symbollist:")
    lc = 0
    for s in symbollist:
        print(lc,s)
        lc += 1
    print("-----------------------")
    '''
    
    def eifinder(eisymbol,eisymbollist):
        c = 1
        for i in range(len(eisymbollist)):
            if eisymbol == eisymbollist[i]:
                return c
            c += 1
        return False
    
    for e in exclusions:
        c = eifinder(e,symbollist)
        if c:
            del symbollist[c-1]
    '''
    print("symbollist:")
    lc = 0
    for s in symbollist:
        print(lc,s)
        lc += 1
    print("-----------------------")
    '''
    for i in inclusions:
        c = eifinder(i,symbollist)
        if not c:
            symbollist.insert(0, i)
    '''
    print("symbollist:")
    lc = 0
    for s in symbollist:
        print(lc,s)
        lc += 1
    print("-----------------------")
    '''
    
    sqlite3ClearCreate(dbfilename)
    dbc = dbconnect(dbfilename)
    makeTables(dbc,symbollist,graphtimeperiodlist,prefix,limit)
    

# most probably main
if __name__ == '__main__':
    main()
