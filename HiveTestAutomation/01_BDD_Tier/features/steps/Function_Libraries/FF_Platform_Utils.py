"""
Created on 27 Jan 2016

@author: ranganathan.veluswamy

@author: Hitesh Sharma 10 Aug 2016
@note: added functions getSyntheticDeviceID - get the synthetic device id for CS, getCSAttributes - get the CS attributes, getAttribute- get the current state for CS from platform
@note: 13 Sept 2016 - added functions getTHENValueAndDurationForRecipe, getLightBulbAttributes and getColourTemprature for recipes and light bulb
"""

import collections
import json
import time
import FF_alertmeApi as ALAPI
import FF_utils as utils
import FF_Beekeeper as ALBKP

oWeekDayList = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


# Get the Node ID for the given device type
def getNodeAndDeviceVersionID():
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    oDeviceDetails = {}
    for oNode in resp['nodes']:
        if ('supportsHotWater' not in oNode['attributes']) and "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "model" in oNode["attributes"]:
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
                    if "softwareVersion" in oNode["attributes"]:
                        oDeviceDetails[strModel]["version"] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    if "presence" in oNode["attributes"]:
                        oDeviceDetails[strModel]["presence"] = oNode["attributes"]["presence"]["reportedValue"]

            elif "hardwareVersion" in oNode["attributes"]:
                strHubModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                if "NANO" in strHubModel:
                    oDeviceDetails[strHubModel] = {}
                    oDeviceDetails[strHubModel]["nodeID"] = oNode["id"]
                    oDeviceDetails[strHubModel]["version"] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    oDeviceDetails[strHubModel]["presence"] = oNode["attributes"]["presence"]["reportedValue"]
    ALAPI.deleteSessionV6(session)
    return oDeviceDetails


# Get the Nodes
def getNodes():
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    nodes = ALAPI.getNodesV6(session)
    ALAPI.deleteSessionV6(session)
    return nodes


# Get the Nodes for specific Node ID
def getNodeByID(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    nodes = ALAPI.getNodesByIDV6(session, nodeID)
    ALAPI.deleteSessionV6(session)
    return nodes


def getHubNodeID():
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oHubNodeID = oNodeIDList[searchSubStringInList(oKeyList, "NANO")[0]]["nodeID"]
    return oHubNodeID


def getDeviceNodeID(deviceType):
    oDeviceNodeID = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType)
    if len(oSearchedList) > 0:
        strKey = oSearchedList[0]
        oDeviceNodeID = oNodeIDList[strKey]["nodeID"]
    return oDeviceNodeID


def getOnlineDeviceNodeID(deviceType):
    oDeviceNodeID = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType)
    if len(oSearchedList) > 0:
        for a in range(len(oSearchedList)):
            strKey = oSearchedList[a]
            oDevicePresence = oNodeIDList[strKey]["presence"]
            if oDevicePresence == 'PRESENT':
                oDeviceNodeID = oNodeIDList[strKey]["nodeID"]
                break
    return oDeviceNodeID


def getDeviceName(deviceType):
    oDeviceName = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType)
    if len(oSearchedList) > 0:
        strKey = oSearchedList[0]
        oDeviceName = oNodeIDList[strKey]["name"]
    return oDeviceName


def getDeviceNames():
    oDeviceName = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    intCounter = 0
    for oNode in oNodeIDList:
        oDeviceName += oNode["name"]
        oDeviceName += ";"

    return oDeviceName


def getDeviceVersion(deviceType):
    oDeviceVersion = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType)
    if len(oSearchedList) > 0:
        strKey = oSearchedList[0]
        oDeviceVersion = oNodeIDList[strKey]["version"]
    return oDeviceVersion


def getDevicePresence(deviceType):
    oDevicePresence = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType)
    if len(oSearchedList) > 0:
        strKey = oSearchedList[0]
        oDevicePresence = oNodeIDList[strKey]["presence"]
    return oDevicePresence

def getDevicePresenceByName(deviceType, deviceName):
    oDevicePresence = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    for oNode in oNodeIDList:
        if deviceName in oNodeIDList[oNode]["name"] and deviceType in oNode:
            oDevicePresence = oNodeIDList[oNode]["presence"]
    return oDevicePresence


def getDeviceSDNodeID(nodeID):
    oSDNodeID = ""
    nodes = getNodes()

    for oNode in nodes['nodes']:
        # if ('supportsHotWater'  not in oNode['attributes']) and "nodeType" in oNode:
        if "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and ('fake' not in oNode["nodeType"]):
                if "consumers" in oNode["attributes"]:
                    if nodeID.upper() in oNode["attributes"]["consumers"]["reportedValue"].upper():
                        if not "trigger" in oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]:
                            oSDNodeID = oNode["id"]
                            break

    return oSDNodeID, oNode


def getDeviceSchedule(deviceType):
    nodeID = getDeviceNodeID(deviceType)
    SDNodeID, oNode = getDeviceSDNodeID(nodeID)
    SDConfig = oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]

    if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
    oSchedule = SDConfig["schedule"]

    return oSchedule


def getDeviceScheduleInStandardFormat(deviceType):
    nodeID = getDeviceNodeID(deviceType)
    SDNodeID, oNode = getDeviceSDNodeID(nodeID)
    SDConfig = oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]

    if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
    oSchedule = SDConfig["schedule"]
    oFormattedched = {}
    for oDaySchedList in oSchedule:
        strDay = oWeekDayList[int(oDaySchedList["dayIndex"]) - 1]
        oTransitions = oDaySchedList["transitions"]
        oSchedList = []
        for oEvent in oTransitions:
            strTime = oEvent["time"]
            strState = oEvent["action"]["state"]
            if 'colourMode' in oEvent["action"]:
                strColourMode = oEvent["action"]["colourMode"]
            if not 'colourMode' in oEvent["action"] or 'TUNABLE' in strColourMode:
                if "brightness" in oEvent["action"]:
                    intBrightness = oEvent["action"]["brightness"]
                    if "colourTemperature" in oEvent["action"]:
                        floatColourTemperature = oEvent["action"]["colourTemperature"]
                        strLightTone = getLightTone(floatColourTemperature)
                        oSchedList.append((strTime, strState, intBrightness, strLightTone))
                    else:
                        oSchedList.append((strTime, strState, intBrightness))
                else:
                    oSchedList.append((strTime, strState))
            elif 'COLOUR' in strColourMode:
                intBrightness = oEvent["action"]["hsvValue"]
                intHue = oEvent["action"]["hsvHue"]
                strLightColour = getLightColour(intHue)
                oSchedList.append((strTime, strState, intBrightness, strLightColour))
        oFormattedched[strDay] = oSchedList
    return oFormattedched


def removeDayFromScheduleAPI(oSchedule, oDayList):
    for strDay in oDayList:
        for oDayNode in oSchedule:
            intDayIndex = oDayNode["dayIndex"]
            strDayOnSchd = oWeekDayList[intDayIndex - 1]
            if strDayOnSchd == strDay:
                del oSchedule[oSchedule.index(oDayNode)]
                break

    return oSchedule


# Get Light Attributes
def getLightAttributes(nodeID):
    strLightMode = ""
    strLightState = ""
    intLightBrightness = 0
    floatColourTemperature = ""
    strColourMode = ""
    strLightColour = ""
    strTone = None
    oNode = getNodeByID(nodeID)
    oNode = oNode["nodes"][0]
    if "model" in oNode["attributes"]:
        if not "RGBBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
            if not "TWBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
                if not "FWBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
                    return strLightMode, strLightState, intLightBrightness, floatColourTemperature

    # Get State
    strLightState = oNode["attributes"]["state"]["reportedValue"]
    # Get Brightness
    if not "RGBBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
        intLightBrightness = int(oNode["attributes"]["brightness"]["reportedValue"])
    # GetMode
    SDNodeID, _ = getDeviceSDNodeID(nodeID)
    oSDNode = getNodeByID(SDNodeID)
    SDConfig = oSDNode["nodes"][0]["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
    if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
    boolSchedule = str(SDConfig["enabled"])
    if "TRUE" in boolSchedule.upper():
        strLightMode = "AUTO"
    else:
        strLightMode = "MANUAL"
    # Get Colour Temperature / Colour
    if "TWBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
        floatColourTemperature = float(oNode["attributes"]["colourTemperature"]["reportedValue"])
        strTone = getLightTone(floatColourTemperature)
    elif "RGBBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
        strColourMode = oNode["attributes"]["colourMode"]["reportedValue"]
        if "COLOUR" in strColourMode.upper():
            intLightBrightness = oNode["attributes"]["hsvValue"]["reportedValue"]
            strColourHue = oNode["attributes"]["hsvHue"]["reportedValue"]
            strColour = getLightColour(strColourHue)
            return strLightMode, strLightState, intLightBrightness, strColour
        else:
            floatColourTemperature = float(oNode["attributes"]["colourTemperature"]["reportedValue"])
            strTone = getLightTone(floatColourTemperature)
            return strLightMode, strLightState, intLightBrightness, strTone

    return strLightMode, strLightState, intLightBrightness, strTone


def getLightAttributesFromNode(nodes, oNode):
    strLightMode = ""
    strLightState = ""
    intLightBrightness = 0
    floatColourTemperature = ""
    strColourMode = ""
    strLightColour = ""
    strTone = None
    oSched = ''
    if "model" in oNode["attributes"]:
        if not "RGBBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
            if not "TWBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
                if not "FWBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
                    return strLightMode, strLightState, intLightBrightness, floatColourTemperature, oSched

    # Get State
    strLightState = oNode["attributes"]["state"]["reportedValue"]
    # Get Brightness
    if not "RGBBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
        intLightBrightness = int(oNode["attributes"]["brightness"]["reportedValue"])

    oSched, oSDNode = getScheduleNodeInStandardFormat(nodes, oNode['id'])
    strLightMode = "MANUAL"
    if oSDNode != '':
        SDConfig = oSDNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
        if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
        boolSchedule = str(SDConfig["enabled"])
        if "TRUE" in boolSchedule.upper():
            strLightMode = "AUTO"
    # Get Colour Temperature / Colour
    if "TWBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
        floatColourTemperature = float(oNode["attributes"]["colourTemperature"]["reportedValue"])
        strTone = getLightTone(floatColourTemperature)
    elif "RGBBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
        strColourMode = oNode["attributes"]["colourMode"]["reportedValue"]
        if "COLOUR" in strColourMode.upper():
            intLightBrightness = oNode["attributes"]["hsvValue"]["reportedValue"]
            strColourHue = oNode["attributes"]["hsvHue"]["reportedValue"]
            strColour = getLightColour(strColourHue)
            return strLightMode, strLightState, intLightBrightness, strColour, oSched
        else:
            floatColourTemperature = float(oNode["attributes"]["colourTemperature"]["reportedValue"])
            strTone = getLightTone(floatColourTemperature)
            return strLightMode, strLightState, intLightBrightness, strTone, oSched
    return strLightMode, strLightState, intLightBrightness, strTone, oSched


def getScheduleNodeInStandardFormat(nodes, nodeID):
    oSDNodeID = ''
    oSDNode = ''
    oFormattedched = ''
    for oNode in nodes:
        # if ('supportsHotWater'  not in oNode['attributes']) and "nodeType" in oNode:
        if "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and (not 'fake' in oNode["nodeType"]):
                if "consumers" in oNode["attributes"]:
                    if nodeID.upper() in oNode["attributes"]["consumers"]["reportedValue"].upper():
                        if 'syntheticDeviceConfiguration' in oNode["attributes"]:
                            if not "trigger" in oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]:
                                oSDNodeID = oNode["id"]
                                oSDNode = oNode

    if oSDNodeID != '':
        SDConfig = oSDNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
        if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
        oSchedule = SDConfig["schedule"]
        oFormattedched = {}
        for oDaySchedList in oSchedule:
            strDay = oWeekDayList[int(oDaySchedList["dayIndex"]) - 1]
            oTransitions = oDaySchedList["transitions"]
            oSchedList = []
            for oEvent in oTransitions:
                strTime = oEvent["time"]
                strState = oEvent["action"]["state"]
                if 'colourMode' in oEvent["action"]:
                    strColourMode = oEvent["action"]["colourMode"]
                if not 'colourMode' in oEvent["action"] or 'TUNABLE' in strColourMode:
                    if "brightness" in oEvent["action"]:
                        intBrightness = oEvent["action"]["brightness"]
                        if "colourTemperature" in oEvent["action"]:
                            floatColourTemperature = oEvent["action"]["colourTemperature"]
                            strLightTone = getLightTone(floatColourTemperature)
                            oSchedList.append((strTime, strState, intBrightness, strLightTone))
                        else:
                            oSchedList.append((strTime, strState, intBrightness))
                    else:
                        oSchedList.append((strTime, strState))
                elif 'COLOUR' in strColourMode:
                    intBrightness = oEvent["action"]["hsvValue"]
                    intHue = oEvent["action"]["hsvHue"]
                    strLightColour = getLightColour(intHue)
                    oSchedList.append((strTime, strState, intBrightness, strLightColour))
            oFormattedched[strDay] = oSchedList

    return oFormattedched, oSDNode


def getLightColour(colourHue):
    if 0 <= colourHue <= 10:
        strColour = "RED"
    elif 11 <= colourHue <= 20:
        strColour = "RED ORANGE"
    elif 21 <= colourHue <= 40:
        strColour = "ORANGE"
    elif 41 <= colourHue <= 50:
        strColour = "ORANGE YELLO"
    elif 51 <= colourHue <= 60:
        strColour = "YELLOW"
    elif 61 <= colourHue <= 80:
        strColour = "YELLOW GREEN"
    elif 81 <= colourHue <= 140:
        strColour = "GREEN"
    elif 141 <= colourHue <= 169:
        strColour = "GREEN CYAN"
    elif 170 <= colourHue <= 200:
        strColour = "CYAN"
    elif 201 <= colourHue <= 220:
        strColour = "CYAN BLUE"
    elif 221 <= colourHue <= 240:
        strColour = "BLUE"
    elif 241 <= colourHue <= 280:
        strColour = "BLUE MAGENTA"
    elif 281 <= colourHue <= 320:
        strColour = "MAGENTA"
    elif 321 <= colourHue <= 330:
        strColour = "MAGENTA PINK"
    elif 331 <= colourHue <= 345:
        strColour = "PINK"
    elif 346 <= colourHue <= 355:
        strColour = "PINK RED"
    elif 355 <= colourHue <= 359:
        strColour = "RED"
    return strColour


def getLightTone(floatColourTemperature):
    if 2700 <= floatColourTemperature < 3461:
        strLightTone = "WARMEST WHITE"
    elif 3461 <= floatColourTemperature < 4221:
        strLightTone = "WARM WHITE"
    elif 4221 <= floatColourTemperature < 4981:
        strLightTone = "MID WHITE"
    elif 4981 <= floatColourTemperature < 5741:
        strLightTone = "COOL WHITE"
    elif 5741 <= floatColourTemperature < 6536:
        strLightTone = "COOLEST WHITE"
    return strLightTone


def searchSubStringInList(oList, strSearchString):
    return [oHeader for oHeader in oList if isinstance(oHeader, collections.Iterable) and (strSearchString in oHeader)]


def getSyntheticDeviceID(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    strSyntheticDeviceID = ""
    for oNode in resp['nodes']:
        if "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "producers" in oNode["attributes"]:
                strProducerID = oNode["attributes"]["producers"]["reportedValue"]
                print("strProducerID", strProducerID)
                if nodeID in strProducerID:
                    strSyntheticDeviceID = oNode["id"]
                    break
    ALAPI.deleteSessionV6(session)
    return strSyntheticDeviceID


def getCSAttributes(nodeID):
    finalCSState = ""
    # syntheticNodeID = getSyntheticDeviceID(nodeID)
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        # if "nodeType" in oNode:
        # if '.json' in oNode["nodeType"]:
        if nodeID in oNode["id"]:
            finalCSState = getAttribute(oNode["attributes"], "state")
            # if nodeID in oNode["id"]:
            # finalState = getAttribute(oNode["attributes"], "state")
            print('Reported state for contact sensor is ' + finalCSState)
            break
        else:
            print('Reported state for contact sensor is missing')

    return finalCSState


def getMSAttributes(nodeID):
    finalMSState = ""
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)

    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            finalMSState = getAttribute(oNode["attributes"], "inMotion")
            print('Reported state for motion sensor is ' + str(finalMSState))
    return finalMSState


def getMotionSensorEventLogs(nodeID):
    oMotionEventLogsDict = {}
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getEvents(session, strDeviceType='MOTION SENSOR')
    print(resp)
    oEventDays = resp.keys()
    print(oEventDays)
    print(nodeID)

    for oDayEvents in range(1, (len(resp) + 1)):
        oEventStartTimeList = []
        oEventEndTimeList = []
        oMotionEventsTimingsThatDay = []
        oDay = 'Day ' + str(oDayEvents)
        if 'events' in resp[oDay]:
            for oEvent in resp[oDay]['events']:
                if oEvent['eventType'] == 'MOTION_STARTED':
                    if oEvent['source'] == nodeID:
                        oEventStartTime = oEvent['properties']['triggeringEventTime']
                        oEventStartTimeList.append(int(oEventStartTime))
                elif oEvent['eventType'] == 'MOTION_ENDED':
                    if oEvent['source'] == nodeID:
                        oEventEndTime = oEvent['properties']['triggeringEventTime']
                        oEventEndTimeList.append(int(oEventEndTime))

            oEventStartTimeList.sort()
            oEventEndTimeList.sort()
            print(oEventStartTimeList, oEventEndTimeList)

            for oCount in range(0, (len(oEventStartTimeList))):
                oStartAndEndTime = []
                if oCount == 0:
                    if not (oEventEndTimeList[0] < oEventStartTimeList[0]):
                        oEventStartTimeList[oCount], oEventEndTimeList[oCount] = epochToGMT(oEventStartTimeList[oCount],
                                                                                            oEventEndTimeList[oCount])
                        oStartAndEndTime.append(oEventStartTimeList[oCount])
                        oStartAndEndTime.append(oEventEndTimeList[oCount])
                    else:
                        oEventStartTimeList[oCount], oEventEndTimeList[oCount] = epochToGMT(oEventStartTimeList[oCount],
                                                                                            oEventEndTimeList[oCount])
                        oStartAndEndTime.append('0')
                        oStartAndEndTime.append(oEventEndTimeList[oCount])

                elif oCount == (len(oEventStartTimeList) - 1):
                    if not len(oEventStartTimeList) == len(oEventEndTimeList):
                        if not (oEventStartTimeList[oCount] < oEventEndTimeList[oCount]):
                            oEventStartTimeList[oCount], oEventEndTimeList[oCount] = epochToGMT(
                                oEventStartTimeList[oCount], oEventEndTimeList[oCount])
                            oStartAndEndTime.append(oEventStartTimeList[oCount])
                            oStartAndEndTime.append('0')
                        else:
                            oEventStartTimeList[oCount], oEventEndTimeList[oCount] = epochToGMT(
                                oEventStartTimeList[oCount], oEventEndTimeList[oCount])
                            oStartAndEndTime.append(oEventStartTimeList[oCount])
                            oStartAndEndTime.append(oEventEndTimeList[oCount])

                    elif len(oEventStartTimeList) == len(oEventEndTimeList):

                        if not (oEventStartTimeList[oCount] < oEventEndTimeList[oCount]):
                            oEventStartTimeList[oCount], oEventEndTimeList[oCount] = epochToGMT(
                                oEventStartTimeList[oCount], oEventEndTimeList[oCount])
                            oStartAndEndTime.append(oEventStartTimeList[oCount])
                            oStartAndEndTime.append('0')
                        else:
                            oEventStartTimeList[oCount], oEventEndTimeList[oCount] = epochToGMT(
                                oEventStartTimeList[oCount], oEventEndTimeList[oCount])
                            oStartAndEndTime.append(oEventStartTimeList[oCount])
                            oStartAndEndTime.append(oEventEndTimeList[oCount])

                else:
                    oEventStartTimeList[oCount], oEventEndTimeList[oCount] = epochToGMT(oEventStartTimeList[oCount],
                                                                                        oEventEndTimeList[oCount])
                    oStartAndEndTime.append(oEventStartTimeList[oCount])
                    oStartAndEndTime.append(oEventEndTimeList[oCount])

                # print (oStartAndEndTime)
                oMotionEventsTimingsThatDay.append(oStartAndEndTime)
                print(oMotionEventsTimingsThatDay)

            oMotionEventLogsDict.update({oDay: oMotionEventsTimingsThatDay})
            print(oMotionEventLogsDict)


            # Need to add a logic here to find the duration of motion
            # - once confirming with different terms used in that section in the UI


def epochToGMT(oEventStartTime, oEventEndTime):
    oEventStartTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(oEventStartTime / 1000.0))
    oEventEndTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(oEventEndTime / 1000.0))

    oEventStartTime = oEventStartTime[11:]
    oEventStartTime = oEventStartTime[:5]
    oEventEndTime = oEventEndTime[11:]
    oEventEndTime = oEventEndTime[:5]
    return oEventStartTime, oEventEndTime


def getColourBulbValues(nodeID, attributeVerify, attributeName):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    attributeValue = ""
    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            attributeValue = oNode["attributes"][attributeVerify][attributeName]
            return attributeValue
        else:
            continue


def getAttribute(oAttributeList, strAttributeName):
    if strAttributeName in oAttributeList:
        csState = oAttributeList[strAttributeName]['reportedValue']
        print(csState)
    else:
        print("No such attribute is available for the sensor")
        csState = 'No such attribute'
    return csState


def getTHENValueAndDurationForRecipe(nodeID):
    finalDuration = ""
    strValue = ""
    syntheticNodeID = getSyntheticDeviceIDForRecipe(nodeID)
    print(syntheticNodeID)
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        if oNode["id"] in syntheticNodeID:
            tempDuration = oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
            if isinstance(tempDuration, str):
                tempDuration = json.loads(tempDuration)
                print(tempDuration, "\n")
                finalDuration = tempDuration["action"]["duration"]

            oAction = tempDuration["action"]["action"]
            print(oAction, "\n")
            if isinstance(oAction, str):
                print("oAction is string")
            changeList = oAction["changes"]
            for newDict in changeList:
                strValue = newDict["value"]
            return finalDuration, strValue


def getSyntheticDeviceIDForRecipe(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    strSyntheticDeviceID = ""
    for oNode in resp['nodes']:
        if "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "producers" in oNode["attributes"]:
                strProducersID = oNode["attributes"]["producers"]["reportedValue"]
                print(strProducersID, "\n")

                if nodeID in strProducersID:
                    strSyntheticDeviceID = oNode["id"]
                    print(strSyntheticDeviceID)
                    break
    ALAPI.deleteSessionV6(session)
    return strSyntheticDeviceID


def getLightBulbAttributes(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    lightBulbBrigtness = ""

    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            lightBulbBrigtness = getAttribute(oNode["attributes"], "brightness")
            print(lightBulbBrigtness, "\n")
        else:
            print("Light bulb brightness value is missing")
    return lightBulbBrigtness


def getColourTemprature(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    reportedValue = ""
    targetValue = ""

    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            reportedValue = getAttribute(oNode["attributes"], "colourTemperature")
            targetValue = getAttribute(oNode["attributes"], "colourTemperature")
            print(reportedValue, "\n")
            print(targetValue, "\n")
        else:
            print("Light bulb brightness value is missing")
    return reportedValue, targetValue


def getDeviceModel(deviceName):
    nodes = getNodes()
    for oNode in nodes['nodes']:
        if oNode['name'].upper() == deviceName.upper():
            return oNode["attributes"]["model"]["reportedValue"]


# Get device mode status
def getDeviceModeStatus(nodeID):
    strDeviceMode = ""
    oNode = getNodeByID(nodeID)
    # print(oNode)
    oNode = oNode["nodes"][0]
    if "model" in oNode["attributes"]:
        if not "BULB" in oNode["attributes"]["model"]["displayValue"].upper():
            return strDeviceMode

    # GetMode
    SDNodeID, _ = getDeviceSDNodeID(nodeID)
    oSDNode = getNodeByID(SDNodeID)
    SDConfig = oSDNode["nodes"][0]["attributes"]["syntheticDeviceConfiguration"]["displayValue"]
    if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
    boolSchedule = str(SDConfig["enabled"])
    if "TRUE" in boolSchedule.upper():
        strDeviceMode = "AUTO"
    else:
        strDeviceMode = "MANUAL"

    return strDeviceMode


def getDeviceNodeByName(deviceName):
    nodes = getNodes()
    for oNode in nodes['nodes']:
        if oNode['name'].upper() == deviceName.upper():
            return oNode["id"]


def getAllRecipesCount():
    nodes = getNodes()
    counter = 0
    for oNode in nodes['nodes']:
        if 'nodeType' in oNode:
            if "http://alertme.com/schema/json/node.class.synthetic.rule.json#" in oNode['nodeType']:
                counter = counter + 1
    return counter


def getSensorRecipeCount(sensorName):
    nodes = getNodes()
    id = getDeviceNodeByName(sensorName)
    print(sensorName + " id is : " + str(id))
    '''for char in '["]':
        id = id.replace(char, '')'''
    counter = 0
    for oNode in nodes['nodes']:
        if 'nodeType' in oNode:
            if "http://alertme.com/schema/json/node.class.synthetic.rule.json#" in oNode['nodeType'] and id in \
                    oNode["attributes"]["producers"]["reportedValue"]:
                counter = counter + 1
    return counter


def getDeviceIDsAndPositionsByBeekeeper():
    ALBKP.createCredentialsBeekeeper(utils.getAttribute('common', 'currentEnvironment'))
    BEEsession = ALBKP.sessionObject()
    BeeUserid = BEEsession.userId
    resp = ALBKP.getAttributesBEE(BEEsession, BeeUserid, 'dashboard-config')
    deviceIDAndPosition = {}
    for oNode in resp['pages']:
        for oItems in oNode['items']:
            deviceIDAndPosition[oItems['id']] = oItems['position']

    return deviceIDAndPosition


def getNAThermostat_Nodes(thermostatName):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObjectV6dot5()
    nodes = ALAPI.getNodesV6(session)
    ALAPI.deleteSessionV6(session)
    for oNode in nodes['nodes']:
        if oNode['name'].upper() == thermostatName.upper():
            return oNode


def getUserDevicesCount(session):
    nodes = ALAPI.getNodesV6(session)
    deviceCounts = {'motion-sensor': 0, 'contact-sensor': 0, 'plug': 0, 'lights': 0, 'thermostat': 0, 'hotwater': 0}
    counterMotionSensor = 0
    counterDoorSensor = 0
    counterPlug = 0
    counterLights = 0
    counterWarmLight = 0
    counterTuneableLight = 0
    counterColourLight = 0
    counterHeating = 0
    counterHotWater = 0

    for oNode in nodes['nodes']:
        if 'physical_device_v1' in oNode['features']:
            if "PIR00140005" in oNode["features"]["physical_device_v1"]["model"]["reportedValue"]:
                counterMotionSensor = counterMotionSensor + 1
            elif oNode["features"]["physical_device_v1"]["model"]["reportedValue"] in "WDS00140002":
                counterDoorSensor = counterDoorSensor + 1
            elif oNode["features"]["physical_device_v1"]["model"]["reportedValue"] in "SLP2":
                counterPlug = counterPlug + 1
            elif oNode["features"]["physical_device_v1"]["model"]["reportedValue"] in "FWBulb01":
                counterWarmLight = counterWarmLight + 1
            elif oNode["features"]["physical_device_v1"]["model"]["reportedValue"] in "TWBulb01UK":
                counterTuneableLight = counterTuneableLight + 1
            elif oNode["features"]["physical_device_v1"]["model"]["reportedValue"] in "RGBBulb01UK":
                counterColourLight = counterColourLight + 1
            elif oNode["features"]["physical_device_v1"]["model"]["reportedValue"] in "SLT3" or \
                            oNode["features"]["physical_device_v1"]["model"]["reportedValue"] in "SLT2":
                counterHeating = counterHeating + 1
            elif oNode["features"]["physical_device_v1"]["model"]["reportedValue"] in "SLR2":
                counterHotWater = counterHotWater + 1
            else:
                continue
        else:
            continue
    counterLights = counterWarmLight + counterTuneableLight + counterColourLight
    deviceCounts['motion-sensor'] = counterMotionSensor
    deviceCounts['contact-sensor'] = counterDoorSensor
    deviceCounts['plug'] = counterPlug
    deviceCounts['lights'] = counterLights
    deviceCounts['thermostat'] = counterHeating
    deviceCounts['hotwater'] = counterHotWater
    return deviceCounts


if __name__ == '__main__':
    pass
