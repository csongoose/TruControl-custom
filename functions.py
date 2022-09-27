import yaml

def set_port(state):
    file_name = "config.yml"
    with open(file_name) as f:
        doc = yaml.safe_load(f)

        ard = doc['ARDUINO']
        ard['port'] = state
    with open(file_name, 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)

def set_url(state):
    file_name = "config.yml"
    with open(file_name) as f:
        doc = yaml.safe_load(f)

        cfg = doc['CONFIG']
        cfg['url'] = state
    with open(file_name, 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)

def readArduinoConfig(value):
    with open('config.yml', 'r') as ymlRead:
        configFile = yaml.safe_load(ymlRead)
    arduinoSection = configFile['ARDUINO']
    config = arduinoSection[value]
    return config

def readConfig(value):
    with open('config.yml', 'r') as ymlRead:
        configFile = yaml.safe_load(ymlRead)
    configSection = configFile['CONFIG']
    config = configSection[value]
    return config

def debugprint(msg):
    if readConfig('debugMode'):
        print(msg)