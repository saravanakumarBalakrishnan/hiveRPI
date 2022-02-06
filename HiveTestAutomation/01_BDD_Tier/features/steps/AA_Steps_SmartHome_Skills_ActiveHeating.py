"""
Created on 22 August 2017

@author: rajeshwari.srinivasan
"""
from behave import *
import FF_utils as utils


@Given(u'Mode is {strExecType} changed to {strMode}')
def setSysMode(context, strExecType, strMode):
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


@when(u'For Heating I say {strUtterance}')
def formatUtterance(context, strUtterance):
    strAlexaName = 'Alexa '
    strUtterance = strUtterance.lstrip('Alexa')
    Utterance = strUtterance.replace("<Active Heating>", context.reporter.deviceName)
    print('utterance is' + Utterance)
    context.rFM.callUtterance(context.oThermostatEP, strAlexaName, Utterance)


@then(u'I get a confirmation response from Alexa on heating')
def validateResponse(context):
    expectedResponse = utils.getAlexaResponse()
    actualResponse = context.oThermostatEP.alexaResponse
    context.rFM.validateHeatingResponse(context.reporter, context.oThermostatEP, expectedResponse, actualResponse)


@then(u'I get a error response from Alexa on heating')
def validateerrResponse(context):
    expectedResponse = utils.getAlexaErrorResponse()
    actualResponse = context.oThermostatEP.alexaResponse
    context.rFM.validateHeatingResponse(context.reporter, context.oThermostatEP, expectedResponse, actualResponse)


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


@then(u'validate mode as {strExecType} with Target Temperature as {strExecTemp}')
def validateManualMode(context, strExecType, strExecTemp):
    strExpectedTemperature = strExecTemp
    if strExecType.upper().find('MANUAL') >= 0:
        boolAutoMode = False
    else:
        boolAutoMode = True
    if context.APIType == 'PLATFORM': boolAutoMode = False
    context.rFM.validateSysmode(context.reporter, boolAutoMode, context.oThermostatEP, 'MANUAL',
                                strExpectedTemperature, context.intCheckDuration, context.intCheckIntervalTime)
