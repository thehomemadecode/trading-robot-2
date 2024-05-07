from binance.spot import Spot

rversion = "2.0.0b"

# read config.ini
def init_config(filename):
    config = {}
    current_section = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.split('#')[0].strip()
            line = line.replace(" ", "")
            #line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            elif ':' in line and current_section and not line.startswith('#'):
                key, value = line.split(':')
                config[current_section][key.strip()] = value.strip()
    file.close()
    return config

# get all symbol information to file
def preparedatafile(filename):
    client = Spot()
    alldata = client.exchange_info()
    file = open(filename, "w")
    file.write(str(alldata))
    file.close()
    return alldata

def main():
    # read configs
    filename = "config.ini"
    config = init_config(filename)

    cversion = config['config_version']['cversion']
    if cversion != rversion:
        print("Upss! version robot-config conflict.")
        exit()
    else:
        print("getallexchangeinfo.py version: ",rversion)


    # settings vars
    alldatafilename = config['trobot_Inputs']['alldatafilename']

    # get infos
    alldata = preparedatafile(alldatafilename)

if __name__ == '__main__':
    main()
