import trobot2 as tr

# read config.ini
def read_config(filename):
    config = {}
    current_section = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            elif '=' in line and current_section and not line.startswith('#'):
                key, value = line.split('=')
                config[current_section][key.strip()] = value.strip()
    return config

filename = 'config.ini'
config = read_config(filename)
fx = config['trobot Inputs']['fx']
status = config['trobot Inputs']['status']

allrules = []
for getrule in config['rules']:
    ruleitem = []
    allrules.append(ruleitem)
    ruleitem.append(getrule)
    ruleitem.append(config['rules'][f'{getrule}'])


# call c++ functions
def check1(data):
    data2 = tr.check(data)
    return data2

def check2(data):
    data2 = tr.check(data)
    return data2

def check3(data):
    data2 = tr.check(data)
    return data2

function_map = {
    'check1': check1,
    'check2': check2,
    'check3': check3
}

def execute_function(func_name, *args):
    if func_name in function_map:
        # Retrieve the function from the dictionary and call it with parameters
        return function_map[func_name](*args)
    else:
        return "Function not found"




for getrule in allrules:
    result = execute_function(getrule[0], int(getrule[1]))
    print(getrule,result)
    
   
