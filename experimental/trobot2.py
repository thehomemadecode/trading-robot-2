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
        "C": 4,
        "V": 5
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
    graphtimeperiod = "1d"
    hdate = "17/02/24-03:00"
    period = 9
    OHLC = "V"
        
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
        barOHLC = []
        for b in bars:
            barOHLCrow = []
            for col in range(1,6):
                barOHLCrow.append(float(b[col]))
            barOHLCrow.append(float(((barOHLCrow[0]+barOHLCrow[3])/2)*barOHLCrow[4]))
            barOHLC.append(barOHLCrow)
        # print selected symbol OHLC bars
        # too many lines!
        #print("[.]",totalbar,symbol,":",barOHLC)
        
        # get and print simple moving average
        OHLCpoint = letter_to_number(OHLC)
        smaresult = round(trobot2.sma(barOHLC,OHLCpoint-1,period),4)
        volKlot = round((barOHLC[totalbar-1][4]/1000),2)
        volKusd = round((barOHLC[totalbar-1][5]/1000),2)
        print("[*] ",symbol," SMA(",period,")",OHLC,": ",round((smaresult/1000),2)," Volume(K):",volKlot," Volume($K):",volKusd,sep="")
        s += 1
        time.sleep(3)
        if s==1:break # temporary limiter




















# most probably main
if __name__ == '__main__':
    main()
