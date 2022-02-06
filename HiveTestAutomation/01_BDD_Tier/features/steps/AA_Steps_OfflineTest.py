"""
Created on 30 Mar 2016

@author: ranganathan.veluswamy
"""
from datetime import timedelta
import time

from behave import *
import AA_Steps_SmartPlug as SP
import FF_Platform_Utils as pUtils
import FF_utils as utils
import FF_threadedSerial as AT
import FF_zigbeeToolsConfig as config
import FF_device_utils as dutils
import FF_alertmeApi as ALAPI
import requests
import json


@when(
    u'The Hub is rebooted via telegesis and validate the time taken for the devices to come Online and repeated infinitely')
def validateDeviceUptimeInfintely(context):
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    intCntr = 0
    while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hub Power Cycle Counter : ' + str(intCntr))
        oDevicePresenceJson = resetDeviceListPresenceJson(context)

        # ReebootHub
        power_cycle_hub(context)
        time.sleep(60)
        '''ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session  = ALAPI.sessionObject()
        hubID = pUtils.getHubNodeID()
        ALAPI.rebootHubV6(session, hubID)
        ALAPI.deleteSessionV6(session)'''

        intTCStartTime = time.monotonic()
        intLoopCntr = 0
        flag = False
        intAbsentCounter = 0
        flagHubPresence = True
        flagDevicePresence = True
        for oRow in context.table:
            while intLoopCntr < 360:
                deviceType = oRow['DeviceType']
                context.reporter.ReportEvent("Test Validation",
                                             "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                 deviceType).upper() + "</B>", "DONE")
                if not flag:
                    print(pUtils.getDevicePresence(deviceType).upper())
                    if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                        print(pUtils.getDevicePresence(deviceType).upper())
                        intTCEndTime = time.monotonic()
                        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                        strTCDuration = utils.getDuration(strTCDuration)
                        oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                        oDevicePresenceJson[deviceType]["presence"] = True
                    else:
                        flag = True
                        intTCEndTime = time.monotonic()
                        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                        strTCDuration = utils.getDuration(strTCDuration)
                        oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                        oDevicePresenceJson[deviceType]["presence"] = True
                else:
                    intAbsentCounter = intAbsentCounter + 1
                    print("inner" + pUtils.getDevicePresence(deviceType).upper())
                    print("Hub Status " + pUtils.getDevicePresence("NANO2").upper())
                    context.reporter.ReportEvent("Test Validation",
                                                 "Hub Status <B>" + pUtils.getDevicePresence("NANO2").upper() + "</B>",
                                                 "Done")
                    if pUtils.getDevicePresence("NANO2").upper() == "PRESENT":
                        if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                            if flagHubPresence:
                                time.sleep(180)
                                flagHubPresence = False
                            if flagDevicePresence:
                                intLoopCntr = 350
                                flagDevicePresence = False
                        else:
                            flag = True
                            intAbsentCounter = intAbsentCounter + 1
                            if intAbsentCounter > 20:
                                context.reporter.ReportEvent("Test Validation", "Terminated", "DONE")
                                exit()
            time.sleep(10)
            intLoopCntr = intLoopCntr + 1

        for oKey in oDevicePresenceJson.keys():
            context.reporter.ReportEvent("Test Validation", "Device Type : <B>" + oKey + "</B>", "DONE")
            context.reporter.ReportEvent("Test Validation",
                                         "Device Presence : <B>" + str(oDevicePresenceJson[oKey]["presence"]) + "</B>",
                                         "DONE")
            context.reporter.ReportEvent("Test Validation", "Time taken to come Online : <B>" + str(
                oDevicePresenceJson[oKey]["timeTakenToGetOnline"]) + "</B>", "DONE")


def resetDeviceListPresenceJson(context):
    oDevicePresenceJson = {}
    for oRow in context.table:
        deviceType = oRow['DeviceType']
        oDevicePresenceJson[deviceType] = {}
        oDevicePresenceJson[deviceType]["presence"] = False
        oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = ""
    return oDevicePresenceJson


# Power cycle the HUB
def power_cycle_hub(context):
    strPORT = utils.get_Port_Id_TG()
    if not strPORT == "":
        AT.stopThread.clear()
        AT.startSerialThreads("/dev/" + strPORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
        respState, _, resp = utils.discoverNodeIDbyCluster('0006')
        if respState:
            utils.setSPOnOff(myNodeId=resp, strOnOff='OFF', boolZigbee=True)
            context.reporter.ReportEvent("Test Validation", "Hub is turned OFF", "DONE")
            time.sleep(300)
            utils.setSPOnOff(myNodeId=resp, strOnOff='ON', boolZigbee=True)
            context.reporter.ReportEvent("Test Validation", "Hub is turned ON", "DONE")
            time.sleep(10)
        AT.stopThreads()

# Power cycle the HUB
def power_cycle_hub_API(context, hubID):
    """
       """
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    payload = json.dumps({"nodes": [{"attributes": {"powerSupply": {"targetValue": "REBOOT"}}}]})
    url = ALAPI.API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(hubID)

    r = requests.put(url, headers=session.headers, data=payload)

    if r.status_code != 200:
        print("ERROR in getHubLogsV6(): ", r.status_code, r.reason, r.url, r.text)
        exit()
    return r.json()


@when(u'The Hub is rebooted via telegesis and validate the time taken for the devices to come Online')
def validateDeviceUptime(context):
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    intCntr = 0
    intCntr = intCntr + 1
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hub Power Cycle Counter : ' + str(intCntr))
    oDevicePresenceJson = resetDeviceListPresenceJson(context)

    # ReebootHub
    power_cycle_hub(context)
    time.sleep(60)
    '''ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    hubID = pUtils.getHubNodeID()
    ALAPI.rebootHubV6(session, hubID)
    ALAPI.deleteSessionV6(session)'''

    intTCStartTime = time.monotonic()
    intLoopCntr = 0
    flag = False
    intAbsentCounter = 0
    flagHubPresence = True
    flagDevicePresence = True
    for oRow in context.table:
        while intLoopCntr < 360:
            deviceType = oRow['DeviceType']
            context.reporter.ReportEvent("Test Validation",
                                         "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                             deviceType).upper() + "</B>", "DONE")
            if not flag:
                print(pUtils.getDevicePresence(deviceType).upper())
                if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                    print(pUtils.getDevicePresence(deviceType).upper())
                    intTCEndTime = time.monotonic()
                    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                    strTCDuration = utils.getDuration(strTCDuration)
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                    oDevicePresenceJson[deviceType]["presence"] = True
                else:
                    flag = True
                    intTCEndTime = time.monotonic()
                    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                    strTCDuration = utils.getDuration(strTCDuration)
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                    oDevicePresenceJson[deviceType]["presence"] = True
            else:
                intAbsentCounter = intAbsentCounter + 1
                print("inner" + pUtils.getDevicePresence(deviceType).upper())
                print("Hub Status " + pUtils.getDevicePresence("NANO2").upper())
                context.reporter.ReportEvent("Test Validation",
                                             "Hub Status <B>" + pUtils.getDevicePresence("NANO2").upper() + "</B>",
                                             "Done")
                if pUtils.getDevicePresence("NANO2").upper() == "PRESENT":
                    if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                        if flagHubPresence:
                            time.sleep(180)
                            flagHubPresence = False
                        if flagDevicePresence:
                            intLoopCntr = 350
                            flagDevicePresence = False
                    else:
                        flag = True
                        intAbsentCounter = intAbsentCounter + 1
                        if intAbsentCounter > 20:
                            context.reporter.ReportEvent("Test Validation", "Terminated", "DONE")
                            exit()
        time.sleep(10)
        intLoopCntr = intLoopCntr + 1

    for oKey in oDevicePresenceJson.keys():
        context.reporter.ReportEvent("Test Validation", "Device Type : <B>" + oKey + "</B>", "DONE")
        context.reporter.ReportEvent("Test Validation",
                                     "Device Presence : <B>" + str(oDevicePresenceJson[oKey]["presence"]) + "</B>",
                                     "DONE")
        context.reporter.ReportEvent("Test Validation", "Time taken to come Online : <B>" + str(
            oDevicePresenceJson[oKey]["timeTakenToGetOnline"]) + "</B>", "DONE")

@when(u'The {strHubType} Hub is rebooted via API and validate the time taken for the devices to come Online')
def validateDeviceUptime(context, strHubType):
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    intCntr = 0
    intCntr = intCntr + 1
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hub Power Cycle Counter : ' + str(intCntr))
    oDevicePresenceJson = resetDeviceListPresenceJson(context)
    nodeIdList = SP.getNodeAndDeviceVersionID()
    hubID = None
    if strHubType in nodeIdList:
        hubID = nodeIdList[strHubType]["nodeID"]

    # ReebootHub
    power_cycle_hub_API(context, hubID)
    context.reporter.ReportEvent("Test Log","Hub is rebooted via API","Done")
    time.sleep(60)

    intTCStartTime = time.monotonic()
    intLoopCntr = 0
    flag = False
    intAbsentCounter = 0
    flagHubPresence = True
    flagDevicePresence = True
    for oRow in context.table:
        while intLoopCntr < 360:
            deviceType = oRow['DeviceType']
            context.reporter.ReportEvent("Test Validation",
                                         "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                             deviceType).upper() + "</B>", "DONE")
            if not flag:
                print(pUtils.getDevicePresence(deviceType).upper())
                if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                    print(pUtils.getDevicePresence(deviceType).upper())
                    intTCEndTime = time.monotonic()
                    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                    strTCDuration = utils.getDuration(strTCDuration)
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                    oDevicePresenceJson[deviceType]["presence"] = True
                else:
                    flag = True
                    intTCEndTime = time.monotonic()
                    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                    strTCDuration = utils.getDuration(strTCDuration)
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                    oDevicePresenceJson[deviceType]["presence"] = False
                time.sleep(1)
            else:
                intTCStartTime = time.monotonic()
                intAbsentCounter = intAbsentCounter + 1
                print("inner" + pUtils.getDevicePresence(deviceType).upper())
                print("Hub Status " + pUtils.getDevicePresence("NANO2").upper())
                context.reporter.ReportEvent("Test Validation",
                                             "Hub Status <B>" + pUtils.getDevicePresence("NANO2").upper() + "</B>",
                                             "Done")
                if pUtils.getDevicePresence("NANO2").upper() == "PRESENT":
                    if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                        context.reporter.ReportEvent("Test Validation",
                                                     "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                         deviceType).upper() + "</B>", "DONE")
                        intTCEndTime = time.monotonic()
                        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                        strTCDuration = utils.getDuration(strTCDuration)
                        oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                        oDevicePresenceJson[deviceType]["presence"] = True
                        break
                    else:
                        flag = True
                        intAbsentCounter = intAbsentCounter + 1
                        time.sleep(30)
                        if intAbsentCounter > 20:
                            context.reporter.ReportEvent("Test Validation", "Terminated", "DONE")
                            exit()
        time.sleep(10)
        intLoopCntr = intLoopCntr + 1

    for oKey in oDevicePresenceJson.keys():
        context.reporter.ReportEvent("Test Validation", "Device Type : <B>" + oKey + "</B>", "DONE")
        context.reporter.ReportEvent("Test Validation",
                                     "Device Presence : <B>" + str(oDevicePresenceJson[oKey]["presence"]) + "</B>",
                                     "DONE")
        context.reporter.ReportEvent("Test Validation", "Time taken to come Online : <B>" + str(
            oDevicePresenceJson[oKey]["timeTakenToGetOnline"]) + "</B>", "DONE")


@step(u'validate the time taken for the devices presence to go {strPresence}')
def validateDeviceUptime(context, strPresence):
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    intCntr = 0
    intCntr = intCntr + 1
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hub Power Cycle Counter : ' + str(intCntr))
    oDevicePresenceJson = resetDeviceListPresenceJson(context)

    intTCStartTime = time.monotonic()
    intLoopCntr = 0
    flag = False
    for oRow in context.table:
        while intLoopCntr < 360:
            deviceType = oRow['DeviceType']
            context.reporter.ReportEvent("Test Validation",
                                         "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                             deviceType).upper() + "</B>", "DONE")
            if not flag:
                print(pUtils.getDevicePresence(deviceType).upper())
                if str(strPresence).upper() in pUtils.getDevicePresence(deviceType).upper():
                    flag = True
                    intTCEndTime = time.monotonic()
                    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                    strTCDuration = utils.getDuration(strTCDuration)
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                    oDevicePresenceJson[deviceType]["presence"] = True
                    context.reporter.ReportEvent("Test Validation",
                                                 "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                     deviceType).upper() + "</B>", "DONE")
                    break
                else:
                    print(pUtils.getDevicePresence(deviceType).upper())
                    intTCEndTime = time.monotonic()
                    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                    strTCDuration = utils.getDuration(strTCDuration)
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                    oDevicePresenceJson[deviceType]["presence"] = True
        time.sleep(10)

    for oKey in oDevicePresenceJson.keys():
        context.reporter.ReportEvent("Test Validation", "Device Type : <B>" + oKey + "</B>", "DONE")
        context.reporter.ReportEvent("Test Validation",
                                     "Device Presence : <B>" + str(oDevicePresenceJson[oKey]["presence"]) + "</B>",
                                     "DONE")
        context.reporter.ReportEvent("Test Validation", "Time taken to come Online : <B>" + str(
            oDevicePresenceJson[oKey]["timeTakenToGetOnline"]) + "</B>", "DONE")


@when(u'The device is untouched and validate the presence status of the devices infinitely')
def validatePresence(context):
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    oDevicePresenceJson = resetDeviceListPresenceJson(context)
    intTCStartTime = time.monotonic()
    intLoopCntr = 0
    for oRow in context.table:
        deviceType = oRow['DeviceType']
        while True:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verification counter : ' + str(intLoopCntr))
            if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                print(pUtils.getDevicePresence(deviceType).upper())
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                oDevicePresenceJson[deviceType]["presence"] = True
                context.reporter.ReportEvent("Test Validation",
                                             "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                 deviceType).upper() + "</B>", "Pass")
            else:
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                oDevicePresenceJson[deviceType]["presence"] = True
                context.reporter.ReportEvent("Test Validation",
                                             "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                 deviceType).upper() + "</B>", "Fail")
            time.sleep(10)
            intLoopCntr = intLoopCntr + 1


@Then(u'change the state of the plug with mac address {strPlugMac} to {strState} via telegesis')
def zigbeeTurnPlugState(context, strPlugMac, strState):
    reporter = context.reporter
    # dutils.putZigbeeDevicesJson(dutils.getNodes(False))
    try:
        AT.stopThreads()
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
    except:
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
    deviceType = dutils.getModelIdWithMAC(strPlugMac)
    NodeId = dutils.getDeviceNodeWithMAC(deviceType, strPlugMac)
    if str(strState).upper() == "OFF":
        utils.setSPOnOff(myNodeId=NodeId, strOnOff='OFF', boolZigbee=True)
    else:
        utils.setSPOnOff(myNodeId=NodeId, strOnOff='ON', boolZigbee=True)
    reporter.ReportEvent("Test Validation", deviceType + " is turned " + str(strState), "DONE")
    AT.stopThreads()

@Then(u'change the state of the plug with mac address {strBox} to {strState} via telegesis through API')
def zigbeeTurnPlugStateAPI(context, strBox, strState):
    reporter = context.reporter
    # dutils.putZigbeeDevicesJson(dutils.getNodes(False))
    url = 'http://'+config.TOPOLOGY_PLUG_API_URL+'/api/plugState?state='+str(strState)+'&nodeId='+str(config.TOPOLOGY_PLUG_NODE_DICT[str(strBox)])
    print(url)
    resp = requests.get(url)
    print(resp)
    if str(resp.status_code) == "200":
        reporter.ReportEvent("Test Validation", str(strBox) + " is turned " + str(strState), "DONE")
    else:
        reporter.ReportEvent("Test Validation", str(strBox) + " is not turned " + str(strState), "FAIL")


@Then(u'validate the time taken for the devices to show {strState} for {intDuration} minutes')
def validateDevicePresence(context, strState, intDuration):
    reporter = context.reporter
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    oDevicePresenceJson = resetDeviceListPresenceJson(context)
    intTCStartTime = time.monotonic()
    intLoopCntr = 0
    startTime = timedelta(seconds=0)
    intSecond = int(intDuration) * 60
    endTime = timedelta(seconds=intSecond)
    while startTime < endTime:
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verification counter : ' + str(intLoopCntr))
        for oRow in context.table:
            deviceType = oRow['DeviceType']
            deviceName = oRow['DeviceName']
            if "PRESENT" in pUtils.getDevicePresenceByName(deviceType,deviceName).upper():
                print(pUtils.getDevicePresenceByName(deviceType,deviceName).upper())
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                oDevicePresenceJson[deviceType]["presence"] = True
                context.reporter.ReportEvent("Test Validation",
                                             deviceName + " Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                 deviceType).upper() + "</B>", "Pass")
            else:
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                oDevicePresenceJson[deviceType]["presence"] = True
                context.reporter.ReportEvent("Test Validation",
                                             deviceName + " Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                 deviceType).upper() + "</B>", "Fail")
        time.sleep(60)
        startTime = timedelta(seconds=0)
        intLoopCntr = intLoopCntr + 1

@when(u'The Hub is rebooted via telegesis and validate the alarm state of device for {strDuration} minutes')
def validateDeviceAlarmState(context, strDuration):
    intDuration = 60 * int(strDuration)
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    intCntr = 0
    intCntr = intCntr + 1

    oDevicePresenceJson = resetDeviceListPresenceJson(context)
    intTCStartTime = time.monotonic()
    intTCEndTime = time.monotonic()+intDuration
    intLoopCntr = 0
    while True:
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hub Power Cycle Counter : ' + str(intCntr))
        # ReebootHub
        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session  = ALAPI.sessionObject()
        hubID = pUtils.getHubNodeID()
        ALAPI.rebootHubV6(session, hubID)
        ALAPI.deleteSessionV6(session)
        context.reporter.ReportEvent("Test Validation","Hub rebooted", "DONE")


        for oRow in context.table:
            while True:
                ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
                session = ALAPI.sessionObject()
                deviceType = oRow['DeviceType']
                context.reporter.ReportEvent("Test Validation",
                                             "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                 deviceType).upper() + "</B>", "DONE")
                DeviceNodeId = pUtils.getDeviceNodeID(oRow['DeviceType'])
                oEventJSON = ALAPI.getEventsForDevice(session, DeviceNodeId, 10)
                flag = False
                for oEvent in oEventJSON['events']:
                    if "ALARM" in str(oEvent['eventType']).upper():
                        context.reporter.ReportEvent("Test Validation", "ALARM MESSAGE <B>" + str(oEvent['eventType']) + "</B> at "+str(oEvent['time']), "DONE")
                        flag = True


                if not flag:
                    context.reporter.ReportEvent("Test Validation",
                                                 "No ALARM MESSAGE received", "DONE")

                time.sleep(60)

                if time.monotonic() >= intTCEndTime:
                    intTCStartTime = time.monotonic()
                    intTCEndTime = time.monotonic() + intDuration
                    ALAPI.deleteSessionV6(session)
                    break
        intLoopCntr = intLoopCntr + 1


