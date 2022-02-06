"""
Created on 06 July 2017

@author: Rajeshwar.Srinivasan
"""

import time
from behave import *
import FF_utils as utils


@given(u'Whether DeviceName state is {strStatus} state')
def setDeviceState(context, strStatus):
    strClientType = 'On the client'
    strPropertyType = 'STATUS'
    utils.setEP(context, context.plugEP.type)
    utils.setClient(context, 'Client')
    context.rFM.getClientStatusHiveDevices(context, context.plugEP, strStatus, context.reporter.deviceName)
    time.sleep(30)


@when(u'I say {strUtterance}')
def formatUtterance(context, strUtterance):
    strAlexaName = 'Alexa '
    strUtterance = strUtterance.lstrip('Alexa')

    if '<Active Plug OFF>' in strUtterance:
        Utterance = strUtterance.replace("<Active Plug OFF>", context.reporter.deviceName)
    elif '<Active Plug>' in strUtterance:
        Utterance = strUtterance.replace("<Active Plug>", context.reporter.deviceName)
    else:
        Utterance = strUtterance.replace("<ALL Active Plug>", "all plug")
    print('utterance is' + Utterance)
    context.rFM.callUtterance(context.plugEP, strAlexaName, Utterance)


@then(u'I get a confirmation response from Alexa')
def validateResponse(context):
    utils.setEP(context, context.plugEP.type)
    expectedResponse = utils.getAlexaResponse()
    actualResponse = context.plugEP.alexaResponse
    context.rFM.validatePlugResponse(context.reporter, context.plugEP, expectedResponse, actualResponse)


@then(u'Confirmation response would be an error message')
def validateErrorResponse(context):
    utils.setEP(context, context.plugEP.type)
    expectedResponse = utils.getAlexaErrorResponse()
    actualResponse = context.oThermostatEP.alexaResponse
    print(expectedResponse)
    print(actualResponse)


@then(u'my device changes to {strExpectedStatus} state at the client')
def validateStatus(context, strExpectedStatus):
    context.plugEP = context.oThermostatClass.plugEP
    context.plugEP.update()
    # strClientType = 'mainClient'
    utils.setEP(context, context.plugEP.type)
    utils.setClient(context, 'Client')
    context.rFM.getStatusHiveDevices(context, context.plugEP, strExpectedStatus, context.reporter.deviceName)
    # if strExpectedStatus == 'ON' : strstatus = 99.0
    # else: strstatus = 0.0
    # context.rFM.getLog(context.oPlugEP, 'CLIENT','',strstatus)
