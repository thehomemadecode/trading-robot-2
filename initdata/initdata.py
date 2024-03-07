import os

def main():
    cmd1 = 'python getallexchangeinfo.py'
    cmd2 = 'python makeCandlestickDB.py'
    cmd3 = 'python makehistory.py'

    cmd4 = 'copy alldata.txt ..\.'
    cmd5 = 'copy candlestick.db ..\.'

    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)

    os.system(cmd4)
    os.system(cmd5)

# most probably main
if __name__ == '__main__':
    main()
