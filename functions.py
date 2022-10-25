import yaml                                     # code cleared up
from time import sleep

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

def askForSetup():
    print('Do you want to run setup the next time you start the software? (y/n)')
    askForInput = True
    while askForInput:
        dInput = input()
        if dInput == 'y':
            with open("config.yml", 'r') as config:
                doc = yaml.safe_load(config)
                cfg = doc['CONFIG']
                cfg['firstRun'] = True
            with open('config.yml', 'w') as config:
                yaml.safe_dump(doc, config, default_flow_style=False)
            print('Setup will be opened the next time you start the software.')
            print('Software will shut down in 3 seconds.')
            askForInput = False
            sleep(3)
            exit()

        elif dInput == 'n':
            print('Setup will not be opened.')
            print('Software will shut down in 3 seconds.')
            askForInput = False
            sleep(3)
            exit()

        elif dInput != 'n' and dInput != 'y':
            print('Please give a valid answer! (y/n)')

def getSwitch(index, sub):
    try:
        with open('keybinding.yml') as f:
            doc = yaml.safe_load(f)
        switch = doc['Switches'][index][sub]
        return switch
    except Exception as e:
        print('An exception occured while reading a switch key from the keybinding.yml file. Error message:')
        print(e)

def getButton(index, sub):
    try:
        with open('keybinding.yml') as f:
            doc = yaml.safe_load(f)
        button = doc['Buttons'][index][sub]
        return button
    except Exception as e:
        print('An exception occured while reading a button key from the keybinding.yml file. Error message:')
        print(e)
