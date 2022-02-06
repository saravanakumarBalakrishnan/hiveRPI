"""
Created on 11 August 2016

@authors:
iOS        - rajeshwaran
Android    - TBD
Web        - TBD
"""

from behave import *
import FF_utils as utils

strMainClient = utils.getAttribute('common', 'mainClient')


# Checks whether the device is paired with hub and then navigates to respective Device Control Page in App
@given(u'The {strdeviceName} is paired with the hub')
def navigateDevice(context, strdeviceName):
    if "MOTION SENSOR" in str(strdeviceName).upper():

        oSensorEP = context.oThermostatClass.heatEP
        oSensorEP.reporter = context.reporter
        oSensorEP.AndroidDriver = context.AndroidDriver
        oSensorEP.iOSDriver = context.iOSDriver
        context.oThermostatEP = oSensorEP

        utils.setClient(context, strMainClient)
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strdeviceName + ' is paired with the hub')
        context.oThermostatEP.validateDeviceWithHub(strdeviceName)

    elif "LIGHT" in str(strdeviceName).upper():
        oSensorEP = context.oThermostatClass.heatEP
        oSensorEP.reporter = context.reporter
        if strMainClient == 'iOS App':
            oSensorEP.iOSDriver = context.iOSDriver
        elif 'ANDROID' in strMainClient.upper():
            oSensorEP.AndroidDriver = context.AndroidDriver
        elif strMainClient == 'Web App':
            oSensorEP.WebDriver = context.WebDriver
        else:
            context.reporter.ReportEvent("Test Validation", "Problem in getting Main client", "FAIL")
        context.reporter.ActionStatus = True
        context.oThermostatEP = oSensorEP
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('The ' + strdeviceName + ' is paired with the hub')
        utils.setClient(context, strMainClient)
        context.oThermostatEP.navigateToActiveLight(strdeviceName)

    else:
        oSensorEP = context.oThermostatClass.heatEP
        oSensorEP.reporter = context.reporter
        if strMainClient == 'iOS App':
            oSensorEP.iOSDriver = context.iOSDriver
        elif 'ANDROID' in strMainClient.upper():
            oSensorEP.AndroidDriver = context.AndroidDriver
        elif strMainClient == 'Web App':
            oSensorEP.WebDriver = context.WebDriver
        else:
            context.reporter.ReportEvent("Test Validation", "Problem in getting Main client", "FAIL")
        context.reporter.ActionStatus = True
        context.oThermostatEP = oSensorEP
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('The ' + strdeviceName + ' is paired with the hub')
        utils.setClient(context, strMainClient)
        context.oThermostatEP.checkDeviceWithHub(strdeviceName)


# Sets the required setting (brightness, tone or colour ) as needed on the Bulb UI
@when(u'User sets the {strSettings} as {strValue} on the App')
def setValueForBulb(context, strSettings, strValue):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'User sets the ' + strSettings + ' as ' + strValue + ' on the App')
    utils.setClient(context, strMainClient)
    context.oThermostatEP.setLocalValues(strSettings, strValue)
    context.oThermostatEP.navigateToDesiredSettings(strSettings)
    context.oThermostatEP.setValueForBulbBySwiping(strSettings, strValue)


# Validates the Bulb setting and value in API (backend)
@then(u'the {strSettings} should be set as expected')
def verifyAPISettings(context, strSettings):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('the ' + strSettings + ' should be set as expected')
    context.oThermostatEP.verifyValueInAPI()
    context.oThermostatEP.setLocalValues("", "")


# Validates the device modes (Manual to Schedule and vice versa)
@then(u'The {strDeviceName} mode is changed and validated from Manual to Schedule and vice versa')
def verifyDeviceModeSettings(context, strDeviceName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Validating the device modes on the App')
    context.oThermostatEP.verifyDeviceModeSettings(strDeviceName)
