name = "TruControl Custom"
version = "0.0.1"

import json
from urllib.request import urlopen

import serial
import yaml
import serial.tools.list_ports
from time import sleep


def debugprint(msg):
    global debugMode
    if debugMode:
        print(msg)

def getState(chckState):
    global data_truck
    state = data_truck.get(chckState)
    return state

def getPrevState(chckState):
    global url
    response = urlopen(url)
    data_json = json.loads(response.read())
    data_truck = data_json.get('truck')
    state = data_truck.get(chckState)
    return state

def set_port(state):
    file_name = "config.yml"
    with open(file_name) as f:
        doc = yaml.safe_load(f)

        ard = doc['ARDUINO']
        ard['port'] = state
    with open(file_name, 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)

def read_port():
    with open('config.yml', 'r') as docread:
        doc = yaml.safe_load(docread)
        ard = doc['ARDUINO']
        rport = ard['port']
        return rport

def sendArduino(msg):
    arduino.write(bytes(msg, 'utf-8'))
    arduino.write(b'\n')


# read config file:
with open('config.yml', 'r') as ymlRead:
    configFile = yaml.safe_load(ymlRead)

configSection = configFile['CONFIG']
url = configSection['url']
debugMode = configSection['debugMode']
firstRun = configSection['firstRun']

arduinoSection = configFile['ARDUINO']
port = arduinoSection['port']
baudRate = arduinoSection['baudRate']

prevGameState = 1

# end of declarations

# first run setup:

if firstRun:
    print('This is your first time running this programme, some setup settings are required.')
    print('Please make sure that your arduino board is connected and running, then press Enter')
    input()
    ports = list(serial.tools.list_ports.comports())
    num = 1
    for p in ports:
        print(str(num), p)
        num +=1
    print()
    print('Please select your arduino board!')
    print('Type the COM port of your board (e.g COM4)')
    portReadFromInput = input()
    try:
        arduino = serial.Serial(port=portReadFromInput, baudrate=baudRate, timeout=.1)
        sendArduino('hndshk')
    except:
        print('Wrong port, please restart the software!')
        exit()

    set_port(portReadFromInput)
    print('Port was set! Baudrate used is: ', str(baudRate))
    print()
    print()

# start of programme

print(name + " " + version)

debugprint('port read:')
debugprint(port)
debugprint('url read:')
debugprint(url)
print('Connecting with arduino...')
arduino = serial.Serial(port=port, baudrate=baudRate, timeout=.1)
print('Attempting connection with the telemetry server...')
response = urlopen(url)
print('Checking for game...')

while True:                                                                 # initializing
    response = urlopen(url)
    data_json = json.loads(response.read())
    data_game = data_json.get('game')
    gameState = data_game.get('connected')
    if (prevGameState == 1) and (not gameState):
        print('Game is not connected (or not running).')
        prevGameState = 0
    elif gameState:
        print('Game is connected and running, you are good to go!')
        prevGameState = 1
        break

blinkerPrevState = 3                                                        # initial variable settings
indLgtHghPrevState = getPrevState('lightsBeamHighOn')
indLgtPrkPrevState = getPrevState('lightsParkingOn')    #
indLgtLowPrevState = getPrevState('lightsBeamLowOn')    #
indLgtBcnPrevState = getPrevState('lightsBeaconOn')     #
# no diff lock info!
indHndBrkPrevState = getPrevState('parkBrakeOn')        #
indNoChrgPrevState = getPrevState('batteryVoltageWarningOn')    #
indNoOilpPrevState = getPrevState('oilPressureWarningOn')       #
truckElecPrevState = getPrevState('electricOn')




while True:
    while arduino.inWaiting():
        message = arduino.readline().decode('utf-8').partition('\n')[0]

    response = urlopen(url)
    data_json = json.loads(response.read())
    data_truck = data_json.get('truck')

    indBlnLft = getState('blinkerLeftOn')
    indBlnRgt = getState('blinkerRightOn')
    indLgtHgh = getState('lightsBeamHighOn')
    indLgtPrk = getState('lightsParkingOn')
    indLgtLow = getState('lightsBeamLowOn')
    indLgtBcn = getState('lightsBeaconOn')
    indHndBrk = getState('parkBrakeOn')
    indNoChrg = getState('batteryVoltageWarningOn')
    indNoOilp = getState('oilPressureWarningOn')
    truckElec = getState('electricOn')

    if (not indBlnLft) and (not indBlnRgt) and (blinkerPrevState != 0):
        sendArduino('indBlnOff')
        blinkerPrevState = 0
        debugprint('Blinkers off, code sent!')
    if indBlnLft and (not indBlnRgt) and (blinkerPrevState != 1):
        sendArduino('indBlnLftOn')
        debugprint('Left blinker on, code sent!')
        blinkerPrevState = 1
    if (not indBlnLft) and indBlnRgt and (blinkerPrevState != 2):
        sendArduino('indBlnRgtOn')
        debugprint('Right blinker on, code sent!')
        blinkerPrevState = 2
    if indBlnLft and indBlnRgt and (blinkerPrevState != 3):
        sendArduino('indHzdOn')
        debugprint('Hazards are on, code sent!')
        blinkerPrevState = 3

    if indLgtPrk != indLgtPrkPrevState:
        if indLgtPrk:
            sendArduino('indLgtPrkOn')
            debugprint('Parking lights on, code sent!')
            indLgtPrkPrevState = True
        elif not indLgtPrk:
            sendArduino('indLgtPrkOff')
            debugprint('Parking lights off, code sent!')
            indLgtPrkPrevState = False

    if truckElec:
        if indLgtLow != indLgtLowPrevState:
            if indLgtLow:
                sendArduino('indLgtLowOn')
                debugprint('Low beams on, code sent!')
                indLgtLowPrevState = True
            elif not indLgtLow:
                sendArduino('indLgtLowOff')
                debugprint('Low beams off, code sent!')
                indLgtLowPrevState = False
                if indLgtHghPrevState:
                    sendArduino('indLgtHghOff')
                    debugprint('High Beams off with low beams, code sent!')
                    indLgtHghPrevState = False

        if indLgtBcn != indLgtBcnPrevState:
            if indLgtBcn:
                sendArduino('indLgtBcnOn')
                debugprint('Beacons on, code sent!')
                indLgtBcnPrevState = True
            elif not indLgtBcn:
                sendArduino('indLgtBcnOff')
                debugprint('Beacons off, code sent!')
                indLgtBcnPrevState = False

        if indHndBrk != indHndBrkPrevState:
            if indHndBrk:
                sendArduino('indHndBrkOn')
                debugprint('Hand brake on, code sent!')
                indHndBrkPrevState = True
            elif not indHndBrk:
                sendArduino('indHndBrkOff')
                debugprint('Hand brake off, code sent!')
                indHndBrkPrevState = False

        if indNoChrg != indNoChrgPrevState:
            if indNoChrg:
                sendArduino('indNoChrgOn')
                debugprint('Battery warning on, code sent!')
                indNoChrgPrevState = True
            elif not indNoChrg:
                sendArduino('indNoChrgOff')
                debugprint('Battery warning off, code sent!')
                indNoChrgPrevState = False

        if indNoOilp != indNoOilpPrevState:
            if indNoOilp:
                sendArduino('indNoOilpOn')
                debugprint('Oil warning on, code sent!')
                indNoOilpPrevState = True
            elif not indNoOilp:
                sendArduino('indNoOilpOff')
                debugprint('Oil warning off, code sent!')
                indNoOilpPrevState = False

        if indLgtHgh != indLgtHghPrevState:
            if indLgtHgh and indLgtLow:
                sendArduino('indLgtHghOn')
                debugprint('High beams on, code sent!')
                indLgtHghPrevState = True
            elif not indLgtHgh:
                sendArduino('indLgtHghOff')
                debugprint('High beams are off, code sent!')
                indLgtHghPrevState = False

        truckElecPrevState = True

    if (not truckElec) and truckElecPrevState:
        if indLgtLowPrevState:
            sendArduino('indLgtLowOff')
            debugprint('Low beams off with electricity, code sent!')
            indLgtLowPrevState = False
        if indLgtBcnPrevState:
            sendArduino('indLgtBcnOff')
            debugprint('Beacons off with electricity, code sent!')
            indLgtBcnPrevState = False
        if indHndBrkPrevState:
            sendArduino('indHndBrkOff')
            debugprint('Hand brake light off with electricity, code sent!')
            indHndBrkPrevState = False
        if indNoChrgPrevState:
            sendArduino('indNoChrgOff')
            debugprint('Battery warning off with electricity, code sent!')
            indNoChrgPrevState = False
        if indNoOilpPrevState:
            sendArduino('indNoOilpOff')
            debugprint('Oil warning off with electricity, code sent!')
            indNoOilpPrevState = False
        if indLgtHghPrevState:
            sendArduino('indLgtHghOff')
            debugprint('High beams off with electricity, code sent!')
            indLgtHghPrevState = False
