"""
Created on 19 Jan 2016

@author: ranganathan.veluswamy
@author: Shubanker
"""

import time

from behave import *

import FF_ScheduleUtils as SchUtils
import FF_alertmeApi as ALAPI
import FF_utils as utils
import FF_Platform_Utils as pUtils
import FF_device_utils as dutils
import CC_platformAPI as platAPI

strMainClient = utils.getAttribute('common', 'mainClient')


@given(u'The {} are paired with the Hive Hub')
def setUpSmartPlugs(context, device):
    # get device versions
    oDeviceVersionList = pUtils.getNodeAndDeviceVersionID()
    print(device)
    print(oDeviceVersionList, "\n")


@when(u'The schedule for the below smart plugs are set and continuously validated via Hub')
def setSPSchedulesAndValidateViaHub(context):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    # get node lists
    oDeviceNodeVersionList = getNodeAndDeviceVersionID()

    oDeviceDetails = {}
    intCntr = 1
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Continuous Schedule Test Week: ' + str(intCntr))
    for oRow in context.table:
        SmartPlug = oRow['SmartPlug']
        intNoOfEvents = int(oRow['NoOfEvents'])

        oDeviceDetails[SmartPlug] = {}
        oDeviceDetails[SmartPlug]["id"] = SmartPlug
        oDeviceDetails[SmartPlug]["noOfEvents"] = intNoOfEvents
        oDeviceDetails[SmartPlug]["nodeId"] = oDeviceNodeVersionList[SmartPlug]["nodeID"]
        oDeviceDetails[SmartPlug]["syntheticID"] = getSyntheticDeviceID(oDeviceNodeVersionList[SmartPlug]["nodeID"])
        print('oDeviceNodeVersionList[SmartPlug]["nodeID"]', oDeviceNodeVersionList[SmartPlug]["nodeID"])
        print("syntheticID", oDeviceDetails[SmartPlug]["syntheticID"])

        payload, oSPSchedDict = SchUtils.createScheduleForSP(intNoOfEvents)
        print(oSPSchedDict, "\n")
        context.oSPSchedDict = oSPSchedDict
        context.SPNodeID = oDeviceDetails[SmartPlug]["nodeId"]
        r, success = ALAPI.setScheduleSP(session, oDeviceDetails[SmartPlug]["syntheticID"], payload)
        print(r, success)
    ALAPI.deleteSessionV6(session)

    SchUtils.runSPValidationForWeekSchedule(context)

    '''while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Continuous Schedule Test Week: ' + str(intCntr))   
        for oRow in context.table:
            SmartPlug = oRow['SmartPlug']
            intNoOfEvents = int(oRow['NoOfEvents'])
            
            payload, oScheduleDict = SchUtils.createScheduleForSP(intNoOfEvents)
            
            # ALAPI.setScheduleSP(session, nodeId, payload)'''


# Get the Node ID for the given device type
def getNodeAndDeviceVersionID():
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    oDeviceDetails = {}
    for oNode in resp['nodes']:
        if ('supportsHotWater' not in oNode['attributes']) and "nodeType" in oNode['attributes']:
            # a = oNode["attributes"]["model"]
            # b = oNode['attributes']["nodeType"]
            # c = oNode["attributes"]
            if '.json' in oNode['attributes']["nodeType"] or "model" in oNode["attributes"]:

                if "reportedValue" in oNode["attributes"]["model"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    strModelTemp = strModel
                    intDeviceCntr = 0
                    while True:
                        intDeviceCntr = intDeviceCntr + 1
                        strModel = strModelTemp + "_" + str(intDeviceCntr)
                        if strModel in oDeviceDetails:
                            continue
                        else:
                            break

                    oDeviceDetails[strModel] = {}
                    strName = ""
                    oDeviceDetails[strModel]["nodeID"] = oNode["id"]
                    if "name" in oNode: strName = oNode["name"]
                    oDeviceDetails[strModel]["name"] = strName
                    oDeviceDetails[strModel]["version"] = oNode["attributes"]["softwareVersion"]["reportedValue"]
            elif "hardwareVersion" in oNode["attributes"]:
                print('inside Else')
                strHubModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                if "NANO" in strHubModel:
                    oDeviceDetails[strHubModel] = {}
                    oDeviceDetails[strHubModel]["nodeID"] = oNode["id"]
                    oDeviceDetails[strHubModel]["version"] = oNode["attributes"]["softwareVersion"]["reportedValue"]
    print("OOodevice",oDeviceDetails)
    return oDeviceDetails
    # ALAPI.deleteSessionV6(session)


    # Get the synthetic Node ID for the given device node ID


def getSyntheticDeviceID(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    strSyntheticDeviceID = ""
    for oNode in resp['nodes']:
        if "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "consumers" in oNode["attributes"]:
                strConsumersID = oNode["attributes"]["consumers"]["reportedValue"]
                print("strConsumersID", strConsumersID)
                if nodeID in strConsumersID:
                    strSyntheticDeviceID = oNode["id"]
                    break
    ALAPI.deleteSessionV6(session)
    return strSyntheticDeviceID


def getAttribute(oAttributeList, strAttributeName):
    reported = oAttributeList[strAttributeName]['reportedValue']
    if 'targetValue' in oAttributeList[strAttributeName]:
        target = oAttributeList[strAttributeName]['targetValue']
        targetTime = oAttributeList[strAttributeName]['targetSetTime']
        currentTime = int(time.time() * 1000)
        if (currentTime - targetTime) < 40000:
            print('taken target value for', strAttributeName)
            return target
    return reported


# Get SP Attributes
def getSPAttributes(nodeID):
    strMode = ""
    strState = ""
    syntheticNodeID = getSyntheticDeviceID(nodeID)
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            strState = getAttribute(oNode["attributes"], "state")
        elif oNode["id"] in syntheticNodeID:
            if getAttribute(oNode["attributes"]["syntheticDeviceConfiguration"], "enabled").upper() == "TRUE":
                strMode = "AUTO"
                strMode = "MANUAL"

    return strMode, strState


@when(
    u'the {strDeviceType} state is changed to below states and validated using the zigbee attribute and repeated {strCount}')
def onOFFValidation(context, strDeviceType, strCount):
    context.nodeId = ""
    context.ep = ""
    myNodeId = ""
    myEp = ""
    if str(strCount).upper() == "INFINITELY":
        intLoopCtr = 1
    else:
        strCount = strCount.replace(" times", "")
        intLoopCtr = int(strCount)
    intCntr = 0
    # intLoopCtr = 0
    flag = True
    while flag:
        for intIter in range(0, intLoopCtr):
            intCntr = intCntr + 1
            intIter = intIter + 1
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('ON-OFF Counter : ' + str(intCntr))
            if "SLP" in str(strDeviceType).upper():
                myEp = "09"
            elif "BULB" in str(strDeviceType).upper():
                myEp = "01"
            for oRow in context.table:
                DeviceType = ""
                NodeID = ""
                if str(strDeviceType).upper() == "GENERIC":
                    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                    # NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                    oJson = dutils.getDeviceNode(DeviceName, False)
                    MAcID = oJson['macID']
                    DeviceType = oJson['name']
                    myNodeId = oJson['nodeID']
                    context.nodeId = myNodeId
                    myEp = oJson["endPoints"][0]
                else:
                    MAcID = dutils.getDeviceMACWithModel(strDeviceType, True)
                    myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType, MAcID)
                print(strDeviceType, myNodeId, MAcID, "\n")
                strExp = ""
                strOpp = ""
                if str(oRow['State']).upper() == "OFF":
                    strExp = "00"
                    strOpp = "01"
                    strOppText = "ON"
                elif str(oRow['State']).upper() == "ON":
                    strExp = "01"
                    strOpp = "00"
                    strOppText = "OFF"
                else:
                    context.report().ReportEvent("Test Validation", "Invalid State", "FAIL")
                    exit()
                utils.setSPOnOff(myNodeId, oRow['State'], True, myEp)
                intCounter = 0
                context.reporter.ReportEvent("Test Validation", strDeviceType + " state is set to " + oRow['State'],
                                             "DONE")
                while intCounter < 6:

                    respState, respCode, respValue = utils.readAttribute("MANUFACTURER", myNodeId, myEp, 0, "0006",
                                                                         "0000")
                    if respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,00," + strExp:
                        context.reporter.ReportEvent("Test Validation",
                                                     "Current " + strDeviceType + " state is " + oRow['State'], "PASS")
                    elif respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,00,01":
                        context.reporter.ReportEvent("Test Validation",
                                                     "Current " + strDeviceType + " state is " + strOppText, "FAIL")
                    elif respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,86":
                        context.reporter.ReportEvent("Test Validation", "Attribute is unreadable", "FAIL")
                    else:
                        context.reporter.ReportEvent("Test Validation", "Unexpected response: " + respValue, "FAIL")
                    time.sleep(10)
                    intCounter = intCounter + 1
            if str(strCount).upper() == "INFINITELY":
                intIter = 0
            if intIter == intLoopCtr:
                flag = False
                break


@then(u'the {strDeviceType} state is changed to {strState} for {strDuration} seconds via telegesis')
def onOFFValidation(context, strDeviceType, strState, strDuration):
    context.nodeId = ""
    context.ep = ""
    myNodeId = ""
    myEp = ""

    context.reporter.HTML_TC_BusFlowKeyword_Initialize(strDeviceType + " " + strState)
    if str(strDeviceType).upper() == "SMARTPLUG":
        for oRow in context.table:
            DeviceType = ""
            NodeID = ""
            if str(oRow['DeviceType']).upper() == "GENERIC":
                DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                oJson = dutils.getDeviceNode(DeviceName, False)
                MAcID = oJson['macID']
                DeviceType = oJson['name']
                myNodeId = oJson['nodeID']
                context.nodeId = myNodeId
                myEp = oJson["endPoints"][0]
            else:
                DeviceName = oRow['DeviceName']
                DeviceType = oRow['DeviceType']
                MAcID = oRow['MacID']
                myNodeId = utils.get_device_node_from_ntable(MAcID)
                myEp = "09"
            print(DeviceName, DeviceType, myNodeId, MAcID, "\n")
            strExp = ""
            strOpp = ""
            if strState.upper() == "OFF":
                strExp = "00"
                strOppText = "ON"
            elif strState.upper() == "ON":
                strExp = "01"
                strOppText = "OFF"
            else:
                context.report().ReportEvent("Test Validation", "Invalid State", "FAIL")
                exit()
            utils.setSPOnOff(myNodeId, strState, True)
            context.reporter.ReportEvent("Test Validation", "Smart Plug state is set to " + strState, "DONE")

            respState, respCode, respValue = utils.readAttribute("MANUFACTURER", myNodeId, myEp, 0, "0006",
                                                                 "0000")
            if respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,00," + strExp:
                context.reporter.ReportEvent("Test Validation", "Current smart Plug state is " + strState,
                                             "PASS")
            elif respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,00,01":
                context.reporter.ReportEvent("Test Validation", "Current smart Plug state is " + strOppText,
                                             "FAIL")
            elif respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,86":
                context.reporter.ReportEvent("Test Validation", "Attribute is unreadable", "FAIL")
            else:
                context.reporter.ReportEvent("Test Validation", "Unexpected response: " + respValue, "FAIL")
            context.reporter.ReportEvent("Test Validation", "Wait for: " + str(strDuration) + " Seconds started",
                                         "Done")
            time.sleep(int(strDuration))
            context.reporter.ReportEvent("Test Validation", "Wait for: " + str(strDuration) + " Seconds completed",
                                         "Done")


@when(
    u'the {strDeviceType} state is changed for {strDuration} to below states and validated using the zigbee attribute and repeated {strCount}')
def onOFFValidation(context, strDeviceType, strCount, strDuration):
    context.nodeId = ""
    context.ep = ""
    myNodeId = ""
    myEp = ""
    if str(strCount).upper() == "INFINITELY":
        intLoopCtr = 1
    else:
        strCount = strCount.replace(" times", "")
        intLoopCtr = int(strCount)
    intCntr = 0
    # intLoopCtr = 0
    flag = True
    while flag:
        for intIter in range(0, intLoopCtr):
            intCntr = intCntr + 1
            intIter = intIter + 1
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('ON-OFF Counter : ' + str(intCntr))
            if "SLP" in str(strDeviceType).upper():
                myEp = "09"
            elif "BULB" in str(strDeviceType).upper():
                myEp = "01"
            for oRow in context.table:
                DeviceType = ""
                NodeID = ""
                if str(strDeviceType).upper() == "GENERIC":
                    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                    # NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                    oJson = dutils.getDeviceNode(DeviceName, False)
                    MAcID = oJson['macID']
                    DeviceType = oJson['name']
                    myNodeId = oJson['nodeID']
                    context.nodeId = myNodeId
                    myEp = oJson["endPoints"][0]
                else:
                    MAcID = dutils.getDeviceMACWithModel(strDeviceType, True)
                    myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType, MAcID)
                print(strDeviceType, myNodeId, MAcID, "\n")
                strExp = ""
                strOpp = ""
                if str(oRow['State']).upper() == "OFF":
                    strExp = "00"
                    strOpp = "01"
                    strOppText = "ON"
                elif str(oRow['State']).upper() == "ON":
                    strExp = "01"
                    strOpp = "00"
                    strOppText = "OFF"
                else:
                    context.report().ReportEvent("Test Validation", "Invalid State", "FAIL")
                    exit()
                utils.setSPOnOff(myNodeId, oRow['State'], True, myEp)
                intCounter = 0
                context.reporter.ReportEvent("Test Validation", strDeviceType + " state is set to " + oRow['State'],
                                             "DONE")
                while intCounter < 6:

                    respState, respCode, respValue = utils.readAttribute("MANUFACTURER", myNodeId, myEp, 0, "0006",
                                                                         "0000")
                    if respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,00," + strExp:
                        context.reporter.ReportEvent("Test Validation",
                                                     "Current " + strDeviceType + " state is " + oRow['State'], "PASS")
                    elif respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,00,01":
                        context.reporter.ReportEvent("Test Validation",
                                                     "Current " + strDeviceType + " state is " + strOppText, "FAIL")
                    elif respValue == "RESPATTR:" + myNodeId + "," + myEp + ",0006,0000,86":
                        context.reporter.ReportEvent("Test Validation", "Attribute is unreadable", "FAIL")
                    else:
                        context.reporter.ReportEvent("Test Validation", "Unexpected response: " + respValue, "FAIL")
                    if str(oRow['State']).upper() == "OFF":
                        time.sleep(5)
                    else:
                        time.sleep(600)
                    intCounter = intCounter + 1
            if str(strCount).upper() == "INFINITELY":
                intIter = 0
            if intIter == intLoopCtr:
                flag = False
                break


@given(u'Hive product {PlugName} with {ModelNo} should be paired to the Hub.')
def setup_menu(context, PlugName, ModelNo):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Checking Plug availability based on Model No and PlugName')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.setup_menu(PlugName, ModelNo)
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.setup_menu(PlugName, ModelNo)


@when(u'User is navigated to {PlugName} Screen.')
def plug_navigation(context, PlugName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the plugs icon from dashboard')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.plugnavigation(PlugName)
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.plugnavigation(PlugName)


@when(u'User is on the {PlugName} Screen.')
def verify_plugscreen(context, PlugName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the plugs screen navigation.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.verifyplugscreen(PlugName)
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.verifyplugscreen(PlugName)


@then(u'Validate the {PlugName} title of the Plug Screen.')
def validate_title(context, PlugName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the title of plugs screen.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.validate_title(PlugName)
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.validate_title(PlugName)


@when(u'User clicks on the {PlugName} toggle button.')
def click_plug_toggle(context, PlugName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Validating the plug state before action and Clicking the plug toggle icon to change its state')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.clickplug_toggle(PlugName)
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.clickplug_toggle(PlugName)


@then(u'{PlugName} should be switched on or off.')
def verify_plugstate(context, PlugName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the plugs state after changing state.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.verify_plugstate(PlugName)
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.verify_plugstate(PlugName)

    @then(u'Validate the {PlugName} state change in Dashboard and Device Screen.')
    def verify_plugstate_dashboard(context, PlugName):
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the plugs state in Dashboard and device Screen.')
        if 'ANDROID' in strMainClient.upper():
            platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
            platMenu.verify_plugstate_dashboard_devicelist(PlugName)
        elif 'IOS' in strMainClient.upper():
            platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
            platMenu.verify_plugstate_dashboard_devicelist(PlugName)


@when(u'User clicks on the {PlugName} arrow button from the bottom of plug screen.')
def click_plug_mode(context, PlugName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Validating the plug mode before action and Clicking the arrow button to change the mode.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.click_plug_mode(PlugName)
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.click_plug_mode(PlugName)


@then(u'{PlugName} Mode should be changed either to Manual or Schedule.')
def verify_plugmode(context, PlugName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the plugs state after changing the mode.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.verify_plugmode(PlugName)
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.verify_plugmode(PlugName)


@when(u'User clicks on the Schedule icon in Plugs Screen.')
def click_scheduleicon(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the Schedule icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.click_scheduleicon()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.click_scheduleicon()


@then(u'User should be navigated to the Schedule page of Plugs Screen.')
def verify_schedulescreen(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the Schedule screen of plugs.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.verify_schedulescreen()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.verify_schedulescreen()


@when(u'User clicks on the Recipes icon in Plugs Screen.')
def click_recipesicon(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the Recipes icon in plugs screen.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.click_recipesicon()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.click_recipesicon()


@then(u'User should be navigated to Recipes Page of Plugs Screen.')
def verify_recipesscreen(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the Recipes screen in plugs.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.verify_recipesscreen()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.verify_recipesscreen()


@when(u'User clicks on the Control icon in Plugs screen.')
def click_controlicon(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the control icon in plugs')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.click_controlicon()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.click_controlicon()


@then(u'User should be navigated to the control page of Plugs Screen.')
def verify_controlscreen(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the control screen in plugs')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.AndroidDriver, context.reporter)
        platMenu.verify_controlscreen()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.Plugs(context.iOSDriver, context.reporter)
        platMenu.verify_controlscreen()
