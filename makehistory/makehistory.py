from binance.spot import Spot
import time

# date conversion: human readable to machine
def dateconvert(date):
    date = time.strptime(date, "%d/%m/%y-%H:%M")
    date = time.mktime(date)
    date = int(date*1000)
    return date

def main():
    # settings const
    fxtypes = ["ALL", "USDT", "TUSD", "USDC", "BTC", "ETH"]
    statustypes = ["ALL", "TRADING", "BREAK"]
    # settings vars
    filename = "alldata.txt"
    fx = fxtypes[1]
    status = statustypes[1]
    maxklines = 3
    #graphtimeperiodlist = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
    graphtimeperiodlist = ["1m", "15m", "4h", "1d"]
    
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

    # get selected symbol's OHLCV & data & calculate indicators
    s = 0 # temporary counter for symbol limiter
    symbolTable = []
    for symbol in symbollist:
        symbolTable.append(symbol)
        symbolTable.append([])
        i = 0
        for graphtimeperiod in graphtimeperiodlist:
            symbolTable[1].append([graphtimeperiod])
            time.sleep(1)
            bars = client.klines(symbol, graphtimeperiod, limit = maxklines)
            symbolTable[1][i].append(bars)
            i += 1

        s += 1
        if s==1:break # temporary limiter

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
    






# most probably main
if __name__ == '__main__':
    main()
    
