import os

lightSensorCalibration = {0: (1100, 2000),
                          10: (3000, 3600),
                          20: (3000, 3600),
                          30: (7000, 8500),
                          40: (3000, 3600),
                          50: (9000, 11750),
                          60: (3000, 3600),
                          70: (13000, 15000),
                          80: (3000, 3600),
                          90: (19000, 22000),
                          100: (26000, 30000)}

oColorTempList = {0: 2700,
                  20: 3460,
                  40: 4220,
                  60: 4980,
                  80: 5740,
                  100: 6500}

expectedNodeDescResp = ['NodeDesc:FD90,00',
                        'Type:FFD',
                        'ComplexDesc:No',
                        'UserDesc:No',
                        'APSFlags:00',
                        'FreqBand:40',
                        'MacCap:8E',
                        'ManufCode:1039',
                        'MaxBufSize:52',
                        'MaxInSize:00FF',
                        'SrvMask:0000',
                        'MaxOutSize:00FF',
                        'DescCap:00']

oWeekDayList = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

oHeatScheduleDict = {
    'sat': [('07:00', 28.5), ('09:00', 10.5), ('16:30', 23.5), ('22:00', 15), ('22:00', 15), ('22:00', 15)],
    'sun': [('01:00', 27.5), ('02:00', 1), ('03:00', 12), ('04:00', 1), ('05:00', 28.5), ('23:45', 1)],
    'fri': [('17:30', 1), ('18:00', 11), ('18:30', 28), ('19:00', 1), ('19:30', 29), ('20:00', 1)],
    'wed': [('06:30', 29.5), ('08:30', 13), ('12:00', 19), ('16:30', 22.5), ('22:00', 31), ('22:00', 31)],
    'mon': [('11:30', 27.5), ('11:45', 1), ('12:00', 12), ('12:15', 1), ('12:30', 28.5), ('12:45', 1)],
    'tue': [('06:30', 20), ('08:30', 10), ('16:30', 20), ('22:00', 10), ('22:00', 10), ('22:00', 10)],
    'thu': [('06:30', 20), ('08:30', 18.5), ('16:30', 27), ('22:00', 21), ('22:00', 21), ('22:00', 21)]}

oAtributeDict = {'HeatMode': '',
                 'WaterMode': '',
                 'HeatTemperature': '',
                 'HeatRunningState': '',
                 'WaterRuningState': '',
                 'HeatSchedule': '',
                 'WaterSchedule': ''
                 }

oModeList = ['MANUAL', 'AUTO', 'OFF', 'BOOST']

getWaterModes = {'MANUAL': 'Always ON',
                 'OFF': 'Always OFF',
                 'Always ON': 'Always ON',
                 'ON': 'Always ON',
                 'Always OFF': 'Always OFF',
                 'BOOST': 'BOOST',
                 'BOOST_CANCEL': 'BOOST_CANCEL',
                 'AUTO': 'AUTO',
                 'OVERRIDE': 'OVERRIDE',
                 None: 'None'
                 }

getPlugModes = {'MANUAL': 'MANUAL',
                'Always ON': 'MANUAL',
                'ON': 'MANUAL',
                'AUTO': 'AUTO',
                'SCHEDULE': 'AUTO',
                None: 'None'
                }

nodeTypeDict = {'hub': 'class.hub',
                'boilermodule': 'class.thermostat.json',
                'thermostatui': 'class.thermostatui.json',
                'activeplug': 'class.smartplug.json',
                'contactsensor': 'class.contact.sensor',
                'motionsensor': 'class.motion.sensor',
                'warmwhitelight': 'class.light.json',
                'tuneablelight': 'class.tunable.light.json',
                'colourtuneablelight': 'class.colour.tunable.light.json',
                'signalbooster': 'class.zigbee.range.extender',
                'smartplug': 'class.smartplug.json'
                }
waterModes = [['OFF'],
              ['MANUAL'],
              ['AUTO'],
              ['OFF', 'BOOST'],
              ['MANUAL', 'BOOST'],
              ['AUTO', 'BOOST']]

heatModes = [['OFF'],
             ['MANUAL'],
             ['AUTO'],
             ['AUTO', 'OVERRIDE'],
             ['OFF', 'BOOST'],
             ['MANUAL', 'BOOST'],
             ['AUTO', 'BOOST'],
             ['AUTO', 'OVERRIDE', 'BOOST'],
             ['OFF', 'BOOST', 'BOOST'],
             ['MANUAL', 'BOOST', 'BOOST'],
             ['AUTO', 'BOOST', 'BOOST'],
             ['AUTO', 'BOOST', 'BOOST']]

oWeekDayDict = {'SUNDAY': 'sun',
                'MONDAY': 'mon',
                'TUESDAY': 'tue',
                'WEDNESDAY': 'wed',
                'THURSDAY': 'thu',
                'FRIDAY': 'fri',
                'SATURDAY': 'sat'}

oEventPositionDict = {'FIRST': 1,
                      'SECOND': 2,
                      'THIRD': 3,
                      'FOURTH': 4,
                      'FIFTH': 5,
                      'SIXTH': 6}

oWaterStateDict = {'ON': 99.0,
                   'OFF': 0.0,
                   99.0: 'ON',
                   0.0: 'OFF'}

oPlugStateDict = {'ON': 'ON',
                  'OFF': 'OFF',
                  99.0: 'ON',
                  0.0: 'OFF'}

testModesCommandList = {"VERSIONS": "test Gver",
                        "RESET": "reset",
                        "DEVICETYPE": "test Gdev",
                        "STACKVERSION": "test Gstk",
                        "EUI": "test Geui",
                        "BATTERYVOLTAGE": "test Gvcc",
                        "LEDON": "test SledA",
                        "LEDOFF": "test Sleda",
                        "RADIO11": "test Srad11",
                        "RADIO12": "test Srad12",
                        "RADIO13": "test Srad13",
                        "RADIO14": "test Srad14",
                        "RADIO15": "test Srad15",
                        "RADIO16": "test Srad16",
                        "RADIO17": "test Srad17",
                        "RADIO18": "test Srad18",
                        "RADIO19": "test Srad19",
                        "RADIO20": "test Srad20",
                        "RADIO21": "test Srad21",
                        "RADIO22": "test Srad22",
                        "RADIO23": "test Srad23",
                        "RADIO24": "test Srad24",
                        "RADIO25": "test Srad25",
                        "RADIO26": "test Srad26",
                        "RADIOSTOP": "test Srad",
                        "SLEEP": "test Sslp",
                        "ZIGBEE": "test Tzig",
                        "SWITCH": "test Tswi",
                        "REARBUTTON": "test Tbtn"}

testModesResponseList = {"VERSIONS": "Iver",
                         "RESET": "HIVEHOME.COM",
                         "DEVICETYPE": "IdevButton01",
                         "STACKVERSION": "Istk",
                         "EUI": "Ieui",
                         "BATTERYVOLTAGE": "Ivcc",
                         "LEDON": "Cled",
                         "LEDOFF": "Cled",
                         "RADIO11": "Crad11",
                         "RADIO12": "Crad12",
                         "RADIO13": "Crad13",
                         "RADIO14": "Crad14",
                         "RADIO15": "Crad15",
                         "RADIO16": "Crad16",
                         "RADIO17": "Crad17",
                         "RADIO18": "Crad18",
                         "RADIO19": "Crad19",
                         "RADIO20": "Crad20",
                         "RADIO21": "Crad21",
                         "RADIO22": "Crad22",
                         "RADIO23": "Crad23",
                         "RADIO24": "Crad24",
                         "RADIO25": "Crad25",
                         "RADIO26": "Crad26",
                         "RADIOSTOP": "Crad",
                         "SLEEP": "Cslp",
                         "ZIGBEE": "Izig",
                         "SWITCH": "Cswi",
                         "REARBUTTON": "Cbtn"}

sensorTestModesCommandList = {"VERSIONS": "test Gver",
                              "MOTIONDEVICETYPE": "test Gdev",
                              "CONTACTDEVICETYPE": "test Gdev",
                              "STACKVERSION": "test Gstk",
                              "EUI": "test Geui",
                              "TEMP": "test Gtmp",
                              "BATTERYVOLTAGE": "test Gvcc",
                              "LUX": "test Glux",
                              "LEDRON": "test SledRg",
                              "LEDGON": "test SledrG",
                              "LEDOFF": "test Sledrg",
                              "NVM": "test Snvm",
                              "RADIO11": "test Trad11",
                              "RADIO12": "test Trad12",
                              "RADIO13": "test Trad13",
                              "RADIO14": "test Trad14",
                              "RADIO15": "test Trad15",
                              "RADIO16": "test Trad16",
                              "RADIO17": "test Trad17",
                              "RADIO18": "test Trad18",
                              "RADIO19": "test Trad19",
                              "RADIO20": "test Trad20",
                              "RADIO21": "test Trad21",
                              "RADIO22": "test Trad22",
                              "RADIO23": "test Trad23",
                              "RADIO24": "test Trad24",
                              "RADIO25": "test Trad25",
                              "RADIO26": "test Trad26",
                              "RADIOSTOP": "test Srad",
                              "ZIGBEE11": "test Tzig11",
                              "ZIGBEE12": "test Tzig12",
                              "ZIGBEE13": "test Tzig13",
                              "ZIGBEE14": "test Tzig14",
                              "ZIGBEE15": "test Tzig15",
                              "ZIGBEE16": "test Tzig16",
                              "ZIGBEE17": "test Tzig17",
                              "ZIGBEE18": "test Tzig18",
                              "ZIGBEE19": "test Tzig19",
                              "ZIGBEE20": "test Tzig20",
                              "ZIGBEE21": "test Tzig21",
                              "ZIGBEE22": "test Tzig22",
                              "ZIGBEE23": "test Tzig23",
                              "ZIGBEE24": "test Tzig24",
                              "ZIGBEE25": "test Tzig25",
                              "ZIGBEE26": "test Tzig26",
                              "MEMORY": "test Tmem",
                              "PIR": "test Tpir",
                              "MAGNET": "test Tmag",
                              "REARBUTTON": "test Tbtn"}

sensorTestModesResponseList = {"VERSIONS": "IverIceOS",
                               "MOTIONDEVICETYPE": "IdevMotion sensor",
                               "CONTACTDEVICETYPE": "IdevContact sensor",
                               "STACKVERSION": "IstkZStack",
                               "TEMP": "Itmp",
                               "EUI": "Ieui",
                               "BATTERYVOLTAGE": "Ivcc",
                               "LUX": "Ilux",
                               "LEDRON": "CledRg",
                               "LEDGON": "CledrG",
                               "LEDOFF": "CledrG",
                               "NVM": "RnvmP",
                               "RADIO11": "Crad11",
                               "RADIO12": "Crad12",
                               "RADIO13": "Crad13",
                               "RADIO14": "Crad14",
                               "RADIO15": "Crad15",
                               "RADIO16": "Crad16",
                               "RADIO17": "Crad17",
                               "RADIO18": "Crad18",
                               "RADIO19": "Crad19",
                               "RADIO20": "Crad20",
                               "RADIO21": "Crad21",
                               "RADIO22": "Crad22",
                               "RADIO23": "Crad23",
                               "RADIO24": "Crad24",
                               "RADIO25": "Crad25",
                               "RADIO26": "Crad26",
                               "RADIOSTOP": "RradF",
                               "ZIGBEE11": "Izig11",
                               "ZIGBEE12": "Izig12",
                               "ZIGBEE13": "Izig13",
                               "ZIGBEE14": "Izig14",
                               "ZIGBEE15": "Izig15",
                               "ZIGBEE16": "Izig16",
                               "ZIGBEE17": "Izig17",
                               "ZIGBEE18": "Izig18",
                               "ZIGBEE19": "Izig19",
                               "ZIGBEE20": "Izig20",
                               "ZIGBEE21": "Izig21",
                               "ZIGBEE22": "Izig22",
                               "ZIGBEE23": "Izig23",
                               "ZIGBEE24": "Izig24",
                               "ZIGBEE25": "Izig25",
                               "ZIGBEE26": "Izig26",
                               "SWITCH": "Cswi",
                               "MEMORY": "RmemP",
                               "PIR": "RpirP",
                               "MAGNET": "RmagP",
                               "REARBUTTON": "RbtnF"}

""" The Global device ID """
device_id = 'SLT4_1'
''' The device end point '''
DEVICE_ENDPOINT = '05'
'''The stat cluser'''
THERMOSTAT_CLUSTER = '0201'
'''The mcode used to read the manufacturer attribute'''
MANUFACTURER_CODE = '1039'
''' The custom cluster for SLT4'''
MANUFACTURER_CUSTOM_CLUSTER = 'FD01'
''' The stat UI cluster '''
STAT_UI_CLUSTER = '0204'
STAT_HUMIDIFIER_CLUSTER = '0203'

MANUFACTURER_CLUSTER_ATTRIBUTES = {
    'PROTECTION_TIMER': '0021',
    'WIRING_CONNECTION': '0036',
    'HUMIDIFICATION_CONTROL': '0032'
}

''' The user modes that will be used to interact with the stat in the test cases'''
USER_MODES = {
    'OFF': 0,
    'HEAT HOLD': 1,
    'HEAT SCHEDULE': 2,
    'COOL HOLD': 3,
    'COOL SCHEDULE': 4,
    'DUAL HOLD': 5,
    'DUAL SCHEDULE': 6,
    'HEAT_BOOST': 7,
    'COOL_BOOST': 8
}

'''Constants for various mode switch '''
DEVICE_MODE = {
    "OFF": "00",
    "DUAL": "01",
    "COOL": "03",
    "HEAT": "04",
    "EMERGENCY_HEAT": "05",
    "HEAT_BOOST": "14",
    "COOL_BOOST": "13"
}

'''Fan Modes'''
FAN_MODE = {
    'AUTO': '05',
    'ALWAYS_ON': '04',
    'CIRCULATE': '07'
}

''' Constants indicating the device Schedule type and mode '''
DEVICE_SCHEDULE_TYPE = {
    'HOLD': '01',
    'SCHEDULE': '00'
}

DEVICE_CLUSTER_ATTRIBUTES = {
    'MODE': '001C',
    'SCHEDULE_OR_HOLD': '0023',
    'DURATION': '0024',
    'HEAT_TEMP': '0012',
    'COOL_TEMP': '0011',
    'LOCAL_TEMP': '0000',
    'STAT_RUNNING_STATE': '0029',
    'MIN_COOL_TEMP': '0005',
    'MAX_COOL_TEMP': '0006',
    'MIN_HEATING_TEMP': '0003',
    'MAX_HEATING_TEMP': '0004'

}

TEMPERATURE_MODE = {
    'FAHRENHEIT': 0,
    'CELCIUS': 1
}

DEVICE_UI_ATTRIBUTES = {
    'TEMPERATURE_SCALE': '0000'
}
sch_days = {'sun': '01', 'mon': '02', 'tue': '04', 'wed': '08', 'thu': '10', 'fri': '20', 'sat': '40'}

# Setup some constants
debug = False

# Device Types
lampType = 'Lamp'
thermostatType = 'HeatingController'
meterReaderType = 'MeterReader'
smartplugType = 'SmartPlug'
binarySwitchType = 'GenericBinarySwitch'
# Emperor Device Types
empBoilerModule1 = 'HAHVACThermostat'
empBoilerModule2 = 'HAHVACThermostatSLR2'

empThermostat = 'HAHVACTemperatureSensor'
SLT3Thermostat = 'HAHVACTemperatureSensorSLT3'

# Dictionaries of parameters for each data channel
# Channels have various data point intervals and values that can be specified
cost_dict = {'interval': '1', 'operations': 'average+min+max+amount'}
power_dict = {'interval': '1', 'operations': 'average+min+max'}
energy_dict = {'interval': '1', 'operations': 'average+min+max'}

# Min.Max and Average all contain the same values for signal,battery and temperature so only get average.
# AlertMe only have average in the battery channel
temperature_dict = {'interval': '120', 'operations': 'average'}
signal_dict = {'interval': '120', 'operations': 'average'}
battery_dict = {'interval': '86400', 'operations': 'average'}
targetTemperature_dict = {'interval': '120', 'operations': 'average'}
controllerState_dict = {'interval': '120', 'operations': 'dataset'}
rssi_dict = {'interval': '120', 'operations': 'average'}

# Dictionary of device types vs channels and query parameters
deviceChannelParameters = {thermostatType: {'temperature': temperature_dict,
                                            'battery': battery_dict,
                                            'signal': signal_dict},
                           meterReaderType: {'cost': cost_dict,
                                             'battery': battery_dict,
                                             'temperature': temperature_dict,
                                             'power': power_dict,
                                             'signal': signal_dict},
                           empBoilerModule1: {'temperature': temperature_dict,
                                              'signal': signal_dict,
                                              'targetTemperature': targetTemperature_dict,
                                              'controllerState': controllerState_dict,
                                              'rssi': rssi_dict},
                           empBoilerModule2: {'temperature': temperature_dict,
                                              'signal': signal_dict,
                                              'targetTemperature': targetTemperature_dict,
                                              'controllerState': controllerState_dict,
                                              'rssi': rssi_dict},
                           empThermostat: {'temperature': temperature_dict,
                                           'battery': battery_dict,
                                           'signal': signal_dict,
                                           'rssi': rssi_dict},
                           lampType: {'signal': signal_dict},
                           binarySwitchType: {'signal': signal_dict, 'rssi': rssi_dict},
                           smartplugType: {'signal': signal_dict,
                                           'battery': battery_dict,
                                           'temperature': temperature_dict}}

# Server Information and Tokens. Modify pathToFiles from calling module to store files elsewhere.
API_CREDENTIALS = None

strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../../../02_Manager_Tier/EnviromentFile/")
