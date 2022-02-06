"""
Created on 16 July 2016

@authors:
iOS        - rajeshwaran
Android    - Sivakumar
Web        - TBD
"""

from behave import *
import FF_utils as utils
import FF_Platform_Utils as pUtils
import FF_alertmeApi as ALAPI

strMainClient = utils.getAttribute('common', 'mainClient')

@when(u'User navigates to the {nameMotionSensor} screen in the Client')
def navToControlScreen(context, nameMotionSensor):

    oSensorEP = context.oThermostatClass.heatEP
    oSensorEP.reporter = context.reporter
    oSensorEP.AndroidDriver = context.AndroidDriver
    oSensorEP.iOSDriver = context.iOSDriver
    context.oThermostatEP = oSensorEP
    utils.setClient(context, strMainClient)

    context.reporter.HTML_TC_BusFlowKeyword_Initialize('User navigates to the motion sensor screen')
    context.oThermostatEP.navigate_ToDeviceScreen(nameMotionSensor)

@when(u'User navigates to the event logs in the Client')
def navigateEventLogs(context):

    context.reporter.HTML_TC_BusFlowKeyword_Initialize('User navigates to the event logs')
    context.oThermostatEP.navigateTo_eventlogs()

@then(u'Validate the motion event logs are displayed')
def verifyEventLogs(context):

    context.reporter.HTML_TC_BusFlowKeyword_Initialize('validate event logs')
    context.oThermostatEP.verifyEventLogs()

@then(u'Validate the current status of the {nameMotionSensor} in API for for {strDeviceType}')
def verifyCurrentStatus(context, nameMotionSensor,strDeviceType):

    context.reporter.HTML_TC_BusFlowKeyword_Initialize('validate current status')
    context.currentStatus = context.oThermostatEP.validateCurrentStatus(nameMotionSensor)

    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    # get node lists
    oDeviceNodeVersionList = pUtils.getNodeAndDeviceVersionID()
    print(oDeviceNodeVersionList, "\n")
    # Extract only node ID for given device type
    oDeviceNodeID = pUtils.getDeviceNodeByName(nameMotionSensor)
    print(oDeviceNodeID, "\n")

    #Get the the final Status of Contact sensor from platform
    finalCSState = pUtils.getMSAttributes(oDeviceNodeID)

    if str(context.currentStatus).upper() == "TRUE":
        currentStatusLog = "In Motion"
    else:
        currentStatusLog = "No Motion"

    if str(finalCSState).upper() == "TRUE":
        finalCSStateLog = "In Motion"
    else:
        finalCSStateLog = "No Motion"

    if str(context.currentStatus).upper() == str(finalCSState).upper():
        strLog = "State on Client$$State on platform@@@"+currentStatusLog+"$$"+finalCSStateLog
        strStatus = "PASS"
    else:
        strLog = "State on Client$$State on platform@@@||" + currentStatusLog + "$$" + finalCSStateLog
        strStatus = "FAIL"
    context.reporter.ReportEvent('Test Validation', strLog, strStatus, "Center")

    print(finalCSState)
    ALAPI.deleteSessionV6(session)

@when(u'User views {intNumberOf} days back in the event logs in the Client')
def verifyGivenDayLog(context, intNumberOf):

    context.reporter.HTML_TC_BusFlowKeyword_Initialize('validate event log based on the given day to go back')
    context.oThermostatEP.navigateToSelectDaysLogs(intNumberOf)

