    # get quoteAsset
    if fileuse:
        file = open(filename, "r")
        for i in file:
            temp = i
        file.close()
        alldata = eval(temp)
        list1 = []
        for i in alldata['symbols']:
            list1.append(i['quoteAsset'])
        unique_list = []
        for x in list1:
            if x not in unique_list:
                unique_list.append(x)
        print(unique_list)
# -----------------------------------------------------------------------------------------------
alldataindex = ['timezone', 'serverTime', 'rateLimits', 'exchangeFilters', 'symbols']
# -----------------------------------------------------------------------------------------------
https://github.com/binance/binance-connector-python/blob/master/binance/spot/_market.py
# -----------------------------------------------------------------------------------------------
import multiprocessing
import asyncio
import websockets
import json

async def connectsocket(queue):
    #async with websockets.connect("wss://data-stream.binance.vision:443/ws/btcusdt@kline_1m") as ws:
    async with websockets.connect("wss://data-stream.binance.vision:443/ws/btcusdt@miniTicker") as ws:
        fiyat2 = 0
        while True:
            mesaj = await ws.recv()
            temp = json.loads(mesaj)
            #fiyat = temp['k']['c']
            fiyat = temp['c']
            if (fiyat != fiyat2):
                queue.put(fiyat)
                fiyat2 = fiyat

def getprice(queue):
    asyncio.run(connectsocket(queue))

def worker(queue):
    counter = 1
    price2 = 0
    while counter:
        price = queue.get()
        queue.empty()
        time.sleep(1)
        if (price != price2):
            print("Fiyat:", price)
            counter -= 1
            price2 = price

def main():
    q = multiprocessing.Queue()
    p3 = multiprocessing.Process(target=getprice, args=(q,))
    p2 = multiprocessing.Process(target=worker, args=(q,))
    p3.start()
    p2.start()
    p2.join()
    p3.terminate()
# -----------------------------------------------------------------------------------------------
    seritoplam = 0
    for s in range(totalbar-1,totalbar-period-1,-1):
        seri[totalbar-s-1] = float(bar[s][4])
        seritoplam += seri[totalbar-s-1]
    print(seritoplam/9)
# -----------------------------------------------------------------------------------------------
def func():
    try:
        pass
    except Exception as err:
        import sys
        #print('Bir hata oluştu:')
        #print('Satır numarası: {}'.format(sys.exc_info()[-1].tb_lineno))
        #print(type(err).__name__, err)
        exit()
# -----------------------------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
