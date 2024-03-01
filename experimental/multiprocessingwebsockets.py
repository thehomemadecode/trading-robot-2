import asyncio
import websockets
import json
from datetime import datetime
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
import random
import time
import multiprocessing

FORES = [ Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

async def get_data(symbol):
    #url = f"wss://data-stream.binance.vision:443/ws/{symbol}@miniTicker"
    url = f"wss://data-stream.binance.vision:443/ws/{symbol}@kline_1d"
    async with websockets.connect(url) as websocket:
        renk = random.sample(FORES,k=1)
        stil = random.sample(STYLES,k=1)
        file = open(symbol+".txt", "w")
        data2 = ""
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            print(data)
            data = data['c']
            # Verileri ekrana yazdırma
            if (data2 != data):
                data2 = data
                # Verileri ekrana yazdırma
                print(renk[0]+stil[0]+f"[{datetime.now().isoformat()}] {symbol}: {data}")
                file.write(str(data+'\n'))
                file.flush()
                break

async def worker(symbollist,s,f):
    symbollist2 = []
    for i in range(s,f):
       symbollist2.append(symbollist[i].lower())
    tasks = [get_data(symbol) for symbol in symbollist2]
    await asyncio.gather(*tasks)

def dowork(symbollist,s,f):
    asyncio.run(worker(symbollist,s,f))
    
def main():
    fxtypes = ["ALL", "USDT", "TUSD", "USDC", "BTC", "ETH"]
    statustypes = ["ALL", "TRADING", "BREAK"]
    filename = "alldata.txt"
    fx = fxtypes[1]
    status = statustypes[1]

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
    
    #just_fix_windows_console()

    p1 = multiprocessing.Process(target=dowork, args=(symbollist,0,1))
    p2 = multiprocessing.Process(target=dowork, args=(symbollist,1,2))
    p3 = multiprocessing.Process(target=dowork, args=(symbollist,2,3))
    p4 = multiprocessing.Process(target=dowork, args=(symbollist,3,4))
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

if __name__ == '__main__':
    main()