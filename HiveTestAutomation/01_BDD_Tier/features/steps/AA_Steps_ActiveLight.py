"""
Created on 14 Jan 2016

@author: ranganathan.veluswamy
"""

import time
from datetime import timedelta

from behave import *

import AA_Steps_SmartPlug as SP
import FF_alertmeApi as ALAPI
import FF_device_utils as dutils
import FF_threadedSerial as AT
import FF_utils as utils
import FF_zigbeeToolsConfig as config

lightSensorCalibration = {0: (1100, 2000),
						  2: (200, 2000),
						  4: (1100, 2000),
                          6: (3000, 3600),
                          8: (3000, 3600),
                          10: (7000, 8500),
                          12: (3000, 3600),
                          14: (9000, 11750),
                          16: (3000, 3600),
                          18: (13000, 15000),
                          20: (3000, 3600),
                          22: (19000, 22000),
                          24: (200, 2000),
						  26: (1100, 2000),
                          28: (3000, 3600),
                          30: (3000, 3600),
                          32: (7000, 8500),
                          34: (3000, 3600),
                          36: (9000, 11750),
                          38: (3000, 3600),
                          40: (13000, 15000),
                          42: (3000, 3600),
                          44: (19000, 22000),
                          46: (1100, 2000),
                          48: (3000, 3600),
                          50: (3000, 3600),
                          52: (7000, 8500),
                          54: (3000, 3600),
                          56: (9000, 11750),
                          58: (3000, 3600),
                          60: (13000, 15000),
                          62: (3000, 3600),
                          64: (19000, 22000),
                          66: (1100, 2000),
                          68: (3000, 3600),
                          70: (3000, 3600),
                          72: (7000, 8500),
                          74: (3000, 3600),
                          76: (9000, 11750),
                          78: (3000, 3600),
                          80: (13000, 15000),
                          82: (3000, 3600),
                          84: (19000, 22000),
                          86: (1100, 2000),
                          88: (3000, 3600),
                          90: (3000, 3600),
                          92: (3000, 3600),
                          96: (19000, 22000),
                          97: (1100, 2000),
                          98: (3000, 3600),
                          99: (3000, 3600),
                          100: (26000, 30000)}


@when(
    u'The {ActiveLightDevice} is switched ON and OFF state and brightness of the light is varied {times}min and validated for the below brightness values {strDuration} via Hub')
def validateActiveLightFunctionViaHub(context, ActiveLightDevice,times,strDuration):
    oColorTempList = {0: 2700,
                      96: 3460,
                      97: 4220,
                      98: 4980,
                      99: 5740,
                      100: 6500}
    oColorTempPercentageList = list(oColorTempList.keys())

    # get node lists
    nodeIdList = SP.getNodeAndDeviceVersionID()
    print("nodeIdlist",nodeIdList)
    strLightNodeID = ""
    print(nodeIdList)
    if 'ActiveLight' in ActiveLightDevice:
        if 'FWBulb01_1' in nodeIdList:
            strLightNodeID = nodeIdList['FWBulb01_1']["nodeID"]
        elif 'LDS_DimmerLight_1' in nodeIdList:
            strLightNodeID = nodeIdList['LDS_DimmerLight_1']["nodeID"]
        elif 'FWBulb03UK_1' in nodeIdList:
            print('inside FWBulb03UK')
            strLightNodeID = nodeIdList['FWCLBulb03UK_1']["nodeID"]
        elif 'TWGU10Bulb03UK_1' in nodeIdList:
            print('inside RGB')
            strLightNodeID = nodeIdList['TWGU10Bulb03UK_1']["nodeID"]
        elif 'TWBulb03UK_1' in nodeIdList:
            print('inside RGB')
            strLightNodeID = nodeIdList['TWBulb03UK_1']["nodeID"]
        elif 'RGBBulb03UK_1' in nodeIdList:
            print('inside RGB')
            strLightNodeID = nodeIdList['RGBBulb03UK_1']["nodeID"]
        elif 'RGBBulb02UK_1' in nodeIdList:
            print('inside RGB')
            strLightNodeID = nodeIdList['RGBBulb02UK_1']["nodeID"]
    elif ActiveLightDevice in nodeIdList:
        strLightNodeID = nodeIdList[ActiveLightDevice]["nodeID"]
    else:
        context.reporter.ReportEvent('Test Validation', "Active light Node is missing.", "FAIL")
        return False

    intCntr = 0
    count=0
    print("Storage folder "+str(context.reporter.strCurrentTXTFolder))
    # Open Text file to write the light parameters
    oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter

    while count <1:
        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session = ALAPI.sessionObjectV6dot5()

        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        boolPass = True
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Active Light Brightness validation Counter: ' + str(intCntr))

        if "TW" in ActiveLightDevice.upper():
            intTempCntr = intCntr % 5
            myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]

            ALAPI.setActiveLightColourTemperature(session, strLightNodeID, myColourTemp)
            print("lightTemperature",myColourTemp)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>",
                                         "Done")
            strParameterValue = strParameterValue + "," + str(myColourTemp)

        # Set Light ON
        ALAPI.setActiveLightState(session, strLightNodeID, "ON")
        print("LIght node ID",strLightNodeID)
        context.reporter.ReportEvent('Test Validation', "Active light is switched <B>ON</B>", "PASS")
        time.sleep(5)
        oBrightnessList = []
        # ChangeBrightness
        for oRow in context.table:
            intBrightness = int(oRow['BrightnessValue'])
            print("Brightness percentage value \t"+oRow['BrightnessValue'])
            ALAPI.setActiveLightBrightness(session, strLightNodeID, intBrightness)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light Brightness is set to : <B>" + str(intBrightness) + "</B>",
                                         "Done")
            time.sleep(2)
            luxSpikeTest = False
            if intBrightness in lightSensorCalibration:
                if '0' not in times.upper() :
                    luxSpikeTest = True
                if luxSpikeTest is True:
                    for x in range(5):
                        print('inside Spike test sample count:'+str(x))
                        intLowLimit = lightSensorCalibration[intBrightness][0]
                        intHighLimit = lightSensorCalibration[intBrightness][1]
                        time.sleep(5)
                        print("sleepingggggg")
                        
                        sensorValue, _, _ = utils.get_lux_value()
                        if intLowLimit < sensorValue < intHighLimit:
                            context.reporter.ReportEvent('Test Validation',
                                                         "The measured LUX value for Active light Brightness is: <B>" + str(
                                                             sensorValue) + "</B>. Which is within the calibration limit: " + str(
                                                             intLowLimit) + " - " + str(intHighLimit), "PASS")
                        else:
                            context.reporter.ReportEvent('Test Validation',
                                                         "The measured LUX value for Active light Brightness is: <B>" + str(
                                                             sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(
                                                             intLowLimit) + " - " + str(intHighLimit), "FAIL")
                            boolPass = False

                        if not intBrightness in oBrightnessList:
                            # oBrightnessList.append(intBrightness)
                            strParameterValue = str(intBrightness) + "," + str(sensorValue)
                            print("inside writing counter", strParameterValue)
                            print("Storage folder "+str(context.reporter.strCurrentTXTFolder))
                            oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
                            print("inside file", strParameterValue)
                            oFileWriter.write(strParameterValue + "\n")
                            oFileWriter.close()
                            del oFileWriter
                        try:
                         time.sleep(5)
                        except RuntimeError as err:
                         print("error",err)
                else:
                        print('NoSPIKEEE')
                        intLowLimit = lightSensorCalibration[intBrightness][0]
                        intHighLimit = lightSensorCalibration[intBrightness][1]
                        # time.sleep(1800)
#                         print("sleepingggggg 30mins")
                        sensorValue, _, _ = utils.get_lux_value()
                        if intLowLimit < sensorValue < intHighLimit:
                            context.reporter.ReportEvent('Test Validation',
                                                         "The measured LUX value for Active light Brightness is: <B>" + str(
                                                             sensorValue) + "</B>. Which is within the calibration limit: " + str(
                                                             intLowLimit) + " - " + str(intHighLimit), "PASS")
                        else:
                            context.reporter.ReportEvent('Test Validation',
                                                         "The measured LUX value for Active light Brightness is: <B>" + str(
                                                             sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(
                                                             intLowLimit) + " - " + str(intHighLimit), "FAIL")
                            boolPass = False

                        if not intBrightness in oBrightnessList:
                            oBrightnessList.append(intBrightness)
                            strParameterValue = str(intBrightness) + "," + str(sensorValue)
                            print("inside writing counter", strParameterValue)
                            oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
                            print("inside file", strParameterValue)
                            oFileWriter.write(strParameterValue + "\n")
                            oFileWriter.close()
                            del oFileWriter

            else:
                context.reporter.ReportEvent('Test Validation', "The Brightness values should be in multiples of 20",
                                             "FAIL")

        # Update Text file


        # Update the Pass and Fail counters
        context.reporter.intIterationCntr = intCntr
        if boolPass:
            context.reporter.intIterationPassCntr = context.reporter.intIterationPassCntr + 1
        else:
            context.reporter.intIterationFailCntr = context.reporter.intIterationFailCntr + 1

        # Set Light OFF
        ALAPI.setActiveLightState(session, strLightNodeID, "OFF")
        context.reporter.ReportEvent('Test Validation', "Active Plug is switched <B>OFF</B>", "PASS")
        # time.sleep(5)
        ALAPI.deleteSessionV6(session)
        break
    count=3
    


@when(
    u'The {ActiveLightDevice} is switched {strState} and validated via Hub')
def validateActiveLightFunctionViaHub(context, ActiveLightDevice, strState):

    # get node lists
    nodeIdList = SP.getNodeAndDeviceVersionID()
    strNodeID = nodeIdList[ActiveLightDevice]["nodeID"]

    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()

    boolPass = True
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Device state change:')

    # Set Light ON
    ALAPI.setActiveLightState(session, strNodeID, str(strState).upper())
    context.reporter.ReportEvent('Test Validation', "Device is switched <B>"+str(strState).upper()+"</B>", "PASS")
    time.sleep(5)

    ALAPI.deleteSessionV6(session)


@when(
    u'The {ActiveLightDevice} is switched ON and OFF state and brightness of the light is varied and validated for {TimePeriod} for the below brightness values infinitely via Hub')
def validateActiveLightFunctionForPeriodViaHub(context, ActiveLightDevice, TimePeriod):
    TimePeriodinSec = int(TimePeriod) * 60
    oColorTempList = {0: "2700",
                      20: "3460",
                      40: "4220",
                      60: "4980",
                      80: "5740",
                      100: "6500"}
    oColorTempPercentageList = list(oColorTempList.keys())

    # get node lists
    nodeIdList = SP.getNodeAndDeviceVersionID()
    if 'ActiveLight' in ActiveLightDevice:
        if 'FWBulb01_1' in nodeIdList:
            strLightNodeID = nodeIdList['FWBulb01_1']["nodeID"]
        elif 'LDS_DimmerLight_1' in nodeIdList:
            strLightNodeID = nodeIdList['LDS_DimmerLight_1']["nodeID"]
    elif ActiveLightDevice in nodeIdList:
        strLightNodeID = nodeIdList[ActiveLightDevice]["nodeID"]
    else:
        context.reporter.ReportEvent('Test Validation', "Active light Node is missing.", "FAIL")
        return False

    intCntr = 0

    # Open Text file to write the light parameters
    print("Storage folder "+str(context.reporter.strCurrentTXTFolder))
    oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter

    while True:
        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session = ALAPI.sessionObject()

        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        boolPass = True
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Active Light Brightness validation Counter: ' + str(intCntr))

        if "TWBULB" in ActiveLightDevice.upper():
            intTempCntr = intCntr % 5
            myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]

            ALAPI.setActiveLightColourTemperature(session, strLightNodeID, myColourTemp)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>",
                                         "Done")
            strParameterValue = strParameterValue + "," + myColourTemp

        # Set Light ON
        ALAPI.setActiveLightState(session, strLightNodeID, "ON")
        context.reporter.ReportEvent('Test Validation', "Active light is switched <B>ON</B>", "PASS")
        time.sleep(5)
        oBrightnessList = []
        # ChangeBrightness
        for oRow in context.table:
            intBrightness = int(oRow['BrightnessValue'])
            ALAPI.setActiveLightBrightness(session, strLightNodeID, intBrightness)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light Brightness is set to : <B>" + str(intBrightness) + "</B>",
                                         "Done")
            time.sleep(5)
            intCurrentTime = int(time.monotonic())
            intExpiryTime = intCurrentTime + TimePeriodinSec

            oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
            while intExpiryTime > intCurrentTime:
                intCurrentTime = int(time.monotonic())
                if intBrightness in lightSensorCalibration:
                    intLowLimit = lightSensorCalibration[intBrightness][0]
                    intHighLimit = lightSensorCalibration[intBrightness][1]
                    sensorValue, _, _ = utils.get_lux_value()
                    if intLowLimit < sensorValue < intHighLimit:
                        context.reporter.ReportEvent('Test Validation',
                                                     "The measured LUX value for Active light Brightness is: <B>" + str(
                                                         sensorValue) + "</B>. Which is within the calibration limit: " + str(
                                                         intLowLimit) + " - " + str(intHighLimit), "PASS")
                    else:
                        context.reporter.ReportEvent('Test Validation',
                                                     "The measured LUX value for Active light Brightness is: <B>" + str(
                                                         sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(
                                                         intLowLimit) + " - " + str(intHighLimit), "FAIL")
                        boolPass = False

                    if not intBrightness in oBrightnessList:
                        oBrightnessList.append(intBrightness)
                        strParameterValue = str(intBrightness) + "," + str(sensorValue)
                    # Update Text file
                    strParameterValue = str(intBrightness) + "," + str(sensorValue) + "====>" + utils.getTimeStamp(
                        False)
                    oFileWriter.write(strParameterValue + "\n")
                    time.sleep(0.5)
                else:
                    context.reporter.ReportEvent('Test Validation',
                                                 "The Brightness values should be in multiples of 20", "FAIL")
            oFileWriter.close()

            del oFileWriter

        # Update Text file
        oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
        oFileWriter.write(strParameterValue + "\n")
        oFileWriter.close()
        del oFileWriter

        # Update the Pass and Fail counters
        context.reporter.intIterationCntr = intCntr
        if boolPass:
            context.reporter.intIterationPassCntr = context.reporter.intIterationPassCntr + 1
        else:
            context.reporter.intIterationFailCntr = context.reporter.intIterationFailCntr + 1

        # Set Light OFF
        ALAPI.setActiveLightState(session, strLightNodeID, "OFF")
        context.reporter.ReportEvent('Test Validation', "Active Plug is switched <B>OFF</B>", "PASS")
        time.sleep(5)
        ALAPI.deleteSessionV6(session)


@when(
    u'The ActiveLight is switched ON state and brightness of the light is validated for the {strBrightnesValue} brightness for {Duration} via telegesis')
def activeLightBrightnessValidationForSpike(context, strBrightnesValue, Duration):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        Duration = str(Duration).split(" ")[0]
        intMaxExecSeconds = int(Duration) * 60

    oColorTempList = {0: "00A5",
                      20: "00C8",
                      40: "00F0",
                      60: "0118",
                      80: "0140",
                      100: "0172"}

    oColorTempList = {0: 2700,
                      20: 3460,
                      40: 4220,
                      60: 4980,
                      80: 5740,
                      100: 6500}

    oColorTempPercentageList = list(oColorTempList.keys())
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    # Get Model
    _, _, model = AT.getAttribute(myNodeId, "01", "0000", "0005", 'server')
    intTCStartTime = time.monotonic()
    intCntr = 0
    # Open Text file to write the light parameters
    oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP" + str(strBrightnesValue) + ".txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter
    AT.onOff(myNodeId, "01", 0, 1)
    context.reporter.ReportEvent('Test Validation',
                                 "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
    strBrightnesValue = int(strBrightnesValue)
    intTimeLapse = 1
    intTimeLapseRep = '{:04x}'.format(intTimeLapse)
    respState, respCode, respValue = AT.moveToLevel(myNodeId, "01", 0, int(strBrightnesValue),
                                                    int(intTimeLapseRep))
    while True:
        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Active Light Brightness validation Counter: ' + str(intCntr))

        oBrightnessList = []

        context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(
            strBrightnesValue) + "</B>", "Done")
        # Validate Lux

        if strBrightnesValue in lightSensorCalibration:
            intLowLimit = lightSensorCalibration[strBrightnesValue][0]
            intHighLimit = lightSensorCalibration[strBrightnesValue][1]
            sensorValue, _, _ = utils.get_lux_value()
            if intLowLimit < sensorValue < intHighLimit:
                context.reporter.ReportEvent('Test Validation',
                                             "The measured LUX value for Active light Brightness is: <B>" + str(
                                                 sensorValue) + "</B>. Which is within the calibration limit: " + str(
                                                 intLowLimit) + " - " + str(intHighLimit), "PASS")
            else:
                context.reporter.ReportEvent('Test Validation',
                                             "The measured LUX value for Active light Brightness is: <B>" + str(
                                                 sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(
                                                 intLowLimit) + " - " + str(intHighLimit), "FAIL")
                boolPass = False

            if not strBrightnesValue in oBrightnessList:
                oBrightnessList.append(strBrightnesValue)
                strParameterValue = strParameterValue + "," + str(sensorValue)
        else:
            if not ("ON" in str(strBrightnesValue).upper() or "OFF" in str(strBrightnesValue).upper()):
                context.reporter.ReportEvent('Test Validation',
                                             "The Brightness values should be in multiples of 20", "FAIL")

        # Update Text file
        oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP" + str(strBrightnesValue) + ".txt", 'a')
        oFileWriter.write(strParameterValue + "\n")
        oFileWriter.close()
        del oFileWriter

        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
        intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
        intSeconds = int(timedelta(seconds=intTCEndTime - intTCStartTime).seconds)

        if not boolInfiniteExec:
            if intSeconds > intMaxExecSeconds:
                break


@when(
    u'The ActiveLight is switched ON state and brightness of the light is validated for the brightness range between {strBrightnesMaxValue} to {strBrightnesMinValue} for {Duration} via telegesis')
def activeLightBrightnessValidationForSpikeRange(context, strBrightnesMaxValue, strBrightnesMinValue, Duration):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        Duration = str(Duration).split(" ")[0]
        intMaxExecSeconds = int(Duration) * 60

    oColorTempList = {0: "00A5",
                      20: "00C8",
                      40: "00F0",
                      60: "0118",
                      80: "0140",
                      100: "0172"}

    oColorTempList = {0: 2700,
                      20: 3460,
                      40: 4220,
                      60: 4980,
                      80: 5740,
                      100: 6500}

    oColorTempPercentageList = list(oColorTempList.keys())
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    # Get Model
    _, _, model = AT.getAttribute(myNodeId, "01", "0000", "0005", 'server')

    intCntr = 0

    AT.onOff(myNodeId, "01", 0, 1)
    intInc = 0
    if int(strBrightnesMaxValue) > int(strBrightnesMinValue):
        intInc = -1
    else:
        intInc = 1
    strBrightnesValue = strBrightnesMaxValue
    oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter
    while True:
        intTCStartTime = time.monotonic()
        # Open Text file to write the light parameters

        strBrightnesValue = int(strBrightnesValue)
        # hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
        intTimeLapse = 1
        intTimeLapseRep = '{:04x}'.format(intTimeLapse)
        respState, respCode, respValue = AT.moveToLevel(myNodeId, "01", 0, int(strBrightnesValue), int(intTimeLapseRep))
        context.reporter.ReportEvent('Test Validation',
                                     "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
        while True:
            strParameterValue = ""
            intCntr = intCntr + 1
            strParameterValue = str(intCntr)
            context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                'Active Light Brightness validation Counter: ' + str(intCntr))

            oBrightnessList = []

            context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(
                strBrightnesValue) + "</B>", "Done")
            # Validate Lux

            sensorValue, _, _ = utils.get_lux_value()
            context.reporter.ReportEvent('Test Validation',
                                         "The measured LUX value for Active light Brightness is: <B>" + str(
                                             sensorValue) + "</B>.", "DONE")

            strParameterValue = strParameterValue + "," + str(sensorValue) + "," + str(strBrightnesValue)

            # Update Text file
            oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
            oFileWriter.write(strParameterValue + "\n")
            oFileWriter.close()
            del oFileWriter

            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
            intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
            intSeconds = int(timedelta(seconds=intTCEndTime - intTCStartTime).seconds)

            if not boolInfiniteExec:
                print(str(intSeconds) + "=====" + str(intMaxExecSeconds))
                if intSeconds > intMaxExecSeconds:
                    break

        if int(strBrightnesValue) == int(strBrightnesMinValue):
            break
        strBrightnesValue = int(strBrightnesValue) + intInc


@when(
    u'The ActiveLight is switched ON state with given temperature and brightness of the light is validated for the brightness range between {strBrightnesMaxValue} to {strBrightnesMinValue} for {Duration} via telegesis')
def activeLightBrightnessValidationForSpikeRange(context, strBrightnesMaxValue, strBrightnesMinValue, Duration):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        Duration = str(Duration).split(" ")[0]
        intMaxExecSeconds = int(Duration) * 60

    oColorTempList = {0: "00A5",
                      20: "00C8",
                      40: "00F0",
                      60: "0118",
                      80: "0140",
                      100: "0172"}

    oColorTempList = {0: 2700,
                      20: 3460,
                      40: 4220,
                      60: 4980,
                      80: 5740,
                      100: 6500}

    oColorTempPercentageList = list(oColorTempList.keys())
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    # Get Model
    _, _, model = AT.getAttribute(myNodeId, "01", "0000", "0005", 'server')
    print(model)

    intCntr = 0

    AT.onOff(myNodeId, "01", 0, 1)

    for oColor in oColorTempList:
        myColourTemp = oColorTempList[oColor]
        # myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]
        AT.colourTemperature(myNodeId, "01", 0, myColourTemp, 0)
        context.reporter.ReportEvent('Test Validation',
                                     "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>",
                                     "Done")

        intInc = 0
        if int(strBrightnesMaxValue) > int(strBrightnesMinValue):
            intInc = -1
        else:
            intInc = 1
        strBrightnesValue = strBrightnesMaxValue
        oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP" + str(myColourTemp) + ".txt", 'w')
        oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
        oFileWriter.close()
        del oFileWriter
        while True:
            intTCStartTime = time.monotonic()
            # Open Text file to write the light parameters

            strBrightnesValue = int(strBrightnesValue)
            # hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
            intTimeLapse = 1
            intTimeLapseRep = '{:04x}'.format(intTimeLapse)
            respState, respCode, respValue = AT.moveToLevel(myNodeId, "01", 0, int(strBrightnesValue),
                                                            int(intTimeLapseRep))
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            while True:
                strParameterValue = ""
                intCntr = intCntr + 1
                strParameterValue = str(intCntr)
                context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                    'Active Light Brightness validation Counter: ' + str(intCntr))

                oBrightnessList = []

                print(intCntr, respState, respCode, respValue)
                context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(
                    strBrightnesValue) + "</B>", "Done")
                # Validate Lux
                # time.sleep(1)
                sensorValue, _, _ = utils.get_lux_value()
                context.reporter.ReportEvent('Test Validation',
                                             "The measured LUX value for Active light Brightness is: <B>" + str(
                                                 sensorValue) + "</B>.", "DONE")

                strParameterValue = strParameterValue + "," + str(sensorValue) + "," + str(strBrightnesValue)

                # Update Text file
                oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP" + str(myColourTemp) + ".txt", 'a')
                oFileWriter.write(strParameterValue + "\n")
                oFileWriter.close()
                del oFileWriter

                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
                intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
                intSeconds = int(timedelta(seconds=intTCEndTime - intTCStartTime).seconds)

                if not boolInfiniteExec:
                    print(str(intSeconds) + "=====" + str(intMaxExecSeconds))
                    if intSeconds > intMaxExecSeconds:
                        break

            if int(strBrightnesValue) == int(strBrightnesMinValue):
                break
            strBrightnesValue = int(strBrightnesValue) + intInc


@when(
    u'The ActiveLight is switched ON state with given colour and brightness of the light is validated for the brightness range between {strBrightnesMaxValue} to {strBrightnesMinValue} for {Duration} via telegesis')
def activeLightBrightnessValidationForSpikeRange(context, strBrightnesMaxValue, strBrightnesMinValue, Duration):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        Duration = str(Duration).split(" ")[0]
        intMaxExecSeconds = int(Duration) * 60
    myEp = "01"
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    # Get Model
    _, _, model = AT.getAttribute(myNodeId, myEp, "0000", "0005", 'server')
    print(model)

    intCntr = 0

    AT.onOff(myNodeId, myEp, 0, 1)

    for oRow in context.table:
        hexHue = oRow['HueValue']
        sat = oRow['SatValue']

        context.reporter.ReportEvent('Test Validation',
                                     "RGB light is set to Color Hue : <B>" + str(hexHue) + "</B>", "Done")
        respState, respCode, respValue = utils.changeSatOrColorHue(context, myNodeId, myEp, hexHue, sat,
                                                                   myDuration='0000')
        intInc = 0
        if int(strBrightnesMaxValue) > int(strBrightnesMinValue):
            intInc = -1
        else:
            intInc = 1
        strBrightnesValue = strBrightnesMaxValue
        oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP" + str(hexHue) + ".txt", 'w')
        oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
        oFileWriter.close()
        del oFileWriter
        while True:
            intTCStartTime = time.monotonic()
            # Open Text file to write the light parameters

            strBrightnesValue = int(strBrightnesValue)
            # hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
            intTimeLapse = 1
            intTimeLapseRep = '{:04x}'.format(intTimeLapse)
            respState, respCode, respValue = AT.moveToLevel(myNodeId, "01", 0, int(strBrightnesValue),
                                                            int(intTimeLapseRep))
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            while True:
                strParameterValue = ""
                intCntr = intCntr + 1
                strParameterValue = str(intCntr)
                context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                    'Active Light Brightness validation Counter: ' + str(intCntr))

                oBrightnessList = []

                print(intCntr, respState, respCode, respValue)
                context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(
                    strBrightnesValue) + "</B>", "Done")
                # Validate Lux
                # time.sleep(1)
                sensorValue, _, _ = utils.get_lux_value()
                context.reporter.ReportEvent('Test Validation',
                                             "The measured LUX value for Active light Brightness is: <B>" + str(
                                                 sensorValue) + "</B>.", "DONE")

                strParameterValue = strParameterValue + "," + str(sensorValue) + "," + str(strBrightnesValue)

                # Update Text file
                oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP" + str(hexHue) + ".txt", 'a')
                oFileWriter.write(strParameterValue + "\n")
                oFileWriter.close()
                del oFileWriter

                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
                intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
                intSeconds = int(timedelta(seconds=intTCEndTime - intTCStartTime).seconds)

                if not boolInfiniteExec:
                    print(str(intSeconds) + "=====" + str(intMaxExecSeconds))
                    if intSeconds > intMaxExecSeconds:
                        break

            if int(strBrightnesValue) == int(strBrightnesMinValue):
                break
            strBrightnesValue = int(strBrightnesValue) + intInc


@when(
    u'The ActiveLight is switched ON state with given temperature and brightness of the light is validated with varied gain for the brightness range between {strBrightnesMaxValue} to {strBrightnesMinValue} for {Duration} via telegesis')
def activeLightBrightnessValidationForSpikeRange(context, strBrightnesMaxValue, strBrightnesMinValue, Duration):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        Duration = str(Duration).split(" ")[0]
        intMaxExecSeconds = int(Duration) * 60

    oColorTempList = {0: "00A5",
                      20: "00C8",
                      40: "00F0",
                      60: "0118",
                      80: "0140",
                      100: "0172"}

    oColorTempList = {0: 2700,
                      20: 3460,
                      40: 4220,
                      60: 4980,
                      80: 5740,
                      100: 6500}

    oColorTempPercentageList = list(oColorTempList.keys())
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    # Get Model
    _, _, model = AT.getAttribute(myNodeId, "01", "0000", "0005", 'server')
    print(model)

    intCntr = 0

    AT.onOff(myNodeId, "01", 0, 1)

    for oColor in oColorTempList:
        myColourTemp = oColorTempList[oColor]
        AT.colourTemperature(myNodeId, "01", 0, myColourTemp, 0)
        context.reporter.ReportEvent('Test Validation',
                                     "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>",
                                     "Done")

        intInc = 0
        if int(strBrightnesMaxValue) > int(strBrightnesMinValue):
            intInc = -1
        else:
            intInc = 1
        strBrightnesValue = strBrightnesMaxValue
        oFileWriter = open(context.reporter.strCurrentTXTFolder + "16xLUXvsTEMP" + str(myColourTemp) + ".txt", 'w')
        oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
        oFileWriter.close()
        del oFileWriter

        oFileWriter = open(context.reporter.strCurrentTXTFolder + "1xLUXvsTEMP" + str(myColourTemp) + ".txt", 'w')
        oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
        oFileWriter.close()
        del oFileWriter

        while True:
            intTCStartTime = time.monotonic()
            # Open Text file to write the light parameters

            strBrightnesValue = int(strBrightnesValue)
            intTimeLapse = 1
            intTimeLapseRep = '{:04x}'.format(intTimeLapse)
            respState, respCode, respValue = AT.moveToLevel(myNodeId, "01", 0, int(strBrightnesValue),
                                                            int(intTimeLapseRep))
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            while True:
                strParameterValue = ""
                intCntr = intCntr + 1
                strParameterValue1 = str(intCntr)
                strParameterValue2 = str(intCntr)
                context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                    'Active Light Brightness validation Counter: ' + str(intCntr))

                oBrightnessList = []

                print(intCntr, respState, respCode, respValue)
                context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(
                    strBrightnesValue) + "</B>", "Done")
                # Validate Lux
                sensorValue, fullScaled, irScaled = utils.get_lux_value_16x()
                context.reporter.ReportEvent('Test Validation',
                                             "The measured 16x LUX value for Active light Brightness is: <B>" + str(
                                                 sensorValue) + "</B>.", "DONE")

                strParameterValue1 = strParameterValue1 + "," + str(sensorValue) + "," + str(strBrightnesValue)

                # Update Text file
                oFileWriter = open(context.reporter.strCurrentTXTFolder + "16xLUXvsTEMP" + str(myColourTemp) + ".txt",
                                   'a')
                oFileWriter.write(strParameterValue1 + "," + str(fullScaled) + "," + str(irScaled) + "\n")
                oFileWriter.close()
                del oFileWriter

                sensorValue, fullScaled, irScaled = utils.get_lux_value_1x()
                context.reporter.ReportEvent('Test Validation',
                                             "The measured 1x LUX value for Active light Brightness is: <B>" + str(
                                                 sensorValue) + "</B>.", "DONE")

                strParameterValue2 = strParameterValue2 + "," + str(sensorValue) + "," + str(strBrightnesValue)

                # Update Text file
                oFileWriter = open(context.reporter.strCurrentTXTFolder + "1xLUXvsTEMP" + str(myColourTemp) + ".txt",
                                   'a')
                oFileWriter.write(strParameterValue2 + "," + str(fullScaled) + "," + str(irScaled) + "\n")
                oFileWriter.close()
                del oFileWriter

                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
                intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
                intSeconds = int(timedelta(seconds=intTCEndTime - intTCStartTime).seconds)

                if not boolInfiniteExec:
                    print(str(intSeconds) + "=====" + str(intMaxExecSeconds))
                    if intSeconds > intMaxExecSeconds:
                        break

            if int(strBrightnesValue) == int(strBrightnesMinValue):
                break
            strBrightnesValue = int(strBrightnesValue) + intInc


@when(
    u'The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values {Duration} via telegesis')
def activeLightBrightnessValidation(context, Duration):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        Duration = str(Duration).split(" ")[1]
        intMaxExecSeconds = int(Duration) * 60

    oColorTempList = {0: "00A5",
                      20: "00C8",
                      40: "00F0",
                      60: "0118",
                      80: "0140",
                      100: "0172"}

    oColorTempList = {0: 2700,
                      20: 3460,
                      40: 4220,
                      60: 4980,
                      80: 5740,
                      100: 6500}

    oColorTempPercentageList = list(oColorTempList.keys())
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    # Get Model
    _, _, model = AT.getAttribute(myNodeId, "01", "0000", "0005", 'server')
    print(model)
    intTCStartTime = time.monotonic()
    intCntr = 0
    # Open Text file to write the light parameters
    oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter
    while True:
        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Active Light Brightness validation Counter: ' + str(intCntr))

        oBrightnessList = []
        for oRow in context.table:
            strBrightnesValue = oRow['BrightnessValue']
            intTimeLapse = int(oRow['TimeLapse'])

            print(strBrightnesValue, strBrightnesValue, "\n")
            print("myNodeId", myNodeId)

            if "ON" in strBrightnesValue.upper():
                AT.onOff(myNodeId, "01", 0, 1)
                context.reporter.ReportEvent('Test Validation',
                                             "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            elif "OFF" in strBrightnesValue.upper():
                AT.onOff(myNodeId, "01", 0, 0)
                context.reporter.ReportEvent('Test Validation',
                                             "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            else:
                strBrightnesValue = int(strBrightnesValue)
                # hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
                intTimeLapseRep = '{:04x}'.format(intTimeLapse)
                respState, respCode, respValue = AT.moveToLevel(myNodeId, "01", 0, int(strBrightnesValue),
                                                                int(intTimeLapseRep))
                print(intCntr, respState, respCode, respValue)
                context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(
                    strBrightnesValue) + "</B>", "Done")
                # Validate Lux
            time.sleep(5)
            if strBrightnesValue in lightSensorCalibration:
                intLowLimit = lightSensorCalibration[strBrightnesValue][0]
                intHighLimit = lightSensorCalibration[strBrightnesValue][1]
                sensorValue, _, _ = utils.get_lux_value()
                if intLowLimit < sensorValue < intHighLimit:
                    context.reporter.ReportEvent('Test Validation',
                                                 "The measured LUX value for Active light Brightness is: <B>" + str(
                                                     sensorValue) + "</B>. Which is within the calibration limit: " + str(
                                                     intLowLimit) + " - " + str(intHighLimit), "PASS")
                else:
                    context.reporter.ReportEvent('Test Validation',
                                                 "The measured LUX value for Active light Brightness is: <B>" + str(
                                                     sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(
                                                     intLowLimit) + " - " + str(intHighLimit), "FAIL")
                    boolPass = False

                if not strBrightnesValue in oBrightnessList:
                    oBrightnessList.append(strBrightnesValue)
                    strParameterValue = strParameterValue + "," + str(sensorValue)
            else:
                if not ("ON" in str(strBrightnesValue).upper() or "OFF" in str(strBrightnesValue).upper()):
                    context.reporter.ReportEvent('Test Validation',
                                                 "The Brightness values should be in multiples of 20", "FAIL")
            time.sleep(intTimeLapse + 2)

        # Update Text file
        oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
        oFileWriter.write(strParameterValue + "\n")
        oFileWriter.close()
        del oFileWriter

        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
        intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
        intSeconds = intMin * 60.0 + intSeconds

        if not boolInfiniteExec:
            if intSeconds > intMaxExecSeconds:
                return


@when(
    u'The ActiveLight is switched ON and OFF state and brightness of the light is varied to {Brightness} and validated {Duration} with timelapse of {Timelapse} second via telegesis')
def activeLightSpecificBrightnessValidation(context, Duration, Brightness, Timelapse):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        intMaxExecSeconds = int(Duration) * 60

    oColorTempList = {0: 2700,
                      20: 3460,
                      40: 4220,
                      50: 4600,
                      60: 4980,
                      80: 5740,
                      100: 6500}

    oColorTempPercentageList = list(oColorTempList.keys())
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    # Get Model
    _, _, model = AT.getAttribute(myNodeId, "01", "0000", "0005", 'server')
    print(model)
    intTCStartTime = time.monotonic()
    intCntr = 0
    oBrightnessList = []
    # Open Text file to write the light parameters
    oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter
    strParameterValue = ""
    intCntr = 0
    strParameterValue = str(intCntr)
    strBrightnesValue = Brightness
    intTimeLapse = int(Timelapse)
    if "TWBULB01" in model.upper():
        intTempCntr = intCntr % 5
        print(intTempCntr)
        myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]
        AT.colourTemperature(myNodeId, "01", 0, myColourTemp, 0)
        context.reporter.ReportEvent('Test Validation',
                                     "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>",
                                     "Done")
        strParameterValue = strParameterValue + "," + str(myColourTemp)

        print(strBrightnesValue, strBrightnesValue, "\n")
        print("myNodeId", myNodeId)

        if "ON" in strBrightnesValue.upper():
            AT.onOff(myNodeId, "01", 0, 1)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
        elif "OFF" in strBrightnesValue.upper():
            AT.onOff(myNodeId, "01", 0, 0)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
        else:
            strBrightnesValue = int(strBrightnesValue)
            # hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
            intTimeLapseRep = '{:04x}'.format(intTimeLapse)
            respState, respCode, respValue = AT.moveToLevel(myNodeId, "01", 0, int(strBrightnesValue),
                                                            int(intTimeLapseRep))
            print(intCntr, respState, respCode, respValue)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light Brightness is set to : <B>" + str(strBrightnesValue) + "</B>",
                                         "Done")
    if "FWBULB01" in model.upper():
        intTempCntr = intCntr % 5

        if "ON" in strBrightnesValue.upper():
            AT.onOff(myNodeId, "01", 0, 1)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
        elif "OFF" in strBrightnesValue.upper():
            AT.onOff(myNodeId, "01", 0, 0)
            context.reporter.ReportEvent('Test Validation',
                                         "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
        else:
            strBrightnesValue = int(strBrightnesValue)
            # hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
            intTimeLapseRep = '{:04x}'.format(intTimeLapse)
            respState, respCode, respValue = AT.moveToLevel(myNodeId, "01", 0, int(strBrightnesValue),
                                                            int(intTimeLapseRep))
            context.reporter.ReportEvent('Test Validation',
                                         "Active light Brightness is set to : <B>" + str(strBrightnesValue) + "</B>",
                                         "Done")
    while True:
        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Active Light Brightness validation Counter: ' + str(intCntr))

        # Validate Lux
        time.sleep(5)
        if strBrightnesValue in lightSensorCalibration:
            intLowLimit = lightSensorCalibration[strBrightnesValue][0]
            intHighLimit = lightSensorCalibration[strBrightnesValue][1]
            sensorValue, _, _ = utils.get_lux_value()
            if intLowLimit < sensorValue < intHighLimit:
                context.reporter.ReportEvent('Test Validation',
                                             "The measured LUX value for Active light Brightness is: <B>" + str(
                                                 sensorValue) + "</B>. Which is within the calibration limit: " + str(
                                                 intLowLimit) + " - " + str(intHighLimit), "PASS")
            else:
                context.reporter.ReportEvent('Test Validation',
                                             "The measured LUX value for Active light Brightness is: <B>" + str(
                                                 sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(
                                                 intLowLimit) + " - " + str(intHighLimit), "FAIL")
                boolPass = False

            if not strBrightnesValue in oBrightnessList:
                oBrightnessList.append(strBrightnesValue)
                strParameterValue = strParameterValue + "," + str(sensorValue)
        else:
            if not ("ON" in strBrightnesValue.upper() or "OFF" in strBrightnesValue.upper()):
                context.reporter.ReportEvent('Test Validation', "The Brightness values should be in multiples of 20",
                                             "FAIL")
        time.sleep(intTimeLapse + 2)

        # Update Text file
        oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
        oFileWriter.write(strParameterValue + "\n")
        oFileWriter.close()
        del oFileWriter

        intTCEndTime = time.monotonic()
        strTCDuration = str((timedelta(seconds=intTCEndTime - intTCStartTime)).strftime('%H:%M:%S'))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
        intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
        intSeconds = intMin * 60.0 + intSeconds

        if not boolInfiniteExec:
            if intSeconds > intMaxExecSeconds:
                return


@when(u'The hue value of the bulb is changed and validated for the given hue value {Duration} via telegesis')
def RGBColorValidation(context, Duration):
    boolInfiniteExec = False
    print(Duration.upper() + "\n")
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        intMaxExecSeconds = int(Duration) * 60

    AT.debug = True

    AT.stopThread.clear()
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    intTCStartTime = time.monotonic()

    myEp = '01'
    sat = 'Fe'
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    intCntr = 0
    while True:
        intCntr = intCntr + 1

        context.reporter.HTML_TC_BusFlowKeyword_Initialize('RGB Light HUE validation Counter: ' + str(intCntr))

        for oRow in context.table:
            hexHue = oRow['HueValue']
            print(hexHue)
            context.reporter.ReportEvent('Test Validation',
                                         "RGB light is set to Color Hue : <B>" + str(hexHue) + "</B>", "Done")
            respState, respCode, respValue = utils.changeSatOrColorHue(context, myNodeId, myEp, hexHue, sat,
                                                                       myDuration='0000')
            strHeader = 'Hue Validation' + "$$" + 'Color Expected' + "$$" + 'Color actual' + "$$" + '@@@'
            valueRow = "Value" + "$$" + str(hexHue) + "$$" + str(hexHue)

            if respState == True and str(respValue).split(",")[4] == "00":
                strResult = strHeader + valueRow
                context.reporter.ReportEvent("Test Validation", strResult, "PASS", "CENTER")
            else:
                strResult = strHeader + valueRow
                context.reporter.ReportEvent("Test Validation", "||" + strResult, "FAIL", "CENTER")
            time.sleep(int(oRow['TimeLapse']))
        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
        intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
        intSeconds = intMin * 60.0 + intSeconds
        if not boolInfiniteExec:
            if intSeconds > intMaxExecSeconds:
                return


@when(u'The hue value of the bulb is changed and validated for the given saturation value {Duration} via telegesis')
def RGBColorValidation(context, Duration):
    boolInfiniteExec = False
    print(Duration.upper() + "\n")
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        intMaxExecSeconds = int(Duration) * 60

    AT.debug = True

    AT.stopThread.clear()
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    intTCStartTime = time.monotonic()

    myEp = '01'
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    intCntr = 0

    # getting current Hue
    respState, respCode, respValue = utils.readAttribute("MANUFACTURER", myNodeId, myEp, 0, '0300', '0000')
    hue = str(respValue).split(",")[5]
    while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'RGB Light Saturation validation Counter: ' + str(intCntr))
        for oRow in context.table:
            SatValue = oRow['SatValue']
            print(SatValue)
            context.reporter.ReportEvent('Test Validation',
                                         "RGB light is set to Color Saturation : <B>" + str(
                                             SatValue) + " for Color Hue " + hue + "</B>", "Done")
            respState, respCode, respValue = utils.changeSatOrColorHue(context, myNodeId, myEp, hue, SatValue,
                                                                       myDuration='0000')
            strHeader = 'Saturation Validation' + "$$" + 'Saturation Expected' + "$$" + 'Saturation actual' + "$$" + '@@@'
            valueRow = "Value" + "$$" + str(SatValue) + "$$" + str(SatValue)
            if respState == True and str(respValue).split(",")[4] == "00":
                strResult = strHeader + valueRow
                context.reporter.ReportEvent("Test Validation", strResult, "PASS", "CENTER")
            else:
                strResult = strHeader + valueRow
                context.reporter.ReportEvent("Test Validation", "||" + strResult, "FAIL", "CENTER")
            time.sleep(int(oRow['TimeLapse']))

        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
        intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
        intSeconds = intMin * 60.0 + intSeconds
        if not boolInfiniteExec:
            if intSeconds > intMaxExecSeconds:
                return


@when(u'The hue value of the rgb bulb is changed and validated for the given saturation value {Duration} via telegesis')
def ChangeHueAndSaturation(context, Duration):
    boolInfiniteExec = False
    print(Duration.upper() + "\n")
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        intMaxExecSeconds = int(Duration) * 60

    AT.debug = True

    AT.stopThread.clear()
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    intTCStartTime = time.monotonic()

    myEp = '01'
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    intCntr = 0
    while True:
        intCntr = intCntr + 1

        context.reporter.HTML_TC_BusFlowKeyword_Initialize('RGB Light HUE validation Counter: ' + str(intCntr))

        for oRow in context.table:
            hexHue = oRow['HueValue']
            context.reporter.ReportEvent('Test Validation',
                                         "RGB light is set to Color Hue : <B>" + str(hexHue) + "</B>", "Done")
            for tRow in context.table:
                print(hexHue)
                satValue = tRow['SatValue']
                respState, respCode, respValue = utils.changeSatOrColorHue(context, myNodeId, myEp, hexHue, satValue,
                                                                           myDuration='0000')
                strHeader = 'Hue ' + "$$" + 'Sat Expected' + "$$" + 'Sat actual' + "$$" + '@@@'
                valueRow = hexHue + "$$" + satValue + "$$" + satValue

                if respState == True and str(respValue).split(",")[4] == "00":
                    strResult = strHeader + valueRow
                    context.reporter.ReportEvent("Test Validation", strResult, "PASS", "CENTER")
                else:
                    strResult = strHeader + valueRow
                    context.reporter.ReportEvent("Test Validation", "||" + strResult, "FAIL", "CENTER")
                time.sleep(int(oRow['TimeLapse']))
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
            intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
            intSeconds = intMin * 60.0 + intSeconds
            if not boolInfiniteExec:
                if intSeconds > intMaxExecSeconds:
                    return


@when(
    u'The hue value of the {strDeviceType} is changed and validated for the given saturation and brightness value {Duration} via telegesis')
def ChangeHueAndSaturation(context, strDeviceType, Duration):
    boolInfiniteExec = False
    print(Duration.upper() + "\n")
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        intMaxExecSeconds = int(Duration) * 60

    AT.debug = True

    AT.stopThread.clear()
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    intTCStartTime = time.monotonic()
    if "SLP" in str(strDeviceType).upper():
        myEp = "09"
    elif "BULB" in str(strDeviceType).upper():
        myEp = "01"

    # _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
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
    intCntr = 0
    while True:
        intCntr = intCntr + 1

        context.reporter.HTML_TC_BusFlowKeyword_Initialize('RGB Light HUE validation Counter: ' + str(intCntr))

        for oRow in context.table:
            hexHue = oRow['HueValue']
            context.reporter.ReportEvent('Test Validation',
                                         "RGB light is set to Color Hue : <B>" + str(hexHue) + "</B>", "Done")
            for tRow in context.table:
                satValue = tRow['SatValue']
                context.reporter.ReportEvent('Test Validation',
                                             "RGB light is set to Sat  : <B>" + str(satValue) + "</B>", "Done")
                for thirdRaw in context.table:
                    print(hexHue)
                    Brightness = thirdRaw['Brightness']
                    intTimeLapse = int(oRow['TimeLapse'])
                    respState, respCode, respValue = utils.changeSatOrColorHue(context, myNodeId, myEp, hexHue,
                                                                               satValue, myDuration='0000')
                    respStateForBrightness, respCodeForBrightness, respValueForBrightness = AT.moveToLevel(myNodeId,
                                                                                                           "01", 0, int(
                            Brightness),
                                                                                                           int(
                                                                                                               intTimeLapse))
                    strHeader = 'Hue Set' + "$$" + 'Hue Actual' + "$$" + 'Sat Set' + "$$" + 'Sat actual' + "$$" + 'Brightness Set' + "$$" + 'Brightness actual' + '@@@'
                    # valueRow = hexHue + "$$" + satValue + "$$" + satValue +"$$" +Brightness +"$$" +Brightness
                    count = 0
                    while count <= 6:
                        time.sleep(10)
                        Brightness = thirdRaw['Brightness']
                        HueValue, SatValue, BrightnessValue = utils.validateHueSatBrightness(context, myNodeId, myEp)
                        Brightness = int(Brightness)
                        Brightness = (Brightness / 100 * 255)
                        # BrightnessInHex='{:02x}'.format(Brightness)
                        BrightnessInHex = hex(int(Brightness)).split('x')[-1]

                        if hexHue == HueValue and satValue == SatValue and BrightnessInHex.upper() == BrightnessValue:
                            valueRow = hexHue + "$$" + HueValue + "$$" + satValue + "$$" + SatValue + "$$" + str(
                                BrightnessInHex).upper() + "$$" + BrightnessValue
                            strResult = strHeader + valueRow
                            context.reporter.ReportEvent("Test Validation", strResult, "PASS", "CENTER")
                        else:
                            HueResult = HueValue
                            SatResult = SatValue
                            BrightnessResult = BrightnessValue

                            if not hexHue == HueValue:
                                HueResult = "||" + HueValue
                                valueRow = hexHue + "$$" + HueResult + "$$" + satValue + "$$" + SatValue + "$$" + str(
                                    BrightnessInHex).upper() + "$$" + BrightnessValue
                                strHeader = 'Hue Set' + "$$" + "||" + 'Hue Actual' + "$$" + 'Sat Set' + "$$" + 'Sat actual' + "$$" + 'Brightness Set' + "$$" + 'Brightness actual' + '@@@'
                            elif not satValue == SatValue:
                                SatResult = "||" + SatValue
                                valueRow = hexHue + "$$" + HueResult + "$$" + SatResult + "$$" + SatResult + "$$" + str(
                                    BrightnessInHex).upper() + "$$" + BrightnessValue
                                strHeader = 'Hue Set' + "$$" + 'Hue Actual' + "$$" + 'Sat Set' + "$$" + "||" + 'Sat actual' + "$$" + 'Brightness Set' + "$$" + 'Brightness actual' + '@@@'
                            elif not BrightnessInHex.upper() == BrightnessValue:
                                BrightnessResult = "||" + BrightnessValue
                                valueRow = hexHue + "$$" + HueResult + "$$" + SatResult + "$$" + SatValue + "$$" + str(
                                    BrightnessInHex).upper() + "$$" + BrightnessResult
                                strHeader = 'Hue Set' + "$$" + 'Hue Actual' + "$$" + 'Sat Set' + "$$" + 'Sat actual' + "$$" + 'Brightness Set' + "$$" + "||" + 'Brightness actual' + '@@@'

                            strResult = strHeader + valueRow
                            context.reporter.ReportEvent("Test Validation", strResult, "FAIL", "CENTER")
                            count = count + 1
                        time.sleep(int(oRow['TimeLapse']))

                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
                intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
                intSeconds = intMin * 60.0 + intSeconds
                if not boolInfiniteExec:
                    if intSeconds > intMaxExecSeconds:
                        return
        break


@when(u'The Tune value of the TW bulb is changed and validated for the given Brightness value {Duration} via telegesis')
def ChangeTuneAndBrightness(context, Duration):
    boolInfiniteExec = False
    print(Duration.upper() + "\n")
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        intMaxExecSeconds = int(Duration) * 60

    AT.debug = True

    AT.stopThread.clear()
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    intTCStartTime = time.monotonic()

    myEp = '01'
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    intCntr = 0
    while True:
        intCntr = intCntr + 1

        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'TW Light Tune and Brightness validation Counter: ' + str(intCntr))

        for oRow in context.table:
            tuneValue = oRow['Tune']
            respState, respCode, respValue = utils.changeTune(context, myNodeId, myEp, tuneValue, myDuration='0000')
            context.reporter.ReportEvent('Test Validation',
                                         "TW light is set to Tune : <B>" + str(tuneValue) + "</B>", "Done")
            for tRow in context.table:
                print(tuneValue)
                brightnessValue = tRow['BrightnessValue']
                intTimeLapse = tRow['TimeLapse']
                if "ON" in brightnessValue:
                    AT.onOff(myNodeId, "01", 0, 1)
                    context.reporter.ReportEvent('Test Validation',
                                                 "Active light is set to : <B>" + str(brightnessValue) + "</B>",
                                                 "Done")
                elif "OFF" in brightnessValue:
                    AT.onOff(myNodeId, "01", 0, 0)
                    context.reporter.ReportEvent('Test Validation',
                                                 "Active light is set to : <B>" + str(brightnessValue) + "</B>",
                                                 "Done")
                else:
                    respStateForBrightness, respCodeForBrightness, respValueForBrightness = AT.moveToLevel(myNodeId,
                                                                                                           "01", 0, int(
                            brightnessValue), int(intTimeLapse))
                    context.reporter.ReportEvent('Test Validation',
                                                 "Active light is set to : <B>" + str(brightnessValue) + "</B>",
                                                 "Done")
                    intCounter = 0

                    strHeader = 'TuneValue Expected ' + "$$" + 'TuneValue Actual' + "$$" + 'BrightnessValue Expected' + "$$" + 'BrightnessValue actual' + "$$" + '@@@'
                    brightnessValue = int(brightnessValue)
                    brightnessValue = int(brightnessValue / 100 * 255)
                    print(brightnessValue)
                    while intCounter < 6:
                        time.sleep(10)
                        BrightnessResult, TuneResult = utils.validateTuneBrightness(context, myNodeId, myEp)
                        BrightnessResult = int(BrightnessResult, 16)
                        print(BrightnessResult)
                        if brightnessValue == BrightnessResult and str(TuneResult) == str(tuneValue):
                            valueRow = tuneValue + "$$" + TuneResult + "$$" + str(brightnessValue) + "$$" + str(
                                BrightnessResult)
                            strResult = strHeader + valueRow
                            context.reporter.ReportEvent("Test Validation", strResult, "PASS", "CENTER")
                        else:
                            valueRow = tuneValue + "$$" + TuneResult + "$$" + str(brightnessValue) + "$$" + str(
                                BrightnessResult)
                            strResult = strHeader + valueRow
                            context.reporter.ReportEvent("Test Validation", strResult, "FAIL", "CENTER")
                        intCounter = intCounter + 1

                    time.sleep(int(oRow['TimeLapse']))
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
                intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
                intSeconds = intMin * 60.0 + intSeconds
                if not boolInfiniteExec:
                    if intSeconds > intMaxExecSeconds:
                        return
                    break
        break


@when(
    u'The brightness value of the FW bulb is changed and validated for the given Brightness value {Duration} via telegesis')
def ChangeTuneAndBrightness(context, Duration):
    boolInfiniteExec = False
    print(Duration.upper() + "\n")
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else:
        intMaxExecSeconds = int(Duration) * 60

    AT.debug = True

    AT.stopThread.clear()
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    intTCStartTime = time.monotonic()

    myEp = '01'
    _, _, myNodeId = utils.discoverNodeIDbyCluster("0000")
    intCntr = 0
    while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'FW Light Brightness validation Counter: ' + str(intCntr))

        for tRow in context.table:
            brightnessValue = tRow['BrightnessValue']
            intTimeLapse = tRow['TimeLapse']
            if "ON" in brightnessValue:
                AT.onOff(myNodeId, "01", 0, 1)
                context.reporter.ReportEvent('Test Validation',
                                             "Active light is set to : <B>" + str(brightnessValue) + "</B>",
                                             "Done")
            elif "OFF" in brightnessValue:
                AT.onOff(myNodeId, "01", 0, 0)
                context.reporter.ReportEvent('Test Validation',
                                             "Active light is set to : <B>" + str(brightnessValue) + "</B>",
                                             "Done")
            else:
                respStateForBrightness, respCodeForBrightness, respValueForBrightness = AT.moveToLevel(myNodeId, "01",
                                                                                                       0, int(
                        brightnessValue), int(intTimeLapse))
                context.reporter.ReportEvent('Test Validation',
                                             "Active light is set to : <B>" + str(brightnessValue) + "</B>", "Done")
                intCounter = 0
                strHeader = 'BrightnessValue Expected' + "$$" + 'BrightnessValue actual' + "$$" + '@@@'
                brightnessValue = int(brightnessValue)
                brightnessValue = int(brightnessValue / 100 * 255)
                print(brightnessValue)
                while intCounter < 6:
                    time.sleep(10)
                    BrightnessState, BrightnessCode, BrightnessResult = utils.readAttribute("MANUFACTURER", myNodeId,
                                                                                            myEp, 0, '0008', '0000')
                    BrightnessValue = str(BrightnessResult).split(',')[5]
                    BrightnessResult = int(BrightnessValue, 16)
                    print(BrightnessResult)
                    if brightnessValue == BrightnessResult:
                        valueRow = str(brightnessValue) + "$$" + str(BrightnessResult)
                        strResult = strHeader + valueRow
                        context.reporter.ReportEvent("Test Validation", strResult, "PASS", "CENTER")
                    else:
                        valueRow = str(brightnessValue) + "$$" + str(BrightnessResult)
                        strResult = strHeader + valueRow
                        context.reporter.ReportEvent("Test Validation", strResult, "FAIL", "CENTER")
                    intCounter = intCounter + 1
            time.sleep(int(tRow['TimeLapse']))
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
            intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
            intSeconds = intMin * 60.0 + intSeconds
            if not boolInfiniteExec:
                if intSeconds > intMaxExecSeconds:
                    return
        break
def setTemperature(context, myNodeId, oColor):
    try:
        myColourTemp = dutils.oColorTempList[oColor]
        AT.colourTemperature(myNodeId, "01", 0, myColourTemp,0,context, "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>")
        return myColourTemp
    except Exception as e:
        print(e)

@when(
    u'The {ActiveLightDevice} is switched ON and OFF state and brightness of the light is varied {times}min and validated for the below brightness values {strDuration} via TGStick')
def validateActiveLightFunctionViaTGstick(context, ActiveLightDevice, times, strDuration):

    print("step implemetation for TG stick LUX Test")
    oColorTempList = {0: 2700,
                      96: 3460,
                      97: 4220,
                      98: 4980,
                      99: 5740,
                      100: 6500}
    oColorTempPercentageList = list(oColorTempList.keys())

    # get node lists
    #nodeIdList = utils.getNodeList()
    nodeId=dutils.getNodeIDbyDeciveID(ActiveLightDevice)
    context.nodeId=nodeId
    strLightNodeID=nodeId
    print(strLightNodeID)
    try:

        '''print("nodeIdlist", nodeIdList)
        strLightNodeID = ""
        print(nodeIdList)
        if 'ActiveLight' in ActiveLightDevice:
            if 'FWBulb01_1' in nodeIdList:
                strLightNodeID = nodeIdList['FWBulb01_1']["nodeID"]
            elif 'LDS_DimmerLight_1' in nodeIdList:
                strLightNodeID = nodeIdList['LDS_DimmerLight_1']["nodeID"]
            elif 'FWBulb03UK_1' in nodeIdList:
                print('inside FWBulb03UK')
                strLightNodeID = nodeIdList['FWCLBulb03UK_1']["nodeID"]
            elif 'TWGU10Bulb03UK_1' in nodeIdList:
                print('inside RGB')
                strLightNodeID = nodeIdList['TWGU10Bulb03UK_1']["nodeID"]
            elif 'TWBulb03UK_1' in nodeIdList:
                print('inside RGB')
                strLightNodeID = nodeIdList['TWBulb03UK_1']["nodeID"]
            elif 'RGBBulb03UK_1' in nodeIdList:
                print('inside RGB')
                strLightNodeID = nodeIdList['RGBBulb03UK_1']["nodeID"]
            elif 'RGBBulb02UK_1' in nodeIdList:
                print('inside RGB')
                strLightNodeID = nodeIdList['RGBBulb02UK_1']["nodeID"]
        elif ActiveLightDevice in nodeIdList:
            strLightNodeID = nodeIdList[ActiveLightDevice]["nodeID"]
        else:
            context.reporter.ReportEvent('Test Validation', "Active light Node is missing.", "FAIL")
            return False '''

        intCntr = 0
        count = 0
        print("Storage folder " + str(context.reporter.strCurrentTXTFolder))
        # Open Text file to write the light parameters
        oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'w')
        oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
        oFileWriter.close()
        del oFileWriter

        while count < 1:
            #ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
            #session = ALAPI.sessionObjectV6dot5()

            strParameterValue = ""
            intCntr = intCntr + 1
            strParameterValue = str(intCntr)
            boolPass = True
            context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                'Active Light Brightness validation Counter: ' + str(intCntr))

            if "RS 227" in ActiveLightDevice.upper():
                print("TW Bulb Temperature Settings")
                print(strLightNodeID)

                intTempCntr = intCntr % 5
                myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]
                AT.colourTemperature(strLightNodeID, "01", 0, myColourTemp,0)

                #ALAPI.setActiveLightColourTemperature(session, strLightNodeID, myColourTemp)
                print("lightTemperature", myColourTemp)
                context.reporter.ReportEvent('Test Validation',
                                             "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>",
                                             "Done")
                strParameterValue = strParameterValue + "," + str(myColourTemp)

            # Set Light ON
            #ALAPI.setActiveLightState(session, strLightNodeID, "ON")
            #AT.onOff(strLightNodeID,'01',0,1)
            print("LIght node ID", strLightNodeID)
            context.reporter.ReportEvent('Test Validation', "Active light is switched <B>ON</B>", "PASS")
            time.sleep(5)
            oBrightnessList = []
            # ChangeBrightness
            for oRow in context.table:
                intBrightness = int(oRow['BrightnessValue'])
                print("Brightness percentage value \t" + oRow['BrightnessValue'])
                #ALAPI.setActiveLightBrightness(session, strLightNodeID, intBrightness)
                AT.moveToLevel(strLightNodeID, "01", 0, int(intBrightness),0 )
                context.reporter.ReportEvent('Test Validation',
                                             "Active light Brightness is set to : <B>" + str(intBrightness) + "</B>",
                                             "Done")
                time.sleep(2)
                luxSpikeTest = False
                if intBrightness in lightSensorCalibration:
                    if '0' not in times.upper():
                        luxSpikeTest = True
                    if luxSpikeTest is True:
                        for x in range(5):
                            print('inside Spike test sample count:' + str(x))
                            intLowLimit = lightSensorCalibration[intBrightness][0]
                            intHighLimit = lightSensorCalibration[intBrightness][1]
                            time.sleep(5)
                            print("sleepingggggg")

                            sensorValue, _, _ = utils.get_lux_value()
                            if intLowLimit < sensorValue < intHighLimit:
                                context.reporter.ReportEvent('Test Validation',
                                                             "The measured LUX value for Active light Brightness is: <B>" + str(
                                                                 sensorValue) + "</B>. Which is within the calibration limit: " + str(
                                                                 intLowLimit) + " - " + str(intHighLimit), "PASS")
                            else:
                                context.reporter.ReportEvent('Test Validation',
                                                             "The measured LUX value for Active light Brightness is: <B>" + str(
                                                                 sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(
                                                                 intLowLimit) + " - " + str(intHighLimit), "FAIL")
                                boolPass = False

                            if not intBrightness in oBrightnessList:
                                # oBrightnessList.append(intBrightness)
                                strParameterValue = str(intBrightness) + "," + str(sensorValue)
                                print("inside writing counter", strParameterValue)
                                print("Storage folder " + str(context.reporter.strCurrentTXTFolder))
                                oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
                                print("inside file", strParameterValue)
                                oFileWriter.write(strParameterValue + "\n")
                                oFileWriter.close()
                                del oFileWriter
                            try:
                                time.sleep(5)
                            except RuntimeError as err:
                                print("error", err)
                    else:
                        print('NoSPIKEEE')
                        intLowLimit = lightSensorCalibration[intBrightness][0]
                        intHighLimit = lightSensorCalibration[intBrightness][1]
                        # time.sleep(1800)
                        #                         print("sleepingggggg 30mins")
                        sensorValue, _, _ = utils.get_lux_value()
                        if intLowLimit < sensorValue < intHighLimit:
                            context.reporter.ReportEvent('Test Validation',
                                                         "The measured LUX value for Active light Brightness is: <B>" + str(
                                                             sensorValue) + "</B>. Which is within the calibration limit: " + str(
                                                             intLowLimit) + " - " + str(intHighLimit), "PASS")
                        else:
                            context.reporter.ReportEvent('Test Validation',
                                                         "The measured LUX value for Active light Brightness is: <B>" + str(
                                                             sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(
                                                             intLowLimit) + " - " + str(intHighLimit), "FAIL")
                            boolPass = False

                        if not intBrightness in oBrightnessList:
                            oBrightnessList.append(intBrightness)
                            strParameterValue = str(intBrightness) + "," + str(sensorValue)
                            print("inside writing counter", strParameterValue)
                            oFileWriter = open(context.reporter.strCurrentTXTFolder + "LUXvsTEMP.txt", 'a')
                            print("Storage folder " + str(context.reporter.strCurrentTXTFolder))
                            print("inside file", strParameterValue)
                            oFileWriter.write(strParameterValue + "\n")
                            oFileWriter.close()
                            del oFileWriter

                else:
                    context.reporter.ReportEvent('Test Validation', "The Brightness values should be in multiples of 20",
                                                 "FAIL")

            # Update Text file

            # Update the Pass and Fail counters
            context.reporter.intIterationCntr = intCntr
            if boolPass:
                context.reporter.intIterationPassCntr = context.reporter.intIterationPassCntr + 1
            else:
                context.reporter.intIterationFailCntr = context.reporter.intIterationFailCntr + 1

            # Set Light OFF
            #ALAPI.setActiveLightState(session, strLightNodeID, "OFF")
            AT.onOff(strLightNodeID, '01', 0, 0)
            context.reporter.ReportEvent('Test Validation', "Active Plug is switched <B>OFF</B>", "PASS")
            # time.sleep(5)
            #ALAPI.deleteSessionV6(session)
            break
        count = 3
    except Exception as e:
        print(e)

