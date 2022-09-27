import yaml
import serial.tools.list_ports
from time import sleep
from urllib.request import urlopen
from functions import set_port
from functions import set_url
from functions import readArduinoConfig

def firstRun():
    baudRate = readArduinoConfig('baudRate')

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
    readingPort = True

    while readingPort:
        portReadFromInput = input()
        try:
            arduino = serial.Serial(port=portReadFromInput, baudrate=baudRate, timeout=.1)
            arduino.write(b'hndshk')
            arduino.write(b'\n')
            readingPort = False
        except Exception as e:
            print('Wrong port, please try again!')
            print(e)

    set_port(portReadFromInput)
    print('Port was set!')
    print()
    print('Please set the telemetry API url!')
    print('Paste it here:')
    readingUrl = True

    while readingUrl:
        urlInput = input()
        set_url(urlInput)
        try:
            response = urlopen(urlInput)
            print('Url okay, ending setup.')
            readingUrl = False
        except:
            print('Url not found. Please enter a valid url and make sure your telemetry server is running!')
            print('Enter a valid url!')

    print('Setup completed, exiting software in 3 seconds, please restart!')

    with open("config.yml", 'r') as config:
        doc = yaml.safe_load(config)
        cfg = doc['CONFIG']
        cfg['firstRun'] = False
    with open('config.yml', 'w') as config:
        yaml.safe_dump(doc, config, default_flow_style=False)

    sleep(3)
    exit()