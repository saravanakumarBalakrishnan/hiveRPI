from behave import *
import random
import FF_utils as utils
import FF_mimic as mimic
from datetime import datetime, timedelta
import time
import FF_threadedSerial as AT


@given(u'Active lights are paired with Hive')
def initialStep(context):
    context.oMimicEP = context.oThermostatClass.mimicEP
    context.oMimicEP.client = utils.getAttribute('common', 'mainClient')
    context.reporter.platformVersion = context.oMimicEP.platformVersion
    context.oMimicEP.updateMimic()
    context.devicesDict = context.oMimicEP.devicesDict
    context.oMimicLogic = mimic.Mimic(context.reporter)
    context.oMimicLogic.setNodes(context.devicesDict)


@when(u'The mimic is {strSetDuration} for {strNumberOfLight} lights')
def whenStep(context, strSetDuration, strNumberOfLight=None):
    stopMimic(context)
    context.oMimicEP.updateMimic()
    context.devicesDictBefore = context.devicesDict
    totalDevices = len(context.devicesDict.keys())
    if strNumberOfLight.upper() == 'RANDOM' or strNumberOfLight is None:
        intNumberOfLights = (random.sample(range(1, totalDevices), 1))[0]
    elif 'ALL' in strNumberOfLight.upper():
        intNumberOfLights = totalDevices
    else:
        try:
            intNumberOfLights = int(strNumberOfLight)
        except:
            intNumberOfLights = totalDevices
            context.reporter.ReportEvent('Wrong Input', 'Given input ' + strNumberOfLight +
                                         ' in definition for number of lights are wrong', 'FAIL', 'Center')
    if intNumberOfLights > totalDevices:
        print('The given number of devices are not present in the kit ')
        return

    if 'BETWEEN' in strSetDuration.upper():
        strStartTime = strSetDuration.split(' ')[2]
        strEndTime = strSetDuration.split(' ')[4]
    elif 'MINUTES' in strSetDuration.upper():
        # Default duration and setpoints
        lstDuration = strSetDuration.upper().split(' ')
        intMinutes = int(strSetDuration[strSetDuration.index['MINUTES'] - 1])
        dtmFEW = datetime.now() + timedelta(minutes=15)
        strStartTime = dtmFEW.strftime("%H:%M")
        strEndTime = (dtmFEW + timedelta(minutes=intMinutes)).strftime("%H:%M")
    else:
        # Default duration and setpoints
        dtmFEW = datetime.now() + timedelta(minutes=15)
        strStartTime = dtmFEW.strftime("%H:%M")
        strEndTime = (dtmFEW + timedelta(minutes=91)).strftime("%H:%M")

    context.InitialMimicStateForAllLights = 'OFF'
    context.InitialMimicTextForAllLights = 'Bulb turning on soon'

    context.lstTargetTime = [strStartTime, strEndTime]
    context.numberOfLights = intNumberOfLights
    lstRandom = random.sample(range(1, totalDevices + 1), intNumberOfLights)
    intCount = 1
    lights = {}
    light = {}
    for eachItem in context.devicesDict.keys():
        if intCount in lstRandom:
            status = 'true'
        else:
            status = 'false'
        light = {eachItem: status}
        lights.update(light)
        intCount += 1
    context.targetlightsConfig = lights
    context.rFM.setMimic(context)
    time.sleep(60)


@then(u'The mimic behavior is seen for the enabled lights over {strMinutes} minutes')
def thenStep(context, strMinutes):
    print('Then OK')
    context.oMimicLogic.zigbeeThread()
    context.rFM.verifyLightMimicStatus(context)
    context.oMimicLogic.updateMimicDevices(context.targetlightsConfig)
    context.oMimicLogic.fuzzyLogic(context.lstTargetTime)
    context.validationEndTime = datetime.now() + timedelta(minutes=int(strMinutes))
    context.oMimicLogic.validationCycle(context)
    print('After context.oMimicLogic.validationCycle(context)')
    AT.stopThreads()


@then(u'verify mimic is set')
def verifyMimic(context):
    print('Then OK')
    context.rFM.verifyMimic(context)


@then(u'The mimic behavior is seen for the enabled lights')
def verifyLightMimic(context):
    print('Then OK')
    context.rFM.verifyLightMimicStatus(context)


@when(u'Mimic is stopped')
def stopMimic(context):
    if context.oMimicEP.mimicEnabled:
        print('OK')
        context.oMimicEP.stopMimic()


@when(u'Delete Fake Occupancy node')
def delNode(context):
    if context.oMimicEP.FONode:
        print('OK')
        if context.oMimicEP.mimicEnabled:
            context.oMimicEP.stopMimic()
        context.oMimicEP.delMimic()
        context.oMimicEP.updateMimic()


@when(u'A random behavior is set for lights')
def updateBulbs(context):
    totalDevices = len(context.devicesDict.keys())
    intNumberOfLights = random.sample(range(1, totalDevices), 1)
    lstRandom = random.sample(range(1, totalDevices + 1), intNumberOfLights[0])
    intCount = 1
    lights = {}
    lightsMode = {}
    LightMode = ['Manual', 'Schedule']
    for eachItem in context.devicesDict.keys():
        state = 'OFF'
        if intCount in lstRandom: state = 'ON'
        light = {eachItem: state}
        lights.update(light)
        intCount += 1
        mode = random.sample(range(1, 3), 1)[0]
        lightsMode.update({eachItem: LightMode[mode - 1]})
    context.targetlightsMode = lightsMode
    context.targetlightsState = lights
    print(lights)
    print(lightsMode)
    context.rFM.updateLights(context)


@when(u'Mimic starts {strPostion} set points for {strNumberOfLight} lights')
def setMimic(context, strPostion, strNumberOfLight=None):
    context.oMimicEP.updateMimic()
    context.devicesDictBefore = context.devicesDict
    totalDevices = len(context.devicesDict.keys())
    if strNumberOfLight.upper() == 'RANDOM' or strNumberOfLight is None:
        intNumberOfLights = (random.sample(range(1, totalDevices), 1))[0]
    elif 'ALL' in strNumberOfLight.upper():
        intNumberOfLights = totalDevices
    else:
        try:
            intNumberOfLights = int(strNumberOfLight)
        except:
            intNumberOfLights = totalDevices
            context.reporter.ReportEvent('Wrong Input', 'Given input ' + strNumberOfLight +
                                         ' in definition for number of lights are wrong', 'FAIL', 'Center')
    context.numberOfLights = intNumberOfLights
    lstRandom = random.sample(range(1, totalDevices + 1), intNumberOfLights)
    intCount = 1
    lights = {}
    for eachItem in context.devicesDict.keys():
        if intCount in lstRandom:
            status = 'true'
        else:
            status = 'false'
        light = {eachItem: status}
        lights.update(light)
        intCount += 1

    context.targetlightsConfig = lights

    context.InitialMimicStateForAllLights = 'OFF'
    context.InitialMimicTextForAllLights = 'Bulb turning on later'

    if 'BEFORE' in strPostion.upper():
        dtmFEW = datetime.now() + timedelta(minutes=15)
    elif 'MID OF 1ST' in strPostion.upper():
        dtmFEW = datetime.now() - timedelta(minutes=15)
        context.InitialMimicStateForAllLights = 'ON'
        context.InitialMimicTextForAllLights = 'Bulb on'
    elif 'BETWEEN' in strPostion.upper():
        dtmFEW = datetime.now() - timedelta(minutes=50)
        context.InitialMimicStateForAllLights = 'ON'
        context.InitialMimicTextForAllLights = 'Bulb on'
    elif 'MID OF 2ND' in strPostion.upper():
        dtmFEW = datetime.now() - timedelta(minutes=70)
    elif 'JUST AFTER 2ND' in strPostion.upper():
        dtmFEW = datetime.now() - timedelta(minutes=95)
    else:
        dtmFEW = datetime.now() - timedelta(minutes=120)

    if dtmFEW - timedelta(minutes=30) < datetime.now() < dtmFEW:
        context.InitialMimicTextForAllLights = 'Bulb turning on soon'

    strStartTime = dtmFEW.strftime("%H:%M")
    strEndTime = (dtmFEW + timedelta(minutes=100)).strftime("%H:%M")
    context.lstTargetTime = [strStartTime, strEndTime]
    context.rFM.setMimic(context)


@Given('The user is {strSubscriptionStatus} to {strSubscription}')
def setSubscription(context, strSubscriptionStatus, strSubscription):
    context.oMimicEP = context.oThermostatClass.mimicEP
    context.oMimicEP.client = utils.getAttribute('common', 'mainClient')
    context.oMimicEP.reporter = context.reporter
    context.reporter.platformVersion = context.oMimicEP.platformVersion
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Given : The user is ' + strSubscriptionStatus + ' to ' + strSubscription)
    context.oMimicEP.setUserSubcription(strSubscriptionStatus, strSubscription)


@given(u'The device and user language is set to {Language}')
def setDeviceAndUserLanguage(context, Language):
    context.oMimicEP = context.oThermostatClass.mimicEP
    context.oMimicEP.client = utils.getAttribute('common', 'mainClient')
    context.oMimicEP.updateMimic()
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Given : The device and user language is set to ' + Language)
    context.oMimicEP = context.oThermostatClass.mimicEP
    context.oMimicEP.setUserLocaleAndLanguage(Language)


@when(u'I am on the screen {Screen_Name}')
def GotoScreen(context, Screen_Name):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Given : I am on the screen ' + Screen_Name)
    context.oMimicEP = context.oThermostatClass.mimicEP
    context.oMimicEP.gotoMimicFlowScreen(Screen_Name)


@then(u'The text is correct in {Language}')
def GotoScreen(context, Language):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Given : The text is correct')
    context.oMimicEP = context.oThermostatClass.mimicEP
    context.oMimicEP.verifyLocalisedCopyText(Language)
