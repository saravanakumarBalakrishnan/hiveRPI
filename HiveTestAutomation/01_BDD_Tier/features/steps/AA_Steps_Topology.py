"""
Created on 06 Dec 2016

@author: Kingston.SamSelwyn
"""
from behave import *
import FF_ToplogyUtils as tutils
import FF_device_utils as dutils

use_step_matcher("re")


@step(u'the given attenuation is set on the network')
def setToplogy(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Setting Topology')
    oRows = context.table
    context.attenList = tutils.getAttenuatorsIP(context)
    for oRow in oRows:
        resp = tutils.setTopology(context.attenList[oRow["Atten"]], oRow["DB"])
        if str(resp) == "0":
            context.reporter.ReportEvent("Test Validation", "Unable to set the given attenuation", "FAIL")
        if str(resp) == "1":
            context.reporter.ReportEvent("Test Validation",
                                         "Attenuation for " + str(oRow["Atten"]) + " is set to " + str(oRow["DB"]),
                                         "Done")


@when(u"the given topology is formed and verified")
def verfiyTopology(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Topology Verification')
    dutils.AT.stopThread.clear()
    # dutils.AT.startSerialThreads(context.PORT, config.BAUD, printStatus=True, rxQ=True, listenerQ=True)
    oActualDeviceList = dutils.getNodes(True)
    oPreviousDeviceList = dutils.getZigbeeDevicesJson()
    # time.sleep(600)
    flag = False
    for oDevices in list(oActualDeviceList.keys()):
        flag = False
        if oDevices in list(oPreviousDeviceList.keys()):
            context.reporter.ReportEvent("Test Validation", "The device " + oDevices + " is present", "PASS")
        else:
            context.reporter.ReportEvent("Test Validation", "The device " + oDevices + " is not present", "FAIL")
    oDict = []
    for oActual in oPreviousDeviceList:
        flag = False
        if "RFD" not in oPreviousDeviceList[oActual]['type']:
            strParent = ""
            strChild = ""
            for oRow in oPreviousDeviceList[oActual]["childNodes"]:
                oChild = ""
                for oCheck in oPreviousDeviceList:
                    if oPreviousDeviceList[oCheck]["nodeID"] == oRow:
                        oChild = oPreviousDeviceList[oCheck]["name"]
                for oDataRow in context.table:
                    strParent = oDataRow["Parent"]
                    strChild = oDataRow["Child"]
                    if oDataRow["Child"] == oChild and oDataRow["Parent"] == oPreviousDeviceList[oActual]["name"]:
                        flag = True
                        # context.reporter.ReportEvent("Test Validation",
                        #                             "The topology " + oDataRow["Parent"] + "-------->" + oDataRow[
                        #                                 "Child"] + " is found", "PASS")
                        oDict.append({"'" + str(oDataRow["Parent"]) + "'": "'" + str(oChild) + "'"})
                        # if not flag:
                        #        context.reporter.ReportEvent("Test Validation",
                        #                                     "The topology " + strParent + "-------->" + strChild + " is not found", "FAIL")
    print("\n")
    print(str(oDict))
    print("\n")

    print("\n")

    print("\n")

    print("\n")

    print("\n")
    print("\n")

    for oDataRow in context.table:
        flag = False
        for oActual in oDict:
            if str(oDataRow["Parent"]) in str(oActual) and str(oDataRow["Child"]) in str(oActual):
                flag = True
                context.reporter.ReportEvent("Test Validation",
                                             "The topology " + oDataRow["Parent"] + "<-------->" + oDataRow[
                                                 "Child"] + " is  found", "PASS")
        if not flag:
            context.reporter.ReportEvent("Test Validation",
                                         "The topology " + oDataRow["Parent"] + "<-------->" + oDataRow[
                                             "Child"] + " is not found", "FAIL")
