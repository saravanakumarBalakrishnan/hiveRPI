# '''
# Created on 08 Apr 2017
#
# @author: srikrishna.gunasekaran
# '''
#
# from datetime import datetime, timedelta
# import time
#
# from behave import *
#
# import FF_ScheduleUtils as oSchdUtil
# import FF_utils as utils
#
# @given(u'Alexa user is setup with Hive hub and {strDeviceType} for {strSkillName} validation')
# def initSetUp(context,strDeviceType,strSkillName):
#     context.oLightClass = context.oThermostatClass
#     if strDeviceType.upper().find('WARM')>=0:
#         context.oLightEP = context.oLightClass.warmWhiteLightEP
#     elif strDeviceType.upper().find('TUNEABLE') >= 0:
#         context.oLightEP = context.oLightClass.tuneableLightEP
#     else:
#         context.oLightEP = context.oLightClass.colourLightEP
#
#     context.oLightEP.update()
#
# @given(u'{strDeviceType} is renamed to {strDeviceName}')
# def setDeviceName(context,strDeviceType,strDeviceName):
#     '''
#     strClientType = 'On the client'
#     utils.setClient(context, strClientType, True)
#     context.rFM.changeDeviceName(context.reporter, context.oLightEP, context.oLightEP.deviceName,  strDeviceName)
#     '''
#     print()
#
#
# @given(u'{strDeviceName} is in {strStatus} state')
# def setDeviceState(context,strDeviceName,strStatus):
#     strClientType = 'On the client'
#     strPropertyType = 'STATUS'
#     strMode = context.oLightEP.mode
#     context.oLightClass = context.oThermostatClass
#     utils.setClient(context, strClientType, True)
#     context.rFM.setLightSysMode(context.reporter, context.oLightEP, strDeviceName, strMode, strPropertyType,  strStatus)
#     time.sleep(2)
#
#
# @when(u'I say {strUtterance}')
# def formatUtterance(context,strUtterance):
#     strAlexaName = 'Alexa '
#     strUtterance = strUtterance.lstrip('Alexa')
#     context.rFM.callUtterance(context.oLightEP,strAlexaName, strUtterance)
#
#
#
# @then(u'I get a confirmation response from Alexa')
# def validateResponse(context):
#
#     expectedResponse = utils.getAlexaResponse()
#     actualResponse = context.oLightEP.alexaResponse
#     context.rFM.validateResponse(context.reporter,context.oLightEP,expectedResponse,actualResponse)
#
# @then(u'my {strDeviceName} changes to {strExpectedStatus} state')
# def validateStatus(context,strDeviceName,strExpectedStatus):
#     if context.oLightEP.mode.upper().find('AUTO') >= 0:
#         strExpectedMode = 'SCHEDULE'
#     else:
#         strExpectedMode = context.oLightEP.mode.upper()
#     strExpectedStatus = strExpectedStatus.upper()
#
#     context.rFM.validateLight(context.reporter, context.oLightEP, strExpectedMode, strExpectedStatus)
#     context.rFM.validateLightLog(context.reporter, context.oLightEP, 'MAIN CLIENT', strExpectedMode, strExpectedStatus)
#
#
#
#
