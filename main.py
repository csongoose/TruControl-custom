import json
from urllib.request import urlopen
import yaml
import serial.tools.list_ports
import firstrun
import keyboard
import inputhandling
from functions import (readConfig, readArduinoConfig, debugprint, askForSetup)

name = "TruControl Custom"  # code cleaned up
version = "0.1.4c"

print(readConfig('inputsEnabled'))

def getState(chckState):  # only checks in preloaded list
    global data_truck
    state = data_truck.get(chckState)
    return state


def getPrevState(chckState):  # loads url every instance to avoid desync
    global url
    response = urlopen(url)
    data_json = json.loads(response.read())
    data_truck = data_json.get('truck')
    state = data_truck.get(chckState)
    return state


def sendArduino(msg):
    arduino.write(bytes(msg, 'utf-8'))
    arduino.write(b'\n')


# read config file:
with open('config.yml', 'r') as ymlRead:
    configFile = yaml.safe_load(ymlRead)

url = readConfig('url')
debugMode = readConfig('debugMode')
firstRun = readConfig('firstRun')

port = readArduinoConfig('port')
baudRate = readArduinoConfig('baudRate')

prevGameState = 1

# end of declarations

# first run setup:

if firstRun:
    firstrun.firstRun()

# start of programme

print(name + " " + version)

debugprint('port read:')
debugprint(port)
debugprint('url read:')
debugprint(url)
print('Attempting connection with the arduino...')
try:
    arduino = serial.Serial(port=port, baudrate=baudRate, timeout=.1)
except Exception as e2:
    print('Connection failed!')
    debugprint(e2)
    askForSetup()

print('Attempting connection with the telemetry server...')
try:
    response = urlopen(url)
except Exception as e1:
    print('Failed to open telemetry data')
    debugprint(e1)
    askForSetup()
print('Checking for game...')

while True:  # initializing
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

blinkerPrevState = 3  # initial variable settings
indLgtHghPrevState = getPrevState('lightsBeamHighOn')
indLgtPrkPrevState = getPrevState('lightsParkingOn')
indLgtLowPrevState = getPrevState('lightsBeamLowOn')
indLgtBcnPrevState = getPrevState('lightsBeaconOn')
# no diff lock info!
indHndBrkPrevState = getPrevState('parkBrakeOn')
indNoChrgPrevState = getPrevState('batteryVoltageWarningOn')
indNoOilpPrevState = getPrevState('oilPressureWarningOn')
truckElecPrevState = getPrevState('electricOn')
indAirLowPrevState = getPrevState('airPressureWarningOn')
indFueLowPrevState = getPrevState('fuelWarningOn')
indChcEngValPrevState = getPrevState('wearEngine')
indRetardValPrevState = getPrevState('retarderBrake')
indCruisePrevState = getPrevState('cruiseControlOn')
indWaterTempPrevState = getPrevState('waterTemperatureWarningOn')

if indChcEngValPrevState < 0.1:
    indChcEngPrevState = False
elif indChcEngValPrevState >=0.1:
    indChcEngPrevState = True
if indRetardValPrevState == 0:
    indRetardPrevState = False
if indRetardValPrevState > 0:
    indRetardPrevState = True

retarderKeys = inputhandling.keys.Switches.Retarder()
lightKeys = inputhandling.keys.Switches.Lights()
blinkerKeys = inputhandling.keys.Switches.Blinkers()
wiperKeys = inputhandling.keys.Switches.Wipers()
ignitionKeys = inputhandling.keys.Switches.Ignition()
switchboardKeys = inputhandling.keys.Switches.Switchboard()

switchboardButtons = inputhandling.keys.Buttons.Switchboard()
windowButtons = inputhandling.keys.Buttons.Windows()
suspensionButtons = inputhandling.keys.Buttons.Suspension()

while True:
    if readConfig('inputsEnabled'):
        while arduino.inWaiting():  # input handling
            message = arduino.readline().decode('utf-8').partition('\r')[0]

            # retarder
            if message == 'retOff':
                keyboard.press_and_release(retarderKeys.retOffKey)
            elif message == 'retPos1':
                keyboard.press_and_release(retarderKeys.retPos1Key)
            elif message == 'retPos2':
                keyboard.press_and_release(retarderKeys.retPos2Key)
            elif message == 'retPos3':
                keyboard.press_and_release(retarderKeys.retPos3Key)
            elif message == 'retPos4':
                keyboard.press_and_release(retarderKeys.retPos4Key)

            # lights
            elif message == 'lgtOff':
                keyboard.press_and_release(lightKeys.lgtOffKey)
            elif message == 'lgtPrk':
                keyboard.press_and_release(lightKeys.lgtPrkKey)
            elif message == 'lgtLow':
                keyboard.press_and_release(lightKeys.lgtLowKey)
            elif message == 'lgtHgh':
                keyboard.press_and_release(lightKeys.lgtHghKey)

            # blinkers
            elif message == 'blnLftOn' or message == 'blnLftOff':
                keyboard.press_and_release(blinkerKeys.blnLftKey)
            elif message == 'blnRgtOn' or message == 'blnRgtOff':
                keyboard.press_and_release(blinkerKeys.blnRgtKey)

            # wipers
            elif message == 'wipOff':
                keyboard.press_and_release(wiperKeys.wipOffKey)
            elif message == 'wipSpd1':
                keyboard.press_and_release(wiperKeys.wipSpd1Key)
            elif message == 'wipSpd2':
                keyboard.press_and_release(wiperKeys.wipSpd2Key)
            elif message == 'wipSpd3':
                keyboard.press_and_release(wiperKeys.wipSpd3Key)

            # ignition and electrics
            elif message == 'elcOff':
                keyboard.press(ignitionKeys.elcOffKey)
                keyboard.release(ignitionKeys.elcIgnKey)
                keyboard.release(ignitionKeys.engSrtKey)
            elif message == 'elcIgn':
                keyboard.press(ignitionKeys.elcIgnKey)
                keyboard.release(ignitionKeys.elcOffKey)
                keyboard.release(ignitionKeys.engSrtKey)
            elif message == 'engSrt':
                keyboard.press(ignitionKeys.engSrtKey)
                keyboard.release(ignitionKeys.elcOffKey)

            # switches on the switchboard:
            elif message == 'trdWhl':
                keyboard.press_and_release(switchboardKeys.trdWhlKey)
            elif message == 'lgtBcn':
                keyboard.press_and_release(switchboardKeys.lgtBcnKey)
            elif message == 'lgtHzd':
                keyboard.press_and_release(switchboardKeys.lgtHzdKey)
            elif message == 'difLoc':
                keyboard.press_and_release(switchboardKeys.difLocKey)
            elif message == 'hndBrk':
                keyboard.press_and_release(switchboardKeys.hndBrkKey)

            # engine brake
            elif message == 'engBrkOn':
                keyboard.press(switchboardButtons.engBrkKey)
            elif message == 'engBrkOff':
                keyboard.release(switchboardButtons.engBrkKey)

            # axle lifting
            elif message == 'truAxl':
                keyboard.press_and_release(switchboardButtons.truAxlKey)
            elif message == 'trlAxl':
                keyboard.press_and_release(switchboardButtons.trlAxlKey)

            # windows
            # right window
            elif message == 'winRdnOn':
                keyboard.press(windowButtons.winRdnKey)
            elif message == 'winRdnOff':
                keyboard.release(windowButtons.winRdnKey)
            elif message == 'winRupOn':
                keyboard.press(windowButtons.winRupKey)
            elif message == 'winRupOff':
                keyboard.release(windowButtons.winRupKey)

            # left window
            elif message == 'winLdnOn':
                keyboard.press(windowButtons.winLdnKey)
            elif message == 'winLdnOff':
                keyboard.release(windowButtons.winLdnKey)
            elif message == 'winLupOn':
                keyboard.press(windowButtons.winLupKey)
            elif message == 'winLupOff':
                keyboard.release(windowButtons.winLupKey)

            # suspension
            # front suspension
            elif message == 'susFrtUpOn':
                keyboard.press(suspensionButtons.susFrtUpKey)
            elif message == 'susFrtUpOff':
                keyboard.release(suspensionButtons.susFrtUpKey)
            elif message == 'susFrtDnOn':
                keyboard.press(suspensionButtons.susFrtDnKey)
            elif message == 'susFrtDnOff':
                keyboard.release(suspensionButtons.susFrtDnKey)

            # rear suspension
            elif message == 'susBckUpOn':
                keyboard.press(suspensionButtons.susBckUpKey)
            elif message == 'susBckUpOff':
                keyboard.release(suspensionButtons.susBckUpKey)
            elif message == 'susBckDnOn':
                keyboard.press(suspensionButtons.susBckDnKey)
            elif message == 'susBckDnOff':
                keyboard.release(suspensionButtons.susBckDnKey)

            elif message == 'susReset':
                keyboard.press_and_release(suspensionButtons.susResetKey)

            if debugMode:
                if message == 'hndshkresp':
                    print('Handshake completed!')

    response = urlopen(url)
    data_json = json.loads(response.read())
    data_truck = data_json.get('truck')

    indBlnLft = data_json["truck"]["blinkerLeftOn"]
    indBlnRgt = data_json["truck"]["blinkerRightOn"]
    indLgtHgh = getState('lightsBeamHighOn')
    indLgtPrk = getState('lightsParkingOn')
    indLgtLow = getState('lightsBeamLowOn')
    indLgtBcn = getState('lightsBeaconOn')
    indHndBrk = getState('parkBrakeOn')
    indNoChrg = getState('batteryVoltageWarningOn')
    indNoOilp = getState('oilPressureWarningOn')
    truckElec = getState('electricOn')
    indAirLow = getState('airPressureWarningOn')
    indFueLow = getState('fuelWarningOn')
    indChcEngVal = getState('wearEngine')
    indRetardVal = getState('retarderBrake')
    indCruise = getState('cruiseControlOn')
    indWaterTemp = getState('waterTemperatureWarningOn')

    if indChcEngVal < 0.1:
        indChcEngState = False
    elif indChcEngVal >= 0.1:
        indChcEngState = True

    if indRetardVal > 0:
        indRetardState = True
    elif indRetardVal == 0:
        indRetardState = False

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

        if indAirLow != indAirLowPrevState:
            if indAirLow:
                sendArduino('indAirLowOn')
                debugprint('Air pressure warning on, code sent!')
                indAirLowPrevState = True
            elif not indAirLow:
                sendArduino('indAirLowOff')
                debugprint('Air pressure warning off, code sent!')
                indAirLowPrevState = False

        if indFueLow != indFueLowPrevState:
            if indFueLow:
                sendArduino('indFueLowOn')
                debugprint('Fuel warning on, code sent!')
                indFueLowPrevState = True
            elif not indFueLow:
                sendArduino('indFueLowOff')
                debugprint('Fuel warning off, code sent!')
                indFueLowPrevState = False

        if indChcEngState != indChcEngPrevState:
            if indChcEngState:
                sendArduino('indChcEngOn')
                debugprint('Check engine light on, code sent!')
                indChcEngPrevState = True
            elif not indChcEngState:
                sendArduino('indChcEngOff')
                debugprint('Check engine light off, code sent!')
                indChcEngPrevState = False

        if indRetardState != indRetardPrevState:
            if indRetardState:
                sendArduino('indRetardOn')
                debugprint('Retarder light on, code sent!')
                indRetardPrevState = True
            elif not indRetardState:
                sendArduino('indRetardOff')
                debugprint('Retarder light off, code sent!')
                indRetardPrevState = False
        if indCruise != indCruisePrevState:
            if indCruise:
                sendArduino('indCruiseOn')
                debugprint('Cruise control on, code sent!')
                indCruisePrevState = True
            elif not indCruise:
                sendArduino('indCruiseOff')
                debugprint('Cruise control off, code sent!')
                indCruisePrevState = False

        if indWaterTemp != indWaterTempPrevState:
            if indWaterTemp:
                sendArduino('indWatTemOn')
                debugprint('Water temperature warning on, code sent!')
                indWaterTempPrevState = True
            elif not indWaterTemp:
                sendArduino('indWatTemOff')
                debugprint('Water temperature warning off, code sent!')
                indWaterTempPrevState = False

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
        if indAirLowPrevState:
            sendArduino('indAirLowOff')
            debugprint('Air warning light off with electricity, code sent!')
            indAirLowPrevState = False
        if indFueLowPrevState:
            sendArduino('indFueLowOff')
            debugprint('Fuel warning light off with electricity, code sent!')
            indFueLowPrevState = False
        if indChcEngPrevState:
            sendArduino('indChcEngOff')
            debugprint('Check engine light off with electricity, code sent!')
            indChcEngPrevState = False
        if indRetardPrevState:
            sendArduino('indRetardOff')
            debugprint('Retarder light off with electricity, code sent!')
            indRetardPrevState = False
        if indCruisePrevState:
            sendArduino('indCruiseOff')
            debugprint('Cruise control off with electricity, code sent!')
            indCruisePrevState = False
        if indWaterTempPrevState:
            sendArduino('indWatTemOff')
            debugprint('Water temperature warning off with electricity, code sent!')
            indWaterTempPrevState = False
