"""
Created on 06 July 2017

@author: Rajeshwar.Srinivasan
"""

import time

from behave import *

import FF_utils as utils


@given(u'Check {lightname} state is {strStatus} state')
def setDeviceState(context, lightname, strStatus):
    strClientType = 'On the client'
    strPropertyType = 'tone'
    strMode = context.oLightEP.mode
    context.oLightClass = context.oThermostatClass
    utils.setClient(context, strClientType, True)
    if lightname == '<Active Tuneable Light>':
        context.rFM.setLightSysMode(context.reporter, context.oLightEP, 'TUNEABLE LIGHT', strMode, strPropertyType,
                                    strStatus)
    else:
        context.rFM.setLightSysMode(context.reporter, context.oLightEP, 'COLOUR LIGHT', strMode, strPropertyType,
                                    strStatus)
    time.sleep(2)


@When(u'For Lights I say {strUtterance}')
def formatUtterance(context, strUtterance):
    strAlexaName = 'Alexa '
    strUtterance = strUtterance.lstrip('Alexa')
    if '<Active Light>' in strUtterance:
        Utterance = strUtterance.replace("<Active Light>", context.oLightEP.deviceName)
    else:
        Utterance = strUtterance.replace("<The Active Light>", "light")
    print('utterance is' + Utterance)
    context.rFM.callUtterance(context.oLightEP, strAlexaName, Utterance)


@when(u'For Lights brightness I say {strUtterance}')
def formatUtterancebrightness(context, strUtterance):
    strAlexaName = 'Alexa '
    strUtterance = strUtterance.lstrip('Alexa')
    if '<Active Light>' in strUtterance:
        Utterance = strUtterance.replace("<Active Light>", "Warm White Light")
    else:
        Utterance = strUtterance.replace("<The Active Light>", "COLOUR Light")
    print('utterance is' + Utterance)
    context.rFM.callUtterance(context.oLightEP, strAlexaName, Utterance)


@then(u'I get a confirmation response from Alexa on lights')
def validateResponse(context):
    expectedResponse = utils.getAlexaResponse()
    actualResponse = context.oLightEP.alexaResponse
    context.rFM.validateResponse(context.reporter, context.oLightEP, expectedResponse, actualResponse)


@then(u'my light changes to {strExpectedStatus} state at the client')
def validateStatus(context, strExpectedStatus):
    if context.oLightEP.mode.upper().find('AUTO') >= 0:
        strExpectedMode = 'SCHEDULE'
    else:
        strExpectedMode = context.oLightEP.mode.upper()

    strExpectedStatus = strExpectedStatus.upper()

    context.rFM.validateLight(context.reporter, context.oLightEP, strExpectedMode, strExpectedStatus)
    context.rFM.validateLightLog(context.reporter, context.oLightEP, 'MAIN CLIENT', strExpectedMode, strExpectedStatus)


@then(u'my light changes to {strExpectedStatus} brightness at the client')
def brightnessValidate(context, strExpectedStatus):
    if context.oLightEP.mode.upper().find('AUTO') >= 0:
        strExpectedMode = 'SCHEDULE'
    else:
        strExpectedMode = context.oLightEP.mode.upper()

    strExpectedStatus = strExpectedStatus.upper()

    context.rFM.validateLight(context.reporter, context.oLightEP, strExpectedMode, strExpectedStatus)
    context.rFM.validateLightLog(context.reporter, context.oLightEP, 'MAIN CLIENT', strExpectedMode, strExpectedStatus)


@then(u'my light changes to {strExpectedStatus} colour temperature at the client')
def colorTempValidate(context, strExpectedStatus):
    if context.oLightEP.mode.upper().find('AUTO') >= 0:
        strExpectedMode = 'SCHEDULE'
    else:
        strExpectedMode = context.oLightEP.mode.upper()

    strExpectedStatus = strExpectedStatus.upper()

    context.rFM.validateLight(context.reporter, context.oLightEP, strExpectedMode, strExpectedStatus)
    context.rFM.validateLightLog(context.reporter, context.oLightEP, 'MAIN CLIENT', strExpectedMode, strExpectedStatus)


@then(u'my light changes to {strExpectedStatus} color at the client')
def colorValueValidate(context, strExpectedStatus):
    if context.oLightEP.mode.upper().find('AUTO') >= 0:
        strExpectedMode = 'SCHEDULE'
    else:
        strExpectedMode = context.oLightEP.mode.upper()

    strExpectedStatus = strExpectedStatus.upper()

    context.rFM.validateLight(context.reporter, context.oLightEP, strExpectedMode, strExpectedStatus)
    context.rFM.validateLightLog(context.reporter, context.oLightEP, 'MAIN CLIENT', strExpectedMode,
                                 strExpectedStatus)
