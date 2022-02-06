"""
Created on 24 April 2017

@author: anuj kumar
"""
# from behave import *
from datetime import datetime, timedelta
import time

# from behave import *
from behave import *
import FF_ScheduleUtils as oSchdUtil
import FF_utils as utils


@given(u'{strStatName} is paired with NA Hive')
def initialStep(context, strStatName):
    context.oNaThermostatEP = context.oThermostatClass.naThermostatEP
    context.oNaThermostatEP.strThermostatName = strStatName
    context.oNaThermostatEP.getStatType(strStatName)
    if not context.reporter.ActionStatus:
        context.reporter.ReportEvent('Test Validation', 'Thermostat is not available', "FAIL", 'Center', True)
        return
    context.timezone = context.oNaThermostatEP.getTimeZone()
    context.oNaThermostatEP.updateV6point5()
    print(context.oNaThermostatEP.type)
    context.reporter.platformVersion = context.oNaThermostatEP.platformVersion
    print(context.oNaThermostatEP.getSchedule())
    context.oNaThermostatEP.client = utils.getAttribute('common', 'mainClient')
    time.sleep(5)
    context.oNaThermostatEP.thermostat_selection(context.oNaThermostatEP.strThermostatName)


@when('Operating mode is changed to {strOperatingMode} when stat is {strThermostat}')
def setThermostatMode(context, strOperatingMode, strThermostat):
    strOperatingModeSplitted = strOperatingMode.split(' ')
    context.operatingMode = strOperatingMode
    strThermostat = strThermostat.upper()
    context.strTargetedTemp = ''
    if 'TEMPERATURE' in strOperatingMode.upper() and 'SCHEDULE' not in strOperatingMode.upper():
        if 'BETWEEN' in strOperatingMode.upper():
            context.strExpectedTemp = strOperatingModeSplitted[len(strOperatingModeSplitted) - 3] + \
                                      '--' + strOperatingModeSplitted[len(strOperatingModeSplitted) - 1]
            strOperatingMode = strOperatingModeSplitted[0]
            context.strTargetedTemp = context.strExpectedTemp
        else:
            context.strExpectedTemp = strOperatingModeSplitted[len(strOperatingModeSplitted) - 1]
            strOperatingMode = strOperatingModeSplitted[0]
            context.strTargetedTemp = context.strExpectedTemp
    elif 'SCHEDULE' in strOperatingMode.upper():

        oScheduleDict = context.oNaThermostatEP._weeklySchedule
        context.strExpectedTemp, intLeftDuration = oSchdUtil.getCurrentTempFromTimeZoneSchedule(context.timezone,
                                                                                                oScheduleDict)
    else:
        context.strExpectedTemp = context.oNaThermostatEP.occupiedHeatingSetpoint
    context.strOperatingMode = strOperatingMode.upper()
    context.strThermostatTargetedChannel = strThermostat
    context.rFM.setThemostatModeAndTemp(context)


@Then('Validate current mode as {strOperatingMode}')
def validateThermostatMode(context, strOperatingMode):
    context.rFM.validateThemostatMode(context)


@when('The below schedule is set for {strDay} when stat is {strThermostat}')
def setThermostatSchedule(context, strDay, strThermostat):
    strThermostat = strThermostat.upper()
    context.WeeklyScheduleBefore = context.oNaThermostatEP._weeklySchedule
    context.strOperatingMode = 'SCHEDULE'
    context.strThermostatTargetedChannel = strThermostat

    if strDay.upper() == "TOMMOROW":
        strDay = (datetime.today() + timedelta(days=1)).strftime("%a").lower()
    elif strDay.upper() in oSchdUtil.oWeekDayDict:
        strDay = oSchdUtil.oWeekDayDict[strDay.upper()]
    else:
        strDay = datetime.today().strftime("%a").lower()
    print(strDay)
    oSchedDict = {}
    oSchedDict.clear()
    if 'Start Time' in context.table.headings:
        oSheduleList = oSchdUtil.createSceduleFormatFromTable(context)
        if not oSheduleList: return False
        oSchedDict = {strDay: oSheduleList}
    else:
        oSheduleList = oSchdUtil.createSceduleFormatFromTableWithoutStartTime(context)
        if not oSheduleList: return False
        oSchedDict = {strDay: oSheduleList}
    context.oSchedDict = oSchedDict

    context.rFM.setThermostatSchedule(context)


@Then('Validate {feature} Setting should be {featureSettingMode}')
def verifyFeatureSettingsAndMode(context, feature, featureSettingMode):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate {feature} is {featureSettingMode}')
    # getting operating mode from setThermostatMode method via context
    operatingMode = context.operatingMode
    context.oNaThermostatEP.checkFeatureSettingsAndMode(context, feature, featureSettingMode, operatingMode)


@When('user sets Humidity value to {HumidityValue}')
def setHumidityValue(context, HumidityValue):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set Humidity Value {HumidityValue}')
    # set the humidity value
    context.oNaThermostatEP.setUserHumidityValue(context, HumidityValue)


@Then('Validate humidity value sets to {HumidityValue}')
def checkHumidityValue(context, HumidityValue):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate Humidity Value {HumidityValue}')
    # validate the humidity value
    context.oNaThermostatEP.validateHumidityValue(context, HumidityValue)


@When('user select {option} in Fan Setting')
def selectFanSetting(context, option):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Select Fan setting {option}')
    # select Fan Setting
    context.oNaThermostatEP.userSelectFanSetting(context, option)


@Then('Validate {fanOption} should be enabled in Fan Setting')
def checkFanOptionSelected(context, fanOption):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate Fan Setting option as {fanOption}')
    # validate the Fan Setting
    context.oNaThermostatEP.validateFanSetting(context, fanOption)


@Then('it should display with 15mins, 30mins and 45mins')
def checkFanCirculateOptions(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Validate Fan Setting Circulate option displays as 15, 30 and 45mins')
    # validate the Fan Circulate options displays 15, 30 and 45 mins
    context.oNaThermostatEP.validateFanCirculateOptions(context)


@Then('Verify if the {selectedMins} circulate is set')
def checkFanCirculateOptionsSelected(context, selectedMins):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verify if the selected circulate is set')
    # validate the Fan Circulate options selected 15, 30 and 45 mins
    context.oNaThermostatEP.validateFanCirculateOptionsSelected(context, selectedMins)
