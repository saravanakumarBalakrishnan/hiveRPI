"""
Created on 14 Jul 2016

@author: sri.gunasekaran
"""

from behave import *
import FF_utils as utils


@Given(u'The Hive {strNodeType} is paired with Hive Hub and setup for API Validation')
def initialStep(context, strNodeType):
    print(strNodeType)

    context.oLightClass = context.oThermostatClass
    if strNodeType.upper().find('WHITE') >= 0: context.oLightEP = context.oLightClass.warmWhiteLightEP
    if strNodeType.upper().find('TUNEABLE') >= 0: context.oLightEP = context.oLightClass.tuneableLightEP
    if strNodeType.upper().find('COLOUR') >= 0: context.oLightEP = context.oLightClass.colourLightEP
    context.oLightEP.update()

    if 'PLATFORM' in context.APIType.upper():
        print('Platform Version---: ', context.oLightEP.platformVersion)
        context.reporter.platformVersion = context.oLightEP.platformVersion

    strNodeID = context.oLightEP.currentDeviceNodeId
    print('Node ID: ' + strNodeID)
    strInitialMode = context.oLightEP.mode
    print('Current Mode : ' + strInitialMode)
    strInitialState = context.oLightEP.CurrentDeviceState
    print('Current State : ' + strInitialState)
    if 'ON' in strInitialState:
        context.strInitialBrightness = context.oLightEP.lightBrightness
        print('Current Brightness : ' + str(context.strInitialBrightness))
    if strNodeType.upper().find('TUNEABLE') >= 0:
        print('Current Tone : ' + str(context.oLightEP.floatColourTemperature))
    if strNodeType.upper().find('COLOUR') >= 0:
        print('Current Tone / Colour : ' + str(context.oLightEP.floatColourTemperature))
    print('\n\n')


@When(u'The mode and {propertyName} is automatically changed to {strMode} and {propertyValue}')
def setProperty(context, propertyName, strMode, propertyValue):
    context.oLightClass = context.oThermostatClass
    utils.setClient(context, '', True)
    if not strMode.upper().find('MANUAL') >= 0:
        strMode = 'SCHEDULE OVERRIDE'
    strDeviceName = context.oLightEP.deviceName
    strDeviceID = context.oLightEP.currentDeviceNodeId
    context.rFM.setLightSysMode(context.reporter, context.oLightEP, strDeviceName, strDeviceID, strMode, propertyName,
                                propertyValue)


@Then(u'automatically validate the mode and {propertyName} as {strExpectedMode} and {propertyValue}')
def validateProperty(context, propertyName, strExpectedMode, propertyValue):
    strExpectedMode = strExpectedMode.upper()

    if "BRIGHTNESS" in propertyName.upper():
        propertyValue = propertyValue.replace("%", "")
        strExpectedBrightness = propertyValue
    else:
        strExpectedBrightness = context.oLightEP.lightBrightness

    if "STATUS" in propertyName.upper():
        strExpectedStatus = propertyValue.upper()
    else:
        strExpectedStatus = 'ON'

    if "TONE" in propertyName.upper() or "COLOUR" in propertyName.upper():
        strExpToneColour = propertyValue.upper()
    else:
        strExpToneColour = None

    context.rFM.validateLight(context.reporter, context.oLightEP, strExpectedMode, strExpectedStatus,
                              strExpectedBrightness, strExpToneColour)
