from binance.spot import Spot

# get all symbol information to file
def preparedatafile(filename):
    # connect binance
    client = Spot()
    
    alldata = client.exchange_info()
    file = open(filename, "w")
    file.write(str(alldata))
    file.close()
    return alldata

def main():
    # settings vars
    filename = "alldata.txt"

    # get infos
    alldata = preparedatafile(filename)

if __name__ == '__main__':
    main()
  
