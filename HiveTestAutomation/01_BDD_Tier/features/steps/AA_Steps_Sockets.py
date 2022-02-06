"""
Created on 06 Dec 2016

@author: Kingston.SamSelwyn
"""
import time
from behave import *
import FF_utils as utils
import FF_device_utils as dutils


@When(u'The below {strDevice} state is changed to {strDeviceState} and validated infinitely')
def changeStateAndValidate(context, strDevice, strDeviceState):
    deviceType = strDevice
    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
    oJson = dutils.getZigbeeDevicesJson()
    bool = False
    for oItems in oJson:
        if str(strDevice).upper() == str(oJson[oItems]['name']).upper():
            bool = True
            MAcID = oJson[oItems]['macID']
            DeviceType = oJson[oItems]['name']
            myNodeId = oJson[oItems]['nodeID']
            context.nodeId = myNodeId
            if DeviceType == "HAS01UK":
                myEps = oJson[oItems]["endPoints"]
            else:
                myEp = oJson[oItems]["endPoints"][0]

    if bool:
        intCntr = 0
        while True:
            if DeviceType == "HAS01UK":
                intEpIndex = intCntr % 2
                myEp = myEps[intEpIndex]
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Socket : ' + str(intEpIndex))
                if intEpIndex == 0:
                    intIterCounter, _ = divmod(intCntr, 2)
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                        'On Off Validation Counter : ' + str(intIterCounter))
                else:
                    intIterCounter, _ = divmod(intCntr, 2)
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                        'On Off Validation Counter : ' + str(intIterCounter + 1))

            else:
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('On Off Validation Counter : ' + str(intCntr))
            intCntr = intCntr + 1
            for oRow in context.table:
                utils.setOnOff(myNodeId, myEp, oRow["Device State"], True)
                context.reporter.ReportEvent("Test Validation", "The devices is set to " + oRow["Device State"], "Done")
                _, _, respValue = utils.readAttribute("MANUFACTURER", myNodeId, myEp, "0", "0006", "0000")
                if oRow["Device State"] == "ON":
                    if str(respValue) == "RESPATTR:" + str(myNodeId) + "," + str(myEp) + ",0006,0000,00,01":
                        context.reporter.ReportEvent("Test Validation",
                                                     "The state is changed to 01 in the zigbee attribute", "PASS")
                    else:
                        context.reporter.ReportEvent("Test Validation",
                                                     "The current value is " + str(respValue), "FAIL")
                if oRow["Device State"] == "OFF":
                    if str(respValue) == "RESPATTR:" + str(myNodeId) + "," + str(myEp) + ",0006,0000,00,00":
                        context.reporter.ReportEvent("Test Validation",
                                                     "The state is changed to 00 in the zigbee attribute", "PASS")
                    else:
                        context.reporter.ReportEvent("Test Validation",
                                                     "The current value is " + str(respValue), "FAIL")
                time.sleep(10)
