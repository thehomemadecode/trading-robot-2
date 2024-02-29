import sqlite3

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
    
def dbconnect(dbfilename):
    dbconnection = sqlite3.connect(dbfilename)
    return dbconnection

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
    # settings const
    fxtypes = ["ALL", "USDT", "TUSD", "USDC", "BTC", "ETH"]
    statustypes = ["ALL", "TRADING", "BREAK"]
    # settings vars
    filename = "alldata.txt"
    fx = fxtypes[1]
    status = statustypes[1]
    #graphtimeperiodlist = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
    graphtimeperiodlist = ["5m", "1h", "1d"]
    prefix = "tr2"
    dbfilename = "candlestick.db"
    limit = 3
    
    # show infos
    file = open(filename, "r")
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
    
    sqlite3ClearCreate(dbfilename)
    dbc = dbconnect(dbfilename)
    makeTables(dbc,symbollist,graphtimeperiodlist,prefix,limit)


# most probably main
if __name__ == '__main__':
    main()
    
