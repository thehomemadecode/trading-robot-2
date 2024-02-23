from binance.spot import Spot
import time
import trobot

# date conversion: human readable to machine
def dateconvert(date):
    try:
        date = time.strptime(date, "%d/%m/%y-%H:%M")
        date = time.mktime(date)
        date = int(date*1000)
        return date
    except Exception as err:
        import sys
        #print('An error:')
        #print('Line number: {}'.format(sys.exc_info()[-1].tb_lineno))
        #print(type(err).__name__, err)
        exit()

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
    # settings const
    fxtypes = ["ALL", "USDT", "TUSD", "USDC", "BTC", "ETH"]
    statustypes = ["ALL", "TRADING", "BREAK"]
    # settings vars
    filename = "alldata.txt"
    putdatatofile = False
    fileuse = True
    fx = fxtypes[1]
    status = statustypes[1]
    
    # connect binance
    client = Spot()

    # get symbol information to file
    if putdatatofile:
        alldata = client.exchange_info()
        file = open(filename, "w")
        file.write(str(alldata))
        file.close()

    # show infos
    if fileuse:
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

    # get symbol OHLCV & data
    limitnumber = 100
    symbol = symbollist[0]
    per = "4h"
    hdate = "21/02/24-06:00"
    period = 9
    
    mdate = dateconvert(hdate)
    bars = client.klines(symbol, per, startTime = mdate, limit = limitnumber)
    totalbar = len(bars)
    
    OHLC = "C"
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
    print(barOHLC)

    print(trobot.ma(barOHLC,OHLCpoint-1,period))




if __name__ == '__main__':
    main()
