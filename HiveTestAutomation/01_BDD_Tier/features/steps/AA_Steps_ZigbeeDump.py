"""
Created on 19 Aug 2016

@author: kingston.samselwyn
"""

from behave import *
import FF_utils as utils
import os
import FF_device_utils as dutils
import FF_threadedSerial as AT
import FF_zigbeeToolsConfig as config


@When(
    u'the zigbee dump for the {strDeviceType} is downloaded with the clusters and attributes list via telegesis stick')
def getZigbeeDump(context, strDeviceType):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Download the zigbee dump')
    try:
        AT.stopThreads()
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=False)
    except:
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=False)

    if context.table is not None:
        for oRow in context.table:
            myNodeId = ""
            if str(oRow['DeviceType']).upper() == "GENERIC":
                DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                # NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                oJson = dutils.getDeviceNode(DeviceName, False)
                MAcID = oJson['macID']
                DeviceType = oJson['name']
                myNodeId = oJson['nodeID']
            else:
                myNodeId = dutils.getDeviceNodeWithMAC(oRow['DeviceType'], oRow['MACID'])
    else:
        # _AT.setFastPoll()
        macId = dutils.getDeviceMACWithModel(strDeviceType, True)
        myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType, macId)
    # myNodeId = "333E"
    # Get Model & Device firmware

    context.nodeId = myNodeId
    model = utils.getDeviceModeId(myNodeId)
    deviceVersion = utils.getDeviceVersion(myNodeId)
    print(model + "-" + deviceVersion + "\n")

    baselineDumpFile = os.path.abspath(
        __file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/" + model + "_Baseline_Dump.json"
    if os.path.isfile(baselineDumpFile):
        utils.createBaselineDeviceAttrbDumpJson(myNodeId, False)
    else:
        utils.createBaselineDeviceAttrbDumpJson(myNodeId, True)
    latestDumpFile = os.path.abspath(
        __file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/Latest_Attribute_Dump/" + model + "_" + deviceVersion + "_Dump.json"
    utils.getJSONObjectFromFile(context, baselineDumpFile, latestDumpFile)


@then(u'the dump is validated against the corresponding baseline dump file.')
def validateZigbeeDump(context):
    # myNodeId = "333E"
    # Get Model & Device firmware
    myNodeId = context.nodeId
    model = utils.getDeviceModeId(myNodeId)
    deviceVersion = utils.getDeviceVersion(myNodeId)
    print(model + "-" + deviceVersion + "\n")

    baselineDumpFile = os.path.abspath(
        __file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/" + model + "_Baseline_Dump.json"
    latestDumpFile = os.path.abspath(
        __file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/Latest_Attribute_Dump/" + model + "_" + deviceVersion + "_Dump.json"
    reporter = context.reporter
    oBSDumpJson, oLatestDumpJson = utils.validateDumpJsonAndReport(context, reporter, baselineDumpFile, latestDumpFile)
    context.BaseDumpJson = oBSDumpJson
    context.TestDumpJson = oLatestDumpJson
    utils.validateDumpJsonAndReport(context, reporter, latestDumpFile, baselineDumpFile)


@When(
    u'the zigbee dump for dfdsf the selected device is downloaded with the clusters and attributes list via telegesis stick')
def getZigbeeDumpForSelectedDevice(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Download the zigbee dump')
    oJson = dutils.getZigbeeDevicesJson()
    strDeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
    myNodeId = utils.getAttribute("COMMON", "mainClient", None, None)
    # myNodeId = "333E"
    # Get Model & Device firmware
    context.nodeId = myNodeId
    model = utils.getDeviceModeId(myNodeId)
    deviceVersion = utils.getDeviceVersion(myNodeId)
    print(model + "-" + deviceVersion + "\n")

    baselineDumpFile = os.path.abspath(
        __file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/" + model + "_Baseline_Dump.json"
    if os.path.isfile(baselineDumpFile):
        utils.createBaselineDeviceAttrbDumpJson(myNodeId, False)
    else:
        utils.createBaselineDeviceAttrbDumpJson(myNodeId, True)
    latestDumpFile = os.path.abspath(
        __file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/Latest_Attribute_Dump/" + model + "_" + deviceVersion + "_Dump.json"
    utils.getJSONObjectFromFile(context, baselineDumpFile, latestDumpFile)


@then(u'the dump is validated against the corresponding baseline dump file for the selected device.')
def validateZigbeeDumpForSelectedDevice(context):
    # oJson = dutils.getZigbeeDevicesJson()
    strDeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
    myNodeId = utils.getAttribute("COMMON", "mainClient", None, None)
    # Get Model & Device firmware
    model = utils.getDeviceModeId(myNodeId)
    deviceVersion = utils.getDeviceVersion(myNodeId)
    print(model + "-" + deviceVersion + "\n")

    baselineDumpFile = os.path.abspath(
        __file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/" + model + "_Baseline_Dump.json"
    latestDumpFile = os.path.abspath(
        __file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/Latest_Attribute_Dump/" + model + "_" + deviceVersion + "_Dump.json"
    reporter = context.reporter
    oBSDumpJson, oLatestDumpJson = utils.validateDumpJsonAndReport(context, reporter, baselineDumpFile, latestDumpFile)
    context.BaseDumpJson = oBSDumpJson
    context.TestDumpJson = oLatestDumpJson
    utils.validateDumpJsonAndReport(context, reporter, latestDumpFile, baselineDumpFile)
