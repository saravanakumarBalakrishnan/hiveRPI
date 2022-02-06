import FF_device_utils as dutils
from behave import *
import FF_threadedSerial as AT
import FF_convertTimeTemperature as tt
import time
import FF_OCRUtils as oUtils
import FF_utils as utils
import FF_alertmeApi as ALAPI
import CC_thermostatModule as CTM
import BB_ReusableFunctionModule as rFM
from datetime import datetime, timedelta
import FF_ScheduleUtils as oSchdUtil


def OCRprerequisite(context, strDeviceType, fastPoll=True):
    '''try:
        AT.stopThreads()
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
    except:
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)'''

    global myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting Fast Poll on the thermostat")
    if "devices" not in strDeviceType:
        # macId = dutils.getDeviceMACWithModel(strDeviceType,True)
        myNodeId = dutils.getDeviceNodeAndEPWithDeviceType(strDeviceType, True)
        context.nodeId = myNodeId
        myEp = dutils.getDeviceEPWithModel(strDeviceType, True)
        context.myEPList = myEp
    context.nodeId = myNodeId
    context.reporter.ReportEvent("Event Log", "Started setting fast poll", "Done")
    ep = context.myEPList[0]
    if fastPoll is True:
        _, _ = AT.setCompletFastPoll(myNodeId, ep)
        time.sleep(5)
        respSate = AT.setFastPoll()
    else:
        respSate = True
    return myNodeId, ep, respSate


@when(u'the {strType} {strMode} is activated using button on the {strLang} {strDeviceType} for {strDuration}')
def activateBoostDuration(context, strType, strMode, strLang, strDeviceType, strDuration):
    # boost_Timer = {1:0,2:1,3:2,3:4,4:5,5:6}
    global ep, myEp, myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Activate ' + strType + ' ' + strMode + ' mode on the thermostat')
    intDuration = 0
    if 'HOUR' in str(strDuration).upper():
        intDuration = int(str(strDuration).split(" ")[0])
    myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, strType, context, strLang)
    strOverrideTemp = ""
    if "OVERRIDE" in str(strDeviceType).upper():
        strOverrideTemp = str(strDeviceType).split(" ")[2]
    strMode = oUtils.getModeText(strMode, strType, oLang)
    respSate = AT.setFastPoll()

    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if str(strType).upper() == 'HEAT':
            context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                'Set heat mode on the thermostat')
            if str(strMode).upper() == 'BOOST':
                mySetpoint = 22
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(5)
                oImgWake, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Top Right", "Press")
                time.sleep(1)
                oImgBoost, imgBoostName = oUtils.captureOriginal(context)
                for i in range(0, intDuration):
                    dutils.pressDeviceButton(myNodeId, ep, "Top Right", "Press")
                    time.sleep(1)

                _, _ = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(3)

                oImgHome, imgHomeName = oUtils.capture(context)

                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Tick Button", "Done",
                                             ocrImagePath=imgWakeName)
                Mode = oUtils.getText(oImgWake, context)
                Mode = str(Mode).replace("0FF", "OFF").replace("0N", "ON")
                oUtils.printModesHome(Mode, context, oLang)
                context.reporter.ReportEvent("Event Log", "Heat Boost Button is pressed", "Done",
                                             ocrImagePath=imgBoostName)

                oUtils.validateHeatBoostScreen(oImgBoost, imgBoostName, oLang, context)

                Mode = oUtils.getText(oImgHome, context)
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in heat:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgHomeName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[3] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgHomeName)
                context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)
                context.oThermostatEP.model.mode = "BOOST"
        elif str(strType).upper() == 'HOTWATER':
            if str(strMode).upper() == 'BOOST':
                Mode, imgBoostName, oImgBoost, oImgHome, imgHomeName = dutils.waterBoost(context, myNodeId, ep)
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Heat Boost Button is pressed", "Done",
                                             ocrImagePath=imgBoostName)

                oUtils.validateHotBoostScreen(oImgBoost, imgBoostName, oLang, context)

                Mode = oUtils.getText(oImgHome, context)
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in hot:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgHomeName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[2] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgHomeName)
        elif str(strType).upper() == 'HOLIDAY':
            mySetpoint = 1.0
            holidayStartOffset = 60
            intSetTempDuration = 604800
            context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            oImgWake, imgWakeName = oUtils.captureOriginal(context)
            dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
            time.sleep(1)
            oImgMenu, imgMenuName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", 2)
            time.sleep(1)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done")
            oImgHolMenu, imgHolMenuName = oUtils.captureOriginal(context)
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is pressed to Holiday mode", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            strHoldayStart = (datetime.now() + timedelta(seconds=holidayStartOffset)).replace(second=0, microsecond=0)
            strUTCHoldayStart = (datetime.now() + timedelta(seconds=holidayStartOffset)).replace(second=0,
                                                                                                 microsecond=0)
            _, oImgHolFromMonName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Month", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromYearDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Year", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromHourDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Hour", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromMinuteDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Minute", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromDateConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Start Date", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To date", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToMonName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Month", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToYearDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To year", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToHourDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To hour", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToMinuteDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To minute", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToDateConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirm end date", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFrostName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To temperature", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirmation screen", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
            time.sleep(2)
            oImgHolWaterConfirm, oImgHolWaterConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirmation instruction screen", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
            time.sleep(5)
            oImg, oImgName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to save the holiday setting", "Done")

            context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                         ocrImagePath=imgWakeName)

            Mode = oUtils.getText(oImgWake, context)
            oUtils.printModesHome(Mode, context, oLang)

            context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                         ocrImagePath=imgMenuName)

            oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)

            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done",
                                         ocrImagePath=imgHolMenuName)

            oUtils.validateMainMenu(oImgHolMenu, imgHolMenuName, oLang, context)
            oImgHolFromDate = oUtils.loadImage(oImgHolFromDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is pressed to Holiday mode", "Done")
            oUtils.validateHolidayMenu(oImgHolFromDate, oImgHolFromDateName, oLang, context, "FROM", "DATE")
            oImgHolFromDate = None

            oImgHolFromMon = oUtils.loadImage(oImgHolFromMonName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Month", "Done")
            oUtils.validateHolidayMenu(oImgHolFromMon, oImgHolFromMonName, oLang, context, "FROM", "MONTH")
            oImgHolFromMon = None

            oImgHolFromYearDate = oUtils.loadImage(oImgHolFromYearDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Year", "Done")
            oUtils.validateHolidayMenu(oImgHolFromYearDate, oImgHolFromYearDateName, oLang, context, "FROM", "YEAR")
            oImgHolFromYearDate = None

            oImgHolFromHourDate = oUtils.loadImage(oImgHolFromHourDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Hour", "Done")
            oUtils.validateHolidayMenu(oImgHolFromHourDate, oImgHolFromHourDateName, oLang, context, "FROM", "HOUR")
            oImgHolFromHourDate = None

            oImgHolFromMinuteDate = oUtils.loadImage(oImgHolFromMinuteDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Minute", "Done")
            oUtils.validateHolidayMenu(oImgHolFromMinuteDate, oImgHolFromMinuteDateName, oLang, context, "FROM",
                                       "MINUTE")
            oImgHolFromMinuteDate = None

            oImgHolFromDateConfirm = oUtils.loadImage(oImgHolFromDateConfirmName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Start Date", "Done")
            oUtils.validateHolidayMenu(oImgHolFromDateConfirm, oImgHolFromDateConfirmName, oLang, context, "FROM",
                                       "CONFIRM")
            oImgHolFromDateConfirm = None

            oImgHolToDate = oUtils.loadImage(oImgHolToDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done")
            oUtils.validateHolidayMenu(oImgHolToDate, oImgHolToDateName, oLang, context, "To", "DATE")
            oImgHolToDate = None

            oImgHolToMon = oUtils.loadImage(oImgHolToMonName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Month", "Done")
            oUtils.validateHolidayMenu(oImgHolToMon, oImgHolToMonName, oLang, context, "To", "MONTH")
            oImgHolToMon = None

            oImgHolToYearDate = oUtils.loadImage(oImgHolToYearDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Year", "Done")
            oUtils.validateHolidayMenu(oImgHolToYearDate, oImgHolToYearDateName, oLang, context, "To", "YEAR")
            oImgHolToYearDate = None

            oImgHolToHourDate = oUtils.loadImage(oImgHolToHourDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Hour", "Done")
            oUtils.validateHolidayMenu(oImgHolToHourDate, oImgHolToHourDateName, oLang, context, "To", "HOUR")
            oImgHolToHourDate = None

            oImgHolToMinuteDate = oUtils.loadImage(oImgHolToMinuteDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Minute", "Done")
            oUtils.validateHolidayMenu(oImgHolToMinuteDate, oImgHolToMinuteDateName, oLang, context, "To", "MINUTE")
            oImgHolToMinuteDate = None

            oImgHolToDateConfirm = oUtils.loadImage(oImgHolToDateConfirmName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Start Date", "Done")
            oUtils.validateHolidayMenu(oImgHolToDateConfirm, oImgHolToDateConfirmName, oLang, context, "To", "CONFIRM")
            oImgHolToDateConfirm = None

            oImgHolFrost = oUtils.loadImage(oImgHolFrostName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Temperature", "Done")
            oUtils.validateHolidayMenu(oImgHolFrost, oImgHolFrostName, oLang, context, "TEMP")
            oImgHolFrost = None

            oImgHolConfirm = oUtils.loadImage(oImgHolConfirmName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirmation screen", "Done")
            oUtils.validateHolidayMenu(oImgHolConfirm, oImgHolConfirmName, oLang, context, "CONFIRM")

            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirmation instruction screen", "Done")
            oUtils.validateHolidayMenu(oImgHolWaterConfirm, oImgHolWaterConfirmName, oLang, context,
                                       "CONFIRMINSTRUCTION")

            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to save the holiday setting", "Done")

            Mode = oUtils.getText(oImg, context)
            _, _ = oUtils.printHolidayDurationHome(Mode, context, oLang)

            context.oThermostatEP.model.mode = "HOLIDAY"

            context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)

            strHoldayEnd = (strHoldayStart + timedelta(seconds=intSetTempDuration))
            context.oThermostatEP.model.holidayModeEnabled = '01'
            strUTCHoldayEnd = (strHoldayStart + timedelta(seconds=intSetTempDuration))
            context.strHoldayStart = strUTCHoldayStart
            context.strHoldayEnd = strUTCHoldayEnd

            startDateString = datetime.strftime(strHoldayStart, "%Y%m%d")
            startTimeString = datetime.strftime(strHoldayStart, "%H:%M")
            startTimeHex = tt.timeStringToHex(startTimeString)

            endDateString = datetime.strftime(strHoldayEnd, "%Y%m%d")
            endTimeString = datetime.strftime(strHoldayEnd, "%H:%M")
            endTimeHex = tt.timeStringToHex(endTimeString)

            context.oThermostatEP.model.holidayModeStart = context.oThermostatEP._buildHolidayDatetimeUTC(
                startDateString, startTimeHex)
            context.oThermostatEP.model.holidayModeEnd = context.oThermostatEP._buildHolidayDatetimeUTC(endDateString,
                                                                                                        endTimeHex)

        context.reporter.ReportEvent("Event Log", "Re-setting fast poll", "Done")
        AT.resetFastPoll(longPollInt, checkInInt, myNodeId, ep, context)
        context.oThermostatEP.update()
    else:
        context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")


@when(u'the {strType} {strMode} is activated using button on the {strLang} {strDeviceType}')
def activateBoost(context, strType, strMode, strLang, strDeviceType):
    global oImgMenu, ep, myEp, myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Activate ' + strType + ' ' + strMode + ' mode on the thermostat')
    myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, strType, context, strLang)
    if "OVERRIDE" in str(strDeviceType).upper():
        strOverrideTemp = str(strDeviceType).split(" ")[2]
    strMode = oUtils.getModeText(strMode, strType, oLang)
    respSate = AT.setFastPoll()
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if str(strType).upper() == 'HEAT':
            context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                'Set heat mode on the thermostat')
            if str(strMode).upper() == 'BOOST':
                mySetpoint = 22
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(3)
                _, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Top Right", "Press")
                time.sleep(1)
                _, imgBoostName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(1)

                _, _ = oUtils.captureOriginal(context)

                time.sleep(1)

                _, imgHomeName = oUtils.capture(context)

                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Tick Button", "Done",
                                             ocrImagePath=imgWakeName)
                oImgWake = oUtils.loadImage(imgWakeName, context)
                Mode = oUtils.getText(oImgWake, context)
                oImgWake = None
                Mode = str(Mode).replace("0FF", "OFF").replace("0N", "ON")
                oUtils.printModesHome(Mode, context, oLang)
                context.reporter.ReportEvent("Event Log", "Heat Boost Button is pressed", "Done",
                                             ocrImagePath=imgBoostName)
                oImgBoost = oUtils.loadImage(imgBoostName, context)
                oUtils.validateHeatBoostScreen(oImgBoost, imgBoostName, oLang, context)
                oImgBoost = None
                oImgHome = oUtils.loadImage(imgHomeName, context)
                Mode = oUtils.getText(oImgHome, context)
                oImgBoost = None
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in heat:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgHomeName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[3] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgHomeName)
                context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)
                context.oThermostatEP.model.mode = "BOOST"
            if str(strMode).upper() == 'OFF':
                mySetpoint = 1.0
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                time.sleep(3)
                _, imgWakeName = oUtils.captureOriginal(context)

                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                # time.sleep(1)
                _, imgMenuName = oUtils.captureOriginal(context)

                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)
                _, imgHeatName = oUtils.captureOriginal(context)

                dutils.rotateDial(myNodeId, ep, "CLOCKWISE", 2)
                time.sleep(1)
                _, imgOffName = oUtils.captureOriginal(context)

                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(1)
                _, imgOffModeName = oUtils.captureOriginal(context)

                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(1)
                _, imgName = oUtils.captureOriginal(context)

                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)
                oImgWake = oUtils.loadImage(imgWakeName, context)
                Mode = oUtils.getText(oImgWake, context)
                oImgWake = None
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)
                oImgMenu = oUtils.loadImage(imgMenuName, context)
                oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)
                oImgMenu = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgHeatName)
                oImgHeat = oUtils.loadImage(imgHeatName, context)
                oUtils.validateHeatMenu(oImgHeat, imgHeatName, oLang, context)
                oImgHeat = None
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Off mode", "Done",
                                             ocrImagePath=imgOffName)
                oImgOff = oUtils.loadImage(imgOffName, context)
                oUtils.validateHeatMenu(oImgOff, imgOffName, oLang, context)
                oImgOff = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgOffModeName)
                oImgOffMode = oUtils.loadImage(imgOffModeName, context)
                strHeatOffText = oUtils.getHeatOffScreenText(oImgOffMode, oLang)
                oImgOffMode = None
                context.reporter.ReportEvent("Event Log", "Heat off Text is displayed as <B>" + strHeatOffText + "</B>",
                                             "Done")
                context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done",
                                             ocrImagePath=imgName)
                oImg = oUtils.loadImage(imgName, context)
                Mode = oUtils.getText(oImg, context)
                oImg = None
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in heat:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[3] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgName)
                context.oThermostatEP.model.mode = "OFF"
                context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)
            if str(strMode).upper() == 'SCH':
                context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                _, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                time.sleep(1)
                _, imgMenuName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Menu is Pressed on Heat mode", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(1)
                _, imgHeatName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed on Heat mode", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(1)
                _, imgSchModeName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed on Schedule mode", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(1)
                _, imgResumeModeName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed on Resume schedule mode", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                context.reporter.ReportEvent("Event Log", "Confirm button is Pressed", "Done")
                time.sleep(3)
                _, imgName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)
                oImgWake = oUtils.loadImage(imgWakeName, context)
                Mode = oUtils.getText(oImgWake, context)
                oImgWake = None
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)
                oImgMenu = oUtils.loadImage(imgMenuName, context)

                oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)
                oImgMenu = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed to select Heat", "Done",
                                             ocrImagePath=imgHeatName)
                oImgHeat = oUtils.loadImage(imgHeatName, context)

                oUtils.validateHeatMenu(oImgHeat, imgHeatName, oLang, context)
                oImgHeat = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed to select Schedule", "Done",
                                             ocrImagePath=imgSchModeName)
                oImgSchMode = oUtils.loadImage(imgSchModeName, context)
                oUtils.validateHeatScheduleMenu(oImgSchMode, imgSchModeName, oLang, context)
                oImgSchMode = None

                context.reporter.ReportEvent("Event Log", "Dial is pressed to select Resume", "Done",
                                             ocrImagePath=imgResumeModeName)
                oImgResumeMode = oUtils.loadImage(imgResumeModeName, context)
                oUtils.validateHeatScheduleResumeMenu(oImgResumeMode, imgResumeModeName, oLang, context)
                oImgResumeMode = None
                # strHeatOffText = oUtils.getHeatOffScreenText(oImgOffMode, oLang)
                # context.reporter.ReportEvent("Event Log", "Heat off Text is displayed as <B>" + strHeatOffText + "</B>",
                #                             "Done")
                context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done",
                                             ocrImagePath=imgName)
                oImg = oUtils.loadImage(imgName, context)
                Mode = oUtils.getText(oImg, context)
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in heat:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[3] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgName)
                context.oThermostatEP.model.mode = "AUTO"
                nowTime = CTM.getTestTime(CTM.timeOffset)
                scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
                context.oThermostatEP.model.occupiedHeatingSetpoint = scheduleSetpoint
            if str(strMode).upper() == 'SCH-OVERRIDE':
                context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                _, imgWakeName = oUtils.captureOriginal(context)

                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done")
                context.reporter.ReportEvent("Test Validation", "current temp in HEX is " + str(
                    context.oThermostatEP.occupiedHeatingSetpoint), "Done")
                context.reporter.ReportEvent("Test Validation",
                                             " current temp is " + str(
                                                 rFM.ReusableFunctionModule.convertHexTemp(rFM.ReusableFunctionModule,
                                                                                           str(
                                                                                               context.oThermostatEP.occupiedHeatingSetpoint),
                                                                                           False)),
                                             "Done")
                intTemp = float(
                    rFM.ReusableFunctionModule.convertHexTemp(rFM.ReusableFunctionModule,
                                                              context.oThermostatEP.occupiedHeatingSetpoint,
                                                              False))
                intExpTemp = float(strOverrideTemp)
                if intTemp == 1.0:
                    intTemp = intTemp * 7.0
                if intTemp == intExpTemp:
                    context.reporter.ReportEvent("Test Validation",
                                                 "The current temperature is already " + str(intExpTemp), "Done")
                    exit()
                context.reporter.ReportEvent("Test Validation",
                                             " current temp is " + str(intTemp) + " destination is " + str(intExpTemp),
                                             "Done")
                if intTemp < intExpTemp:
                    intDiff = intExpTemp - intTemp
                    for counter in range(0, int(intDiff * 2), 1):
                        dutils.rotateDial(myNodeId, ep, 'CLOCKWISE', 1)
                        oImgInc, imgIncName = oUtils.captureOriginal(context)
                        context.reporter.ReportEvent("Event Log", "Target temperature is incremented to " + str(
                            round((intTemp + (counter / 2) + 0.5), 2)), "Done", ocrImagePath=imgIncName)
                    _, imgOffName = oUtils.captureOriginal(context)
                    context.reporter.ReportEvent("Event Log",
                                                 "Target temperature is set to " + str(intExpTemp), "Done",
                                                 ocrImagePath=imgOffName)
                elif intTemp > intExpTemp:
                    intDiff = intTemp - intExpTemp
                    for counter in range(0, int(intDiff * 2), 1):
                        dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", 1)
                        oImgInc, imgIncName = oUtils.captureOriginal(context)
                        context.reporter.ReportEvent("Event Log",
                                                     "Target temperature is decremented to " + str(
                                                         round((intTemp - (counter / 2) + 0.5), 2)), "Done",
                                                     ocrImagePath=imgIncName)
                    _, imgOffName = oUtils.captureOriginal(context)
                    context.reporter.ReportEvent("Event Log",
                                                 "Target temperature is set to " + str(intExpTemp), "Done",
                                                 ocrImagePath=imgOffName)

                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)
                oImgWake, imgHeatName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgHeatName)
                Mode = oUtils.getText(oImgWake, context)
                oUtils.printModesHome(Mode, context, oLang)
                mySetpoint = intExpTemp
                context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)
            if str(strMode).upper() == 'MANUAL':
                mySetpoint = 20
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                _, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                time.sleep(3)
                context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
                _, imgMenuName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(3)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Heat Menu", "Done")
                _, imgHeatName = oUtils.captureOriginal(context)
                dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
                time.sleep(3)
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Manual mode", "Done")
                _, imgOffName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(3)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Manual mode", "Done")
                _, imgOffModeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(3)
                _, imgName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Manual Water",
                                             "Done")

                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)
                oImgWake = oUtils.loadImage(imgWakeName, context)
                Mode = oUtils.getText(oImgWake, context)
                oImgWake = None
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)
                oImgMenu = oUtils.loadImage(imgMenuName, context)
                oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)
                oImgMenu = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgHeatName)
                oImgHeat = oUtils.loadImage(imgHeatName, context)
                oUtils.validateHeatMenu(oImgHeat, imgHeatName, oLang, context)
                oImgHeat = None
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Manual mode", "Done",
                                             ocrImagePath=imgOffName)
                oImgOff = oUtils.loadImage(imgOffName, context)
                oUtils.validateHeatMenu(oImgOff, imgOffName, oLang, context)
                oImgOff = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgOffModeName)
                oImgOffMode = oUtils.loadImage(imgOffModeName, context)
                strHeatOffText = oUtils.getHeatOffScreenText(oImgOffMode, oLang)
                oImgOffMode = None
                context.reporter.ReportEvent("Event Log",
                                             "Heat Manual Text is displayed as <B>" + strHeatOffText + "</B>",
                                             "Done")
                context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done",
                                             ocrImagePath=imgName)
                oImg = oUtils.loadImage(imgName, context)
                Mode = oUtils.getText(oImg, context)
                oImg = None
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in heat:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[3] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgName)
                context.oThermostatEP.model.mode = "MANUAL"
                context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)
        elif str(strType).upper() == 'HOTWATER':
            if str(strMode).upper() == 'BOOST':
                Mode, imgBoostName, _, _, imgHomeName = dutils.waterBoost(context, myNodeId, ep)
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Heat Boost Button is pressed", "Done",
                                             ocrImagePath=imgBoostName)
                oImgBoost = oUtils.loadImage(imgBoostName, context)
                oUtils.validateHotBoostScreen(oImgBoost, imgBoostName, oLang, context)
                oImgBoost = None
                oImgHome = oUtils.loadImage(imgHomeName, context)
                Mode = oUtils.getText(oImgHome, context)
                oImgHome = None
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in hot:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgHomeName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[2] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgHomeName)

            if str(strMode).upper() == 'OFF':
                mySetpoint = 0.0
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                time.sleep(3)
                _, imgWakeName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                time.sleep(1)
                _, imgMenuName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water mode", "Done")
                dutils.rotateDial(myNodeId, ep, "CLOCKWISE", 1)
                time.sleep(1)
                _, imgMenuHotName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed on Water mode", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(1)
                _, imgHotName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water mode", "Done")
                dutils.rotateDial(myNodeId, ep, "CLOCKWISE", 2)
                time.sleep(1)
                _, imgHotOffName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done")
                time.sleep(1)
                _, imgOffModeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done")
                time.sleep(2)
                _, imgName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)

                oImgWake = oUtils.loadImage(imgWakeName, context)
                Mode = oUtils.getText(oImgWake, context)
                oImgWake = None
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)
                oImgMenu = oUtils.loadImage(imgMenuName, context)
                oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)
                oImgMenu = None
                context.reporter.ReportEvent("Event Log", "Dial is rotated", "Done",
                                             ocrImagePath=imgMenuHotName)

                oImgMenuHot = oUtils.loadImage(imgMenuHotName, context)
                oUtils.validateMainMenu(oImgMenuHot, imgMenuHotName, oLang, context)
                oImgMenuHot = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgHotName)

                oImgHot = oUtils.loadImage(imgHotName, context)
                oUtils.validateHotMenu(oImgHot, imgHotName, oLang, context)
                oImgHot = None
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Off mode", "Done",
                                             ocrImagePath=imgHotOffName)
                oImgHotOff = oUtils.loadImage(imgHotOffName, context)
                oUtils.validateHotMenu(oImgHotOff, imgHotOffName, oLang, context)
                oImgHotOff = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgOffModeName)
                oImgOffMode = oUtils.loadImage(imgOffModeName, context)
                strHeatOffText = oUtils.getHeatOffScreenText(oImgOffMode, oLang)
                oImgOffMode = None
                context.reporter.ReportEvent("Event Log", "Heat off Text is displayed as <B>" + strHeatOffText + "</B>",
                                             "Done")
                context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done",
                                             ocrImagePath=imgOffModeName)
                oImg = oUtils.loadImage(imgName, context)
                Mode = oUtils.getText(oImg, context)
                oImg = None
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in hot:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[2] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgName)
                context.oThermostatEP.model.mode = "OFF"
                context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)

            if str(strMode).upper() == 'SCH':
                context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                _, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                context.reporter.ReportEvent("Event Log", "Menu is Pressed from Home", "Done")
                time.sleep(1)
                _, imgMenuName = oUtils.captureOriginal(context)
                dutils.rotateDial(myNodeId, ep, "CLOCKWISE", 1)
                time.sleep(1)
                _, imgHotMenuName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water mode", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                context.reporter.ReportEvent("Event Log", "Dial is Pressed for Hot Water Mode", "Done")
                time.sleep(1)
                _, imgHotWaterMenuName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                context.reporter.ReportEvent("Event Log", "Dial is Pressed on Schedule mode", "Done")
                time.sleep(1)
                _, imgSchModeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                context.reporter.ReportEvent("Event Log", "Dial is Pressed on Resume schedule mode", "Done")
                time.sleep(1)
                _, imgResumeModeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                context.reporter.ReportEvent("Event Log", "Confirm is Pressed on Resume schedule mode", "Done")
                time.sleep(3)
                _, imgName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)

                oImgWake = oUtils.loadImage(imgWakeName, context)
                Mode = oUtils.getText(oImgWake, context)
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)
                oImgMenu = oUtils.loadImage(imgMenuName, context)
                oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)

                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water mode", "Done",
                                             ocrImagePath=imgHotMenuName)
                oImgMenu = None
                oImgHotMenu = oUtils.loadImage(imgHotMenuName, context)
                oUtils.validateMainMenu(oImgHotMenu, imgHotMenuName, oLang, context)
                oImgHotMenu = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed to select Hot Water", "Done",
                                             ocrImagePath=imgHotWaterMenuName)
                oImgHotWaterMenu = oUtils.loadImage(imgHotWaterMenuName, context)
                oUtils.validateHotMenu(oImgHotWaterMenu, imgHotWaterMenuName, oLang, context)
                oImgHotWaterMenu = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed to select Schedule", "Done",
                                             ocrImagePath=imgSchModeName)
                oImgSchMode = oUtils.loadImage(imgSchModeName, context)
                oUtils.validateHotScheduleMenu(oImgSchMode, imgSchModeName, oLang, context)
                oImgSchMode = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed to select Resume", "Done",
                                             ocrImagePath=imgResumeModeName)
                oImgResumeMode = oUtils.loadImage(imgResumeModeName, context)
                oUtils.validateHotScheduleResumeMenu(oImgResumeMode, imgResumeModeName, oLang, context)
                oImgResumeMode = None
                # strHeatOffText = oUtils.getHeatOffScreenText(oImgOffMode, oLang)
                # context.reporter.ReportEvent("Event Log", "Heat off Text is displayed as <B>" + strHeatOffText + "</B>",
                #                             "Done")
                context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done",
                                             ocrImagePath=imgName)
                oImg = oUtils.loadImage(imgName, context)
                Mode = oUtils.getText(oImg, context)
                oImg = None
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in hot:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[3] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgName)
                context.oThermostatEP.model.mode = "AUTO"
                nowTime = CTM.getTestTime(CTM.timeOffset)
                scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
                context.reporter.ReportEvent("OCR Validation", "scheduleSetpoint " + str(scheduleSetpoint), "Done")
                if scheduleSetpoint == 0:
                    context.oThermostatEP.model.thermostatRunningState = '0000'
                else:
                    context.oThermostatEP.model.thermostatRunningState = '0001'
            if str(strMode).upper() == 'ON':
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                _, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                time.sleep(2)
                context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
                _, imgMenuName = oUtils.captureOriginal(context)
                dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
                time.sleep(1)
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water mode", "Done")
                _, imgMenuHotName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is rotated", "Done",
                                             ocrImagePath=imgMenuHotName)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(3)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Water Menu", "Done")
                _, imgHotName = oUtils.captureOriginal(context)
                dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
                time.sleep(3)
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water AlwaysOn mode", "Done")
                _, imgHotManualName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(3)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Water ON", "Done")
                _, imgManualModeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(3)
                context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Always ON",
                                             "Done")
                _, imgName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)

                oImgWake = oUtils.loadImage(imgWakeName, context)
                Mode = oUtils.getText(oImgWake, context)
                oImgWake = None
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)
                oImgMenu = oUtils.loadImage(imgMenuName, context)
                oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)
                oImgMenu = None
                context.reporter.ReportEvent("Event Log", "Dial is rotated", "Done",
                                             ocrImagePath=imgMenuHotName)
                oImgMenuHot = oUtils.loadImage(imgMenuHotName, context)

                oUtils.validateMainMenu(oImgMenuHot, imgMenuHotName, oLang, context)
                oImgMenuHot = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgHotName)
                oImgHot = oUtils.loadImage(imgHotName, context)
                oUtils.validateHotMenu(oImgHot, imgHotName, oLang, context)
                oImgHot = None
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Always ON mode", "Done",
                                             ocrImagePath=imgHotManualName)
                oImgHotManual = oUtils.loadImage(imgHotManualName, context)
                oUtils.validateHotMenu(oImgHotManual, imgHotManualName, oLang, context)
                oImgHotManual = None
                context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                             ocrImagePath=imgHotManualName)
                oImgManualMode = oUtils.loadImage(imgManualModeName, context)
                strHeatOffText = oUtils.getHeatOffScreenText(oImgManualMode, oLang)
                oImgManualMode = None
                context.reporter.ReportEvent("Event Log",
                                             "Always ON Text is displayed as <B>" + strHeatOffText + "</B>",
                                             "Done")
                context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done",
                                             ocrImagePath=imgManualModeName)
                oImg = oUtils.loadImage(imgName, context)
                Mode = oUtils.getText(oImg, context)
                heat, hot = oUtils.printModesHome(Mode, context, oLang)
                if str(strMode).upper() in hot:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                                 "PASS",
                                                 ocrImagePath=imgName)
                else:
                    context.reporter.ReportEvent("OCR Validation",
                                                 "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                                 Mode.split(" ")[2] + " on the stat screen", "FAIL",
                                                 ocrImagePath=imgName)
                context.oThermostatEP.model.mode = "MANUAL"
                context.oThermostatEP.model.thermostatRunningState = "0001"
        elif str(strType).upper() == 'HOLIDAY':
            mySetpoint = 1.0
            holidayStartOffset = 60
            intSetTempDuration = 604800
            context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            oImgWake, imgWakeName = oUtils.captureOriginal(context)
            dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
            time.sleep(1)
            oImgMenu, imgMenuName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", 2)
            time.sleep(1)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done")
            oImgHolMenu, imgHolMenuName = oUtils.captureOriginal(context)
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is pressed to Holiday mode", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            strHoldayStart = (datetime.now() + timedelta(seconds=holidayStartOffset)).replace(second=0, microsecond=0)
            strUTCHoldayStart = (datetime.now() + timedelta(seconds=holidayStartOffset)).replace(second=0,
                                                                                                 microsecond=0)
            _, oImgHolFromMonName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Month", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromYearDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Year", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromHourDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Hour", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromMinuteDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Minute", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFromDateConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Start Date", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To date", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToMonName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Month", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToYearDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To year", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToHourDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To hour", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToMinuteDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To minute", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToDateConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirm end date", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolFrostName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To temperature", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirmation screen", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
            time.sleep(2)
            oImgHolWaterConfirm, oImgHolWaterConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirmation instruction screen", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
            time.sleep(5)
            oImg, oImgName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to save the holiday setting", "Done")

            context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                         ocrImagePath=imgWakeName)

            Mode = oUtils.getText(oImgWake, context)
            oUtils.printModesHome(Mode, context, oLang)

            context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                         ocrImagePath=imgMenuName)

            oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)

            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done",
                                         ocrImagePath=imgHolMenuName)

            oUtils.validateMainMenu(oImgHolMenu, imgHolMenuName, oLang, context)
            oImgHolFromDate = oUtils.loadImage(oImgHolFromDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is pressed to Holiday mode", "Done")
            oUtils.validateHolidayMenu(oImgHolFromDate, oImgHolFromDateName, oLang, context, "FROM", "DATE")
            oImgHolFromDate = None

            oImgHolFromMon = oUtils.loadImage(oImgHolFromMonName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Month", "Done")
            oUtils.validateHolidayMenu(oImgHolFromMon, oImgHolFromMonName, oLang, context, "FROM", "MONTH")
            oImgHolFromMon = None

            oImgHolFromYearDate = oUtils.loadImage(oImgHolFromYearDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Year", "Done")
            oUtils.validateHolidayMenu(oImgHolFromYearDate, oImgHolFromYearDateName, oLang, context, "FROM", "YEAR")
            oImgHolFromYearDate = None

            oImgHolFromHourDate = oUtils.loadImage(oImgHolFromHourDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Hour", "Done")
            oUtils.validateHolidayMenu(oImgHolFromHourDate, oImgHolFromHourDateName, oLang, context, "FROM", "HOUR")
            oImgHolFromHourDate = None

            oImgHolFromMinuteDate = oUtils.loadImage(oImgHolFromMinuteDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Minute", "Done")
            oUtils.validateHolidayMenu(oImgHolFromMinuteDate, oImgHolFromMinuteDateName, oLang, context, "FROM",
                                       "MINUTE")
            oImgHolFromMinuteDate = None

            oImgHolFromDateConfirm = oUtils.loadImage(oImgHolFromDateConfirmName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Start Date", "Done")
            oUtils.validateHolidayMenu(oImgHolFromDateConfirm, oImgHolFromDateConfirmName, oLang, context, "FROM",
                                       "CONFIRM")
            oImgHolFromDateConfirm = None

            oImgHolToDate = oUtils.loadImage(oImgHolToDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done")
            oUtils.validateHolidayMenu(oImgHolToDate, oImgHolToDateName, oLang, context, "To", "DATE")
            oImgHolToDate = None

            oImgHolToMon = oUtils.loadImage(oImgHolToMonName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Month", "Done")
            oUtils.validateHolidayMenu(oImgHolToMon, oImgHolToMonName, oLang, context, "To", "MONTH")
            oImgHolToMon = None

            oImgHolToYearDate = oUtils.loadImage(oImgHolToYearDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Year", "Done")
            oUtils.validateHolidayMenu(oImgHolToYearDate, oImgHolToYearDateName, oLang, context, "To", "YEAR")
            oImgHolToYearDate = None

            oImgHolToHourDate = oUtils.loadImage(oImgHolToHourDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Hour", "Done")
            oUtils.validateHolidayMenu(oImgHolToHourDate, oImgHolToHourDateName, oLang, context, "To", "HOUR")
            oImgHolToHourDate = None

            oImgHolToMinuteDate = oUtils.loadImage(oImgHolToMinuteDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Minute", "Done")
            oUtils.validateHolidayMenu(oImgHolToMinuteDate, oImgHolToMinuteDateName, oLang, context, "To", "MINUTE")
            oImgHolToMinuteDate = None

            oImgHolToDateConfirm = oUtils.loadImage(oImgHolToDateConfirmName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Start Date", "Done")
            oUtils.validateHolidayMenu(oImgHolToDateConfirm, oImgHolToDateConfirmName, oLang, context, "To", "CONFIRM")
            oImgHolToDateConfirm = None

            oImgHolFrost = oUtils.loadImage(oImgHolFrostName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Temperature", "Done")
            oUtils.validateHolidayMenu(oImgHolFrost, oImgHolFrostName, oLang, context, "TEMP")
            oImgHolFrost = None

            oImgHolConfirm = oUtils.loadImage(oImgHolConfirmName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirmation screen", "Done")
            oUtils.validateHolidayMenu(oImgHolConfirm, oImgHolConfirmName, oLang, context, "CONFIRM")

            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to confirmation instruction screen", "Done")
            oUtils.validateHolidayMenu(oImgHolWaterConfirm, oImgHolWaterConfirmName, oLang, context,
                                       "CONFIRMINSTRUCTION")

            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to save the holiday setting", "Done")

            Mode = oUtils.getText(oImg, context)
            _, _ = oUtils.printHolidayDurationHome(Mode, context, oLang)

            context.oThermostatEP.model.mode = "HOLIDAY"

            context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)

            strHoldayEnd = (strHoldayStart + timedelta(seconds=intSetTempDuration))
            context.oThermostatEP.model.holidayModeEnabled = '01'
            strUTCHoldayEnd = (strHoldayStart + timedelta(seconds=intSetTempDuration))
            context.strHoldayStart = strUTCHoldayStart
            context.strHoldayEnd = strUTCHoldayEnd

            startDateString = datetime.strftime(strHoldayStart, "%Y%m%d")
            startTimeString = datetime.strftime(strHoldayStart, "%H:%M")
            startTimeHex = tt.timeStringToHex(startTimeString)

            endDateString = datetime.strftime(strHoldayEnd, "%Y%m%d")
            endTimeString = datetime.strftime(strHoldayEnd, "%H:%M")
            endTimeHex = tt.timeStringToHex(endTimeString)

            context.oThermostatEP.model.holidayModeStart = context.oThermostatEP._buildHolidayDatetimeUTC(
                startDateString, startTimeHex)
            context.oThermostatEP.model.holidayModeEnd = context.oThermostatEP._buildHolidayDatetimeUTC(endDateString,
                                                                                                        endTimeHex)

        context.reporter.ReportEvent("Event Log", "Re-setting fast poll", "Done")
        AT.resetFastPoll(longPollInt, checkInInt, myNodeId, ep, context)
        context.oThermostatEP.update()
    else:
        context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")


@step(u'the {strType} {strMode} is deactivated using button on the {strLang} in {strDeviceType}')
def deactivateHoliday(context, strType, strMode, strLang, strDeviceType):
    global ep, myEp, myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Dectivate ' + strType + ' ' + strMode + ' mode on the ' + strDeviceType)
    '''try:
        AT.stopThreads()
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
    except:
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)'''
    flag = False
    if 'when both boost is active' in strDeviceType:
        flag = True
    strExpMode = ''
    strExpType = ''
    if 'to' in strDeviceType:
        strExpMode = str(strDeviceType).split(' ')[3]
        strExpType = str(strDeviceType).split(' ')[2]
        strDeviceType = str(strDeviceType).split(' ')[0]
    myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, strType, context, strLang)
    strMode = oUtils.getModeText(strMode, strType, oLang)
    respSate = AT.setFastPoll()
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if str(strType).upper() == 'HOTWATER':
            if 'BOOST' in strMode.upper():
                context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                oImgWake, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "BACK", "Press")
                time.sleep(1)
                oImgMenu, imgMenuName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Cancel Holiday Mode by pressing BACK button", "Done")
                oImgHW, imgHWName = None, None
                if flag:
                    oImgHW, imgHWName = oUtils.captureOriginal(context)
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    context.reporter.ReportEvent("Event Log", "Dial is Pressed on Hot Water Boost", "Done")
                    time.sleep(5)
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                time.sleep(2)
                oImg, oImgName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  to save the holiday setting", "Done")
                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)
                Mode = oUtils.getText(oImgWake, context)
                oUtils.printHolidayDurationHome(Mode, context, oLang)
                context.reporter.ReportEvent("Event Log", "Back Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)
                if flag:
                    oUtils.validateBoostCancelSelectionScreen(oImgHW, imgHWName, oLang, context)
                    context.reporter.ReportEvent("Event Log", "Boost cancellation screen", "Done",
                                                 ocrImagePath=imgHWName)
                Mode = oUtils.getText(oImg, context)
                _, _ = oUtils.printModesHome(Mode, context, oLang)
                if 'OFF' in str(strExpMode).upper():
                    context.oThermostatEP.model.mode = "OFF"
        if str(strType).upper() == 'HEAT':
            if 'BOOST' in strMode.upper():
                context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                oImgWake, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "BACK", "Press")
                time.sleep(1)
                oImgMenu, imgMenuName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Cancel Holiday Mode by pressing BACK button", "Done")
                oImgHotMenu, imgHotMenuName, oImgHotCMenu, imgHotCMenuName = None, None, None, None
                if flag:
                    oImgHotMenu, imgHotMenuName = oUtils.captureOriginal(context)
                    dutils.rotateDial(myNodeId, ep, "CLOCKWISE", 1)
                    time.sleep(1)
                    oImgHotCMenu, imgHotCMenuName = oUtils.captureOriginal(context)
                    context.reporter.ReportEvent("Event Log", "Dial is rotated to Heat Boost", "Done")
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    context.reporter.ReportEvent("Event Log", "Dial is Pressed on Heat Boost", "Done")
                    time.sleep(5)

                dutils.wakeUpTheDevice(context, myNodeId, ep)
                time.sleep(2)
                oImg, oImgName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  to save the holiday setting", "Done")
                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)
                Mode = oUtils.getText(oImgWake, context)
                oUtils.printHolidayDurationHome(Mode, context, oLang)
                context.reporter.ReportEvent("Event Log", "Back Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)
                if flag:
                    oUtils.validateBoostCancelSelectionScreen(oImgHotMenu, imgHotMenuName, oLang, context)
                    context.reporter.ReportEvent("Event Log", "Boost cancellation screen", "Done",
                                                 ocrImagePath=imgHotMenuName)
                    oUtils.validateBoostCancelSelectionScreen(oImgHotCMenu, imgHotCMenuName, oLang, context)
                    context.reporter.ReportEvent("Event Log", "Boost cancellation screen heat selection ", "Done",
                                                 ocrImagePath=imgHotCMenuName)

                Mode = oUtils.getText(oImg, context)
                _, _ = oUtils.printModesHome(Mode, context, oLang)

                context.oThermostatEP.model.mode = strExpMode
                if 'OFF' in str(strExpMode).upper():
                    mySetPoint = 1.0
                    context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetPoint)
        if str(strType).upper() == 'HOLIDAY':
            context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            oImgWake, imgWakeName = oUtils.captureOriginal(context)
            dutils.pressDeviceButton(myNodeId, ep, "BACK", "Press")
            time.sleep(1)
            oImgMenu, imgMenuName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Cancel Holiday Mode by pressing BACK button", "Done")
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            time.sleep(2)
            oImg, oImgName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to save the holiday setting", "Done")
            context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                         ocrImagePath=imgWakeName)
            Mode = oUtils.getText(oImgWake, context)
            oUtils.printHolidayDurationHome(Mode, context, oLang)
            context.reporter.ReportEvent("Event Log", "Back Button is pressed", "Done",
                                         ocrImagePath=imgMenuName)
            Mode = oUtils.getText(oImg, context)
            oUtils.printModesHome(Mode, context, oLang)
            context.oThermostatEP.model.holidayModeEnabled = '00'
            context.oThermostatEP.model.holidayModeStart = ''
            context.oThermostatEP.model.holidayModeEnd = ''
        context.reporter.ReportEvent("Event Log", "Re-setting fast poll", "Done")
        AT.resetFastPoll(longPollInt, checkInInt, myNodeId, ep, context)
        context.oThermostatEP.update()
    else:
        context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")


@step(u'validate current {strType} mode as {strMode} on the {strDeviceType} screen in {strLang}')
def validateModeOnScreen(context, strType, strMode, strDeviceType, strLang):
    global myEp
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Validate ' + strType + ' ' + strMode + ' mode on the thermostat')
    myNodeId = ""
    ep = ""

    myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, strType, context, strLang)

    time.sleep(5)
    respSate = AT.setFastPoll()
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
        time.sleep(4)
    else:
        context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")
    oImg, imgName = oUtils.captureOriginal(context)
    AT.resetFastPoll(longPollInt, checkInInt, myNodeId, ep)
    Mode = oUtils.getText(oImg, context)
    Mode = Mode.replace("0FF", "OFF").replace("0N", "ON").replace("oN", "ON").replace("oFF","OFF").replace("BO0ST","BOOST").replace("MANuAL","MANUAL").replace("BoosT","BOOST")
    Mode = Mode.strip()
    if oLang.BootScreen.ReceivingText in Mode:
        context.reporter.ReportEvent("OCR Validation", "Screen is in Receiving", "FAIL")
        exit()
    heat,hot = oUtils.printModesHome(Mode,context,oLang)
    context.reporter.ReportEvent("Event Log", "Attributes $$ Value @@@ $~Current Heat Mode$$" + heat + " $~Current Hot Water Mode$$" + hot, "Done")
    context.reporter.ReportEvent("Event Log", "OCR Mode = " + Mode, "Done")

    strMode = oUtils.getModeText(strMode, strType, oLang)
    if strMode == "SCH-OVERRIDE":
        strMode = "SCH"
    if str(strType).upper() == "HEAT":
        if str(strMode).upper() in heat:
            context.reporter.ReportEvent("OCR Validation",
                                         "Attributes $$ Expected and Actual @@@ $~Current Mode$$" + strMode, "PASS",
                                         ocrImagePath=imgName)
        else:
            context.reporter.ReportEvent("OCR Validation",
                                         "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                         heat + " on the stat screen", "FAIL", ocrImagePath=imgName)
    elif str(strType).upper() == "HOTWATER":
        Mode = Mode.replace("0FF", "OFF").replace("0N", "ON")
        if str(strMode).upper() in hot:
            context.reporter.ReportEvent("OCR Validation",
                                         "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode, "PASS",
                                         ocrImagePath=imgName)
        else:
            context.reporter.ReportEvent("OCR Validation",
                                         "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                         hot + " on the stat screen", "FAIL", ocrImagePath=imgName)
    elif str(strType).upper() == "HOLIDAY":

        if str(strMode).split(",")[0] in hot:
            context.reporter.ReportEvent("OCR Validation",
                                         "Attributes $$ Expected and Actual @@@ $~Holiday Days$$" + hot, "PASS",
                                         ocrImagePath=imgName)
        else:
            context.reporter.ReportEvent("OCR Validation",
                                         "Attributes $$ Expected $$ Actual @@@ $~Holiday Days$$ " + strMode + " $$ " +
                                         hot + " on the stat screen", "FAIL", ocrImagePath=imgName)
        if str(strMode).split(",")[1] in heat:
            context.reporter.ReportEvent("OCR Validation",
                                         "Attributes $$ Expected and Actual @@@ $~Holiday Hours$$" + strMode, "PASS",
                                         ocrImagePath=imgName)
        else:
            context.reporter.ReportEvent("OCR Validation",
                                         "Attributes $$ Expected $$ Actual @@@ $~Holiday Hours$$ " + strMode + " $$ " +
                                         heat + " on the stat screen", "FAIL", ocrImagePath=imgName)
    AT.resetFastPoll(longPollInt, checkInInt, myNodeId, ep)
    context.reporter.ReportEvent("Event Log", "Re-setting fast poll", "Done")


@when(u'the {strType} is activated and deactivated using button flow on the {strLang} {strDeviceType}')
def activateChildLock(context, strType, strLang, strDeviceType):
    global myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Activate ' + strType + ' ' + strType + ' mode on the thermostat')
    myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, strType, context, strLang)
    time.sleep(5)
    respSate = AT.setFastPoll()
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
        time.sleep(4)
        context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done")
        # Child lock via Menu
        ''' dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
        time.sleep(4)
        context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Settings ", "Done")
        dutils.rotateDial(myNodeId, ep, "CLOCKWISE", 3)
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed on Settings", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is rotated Child Lock OFF Settings ", "Done")
        dutils.rotateDial(myNodeId, ep, "CLOCKWISE", 2)
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed on Child Lock", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed on Child Lock", "Done")'''
        # direct child lock from home screen-Start
        dutils.pressDeviceButton(myNodeId, ep, "Back", "Hold", 0, True)
        context.reporter.ReportEvent("Event Log", "Back is on HOLD for Child Lock", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Hold", 0, True)
        context.reporter.ReportEvent("Event Log", "Tick is on HOLD for Child Lock", "Done")
        time.sleep(3)
        dutils.pressDeviceButton(myNodeId, ep, "Back", "Release")
        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Release")
        oImgLock, oImgLockName = oUtils.captureOriginal(context)

        Mode = oUtils.getText(oImgLock, context)
        oUtils.printModesHome(Mode, context, oLang)

        context.reporter.ReportEvent("Event Log", "Locked", "Done",
                                     ocrImagePath=oImgLockName)

        time.sleep(8)
        dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
        time.sleep(5)
        oImgHome, oImgHomeName = oUtils.captureOriginal(context)
        Mode = oUtils.getText(oImgHome, context)
        oUtils.printModesHome(Mode, context, oLang)

        context.reporter.ReportEvent("Event Log", "Child Lock in active", "Done",
                                     ocrImagePath=oImgHomeName)
        dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
        time.sleep(3)
        dutils.pressDeviceButton(myNodeId, ep, "Back", "Hold", 0, True)
        context.reporter.ReportEvent("Event Log", "Back is on HOLD for Child Lock", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Hold", 0, True)
        context.reporter.ReportEvent("Event Log", "Tick is on HOLD for Child Lock", "Done")
        time.sleep(3)
        dutils.pressDeviceButton(myNodeId, ep, "Back", "Release")
        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Release")
        # direct child lock from home screen-End


@when(u'the {strType} {strMode} is set with {strOption} with {ScheduleType} on the {strDeviceType} screen in {strLang}')
def setSchedule(context, strType, strMode, strOption, ScheduleType, strDeviceType, strLang):
    global myEp
    myNodeId, ep, respSate = OCRprerequisite(context, strDeviceType)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Activate ' + strType + ' ' + strMode + ' mode on the thermostat')
    myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, strType, context, strLang)
    strOverrideTemp = ""
    if "OVERRIDE" in str(strDeviceType).upper():
        strOverrideTemp = str(strDeviceType).split(" ")[2]
    strMode = oUtils.getModeText(strMode, strType, oLang)

    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if "HEAT" in str(strType).upper():
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            _, imgWakeName = oUtils.captureOriginal(context)
            imgMenuName, imgHeatName, imgSchModeName = oUtils.navigateToHeadScheduleScreen(context, myNodeId, ep)
            time.sleep(1)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Heat Schedule startover mode",
                                         "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", 2)
            time.sleep(1)
            _, imgSOModeName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(1)
            _, imgSOModeConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver Confirm", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(1)
            _, imgTypeConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver Energy Efficient",
                                         "Done")
            oImgTypeEE, imgSOModeEEName = None, None
            if oLang.HeatMenuScreen.HeatStartOverOptionsEE in strOption:
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(1)
                _, imgSOModeEEName = oUtils.captureOriginal(context)
            elif oLang.HeatMenuScreen.HeatStartOverOptionsC in strOption:
                dutils.rotateDial(myNodeId, ep, "Clockwise", 2)
                time.sleep(1)
                context.reporter.ReportEvent("Event Log",
                                             "Dial is rotated clockwise to Heat Schedule startover comfort mode",
                                             "Done")
                oImgECMode, imgECModeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(1)
                _, imgSOModeEEName = oUtils.captureOriginal(context)
            else:
                context.reporter.ReportEvent("Event Log", "INVAID INPUT " + strOption,
                                             "FAIL")
                exit()
            context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Schedule StartOver Energy Efficient",
                                         "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
            time.sleep(1)
            _, imgSOModeEEConfirmName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Exit Option", "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
            time.sleep(1)
            _, imgExitName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log",
                                         "Dial is Pressed for Heat Schedule StartOver Energy Efficient Complete",
                                         "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            oImg, imgName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                         ocrImagePath=imgWakeName)
            oImgWake = oUtils.loadImage(imgWakeName, context)
            Mode = oUtils.getText(oImgWake, context)
            oImgWake = None
            oUtils.printModesHome(Mode, context, oLang)

            context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                         ocrImagePath=imgMenuName)
            oImgMenu = oUtils.loadImage(imgMenuName, context)
            oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)
            oImgMenu = None

            context.reporter.ReportEvent("Event Log", "Dial is pressed to select Heat", "Done",
                                         ocrImagePath=imgHeatName)
            oImgHeat = oUtils.loadImage(imgHeatName, context)
            oUtils.validateHeatMenu(oImgHeat, imgHeatName, oLang, context)
            oImgHeat = None

            context.reporter.ReportEvent("Event Log", "Dial is pressed to select Schedule", "Done",
                                         ocrImagePath=imgSchModeName)
            oImgSchMode = oUtils.loadImage(imgHeatName, context)
            oUtils.validateHeatScheduleMenu(oImgSchMode, imgSchModeName, oLang, context)
            oImgSchMode = None
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Heat Schedule startover mode",
                                         "Done")

            context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver", "Done",
                                         ocrImagePath=imgSOModeName)
            oImgSOMode = oUtils.loadImage(imgSOModeName, context)
            oUtils.validateHeatScheduleMenu(oImgSOMode, imgSOModeName, oLang, context)
            oImgSOMode = None

            context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver Confirm", "Done",
                                         ocrImagePath=imgSOModeConfirmName)
            oImgSOModeConfirm = oUtils.loadImage(imgSOModeConfirmName, context)
            oUtils.validateStartOverInitialScreen(oImgSOModeConfirm, imgSOModeConfirmName, oLang, context)
            oImgSOModeConfirm = None

            context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver Energy Efficient",
                                         "Done", ocrImagePath=imgTypeConfirmName)
            oImgTypeConfirm = oUtils.loadImage(imgTypeConfirmName, context)
            oUtils.validateStartOverSelectionScreen(oImgTypeConfirm, imgTypeConfirmName, oLang, context)
            oImgTypeConfirm = None

            context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver selected mode",
                                         "Done", ocrImagePath=imgSOModeEEName)
            oImgTypeEE = oUtils.loadImage(imgSOModeEEName, context)
            oUtils.validateStartOverTypeSelectionScreen(oImgTypeEE, imgSOModeEEName, oLang, context, strOption)
            oImgTypeEE = None
            context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Schedule StartOver Energy Efficient",
                                         "Done")
            oImgTypeEEConfirm = oUtils.loadImage(imgSOModeEEConfirmName, context)
            oUtils.validateStartOverConfirmationScreen(oImgTypeEEConfirm, imgSOModeEEConfirmName, oLang, context)
            oImgTypeEEConfirm = None

            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Exit Option", "Done",
                                         ocrImagePath=imgSOModeEEName)
            oImgExit = oUtils.loadImage(imgExitName, context)
            oUtils.validateStartOverConfirmationScreen(oImgExit, imgExitName, oLang, context)
            oImgExit = None
            context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                         ocrImagePath=imgName)

            Mode = oUtils.getText(oImg, context)
            oUtils.printModesHome(Mode, context, oLang)
            nowTime = CTM.getTestTime(CTM.timeOffset)
            scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
            context.oThermostatEP.model.occupiedHeatingSetpoint = scheduleSetpoint
        elif "STARTOVER" in str(ScheduleType).upper() and "WATER" in str(strType).upper():
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            _, imgWakeName = oUtils.captureOriginal(context)

            imgMenuName, imgHotMenuName, imgHotWaterMenuName, imgSchModeName, imgSOModeName, imgSOModeConfirmName, imgTypeConfirmName = oUtils.navigateToHotWaterStartover(context, myNodeId, ep)
            oUtils.pressAndCature(context, myNodeId, ep, "Tick", "Press", 2, "Event Log",
                                  "Tick is on Confirm for Schedule StartOver", "Done")

        context.reporter.ReportEvent("Event Log", "Re-setting fast poll", "Done")
        AT.resetFastPoll(longPollInt, checkInInt, myNodeId, ep, context)
        context.oThermostatEP.model.mode = "AUTO"

        context.oThermostatEP.update()
    else:
        context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")

@when(u'the {strType} {strMode} maximum and minimum start time of an event is validated on the {strDeviceType} screen in {strLang}')
def validateEventStartTime(context, strType, strMode, strDeviceType, strLang):
    global ep, myEp, myNodeId
    myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, strType, context, strLang)
    respSate = AT.setFastPoll()
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if str(strType).upper() == 'HEAT':
            context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                'Validate heat schedule event on the thermostat')
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            imgMenuName, imgHeatName, imgSchModeName, imgSOModeName, imgSOModeConfirmName, imgTypeConfirmName, imgSOModeEEName, imgSOModeEEEdit = oUtils.navigateToHotWaterScheduleStartOverEE(
                context, myNodeId, ep)
            lstReport = []
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(8)
            _, imgSOModeEEM = oUtils.captureOriginal(context)
            lstReport.append([imgSOModeEEM, "Event Log",
                              "Dial is Pressed to Select ",
                              "Done"])
            print("Pressing Tick")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
            time.sleep(5)
            _, imgSOModeEEM = oUtils.captureOriginal(context)
            lstReport.append([imgSOModeEEM, "Event Log",
                              "Tick is Pressed to Select ",
                              "Done"])
            time.sleep(1)
            dutils.rotateDial(myNodeId, ep, "AntiClockwise", 30)
            time.sleep(1)
            oImgMin, imgMin = oUtils.captureOriginal(context)
            dutils.rotateDial(myNodeId, ep, "Clockwise", 100)
            time.sleep(1)
            oImgMax, imgMax = oUtils.captureOriginal(context)
            oUtils.validateMinOrMaxEvent(oImgMin, imgMin, oLang, context, "Min")
            oUtils.validateMinOrMaxEvent(oImgMax, imgMax, oLang, context, "Max")

@when(u'the {strMode} is set to Manual on the {strDeviceType}')
def setManualMode(context, strMode, strDeviceType):
    myNodeId, ep, respSate = OCRprerequisite(context, strDeviceType)
    strLang = ""
    oLang = oUtils.getLanguage(strLang)
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if "WATER" in str(strMode).upper():
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            oImgWake, imgWakeName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
            time.sleep(1)
            oImgMenu, imgMenuName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water mode", "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
            time.sleep(1)
            oImgMenuHot, imgMenuHotName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is rotated", "Done",
                                         ocrImagePath=imgMenuHotName)
            oUtils.validateMainMenu(oImgMenuHot, imgMenuHotName, oLang, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Water Menu", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            oImgHot, imgHotName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water AlwaysOn mode", "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
            time.sleep(3)
            oImgHotManual, imgHotManualName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Water OFF", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            oImgManualMode, imgManualModeName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Manual Heat",
                                         "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
            time.sleep(3)
            oImg, imgName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                         ocrImagePath=imgWakeName)

            Mode = oUtils.getText(oImgWake, context)
            oUtils.printModesHome(Mode, context, oLang)

            context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                         ocrImagePath=imgMenuName)

            oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)

            context.reporter.ReportEvent("Event Log", "Dial is rotated", "Done",
                                         ocrImagePath=imgMenuHotName)

            oUtils.validateMainMenu(oImgMenuHot, imgMenuHotName, oLang, context)

            context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                         ocrImagePath=imgHotName)

            oUtils.validateHotMenu(oImgHot, imgHotName, oLang, context)

            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Always ON mode", "Done",
                                         ocrImagePath=imgHotManualName)
            oUtils.validateHotMenu(oImgHotManual, imgHotManualName, oLang, context)

            context.reporter.ReportEvent("Event Log", "Dial is pressed", "Done",
                                         ocrImagePath=imgHotManualName)
            strHeatOffText = oUtils.getHeatOffScreenText(oImgManualMode, oLang)
            context.reporter.ReportEvent("Event Log", "Always ON Text is displayed as <B>" + strHeatOffText + "</B>",
                                         "Done")
            context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done",
                                         ocrImagePath=imgManualModeName)
            Mode = oUtils.getText(oImg, context)
            heat, hot = oUtils.printModesHome(Mode, context, oLang)
            if str(strMode).upper() in hot:
                context.reporter.ReportEvent("OCR Validation",
                                             "Attributes $$ Expected and Actual @@@$~Current Mode$$" + strMode,
                                             "PASS",
                                             ocrImagePath=imgName)
            else:
                context.reporter.ReportEvent("OCR Validation",
                                             "Attributes $$ Expected $$ Actual @@@ $~Current Mode$$ " + strMode + " $$ " +
                                             Mode.split(" ")[2] + " on the stat screen", "FAIL",
                                             ocrImagePath=imgName)
            context.oThermostatEP.model.mode = "MANUAL"
            context.oThermostatEP.model.thermostatRunningState = "0001"


        elif "HEAT" in str(strMode).upper():
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Water Menu", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water AlwaysOn mode", "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Water OFF", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Manual Water",
                                         "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")

            # AT.stopThreads()

@when(u'the {strMode} is set to Default Schedule on the {strDeviceType}')
def setManualMode(context, strMode, strDeviceType):
    myNodeId, ep, respSate = OCRprerequisite(context, strDeviceType)
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if "heat" in strMode:
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Heat Menu", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Heat Schedule", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Heat Schedule Resume", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Heat Schedule Resume",
                                         "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
        if "water" in strMode:
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Water mode", "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Water Menu", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for water Schedule", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Water Schedule Resume", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Manual Heat",
                                         "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")

        AT.stopThreads()

@when(u'the {strMode} boost is cancelled on the {strDeviceType}')
def setHeatModeStop(context, strMode, strDeviceType):
    myNodeId, ep, respSate = OCRprerequisite(context, strDeviceType)
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if "heat" in strMode or "water" in strMode:
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            context.reporter.ReportEvent("Event Log", "Back Button is Pressed  for Cancel Boost", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Back", "Press")

        AT.stopThreads()

@when(u'the Frost temperature is set to {frostExpected}  on the {strDeviceType} with screen in {strLang}')
def setFrostTemp(context, frostExpected, strDeviceType, execType):
    myNodeId, ep, respSate = OCRprerequisite(context, strDeviceType)
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        dutils.wakeUpTheDevice(context, myNodeId, ep)
        context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Setting mode", "Done")
        dutils.rotateDial(myNodeId, ep, "Clockwise", 3)
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Setting", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Frost temperature", "Done")
        dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Frost", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        # get Current Frost
        frostActualValue = utils.getFrostTemperature()
        clockwiseCount = int(frostActualValue) - int(frostExpected)
        print("frostExpected" + frostExpected + " frostActual" + frostActualValue)
        if clockwiseCount > 0:
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Setting mode", "Done")
            dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", abs(clockwiseCount))
            print("anticlockwise", clockwiseCount)
            time.sleep(1)
        else:
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Setting mode", "Done")
            if clockwiseCount == 0:
                print("Expected and actual are same , so rotate count:0", clockwiseCount)
            else:
                dutils.rotateDial(myNodeId, ep, "Clockwise", abs(clockwiseCount))
                print("clockwise", clockwiseCount)
                time.sleep(5)

        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Frost Temperature", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(2)
        context.reporter.ReportEvent("Event Log", "Tick is on Confirm for Frost Temperature of " + frostExpected,
                                     "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
        time.sleep(5)

@when(
    u'The holiday set for Current day for {timeInMin} min for temperature {ExpectedHolidayTemp} degrees and cancel {CancelFlag} on the {strDeviceType}')
def setHolidayMode(context, timeInMin, ExpectedHolidayTemp, CancelFlag, strDeviceType):
    myNodeId, ep, respSate = OCRprerequisite(context, strDeviceType)
    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        dutils.wakeUpTheDevice(context, myNodeId, ep)
        context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done")
        dutils.rotateDial(myNodeId, ep, "Clockwise", 2)
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is rotated ANTICLOCKWISE to holiday current day as End date",
                                     "Done")
        dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", 7)
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Holiday", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise set end time after expected time", "Done")
        dutils.rotateDial(myNodeId, ep, "Clockwise", int(timeInMin))
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Confirmating time", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Confirmating time", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        frostActualValue = utils.getFrostTemperature()
        clockwiseCount = int(frostActualValue) - int(ExpectedHolidayTemp)
        if clockwiseCount > 0:
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Setting mode", "Done")
            dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", clockwiseCount)
            time.sleep(3)
        else:
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Setting mode", "Done")
            dutils.rotateDial(myNodeId, ep, "Clockwise", abs(clockwiseCount))
            time.sleep(3)
        context.reporter.ReportEvent("Event Log", "Dial is Pressed  for Confirmating time", "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(3)
        context.reporter.ReportEvent("Event Log",
                                     "Tick is on Confirm for  Temperature of" + ExpectedHolidayTemp + ' for holiday',
                                     "Done")
        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
        if CancelFlag is True:
            time.sleep(3)
            context.reporter.ReportEvent("Event Log",
                                         "Cancel " + ExpectedHolidayTemp + ' for holiday',
                                         "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Back", "Press")
            AT.stopThreads()

        AT.stopThreads()

@then(u'Validate {expectedFrostTemperature} on Platform and device for {strDeviceType}')
def validateFrostWithPlatform(context, expectedFrostTemperature, strDeviceType):
    _, _, _ = OCRprerequisite(context, strDeviceType, False)
    time.sleep(15)
    frostActualValue = utils.getFrostTemperature()
    if int(frostActualValue) == int(expectedFrostTemperature):
        context.reporter.ReportEvent("Event Log",
                                     "Expected $$ Value On Zigbee @@@ $~Current Frost Temperature$$" + expectedFrostTemperature + " $~ Zigbee Current Frost Temperature on Stat$$" + frostActualValue,
                                     "PASS")
    else:
        context.reporter.ReportEvent("Event Log",
                                     "Expected $$ Value On Zigbee @@@ $~Current Frost Temperature$$" + expectedFrostTemperature + " $~ Zigbee Current Frost Temperature on Stat$$" + frostActualValue,
                                     "Fail")
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        if 'frostProtectTemperature' in oNode['attributes']:
            platformFrostValue = int(round(oNode['attributes']['frostProtectTemperature']['displayValue']))
            if platformFrostValue == int(expectedFrostTemperature):
                context.reporter.ReportEvent("Event Log",
                                             "Expected $$ Value On Platform @@@ $~Current Frost Temperature$$" + expectedFrostTemperature + " $~ Platform Current Frost Temperature on Stat$$" + str(
                                                 platformFrostValue),
                                             "PASS")
            else:
                context.reporter.ReportEvent("Event Log",
                                             "Expected $$ Value Platform @@@ $~Current Frost Temperature$$" + expectedFrostTemperature + " $~ Platform Current Frost Temperature on Stat$$" + str(
                                                 platformFrostValue),
                                             "Fail")

def readStatVoltageAttr(reporter, nodeId, screen_name):
    print('Reading the device attribute ...')
    respState, respCode, respValue = utils.readAttribute("MANUFACTURER", nodeId, "09", "0", "0001", "0020")
    voltage_value = float(int(respValue.split(',')[5], 16)/10)
    if voltage_value < 3.2:
        reporter.ReportEvent("Test Validation ","The voltage attribute has a value  of {0} volts - Response [{1}] when the {2} is shown ".format(voltage_value, respValue, screen_name), "FAIL")
    else :
        reporter.ReportEvent("Test Validation", "The voltage attribute has a value  of {0} volts - Response [{1}] when the {2} is shown".format(voltage_value, respValue, screen_name), "PASS")

@When(
    u'the {strDeviceType} is rebooted after {time_val:d} min')
def rebootDevice(context, strDeviceType, time_val):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize("rebooted the" + strDeviceType)
    macId = dutils.getDeviceMACWithModel(strDeviceType, True)
    myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType, macId)
    context.nodeId = myNodeId
    myEp = "09"
    context.myEPList = myEp
    sleep_time = int(time_val) * 60
    print('The sleep time is {}'.format(sleep_time))
    #myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, "", context, "English")
    longPollInt, checkInInt = AT.setCompletFastPoll(myNodeId, myEp)
    respSate = AT.setFastPoll()
    while True:
     if dutils.rebootDevice(myNodeId, "09"):
        context.reporter.ReportEvent("Test Validation", "Reboot of stat is successful", "PASS")
        time.sleep(9)
        readStatVoltageAttr(context.reporter, myNodeId, 'Welcome Screen')
        time.sleep(5)
        readStatVoltageAttr(context.reporter, myNodeId, 'Reconnecting Screen')
        time.sleep(10)
        readStatVoltageAttr(context.reporter, myNodeId, 'Landing Screen')
        time.sleep(40)
        readStatVoltageAttr(context.reporter, myNodeId, 'Landing Screen(40 seconds after reboot)')
        AT.setCompletFastPoll(myNodeId, myEp)
        time.sleep(sleep_time)
     else:
        context.reporter.ReportEvent("Test Validation", "Reboot of stat is unsuccessful", "FAIL")


@When(
    u'the {strDeviceType} is {strFunction} via telegesis to change {strType} mode to {strMode} with Target Temperature as {strTemp} in {strLang}')
def rebootDevice(context, strDeviceType, strFunction, strType, strMode, strTemp, strLang):
    if strType.upper().find('HOTWATER') >= 0:
        context.oThermostatEP = context.oThermostatClass.waterEP
    elif strType.upper().find('PLUG') >= 0:
        context.oThermostatEP = context.oThermostatClass.plugEP
    else:
        context.oThermostatEP = context.oThermostatClass.heatEP

    if "SLR" in str(strDeviceType).upper():

        context.reporter.HTML_TC_BusFlowKeyword_Initialize(strFunction + " the " + strDeviceType)
        macId = dutils.getDeviceMACWithModel(strDeviceType, True)
        myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType, macId)
        context.nodeId = myNodeId
        myEp = dutils.getDeviceEPWithModel(strDeviceType, True)
        context.myEPList = myEp
        oLang = oUtils.getLanguage(strLang)
        strMode = oUtils.getModeText(strMode, strType, oLang)
        if "REBOOT" in str(strFunction).upper():
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Reboot the BM")
            if dutils.rebootDevice(myNodeId, "05"):
                context.reporter.ReportEvent("Test Validation", "Reboot of BM is successful", "PASS")
            else:
                context.reporter.ReportEvent("Test Validation", "Reboot of BM is unsuccessful", "FAIL")
            print("\n" + myNodeId + "---" + myEp[0])
            dutils.rebootDevice(myNodeId, myEp[0])
            time.sleep(5)
            mySetpoint = float(strTemp)
            context.oThermostatEP.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)
            if "OFF" in str(strMode).upper():
                context.oThermostatEP.model.mode = strMode
        context.oThermostatEP.update()

@When(u'the below {strType} schedule is set on the {strDeviceType} screen in {strLang} using {strOption}')
def setCustomSchedule(context, strType, strDeviceType, strLang, strOption):
    global ep, myEp, myNodeId
    myNodeId, myEp, ep, oLang, longPollInt, checkInInt = startUpOCR(strDeviceType, strType, context, strLang)
    strMode = oUtils.getModeText('schedule', strType, oLang)
    respSate = AT.setFastPoll()
    oSchedDict = {}
    oSchedDict.clear()
    oSchedDict = oSchdUtil.createWeekSceduleFormatFromTable(context)
    magicNumber = 7.0
    context.oSchedDict = oSchedDict


    if respSate:
        context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
        if strOption.upper() == "STARTOVER":
            if str(strType).upper() == 'HEAT':
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                imgMenuName, imgHeatName, imgSchModeName, imgSOModeName, imgSOModeConfirmName, imgTypeConfirmName, imgSOModeEEName, imgSOModeEEEdit = oUtils.navigateToHotWaterScheduleStartOverEE(context, myNodeId, ep)
                DayValue = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}
                timeValue = {"00":0,"15":1,"30":2,"45":3}
                lstReport = []
                counter = 0
                for oRows in context.table:
                    counter = counter + 1
                    #dutils.rotateDial(myNodeId, ep, "AntiClockwise", 7)
                    time.sleep(1)
                    if DayValue[oRows['Day']] > 0:
                        dutils.rotateDial(myNodeId,ep,"clockwise",DayValue[oRows['Day']])
                    time.sleep(5)
                    print("Pressing Dial")
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(8)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM,"Event Log",
                                                 "Dial is Pressed to Select "+oRows['Day'],
                                                 "Done"])
                    print("Pressing Tick")
                    dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                    time.sleep(5)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Tick is Pressed to Select " + oRows['Day'],
                                      "Done"])
                    time.sleep(1)
                    dutils.rotateDial(myNodeId, ep, "AntiClockwise", 30)
                    time.sleep(1)
                    oImg, imgSOModeEEM = oUtils.captureOriginal(context)

                    if oRows['Event1'] is not None:
                        if str(oRows['Event1']) is "":
                            context.reporter.ReportEvent("Event Log","Please enter the event1","FAIL")
                            exit()
                        else:
                            if float(str(oRows['Event1']).split(",")[1].split(".")[0]) == 1.0:
                                oRows['Event1'] = str(oRows['Event1']).replace(",1.0",","+str(magicNumber))
                            intRot = (int(str(oRows['Event1']).split(":")[0]) * 4) + timeValue[str(oRows['Event1']).split(":")[1].split(",")[0]]
                            if intRot > 0:
                                time.sleep(3)
                                dutils.rotateDial(myNodeId, ep, "clockwise", intRot)
                            time.sleep(4)
                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                            lstReport.append([imgSOModeEEM, "Event Log",
                                              "Dial is Rotatate to start time " + str(oRows['Event1']).split(",")[0],
                                              "Done"])
                            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                            time.sleep(3)
                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                            lstReport.append([imgSOModeEEM, "Event Log",
                                              "Dial is Pressed at start time " + str(oRows['Event1']).split(",")[0],
                                              "Done"])
                            intDecRot = 0
                            if int(str(oRows['Event1']).split(",")[1].split(".")[1]) > 0:
                                intDecRot = 1

                            intTempRot = 0
                            if int(str(oRows['Event1']).split(",")[1].split(".")[0]) == 18:
                                intTempRot = 0
                                if (intTempRot + intDecRot) > 0:
                                    dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                            if int(str(oRows['Event1']).split(",")[1].split(".")[0]) > 18:
                                intTempRot = ((int(str(oRows['Event1']).split(",")[1].split(".")[0]) -18) * 2)
                                dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                            if int(str(oRows['Event1']).split(",")[1].split(".")[0]) < 18:
                                intTempRot = ((18-(int(str(oRows['Event1']).split(",")[1].split(".")[0]))) * 2)
                                dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                            time.sleep(2)
                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                            lstReport.append([imgSOModeEEM, "Event Log",
                                              "Dial is rotated for the temperature " + str(oRows['Event1']).split(",")[1],
                                              "Done"])
                            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                            time.sleep(2)
                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                            lstReport.append([imgSOModeEEM, "Event Log",
                                              "Dial is Pressed at start time " + str(oRows['Event1']).split(",")[1],
                                              "Done"])
                            intValue = (int(str(oRows['Event2']).split(":")[0]) * 4) + timeValue[
                                str(oRows['Event2']).split(":")[1].split(",")[0]] - (intRot + 4)
                            if intValue > 0:
                                dutils.rotateDial(myNodeId, ep, "clockwise", intValue)

                            if intValue < 0:
                                dutils.rotateDial(myNodeId, ep, "anticlockwise", intValue)
                            time.sleep(2)
                            intRot = intRot + 4 + intValue
                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                            lstReport.append([imgSOModeEEM, "Event Log",
                                              "Dial is rotated to time " + str(oRows['Event2']).split(",")[0],
                                              "Done"])
                            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                            time.sleep(1)
                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                            lstReport.append([imgSOModeEEM, "Event Log",
                                              "Dial is Pressed at End Time",
                                              "Done"])
                            if oRows['Event3'] is not None:
                                if str(oRows['Event3']) is not "":
                                    if float(str(oRows['Event3']).split(",")[1].split(".")[0]) == 1.0:
                                        oRows['Event3'] = str(oRows['Event3']).replace(",1.0", "," + str(magicNumber))
                                    dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                                    time.sleep(3)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is rotated to No",
                                                      "Done"])
                                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                    time.sleep(3)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is Pressed at No",
                                                      "Done"])
                                    intValue = (int(str(oRows['Event3']).split(":")[0]) * 4) + timeValue[
                                        str(oRows['Event3']).split(":")[1].split(",")[0]] - (intRot + 4)
                                    if intValue > 0:
                                        dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                                    if intValue < 0:
                                        dutils.rotateDial(myNodeId, ep, "anticlockwise", intValue)
                                    time.sleep(1)
                                    intRot = intRot + 4 + intValue
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is rotated to time " + str(oRows['Event3']).split(",")[0],
                                                      "Done"])

                                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                    time.sleep(1)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is Pressed at start time " + str(oRows['Event3']).split(",")[0],
                                                      "Done"])

                                    intDecRot = 0
                                    if int(str(oRows['Event3']).split(",")[1].split(".")[1]) > 0:
                                        intDecRot = 1

                                    intTempRot = 0
                                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) == 18:
                                        intTempRot = 0
                                        if (intTempRot + intDecRot) > 0:
                                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) > 18:
                                        intTempRot = ((int(str(oRows['Event3']).split(",")[1].split(".")[0]) - 18) * 2)
                                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) < 18:
                                        intTempRot = ((18 - (int(str(oRows['Event3']).split(",")[1].split(".")[0]))) * 2)
                                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                                    time.sleep(1)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is rotated for the temperature " +
                                                      str(oRows['Event3']).split(",")[1],
                                                      "Done"])
                                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                    time.sleep(1)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is Pressed for Event 3 confirmation",
                                                      "Done"])
                                    intValue = (int(str(oRows['Event4']).split(":")[0]) * 4) + timeValue[
                                        str(oRows['Event4']).split(":")[1].split(",")[0]] - (intRot + 4)
                                    if intValue > 0:
                                        dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                                    if intValue < 0:
                                        dutils.rotateDial(myNodeId, ep, "anticlockwise", intValue)
                                    time.sleep(1)
                                    intRot = intRot + 4 + intValue
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is rotated to time " + str(oRows['Event4']).split(",")[0],
                                                      "Done"])
                                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                    time.sleep(1)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is Pressed at End Time",
                                                      "Done"])
                                    if oRows['Event5'] is not None:
                                        if str(oRows['Event5']) is not "":
                                            if float(str(oRows['Event5']).split(",")[1].split(".")[0]) == 1.0:
                                                oRows['Event5'] = str(oRows['Event5']).replace(",1.0",
                                                                                               "," + str(magicNumber))
                                            dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                                            time.sleep(3)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is rotated to No",
                                                              "Done"])
                                            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                            time.sleep(3)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is Pressed at No",
                                                              "Done"])
                                            intValue = (int(str(oRows['Event5']).split(":")[0]) * 4) + timeValue[
                                                str(oRows['Event5']).split(":")[1].split(",")[0]] - (intRot + 4)
                                            if intValue > 0:
                                                dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                                            if intValue < 0:
                                                dutils.rotateDial(myNodeId, ep, "anticlockwise", intValue)
                                            time.sleep(1)
                                            intRot = intRot + 4 + intValue
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is rotated to time " + str(oRows['Event5']).split(",")[
                                                                  0],
                                                              "Done"])
                                            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                            time.sleep(1)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is Pressed at start time " +
                                                              str(oRows['Event5']).split(",")[0],
                                                              "Done"])

                                            intDecRot = 0
                                            if int(str(oRows['Event5']).split(",")[1].split(".")[1]) > 0:
                                                intDecRot = 1

                                            intTempRot = 0
                                            if int(str(oRows['Event5']).split(",")[1].split(".")[0]) == 18:
                                                intTempRot = 0
                                                if (intTempRot + intDecRot) > 0:
                                                    dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                                            if int(str(oRows['Event5']).split(",")[1].split(".")[0]) > 18:
                                                intTempRot = (
                                                (int(str(oRows['Event5']).split(",")[1].split(".")[0]) - 18) * 2)
                                                dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                                            if int(str(oRows['Event5']).split(",")[1].split(".")[0]) < 18:
                                                intTempRot = (
                                                (18 - (int(str(oRows['Event5']).split(",")[1].split(".")[0]))) * 2)
                                                dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                                            time.sleep(1)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is rotated for the temperature " +
                                                              str(oRows['Event5']).split(",")[1],
                                                              "Done"])
                                            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                            time.sleep(1)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is Pressed for Event 3 confirmation",
                                                              "Done"])
                                            intValue = (int(str(oRows['Event6']).split(":")[0]) * 4) + timeValue[
                                                str(oRows['Event6']).split(":")[1].split(",")[0]] - (intRot + 4)
                                            if intValue > 0:
                                                dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                                            if intValue < 0:
                                                dutils.rotateDial(myNodeId, ep, "anticlockwise", intValue)
                                            time.sleep(1)
                                            intRot = intRot + 4 + intValue
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is rotated to time " + str(oRows['Event6']).split(",")[
                                                                  0],
                                                              "Done"])
                                            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                            time.sleep(1)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is Pressed at End Time",
                                                              "Done"])
                                            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                                            time.sleep(5)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Tick is Pressed to confirm",
                                                              "Done"])
                                            time.sleep(2)
                                        else:
                                            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                            time.sleep(5)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is Pressed at Yes",
                                                              "Done"])
                                            dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                                            time.sleep(5)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Tick is Pressed to confirm",
                                                              "Done"])
                                            dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                                            time.sleep(5)
                                            _, imgSOModeEEM = oUtils.captureOriginal(context)
                                            lstReport.append([imgSOModeEEM, "Event Log",
                                                              "Dial is rotated to No",
                                                              "Done"])
                                else:
                                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                                    time.sleep(1)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is Pressed at Yes",
                                                      "Done"])
                                    dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                                    time.sleep(1)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Tick is Pressed to confirm",
                                                      "Done"])
                                    dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                                    time.sleep(1)
                                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                                    lstReport.append([imgSOModeEEM, "Event Log",
                                                      "Dial is rotated to No",
                                                      "Done"])
                        dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                        time.sleep(3)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM, "Event Log",
                                          "Dial is rotated to No",
                                          "Done"])
                        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                        time.sleep(3)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM, "Event Log",
                                          "Dial is Pressed at No",
                                          "Done"])
                        if len(context.table.rows) > counter:
                            dutils.rotateDial(myNodeId, ep, "Anticlockwise", 6)
                            time.sleep(4)
                context.oThermostatEP.model.mode = "AUTO"
                nowTime = CTM.getTestTime(CTM.timeOffset)
                scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
                context.oThermostatEP.model.occupiedHeatingSetpoint = scheduleSetpoint
                context.oThermostatEP.update()
                # Getting weekly schedule after the Set Schedule
                context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
            if str(strType).upper() == 'HOTWATER':
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                _, imgWakeName = oUtils.captureOriginal(context)
                imgMenuName, imgHotMenuName, imgHotWaterMenuName, imgSchModeName, imgSOModeName, imgSOModeConfirmName, imgTypeConfirmName = oUtils.navigateToHotWaterStartover(context, myNodeId,ep)
                _, imgSOModeEEEdit = oUtils.pressAndCature(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                                           "Dial is Pressed to Edit Hotwater Schedule StartOver", "Done")
                DayValue = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}
                timeValue = {"00":0,"15":1,"30":2,"45":3}
                lstReport = []
                counter = 0
                for oRows in context.table:
                    counter = counter + 1
                    #dutils.rotateDial(myNodeId, ep, "AntiClockwise", 7)
                    time.sleep(1)
                    if DayValue[oRows['Day']] > 0:
                        dutils.rotateDial(myNodeId,ep,"clockwise",DayValue[oRows['Day']])
                    time.sleep(5)
                    print("Pressing Dial")
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(8)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM,"Event Log",
                                                 "Dial is Pressed to Select "+oRows['Day'],
                                                 "Done"])
                    print("Pressing Tick")

                    time.sleep(1)
                    dutils.rotateDial(myNodeId, ep, "AntiClockwise", 30)
                    time.sleep(1)
                    oImg, imgSOModeEEM = oUtils.captureOriginal(context)

                    if oRows['Event1'] is not None:
                        if str(oRows['Event1']) is "":
                            context.reporter.ReportEvent("Event Log","Please enter the event1","FAIL")
                            exit()
                        else:
                            oUtils.navigateAndSetHWScheduleEvents(context, myNodeId, ep, oRows, lstReport, edit=False,
                                                           startover=True)

                        del DayValue[oRows['Day']]
                        counter = 0
                        for oday in DayValue:
                            DayValue[oday] = int(DayValue[oday] - 1)
                context.oThermostatEP.model.mode = "AUTO"
                nowTime = CTM.getTestTime(CTM.timeOffset)
                scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
                context.reporter.ReportEvent("OCR Validation", "scheduleSetpoint " + str(scheduleSetpoint), "Done")
                if scheduleSetpoint == 0:
                    context.oThermostatEP.model.thermostatRunningState = '0000'
                else:
                    context.oThermostatEP.model.thermostatRunningState = '0001'
                # Getting weekly schedule after the Set Schedule
                context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        if strOption.upper() == "EDIT":
            if str(strType).upper() == 'HEAT':
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                imgMenuName, imgHeatName, imgSchModeName = oUtils.navigateToHeadScheduleScreen(context, myNodeId, ep)
                if context.oThermostatEP.model.mode is not "AUTO":
                    context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Heat Schedule edit mode",
                                                 "Done")
                    dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
                    time.sleep(3)
                    _, imgSOModeName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(3)

                DayValue = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}
                timeValue = {"00":0,"15":1,"30":2,"45":3}
                lstReport = []
                counter = 0

                for oRows in context.table:
                    counter = counter + 1
                    #dutils.rotateDial(myNodeId, ep, "AntiClockwise", 7)
                    time.sleep(1)
                    if DayValue[oRows['Day']] > 0:
                        dutils.rotateDial(myNodeId,ep,"clockwise",DayValue[oRows['Day']])
                    time.sleep(5)
                    print("Pressing Dial")
                    if counter == 1:
                        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                        time.sleep(5)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM,"Event Log",
                                                     "Dial is Pressed to Select "+oRows['Day'],
                                                     "Done"])
                    print("Pressing Tick")
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed to Select " + oRows['Day'],
                                      "Done"])
                    time.sleep(1)
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed to Select " + oRows['Day'],
                                      "Done"])
                    time.sleep(1)
                    dutils.rotateDial(myNodeId, ep, "AntiClockwise", 30)
                    time.sleep(1)
                    oImg, imgSOModeEEM = oUtils.captureOriginal(context)



                    if float(str(oRows['Event1']).split(",")[1].split(".")[0]) == 1.0:
                        oRows['Event1'] = str(oRows['Event1']).replace(",1.0",","+str(magicNumber))

                    intRot = (int(str(oRows['Event1']).split(":")[0]) * 4) + timeValue[str(oRows['Event1']).split(":")[1].split(",")[0]]
                    if intRot > 0:
                        time.sleep(3)
                        dutils.rotateDial(myNodeId, ep, "clockwise", intRot)
                    time.sleep(4)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Rotatate to start time " + str(oRows['Event1']).split(",")[0],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event1']).split(",")[0],
                                      "Done"])
                    intDecRot = 0
                    if int(str(oRows['Event1']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event1']).split(",")[1].split(".")[0]) == 18:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event1']).split(",")[1].split(".")[0]) > 18:
                        intTempRot = ((int(str(oRows['Event1']).split(",")[1].split(".")[0]) -18) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event1']).split(",")[1].split(".")[0]) < 18:
                        intTempRot = ((18-(int(str(oRows['Event1']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " + str(oRows['Event1']).split(",")[1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event1']).split(",")[1],
                                      "Done"])

                    if float(str(oRows['Event2']).split(",")[1].split(".")[0]) == 1.0:
                        oRows.cells[2] = str(oRows['Event2']).replace(",1.0",","+str(magicNumber))

                    intValue = (int(str(oRows['Event2']).split(":")[0]) * 4) + timeValue[
                        str(oRows['Event2']).split(":")[1].split(",")[0]] - (intRot + 8)
                    if intValue > 0:
                        dutils.rotateDial(myNodeId, ep, "clockwise", intValue)

                    if intValue < 0:
                        dutils.rotateDial(myNodeId, ep, "anticlockwise", intValue)
                    time.sleep(2)
                    intRot = intRot + 8 + intValue
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated to time " + str(oRows['Event2']).split(",")[0],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    intDecRot = 0
                    if int(str(oRows['Event2']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event2']).split(",")[1].split(".")[0]) == 7:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event2']).split(",")[1].split(".")[0]) > 7:
                        intTempRot = ((int(str(oRows['Event2']).split(",")[1].split(".")[0]) - 7) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event2']).split(",")[1].split(".")[0]) < 7:
                        intTempRot = ((7 - (int(str(oRows['Event2']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " + str(oRows['Event2']).split(",")[
                                          1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event2']).split(",")[1],
                                      "Done"])

                    intValue = (int(str(oRows['Event3']).split(":")[0]) * 4) + timeValue[
                        str(oRows['Event3']).split(":")[1].split(",")[0]] - (intRot + 14)
                    if intValue > 0:
                        dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                    if intValue < 0:
                        dutils.rotateDial(myNodeId, ep, "anticlockwise", (intValue * -1))
                    time.sleep(1)
                    intRot = intRot + 14 + intValue
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated to time " + str(oRows['Event3']).split(",")[0],
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event3']).split(",")[0],
                                      "Done"])



                    if float(str(oRows['Event3']).split(",")[1].split(".")[0]) == 1.0:
                        oRows['Event3'] = str(oRows['Event3']).replace(",1.0", "," + str(magicNumber))
                    if float(str(oRows['Event4']).split(",")[1].split(".")[0]) == 1.0:
                        oRows.cells[4] = str(oRows['Event4']).replace(",1.0",","+str(magicNumber))

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at No",
                                      "Done"])


                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event3']).split(",")[0],
                                      "Done"])


                    intDecRot = 0
                    if int(str(oRows['Event3']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) == 7:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) > 7:
                        intTempRot = ((int(str(oRows['Event3']).split(",")[1].split(".")[0]) - 7) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) < 7:
                        intTempRot = ((7 - (int(str(oRows['Event3']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " +
                                      str(oRows['Event3']).split(",")[1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed for Event 3 confirmation",
                                      "Done"])
                    intValue = (int(str(oRows['Event4']).split(":")[0]) * 4) + timeValue[
                        str(oRows['Event4']).split(":")[1].split(",")[0]] - (intRot + 14)
                    if intValue > 0:
                        dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                    if intValue < 0:
                        dutils.rotateDial(myNodeId, ep, "anticlockwise", (intValue * -1))
                        time.sleep(1)
                    intRot = intRot + 14 + intValue
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated to time " + str(oRows['Event4']).split(",")[0],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    intDecRot = 0
                    if int(str(oRows['Event4']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event4']).split(",")[1].split(".")[0]) == 7:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event4']).split(",")[1].split(".")[0]) > 7:
                        intTempRot = ((int(str(oRows['Event4']).split(",")[1].split(".")[0]) - 7) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event4']).split(",")[1].split(".")[0]) < 7:
                        intTempRot = ((7 - (int(str(oRows['Event4']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " + str(oRows['Event4']).split(",")[
                                          1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event4']).split(",")[1],
                                      "Done"])
                    if float(str(oRows['Event5']).split(",")[1].split(".")[0]) == 1.0:
                        oRows['Event5'] = str(oRows['Event5']).replace(",1.0",
                                                                       "," + str(magicNumber))

                    if float(str(oRows['Event6']).split(",")[1].split(".")[0]) == 1.0:
                        oRows.cells[6] = str(oRows['Event6']).replace(",1.0",","+str(magicNumber))

                    intValue = (int(str(oRows['Event5']).split(":")[0]) * 4) + timeValue[
                        str(oRows['Event5']).split(":")[1].split(",")[0]] - (intRot + 14)
                    if intValue > 0:
                        dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                    if intValue < 0:
                        dutils.rotateDial(myNodeId, ep, "anticlockwise", (intValue*-1))
                    time.sleep(1)
                    intRot = intRot + 14 + intValue
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated to time " + str(oRows['Event5']).split(",")[
                                          0],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " +
                                      str(oRows['Event5']).split(",")[0],
                                      "Done"])



                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at No",
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at No",
                                      "Done"])


                    intDecRot = 0
                    if int(str(oRows['Event5']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event5']).split(",")[1].split(".")[0]) == 18:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event5']).split(",")[1].split(".")[0]) > 18:
                        intTempRot = (
                        (int(str(oRows['Event5']).split(",")[1].split(".")[0]) - 18) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event5']).split(",")[1].split(".")[0]) < 18:
                        intTempRot = (
                        (18 - (int(str(oRows['Event5']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " +
                                      str(oRows['Event5']).split(",")[1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed for Event 3 confirmation",
                                      "Done"])
                    intValue = (int(str(oRows['Event6']).split(":")[0]) * 4) + timeValue[
                        str(oRows['Event6']).split(":")[1].split(",")[0]] - (intRot + 26)
                    if intValue > 0:
                        dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                    if intValue < 0:
                        dutils.rotateDial(myNodeId, ep, "anticlockwise", (intValue * -1))
                    time.sleep(1)
                    intRot = intRot + 26 + intValue
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated to time " + str(oRows['Event6']).split(",")[
                                          0],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    intDecRot = 0
                    if int(str(oRows['Event6']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event6']).split(",")[1].split(".")[0]) == 7:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event6']).split(",")[1].split(".")[0]) > 7:
                        intTempRot = ((int(str(oRows['Event6']).split(",")[1].split(".")[0]) - 7) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event6']).split(",")[1].split(".")[0]) < 7:
                        intTempRot = ((7 - (int(str(oRows['Event6']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " + str(oRows['Event6']).split(",")[
                                          1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event6']).split(",")[1],
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                    time.sleep(5)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Tick is Pressed to confirm",
                                      "Done"])
                    time.sleep(2)

                    if len(DayValue) > 0:
                        del DayValue[oRows['Day']]
                        for oday in DayValue:
                            DayValue[oday] = int(DayValue[oday] - 1)
                        dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                        time.sleep(3)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM, "Event Log",
                                          "Dial is rotated to No",
                                          "Done"])
                        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                        time.sleep(3)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM, "Event Log",
                                          "Dial is Pressed at No",
                                          "Done"])

                context.oThermostatEP.model.mode = "AUTO"
                nowTime = CTM.getTestTime(CTM.timeOffset)
                scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
                context.oThermostatEP.model.occupiedHeatingSetpoint = scheduleSetpoint
                context.oThermostatEP.update()
                # Getting weekly schedule after the Set Schedule
                context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
            if str(strType).upper() == 'HOTWATER':
                dutils.wakeUpTheDevice(context, myNodeId, ep)

                _, imgWakeName = oUtils.captureOriginal(context)
                imgMenuName, imgHotMenuName, imgHotWaterMenuName, imgSchModeName = oUtils.naviagateToScheduleScreen(
                    context,
                    myNodeId,
                    ep)

                DayValue = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}
                timeValue = {"00":0,"15":1,"30":2,"45":3}
                lstReport = []
                counter = 0

                for oRows in context.table:
                    counter = counter + 1
                    # dutils.rotateDial(myNodeId, ep, "AntiClockwise", 7)
                    time.sleep(1)
                    if DayValue[oRows['Day']] > 0:
                        dutils.rotateDial(myNodeId, ep, "clockwise", DayValue[oRows['Day']])
                    time.sleep(5)
                    print("Pressing Dial")
                    if counter == 1:
                        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                        time.sleep(5)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM, "Event Log",
                                          "Dial is Pressed to Select " + oRows['Day'],
                                          "Done"])
                    print("Pressing Tick")

                    oUtils.navigateAndSetHWScheduleEvents(context, myNodeId, ep, oRows, lstReport, edit=True, startover=False)

                    if len(DayValue) > 0:
                        del DayValue[oRows['Day']]
                        for oday in DayValue:
                            DayValue[oday] = int(DayValue[oday] - 1)
                        dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                        time.sleep(3)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM, "Event Log",
                                          "Dial is rotated to No",
                                          "Done"])
                        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                        time.sleep(3)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM, "Event Log",
                                          "Dial is Pressed at No",
                                          "Done"])
                context.oThermostatEP.model.mode = "AUTO"
                nowTime = CTM.getTestTime(CTM.timeOffset)
                scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
                context.reporter.ReportEvent("OCR Validation", "scheduleSetpoint " + str(scheduleSetpoint), "Done")
                if scheduleSetpoint == 0:
                    context.oThermostatEP.model.thermostatRunningState = '0000'
                else:
                    context.oThermostatEP.model.thermostatRunningState = '0001'
                # Getting weekly schedule after the Set Schedule
                context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        if "COPY" in strOption.upper():
            if strType.upper() == 'HEAT':
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                _, imgWakeName = oUtils.captureOriginal(context)
                imgMenuName, imgHeatName, imgSchModeName = oUtils.navigateToHeadScheduleScreen(context, myNodeId, ep)
                if context.oThermostatEP.model.mode is not "AUTO":
                    context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Heat Schedule edit mode",
                                                 "Done")
                    dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
                    time.sleep(3)
                    _, imgSOModeName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed for Heat Schedule StartOver", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(3)

                DayValue = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}
                timeValue = {"00":0,"15":1,"30":2,"45":3}
                lstReport = []
                counter = 0

                for oRows in context.table:
                    counter = counter + 1
                    #dutils.rotateDial(myNodeId, ep, "AntiClockwise", 7)
                    time.sleep(1)
                    if DayValue[oRows['Day']] > 0:
                        dutils.rotateDial(myNodeId,ep,"clockwise",DayValue[oRows['Day']])
                    time.sleep(5)
                    print("Pressing Dial")
                    if counter == 1:
                        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                        time.sleep(5)
                        _, imgSOModeEEM = oUtils.captureOriginal(context)
                        lstReport.append([imgSOModeEEM,"Event Log",
                                                     "Dial is Pressed to Select "+oRows['Day'],
                                                     "Done"])
                    print("Pressing Tick")
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed to Select " + oRows['Day'],
                                      "Done"])
                    time.sleep(1)
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed to Select " + oRows['Day'],
                                      "Done"])
                    time.sleep(1)

                    if float(str(oRows['Event1']).split(",")[1].split(".")[0]) == 1.0:
                        oRows['Event1'] = str(oRows['Event1']).replace(",1.0",","+str(magicNumber))


                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event1']).split(",")[0],
                                      "Done"])
                    intDecRot = 0
                    if int(str(oRows['Event1']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event1']).split(",")[1].split(".")[0]) == 18:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event1']).split(",")[1].split(".")[0]) > 18:
                        intTempRot = ((int(str(oRows['Event1']).split(",")[1].split(".")[0]) -18) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event1']).split(",")[1].split(".")[0]) < 18:
                        intTempRot = ((18-(int(str(oRows['Event1']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " + str(oRows['Event1']).split(",")[1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event1']).split(",")[1],
                                      "Done"])


                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    intDecRot = 0
                    if int(str(oRows['Event2']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if float(str(oRows['Event2']).split(",")[1].split(".")[0]) == 1.0:
                        oRows.cells[2] = str(oRows['Event2']).replace(",1.0",","+str(magicNumber))
                    if int(str(oRows['Event2']).split(",")[1].split(".")[0]) == 7:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event2']).split(",")[1].split(".")[0]) > 7:
                        intTempRot = ((int(str(oRows['Event2']).split(",")[1].split(".")[0]) - 7) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event2']).split(",")[1].split(".")[0]) < 7:
                        intTempRot = ((7 - (int(str(oRows['Event2']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " + str(oRows['Event2']).split(",")[
                                          1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event2']).split(",")[1],
                                      "Done"])


                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event3']).split(",")[0],
                                      "Done"])



                    if float(str(oRows['Event3']).split(",")[1].split(".")[0]) == 1.0:
                        oRows['Event3'] = str(oRows['Event3']).replace(",1.0", "," + str(magicNumber))
                    if float(str(oRows['Event4']).split(",")[1].split(".")[0]) == 1.0:
                        oRows.cells[4] = str(oRows['Event4']).replace(",1.0",","+str(magicNumber))

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at No",
                                      "Done"])


                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event3']).split(",")[0],
                                      "Done"])


                    intDecRot = 0
                    if int(str(oRows['Event3']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) == 7:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) > 7:
                        intTempRot = ((int(str(oRows['Event3']).split(",")[1].split(".")[0]) - 7) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event3']).split(",")[1].split(".")[0]) < 7:
                        intTempRot = ((7 - (int(str(oRows['Event3']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " +
                                      str(oRows['Event3']).split(",")[1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed for Event 3 confirmation",
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    intDecRot = 0
                    if int(str(oRows['Event4']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event4']).split(",")[1].split(".")[0]) == 7:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event4']).split(",")[1].split(".")[0]) > 7:
                        intTempRot = ((int(str(oRows['Event4']).split(",")[1].split(".")[0]) - 7) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event4']).split(",")[1].split(".")[0]) < 7:
                        intTempRot = ((7 - (int(str(oRows['Event4']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " + str(oRows['Event4']).split(",")[
                                          1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event4']).split(",")[1],
                                      "Done"])
                    if float(str(oRows['Event5']).split(",")[1].split(".")[0]) == 1.0:
                        oRows['Event5'] = str(oRows['Event5']).replace(",1.0",
                                                                       "," + str(magicNumber))

                    if float(str(oRows['Event6']).split(",")[1].split(".")[0]) == 1.0:
                        oRows.cells[6] = str(oRows['Event6']).replace(",1.0",","+str(magicNumber))


                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated to time " + str(oRows['Event5']).split(",")[
                                          0],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " +
                                      str(oRows['Event5']).split(",")[0],
                                      "Done"])



                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at No",
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at No",
                                      "Done"])


                    intDecRot = 0
                    if int(str(oRows['Event5']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event5']).split(",")[1].split(".")[0]) == 18:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event5']).split(",")[1].split(".")[0]) > 18:
                        intTempRot = (
                        (int(str(oRows['Event5']).split(",")[1].split(".")[0]) - 18) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event5']).split(",")[1].split(".")[0]) < 18:
                        intTempRot = (
                        (18 - (int(str(oRows['Event5']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " +
                                      str(oRows['Event5']).split(",")[1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed for Event 3 confirmation",
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(1)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at End Time",
                                      "Done"])
                    intDecRot = 0
                    if int(str(oRows['Event6']).split(",")[1].split(".")[1]) > 0:
                        intDecRot = 1

                    intTempRot = 0
                    if int(str(oRows['Event6']).split(",")[1].split(".")[0]) == 7:
                        intTempRot = 0
                        if (intTempRot + intDecRot) > 0:
                            dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event6']).split(",")[1].split(".")[0]) > 7:
                        intTempRot = ((int(str(oRows['Event6']).split(",")[1].split(".")[0]) - 7) * 2)
                        dutils.rotateDial(myNodeId, ep, "clockwise", (intTempRot + intDecRot))
                    if int(str(oRows['Event6']).split(",")[1].split(".")[0]) < 7:
                        intTempRot = ((7 - (int(str(oRows['Event6']).split(",")[1].split(".")[0]))) * 2)
                        dutils.rotateDial(myNodeId, ep, "Anticlockwise", (intTempRot + intDecRot))
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is rotated for the temperature " + str(oRows['Event6']).split(",")[
                                          1],
                                      "Done"])
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(2)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Dial is Pressed at start time " + str(oRows['Event6']).split(",")[1],
                                      "Done"])

                    dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                    time.sleep(5)
                    _, imgSOModeEEM = oUtils.captureOriginal(context)
                    lstReport.append([imgSOModeEEM, "Event Log",
                                      "Tick is Pressed to confirm",
                                      "Done"])
                    time.sleep(2)


                    del DayValue[oRows['Day']]
                for oday in DayValue:
                    DayValue[oday] = int(DayValue[oday] - 1)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(3)
                _, imgSOModeEEM = oUtils.captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Dial is Pressed at No",
                                  "Done"])
                strCopyDays = str(strOption).split( )[4].split(",")
                for st in strCopyDays:
                    intRot = DayValue[st]
                    if intRot > 0:
                        dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
                        time.sleep(3)
                        _, imgSOModeName = oUtils.captureOriginal(context)
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(3)
                    context.reporter.ReportEvent("Event Log", "Dial is Pressed for copy to "+str(st)+" day", "Done")

                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(5)
                _, imgSOModeEEM = oUtils.captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Tick is Pressed to confirm",
                                  "Done"])

                dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
                time.sleep(5)
                _, imgSOModeEEM = oUtils.captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Tick is Pressed to confirm",
                                  "Done"])

                context.oThermostatEP.model.mode = "AUTO"
                nowTime = CTM.getTestTime(CTM.timeOffset)
                scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
                context.oThermostatEP.model.occupiedHeatingSetpoint = scheduleSetpoint
                context.oThermostatEP.update()
                # Getting weekly schedule after the Set Schedule
                context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
            if str(strType).upper() == 'HOTWATER':
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                _, imgWakeName = oUtils.captureOriginal(context)
                imgMenuName, imgHotMenuName, imgHotWaterMenuName, imgSchModeName = oUtils.naviagateToScheduleScreen(context,
                                                                                                             myNodeId,
                                                                                                             ep)

                DayValue = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}
                timeValue = {"00":0,"15":1,"30":2,"45":3}
                lstReport = []
                counter = 0

                for oRows in context.table:
                    counter = counter + 1
                    time.sleep(1)
                    if DayValue[oRows['Day']] > 0:
                        dutils.rotateDial(myNodeId, ep, "clockwise", DayValue[oRows['Day']])
                    time.sleep(5)

                    if counter == 1:
                        oUtils.pressAndAppendList(context,myNodeId, ep, "Dial", "Press",5 ,"Event Log", "Dial is Pressed to Select " + oRows['Day'], "Done", lstReport)

                    oUtils.navigateAndSetHWScheduleEvents(context, myNodeId, ep, oRows, lstReport,edit=False, startover=False)

                    del DayValue[oRows['Day']]

                for oday in DayValue:
                    DayValue[oday] = int(DayValue[oday] - 1)

                oUtils.pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 5, "Event Log","Dial is Pressed at No", "Done", lstReport)
                strCopyDays = str(strOption).split( )[4].split(",")
                for st in strCopyDays:
                    intRot = DayValue[st]
                    if intRot > 0:
                        dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
                        time.sleep(3)
                        _, imgSOModeName = oUtils.captureOriginal(context)
                    oUtils.pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 5, "Event Log","Dial is Pressed for copy to "+str(st)+" day", "Done", lstReport)

                oUtils.pressAndAppendList(context, myNodeId, ep, "Tick", "Press", 5, "Event Log",
                                          "Tick is Pressed to confirm", "Done", lstReport)

                oUtils.pressAndAppendList(context, myNodeId, ep, "Tick", "Press", 5, "Event Log",
                                         "Tick is Pressed to confirm", "Done", lstReport)
                dutils.rotateDial(myNodeId, ep, "clockwise", 1)

                oUtils.pressAndAppendList(context, myNodeId, ep, "Tick", "Press", 5, "Event Log",
                                          "Tick is Pressed to confirm", "Done", lstReport)
                context.oThermostatEP.model.mode = "AUTO"
                nowTime = CTM.getTestTime(CTM.timeOffset)
                scheduleSetpoint, _, _ = context.oThermostatEP.model._eventStatus(nowTime)
                context.reporter.ReportEvent("OCR Validation", "scheduleSetpoint " + str(scheduleSetpoint), "Done")
                if scheduleSetpoint == 0:
                    context.oThermostatEP.model.thermostatRunningState = '0000'
                else:
                    context.oThermostatEP.model.thermostatRunningState = '0001'
                # Getting weekly schedule after the Set Schedule
                context.oThermostatEP.update()
                context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
    else:
        context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")

def startUpOCR(strDeviceType,strType,context,strLang):
    myNodeId,myEp,ep = None, None, None
    if "devices" not in strDeviceType.split(" ")[0]:
        macId = dutils.getDeviceMACWithModel(strDeviceType.split(" ")[0], True)
        myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType.split(" ")[0], macId)
        context.nodeId = myNodeId
        myEp = dutils.getDeviceEPWithModel(strDeviceType.split(" ")[0], True)
        context.myEPList = myEp

    if strType.upper().find('HOTWATER') >= 0:
        context.oThermostatEP = context.oThermostatClass.waterEP
    elif strType.upper().find('PLUG') >= 0:
        context.oThermostatEP = context.oThermostatClass.plugEP
    else:
        context.oThermostatEP = context.oThermostatClass.heatEP
    oZDLJsonDict = dutils.getZigbeeDevicesJson()
    strBMType = None
    for oNode in oZDLJsonDict:
        if "SLR" in oZDLJsonDict[oNode]["name"]:
            strBMType = oZDLJsonDict[oNode]["name"]
    if strBMType is None:
        context.reporter.ReportEvent("Kit Validation", "The BM is not connected", "FAIL")
        exit()
    context.nodeId = myNodeId
    if "SLT3" in strDeviceType.upper():
        if "HEAT" in strType.upper():
            ep = myEp[0]
        if "HOTWATER" in strType.upper():
            if "SLR1" in strBMType:
                context.reporter.ReportEvent("Kit Validation","The BM Connected connected is not valid for Hot Water","FAIL")
                exit()
            ep = myEp[1]
    else:
        ep = context.myEPList[0]

    context.reporter.ReportEvent("Event Log", "Started setting fast poll", "Done")

    longPollInt, checkInInt = AT.setCompletFastPoll(myNodeId, ep)
    time.sleep(3)
    oLang = oUtils.getLanguage(strLang)
    return myNodeId,myEp,ep,oLang,longPollInt, checkInInt

@When(u'the {strType} {strMode} with {strTime} hours ahead after {strDays} days using button on the {strDeviceType} in {strLang} for the {strstart} date')
def SetHoliday(context, strType, strMode, strTime, strDays, strstart, strLang, strDeviceType):
    global oImgMenu, ep, myEp, myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Activate ' + strType + ' ' + strMode + ' mode on the thermostat')
    context.oThermostatEP = context.oThermostatClass.heatEP
    if "devices" not in strDeviceType.split(" ")[0]:
        macId = dutils.getDeviceMACWithModel(strDeviceType.split(" ")[0], True)
        myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType.split(" ")[0], macId)
        context.nodeId = myNodeId
        myEp = dutils.getDeviceEPWithModel(strDeviceType.split(" ")[0], True)
        context.myEPList = myEp
        ep = context.myEPList[0]
        if str(strType).upper() == 'HOLIDAY' and str(strstart).upper() == 'START':
            # mySetpoint = 1.0
            # holidayStartOffset = 60
            # intSetTempDuration = 604800
            longPollInt, checkInInt = AT.setCompletFastPoll(myNodeId, ep)
            time.sleep(3)
            oLang = oUtils.getLanguage(strLang)
            strMode = oUtils.getModeText(strMode, strType, oLang)
            respSate = AT.setFastPoll()
            if respSate:
                context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                oImgWake, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                time.sleep(1)
                oImgMenu, imgMenuName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
                dutils.rotateDial(myNodeId, ep, "Clockwise", 2)
                context.reporter.ReportEvent("Event Log", "Started setting fast poll", "Done")
                time.sleep(1)
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done")
                oImgHolMenu, imgHolMenuName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)

                # Dial to turn
                FixedTime = str(datetime.now())
                FixStartDate = FixedTime.split('-')
                FixStartDay = FixStartDate[2].split(' ')
                # Displays the initial set  Month
                Fixnum = int(FixStartDay[0])
                intdays = int(strDays)

                # Date for start time
                StartTime = str(datetime.now() + timedelta(days=intdays))
                ArrStartDate = StartTime.split('-')
                ArrStartDay = ArrStartDate[2].split(' ')

                # Displays the start Month
                intnum = int(ArrStartDay[0])

                # Difference of date, month and year
                diffDay = int(Fixnum) - int(intnum)
                diffMonth = int(FixStartDate[1]) - int(ArrStartDate[1])
                diffYear = int(FixStartDate[0]) - int(ArrStartDate[0])

                # To set for the date
                if diffDay > 0:
                    time.sleep(2)
                    dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", abs(diffDay))
                elif diffDay < 0:
                    time.sleep(2)
                    dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(diffDay))

                _, oImgHolFromDateName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Start Day is changed to " + ArrStartDay[0], "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)

                # To set for the Month
                if diffMonth > 0:
                    time.sleep(2)
                    dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", abs(diffMonth))
                elif diffMonth < 0:
                    time.sleep(2)
                    dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(diffMonth))

                _, oImgHolFromMonName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Start Month is changed to " + ArrStartDate[1], "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)

                # To set for the Year
                if diffYear > 0:
                    time.sleep(2)
                    dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", abs(diffYear))
                elif diffYear < 0:
                    time.sleep(2)
                    dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(diffYear))

                _, oImgHolFromYearDateName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Start Year is changed to " + ArrStartDate[0], "Done")
                context.reporter.ReportEvent("Event Log",
                                             "Start Date is set to " + ArrStartDay[0] + " / " + ArrStartDate[
                                                 1] + " / " + ArrStartDate[0], "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)

                inthour = int(strTime)

                # Date for start time
                StartTime = str(datetime.now() + timedelta(hours=inthour))
                ArrStartTime = StartTime.split(' ')
                ArrStarthour = ArrStartTime[1].split(":")

                dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(inthour))
                _, oImgHolFromHourDateName = oUtils.captureOriginal(context)

                context.reporter.ReportEvent("Event Log", "Start Hour is changed to " + str(inthour) + "hours", "Done")
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)
                _, oImgHolFromDateConfirmName = oUtils.captureOriginal(context)
                time.sleep(2)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")

                Mode = oUtils.getText(oImgWake, context)
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)

                oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)

                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done",
                                             ocrImagePath=imgHolMenuName)

                oUtils.validateMainMenu(oImgHolMenu, imgHolMenuName, oLang, context)
                oImgHolFromDate = oUtils.loadImage(oImgHolFromDateName, context)
                context.reporter.ReportEvent("Event Log", "Dial is pressed to Holiday mode", "Done")
                oUtils.validateHolidayMenu(oImgHolFromDate, oImgHolFromDateName, oLang, context, "FROM", "DATE")
                oImgHolFromDate = None

                oImgHolFromMon = oUtils.loadImage(oImgHolFromMonName, context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Month", "Done")
                oUtils.validateHolidayMenu(oImgHolFromMon, oImgHolFromMonName, oLang, context, "FROM", "MONTH")
                oImgHolFromMon = None

                oImgHolFromYearDate = oUtils.loadImage(oImgHolFromYearDateName, context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Year", "Done")
                oUtils.validateHolidayMenu(oImgHolFromYearDate, oImgHolFromYearDateName, oLang, context, "FROM", "YEAR")
                oImgHolFromYearDate = None

                oImgHolFromHourDate = oUtils.loadImage(oImgHolFromHourDateName, context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select From Hour", "Done")
                oUtils.validateHolidayMenu(oImgHolFromHourDate, oImgHolFromHourDateName, oLang, context, "FROM", "HOUR")
                oImgHolFromHourDate = None

                oImgHolFromDateConfirm = oUtils.loadImage(oImgHolFromDateConfirmName, context)
                context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Start Date", "Done")
                oUtils.validateHolidayMenu(oImgHolFromDateConfirm, oImgHolFromDateConfirmName, oLang, context, "FROM",
                                           "CONFIRM")
                oImgHolFromDateConfirm = None

                context.oThermostatEP.model.mode = "HOLIDAY"
                context.oThermostatEP.model.holidayModeEnd = datetime.now() + timedelta(hours=inthour)

                context.oThermostatEP.update()

                context.oThermostatEP.model.mode = "HOLIDAY"
                context.oThermostatEP.model.holidayModeEnabled = '01'
                context.strHoldayStart = datetime.now() + timedelta(days=intdays)

                startDateString = datetime.strftime(datetime.now() + timedelta(days=intdays), "%Y%m%d")
                startTimeString = datetime.strftime(datetime.now() + timedelta(days=intdays), "%H:%M")
                startTimeHex = tt.timeStringToHex(startTimeString)

                context.oThermostatEP.model.holidayModeStart = context.oThermostatEP._buildHolidayDatetimeUTC(
                    startDateString, startTimeHex)

                context.oThermostatEP.update()

        elif str(strType).upper() == 'HOLIDAY' and str(strstart).upper() == 'END':

            dutils.wakeUpTheDevice(context, myNodeId, ep)
            oLang = oUtils.getLanguage(strLang)
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            # Dial to turn
            FixedTime = str(datetime.now())
            FixEndDate = FixedTime.split('-')
            FixEndDay = FixEndDate[2].split(' ')
            # Displays the initial set  Month
            Fixnum = int(FixEndDay[0])
            intdays = int(strDays)

            # Date for start time
            EndTime = str(datetime.now() + timedelta(days=intdays))
            ArrEndDate = EndTime.split('-')
            ArrEndDay = ArrEndDate[2].split(' ')

            # Displays the start Month
            intnum = int(ArrEndDay[0])

            # Difference of date, month and year
            diffDay = int(Fixnum) - int(intnum)
            diffMonth = int(FixEndDate[1]) - int(ArrEndDate[1])
            diffYear = int(FixEndDate[0]) - int(ArrEndDate[0])

            # To set for the date
            if diffDay > 0:
                time.sleep(2)
                dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", abs(diffDay))
            elif diffDay < 0:
                time.sleep(2)
                dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(diffDay))
            _, oImgHolToDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "End Day is changed to " + ArrEndDay[0], "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)

            # To set for the Month
            if diffMonth > 0:
                time.sleep(2)
                dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", abs(diffMonth))
            elif diffMonth < 0:
                time.sleep(2)
                dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(diffMonth))
            _, oImgHolToMonName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "End Month is changed to " + ArrEndDate[1], "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)

            # To set for the Year
            if diffYear > 0:
                time.sleep(2)
                dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", abs(diffYear))
            elif diffYear < 0:
                time.sleep(2)
                dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(diffYear))
            _, oImgHolToYearDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "End Year is changed to " + ArrEndDate[0], "Done")
            context.reporter.ReportEvent("Event Log",
                                         "Start Date is set to " + ArrEndDay[0] + " / " + ArrEndDate[
                                             1] + " / " + ArrEndDate[0], "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)

            inthour = int(strTime)

            # Date for start time
            EndTime = str(datetime.now() + timedelta(hours=inthour))
            ArrEndTime = EndTime.split(' ')
            ArrEndhour = ArrEndTime[1].split(":")

            dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(inthour))
            _, oImgHolToHourDateName = oUtils.captureOriginal(context)
            context.reporter.ReportEvent("Event Log", "End Hour is changed to "+str(inthour)+ "hours", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)
            _, oImgHolToDateConfirmName = oUtils.captureOriginal(context)

            context.reporter.ReportEvent("Event Log", "End date is set", "Done")
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(2)

            oImgHolToDate = oUtils.loadImage(oImgHolToDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done")
            oUtils.validateHolidayMenu(oImgHolToDate, oImgHolToDateName, oLang, context, "To", "DATE")
            oImgHolToDate = None

            oImgHolToMon = oUtils.loadImage(oImgHolToMonName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Month", "Done")
            oUtils.validateHolidayMenu(oImgHolToMon, oImgHolToMonName, oLang, context, "To", "MONTH")
            oImgHolToMon = None

            oImgHolToYearDate = oUtils.loadImage(oImgHolToYearDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Year", "Done")
            oUtils.validateHolidayMenu(oImgHolToYearDate, oImgHolToYearDateName, oLang, context, "To", "YEAR")
            oImgHolToYearDate = None

            oImgHolToHourDate = oUtils.loadImage(oImgHolToHourDateName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to select To Hour", "Done")
            oUtils.validateHolidayMenu(oImgHolToHourDate, oImgHolToHourDateName, oLang, context, "To", "HOUR")
            oImgHolToHourDate = None

            oImgHolToDateConfirm = oUtils.loadImage(oImgHolToDateConfirmName, context)
            context.reporter.ReportEvent("Event Log", "Dial is Pressed  to Confirm Start Date", "Done")
            oUtils.validateHolidayMenu(oImgHolToDateConfirm, oImgHolToDateConfirmName, oLang, context, "To",
                                       "CONFIRM")
            oImgHolToDateConfirm = None

            context.oThermostatEP.model.mode = "HOLIDAY"
            context.oThermostatEP.model.holidayModeEnd = datetime.now() + timedelta(hours=inthour)

            context.oThermostatEP.update()

            context.oThermostatEP.model.mode = "HOLIDAY"
            context.oThermostatEP.model.holidayModeEnabled = '01'
            context.strHoldayEnd = datetime.now() + timedelta(days=intdays)

            EndDateString = datetime.strftime(datetime.now() + timedelta(days=intdays), "%Y%m%d")
            EndTimeString = datetime.strftime(datetime.now() + timedelta(days=intdays), "%H:%M")
            EndTimeHex = tt.timeStringToHex(EndTimeString)

            context.oThermostatEP.model.holidayModeEnd = context.oThermostatEP._buildHolidayDatetimeUTC(
                EndDateString, EndTimeHex)

            context.oThermostatEP.update()
    else:
        context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")

@When(u'Set current mode as {strType} with Target Temperature as {inttemp} on the stat')
def SetHolidayTemp(context, strType, inttemp):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Activate ' + strType + ' ' + inttemp + ' mode on the thermostat')
    dutils.wakeUpTheDevice(context, myNodeId, ep)
    time.sleep(2)
    if str(strType).upper() == 'HOLIDAY':
        scheduleSetpoint = float(rFM.ReusableFunctionModule.convertHexTemp(rFM.ReusableFunctionModule,
                                                                           context.oThermostatEP.frostProtectionSetpoint,
                                                                           False))
        print(float(scheduleSetpoint))
        print(float(inttemp))
        diffTemp = float(scheduleSetpoint) - (float(inttemp))
        print(diffTemp)

        if diffTemp > 0:
            time.sleep(2)
            dutils.rotateDial(myNodeId, ep, "ANTICLOCKWISE", abs(diffTemp))
        elif diffTemp < 0:
            time.sleep(2)
            dutils.rotateDial(myNodeId, ep, "CLOCKWISE", abs(diffTemp))

        dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
        time.sleep(2)
        context.reporter.ReportEvent("Event Log", "Temperature is Set", "Done")

        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
        time.sleep(5)
        context.reporter.ReportEvent("Event Log", "Start Date and End Date is displayed", "Done")

        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
        time.sleep(5)
        context.reporter.ReportEvent("Event Log", "Start Date and End Date with temp is confirmed", "Done")

    else:
        context.reporter.ReportEvent("Event Log", "Holiday is not found", "FAIL")

@Then(u'the {strType} {strMode} set on the {strDeviceType} {strLang} is set to {strState} and validated')
def SetHoliday(context, strType, strMode, strLang, strState, strDeviceType):
    global oImgMenu, ep, myEp, myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Activate ' + strType + ' ' + strMode + ' ' + ' to set' + strState + ' mode on the thermostat')
    context.oThermostatEP = context.oThermostatClass.heatEP
    if "devices" not in strDeviceType.split(" ")[0]:
        macId = dutils.getDeviceMACWithModel(strDeviceType.split(" ")[0], True)
        myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType.split(" ")[0], macId)
        context.nodeId = myNodeId
        myEp = dutils.getDeviceEPWithModel(strDeviceType.split(" ")[0], True)
        context.myEPList = myEp
        ep = context.myEPList[0]
        if str(strType).upper() == 'HOLIDAY':
            # mySetpoint = 1.0
            # holidayStartOffset = 60
            # intSetTempDuration = 604800
            longPollInt, checkInInt = AT.setCompletFastPoll(myNodeId, ep)
            time.sleep(3)
            oLang = oUtils.getLanguage(strLang)
            strMode = oUtils.getModeText(strMode, strType, oLang)
            respSate = AT.setFastPoll()
            if respSate:
                context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
                dutils.wakeUpTheDevice(context, myNodeId, ep)
                oImgWake, imgWakeName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
                time.sleep(1)
                oImgMenu, imgMenuName = oUtils.captureOriginal(context)
                context.reporter.ReportEvent("Event Log", "Menu by pressing Menu button", "Done")
                dutils.rotateDial(myNodeId, ep, "Clockwise", 2)
                context.reporter.ReportEvent("Event Log", "Started setting fast poll", "Done")
                time.sleep(1)
                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done")
                oImgHolMenu, imgHolMenuName = oUtils.captureOriginal(context)
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(2)
                context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done",
                                             ocrImagePath=imgWakeName)

                if str(strState).upper() == 'CANCEL':
                    dutils.rotateDial(myNodeId, ep, "Clockwise", 0)
                    oImgHolidayMenu, imgHolidayMenuName = oUtils.captureOriginal(context)
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(5)
                    context.reporter.ReportEvent("Event Log", "Holiday Mode is pressed", "Done")
                    context.oThermostatEP.update()
                    strCancel = str(context.oThermostatEP.holidayModeEnabled)
                    print(strCancel)
                    if strCancel == '00':
                        context.reporter.ReportEvent("Event Log", "Holiday Mode is cancelled successfully", "PASS")
                    else:
                        context.reporter.ReportEvent("Event Log", "Holiday Mode is not cancelled", "FAIL")
                elif str(strState).upper() == 'EDIT':
                    dutils.rotateDial(myNodeId, ep, "Clockwise", 1)
                    oImgHolidayMenu, imgHolidayMenuName = oUtils.captureOriginal(context)
                    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                    time.sleep(5)
                    context.reporter.ReportEvent("Event Log", "Holiday Mode is pressed", "Done")
                    context.oThermostatEP.update()
                    strCancel = str(context.oThermostatEP.holidayModeEnabled)
                    print(strCancel)
                    if strCancel == '01':
                        context.reporter.ReportEvent("Event Log", "Holiday Mode is edited successfully", "PASS")
                    else:
                        context.reporter.ReportEvent("Event Log", "Holiday Mode is not edited", "FAIL")

                Mode = oUtils.getText(oImgWake, context)
                oUtils.printModesHome(Mode, context, oLang)

                context.reporter.ReportEvent("Event Log", "Menu Button is pressed", "Done",
                                             ocrImagePath=imgMenuName)

                oUtils.validateMainMenu(oImgMenu, imgMenuName, oLang, context)

                context.reporter.ReportEvent("Event Log", "Dial is rotated clockwise to Holiday mode", "Done",
                                             ocrImagePath=imgHolMenuName)

                oUtils.validateMainMenu(oImgHolMenu, imgHolMenuName, oLang, context)
                oUtils.validateHolidayCancelOptions(oImgHolidayMenu, imgHolidayMenuName, oLang, context)
    else:
        context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")

@step(u'validate if the screen remains in {strType} {strMode} on the {strDeviceType} in {strLang} after {inttime} seconds')
def ValidateNoChangeinHoliday(context, strType, strMode, inttime, strDeviceType, strLang):
    global oImgMenu, ep, myEp, myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Validate ' + strType + ' ' + strMode + ' ' + ' is on the same screen on the thermostat')
    context.oThermostatEP = context.oThermostatClass.heatEP
    if "devices" not in strDeviceType.split(" ")[0]:
        macId = dutils.getDeviceMACWithModel(strDeviceType.split(" ")[0], True)
        myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType.split(" ")[0], macId)
        context.nodeId = myNodeId
        myEp = dutils.getDeviceEPWithModel(strDeviceType.split(" ")[0], True)
        context.myEPList = myEp
        ep = context.myEPList[0]
        if str(strType).upper() == 'HOLIDAY' :
            time.sleep(int(inttime))
            context.reporter.ReportEvent("Event Log", "Device is awake after "+str(inttime), "Done")
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            oImgWake, imgWakeName = oUtils.captureOriginal(context)
            oLang = oUtils.getLanguage(strLang)
            strMode = oUtils.getModeText(strMode, strType, oLang)
            oUtils.validateHolidayMenu(oImgWake, imgWakeName, oLang, context, "FROM", "CONFIRM")
        else:
            context.reporter.ReportEvent("Event Log", "Holiday Mode is not on the same screen", "FAIL")
    else:
        context.reporter.ReportEvent("Event Log", "Device not found", "FAIL")

@step(u'the {strDeviceType} {strLang} is in the {strMenu} Screen')
def ValidateMainMenuScreen(context, strMenu, strDeviceType, strLang):
    global oImgWake, ep, myEp, myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Device ' + strDeviceType + ' ' + strMenu + 'Screen Flows')
    context.oThermostatEP = context.oThermostatClass.heatEP
    if "devices" not in strDeviceType.split(" ")[0]:
        macId = dutils.getDeviceMACWithModel(strDeviceType.split(" ")[0], True)
        myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType.split(" ")[0], macId)
        context.nodeId = myNodeId
        myEp = dutils.getDeviceEPWithModel(strDeviceType.split(" ")[0], True)
        context.myEPList = myEp
        ep = context.myEPList[0]
        AT.setCompletFastPoll(myNodeId, ep)
        time.sleep(3)
        oLang = oUtils.getLanguage(strLang)
        respState = AT.setFastPoll()
        if respState:
            context.reporter.ReportEvent("Event Log", "Fast poll set successfully", "Done")
            dutils.wakeUpTheDevice(context, myNodeId, ep)
            oImgWake, imgWakeName = oUtils.captureOriginal(context)
            if oLang.HomeScreen.Target_Text in oUtils.getText(oImgWake, context):
                context.reporter.ReportEvent("Event Log", "Main menu is found", "PASS")
                exit()
        else:
            context.reporter.ReportEvent("Event Log", "Setting fast poll is failed", "FAIL")

@step(u'the {strMainMenu} options are validated in {strLang}')
def ValidateMainMenuOptionScreen(context, strMainMenu, strLang):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Validation of ' + strMainMenu + 'options on the thermostat')
    context.oThermostatEP = context.oThermostatClass.heatEP
    dutils.wakeUpTheDevice(context, myNodeId, ep)
    oImgWake, imgWakeName = oUtils.captureOriginal(context)
    oLang = oUtils.getLanguage(strLang)
    dutils.pressDeviceButton(myNodeId, ep, "Menu", "Press")
    time.sleep(1)
    oUtils.validateMainMenu(oImgWake, imgWakeName, oLang, context)

@step(u'validate if the {strButtonType} Button is enabled on {strDeviceType}')
def ValidateMainMenuOptionScreen(context, strButtonType, strDeviceType):
    global ep, myEp, myNodeId
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Validation of ' + strButtonType + 'is enabled on the thermostat')

    if "devices" not in strDeviceType.split(" ")[0]:
        macId = dutils.getDeviceMACWithModel(strDeviceType.split(" ")[0], True)
        myNodeId = dutils.getDeviceNodeWithMAC(strDeviceType.split(" ")[0], macId)
        context.nodeId = myNodeId
        myEp = dutils.getDeviceEPWithModel(strDeviceType.split(" ")[0], True)
        context.myEPList = myEp
        ep = context.myEPList[0]
        dutils.wakeUpTheDevice(context, myNodeId, ep)
        oImgWake, imgWakeName = oUtils.captureOriginal(context)
        BackButton, MenuButton, TickButton = dutils.getButtonType(oImgWake, context)

        #Validation for Tick Button
        if str(strButtonType).upper() == 'TICK':
            _r, _g, _b = context.get_weighted_color_average(TickButton)
            if int(_g) > int(_r) and int(_g) > int(_b):
                context.reporter.ReportEvent("Button Validation", str(strButtonType).upper()+" Button is displayed ",
                                             "PASS")
            else:
                context.reporter.ReportEvent("Button Validation", str(strButtonType).upper() + " Button is not displayed ",
                                             "FAIL")

        #Validation for Back Button
        if str(strButtonType).upper() == 'BACK':
            _r, _g, _b = context.get_weighted_color_average(BackButton)
            if int(_r) > int(_g) and int(_r) > int(_b):
                context.reporter.ReportEvent("Button Validation", str(strButtonType).upper()+" Button is displayed ",
                                             "PASS")
            else:
                context.reporter.ReportEvent("Button Validation", str(strButtonType).upper() + " Button is not displayed ",
                                             "FAIL")

        # Validation for Menu Button
        if str(strButtonType).upper() == 'MENU':
            _r, _g, _b = context.get_weighted_color_average(MenuButton)
            if int(_g) == int(_r) and int(_g) == int(_b):
                context.reporter.ReportEvent("Button Validation", str(strButtonType).upper() + " Button is displayed ",
                                             "PASS")
            else:
                context.reporter.ReportEvent("Button Validation", str(strButtonType).upper() + " Button is not displayed ",
                                             "FAIL")
    else:
        context.reporter.ReportEvent("Event Log", "Device not found", "FAIL")
