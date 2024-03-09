import os

def main():
    cmd1 = 'python3 getallexchangeinfo.py'
    cmd2 = 'python3 makeCandlestickDB.py'
    cmd3 = 'python3 makehistory.py'

    cmd4 = 'cp alldata.txt ../.'
    cmd5 = 'cp candlestick.db ../.'
    cmd6 = 'cp config.ini ../.'

    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)

    #os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)

# most probably main
if __name__ == '__main__':
    main()
