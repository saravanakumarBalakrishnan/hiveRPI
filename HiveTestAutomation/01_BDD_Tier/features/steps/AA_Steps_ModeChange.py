"""
Created on 22 May 2015

@author: ranganathan.veluswamy
"""
# from behave import *
from datetime import datetime, timedelta
import time

# from behave import *
from behave import *
import FF_ScheduleUtils as oSchdUtil
import FF_utils as utils
import FF_threadedSerial as AT
import FF_zigbeeToolsConfig as config
import CC_thermostatModule as st


# import DD_Page_WebApp as oPageWeb

@given(u'The Hive product is paired and setup for Routing Topology')
def inittialStepTopology(context):
    print("Getting started")
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Initial Setup before test')


@given(u'The Hive product is paired and setup for {strNodeType}')
def inittialStep(context, strNodeType):
    print("Getting started")
    if 'ZIGBEE' in context.APIType.upper():
        if "HEATING" in str(strNodeType).upper() or "WATER" in str(strNodeType).upper():
            AT.startAttributeListener(printStatus=False)
            context.nodes = utils.getNodes()
            print(context.nodes, 'context.nodes')
            reporter = context.reporter
            reporter.strNodeID = context.nodes['BM']
            config.node1 = context.nodes['BM']
            AT.getInitialData(reporter.strNodeID, fastPoll=False, printStatus=False)
            # Instantiate ThermostatEndpoint class
            oThermostatClass = st.thermostatClass(context.reporter.strNodeID)
            context.oThermostatClass = oThermostatClass
    # Set the Type Heat or Water
    if strNodeType.upper().find('WATER') >= 0:
        context.oThermostatEP = context.oThermostatClass.waterEP
    elif strNodeType.upper().find('PLUG') >= 0:
        context.oThermostatEP = context.oThermostatClass.plugEP
    elif strNodeType.upper().find('HOLIDAY') >= 0:
        context.oThermostatEP = context.oThermostatClass.holidayEP
    else:
        context.oThermostatEP = context.oThermostatClass.heatEP
    context.oThermostatEP.update()
    print(context.oThermostatEP.type)
    strClientType = 'mainClient'

    # initialize Appium & Selenium Drivers
    if 'PLATFORM' in context.APIType.upper():
        # context.oThermostatEP.reporter = context.reporter
        print('Platform Version---: ', context.oThermostatEP.platformVersion)
        context.reporter.platformVersion = context.oThermostatEP.platformVersion
        # context.rFM.intializeDrivers(context)
        '''context.oThermostatEP.iOSDriver = context.iOSDriver
        context.oThermostatEP.AndroidDriver = context.AndroidDriver
        context.oThermostatEP.WebDriver = context.WebDriver'''

    if not (strNodeType.upper().find('NOTIFICATION') >= 0 and "upgrades" not in strNodeType):
        if not (strNodeType.upper().find('HOLIDAY') >= 0):
            print(context.oThermostatEP.getSchedule())
    elif "upgrades" not in strNodeType:
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Initial Setup before test')
    else:
        context.oThermostatEP.getHeatRule()
        utils.setClient(context, strClientType)
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Initial Setup before test')
        context.oThermostatEP.navigate_to_settingScreen('NOTIFICATION')

        '''
        oNavigator = oPageWeb.BasePage(context.WebDriver,context.reporter)

        oNavigator.navigate_to_page('NOTIFICATION')
        '''

    # Get Current Temperature and Mode
    if not (strNodeType.upper().find('NOTIFICATION') >= 0) and "upgrades" not in strNodeType and strNodeType.upper().find('PLUG') < 0:
        strInitialMode = context.oThermostatEP.mode
        strInitialTemperature = 1.0
        if (context.oThermostatEP.type == 'HEAT') or (context.oThermostatEP.type == 'HOLIDAY'):
            strInitialTemperature = context.rFM.convertHexTemp(context.oThermostatEP.occupiedHeatingSetpoint, False)
        # Logs the initial setup before the start of the test
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Initial Setup before test')
        strLog = context.rFM.getLog(context.oThermostatEP, 'Test', strInitialMode, strInitialTemperature)
        context.reporter.ReportEvent('Test Validation', strLog[0], "Done")

        if not (strNodeType.upper().find('HOLIDAY') >= 0):
            print(oSchdUtil.getCurrentTempFromSchedule(context.oThermostatEP.getSchedule()))
    else:
        if "upgrades" not in strNodeType:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Initial Setup before test')
    time.sleep(5)


@when(
    'Mode is {strExecType} changed to {strMode} with Target Temperature as {fltSetTemperature:.1f} for a duration of {intSetTempDuration:d} {strClientType}')
def setSysModeWithTTemp(context, strExecType, strMode, fltSetTemperature, intSetTempDuration, strClientType):
    if 'HOLIDAY' in strMode:
        utils.setEP(context, 'HEATING')
    else:
        utils.setEP(context, strMode)

    utils.setClient(context, strClientType)

    if strMode.split()[0].upper() == 'ALWAYS':
        strMode = strMode.split()[0] + ' ' + strMode.split()[1]
    else:
        strMode = strMode.split()[0]
    print(strMode)

    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True

    if 'HOLIDAY' in strMode.upper():
        holidayStartOffset = 60  # Start offset from now in seconds.
        strHoldayStart = (datetime.now() + timedelta(seconds=holidayStartOffset)).replace(second=0, microsecond=0)
        strHoldayEnd = (strHoldayStart + timedelta(seconds=intSetTempDuration))

        strUTCHoldayStart = (datetime.now() + timedelta(seconds=holidayStartOffset)).replace(second=0, microsecond=0)
        strUTCHoldayEnd = (strHoldayStart + timedelta(seconds=intSetTempDuration))
        context.strHoldayStart = strUTCHoldayStart
        context.strHoldayEnd = strUTCHoldayEnd
        time.sleep(60 - int(datetime.today().strftime("%S")))
        context.rFM.setHoldayMode(context.reporter, boolAutoMode, context.oThermostatEP, strMode, fltSetTemperature,
                                  intSetTempDuration, strHoldayStart, strHoldayEnd)
    else:
        context.rFM.setSysMode(context.reporter, boolAutoMode, context.oThermostatEP, strMode, fltSetTemperature,
                               intSetTempDuration)


@when('Mode is {strExecType} changed to {strMode} for a duration of {intSetTempDuration:d} hour{strClientType}')
def setSysModeForDuration(context, strExecType, strMode, intSetTempDuration, strClientType):
    utils.setEP(context, strMode)
    utils.setClient(context, strClientType)

    if strMode.split()[0].upper() == 'ALWAYS':
        strMode = strMode.split()[0] + ' ' + strMode.split()[1]
    else:
        strMode = strMode.split()[0]
    print(strMode)

    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True
    context.rFM.setSysMode(context.reporter, boolAutoMode, context.oThermostatEP, strMode, None, intSetTempDuration)


@when('Mode is {strExecType} changed to {strMode}')
def setSysMode(context, strMode, strExecType):
    utils.setEP(context, context.oThermostatEP.type)
    utils.setClient(context, strMode)

    if strMode.split()[0].upper() == 'ALWAYS':
        strMode = strMode.split()[0] + ' ' + strMode.split()[1]
    else:
        strMode = strMode.split()[0]
    print(strMode)
    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True

    context.rFM.setSysMode(context.reporter, boolAutoMode, context.oThermostatEP, strMode)


# @when('Target Temperature is {strExecType} set to {strSetTemperature:.1f}{strClientType}')
@when('Target Temperature is {strExecType} set to {strSetTemperature}')
def setTargetTemperature(context, strExecType, strSetTemperature):  # , strClientType):
    strClientType = strSetTemperature
    utils.setEP(context, strClientType)
    utils.setClient(context, strClientType)

    strSetTemperature = float(strSetTemperature.split()[0])
    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True
    context.rFM.setTargetTemperature(context.reporter, boolAutoMode, context.oThermostatEP, strSetTemperature)


# Function added for Change plug state (similar to setSysMode above)
@when('State is {strExecType} changed to {strExpectedState} while in {strExpectedMode}')
def setSysState(context, strExecType, strExpectedState, strExpectedMode):
    utils.setEP(context, strExpectedState)
    utils.setClient(context, strExpectedState)

    if strExpectedMode.upper().find('MANUAL') >= 0:
        strExpectedMode = 'MANUAL'
    else:
        strExpectedMode = 'AUTO'
    if strExpectedState.split()[0].upper() == 'ON':
        strExpectedState = 'ON'
    else:
        strExpectedState = 'OFF'
    print("Plug state to be set in the client is : %s " % strExpectedState)
    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True
    context.rFM.setSysState(context.reporter, boolAutoMode, context.oThermostatEP, strExpectedState, strExpectedMode)


@then(
    '{strExecType} validate current mode as {strExpectedMode} with Target Temperature as {strExpectedTemperature:.1f}')
def validateSysmode(context, strExecType, strExpectedMode, strExpectedTemperature):
    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True
    if context.APIType == 'PLATFORM': boolAutoMode = False
    if 'PLATFORM' in context.APIType.upper() and 7.0 == strExpectedTemperature: strExpectedTemperature = 1.0
    if strExpectedMode == 'MANUAL' and context.APIType == 'PLATFORM' and strExpectedTemperature == 20.0:
        if context.oThermostatEP.Web_ManualModeTargTemp is not None: strExpectedTemperature = context.oThermostatEP.Web_ManualModeTargTemp

    strHoldayStart = ""
    strHoldayEnd = ""
    if 'HOLIDAY' in strExpectedMode:
        strHoldayStart = context.strHoldayStart
        strHoldayEnd = context.strHoldayEnd
    context.rFM.validateSysmode(context.reporter, boolAutoMode, context.oThermostatEP, strExpectedMode,
                                strExpectedTemperature, context.intCheckDuration, context.intCheckIntervalTime,
                                strHoldayStart, strHoldayEnd)


@then('{strExecType} validate current mode as AUTO with Current Target Temperature')
def validateAutoMode(context, strExecType):
    fltTemp, intCurrentEvenDuration = oSchdUtil.getCurrentTempFromSchedule(context.oThermostatEP.getSchedule())
    if intCurrentEvenDuration <= int(context.intCheckDuration / 60):
        time.sleep(intCurrentEvenDuration * 60 + 60)
        fltTemp, intCurrentEvenDuration = oSchdUtil.getCurrentTempFromSchedule(context.oThermostatEP.getSchedule())
    strExpectedTemperature = fltTemp
    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True
    if context.APIType == 'PLATFORM': boolAutoMode = False
    context.rFM.validateSysmode(context.reporter, boolAutoMode, context.oThermostatEP, 'AUTO', strExpectedTemperature,
                                context.intCheckDuration, context.intCheckIntervalTime)


# @then('{strExecType} validate current mode as {strExpectedMode} for duration of {intCheckDuration:d} seconds in interval of {intCheckIntervalTime:d} seconds')
@then('{strExecType} validate current mode as {strExpectedMode}')
def validateSysmodeWithoutTargTemp(context, strExecType, strExpectedMode):
    print(strExpectedMode)
    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True
    if context.APIType == 'PLATFORM': boolAutoMode = False
    context.rFM.validateSysmodeWithoutTargTemp(context.reporter, boolAutoMode, context.oThermostatEP, strExpectedMode,
                                               context.intCheckDuration, context.intCheckIntervalTime)


@then('{strExecType} validate current state as {strExpectedState} while in {strExpectedMode}')
def validateSysStateWithoutTargTemp(context, strExecType, strExpectedState, strExpectedMode):
    if strExpectedState.upper().find('OFF') >= 0 or strExpectedState.upper().find('ON') >= 0:
        print(strExpectedState)
    else:
        fltTemp, intCurrentEvenDuration = oSchdUtil.getCurrentTempFromSchedule(context.oThermostatEP.getSchedule())
        strExpectedState = fltTemp
        print('Current Schedule event is : ', strExpectedState)
    if strExpectedMode.upper().find('MANUAL') >= 0:
        strExpectedMode = 'MANUAL'
    else:
        strExpectedMode = 'AUTO'
    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True
    if context.APIType == 'PLATFORM': boolAutoMode = False
    context.rFM.validateSysState(context.reporter, boolAutoMode, context.oThermostatEP, strExpectedState,
                                 strExpectedMode, context.intCheckDuration, context.intCheckIntervalTime)
    # if strExpectedMode.upper().find('MANUAL') >= 0:
    #     strExpectedMode = 'MANUAL'
    # else:
    #     strExpectedMode = 'AUTO'
    # if strExecType.upper().find('MANUAL') >= 0:
    #     boolAutoMode = False
    # else:
    #     boolAutoMode = True
    # if context.APIType == 'PLATFORM': boolAutoMode = False
    # context.rFM.validateSysState(context.reporter, boolAutoMode, context.oThermostatEP, strExpectedState,
    #                              strExpectedMode, context.intCheckDuration, context.intCheckIntervalTime)
