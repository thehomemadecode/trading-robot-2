import time
# read config.ini
def init_config(filename):
    config = {}
    current_section = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            elif ':' in line and current_section and not line.startswith('#'):
                key, value = line.split(':')
                config[current_section][key.strip()] = value.strip()
    file.close()
    return config

def main():
    # read configs
    filename = "config.ini"
    config = init_config(filename)

    # settings const
    fxtypes = eval(config['trobot Inputs']['fxtypes'])
    statustypes = eval(config['trobot Inputs']['statustypes'])
    # settings vars
    alldatafilename = config['trobot Inputs']['alldatafilename']
    fx = fxtypes[1]
    status = statustypes[1]
    graphtimeperiodlist = eval(config['trobot Inputs']['graphtimeperiodlist'])
    prefix = config['trobot Inputs']['prefix']
    dbfilename = config['trobot Inputs']['dbfilename']
    limit = int(config['trobot Inputs']['assetlimit'])
    
    # show infos
    file = open(alldatafilename, "r")
    for content in file:
        temp = content
    file.close()
    alldata = eval(temp)
    
    '''
    e = 1
    a = 1
    for element in alldata['symbols']:
        if (element['isMarginTradingAllowed']):
            print(e,element['symbol'],element['status'],element['quoteAsset'])
            print("isSpotTradingAllowed:",element['isSpotTradingAllowed'])
            print("isMarginTradingAllowed:",element['isMarginTradingAllowed'])
            e += 1
            for atom in element:
                print(atom)
            print("--------- element end -------------------------------------------------------------")
            break
    '''
    
    for element in alldata['symbols']:
        print(element['isMarginTradingAllowed'])


# most probably main
if __name__ == '__main__':
    main()
