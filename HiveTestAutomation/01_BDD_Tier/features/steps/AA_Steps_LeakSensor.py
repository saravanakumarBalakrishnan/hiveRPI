"""
Created on 28 May 2017

@author: anuj kumar
"""

from behave import *
import FF_utils as utils
import AA_troubleshooting as TS


@given(u'A Leak sensor is paired with the user')
def initialStep(context):
    context.leakSensorEP = context.oThermostatClass.leakSensorEP
    context.reporter.platformVersion = context.leakSensorEP.platformVersion
    context.leakSensorEP.client = utils.getAttribute('common', 'mainClient')
    context.leakSensorEP.getLeakSensorNode()


@given(u'A Leak sensor is paired with the user along with alert settings')
def initialStepAndAlert(context):
    context.leakSensorEP = context.oThermostatClass.leakSensorEP
    context.reporter.platformVersion = context.leakSensorEP.platformVersion
    context.leakSensorEP.client = utils.getAttribute('common', 'mainClient')
    context.leakSensorEP.getLeakSensorNode()
    dictStatus = {'PushNotification': 'INACTIVE', 'SendEmail': 'INACTIVE', 'SendSubscriptionSMS': 'INACTIVE'}
    for oRow in context.table:
        dictStatus.update({oRow['Alert Type']: oRow['Alert Status'].upper()})
    dictPayload = {"rules": [{"actions": [{"status": dictStatus['SendEmail'], "type": "SendEmail"},
                                          {"status": dictStatus['SendSubscriptionSMS'], "type": "SendSubscriptionSMS"},
                                          {"status": dictStatus['PushNotification'], "type": "PushNotification"}]}]}
    context.leakSensorEP.setRules(dictPayload)


@when('User checks the current leak status in the App')
def getAppLeakStaus(context):
    context.rFM.update_clientleakStatus(context)


@when('{strNotification} Notification is triggered')
def triggerNotification(context, strNotification):
    context.leakSensorEP.getLeakSensorNode()
    dict = {'High Water Usage': 'Large Flow', 'Low Water Flow': 'Small Leak'}
    if strNotification in dict: context.strNotification = dict[strNotification]
    context.strNotification = context.strNotification.upper()
    context.rFM.leakNotification(context)


@when('Alert Settings are updated as listed below')
def alertSettings(context):
    oAlertDict = {}
    oAlertTypeDict = {'PUSH': 'PushNotification', 'EMAIL': 'SendEmail', 'TEXT': 'SendSubscriptionSMS'}
    oAlertSettingsDict = {'PushNotification': 'INACTIVE',
                          'SendSubscriptionSMS': 'INACTIVE', 'SendEmail': 'INACTIVE'}
    for oRow in context.table:
        strAlertType = oAlertTypeDict[oRow['Alert Type'].upper()]
        strAlertStatus = oRow['Alert Status']
        oAlertDict.update({strAlertType: strAlertStatus})
    for oKeyAPI in oAlertDict:
        oAlertSettingsDict[oKeyAPI] = oAlertDict[oKeyAPI]
    context.oDictTargetAlertSettings = oAlertSettingsDict
    context.rFM.alertSettings(context)


@when('Min Leak duration is set as {strTargetminLeak} mins')
def setMinLeakDuration(context, strTargetminLeak):
    context.TargetminLeakDuration = strTargetminLeak
    context.rFM.minLeak(context)


@Then('Validate if the Min Leak duration is set as expected')
def validate_alertSettings(context):
    context.rFM.validateMinLeakLog(context)


@Then('The leak status should be displayed as expected')
def validateThermostatMode(context):
    context.rFM.update_clientleakStatus(context)
    context.rFM.validateLeakStatus(context)


@Then('Validate if the alert settings are set as expected')
def validate_alertSettings(context):
    context.rFM.validateAlertLog(context)


@Then('The banner appears on the product page')
def validate_banner(context):
    context.rFM.validateBanner(context)


@when('Leak status is set as {status}')
def setStatus(context, status):
    context.strNotification = status
    dict = {'High Water Usage': 'Large Flow', 'Low Water Flow': 'Small Leak'}
    if context.strNotification in dict: context.strNotification = dict[context.strNotification].upper()
    context.strNotification = context.strNotification.upper()
    context.leakSensorEP.trigger_notification(context.strNotification)


@Then('Load troubleshooting screen')
def loadTroubleshootingScreen(context):
    context.rFM.load_trobleshootingScreen(context)


@When('It is an intended usage')
def intendedUsage(context):
    context.rFM.intendedUsage(context)


@When('user inputs to remind me later')
def remindLater(context):
    context.leakSensorEP.remindLater()


@When('User navigates around the app')
def naviagation(context):
    context.leakSensorEP.navigateToFroDashboard()


@Then('the pop is not reappeared')
def popUpDisappear(context):
    context.leakSensorEP.bannerDisappear(context.strNotification)


@when(u'User is fixing the problem')
def TSStepFix(context):
    oTroubleshooting = TS.Troubleshooting()
    oTroubleshooting.loadQuestions(context.strNotification)
    oTroubleshooting.findPaths()
    oTroubleshooting.find_action_path('I CAN FIX')
    context.navigationList = oTroubleshooting.action_path
    context.rFM.troublshooting_navigation(context)
    context.strNotification = 'LEAK_FIXED'


@when(u'User is calling a plumber')
def TSStepPlumber(context):
    oTroubleshooting = TS.Troubleshooting()
    oTroubleshooting.loadQuestions(context.strNotification)
    oTroubleshooting.findPaths()
    oTroubleshooting.find_action_path('CALL PLUMBER')
    context.navigationList = oTroubleshooting.action_path
    context.rFM.troublshooting_navigation(context)
    context.rFM.validate_plumberScreen(context)
    if 'LOW' in context.strNotification or 'SMALL' in context.strNotification:
        context.strNotification = 'USER_OVERRIDE_LOW'
    else:
        context.strNotification = 'USER_OVERRIDE_HIGH'


@when(u'User ignores the leak after troubleshooting')
def TSStepNoCare(context):
    oTroubleshooting = TS.Troubleshooting()
    oTroubleshooting.loadQuestions(context.strNotification)
    oTroubleshooting.findPaths()
    oTroubleshooting.find_action_path('IGNORE')
    context.navigationList = oTroubleshooting.action_path
    context.rFM.troublshooting_navigation(context)
    if 'LOW' in context.strNotification or 'SMALL' in context.strNotification:
        context.strNotification = 'USER_OVERRIDE_LOW'
    else:
        context.strNotification = 'USER_OVERRIDE_HIGH'
