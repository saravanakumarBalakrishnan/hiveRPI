from datetime import datetime, timedelta
import time
import FF_threadedSerial as AT
import FF_zigbeeToolsConfig as config
from threading import Thread
import FF_utils as utils
import json
import os
import traceback


class Mimic(object):
    def __init__(self, reporter):
        self.mimicDevices = []
        self.fuzzyMinStartTime = None
        self.fuzzyMaxStartTime = None
        self.fuzzyMaxStartTimeForAll = None
        self.fuzzyMinEndTime = None
        self.fuzzyMaxEndTime = None
        self.fuzzyMaxEndTimeForAll = None
        self.fuzzyMinStartTime = None
        self.fuzzyMinStartTime = None
        self.triggeredDevice = ''
        self.triggeredDevices = {}
        self.fluctuationLogs = {}
        self.allMimicDevicesDict = {}
        self.nonMimicDevicesDict = {}
        self.reporter = reporter
        self.fuzzyWindow = []
        self.TriggeredAll = False
        self.logsPath = ''
        self.oLJson = None
        self.nodes = {}
        self.DeviceLogs = ''
        self.Thread = True
        self.dict = {'01': 'ON', '00': 'OFF'}
        self.initialCounter = 1
        self.statusUpdatethread = None
        self.reporter.ActionStatus = True

    # Report the Failure step the HTML report
    def report_fail(self, strFailDescription):
        self.reporter.ActionStatus = False
        self.reporter.ReportEvent('Test Validation', strFailDescription, "FAIL", 'Center', True)
        self.Thread = False
        AT.stopThread.clear()

    # Report the Pass step the HTML report
    def report_pass(self, strPassDescription):
        self.reporter.ReportEvent('Test Validation', strPassDescription, "PASS", 'Center', True)

    def fuzzyLogic(self, fuzzyWindow, nextDay=False):
        try:
            if self.reporter.ActionStatus:
                day = datetime.now().strftime("%B %d %Y")
                startTime = fuzzyWindow[0]
                endTime = fuzzyWindow[1]
                dtmStartTime = datetime.strptime(day + ' ' + startTime, '%B %d %Y %H:%M')
                dtmEndTime = datetime.strptime(day + ' ' + endTime, '%B %d %Y %H:%M')
                if nextDay:
                    dtmStartTime += timedelta(hours=24)
                    dtmEndTime += timedelta(hours=24)
                if dtmEndTime < dtmStartTime: dtmEndTime + timedelta(hours=24)
                self.fuzzyMinStartTime = dtmStartTime
                self.fuzzyMaxStartTime = dtmStartTime + timedelta(minutes=30)
                self.fuzzyMaxStartTimeForAll = self.fuzzyMaxStartTime + timedelta(minutes=15)

                self.fuzzyMinEndTime = dtmEndTime - timedelta(minutes=30)
                self.fuzzyMaxEndTime = dtmEndTime
                self.fuzzyMaxEndTimeForAll = dtmEndTime + timedelta(minutes=15)
        except:
            self.report_fail('Mimic Logic : Exception: in fuzzyLogic Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def updateMimicDevices(self, Devices):
        # Devices - {'name', 'true'/'false'}
        try:
            if self.reporter.ActionStatus:
                mimicDevices = []
                for eachDevice in Devices.keys():
                    if 'true' == Devices[eachDevice]:
                        mimicDevices.append(eachDevice)
                self.mimicDevices = mimicDevices
        except:
            self.report_fail('Mimic Logic : Exception: in updateMimicDevices Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def validationCycle(self, context):
        time.sleep(60)
        try:
            if self.reporter.ActionStatus:
                dtmNow = datetime.now()
                dtmLoopEndTime = context.validationEndTime
                while dtmNow < dtmLoopEndTime:
                    self.getLightsStatus()
                    numberOfMimicDevicesON, allMimicDevicesDict, nonMimicDevicesDict = self.getNumberOfMimicDevicesOn(
                        context)
                    numberOfMimicDevicesONZigbee, allMimicDevicesDictZigbee, nonMimicDevicesDictZigbee = self.numberOfMimicDevicesONusingZigbee()

                    if self.fuzzyMinStartTime < dtmNow < self.fuzzyMaxStartTime:
                        if self.fetchTriggerTime(context, 'ON'):
                            self.report_pass('API Validation - Device ' + self.triggeredDevice + ' turned On')
                        else:
                            self.report_fail('None of the Device turned On')

                        if self.validateSingleDevice('ON'):
                            self.report_pass('Zigbee Validation - Device ' + self.triggeredDevice + ' turned ON ')
                        else:
                            self.report_fail('Zigbee Validation - the mimic devices status are not as expected ')


                    elif self.fuzzyMaxStartTime <= dtmNow < self.fuzzyMaxStartTimeForAll:
                        if self.allMimicDevicesUpdated(context, 'ON'):
                            self.fuzzyMaxStartTimeForAll = datetime.now()
                            self.TriggeredAll = False
                            self.report_pass('API Validation - All the mimic devices have turned ON')
                        else:
                            self.report_fail('Not all the devices at platform turned ON')
                        if not self.fluctuationLogs == {}:
                            for eachnode in self.fluctuationLogs:
                                self.report_fail('API Validation ' + self.fluctuationLogs[eachnode])

                        if self.validateAllDevices('ON'):
                            self.report_pass('ZIGBEE Validation - All the mimic devices have turned ON ')
                        else:
                            self.report_fail('Zigbee Validation - All the mimic devices status are not as expected ')
                        self.fluctuationZigbeeLogs = {}
                        self.display_flactuation()

                    elif self.fuzzyMaxStartTimeForAll <= dtmNow <= self.fuzzyMinEndTime:
                        if numberOfMimicDevicesON == len(self.mimicDevices):
                            self.report_pass('API Validation - All the mimic devices are in ON state ')
                        if self.validateAllDevices('ON'):
                            self.report_pass(
                                'ZIGBEE Validation - All the mimic devices are in ON state ')
                        else:
                            self.report_fail('Zigbee Validation - All the mimic devices status are not as expected ')

                    elif self.fuzzyMinEndTime < dtmNow <= self.fuzzyMaxEndTime:
                        self.triggeredDevice = ''
                        self.triggeredDevices = {}
                        self.fluctuationLogs = {}
                        if self.fetchTriggerTime(context, 'OFF'):
                            self.report_pass('API Validation - Device ' + self.triggeredDevice + ' turned Off')
                        else:
                            self.report_fail('API Validation - the mimic devices status are not as expected ')
                        if self.validateSingleDevice('OFF'):
                            self.report_pass('Zigbee Validation - Device ' + self.triggeredDevice + ' turned OFF')
                        else:
                            self.report_fail('Zigbee Validation - the mimic devices status are not as expected ')

                    elif self.fuzzyMaxEndTime < dtmNow < self.fuzzyMaxEndTimeForAll:
                        if self.allMimicDevicesUpdated(context, 'OFF'):
                            self.report_pass('API Validation - All the mimic devices have turned OFF')
                            self.fuzzyMaxEndTimeForAll = datetime.now()
                            self.TriggeredAll = False
                        if not self.fluctuationLogs == {}:
                            for eachnode in self.fluctuationLogs:
                                self.report_fail('API Validation ' + self.fluctuationLogs[eachnode])
                        if self.validateAllDevices('OFF'):
                            self.report_pass(
                                'ZIGBEE Validation - All the mimic devices have turned OFF ')
                        else:
                            self.report_fail('Zigbee Validation - All the mimic devices status are not as expected ')

                        self.fluctuationZigbeeLogs = {}
                        self.display_flactuation()
                    else:
                        if numberOfMimicDevicesON != 0 or numberOfMimicDevicesONZigbee != 0:
                            self.report_fail('Mimic device turned On outside of fuzzy window')
                        else:
                            self.report_pass(
                                'All the mimic devices are in OFF state ')
                        self.fluctuationZigbeeLogs = {}
                        self.display_flactuation(0)
                        if datetime.now() > self.fuzzyMaxEndTimeForAll: self.fuzzyLogic(context.lstTargetTime,
                                                                                        nextDay=True)

                    log = self.generatelog(self.zigbeeStatus, context.oMimicEP.devicesDict)
                    self.report_pass(log)
                    time.sleep(150)
                    dtmNow = datetime.now()
                    if not context.reporter.ActionStatus or not self.reporter.ActionStatus:
                        self.Thread = False
                        break

                self.Thread = False
                self.Zigebeethread.join()
        except:
            self.report_fail('Mimic Logic : Exception: in validationCycle Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def getNumberOfMimicDevicesOn(self, context):
        # Should be generic later - AnujComments
        count, allMimicDevicesDict, nonMimicDevicesDict = None, None, None
        try:
            if self.reporter.ActionStatus:
                mimicDevices = self.mimicDevices
                context.oMimicEP.updateMimic()
                currentDevicesStatus = context.oMimicEP.devicesDict
                # /Should be generic later

                count = 0
                allMimicDevicesDict, nonMimicDevicesDict = {}, {}
                for eachdevice in currentDevicesStatus.keys():
                    state = currentDevicesStatus[eachdevice]['deviceState']
                    if eachdevice in mimicDevices:
                        if state == 'ON':
                            count += 1
                        dict = {eachdevice: state}
                        allMimicDevicesDict.update(dict)
                    else:
                        dict = {eachdevice: state}
                        nonMimicDevicesDict.update(dict)
        except:
            self.report_fail('Mimic Logic : Exception: in getNumberOfMimicDevicesOn Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

        return count, allMimicDevicesDict, nonMimicDevicesDict

    def fetchTriggerTime(self, context, triggerState):
        # Should be generic later - AnujComments
        blntrigger = False
        try:
            if self.reporter.ActionStatus:
                mimicDevices = self.mimicDevices
                context.oMimicEP.updateMimic()
                currentDevicesStatus = context.oMimicEP.devicesDict
                # /Should be generic later
                count = 0

                triggeredDevices = {}
                if triggerState == 'ON':
                    endlooptime = self.fuzzyMaxStartTime
                    mintriggertime = self.fuzzyMinStartTime
                else:
                    endlooptime = self.fuzzyMaxEndTime
                    mintriggertime = self.fuzzyMinEndTime
                # Get UTC value - AnujComments
                blntrigger = False
                startLoopTime = mintriggertime
                while startLoopTime < endlooptime + timedelta(seconds=60) and not blntrigger:
                    allMimicDevicesDict, nonMimicDevicesDict = {}, {}
                    # considering all the mimic Devices working as expected
                    for eachdevice in currentDevicesStatus.keys():
                        state = currentDevicesStatus[eachdevice]['deviceState']
                        dict = {eachdevice: state}
                        if eachdevice in mimicDevices:
                            if state == triggerState:
                                triggeredDevices.update({eachdevice: state})
                                triggerTime = currentDevicesStatus[eachdevice]['triggerTime']
                                self.report_pass(
                                    'First Light ' + eachdevice + ' switched ' + triggerState + ' at ' + triggerTime.strftime(
                                        '%T'))
                                mintriggertime = triggerTime
                                self.triggeredDevice = eachdevice
                                blntrigger = True
                            allMimicDevicesDict.update(dict)
                        else:
                            nonMimicDevicesDict.update(dict)
                        if blntrigger: break

                    time.sleep(60)
                    if not blntrigger:
                        self.report_pass('No Light turned On between -' + startLoopTime.strftime('%T') +
                                         ' and ' + datetime.now().strftime('%T'))

                    startLoopTime = datetime.now()
                    self.allMimicDevicesDict = allMimicDevicesDict
                    self.nonMimicDevicesDict = nonMimicDevicesDict
                    context.oMimicEP.updateMimic()
                    currentDevicesStatus = context.oMimicEP.devicesDict
                    self.getLightsStatus()
                    log = self.generatelog(self.zigbeeStatus, context.oMimicEP.devicesDict)
                    self.report_pass(log)

                if blntrigger:
                    if triggerState == 'ON':
                        self.fuzzyMaxStartTime = mintriggertime
                        self.fuzzyMaxStartTimeForAll = mintriggertime + timedelta(minutes=15)
                    else:
                        self.fuzzyMaxEndTime = mintriggertime
                        self.fuzzyMaxEndTimeForAll = mintriggertime + timedelta(minutes=15)

        except:
            self.report_fail('Mimic Logic : Exception: in fetchTriggerTime Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

        return blntrigger

    def allMimicDevicesUpdated(self, context, triggerState):
        # Should be generic later - AnujComments
        try:
            if self.reporter.ActionStatus:
                context.oMimicEP.updateMimic()
                mimicDevices = self.mimicDevices
                currentDevicesStatus = context.oMimicEP.devicesDict
                # Get UTC value - AnujComments
                triggeredDevices = self.triggeredDevices
                fluctuationDict = {}
                allMimicDevicesDict, nonMimicDevicesDict = {}, {}
                # considering all the mimic Devices working as expected
                if triggerState == 'ON':
                    endlooptime = self.fuzzyMaxStartTimeForAll
                    mintriggertime = self.fuzzyMaxStartTime
                else:
                    endlooptime = self.fuzzyMaxEndTimeForAll
                    mintriggertime = self.fuzzyMaxEndTime
                startLoopTime = mintriggertime
                while startLoopTime < endlooptime + timedelta(seconds=60) and not self.TriggeredAll:
                    for eachdevice in currentDevicesStatus.keys():
                        state = currentDevicesStatus[eachdevice]['deviceState']
                        triggertime = currentDevicesStatus[eachdevice]['triggerTime']
                        dict = {eachdevice: state}
                        if eachdevice in mimicDevices:
                            if eachdevice in triggeredDevices.keys():
                                prevState = triggeredDevices[eachdevice]
                                if state != prevState:
                                    fluctuationDict.update(
                                        {eachdevice: {'fluctuation at API': prevState + ' to ' + state,
                                                      'triggertime': triggertime}})
                                    triggeredDevices.pop(eachdevice)
                            else:
                                if state == triggerState:
                                    triggeredDevices.update(dict)
                                    self.report_pass(
                                        'Light ' + eachdevice + ' switched ' + triggerState + ' at ' + triggertime.strftime(
                                            '%T'))
                                if len(triggeredDevices.keys()) == len(mimicDevices):
                                    self.TriggeredAll = True
                            allMimicDevicesDict.update(dict)
                        else:
                            nonMimicDevicesDict.update(dict)

                        self.allMimicDevicesDict = allMimicDevicesDict
                        self.nonMimicDevicesDict = nonMimicDevicesDict
                        context.oMimicEP.updateMimic()
                        currentDevicesStatus = context.oMimicEP.devicesDict
                        self.triggeredDevices = triggeredDevices
                        self.fluctuationLogs = fluctuationDict
                        self.getLightsStatus()
                        log = self.generatelog(self.zigbeeStatus, context.oMimicEP.devicesDict)
                        self.report_pass(log)
                    time.sleep(60)

                if self.TriggeredAll:
                    return True
                else:
                    return False
        except:
            self.report_fail('Mimic Logic : Exception: in allMimicDevicesUpdated Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def setNodes(self, devicesDict):
        try:
            if self.reporter.ActionStatus:
                for eachDevice in devicesDict.keys():
                    nodeID = devicesDict[eachDevice]['nativeIdentifier']
                    node = {eachDevice: nodeID}
                    self.nodes.update(node)
        except:
            self.report_fail('Mimic Logic : Exception: in setNodes Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def zigbeeThread(self):
        try:
            if self.reporter.ActionStatus:
                AT.stopThread.clear()
                AT.startSerialThreads(config.PORT, config.BAUD, AT.debug, True, False)
                self.Zigebeethread = Thread(target=self.get_attributes, args=(10,))
                self.Zigebeethread.start()
        except:
            self.report_fail('Mimic Logic : Exception: in zigbeeThread Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def get_attributes(self, arg):
        if self.reporter.ActionStatus:
            if not self.createlogfile():
                return
            dict = self.dict
            while self.Thread:
                jsonFile = open(self.logsPath, "r+")
                data = json.load(jsonFile)
                newdata = {}
                dtmNow = datetime.now().strftime("%d %b %Y %H:%M:%S")

                try:
                    for eachnode in self.nodes.keys():
                        respState, respCode, respValue = utils.readAttribute("MANUFACTURER", self.nodes[eachnode], '01',
                                                                             0, "0006",
                                                                             "0000")
                        if self.nodes[eachnode] in data:
                            listData = data[self.nodes[eachnode]]['attributes']
                            oJsonDict = {"timestamp": dtmNow, "state": dict[respCode]}
                            listData.append(oJsonDict)
                            data[self.nodes[eachnode]]['attributes'] = listData
                        newdata = data

                    jsonFile.seek(0)
                    jsonFile.write(json.dumps(newdata))
                    jsonFile.truncate()
                    jsonFile.seek(0)
                    jsonFile.close()
                    time.sleep(30)
                except:

                    self.report_fail('Error Response from device \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))
                    self.Thread = False

    def createlogfile(self):
        if self.reporter.ActionStatus:
            self.logsPath = os.path.abspath(self.reporter.strCurrentResFolder + '/ZigbeeLogs.json')
            oLJson = open(self.logsPath, mode='x')
            dict = self.dict
            newdata = {}
            try:
                for eachNode in self.nodes.keys():
                    dtmNow = datetime.now().strftime("%d %b %Y %H:%M:%S")
                    respState, respCode, respValue = utils.readAttribute("MANUFACTURER", self.nodes[eachNode], '01', 0,
                                                                         "0006",
                                                                         "0000")
                    lightNode = {self.nodes[eachNode]: {"attributes": [{"timestamp": dtmNow, "state": dict[respCode]}]}}
                    newdata.update(lightNode)
                oLJson.write(json.dumps(newdata))
                oLJson.close()
                return True
            except:
                self.report_fail('Error Response from device \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
                self.Thread = False
                return False

    def readlogFile(self):
        try:
            if self.reporter.ActionStatus:
                self.logsPath = os.path.abspath(self.reporter.strCurrentResFolder + '/ZigbeeLogs.json')
                strJson = open(self.logsPath, mode='r')
                self.DeviceLogs = json.loads(strJson.read())
                # with open(self.logsPath) as jsonfile:
                #   self.DeviceLogs = jsonfile.read()
                strJson.close()

        except:
            self.report_fail('Mimic Logic : Exception: in readlogFile Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def getLightsStatus(self):
        try:
            if self.reporter.ActionStatus:
                self.readlogFile()
                self.zigbeeStatus = {}
                for eachNode in self.DeviceLogs:
                    values = self.DeviceLogs[eachNode]['attributes']
                    currentValue = values[len(values) - 1]['state']
                    deviceNode = {eachNode: currentValue}
                    self.zigbeeStatus.update(deviceNode)
        except:
            self.report_fail('Mimic Logic : Exception: in getLightsStatus Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def numberOfMimicDevicesONusingZigbee(self):
        intCount, devicesDict, nonMimicDevicesDict = None, None, None
        try:
            if self.reporter.ActionStatus:
                intCount = 0
                devicesDict = {}
                nonMimicDevicesDict = {}
                for eachNode in self.nodes:
                    nodeID = self.nodes[eachNode]
                    status = self.zigbeeStatus[nodeID]
                    if eachNode in self.mimicDevices:
                        if status == 'ON':
                            intCount += 1
                        devicesDict.update({eachNode: status})
                    else:
                        nonMimicDevicesDict.update({eachNode: status})
        except:
            self.report_fail('Mimic Logic : Exception: in numberOfMimicDevicesONusingZigbee Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

        return intCount, devicesDict, nonMimicDevicesDict

    def validateSingleDevice(self, triggeredDevicestate):
        try:
            if self.reporter.ActionStatus:
                self.getLightsStatus()
                mimicDevices = self.mimicDevices
                mimicNodes = []
                for eachMimicDevice in mimicDevices:
                    mimicNodes.append(self.nodes[eachMimicDevice])
                blntriggerdFlag = False
                blnFlag = True
                nodeID = self.nodes[self.triggeredDevice]
                for eachnode in self.zigbeeStatus:
                    currentValue = self.zigbeeStatus[eachnode]
                    if nodeID == eachnode:
                        if currentValue == triggeredDevicestate:
                            blntriggerdFlag = True
                    else:
                        if currentValue == triggeredDevicestate and eachnode in mimicNodes:
                            blnFlag = False
                if blnFlag and blntriggerdFlag:
                    return True
                else:
                    return False
        except:
            self.report_fail('Mimic Logic : Exception: in validateSingleDevice Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def validateAllDevices(self, triggeredDevicestate):
        try:
            if self.reporter.ActionStatus:
                self.getLightsStatus()
                blntriggerdFlag = True
                mimicDevices = self.mimicDevices
                mimicNodes = []
                for eachMimicDevice in mimicDevices:
                    mimicNodes.append(self.nodes[eachMimicDevice])
                for eachnode in self.mimicDevices:
                    nodeID = self.nodes[eachnode]
                    if nodeID in self.zigbeeStatus:
                        currentValue = self.zigbeeStatus[nodeID]
                        if currentValue != triggeredDevicestate and eachnode in mimicNodes:
                            blntriggerdFlag = False
                    else:
                        blntriggerdFlag = False
                        self.report_fail('Node ID - ' + nodeID + ' is not found in logs')
                if blntriggerdFlag:
                    return True
                else:
                    return False
        except:
            self.report_fail('Mimic Logic : Exception: in validateAllDevices Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def getFlactuation(self):
        try:
            if self.reporter.ActionStatus:
                self.readlogFile()
                self.fluctuationZigbeeLogs = {}
                values = self.initialCounter
                for eachnode in self.mimicDevices:
                    nodeID = self.nodes[eachnode]
                    eachNodeDict = {eachnode: []}
                    if nodeID in self.DeviceLogs:
                        values = self.DeviceLogs[nodeID]['attributes']
                        blnFlag = True
                        for intCount in range(self.initialCounter, len(values)):
                            prevValue = values[intCount - 1]['state']
                            currentValue = values[intCount]['state']
                            triggertime = values[intCount]['timestamp']
                            if currentValue != prevValue:
                                lst = eachNodeDict[eachnode]
                                lst.append({'timestamp': triggertime, 'fluctuation': prevValue + ' to ' + currentValue})
                                eachNodeDict[eachnode] = lst

                        self.fluctuationZigbeeLogs.update(eachNodeDict)
                self.initialCounter = len(values)
        except:
            self.report_fail('Mimic Logic : Exception: in getFlactuation Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def display_flactuation(self, expectedCount=1):
        try:
            if self.reporter.ActionStatus:
                self.getFlactuation()
                fluctuationLogs = self.fluctuationZigbeeLogs

                for eachNode in fluctuationLogs:
                    if len(fluctuationLogs[eachNode]) > 1:
                        self.report_fail(
                            "Zigbee Validation - Triggering pattern for device " + eachNode + " is not as expected")
                        for eachItem in fluctuationLogs[eachNode]:
                            self.report_fail("fluctuation - " + fluctuationLogs[eachNode][eachItem]['fluctuation'] +
                                             " at " + fluctuationLogs[eachNode][eachItem]['timestamp'])
                    else:
                        if len(fluctuationLogs[eachNode]) != expectedCount:
                            if expectedCount == 1:
                                self.report_fail(
                                    "Zigbee Validation - there is no event for device " + eachNode + " in Fuzzy Window ")
                            else:
                                self.report_fail(
                                    "Zigbee Validation - there is an event for device " + eachNode + " outside Fuzzy Window ")
        except:
            self.report_fail('Mimic Logic : Exception: in display_flactuation Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def logCreation(self, actualAttributes, expectedAttributes):

        boolStatus = True
        try:
            if self.reporter.ActionStatus:
                for eachAttribute in actualAttributes.keys():
                    actualAttributeValue = actualAttributes[eachAttribute]
                    expectedAttributeValue = expectedAttributes[eachAttribute]
                    if actualAttributeValue == expectedAttributeValue:
                        actualAttributeValue = '$$' + actualAttributeValue
                    else:
                        actualAttributeValue = '$$||' + actualAttributeValue
                        boolStatus = False
                    actualAttributes.update({eachAttribute: actualAttributeValue})
                if boolStatus:
                    strHeader = 'Attributes$$ Expected values and Actual values@@@'
                    for eachAttribute in actualAttributes.keys():
                        actualAttributes.update({eachAttribute: ''})
                    strStatus = "PASS"
                else:
                    strHeader = 'Attributes$$ Expected values$$ Actual values@@@'
                    strStatus = "FAIL"
                resultstr = strHeader
                for eachAttribute in expectedAttributes.keys():
                    actualAttributeValue = actualAttributes[eachAttribute]
                    expectedAttributeValue = expectedAttributes[eachAttribute]
                    resultstr += eachAttribute + '$$' + expectedAttributeValue + actualAttributeValue + '$~'

                return resultstr[:-2], strStatus
        except:
            self.report_fail('Mimic Logic : Exception: in logCreation Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))
            return None, None

    def generatelog(self, zigBeeDict, APIDict, triggerStatus=None):
        strLog = None
        try:
            if self.reporter.ActionStatus:
                strLog = 'Light Name$$MIMIC Status$$ Status at Zigbee$$Status at API@@@'
                for eachItem in APIDict:
                    if eachItem in self.mimicDevices:
                        mimicStatus = 'ACTIVE'
                    else:
                        mimicStatus = 'INACTIVE'
                    zigBeeStatus = zigBeeDict[APIDict[eachItem]['nativeIdentifier']]
                    APIStatus = APIDict[eachItem]['deviceState']
                    if triggerStatus is not None:
                        if zigBeeStatus != triggerStatus: zigBeeStatus = '||' + zigBeeStatus
                        if APIStatus != triggerStatus: APIStatus = '||' + APIStatus
                    strLog += eachItem + '$$' + mimicStatus + '$$' + zigBeeStatus + '$$' + APIStatus + '$~'
        except:
            self.report_fail('Mimic Logic : Exception: in generatelog Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

        return strLog

    def updateMimicExpected(self, context):
        updatelightsStatus = None
        try:
            if self.reporter.ActionStatus:
                lightsState = context.targetlightsState
                lightsConfig = context.targetlightsConfig
                expectedMimicLightsStatus = context.InitialMimicStateForAllLights
                expectedMimicLightsText = context.InitialMimicTextForAllLights
                updatelightsStatus = {}
                for eachlight in lightsConfig:
                    if lightsConfig[eachlight] == 'true':
                        updatelightsStatus.update({eachlight: {'mimicStatus': 'ACTIVE', 'textStatus':
                            expectedMimicLightsText, 'IconStatus': expectedMimicLightsStatus}})
                    else:
                        expectedState = lightsState[eachlight]
                        updatelightsStatus.update({eachlight: {'mimicStatus':
                                                                   'INACTIVE', 'textStatus': expectedState,
                                                               'IconStatus': expectedState}})

        except:
            self.report_fail('Mimic Logic : Exception: in updateMimicExpected Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

        return {'Target Values': updatelightsStatus}

    def get_platform_dict(self, devicesDict):
        lights = {}
        try:
            if self.reporter.ActionStatus:
                dict = {True: 'ACTIVE', False: 'INACTIVE'}
                for eachlight in devicesDict:
                    CurrentDeviceState = devicesDict[eachlight]['deviceState']
                    mimicStatus = dict[devicesDict[eachlight]['mimic']]
                    lights.update({eachlight: {'mimicStatus': mimicStatus, 'IconStatus': CurrentDeviceState}})
        except:
            self.report_fail('Mimic Logic : Exception: in get_platform_dict Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

        return {'Platform Values': lights}
