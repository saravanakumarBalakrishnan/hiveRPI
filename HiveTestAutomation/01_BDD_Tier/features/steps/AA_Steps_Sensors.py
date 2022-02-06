"""
Created on 05 Oct 2017

@author: selvaraj.kuppusamy
"""

from behave import *


@given(u'The {strNodeType} is paired with a Hive Hub and setup for API Validation')
def initialllStep1234(context, strNodeType):
    print(strNodeType)

    context.oSensorClass = context.oThermostatClass
    if strNodeType.upper().find('MOTION') >= 0: context.oSensorEP = context.oSensorClass.motionSensorEP
    if strNodeType.upper().find('CONTACT') >= 0: context.oSensorEP = context.oSensorClass.contactSensorEP
    context.oSensorEP.update()

    if 'PLATFORM' in context.APIType.upper():
        print('Platform Version---: ', context.oSensorEP.platformVersion)
        context.reporter.platformVersion = context.oSensorEP.platformVersion

    strInitialState = context.oSensorEP.CurrentDeviceStateFromHoneyComb
    print('Current State : ' + str(strInitialState))
    strEventLogs = context.oSensorEP.eventLogs
    print(strEventLogs)
    print('\n\n')


@when(u'a User navigates to {strSensorType} screen in the Client')
def navigateToSensorScreen(context, strSensorType):
    context.rFM.navigateToSensorScreen(context.reporter, context.oSensorEP, strSensorType)


@then(u'Automatically validate the state of the {strSensorType}')
def validateSensorStateFromHoneyComb(context, strSensorType):
    context.rFM.validateSensorState(context.reporter, context.oSensorEP, strSensorType)


@then(u'Automatically validate the eventLogs of the {strSensorType}')
def validateSensorEventLogsFromHoneyComb(context, strSensorType):
    context.rFM.validateSensorState(context.reporter, context.oSensorEP, strSensorType)
