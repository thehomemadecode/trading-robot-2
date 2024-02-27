from binance.spot import Spot
import time
import sqlite3

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
    # settings const
    fxtypes = ["ALL", "USDT", "TUSD", "USDC", "BTC", "ETH"]
    statustypes = ["ALL", "TRADING", "BREAK"]
    # settings vars
    filename = "alldata.txt"
    fx = fxtypes[1]
    status = statustypes[1]
    maxklines = 200
    #graphtimeperiodlist = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
    graphtimeperiodlist = ["1m", "5m", "15m", "1h", "4h", "1d"]
    prefix = "tr2"
    dbfilename = "candlestick.db"

    # connect binance
    client = Spot()

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
                dizi = b
                # Diziyi düzeltme
                sql3 = ",".join(str(x) for x in dizi)
                #print(sql3)
                sql = sql1+sql2+f"VALUES({sql3})"
                dbcursor.execute(sql)
                dbconnection.commit()
            
            #symbolTable[1][i].append(bars)
            #i += 1
        s += 1
        print("----",s,say,"-----------------------")
        time.sleep(1)
        #if s==1:break # temporary limiter
    
    print(s)
    print(say)
    
    
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
