"""
Created on Nov 27, 2014

@author: keith
"""

statusCodes = {'SUCCESS': '00',
               'ZCL_MALFORMED_COMMAND': '80',
               'ZCL_UNSUPPORTED_CLUSTER_COMMAND': '81',
               'ZCL_UNSUPPORTED_GENERAL_COMMAND': '82',
               'ZCL_UNSUPPORTED_MANUFACTURER_CLUSTER_COMMAND': '83',
               'ZCL_UNSUPPORTED_MANUFACTURER_GENERAL_COMMAND': '84',
               'ZCL_INVALID_FIELD': '85',
               'ZCL_UNSUPPORTED_ATTRIBUTE': '86',
               'ZCL_INVALID_VALUE': '87',
               'ZCL_READ_ONLY': '88',
               'ZCL_INSUFFICIENT_SPACE': '89',
               'ZCL_DUPLICATE_EXISTS': '8A',
               'ZCL_NOT_FOUND': '8B',
               'ZCL_UNREPORTABLE_ATTRIBUTE': '8C',
               'ZCL_RESERVED': 'C3',
               'ZCL_INVALID_DATA_TYPE': '8D'}

scLookup = dict((cn, cs) for cs, cn in statusCodes.items())

deviceIDs = {'0008': 'Range Extender',
             '0009': 'Mains Power Outlet',
             '0051': 'Smart plug',
             '0100': 'On/Off light',
             '0101': 'Dimmable Light',
             '0102': 'Color Dimmable Light',
             '0301': 'Thermostat',
             '0302': 'Temperature Sensor',
             '0402': 'IAS Zone',
             }

dataTypes = {'10': {'name': 'boolean', 'bits': 8, 'type': 'D'},
             '18': {'name': 'bitmap8', 'bits': 8, 'type': 'D'},
             '19': {'name': 'bitmap16', 'bits': 16, 'type': 'D'},
             '20': {'name': 'uint8', 'bits': 8, 'type': 'A'},
             '21': {'name': 'uint16', 'bits': 16, 'type': 'A'},
             '23': {'name': 'uint32', 'bits': 32, 'type': 'A'},
             '25': {'name': 'uint48', 'bits': 48, 'type': 'A'},
             '28': {'name': 'int8', 'bits': 8, 'type': 'A'},
             '29': {'name': 'int16', 'bits': 16, 'type': 'A'},
             '2A': {'name': 'int24', 'bits': 24, 'type': 'A'},
             '2B': {'name': 'int32', 'bits': 32, 'type': 'A'},
             '30': {'name': 'enum8', 'bits': 8, 'type': 'D'},
             '42': {'name': 'charString', 'bits': 0, 'type': 'D'},
             'E2': {'name': 'utcTime', 'bits': 32, 'type': 'A'},
             'F0': {'name': 'ieeAddress', 'bits': 64, 'type': 'D'}}

basicClusterAttrs = {
    '0000': {'name': 'zclVersion', 'type': '20'},
    '0001': {'name': 'applicationVersion', 'type': '20'},
    '0002': {'name': 'stackVersion', 'type': '20'},
    '0003': {'name': 'hardwareVersion', 'type': '20'},
    '0004': {'name': 'manufacturerName', 'type': '42'},
    '0005': {'name': 'modelIdentifier', 'type': '42'},
    '0006': {'name': 'dateCode', 'type': '42'},
    '0007': {'name': 'powerSource', 'type': '30'},
    '0008': {'name': 'applicationProfileVersion', 'type': '23'},
    '0009': {'name': 'genericDeviceType', 'type': '30'},
    '000A': {'name': 'productCode', 'type': '41'},
    '000B': {'name': 'productUrl', 'type': '42'},
    '0010': {'name': 'locationDescription', 'type': '42'},
    '0011': {'name': 'physicalEnvironment', 'type': '30'},
    '0012': {'name': 'deviceEnabled', 'type': '10'},
    '0013': {'name': 'alarmMask', 'type': '18'},
    '0014': {'name': 'disableLocalConfig', 'type': '18'},
    '4000': {'name': 'sw build id', 'type': '42'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
    '0000_msp': {'name': '*** UNKOWN ATTRIBUTE', 'type': '20'},
    '0001_msp': {'name': '*** UNKOWN ATTRIBUTE', 'type': '27'},
    '0100_msp': {'name': 'LED Intensity', 'type': '20'},
    '4001_msp': {'name': '*** UNKOWN ATTRIBUTE', 'type': 'F1'},
    '4002_msp': {'name': '*** UNKOWN ATTRIBUTE', 'type': 'F0'},
    '8000_msp': {'name': 'Name not Found in Specification', 'type': '18'},
    '8001_msp': {'name': 'Boiler IQ Device Status', 'type': '18'},
    '8002_msp': {'name': 'Boiler IQ Device Status description', 'type': '42'},
    '8003_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8004_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8005_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8006_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8007_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8008_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8009_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '800A_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '800B_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '800C_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '800D_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '800E_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '800F_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8010_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8011_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8012_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8013_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8014_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8015_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8016_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8017_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8018_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '8019_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '801A_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '801B_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '801C_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '801D_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '801E_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},
    '801F_msp': {'name': 'Boiler IQ Device Configuration', 'type': '23'},

}

powerConfigurationClusterAttrs = {
    '0000': {'name': 'mainsVoltage', 'type': '21'},
    '0001': {'name': 'mainsFrequency', 'type': '20'},
    '0020': {'name': 'batteryVoltage', 'type': '20'},
    '0021': {'name': 'batteryPercentageRemaining', 'type': '20'},
    '0030': {'name': 'batteryManufacturer', 'type': '42'},
    '0031': {'name': 'batterySize', 'type': '30'},
    '0032': {'name': 'batteryAHrRating', 'type': '21'},
    '0033': {'name': 'batteryQuantity', 'type': '20'},
    '0034': {'name': 'batteryRatedVoltage', 'type': '20'},
    '0035': {'name': 'batteryAlarmMask', 'type': '18'},
    '0036': {'name': 'batteryVoltageMinThreshold', 'type': '20'},
    '0037': {'name': 'batteryVoltageThreshold1', 'type': '20'},
    '0038': {'name': 'batteryVoltageThreshold2', 'type': '20'},
    '0039': {'name': 'batteryVoltageThreshold3', 'type': '20'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

deviceTemperatureConfigurationClusterAttrs = {
    '0000': {'name': 'currentTemperature', 'type': '29'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

identifyClusterAttrs = {
    '0000': {'name': 'identifyTime', 'type': '21'},
    '0001': {'name': 'commissionState', 'type': '18'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

groupsClusterAttrs = {
    '0000': {'name': 'nameSupport', 'type': '18'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

scenesClusterAttrs = {
    '0000': {'name': 'sceneCount', 'type': '20'},
    '0001': {'name': 'currentScene', 'type': '20'},
    '0002': {'name': 'currentGroup', 'type': '21'},
    '0003': {'name': 'sceneValid', 'type': '10'},
    '0004': {'name': 'nameSupport', 'type': '18'},
    '0005': {'name': 'lastConfiguredBy', 'type': 'F0'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

onOffClusterAttrs = {
    '0000': {'name': 'onOff', 'type': '10'},
    '4000': {'name': 'GlobalSceneControl', 'type': '10'},
    '4001': {'name': 'OnTime', 'type': '21'},
    '4002': {'name': 'OffWaitTime', 'type': '21'},
    '4003': {'name': 'StartUpOnOff', 'type': '30'},
    'FD00': {'name': 'clickTypeCfg', 'type': '18'},
    'FD01': {'name': 'doubleClickTimer', 'type': '21'},
    'FD02': {'name': 'longClickTimer', 'type': '21'},
    'FD03': {'name': 'lastClickType', 'type': '18'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

levelControlClusterAttrs = {
    '0000': {'name': 'currentLevel', 'type': '20'},
    '0001': {'name': 'remainingTime', 'type': '21'},
    '0002': {'name': '*** UNKNOWN NEED TO RAISE ***', 'type': '21'},
    '000F': {'name': '*** UNKNOWN NEED TO RAISE ***', 'type': '18'},
    '0010': {'name': 'onOffTransitionTime', 'type': '21'},
    '0011': {'name': 'onLevel', 'type': '20'},
    '4000': {'name': 'StartupCurrentLevel', 'type': '30'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

alarmsClusterAttrs = {
    '0000': {'name': 'alarmCount', 'type': '21'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

timeClusterAttrs = {
    '0000': {'name': 'time', 'type': 'E2'},
    '0001': {'name': 'timeStatus', 'type': '18'},
    '0002': {'name': 'timeZone', 'type': '2B'},
    '0003': {'name': 'dstStart', 'type': '23'},
    '0004': {'name': 'dstEnd', 'type': '23'},
    '0005': {'name': 'dstShift', 'type': '2B'},
    '0007': {'name': 'localTime', 'type': '23'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

commissioningClusterAttrs = {
    '0000': {'name': 'shortAddress', 'type': '21'},
    '0001': {'name': 'extendedPanId', 'type': 'F0'},
    '0002': {'name': 'panId', 'type': '21'},
    '0003': {'name': 'channelMask', 'type': '1B'},
    '0006': {'name': 'startupControl', 'type': '30'},
    '0010': {'name': 'trustCentreAddress', 'type': 'F0'},
    '0011': {'name': 'trustCentreMasterKey', 'type': 'F1'},
    '0012': {'name': 'networkKey', 'type': 'F1'},
    '0013': {'name': 'unsecureJoin', 'type': '10'},
    '0014': {'name': 'preconfiguredLinkKey', 'type': 'F1'},
    '0015': {'name': 'networkKeySequenceNumber', 'type': '20'},
    '0016': {'name': 'networkKeyType', 'type': '30'},
    '0017': {'name': 'networkManagerAddress', 'type': '21'},
    '0020': {'name': 'scanAttempts', 'type': '20'},
    '0021': {'name': 'timeBetweenScans', 'type': '21'},
    '0022': {'name': 'rejoinInterval', 'type': '21'},
    '0023': {'name': 'maxRejoinInterval', 'type': '21'},
    '0030': {'name': 'indirectPollRate', 'type': '21'},
    '0031': {'name': 'parentRetryThreshold', 'type': '20'},
    '0040': {'name': 'concentratorFlag', 'type': '10'},
    '0041': {'name': 'concentratorRadius', 'type': '20'},
    '0042': {'name': 'concentratorDiscoveryTime', 'type': '20'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

otaClusterAttrs = {
    '0000': {'name': 'upgradeServerId', 'type': 'F0'},
    '0001': {'name': 'file Offset', 'type': '23'},
    '0002': {'name': 'current File Version', 'type': '23'},
    '0003': {'name': 'current ZigBee Stack Version', 'type': '21'},
    '0004': {'name': 'downloaded File Version', 'type': '23'},
    '0005': {'name': 'downloaded ZigBee Stack Version', 'type': '21'},
    '0006': {'name': 'image Upgrade Status', 'type': '30'},
    '0007': {'name': 'manufacturerId', 'type': '21'},
    '0008': {'name': 'imageTypeId', 'type': '21'},
    '0009': {'name': 'minimumBlockRequestDelay', 'type': '21'},
    '000A': {'name': 'imageStamp', 'type': '23'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

pollControlClusterAttrs = {
    '0000': {'name': 'checkInInterval', 'type': '23'},
    '0001': {'name': 'longPollInterval', 'type': '23'},
    '0002': {'name': 'shortPollInterval', 'type': '21'},
    '0003': {'name': 'fastPollTimeout', 'type': '21'},
    '0004': {'name': 'checkInIntervalMin', 'type': '23'},
    '0005': {'name': 'LongPollIntervalMin', 'type': '23'},
    '0006': {'name': 'fastPollTimeoutMax', 'type': '21'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

thermostatClusterAttrs = {
    '0000': {'name': 'localTemperature', 'type': '29'},
    '0001': {'name': 'outsideTemperature', 'type': '29'},
    '0002': {'name': 'occupancy', 'type': '00'},
    '0003': {'name': 'absMinHeatSetpointLimit', 'type': '29'},
    '0004': {'name': 'absMaxHeatSetpointLimit', 'type': '29'},
    '0005': {'name': 'absMinCoolSetpointLimit', 'type': '29'},
    '0006': {'name': 'absMaxCoolSetpointLimit', 'type': '29'},
    '0009': {'name': 'HVACSystemTypeConfiguration', 'type': '18'},
    '0010': {'name': 'localTemperatureCalibration', 'type': '28'},
    '0011': {'name': 'occupiedCoolingSetpoint', 'type': '29'},
    '0012': {'name': 'occupiedHeatingSetpoint', 'type': '29'},
    '0013': {'name': 'unoccupiedCoolingSetpoint', 'type': '29'},
    '0014': {'name': 'unoccupiedHeatingSetpoint', 'type': '29'},
    '0015': {'name': 'minHeatSetpointLimit', 'type': '29'},
    '0016': {'name': 'maxHeatSetpointLimit', 'type': '29'},
    '0017': {'name': 'minCoolSetpointLimit', 'type': '29'},
    '0018': {'name': 'maxCoolSetpointLimit', 'type': '29'},
    '0019': {'name': 'minSetPointDeadBand', 'type': '28'},
    '001B': {'name': 'controlSequenceOfOperation', 'type': '30'},
    '001C': {'name': 'systemMode', 'type': '30'},
    '001E': {'name': 'ThermostatRunningMode', 'type': '30'},
    '001D': {'name': 'alarmMask', 'type': '18'},
    '0020': {'name': 'startOfWeek', 'type': '30'},
    '0021': {'name': 'numberOfWeeklyTransitions', 'type': '20'},
    '0022': {'name': 'numberOfDailyTransitions', 'type': '20'},
    '0023': {'name': 'temperatureSetpointHold', 'type': '30'},
    '0024': {'name': 'temperatureSetpointHoldDuration', 'type': '21'},
    '0029': {'name': 'thermostatRunningState', 'type': '19'},
    '9540_msp': {'name': 'Thermostat/HotWaterTankLevel', 'type': '20'},
    '9541_msp': {'name': 'Thermostat/ZoneId', 'type': '20'},
    '9542_msp': {'name': 'Thermostat/ButtonStates', 'type': '18'},
    '9543_msp': {'name': 'Thermostat/FrostProtectionTemperature', 'type': '29'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

thermostatUiClusterAttrs = {
    '0000': {'name': 'temperatureDisplayMode', 'type': '30'},
    '0001': {'name': 'keypadLockout', 'type': '30'},
    '0002': {'name': 'scheduleProgrammingVisibility', 'type': '30'},
    '9550': {'name': '', 'type': '30'},
    '9551': {'name': '', 'type': '42'},
    '9552': {'name': '', 'type': '29'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

illuminanceClusterAttrs = {
    '0000': {'name': 'occupancy', 'type': '21'},
    '0001': {'name': 'occupancySensorType', 'type': '21'},
    '0002': {'name': 'PirOccupiedToUnoccupiedDelay', 'type': '21'},
    '0003': {'name': 'PirUnoccupiedToOccupiedDelay', 'type': '21'},
    '0004': {'name': 'PirUnoccupiedToOccupiedThreshold', 'type': '30'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

colorControlClusterAttrs = {
    '0000': {'name': 'currentHue', 'type': '20'},
    '0001': {'name': 'currentSaturation', 'type': '20'},
    '0002': {'name': 'remainingTime', 'type': '21'},
    '0003': {'name': 'currentX', 'type': '21'},
    '0004': {'name': 'currentY', 'type': '21'},
    '0007': {'name': 'colorTemperature', 'type': '21'},
    '0008': {'name': 'colorMode', 'type': '30'},
    '000F': {'name': '*** UNKNOWN NEED TO RAISE ***', 'type': '18'},
    '0010': {'name': 'numberOfPrimaries', 'type': '20'},
    '0011': {'name': 'primary1X', 'type': '21'},
    '0012': {'name': 'primary1Y', 'type': '21'},
    '0013': {'name': 'primaryIntensity', 'type': '20'},
    '0015': {'name': 'primary2X', 'type': '21'},
    '0016': {'name': 'primary2Y', 'type': '21'},
    '0017': {'name': 'primary2Intensity', 'type': '20'},
    '0019': {'name': 'primary3X', 'type': '21'},
    '001A': {'name': 'primary3Y', 'type': '21'},
    '001B': {'name': 'primary3Intensity', 'type': '20'},
    '0020': {'name': 'primary4X', 'type': '21'},
    '0021': {'name': 'primary4Y', 'type': '21'},
    '0022': {'name': 'primary4Intensity', 'type': '20'},
    '0024': {'name': 'primary5X', 'type': '21'},
    '0025': {'name': 'primary5Y', 'type': '21'},
    '0026': {'name': 'primary5Intensity', 'type': '20'},
    '0028': {'name': 'primary6X', 'type': '21'},
    '0029': {'name': 'primary6Y', 'type': '21'},
    '002A': {'name': 'primary6Intensity', 'type': '20'},
    '0032': {'name': 'colorPointRX', 'type': '21'},
    '0033': {'name': 'colorPointRY', 'type': '21'},
    '0034': {'name': 'colorPointRIntensity', 'type': '20'},
    '0036': {'name': 'colorPoinrGX', 'type': '21'},
    '0037': {'name': 'colorPointGY', 'type': '21'},
    '0038': {'name': 'colorPoinGIntensity', 'type': '20'},
    '003A': {'name': 'colorPointBX', 'type': '21'},
    '003B': {'name': 'colorPointBY', 'type': '21'},
    '003C': {'name': 'colorPointBIntensity', 'type': '20'},
    '4001': {'name': 'enhancedColorMode', 'type': '19'},
    '400A': {'name': 'colourCapabilities', 'type': '21'},
    '400B': {'name': 'colourTemperatureMiredPhyMin', 'type': '21'},
    '400C': {'name': 'colourTemperatureMiredPhyMax', 'type': '21'},
    '400D': {'name': '*** UNKNOWN NEED TO RAISE ***', 'type': '21'},
    '4010': {'name': '*** UNKNOWN NEED TO RAISE ***', 'type': '21'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

illuminanceMeasurementClusterAttrs={
    '0000':{'name':'measuredValue',           'type':'21'},
    '0001':{'name':'minMeasuredValue',        'type':'21'},
    '0002':{'name':'maxMeasuredValue',        'type':'21'},
    '0003':{'name':'tolerance',               'type':'21'},
    '0004':{'name':'lightSensorType',         'type':'30'},
}

temperatureMeasurementClusterAttrs = {
    '0000': {'name': 'measuredValue', 'type': '29'},
    '0001': {'name': 'minMeasuredValue', 'type': '29'},
    '0002': {'name': 'maxMeasuredValue', 'type': '29'},
    '0003': {'name': 'tolerance', 'type': '21'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

occupancySensorClusterAttrs = {
    '0000': {'name': 'occupancy', 'type': '18'},
    '0001': {'name': 'occupancySensorType', 'type': '30'},
    '0010': {'name': 'PirOccupiedToUnoccupiedDelay', 'type': '21'},
    '0011': {'name': 'PirUnoccupiedToOccupiedDelay', 'type': '21'},
    '0012': {'name': 'PirUnoccupiedToOccupiedThreshold', 'type': '20'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

meteringClusterAttrs = {
    '0000': {'name': 'currentSummationDelivered', 'type': '25'},
    '0001': {'name': 'currentSummationReceived', 'type': '25'},
    '0006': {'name': 'powerFactor', 'type': '28'},
    '0200': {'name': 'status', 'type': '18'},
    '0300': {'name': 'unitOfMeasure', 'type': '30'},
    '0301': {'name': 'multiplier', 'type': '22'},
    '0302': {'name': 'divisor', 'type': '22'},
    '0303': {'name': 'summationFormatting', 'type': '18'},
    '0304': {'name': 'demandFormatting', 'type': '18'},
    '0305': {'name': 'histoticConsumptionFormatting', 'type': '18'},
    '0306': {'name': 'meteringDeviceType', 'type': '18'},
    '0400': {'name': 'instantaneousDemand', 'type': '2A'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

keyEstablishmentAttrs = {
    '0000': {'name': 'keyEstablishmentSuite', 'type': ''},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

diagnosticsClusterAttrs = {
    '011B': {'name': 'AverageMACRetryPerAPSMessageSent', 'type': '21'},
    '011C': {'name': 'lastMessageLQI', 'type': '20'},
    '011D': {'name': 'lastMessageRSSI', 'type': '28'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

bgClusterAttrs = {
    '0000_msp': {'name': 'algorithmModeSelector', 'type': '18'},
    '0001_msp': {'name': 'delayCompensationTime', 'type': '21'},
    '0002_msp': {'name': 'delayCompensatedTemperature', 'type': '29'},
    '0003_msp': {'name': 'propThreshold', 'type': '20'},
    '0004_msp': {'name': 'integral', 'type': '20'},
    '0005_msp': {'name': 'rateEstimate', 'type': '21'},
    '0006_msp': {'name': 'minOffCycles', 'type': '20'},
    '0007_msp': {'name': 'optStartMax', 'type': '20'},
    '0008_msp': {'name': 'minDeltaT', 'type': '20'},
    '0009_msp': {'name': 'advanceOffset', 'type': '20'},
    '0010'    : {'name': 'holidayModeStart', 'type': '23'},
    '000A_msp': {'name': 'advanceFactor', 'type': '20'},
    '0011'    : {'name': 'holidayModeStop', 'type': '23'},
    '0011_msp': {'name': 'systemConfiguration', 'type': '30'},
    '0012'    : {'name': '*** Unknown Attr. ***', 'type': '30'},
    '0013'    : {'name': 'holidayModeSettings', 'type': '25'},
    '0014'    : {'name': 'previousSettings', 'type': '25'},
    '0015'    : {'name': '*** Unknown Attr. ***', 'type': '30'},
    '0020'    : {'name': 'fanCirculateTimerCountdown', 'type': '20'},
    '0021'    : {'name': 'protectionTimer', 'type': '30'},
    '0020_msp': {'name': 'holidayModeEnabled', 'type': '30'},
    '0021_msp': {'name': 'holidayModeActive', 'type': '30'},
    '0022_msp': {'name': 'holidayStartDate', 'type': '42'},
    '0022'    : {'name': 'fanCirculateTimer', 'type': '20'},
    '0023_msp': {'name': 'holidayStartTime', 'type': '21'},
    '0024_msp': {'name': 'holidayEndDate', 'type': '42'},
    '0025_msp': {'name': 'holidayEndTime', 'type': '21'},
    '0026_msp': {'name': 'holidaySetpoint', 'type': '29'},
    '0027_msp': {'name': 'previousHeatMode', 'type': '30'},
    '0028_msp': {'name': 'previousWaterMode', 'type': '30'},
    '0029_msp': {'name': 'previousHeatSetpoint', 'type': '29'},
    '0030_msp': {'name': 'firstScheduleSet', 'type': '30'},
    '0031'    : {'name': 'languageSettings', 'type': '30'},
    '0032'    : {'name': 'humiditySettings', 'type': '30'},
    '0031_msp': {'name': 'frostProtectionSetpoint', 'type': '29'},
    '0032_msp': {'name': 'languageAttribute', 'type': '30'},
    '0033'    : {'name': 'clientFeatureDisplay', 'type': '30'},
    '0034'    : {'name': 'fuelType', 'type': '30'},
    '0035'    : {'name': 'swingTemperature', 'type': '30'},
    '0036'    : {'name': 'wiringConfiguration', 'type': "29"},
    '0037'    : {'name': 'outsideTemperature', 'type': '29'},
    '0040_msp': {'name': 'debug1', 'type': '42'},
    '0041_msp': {'name': 'debug2', 'type': '42'},
    '0042_msp': {'name': 'debug3', 'type': '42'},
    '0043_msp': {'name': 'debug4', 'type': '42'},
    '0044_msp': {'name': 'debug5', 'type': '42'},
    '0100_msp': {'name': 'buttonHold', 'type': '18'},
    '0101_msp': {'name': 'parameterHold', 'type': '18'},
    'FFFD_msp': {'name': 'Ember: Cluster Version', 'type': '21'},

}

netvoxClusterAttrs = {
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'}
}

iasZoneClusterAttrs = {
    '0000': {'name': 'zoneState', 'type': '30'},
    '0001': {'name': 'zoneType', 'type': '31'},
    '0002': {'name': 'zoneStatus', 'type': '19'},
    '0010': {'name': 'iasCieAddress', 'type': 'F0'},
    '0011': {'name': 'zoneId', 'type': '20'},
    '0012': {'name': 'numberOfZoneSensitivityLevelsS', 'type': '20'},
    '0013': {'name': '', 'type': '20'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

amClusterAttrs = {
    '0002': {'name': '*** AM', 'type': '23'},
    '0003': {'name': '*** AM', 'type': '21'},
    '0007': {'name': '*** AM', 'type': '21'},
}

genericTunnelClusterAttrs = {
    '0001': {'name': 'maximumIncomingTrasnferSize', 'type': '21'},
    '0002': {'name': 'maximumOutgoingTransferSize', 'type': '21'},
    '0003': {'name': 'protocolAddress', 'type': '41'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'}
}

smartEnergyTunnellingClusterAttrs = {
    '0000': {'name': 'closeTunnelTimeout', 'type': '21'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'},
}

dummy0021Attrs = {}

fanControlClusterAttrs = {
    '0000': {'name': 'fanMode', 'type': '30'},
    '0001': {'name': 'fanModeSequence', 'type': '30'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'}
}

dehumidificationControlClusterAttrs = {
    '0000': {'name': 'relativeHumidity', 'type': '20'},
    '0001': {'name': 'dehumidificationCooling', 'type': '20'},
    '0010': {'name': 'rhDehumidificationSetpoint', 'type': '20'},
    '0012': {'name': 'dehumidificationLockout', 'type': '30'},
    '0013': {'name': 'dehumidificationHysterisis', 'type': '20'},
    '0014': {'name': 'dehumidificationMaxCool', 'type': '20'},
    '0015': {'name': 'relativeHumidityDisplay', 'type': '30'},
    'FFFD': {'name': 'Ember: Cluster Version', 'type': '21'}
}

relativeHumidityMeasurementAttrs = {

}

clusters = {
    '0000': {'name': 'Basic Cluster', 'clustAttrs': basicClusterAttrs},
    '0001': {'name': 'Power Configuration Cluster', 'clustAttrs': powerConfigurationClusterAttrs},
    '0002': {'name': 'Device Temperature Configuration Cluster',
             'clustAttrs': deviceTemperatureConfigurationClusterAttrs},
    '0003': {'name': 'Identify Cluster', 'clustAttrs': identifyClusterAttrs},
    '0004': {'name': 'Groups Cluster', 'clustAttrs': groupsClusterAttrs},
    '0005': {'name': 'Scenes Cluster', 'clustAttrs': scenesClusterAttrs},
    '0006': {'name': 'On/Off Cluster', 'clustAttrs': onOffClusterAttrs},
    '0008': {'name': 'Level Control Cluster', 'clustAttrs': levelControlClusterAttrs},
    '0009': {'name': 'Alarms Cluster', 'clustAttrs': alarmsClusterAttrs},
    '000A': {'name': 'Time Cluster', 'clustAttrs': timeClusterAttrs},
    '0015': {'name': 'Commissioning Cluster', 'clustAttrs': commissioningClusterAttrs},
    '0019': {'name': 'OTA Cluster', 'clustAttrs': otaClusterAttrs},
    '0020': {'name': 'Poll Control Cluster', 'clustAttrs': pollControlClusterAttrs},
    '0201': {'name': 'Thermostat Cluster', 'clustAttrs': thermostatClusterAttrs},
    '0204': {'name': 'Thermostat UI Cluster', 'clustAttrs': thermostatUiClusterAttrs},
    '0300': {'name': 'Color Control Cluster', 'clustAttrs': colorControlClusterAttrs},
    '0400': {'name': 'Illuminance Cluster', 'clustAttrs': illuminanceClusterAttrs},
    '0402': {'name': 'Temperature Measurement Cluster', 'clustAttrs': temperatureMeasurementClusterAttrs},
    '0406': {'name': 'Occupancy Sensor Cluster', 'clustAttrs': occupancySensorClusterAttrs},
    '0500': {'name': 'IAS Zone Cluster', 'clustAttrs': iasZoneClusterAttrs},
    '0600': {'name': 'Generic Tunnel Cluster', 'clustAttrs': genericTunnelClusterAttrs},
    '0702': {'name': 'Metering Cluster', 'clustAttrs': meteringClusterAttrs},
    '0704': {'name': 'Smart Energy Tunnelling Cluster', 'clustAttrs': smartEnergyTunnellingClusterAttrs},
    '0800': {'name': 'Key Establishment Cluster', 'clustAttrs': keyEstablishmentAttrs},
    '0B05': {'name': 'Diagnostics Cluster', 'clustAttrs': diagnosticsClusterAttrs},
    '1000': {'name': '*** Netvox Light Link Cluster', 'clustAttrs': netvoxClusterAttrs},
    'FC00': {'name': '*** AM Cluster', 'clustAttrs': amClusterAttrs},
    '0021': {'name': '*** Dummy 0021 Cluster', 'clustAttrs': dummy0021Attrs},
    'FD00': {'name': 'BG Cluster', 'clustAttrs': bgClusterAttrs},
    '0202': {'name': 'Fan Control Cluster', 'clustAttrs': fanControlClusterAttrs},
    '0203': {'name': 'Dehumidification Control Cluster', 'clustAttrs': dehumidificationControlClusterAttrs},
    '0405': {'name': 'Relative Humidity Measurement Cluster', 'clustAttrs': relativeHumidityMeasurementAttrs},
    'FD01': {'name': 'BG Cluster SLT4', 'clustAttrs': bgClusterAttrs},
}

BG_Clusters = ('FC00', 'FD00', 'FD01')



def getClusterNameAndId(myCluster):
    """ Accept either id's or names, return clustId,clustName

    """
    clustFound = False

    # First look for a match on IDs
    if myCluster in clusters:
        clustFound = True
        clustId = myCluster
        clustName = clusters[myCluster]['name']
    # Else look for a match on cluster name
    else:
        for clust in clusters:
            if clusters[clust]['name'] == myCluster:
                clustFound = True
                clustId = clust
                clustName = clusters[clust]['name']

    if not clustFound:
        print("Stop. Cluster {} not found in lookup tables".format(myCluster))
        exit()
    return clustId, clustName


def getAttributeNameAndId(cluster, attribute):
    """ Accept either id's or names, return attrId,attrName,attrType

    """

    attrFound = False
    clustId, _ = getClusterNameAndId(cluster)

    if attribute in clusters[clustId]['clustAttrs']:
        attrFound = True
        attrId = attribute
        attrName = clusters[clustId]['clustAttrs'][attribute]['name']
        attrType = clusters[clustId]['clustAttrs'][attribute]['type']
    else:
        for attr in clusters[clustId]['clustAttrs']:
            if clusters[clustId]['clustAttrs'][attr]['name'] == attribute:
                attrFound = True
                attrId = attr
                attrName = clusters[clustId]['clustAttrs'][attr]['name']
                attrType = clusters[clustId]['clustAttrs'][attr]['type']

    if not attrFound:
        print('Cluster={}, Attribute={} was not found in the library'.format(cluster, attribute))
        return attribute, "*** Unknown Attr. ***", None
    return attrId, attrName, attrType


def getDeviceType(myDeviceId):
    """ Lookup the device type using DeviceID (from simple descriptor)

    """
    if myDeviceId[:4] in deviceIDs:
        return deviceIDs[myDeviceId[:4]]
    else:
        return None


def listAllTypes():
    myTypes = []
    for clust in sorted(clusters):
        for attr in sorted(clusters[clust]['clustAttrs']):
            myType = clusters[clust]['clustAttrs'][attr]['type']
            if myType not in myTypes:
                myTypes.append(myType)
    print(sorted(myTypes))


def lookupStatusCode(myStatusCode):
    """
    """
    if myStatusCode in scLookup:
        return scLookup[myStatusCode]
    else:
        return "AT response code not found in zcl Library. Code={}".format(myStatusCode)


# Main Program Starts
if __name__ == "__main__":

    print('Status Codes..\n')
    for c in statusCodes:
        print('{0:45},{1}'.format(c, statusCodes[c]))

    print()
    lookupCode = 'FD'
    print('Lookup "{}"'.format(lookupCode))
    print(lookupStatusCode(lookupCode))
    print()

    print('Listing all clusters and attributes...\r\n')

    for clust in sorted(clusters):
        print(clust, clusters[clust]['name'])

        for attr in sorted(clusters[clust]['clustAttrs']):
            print("{0:>8},{1:2},{2}".format(attr,
                                            clusters[clust]['clustAttrs'][attr]['type'],
                                            clusters[clust]['clustAttrs'][attr]['name']))

        print()

    print('*** Method Tests')
    print()
    myCluster = '0001'
    test = getClusterNameAndId(myCluster)
    print(test, "param={}".format(myCluster))
    myCluster = 'Power Configuration Cluster'
    test = getClusterNameAndId(myCluster)
    print(test, "param={}".format(myCluster))

    print()
    myCluster = '0001'
    myAttribute = '0020'
    test = getAttributeNameAndId(myCluster, myAttribute)
    print(test, "param={},{}".format(myCluster, myAttribute))
    myAttribute = 'BatteryVoltage'
    test = getAttributeNameAndId(myCluster, myAttribute)
    print(test, "param={},{}".format(myCluster, myAttribute))

    # Check that calls fail if incorrect names given
    print()
    try:
        junk = getClusterNameAndId('BLARP')
    except AssertionError:
        print('Cluster not found - trapped by assertion')

    try:
        junk = getAttributeNameAndId('BG Cluster', 'PARP')
    except AssertionError:
        print('Attribute not found - trapped by assertion')

    print("\nAll Done.")

