# Config for zigbeeTools
# File path, UART config, NodeID and Endpoint
import serial
import subprocess
import platform
import sys

FIRMWARE_ROOT_FILE_PATH = '/home/pi/hardware/firmware-release-notes//'

# Serial Port Parameters
# PORT = '/dev/ttyUSB0'
BUTTON_PORT = '/dev/cu.usbserial-FT9QCVEU'
# Serial Port Parameters
if 'DARWIN' in platform.system().upper():
    networkBasePath = '/volumes/hardware/'
    PORT = '/dev/tty.SLAB_USBtoUART'
    # BUTTON_PORT = str(subprocess.run("ls /dev/cu.usb*", shell=True, stdout=subprocess.PIPE,
    #                        universal_newlines=True).stdout).replace("\n","")
elif 'LINUX' in platform.system().upper():
    networkBasePath = '/home/pi/hardware/'
    PORT = '/dev/ttyUSB0'
elif sys.platform.startswith('win'):
    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    FinalPort = ""
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
            FinalPort = port
        except (OSError, serial.SerialException):
            pass
    print(result)
    networkBasePath = "\\\\nas1\Hardware\\"
    PORT = FinalPort
else:
    networkBasePath = ""
    PORT = ""
# PORT = '/dev/tty.SLAB_USBtoUART'
BAUD = 115200
CAMPORT = '/dev/tty.usbmodem1411'
# NodeID & Endpoint
NODE_ID = '07CA'
EP_ID = '06'
TOPOLOGY_PLUG_API_URL = 'devices-rpi3.local:8081'
TOPOLOGY_PLUG_NODE_DICT = {'BOX1':'7C1B','BOX2':'DF76','BOX3':'AF01','BOX4':'9CB4'}
RPIURL = {#"RPI1": "http://devices-rpi1.local:8081",
                          "RPI2": "http://devices-rpi2.local:8081",
                          "RPI3": "http://devices-rpi3.local:8081",
                          "RPI4": "http://devices-rpi4.local:8081",
                          "RPI5": "http://devices-rpi5.local:8081",
                          #"RPI6": "http://devices-rpi6.local:8081",
                          "RPI7": "http://devices-rpi7.local:8081",
                          "RPI8": "http://devices-rpi8.local:8081",
                          "RPI9": "http://devices-rpi9.local:8081",
                          "RPI10": "http://devices-rpi10.local:8081",
                          #"RPI11": "http://devices-rpi11.local:8081",
                          "RPI12": "http://devices-rpi12.local:8081",
                          #"RPI13": "http://devices-rpi13.local:8081",
                          #"RPI14": "http://devices-rpi14.local:8081",
                          #"RPI15": "http://devices-rpi15.local:8081",
                          #"RPI16": "http://devices-rpi16.local:8081",
                          }

