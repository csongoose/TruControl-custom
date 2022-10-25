import json
from urllib.request import urlopen
import yaml
import serial.tools.list_ports
import firstrun
import keyboard
import pydirectinput as pyautogui
import inputhandling
from functions import (readConfig, readArduinoConfig, debugprint, askForSetup)

name = "TruControl Custom"  # code cleaned up
version = "0.1.2"

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
    sendArduino('hndshk')
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
indLgtPrkPrevState = getPrevState('lightsParkingOn')  #
indLgtLowPrevState = getPrevState('lightsBeamLowOn')  #
indLgtBcnPrevState = getPrevState('lightsBeaconOn')  #
# no diff lock info!
indHndBrkPrevState = getPrevState('parkBrakeOn')  #
indNoChrgPrevState = getPrevState('batteryVoltageWarningOn')  #
indNoOilpPrevState = getPrevState('oilPressureWarningOn')  #
truckElecPrevState = getPrevState('electricOn')

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
    while arduino.inWaiting():  # input handling
        message = arduino.readline().decode('utf-8').partition('\r')[0]

        # retarder
        if message == 'retOff':
            pyautogui.press(retarderKeys.retOffKey)
        elif message == 'retPos1':
            pyautogui.press(retarderKeys.retPos1Key)
        elif message == 'retPos2':
            pyautogui.press(retarderKeys.retPos2Key)
        elif message == 'retPos3':
            pyautogui.press(retarderKeys.retPos3Key)
        elif message == 'retPos4':
            pyautogui.press(retarderKeys.retPos4Key)

        # lights
        elif message == 'lgtOff':
            pyautogui.press(lightKeys.lgtOffKey)
        elif message == 'lgtPrk':
            pyautogui.press(lightKeys.lgtPrkKey)
        elif message == 'lgtLow':
            pyautogui.press(lightKeys.lgtLowKey)
        elif message == 'lgtHgh':
            pyautogui.press(lightKeys.lgtHghKey)

        # blinkers
        elif message == 'blnLftOn' or message == 'blnLftOff':
            pyautogui.press(blinkerKeys.blnLftKey)
        elif message == 'blnRgtOn' or message == 'blnRgtOff':
            pyautogui.press(blinkerKeys.blnRgtKey)

        # wipers
        elif message == 'wipOff':
            keyboard.press_and_release(wiperKeys.wipOffKey)
        elif message == 'wipSpd1':
            keyboard.press_and_release(wiperKeys.wipSpd1Key)
        elif message == 'wipSpd2':
            keyboard.press_and_release(wiperKeys.wipSpd2Key)
        elif message == 'wipSpd3':
            keyboard.press_and_release(wiperKeys.wipSpd3Key)

        # ignition and electrics - NOTE: handled by keyboard module due to the numpad limitations of pyautogui
        elif message == 'elcOff':
            keyboard.press_and_release(ignitionKeys.elcOffKey)
        elif message == 'elcIgn':
            keyboard.press_and_release(ignitionKeys.elcIgnKey)
        elif message == 'engSrt':
            keyboard.press_and_release(ignitionKeys.engSrtKey)

        # switches on the switchboard:
        elif message == 'trdWhl':
            pyautogui.press(switchboardKeys.trdWhlKey)
        elif message == 'lgtBcn':
            pyautogui.press(switchboardKeys.lgtBcnKey)
        elif message == 'lgtHzd':
            pyautogui.press(switchboardKeys.lgtHzdKey)
        elif message == 'difLoc':
            pyautogui.press(switchboardKeys.difLocKey)
        elif message == 'hndBrk':
            pyautogui.press(switchboardKeys.hndBrkKey)

        # engine brake
        elif message == 'engBrkOn':
            pyautogui.keyDown(switchboardButtons.engBrkKey)
        elif message == 'engBrkOff':
            pyautogui.keyUp(switchboardButtons.engBrkKey)

        # axle lifting
        elif message == 'truAxl':
            pyautogui.press(switchboardButtons.truAxlKey)
        elif message == 'trlAxl':
            pyautogui.press(switchboardButtons.trlAxlKey)

        # windows
        # right window
        elif message == 'winRdnOn':
            pyautogui.keyDown(windowButtons.winRdnKey)
        elif message == 'winRdnOff':
            pyautogui.keyUp(windowButtons.winRdnKey)
        elif message == 'winRupOn':
            pyautogui.keyDown(windowButtons.winRupKey)
        elif message == 'winRupOff':
            pyautogui.keyUp(windowButtons.winRupKey)

        # left window
        elif message == 'winLdnOn':
            pyautogui.keyDown(windowButtons.winLdnKey)
        elif message == 'winLdnOff':
            pyautogui.keyUp(windowButtons.winLdnKey)
        elif message == 'winLupOn':
            pyautogui.keyDown(windowButtons.winLupKey)
        elif message == 'winLdnOn':
            pyautogui.keyUp(windowButtons.winLupKey)

        # suspension
        # front suspension
        elif message == 'susFrtUpOn':
            keyboard.press(suspensionButtons.susFrtUpKey)
        elif message == 'susFrtUpOff':
            keyboard.release(suspensionButtons.susFrtUpKey)
        elif message == 'susFrtDnOn':
            keyboard.press(suspensionButtons.susFrtDnKey)
        elif message == 'susFrtUpOn':
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
            pyautogui.press(suspensionButtons.susResetKey)

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
