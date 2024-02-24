from binance.spot import Spot
import time
import trobot2

# get all symbol information to file
def preparedatafile(filename):
    alldata = client.exchange_info()
    file = open(filename, "w")
    file.write(str(alldata))
    file.close()
    return alldata

# date conversion: human readable to machine
def dateconvert(date):
    date = time.strptime(date, "%d/%m/%y-%H:%M")
    date = time.mktime(date)
    date = int(date*1000)
    return date

# convert OHLC letters to numbers, default:C
def letter_to_number(arg):
    switcher = {
        "O": 1,
        "H": 2,
        "L": 3,
        "C": 4
    }
    return switcher.get(arg, 4)

def main():
    debug = False
    # settings const
    filename = "alldata.txt"
    fxtypes = ["ALL", "USDT", "TUSD", "USDC", "BTC", "ETH"]
    statustypes = ["ALL", "TRADING", "BREAK"]
    # settings vars
    fx = fxtypes[1]
    status = statustypes[1]
    maxklines = 200
    graphtimeperiod = "4h"
    hdate = "21/02/24-06:00"
    period = 9
    OHLC = "C"
        
    # connect binance
    global client
    client = Spot()

    # get infos
    try:
        if debug:print("[.] debug: get infos - try")
        file = open(filename, "r")
        for content in file:
            temp = content
        file.close()
        alldata = eval(temp)
    except Exception as err:
        if debug:print("[.] debug: get infos - except")
        alldata = preparedatafile(filename)

    # get selected assest's infos
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
    s = 0 # temporary limiter counter
    for symbol in symbollist:
        mdate = dateconvert(hdate)
        bars = client.klines(symbol, graphtimeperiod, startTime = mdate, limit = maxklines)
        totalbar = len(bars)
        OHLCpoint = letter_to_number(OHLC)
        barOHLC = []
        for b in bars:
            temp1 = float(b[1])
            temp2 = float(b[2])
            temp3 = float(b[3])
            temp4 = float(b[4])
            temp = []
            temp.append(temp1)
            temp.append(temp2)
            temp.append(temp3)
            temp.append(temp4)
            barOHLC.append(temp)
        
        # print selected symbol OHLC bars
        # too many lines!
        #print("[.]",symbol,":",barOHLC)
        
        # get and print simple moving average
        print("[*] ",symbol," SMA(",period,"): ",trobot2.sma(barOHLC,OHLCpoint-1,period),sep="")
        s += 1
        if s==3:break # temporary limiter




















# most probably main
if __name__ == '__main__':
    main()