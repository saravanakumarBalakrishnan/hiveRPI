"""
Created on 6 Jan 2016

@author: ranganathan.veluswamy
"""
from datetime import timedelta
import time
from behave import *
import CC_thermostatModule as st
import FF_alertmeApi as ALAPI
import FF_threadedSerial as AT
import FF_utils as utils
import FF_device_utils as dutils
import AA_Steps_SmartPlug as SP
import FF_zigbeeToolsConfig as config


@given(u'The telegesis is paired with given {strDeviceType}')
def pair_given_devices(context, strDeviceType):
    try:
        AT.stopThreads()
    except:
        print("Thread check Already Stopped")

    dutils.putZigbeeDevicesJson(dutils.getNodes(False))
    oNodes = dutils.getZigbeeDevicesJson()
    strLog = "Device $$ Mac Address @@@"
    for oNode in oNodes:
        strLog = strLog + "$~" + oNode + "$$" + oNodes[oNode]["macID"]
    context.reporter.ReportEvent("Event Log", strLog, "Done")
    try:
        AT.stopThreads()
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
    except:
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)

    if "HEATING" in str(strDeviceType).upper() or "WATER" in str(strDeviceType).upper():
        AT.startAttributeListener(printStatus=False)
        context.nodes = utils.getNodes()
        print(context.nodes, 'context.nodes')
        reporter = context.reporter
        reporter.strNodeID = context.nodes['BM']
        config.node1 = context.nodes['BM']
        AT.getInitialData(reporter.strNodeID, fastPoll=False, printStatus=False)
        # Instantiate ThermostatEndpoint class
        oThermostatClass = st.thermostatClass(context.reporter.strNodeID)
        context.oThermostatClass = oThermostatClass
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('List of Devices Paired')
    '''respState, nTable, rows = utils.getNtable("FF")
    strNtableHeader = 'No.' +"$$" + 'Dev' +"$$" + 'EUI' +"$$" + 'NodeID' +"$$" + 'LQI'  + '@@@'
    strNtableBody = ""
    intIndex = 0
    
    for oRow in range(3, len(rows)):
        print(oRow)
        arrCell = rows[oRow].split("|")
        strNtableBody = strNtableBody + str(intIndex) + "." +"$$" +  arrCell[1].strip() +"$$" +  arrCell[2].strip() +"$$" +  arrCell[3].strip() +"$$" + arrCell[4].strip() + "$~"
        intIndex = intIndex + 1
    context.reporter.ReportEvent("Test Validation", strNtableHeader + strNtableBody, "PASS", "CENTER")'''


@given(u'The {strDeviceType} is plugged in to the port for Factory Test')
def enableFactoryTest(context, strDeviceType):
    if 'BUTTON' in str(strDeviceType).upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Button Factory Test Enabled')


@then(u'the below devices are paired and unpaired sequentially and validated {strCount} via Telegesis')
def pair_unpair_devices(context, strCount):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    intLoopCtr = 1
    # strCount = ""
    if str(strCount).upper() == "INFINITELY":
        intLoopCtr = 1
    else:
        strCount = strCount.replace(" times", "")
        intLoopCtr = int(strCount)

    flag = True
    while flag:
        for intIter in range(0, intLoopCtr):
            intCntr = intCntr + 1
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
            MAcID = ""
            for oRow in context.table:
                NodeID = ""
                DeviceType = ""
                if str(oRow['DeviceType']).upper() == "GENERIC":
                    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                    # NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                    oJson = dutils.getDeviceNode(DeviceName, False)
                    MAcID = oJson['macID']
                    DeviceType = oJson['name']
                    NodeID = oJson['nodeID']
                else:
                    DeviceName = oRow['DeviceName']
                    DeviceType = oRow['DeviceType']
                    MAcID = oRow['MacID']
                    NodeID = utils.get_device_node_from_ntable(MAcID)

                print(DeviceName, DeviceType, NodeID, MAcID, "\n")
                # Unpair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ')

                context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
                context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")

                utils.remove_device_from_network(NodeID)
                time.sleep(30)
                '''time.sleep(5)
                utils.setSPOnOff("DAF8", "OFF")
                time.sleep(2)
                utils.setSPOnOff("DAF8", "ON")
                time.sleep(5)'''

                # Pair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
                print(utils.getTimeStamp(False), "Join Device to the network")
                intStartTime = time.time()
                intTCStartTime = time.monotonic()
                respState, respCode, resp = utils.check_device_joined(MAcID, "FFD", "1E")
                print("respState", respState)
                if respState:
                    intPassCntr = intPassCntr + 1
                    myNodeID = resp
                    time.sleep(60)
                    if str(oRow['DeviceType']).upper() == "GENERIC":
                        oNodeJson = dutils.getZigbeeDevicesJson()
                        oNodeJson[DeviceName]['nodeID'] = myNodeID
                        dutils.putZigbeeDevicesJson(oNodeJson)
                    context.reporter.ReportEvent("Test Validation",
                                                 "Device Joined the network with Node ID : <B>" + myNodeID + "</B>",
                                                 "PASS")
                    print("Device Joined the network with Node ID : ", myNodeID)
                else:
                    intFailCntr = intFailCntr + 1
                    context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                    print("join is unsuccessfull")
                    return False
                    '''print("Restarting the Smart Plug")
                    utils.setSPOnOff(NodeID, 'OFF')
                    time.sleep(5)
                    utils.setSPOnOff(NodeID, 'ON')
                    time.sleep(5)'''

                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
                if intSeconds > 20:
                    strStatus = "FAIL"
                else:
                    strStatus = "PASS"
                context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
                print("Time taken: ", strTCDuration)
                print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print()
                if str(strCount).upper() == "INFINITELY":
                    intIter = 1
                else:
                    if intIter == intLoopCtr - 1:
                        flag = False
                        break


@then(u'the below devices are unpaired via Telegesis')
def unpair_devices(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Device Removal')
    MAcID = ""
    NodeID = ""
    DeviceType = ""
    for oRow in context.table:
        DeviceName = oRow['DeviceName']
        DeviceType = oRow['DeviceType']
        MAcID = oRow['MacID']
        NodeID = utils.get_device_node_from_ntable(MAcID)

        print(DeviceName, DeviceType, NodeID, MAcID, "\n")

        # Unpair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ')

        context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
        context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")

        utils.remove_device_from_network(NodeID)
        time.sleep(30)


@then(u'the below devices are paired via Telegesis')
def pair_devices(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Device Removal')
    MAcID = ""
    NodeID = ""
    DeviceType = ""
    for oRow in context.table:

        DeviceName = oRow['DeviceName']
        DeviceType = oRow['DeviceType']
        MAcID = oRow['MacID']
        NodeID = utils.get_device_node_from_ntable(MAcID)

        print(DeviceName, DeviceType, NodeID, MAcID, "\n")

        # Pair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
        print(utils.getTimeStamp(False), "Join Device to the network")
        intStartTime = time.time()
        intTCStartTime = time.monotonic()
        respState, respCode, resp = utils.check_device_joined(MAcID, "FFD", "1E")
        print("respState", respState)
        if respState:
            myNodeID = resp
            time.sleep(60)
            if str(oRow['DeviceType']).upper() == "GENERIC":
                oNodeJson = dutils.getZigbeeDevicesJson()
                oNodeJson[DeviceName]['nodeID'] = myNodeID
                dutils.putZigbeeDevicesJson(oNodeJson)
            context.reporter.ReportEvent("Test Validation",
                                         "Device Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
            print("Device Joined the network with Node ID : ", myNodeID)
        else:
            context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
            print("join is unsuccessfull")
            return False


@when(u'the selected devices are paired and unpaired sequentially and validated {intCount} times via Telegesis')
def pair_unpair_devices_specific_time(context, intCount):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    while intCntr < int(intCount):
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))

        NodeID = utils.getAttribute("COMMON", "mainClient", None, None)
        MAcID = utils.getAttribute("COMMON", "macID", None, None)

        # NodeID = utils.get_device_node_from_ntable(MAcID)
        # print(DeviceName, DeviceType, NodeID, MAcID, "\n")
        # Unpair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ')

        context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
        context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")

        utils.remove_device_from_network(NodeID)
        time.sleep(30)
        '''time.sleep(5)
        utils.setSPOnOff("DAF8", "OFF")
        time.sleep(2)
        utils.setSPOnOff("DAF8", "ON")
        time.sleep(5)'''

        # Pair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
        print(utils.getTimeStamp(False), "Join Device to the network")
        intStartTime = time.time()
        intTCStartTime = time.monotonic()

        respState, respCode, resp = utils.check_device_joined(MAcID, "FFD", "1E")
        print("respState", respState)
        if respState:
            intPassCntr = intPassCntr + 1
            myNodeID = resp
            utils.setAttribute("COMMON", "mainClient", myNodeID)
            context.reporter.ReportEvent("Test Validation",
                                         "Device Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
            print("Device Joined the network with Node ID : ", myNodeID)
            time.sleep(60)
        else:
            intFailCntr = intFailCntr + 1
            context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
            print("join is unsuccessfull")
            return False
            '''print("Restarting the Smart Plug")
            utils.setSPOnOff(NodeID, 'OFF')
            time.sleep(5)
            utils.setSPOnOff(NodeID, 'ON')
            time.sleep(5)'''

        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
        if intSeconds > 20:
            strStatus = "FAIL"
        else:
            strStatus = "PASS"
        context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
        print("Time taken: ", strTCDuration)
        print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print()


USDevicesList = {"SLP2C", "SLB3", "SLB2C", "SLT4"}


@when(
    u'the below devices are paired and unpaired sequentially on all Zigbee Channels and validated{strDuration}via Telegesis')
def pair_unpair_devices_on_all_channels(context, strDuration):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    ZigbeeChannelList = []

    for intChannel in range(11, 27):
        ZigbeeChannelList.append(intChannel)
    intTotalChannel = len(ZigbeeChannelList)

    intLoopCtr = 0
    flag = True
    while flag:
        intCntr = intCntr + 1
        MAcID = ""
        # Get new Channel number
        channelIndex = intCntr % intTotalChannel
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
        for oRow in context.table:
            DeviceType = ""
            NodeID = ""
            if str(oRow['DeviceType']).upper() == "GENERIC":
                DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                # NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                oJson = dutils.getDeviceNode(DeviceName, False)
                MAcID = oJson['macID']
                DeviceType = oJson['name']
                NodeID = oJson['nodeID']
            else:
                DeviceName = oRow['DeviceName']
                DeviceType = oRow['DeviceType']
                MAcID = oRow['MacID']
                NodeID = utils.get_device_node_from_ntable(MAcID)
            print(DeviceName, DeviceType, NodeID, MAcID, "\n")

            # Unpair the Device from Telegesis
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ')

            context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
            context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")

            if "TH" in DeviceName.upper():
                utils.remove_device_from_network(NodeID, 2)
                time.sleep(2)
                bmMacID = oRow['BMMacID']
                bmNodeID = utils.get_device_node_from_ntable(bmMacID)
                # Unpair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the BM from Telegesis: ')
                context.reporter.ReportEvent("Test Validation", "BM NodeID : <B>" + bmNodeID + "</B>", "Done")
                context.reporter.ReportEvent("Test Validation", "BM MAcID : <B>" + bmMacID + "</B>", "Done")
                utils.remove_device_from_network(bmNodeID)
                time.sleep(2)
                plugMacID = oRow['plugMacID']
                plugNodeID = utils.get_device_node_from_ntable(plugMacID)
                utils.setSPOnOff(plugNodeID, "OFF")
                utils.remove_device_from_network(plugNodeID)
                time.sleep(2)
            else:
                utils.remove_device_from_network(NodeID)
                time.sleep(2)
            '''time.sleep(5)
            utils.setSPOnOff("DAF8", "OFF")
            time.sleep(2)
            utils.setSPOnOff("DAF8", "ON")
            time.sleep(5)'''

            # Reset Telegesis to a new channel
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Reset Telegesis to a new channel')
            utils.disassociate_from_pan()

            # Establish Network on new channel
            context.reporter.ReportEvent("Test Validation", "Establish Network on the Channel : <B>" + str(
                ZigbeeChannelList[channelIndex]) + "</B>", "PASS")
            utils.establish_network(ZigbeeChannelList[channelIndex])

            # Pair the Device from Telegesis
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
            print(utils.getTimeStamp(False), "Join Device to the network")
            intStartTime = time.time()
            intTCStartTime = time.monotonic()
            oDictSED = AT.oDictSED
            strDevType = ''
            if str(DeviceType).upper() in oDictSED:
                strDevType = 'SED'
            else:
                strDevType = 'FFD'
            respState, respCode, resp = utils.check_device_joined(MAcID, strDevType, "1E")
            print("respState", respState)
            boolJoined = respState
            if respState:
                if int(ZigbeeChannelList[channelIndex]) == 26 or int(ZigbeeChannelList[channelIndex]) == 25 and (
                            DeviceType.upper() in USDevicesList):
                    if DeviceType.upper() in USDevicesList:
                        context.reporter.ReportEvent("Test Validation",
                                                     "Device Joined the network with Node ID : <B>" + NodeID + "</B>",
                                                     "FAIL")
                        context.reporter.ReportEvent("Test Validation",
                                                     DeviceType.upper() + " should not pair in the channel" + str(
                                                         ZigbeeChannelList[channelIndex]), "FAIL")
                        intFailCntr = intFailCntr + 1
                else:
                    intPassCntr = intPassCntr + 1
                    context.reporter.ReportEvent("Test Validation",
                                                 "Device Joined the network with Node ID : <B>" + NodeID + "</B>",
                                                 "PASS")
                myNodeID = resp
                if str(oRow['DeviceType']).upper() == "GENERIC":
                    oNodeJson = dutils.getZigbeeDevicesJson()
                    oNodeJson[DeviceName]['nodeID'] = myNodeID
                    dutils.putZigbeeDevicesJson(oNodeJson)

                print("Device Joined the network with Node ID : ", myNodeID)
            else:
                if (int(ZigbeeChannelList[channelIndex]) == 26 or int(ZigbeeChannelList[channelIndex]) == 25) and (
                            DeviceType.upper() in USDevicesList):
                    context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "PASS")
                    context.reporter.ReportEvent("Test Validation",
                                                 DeviceType.upper() + " should pair in the channel" + str(
                                                     ZigbeeChannelList[channelIndex]), "PASS")
                    intPassCntr = intPassCntr + 1
                else:
                    intFailCntr = intFailCntr + 1
                    context.reporter.ReportEvent("Test Validation", "Join is unsuccessful", "FAIL")
                    print("join is unsuccessfull")
                    # return False
                '''print("Restarting the Smart Plug")
                utils.setSPOnOff(NodeID, 'OFF')
                time.sleep(5)
                utils.setSPOnOff(NodeID, 'ON')
                time.sleep(5)'''
            if "TH" in DeviceName.upper():
                plugMacID = oRow['plugMacID']
                plugNodeID = utils.get_device_node_from_ntable(plugMacID)
                if " " in plugNodeID:
                    respState, respCode, resp = utils.check_device_joined(plugMacID, "FFD", "1E")
                    if not respState:
                        context.reporter.ReportEvent("Test Validation", "plug did not pair", "Fail")
                        exit()
                    else:
                        plugNodeID = utils.get_device_node_from_ntable(plugMacID)
                utils.setSPOnOff(plugNodeID, "ON")
                bmMacID = oRow['BMMacID']
                strDevType = 'FFD'
                respState, respCode, resp = utils.check_device_joined(bmMacID, strDevType, "1E")
                print("respState", respState)
                boolJoined = respState
                if respState:
                    if int(ZigbeeChannelList[channelIndex]) == 26 or int(ZigbeeChannelList[channelIndex]) == 25 and (
                                DeviceType.upper() in USDevicesList):
                        if DeviceType.upper() in USDevicesList:
                            context.reporter.ReportEvent("Test Validation",
                                                         "BM Joined the network with Node ID : <B>" + NodeID + "</B>",
                                                         "FAIL")
                            context.reporter.ReportEvent("Test Validation",
                                                         DeviceType.upper() + " should not pair in the channel" + str(
                                                             ZigbeeChannelList[channelIndex]), "FAIL")
                            intFailCntr = intFailCntr + 1
                    else:
                        intPassCntr = intPassCntr + 1
                        context.reporter.ReportEvent("Test Validation",
                                                     "Device Joined the network with Node ID : <B>" + NodeID + "</B>",
                                                     "PASS")
                    myNodeID = resp
                    if str(oRow['DeviceType']).upper() == "GENERIC":
                        oNodeJson = dutils.getZigbeeDevicesJson()
                        oNodeJson[DeviceName]['nodeID'] = myNodeID
                        dutils.putZigbeeDevicesJson(oNodeJson)

                    print("Device Joined the network with Node ID : ", myNodeID)
                else:
                    if (int(ZigbeeChannelList[channelIndex]) == 26 or int(ZigbeeChannelList[channelIndex]) == 25) and (
                                DeviceType.upper() in USDevicesList):
                        context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "PASS")
                        context.reporter.ReportEvent("Test Validation",
                                                     DeviceType.upper() + " should pair in the channel" + str(
                                                         ZigbeeChannelList[channelIndex]), "PASS")
                        intPassCntr = intPassCntr + 1
                    else:
                        intFailCntr = intFailCntr + 1
                        context.reporter.ReportEvent("Test Validation", "Join is unsuccessful", "FAIL")
                        print("join is unsuccessfull")
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
            if intSeconds > 20:
                strStatus = "FAIL"
                if not boolJoined:
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize("Pairing in channel 11 for re-use")
                    # Reset Telegesis to a new channel
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Reset Telegesis to a new channel')

                    utils.disassociate_from_pan()

                    # Establish Network on new channel
                    context.reporter.ReportEvent("Test Validation", "Establish Network on the Channel : <B>11</B>",
                                                 "PASS")
                    utils.establish_network(11)

                    # Pair the Device from Telegesis
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
                    print(utils.getTimeStamp(False), "Join Device to the network")
                    intStartTime = time.time()
                    intTCStartTime = time.monotonic()

                    respState, respCode, resp = utils.check_device_joined(MAcID, strDevType, "1E")
                    if respState:
                        myNodeID = resp
                        context.reporter.ReportEvent("Test Validation", "Device paired for re-use in channel 11",
                                                     "DONE")
                    else:
                        context.reporter.ReportEvent("Test Validation", "Device did not pair in channel 11", "DONE")
                    if "TH" in DeviceName.upper():
                        bmMacID = oRow['BMMacID']
                        strDevType = 'FFD'
                        respState, respCode, resp = utils.check_device_joined(MAcID, strDevType, "1E")
                        if respState:
                            myNodeID = resp
                            context.reporter.ReportEvent("Test Validation", "BM paired for re-use in channel 11",
                                                         "DONE")
                        else:
                            context.reporter.ReportEvent("Test Validation", "BM did not pair in channel 11", "DONE")

            else:
                strStatus = "PASS"
            context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
            print("Time taken: ", strTCDuration)
            print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print()
            time.sleep(60)
            if strDuration.replace(" ", "") == "":
                intLoopCtr += 1
                if intLoopCtr > 15:
                    flag = False
                    break


@when(
    u'the selected device is paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis')
def pair_unpair_selected_device_on_all_channels(context):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    ZigbeeChannelList = []
    for intChannel in range(11, 27):
        ZigbeeChannelList.append(intChannel)
    intTotalChannel = len(ZigbeeChannelList)

    while True:
        intCntr = intCntr + 1

        # Get new Channel number
        channelIndex = intCntr % intTotalChannel
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
        NodeID = utils.getAttribute("COMMON", "mainClient", None, None)
        MAcID = utils.getAttribute("COMMON", "macID", None, None)

        # NodeID = utils.get_device_node_from_ntable(MAcID)

        # Unpair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ')

        context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
        context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")

        utils.remove_device_from_network(NodeID)
        time.sleep(2)
        '''time.sleep(5)
        utils.setSPOnOff("DAF8", "OFF")
        time.sleep(2)
        utils.setSPOnOff("DAF8", "ON")
        time.sleep(5)'''

        # Reset Telegesis to a new channel
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Reset Telegesis to a new channel')
        utils.disassociate_from_pan()

        # Establish Network on new channel
        context.reporter.ReportEvent("Test Validation", "Establish Network on the Channel : <B>" + str(
            ZigbeeChannelList[channelIndex]) + "</B>", "PASS")
        utils.establish_network(ZigbeeChannelList[channelIndex])

        # Pair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
        print(utils.getTimeStamp(False), "Join Device to the network")
        intStartTime = time.time()
        intTCStartTime = time.monotonic()

        respState, respCode, resp = utils.check_device_joined(MAcID, "FFD", "1E")
        print("respState", respState)
        if respState:
            intPassCntr = intPassCntr + 1
            myNodeID = resp
            utils.setAttribute("COMMON", "mainClient", myNodeID)
            context.reporter.ReportEvent("Test Validation",
                                         "Device Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
            print("Device Joined the network with Node ID : ", myNodeID)
        else:
            intFailCntr = intFailCntr + 1
            context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
            print("join is unsuccessfull")
            return False

        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
        if intSeconds > 20:
            strStatus = "FAIL"
        else:
            strStatus = "PASS"
        context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
        print("Time taken: ", strTCDuration)
        print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print()
        if intCntr >= 15:
            break
        time.sleep(60)


@when(u'the below devices are paired and unpaired sequentially and validated infinitely via {HubType} Hub')
def pair_unpair_devices_via_hub(context, HubType):
    HubType = HubType.upper().strip()
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
        for oRow in context.table:
            DeviceName = oRow['DeviceName']
            DeviceType = oRow['DeviceType']
            # HubType = oRow['HubType']
            # get node lists
            ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
            session = ALAPI.sessionObject()
            # nodeIdList = context.oThermostatEP.getNodeID(resp)
            nodeIdList = SP.getNodeAndDeviceVersionID()
            if DeviceType in nodeIdList:
                NodeID = nodeIdList[DeviceType]["nodeID"]
                print(DeviceName, DeviceType, NodeID, "\n")
                # Unpair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device ' + DeviceType + ' from HUb: ')

                context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")

                print(utils.getTimeStamp(False), "Sending Leave request for device")
                ALAPI.deleteDeviceV6(session, NodeID)
                print(utils.getTimeStamp(False), "Wait for 40 seconds")
                time.sleep(90)

            '''time.sleep(5)
            utils.setSPOnOff("DAF8", "OFF")
            time.sleep(2)
            utils.setSPOnOff("DAF8", "ON")
            time.sleep(5)'''

            # Pair the Device via Hub
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device ' + DeviceType + ' to Hub: ')
            print(utils.getTimeStamp(False), "Join Device to the network")
            ALAPI.setHubStateV6(session, nodeIdList[HubType]["nodeID"], "DISCOVERING")
            intStartTime = time.time()
            intTCStartTime = time.monotonic()

            boolPairStatus = False
            sleepTime = 0
            while True:
                # Validate if node is added the network
                nodeIdList = SP.getNodeAndDeviceVersionID()
                if DeviceType in nodeIdList:
                    boolPairStatus = True
                    break
                elif sleepTime > 250:
                    break
                time.sleep(30)
                sleepTime = sleepTime + 30

            ALAPI.setHubStateV6(session, nodeIdList[HubType]["nodeID"], "UP")
            ALAPI.deleteSessionV6(session)

            print("boolPairStatus", boolPairStatus)
            if boolPairStatus:
                intPassCntr = intPassCntr + 1
                myNodeID = nodeIdList[DeviceType]["nodeID"]

                context.reporter.ReportEvent("Test Validation",
                                             "Device " + DeviceType + " Joined the network with Node ID : <B>" + myNodeID + "</B>",
                                             "PASS")
                print("Device Joined the network with Node ID : ", myNodeID)
            else:
                intFailCntr = intFailCntr + 1
                context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                print("join is unsuccessfull")
                return False
                '''print("Restarting the Smart Plug")
                utils.setSPOnOff(NodeID, 'OFF')
                time.sleep(5)
                utils.setSPOnOff(NodeID, 'ON')
                time.sleep(5)'''

            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
            intMin = int(strTCDuration.split(",")[0].strip().split(" ")[0])
            intSeconds = intMin * 60 + intSeconds
            if intSeconds > 60:
                strStatus = "FAIL"
            else:
                strStatus = "PASS"
            context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
            print("Time taken: ", strTCDuration)
            print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print()
            time.sleep(180)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


@step("the telegesis stick is in pairing mode until below device is found")
def pair_until_device_found(context):
    MACID = ""
    DeviceType = ""
    for oRow in context.table:
        MACID = oRow["MacID"]
        DeviceType = oRow["DeviceType"]
    while True:
        respState, respCode, resp = utils.check_device_joined(MACID, DeviceType, "FF")
        print("respState", respState)
        if respState:
            myNodeID = resp
            context.reporter.ReportEvent("Test Validation",
                                         "Device Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
            print("Device Joined the network with Node ID : ", myNodeID)
        else:
            context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
    time.sleep(300)


@when("the below devices are paired and unpaired sequentially and validated {strCount} via Telegesis")
def pair_unpair_for_period(context, strCount):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    intLoopCtr = 1
    # strCount = ""
    if str(strCount).upper() == "INFINITELY":
        intLoopCtr = 1
    else:
        strCount = strCount.replace(" times", "")
        intLoopCtr = int(strCount)

    flag = True
    while flag:
        for intIter in range(0, intLoopCtr):
            intCntr = intCntr + 1
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
            MAcID = ""
            for oRow in context.table:
                NodeID = ""
                DeviceType = ""
                if str(oRow['DeviceType']).upper() == "GENERIC":
                    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                    # NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                    oJson = dutils.getDeviceNode(DeviceName, False)
                    MAcID = oJson['macID']
                    DeviceType = oJson['name']
                    NodeID = oJson['nodeID']
                else:
                    DeviceName = oRow['DeviceName']
                    DeviceType = oRow['DeviceType']
                    MAcID = oRow['MacID']
                    NodeID = utils.get_device_node_from_ntable(MAcID)

                print(DeviceName, DeviceType, NodeID, MAcID, "\n")
                # Unpair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ')

                context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
                context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")

                if "TH" in DeviceName.upper():
                    utils.remove_device_from_network(NodeID, 2)
                    time.sleep(2)
                    bmMacID = oRow['BMMacID']
                    bmNodeID = utils.get_device_node_from_ntable(bmMacID)
                    # Unpair the Device from Telegesis
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the BM from Telegesis: ')
                    context.reporter.ReportEvent("Test Validation", "BM NodeID : <B>" + bmNodeID + "</B>", "Done")
                    context.reporter.ReportEvent("Test Validation", "BM MAcID : <B>" + bmMacID + "</B>", "Done")
                    utils.remove_device_from_network(bmNodeID)
                    time.sleep(2)
                    plugMacID = oRow['plugMacID']
                    plugNodeID = utils.get_device_node_from_ntable(plugMacID)
                    utils.setSPOnOff(plugNodeID, "OFF")
                    time.sleep(2)
                else:
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the device from Telegesis: ')
                    utils.remove_device_from_network(NodeID, 2)
                    time.sleep(2)

                '''time.sleep(5)
                utils.setSPOnOff("DAF8", "OFF")
                time.sleep(2)
                utils.setSPOnOff("DAF8", "ON")
                time.sleep(5)'''

                # Pair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
                print(utils.getTimeStamp(False), "Join Device to the network")
                intStartTime = time.time()
                intTCStartTime = time.monotonic()
                oDictSED = AT.oDictSED
                strDevType = ''
                if str(DeviceType).upper() in oDictSED:
                    strDevType = 'SED'
                else:
                    strDevType = 'FFD'
                respState, respCode, resp = utils.check_device_joined(MAcID, strDevType, "1E")
                print("respState", respState)

                if respState:
                    intPassCntr = intPassCntr + 1
                    myNodeID = resp
                    context.nodeId = myNodeID
                    time.sleep(240)
                    if str(oRow['DeviceType']).upper() == "GENERIC":
                        oNodeJson = dutils.getZigbeeDevicesJson()
                        oNodeJson[DeviceName]['nodeID'] = myNodeID
                        dutils.putZigbeeDevicesJson(oNodeJson)
                    context.reporter.ReportEvent("Test Validation",
                                                 "Device Joined the network with Node ID : <B>" + myNodeID + "</B>",
                                                 "PASS")
                    print("Device Joined the network with Node ID : ", myNodeID)
                else:
                    intFailCntr = intFailCntr + 1
                    context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                    print("join is unsuccessfull")
                    return False

                if "TH" in DeviceName.upper():
                    plugMacID = oRow['plugMacID']
                    plugNodeID = utils.get_device_node_from_ntable(plugMacID)
                    utils.setSPOnOff(plugNodeID, "ON")
                    bmMacID = oRow['BMMacID']
                    strDevType = 'FFD'
                    respState, respCode, resp = utils.check_device_joined(bmMacID, strDevType, "1E")
                    print("respState", respState)
                    boolJoined = respState
                    if boolJoined:
                        context.reporter.ReportEvent("Test Validation",
                                                     "Device Joined the network with Node ID : <B>" + resp + "</B>",
                                                     "PASS")
                        print("Device Joined the network with Node ID : ", resp)
                        time.sleep(240)
                    else:
                        intFailCntr = intFailCntr + 1
                        context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                        print("join is unsuccessfull")

                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
                if intSeconds > 20:
                    strStatus = "FAIL"
                else:
                    strStatus = "PASS"
                context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
                print("Time taken: ", strTCDuration)
                print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print()
                if str(strCount).upper() == "INFINITELY":
                    intIter = 0
                else:
                    if intIter == intLoopCtr - 1:
                        flag = False
                        break


@when(
    "the below devices are paired and unpaired after {strDuration} minutes and send identify command sequentially validated {strCount} via Telegesis")
def pair_unpair_duration_for_period(context, strCount, strDuration):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    intLoopCtr = 1
    # strCount = ""
    if str(strCount).upper() == "INFINITELY":
        intLoopCtr = 1
    else:
        strCount = strCount.replace(" times", "")
        intLoopCtr = int(strCount)

    flag = True
    while flag:
        for intIter in range(0, intLoopCtr):
            intCntr = intCntr + 1
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
            MAcID = ""
            for oRow in context.table:
                NodeID = ""
                DeviceType = ""
                if str(oRow['DeviceType']).upper() == "GENERIC":
                    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                    # NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                    oJson = dutils.getDeviceNode(DeviceName, False)
                    MAcID = oJson['macID']
                    DeviceType = oJson['name']
                    NodeID = oJson['nodeID']
                else:
                    DeviceName = oRow['DeviceName']
                    DeviceType = oRow['DeviceType']
                    MAcID = oRow['MacID']
                    NodeID = utils.get_device_node_from_ntable(MAcID)

                myEp = dutils.getDeviceEPWithModel(DeviceType)
                myEp = str(myEp).split("'")[1]
                print(DeviceName, DeviceType, NodeID, MAcID, "\n")
                # Unpair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ')

                context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
                context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")

                utils.remove_device_from_network(NodeID)
                time.sleep(30)
                '''time.sleep(5)
                utils.setSPOnOff("DAF8", "OFF")
                time.sleep(2)
                utils.setSPOnOff("DAF8", "ON")
                time.sleep(5)'''

                # Pair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
                print(utils.getTimeStamp(False), "Join Device to the network")
                intStartTime = time.time()
                intTCStartTime = time.monotonic()
                oDictSED = AT.oDictSED
                strDevType = ''
                if str(DeviceType).upper() in oDictSED:
                    strDevType = 'SED'
                else:
                    strDevType = 'FFD'
                respState, respCode, resp = utils.check_device_joined(MAcID, strDevType, "1E")
                print("respState", respState)
                if respState:
                    intPassCntr = intPassCntr + 1
                    myNodeID = resp
                    context.nodeId = myNodeID
                    # time.sleep(240)
                    if str(oRow['DeviceType']).upper() == "GENERIC":
                        oNodeJson = dutils.getZigbeeDevicesJson()
                        oNodeJson[DeviceName]['nodeID'] = myNodeID
                        dutils.putZigbeeDevicesJson(oNodeJson)
                    context.reporter.ReportEvent("Test Validation",
                                                 "Device Joined the network with Node ID : <B>" + myNodeID + "</B>",
                                                 "PASS")
                    print("Device Joined the network with Node ID : ", myNodeID)
                else:
                    intFailCntr = intFailCntr + 1
                    context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                    print("join is unsuccessfull")
                    return False
                    '''print("Restarting the Smart Plug")
                    utils.setSPOnOff(NodeID, 'OFF')
                    time.sleep(5)
                    utils.setSPOnOff(NodeID, 'ON')
                    time.sleep(5)'''

                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
                if intSeconds > 20:
                    strStatus = "FAIL"
                else:
                    strStatus = "PASS"
                utils.setIdentifyCommand(context, myNodeID, myEp, "{:04X}".format(int(strDuration) * 60))
                time.sleep(int(strDuration) * 60)
                context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
                print("Time taken: ", strTCDuration)
                print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print()
                if str(strCount).upper() == "INFINITELY":
                    intIter = 0
                else:
                    if intIter == intLoopCtr - 1:
                        flag = False
                        break


@when(
    "the below devices are re-paired and send identify command for {strDuration} seconds and wait {strWaitDuration} seconds sequentially validated {strCount} for {strIter} iterations via Telegesis")
def pair_unpair_duration_for_period(context, strDuration, strWaitDuration, strCount, strIter):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    intLoopCtr = 1
    # strCount = ""
    strCount = str(strCount).replace(" times", "")
    if str(strIter).upper() == "INFINITELY":
        intLoopCtr = 1
    else:
        intLoopCtr = int(strIter)

    flag = True
    while flag:
        for intIter in range(0, intLoopCtr):
            intCntr = intCntr + 1
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
            MAcID = ""
            for oRow in context.table:
                NodeID = ""
                DeviceType = ""
                if str(oRow['DeviceType']).upper() == "GENERIC":
                    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                    # NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                    oJson = dutils.getDeviceNode(DeviceName, False)
                    MAcID = oJson['macID']
                    DeviceType = oJson['name']
                    NodeID = oJson['nodeID']
                else:
                    DeviceName = oRow['DeviceName']
                    DeviceType = oRow['DeviceType']
                    MAcID = oRow['MacID']
                    NodeID = utils.get_device_node_from_ntable(MAcID)

                myEp = dutils.getDeviceEPWithModel(DeviceType)
                myEp = str(myEp).split("'")[1]
                print(DeviceName, DeviceType, NodeID, MAcID, "\n")
                # Unpair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ')

                context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
                context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")

                utils.remove_device_from_network(NodeID)
                time.sleep(30)
                '''time.sleep(5)
                utils.setSPOnOff("DAF8", "OFF")
                time.sleep(2)
                utils.setSPOnOff("DAF8", "ON")
                time.sleep(5)'''

                # Pair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ')
                print(utils.getTimeStamp(False), "Join Device to the network")
                intStartTime = time.time()
                intTCStartTime = time.monotonic()
                oDictSED = AT.oDictSED
                strDevType = ''
                if str(DeviceType).upper() in oDictSED:
                    strDevType = 'SED'
                else:
                    strDevType = 'FFD'
                respState, respCode, resp = utils.check_device_joined(MAcID, strDevType, "1E")
                print("respState", respState)
                if respState:
                    intPassCntr = intPassCntr + 1
                    myNodeID = resp
                    context.nodeId = myNodeID
                    # time.sleep(240)
                    if str(oRow['DeviceType']).upper() == "GENERIC":
                        oNodeJson = dutils.getZigbeeDevicesJson()
                        oNodeJson[DeviceName]['nodeID'] = myNodeID
                        dutils.putZigbeeDevicesJson(oNodeJson)
                    context.reporter.ReportEvent("Test Validation",
                                                 "Device Joined the network with Node ID : <B>" + myNodeID + "</B>",
                                                 "PASS")
                    print("Device Joined the network with Node ID : ", myNodeID)
                else:
                    intFailCntr = intFailCntr + 1
                    context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                    print("join is unsuccessfull")
                    return False
                    '''print("Restarting the Smart Plug")
                    utils.setSPOnOff(NodeID, 'OFF')
                    time.sleep(5)
                    utils.setSPOnOff(NodeID, 'ON')
                    time.sleep(5)'''

                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
                context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
                if intSeconds > 20:
                    strStatus = "FAIL"
                else:
                    strStatus = "PASS"
                for i in range(0, int(strCount)):
                    utils.setIdentifyCommand(context, myNodeID, myEp, "{:04X}".format(int(strDuration)))
                    context.reporter.ReportEvent("Test Validation",
                                                 "Identification command set for : " + str(strDuration), "Done")
                    time.sleep(int(strDuration))
                    context.reporter.ReportEvent("Test Validation",
                                                 "wait for : " + str(strWaitDuration), "Done")
                    time.sleep(int(strWaitDuration))

                print("Time taken: ", strTCDuration)
                print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print()
                if str(strCount).upper() == "INFINITELY":
                    intIter = 0
                else:
                    if intIter == intLoopCtr - 1:
                        flag = False
                        break


@then(u'the below devices are unpaired via {HubType} Hub')
def unpair_devices_via_hub(context, HubType):
    intStartTime = time.time()
    intTCStartTime = time.monotonic()
    HubType = HubType.upper().strip()
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    intCntr = intCntr + 1
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
    for oRow in context.table:
        DeviceName = oRow['DeviceName']
        DeviceType = oRow['DeviceType']
        # HubType = oRow['HubType']
        # get node lists
        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session = ALAPI.sessionObject()
        # nodeIdList = context.oThermostatEP.getNodeID(resp)
        nodeIdList = SP.getNodeAndDeviceVersionID()
        if DeviceType in nodeIdList:
            NodeID = nodeIdList[DeviceType]["nodeID"]
            print(DeviceName, DeviceType, NodeID, "\n")
            # Unpair the Device from Telegesis
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device ' + DeviceType + ' from HUb: ')

            context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")

            print(utils.getTimeStamp(False), "Sending Leave request for device")
            ALAPI.deleteDeviceV6(session, NodeID)
            time.sleep(5)
            nodeIdList = SP.getNodeAndDeviceVersionID()
            if DeviceType not in nodeIdList:
                break

    intTCEndTime = time.monotonic()
    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
    strTCDuration = utils.getDuration(strTCDuration)
    intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
    intMin = int(strTCDuration.split(",")[0].strip().split(" ")[0])
    intSeconds = intMin * 60 + intSeconds
    if intSeconds > 60:
        strStatus = "FAIL"
    else:
        strStatus = "PASS"
    context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
    print("Time taken: ", strTCDuration)
    print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print()
    time.sleep(60)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


@then(u'the below devices are paired via {HubType} Hub')
def pair_devices_via_hub(context, HubType):
    intStartTime = time.time()
    intTCStartTime = time.monotonic()
    HubType = HubType.upper().strip() + "_1"
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    intCntr = intCntr + 1
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))
    for oRow in context.table:
        DeviceName = oRow['DeviceName']
        DeviceType = oRow['DeviceType']
        # HubType = oRow['HubType']
        # get node lists
        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session = ALAPI.sessionObject()
        # nodeIdList = context.oThermostatEP.getNodeID(resp)
        nodeIdList = SP.getNodeAndDeviceVersionID()
    boolPairStatus = False
    sleepTime = 0
    # Pair the Device via Hub
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device ' + DeviceType + ' to Hub: ')
    print(utils.getTimeStamp(False), "Join Device to the network")
    ALAPI.setHubStateV6(session, nodeIdList[HubType]["nodeID"], "DISCOVERING")
    intCounter = 0
    while intCounter <= 300:
    # Validate if node is added the network
        nodeIdList = SP.getNodeAndDeviceVersionID()
        if DeviceType in nodeIdList:
            boolPairStatus = True
            break
        time.sleep(1)
    time.sleep(30)
    sleepTime = sleepTime + 30

    print("boolPairStatus", boolPairStatus)
    if boolPairStatus:
        intPassCntr = intPassCntr + 1
        myNodeID = nodeIdList[DeviceType]["nodeID"]

        context.reporter.ReportEvent("Test Validation",
                                     "Device " + DeviceType + " Joined the network with Node ID : <B>" + myNodeID + "</B>",
                                     "PASS")
        print("Device Joined the network with Node ID : ", myNodeID)
    else:
        intFailCntr = intFailCntr + 1
        context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
        print("join is unsuccessfull")
        return False

    intTCEndTime = time.monotonic()
    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
    strTCDuration = utils.getDuration(strTCDuration)
    intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
    intMin = int(strTCDuration.split(",")[0].strip().split(" ")[0])
    intSeconds = intMin * 60 + intSeconds
    if intSeconds > 60:
        strStatus = "FAIL"
    else:
        strStatus = "PASS"
    context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
    print("Time taken: ", strTCDuration)
    print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print()
    time.sleep(180)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
