"""
Created on 25 May 2015

@author: ranganathan.veluswamy
"""
from datetime import datetime
from datetime import timedelta
import json
import time
import math
import traceback
import FF_ScheduleUtils as oSchdUtil
import random
import CC_thermostatModule as st
import CC_platformAPI as PAPI
import DD_Page_AndroidApp as paygeAndroid
import DD_Page_WebApp as paygeWeb
import DD_Page_iOSApp as paygeiOS
import FF_ScheduleUtils as oSchdUt
import FF_alertmeApi as ALAPI
import FF_utils as utils
import FF_Platform_Utils as pUtils
import FF_zbOTA as ota
import FF_zbOTA_ForDevice as Deviceota
import FF_zigbeeToolsConfig as config
import FF_threadedSerial as AT
import FF_device_utils as dutils
import FF_Email as emails
import os
#import speech_recognition as sr
from subprocess import call


class ReusableFunctionModule:
    def __init__(self):
        self.getWaterModes = {'MANUAL': 'Always ON',
                              'OFF': 'Always OFF',
                              'Always ON': 'Always ON',
                              'ON': 'Always ON',
                              'Always OFF': 'Always OFF',
                              'BOOST': 'BOOST',
                              'BOOST_CANCEL': 'BOOST_CANCEL',
                              'AUTO': 'AUTO',
                              'OVERRIDE': 'OVERRIDE',
                              None: 'None'
                              }

        self.getPlugModes = {'MANUAL': 'MANUAL',
                             'Always ON': 'MANUAL',
                             'ON': 'MANUAL',
                             'AUTO': 'AUTO',
                             'SCHEDULE': 'AUTO',
                             None: 'None'
                             }

        self.beekeeperRequests = {'getProducts': ['getProductsBEE', 'getNodesAPI'],
                                  'getDevices': ['getNodesAPI', 'getDevicesBEE'],
                                  # 'deleteDevice'   : ['deleteDeviceBEE', 'getDevicesBEE', 'getNodesAPI']
                                  # 'heatingHistory' : ['heatingHistoryBEE', TBC for API],
                                  # 'login'          : ['beekeeperLogin' , 'apiLogin', 'getUsersAPI'],
                                  # 'adminLogin'     : ['beeAdminLogin' , 'apiLogin', 'getUsersAPI'],
                                  # 'restPassword'   : ['resetPasswordBEE],
                                  # 'sendPasswordReset : ['sendPasswordResetBEE'],
                                  'getHolidayMode': ['getHolidayModeBEE', 'getHolidayModeAPI'],
                                  'startHolidayMode': ['startHolidayModeBEE', 'getHolidayModeBEE', 'getHolidayModeAPI'],
                                  'endHolidayMode': ['endHolidayModeBEE', 'getHolidayModeBEE', 'getHolidayModeAPI'],
                                  'getContacts': ['getContactsBEE', 'getContactsAPI'],
                                  'updateContacts': ['updateContactsBEE', 'getContactsBEE', 'getContactsAPI'],
                                  'addContacts': ['addContactsBEE', 'getContactsBEE', 'getContactsAPI'],
                                  'deleteContacts': ['deleteContactsBEE', 'getContactsBEE', 'getContactsAPI'],
                                  'updateNode': ['updateNodeBEE']  # , 'getProductsBEE', 'getNodesAPI'],
                                  # 'deleteZone'     : ['deleteZoneBEE', 'getProductsBEE', 'getNodesAPI']
                                  }

    # Beekeeper Functions
    def setBeeRequest(self, context, strRequest, strServerName, oAttribute='', oTargetValue='', oType='',
                      strContact=''):
        if strRequest in self.beekeeperRequests:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Sending ' + \
                                                               strRequest + '() Request to Honeycomb via Beekeeper')
            oRequestList = self.beekeeperRequests[strRequest]
            if oTargetValue == '':
                context.oThermostatEP.makeRequest(oRequestList, strServerName, context, strRequest, strContact)
            else:
                strContact = [oAttribute, oTargetValue, oType]
                context.oThermostatEP.makeRequest(oRequestList, strServerName, context, strRequest, strContact)

        else:
            # Need to work out for platAPI error.
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Fetching data from API and Beekeeper')
            platAPI = PAPI.platformAPIClass
            oThermostatEndpoint = PAPI.thermostatEndpoint(platAPI, strServerName, context.oThermostatEP)
            context.oTEP = oThermostatEndpoint
            context.oTEP.report_fail('Beekeeper Caller : No such request exists, please check the Request name')

    def setAdminLoginRequest(self, context, strLoginType):

        if strLoginType == 'ADMIN':
            context.oThermostatEP.beeAdminLogin(self, context)

    def ValidateBeeResponse(self, context, strRequest, strServerName):
        if strRequest == 'ValidateUserDetails':
            context.oThermostatEP.validateUserDetails(self, context)

        elif strRequest in self.beekeeperRequests:
            print('\nValidating Beekeeper Response for ' + strRequest, 'request')
            oRequestList = self.beekeeperRequests[strRequest]
            context.oThermostatEP.validateBeekeeper(strRequest, strServerName, context)

        else:
            print('Request name NOT found in Beekeeper requests list - please check the feature file')

    def changeDeviceName(self, reporter, oLightEP, oDeviceCurrentName, oDeviceNewName):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Set Device Name : ' + str(oDeviceNewName))
        reporter.ReportEvent('Test Validation',
                             'Setting up device name to <B>' + oDeviceNewName + '</B>', 'Done')
        oLightEP.setDeviceName(oDeviceCurrentName, oDeviceNewName)

    # Sets the Target temperature
    def setTargetTemperature(self, reporter, boolAutoMode, oThermostatEP, strSetTemperature):
        strBeforeTemperature = self.convertHexTemp(oThermostatEP.occupiedHeatingSetpoint, False)
        strBeforeMode = oThermostatEP.mode

        # Set Expected mode based on the expected logic
        if strBeforeMode == 'OFF' and int(strSetTemperature) > 1.0:
            strExpectedMode = 'MANUAL'
        elif strBeforeMode == 'AUTO':
            strExpectedMode = 'OVERRIDE'
        else:
            strExpectedMode = strBeforeMode

        reporter.HTML_TC_BusFlowKeyword_Initialize('Set Target Temperature : ' + str(strSetTemperature) + 'C')
        # Set the Target temperature
        if boolAutoMode:
            strReportMode = 'Automatically'
            try:
                oThermostatEP.setSetpoint(strSetTemperature)
            except:
                oThermostatEP.setSetpoint(strExpectedMode, strSetTemperature)
            if int(strSetTemperature) == 7: strSetTemperature = 1.0
        else:
            strReportMode = 'Manually'
            input(
                '\n*********************************************************************************************************************************\n' + \
                '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                '*********************************************************************************************************************************\n'
                'On the Thermostat Manually set up Target Temperature to ' + strSetTemperature + 'C\n' + \
                'If Action is Completed then please type \'Y\' and press Enter key>>>')
            strReportLog = self.getLog(oThermostatEP, 'Test', strExpectedMode, strSetTemperature)
            print('\nPlease validate if the below attribute values are displayed on the Thermostat Screen:')
            print(self.conertToPrintLog(strReportLog[0]))

        reporter.ReportEvent('Test Validation',
                             strReportMode + 'Setting up Target Temperature to <B>' + str(strSetTemperature) + \
                             ' <B>from </B>' + str(
                                 strBeforeTemperature) + 'C </B>with current system mode as <B>' + oThermostatEP.mode,
                             'Done')

        if not reporter.ActionStatus: return False

        # Validate the change and Log into the report
        if boolAutoMode and 'PLATFORM' not in reporter.APIType.upper():
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')
        else:

            print("Vlidating Main Client")
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Main Client', strExpectedMode, strSetTemperature)

            strMainClientTemp = oThermostatEP.client
            if 'Y' in utils.getAttribute('common', 'secondClientValidateFlag'):
                print("Vlidating Second Client")
                oThermostatEP.client = utils.getAttribute('common', 'secondClient')
                try:
                    self.validateAndUpdateLog(reporter, oThermostatEP, 'Secondary Client', strExpectedMode,
                                              strSetTemperature)
                except:
                    print('Error in Validating second client')
                oThermostatEP.client = strMainClientTemp
        self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strExpectedMode, strSetTemperature)

    # Sets the system mode for the given temperature if required
    def setSysMode(self, reporter, boolAutoMode, oThermostatEP, strMode, strSetTemperature=None,
                   strSetDurationInHours=1):
        print(strSetTemperature, 'strSetTemperature', '\n')
        if 'MANUAL' in strMode.upper():
            if oThermostatEP.type == 'PLUG':
                strExpectedTemperature = None
            else:
                strExpectedTemperature = 20.0
                if reporter.APIType == 'PLATFORM':
                    if not oThermostatEP.Web_ManualModeTargTemp is None: strExpectedTemperature = oThermostatEP.Web_ManualModeTargTemp
        # Modification - change the below condition for OFF
        elif "OFF" in strMode.upper():
            strExpectedTemperature = 1.0
        elif strMode.upper() == 'AUTO':
            if oThermostatEP.type == 'PLUG':
                strExpectedTemperature = None
            else:
                fltTemp = oSchdUt.getCurrentTempFromSchedule(oThermostatEP.getSchedule())
                strExpectedTemperature = fltTemp[0]
        else:
            strExpectedTemperature = strSetTemperature

        strModeOnReport = strMode
        if oThermostatEP.type == 'WATER':
            if strMode.upper().find('ON') >= 0:
                strMode = 'MANUAL'
            elif strMode.upper().find('OFF') >= 0:
                strMode = 'OFF'
            strExpectedTemperature = None

        reporter.HTML_TC_BusFlowKeyword_Initialize('Set ' + strModeOnReport + ' Mode')
        strWithTargTemp = ''
        if not strExpectedTemperature is None: strWithTargTemp = 'with Target Temperature as ' + str(
            strExpectedTemperature) + 'C'

        # Set the System Mode
        if boolAutoMode:
            strReportMode = 'Automatically'
            print(strMode, strSetTemperature, strSetDurationInHours, '\n')
            oThermostatEP.setMode(strMode, strSetTemperature, strSetDurationInHours)
        else:
            strReportMode = 'Manually'
            input(
                '\n*********************************************************************************************************************************\n' + \
                '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                '*********************************************************************************************************************************\n'
                'On the Thermostat Manually set up ' + strModeOnReport + ' Mode ' + strWithTargTemp + '\n' + \
                'If Action is Completed then please type \'Y\' and press Enter key>>>')
            strReportLog = self.getLog(oThermostatEP, 'Test', strModeOnReport, strExpectedTemperature)
            print('\nPlease validate if the below attribute values are displayed on the Thermostat Screen:')
            print(self.conertToPrintLog(strReportLog[0]))

        reporter.ReportEvent('Test Validation',
                             strReportMode + ' Setting up <B>' + strModeOnReport + '</B> Mode ' + strWithTargTemp,
                             'Done')

        # Check if action status is True. If False then skip Scenario
        if not reporter.ActionStatus: return False

        # Validate the change and Log into the report
        if boolAutoMode and reporter.APIType != 'PLATFORM':
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')
        else:
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Main Client', strModeOnReport, strExpectedTemperature)
            strMainClientTemp = oThermostatEP.client
            if 'Y' in utils.getAttribute('common', 'secondClientValidateFlag'):
                oThermostatEP.client = utils.getAttribute('common', 'secondClient')
                try:
                    self.validateAndUpdateLog(reporter, oThermostatEP, 'Secondary Client', strModeOnReport,
                                              strExpectedTemperature)
                except:
                    print('Error in Validating second client')
                oThermostatEP.client = strMainClientTemp

        self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strModeOnReport, strExpectedTemperature)

    # Sets the system mode for the given temperature if required
    def setSysState(self, reporter, boolAutoMode, oThermostatEP, strExpectedState, strExpectedMode,
                    strSetTemperature=None, strSetDurationInHours=1):

        strStateOnReport = strExpectedState
        if oThermostatEP.type == 'PLUG':
            if strExpectedState.upper().find('ON') >= 0:
                strExpectedState = 'ON'
            elif strExpectedState.upper().find('OFF') >= 0:
                strExpectedState = 'OFF'
            strExpectedTemperature = None

        reporter.HTML_TC_BusFlowKeyword_Initialize('Setting Plug to ' + strStateOnReport + ' state')

        strWithTargTemp = ''
        if not strExpectedTemperature is None: strWithTargTemp = 'with Target Temperature as ' + str(
            strExpectedTemperature) + 'C'

        # Set the System State
        if boolAutoMode:
            strReportMode = 'Automatically'
            print(strExpectedState, strSetTemperature, strSetDurationInHours, '\n')
            oThermostatEP.setState(strExpectedState, strSetTemperature, strSetDurationInHours)
        else:
            strReportMode = 'Manually'
            input(
                '\n*********************************************************************************************************************************\n' + \
                '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                '*********************************************************************************************************************************\n'
                'On the Plug Manually set up ' + strStateOnReport + ' state \n' + \
                'If Action is Completed then please type \'Y\' and press Enter key>>>')
            strReportLog = self.getLog(oThermostatEP, 'Test', strStateOnReport, strExpectedTemperature)
            print('\nPlease validate if the below attribute values are displayed on the Thermostat Screen:')
            print(self.conertToPrintLog(strReportLog[0]))

        reporter.ReportEvent('Test Validation',
                             strReportMode + ' Setting up the plug state to <B>' + strStateOnReport + '</B> ' + strWithTargTemp,
                             'Done')

        # Check if action status is True. If False then skip Scenario
        if not reporter.ActionStatus: return False

        # Validate the change and Log into the report
        if boolAutoMode and reporter.APIType != 'PLATFORM':
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')
        else:
            self.validateAndUpdateStateLog(reporter, oThermostatEP, 'Main Client', strExpectedState, strExpectedMode,
                                           strExpectedTemperature)

            strMainClientTemp = oThermostatEP.client
            if 'Y' in utils.getAttribute('common', 'secondClientValidateFlag'):
                oThermostatEP.client = utils.getAttribute('common', 'secondClient')
                try:
                    self.validateAndUpdateStateLog(reporter, oThermostatEP, 'Secondary Client', strExpectedState,
                                                   strExpectedMode, strExpectedTemperature)
                except:
                    print('Error in Validating second client')
                oThermostatEP.client = strMainClientTemp

        self.validateAndUpdateStateLog(reporter, oThermostatEP, 'Test', strExpectedState, strExpectedMode,
                                       strExpectedTemperature)

    def navigateToSensorScreen(self, reporter, oSensorEP, strSensorType):

        reporter.HTML_TC_BusFlowKeyword_Initialize('Navigate to sensor product page')
        oSensorEP.navigateToSensorScreen(strSensorType)

        strLog = 'User navigated to' + str(strSensorType) + 'product page successfully'
        reporter.ReportEvent("Test Validation", strLog, "PASS")

        if not reporter.ActionStatus:
            return False

    def validateSensorState(self, reporter, oSensorEP, strSensorType):

        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate the current STATE of the motion sensor')
        oSensorEP.getAttributesFromClient()
        strDeviceStateFromHoneyComb = oSensorEP.CurrentDeviceStateFromHoneyComb
        if strDeviceStateFromHoneyComb:
            strDeviceStateFromHoneyComb = 'ON'
        elif not strDeviceStateFromHoneyComb:
            strDeviceStateFromHoneyComb = 'OFF'
        strCurrentDeviceStateFromApp = oSensorEP.CurrentDeviceStateFromApp

        if strCurrentDeviceStateFromApp == 'MOTION' or strCurrentDeviceStateFromApp == 'ON':
            print("App is displaying as Motion detected")
            if strCurrentDeviceStateFromApp == strDeviceStateFromHoneyComb:
                strLog = 'Sensor state' + '$$' + 'Currently DETECTING motion'
                reporter.ReportEvent("Test Validation", strLog, "PASS")
            else:
                reporter.ReportEvent("Test Validation",
                                     "The Motion sensor state is not matching with response from HoneyComb", "FAIL")

        elif strCurrentDeviceStateFromApp == 'NO MOTION' or strCurrentDeviceStateFromApp == 'OFF':
            print("App is displaying as Motion Not detected")
            if strCurrentDeviceStateFromApp == strDeviceStateFromHoneyComb:
                strLog = 'Sensor state' + '$$' + 'Currently NOT DETECTING motion'
                reporter.ReportEvent("Test Validation", strLog, "PASS")
            else:
                reporter.ReportEvent("Test Validation",
                                     "The Motion sensor state is not matching with response from HoneyComb", "FAIL")

        else:
            reporter.ReportEvent("Test Validation", "TEXT DISPLAYED in the motion sensor state in the app IS WRONG",
                                 "FAIL")

        LastDetected = oSensorEP.LastDetected
        strLog = 'Last Detected' + '$$' + str(LastDetected)
        reporter.ReportEvent("Test Validation", strLog, "PASS")

        NoOfTimesSensorTriggeredToday = oSensorEP.NoOfTimesSensorTriggeredToday
        strLog = 'Number of Detections' + '$$' + str(NoOfTimesSensorTriggeredToday)
        reporter.ReportEvent("Test Validation", strLog, "PASS")

        if not oSensorEP.NoOfTimesSensorTriggeredToday == 0:
            busiestPeriod = oSensorEP.BusiestPeriod
            strLog = 'Busiest Period today' + '$$' + str(busiestPeriod)
            reporter.ReportEvent("Test Validation", strLog, "PASS")

        # Event logs validation to be done here
        EventLogsFromHoneyComb = oSensorEP.eventLogs
        EventLogsFromApp = oSensorEP.eventLogsFromApp

        if not reporter.ActionStatus:
            return False

    def setLightSysMode(self, reporter, oLightEP, oDeviceName, oDeviceID, strMode, propertyName, propertyValue):
        # mode, currentDeviceState, activeLightBrightness = getLightAttributes('FWBULB')
        # if 'MANUAL ON' in strMode.upper() :
        # strExpectedBrightness = strSetBrightness

        strReportMode = 'Automatically'
        reporter.HTML_TC_BusFlowKeyword_Initialize('Set ' + strMode + ' Mode')

        reporter.ReportEvent('Test Validation',
                             strReportMode + ' setting up <B>' + strMode + '</B> Mode with ' + propertyName + ' as <B>' + str(
                                 propertyValue) + '</B>', 'Done')

        if "BRIGHTNESS" in propertyName.upper():
            propertyValue = propertyValue.replace("%", "")

        oLightEP.setLightMode(oDeviceName, oDeviceID, strMode, propertyName, propertyValue)

        if not reporter.ActionStatus:
            return False

    # Sets the system mode for the given temperature if required
    def setHoldayMode(self, reporter, boolAutoMode, oThermostatEP, strMode, strSetTemperature=None,
                      strSetDurationInHours=1, strHoldayStart="", strHoldayEnd=""):
        strExpectedTemperature = strSetTemperature
        strModeOnReport = strMode
        reporter.HTML_TC_BusFlowKeyword_Initialize('Set ' + strModeOnReport + ' Mode')
        strWithTargTemp = ''
        if not strExpectedTemperature is None: strWithTargTemp = 'with Target Temperature as ' + str(
            strExpectedTemperature) + 'C'

        # Set the System Mode
        if boolAutoMode:
            strReportMode = 'Automatically'
            print(strMode, strSetTemperature, strSetDurationInHours, strHoldayStart, strHoldayEnd, '\n')
            oThermostatEP.setHoliday(strHoldayStart, strHoldayEnd, strSetTemperature)

        else:
            strReportMode = 'Manually'
            input(
                '\n*********************************************************************************************************************************\n' + \
                '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                '*********************************************************************************************************************************\n'
                'On the Thermostat Manually set up ' + strModeOnReport + ' Mode ' + strWithTargTemp + '\n' + \
                'If Action is Completed then please type \'Y\' and press Enter key>>>')
            strReportLog = self.getLog(oThermostatEP, 'Test', strModeOnReport, strExpectedTemperature, strHoldayStart,
                                       strHoldayEnd)
            print('\nPlease validate if the below attribute values are displayed on the Thermostat Screen:')
            print(self.conertToPrintLog(strReportLog[0]))

        reporter.ReportEvent('Test Validation',
                             strReportMode + ' Setting up <B>' + strModeOnReport + '</B> Mode ' + strWithTargTemp,
                             'Done')

        # Check if action status is True. If False then skip Scenario
        if not reporter.ActionStatus: return False

        # Validate the change and Log into the report
        if boolAutoMode and reporter.APIType != 'PLATFORM':
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')
        else:
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Main Client', strModeOnReport, strExpectedTemperature,
                                      strHoldayStart, strHoldayEnd)
            strMainClientTemp = oThermostatEP.client
            if 'Y' in utils.getAttribute('common', 'secondClientValidateFlag'):
                oThermostatEP.client = utils.getAttribute('common', 'secondClient')
                try:
                    self.validateAndUpdateLog(reporter, oThermostatEP, 'Secondary Client', strModeOnReport,
                                              strExpectedTemperature, strHoldayStart, strHoldayEnd)
                except:
                    print('Error in Validating second client')
                oThermostatEP.client = strMainClientTemp

        self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strModeOnReport, strExpectedTemperature,
                                  strHoldayStart, strHoldayEnd)

    def setSchedule(self, context, oSchedule, boolStandaloneMode=False, boolViaHub=False, nodeId=""):
        context.oThermostatEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oThermostatEP.getSchedule()
        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting the given Schedule")
        '''
        if strAppVersion == 'V6' and 'WEB111' in context.oThermostatEP.client.upper():
            input('\n*********************************************************************************************************************************\n' + \
                '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                '*********************************************************************************************************************************\n'
                'On the V6 Web App Manually setup the above Schedule' + '\n' +\
                'If Action is Completed then please type \'Y\' and press Enter key>>>')
        else:'''

        if not 'PLATFORM' in context.APIType.upper():
            context.oThermostatEP.setSchedule(oSchedule, boolStandaloneMode)
            if boolStandaloneMode:
                strEP = context.oThermostatEP.type
                context.oThermostatClass = st.thermostatClass(context.reporter.strNodeID)
                if strEP.upper().find('WATER') >= 0:
                    context.oThermostatEP = context.oThermostatClass.waterEP
                else:
                    context.oThermostatEP = context.oThermostatClass.heatEP
        else:
            if boolViaHub:
                oCurrrentSchedules = pUtils.getDeviceSchedule(context.deviceType)
                oCurrrentSchedulesFiltered = pUtils.removeDayFromScheduleAPI(oCurrrentSchedules, oSchedule.keys())
                payload = oSchdUtil.createScheduleForHubAPI(oSchedule, oCurrrentSchedulesFiltered)
                context.oThermostatEP.setScheduleViaAPI(nodeId, payload)
            else:
                context.oThermostatEP.setSchedule(oSchedule)
        # Check if action status is True. If False then skip Scenario

        if not context.reporter.ActionStatus: return False
        try:
            context.oThermostatEP.update()
        except:
            pass

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Schedule is set as below')
        context.reporter.ReportEvent('Test Validation', 'The Schedule that has been set as below', 'DONE', 'CENTER')
        if context.oThermostatEP.type == 'WATER':
            oSchedule = oSchdUt.converWaterStateForSchedule(oSchedule)
        elif context.oThermostatEP.type == 'PLUG':
            oSchedule = oSchdUt.converPlugStateForSchedule(oSchedule)
        oSchdUt.reportSchedule(context.oThermostatEP, context.reporter, oSchedule)

        # Sets the mode to Auto
        if not boolViaHub:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting Schedule Mode")
            context.oThermostatEP.setMode('AUTO')
            time.sleep(10)
            try:
                context.oThermostatEP.update()
            except:
                pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            if context.oThermostatEP.type == 'WATER':
                context.WeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converWaterStateForSchedule(context.oSchedDict)
            elif context.oThermostatEP.type == 'PLUG':
                context.WeeklyScheduleBefore = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converPlugStateForSchedule(context.oSchedDict)
            oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                     context.WeeklyScheduleAfter)

    def addSchedule(self, context, oSchedule, boolStandaloneMode=False, boolViaHub=False, nodeId=""):
        context.oThermostatEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oThermostatEP.getSchedule()
        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Adding the given Schedule")

        context.oThermostatEP.addSchedule(context)
        # Check if action status is True. If False then skip Scenario

        if not context.reporter.ActionStatus: return False
        try:
            context.oThermostatEP.update()
        except:
            pass

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Schedule is set as below')
        context.reporter.ReportEvent('Test Validation', 'The Schedule that has been set as below', 'DONE',
                                     'CENTER')

        if context.oThermostatEP.type == 'PLUG':
            oSchedule = oSchdUt.converPlugStateForSchedule(oSchedule)
        oSchdUt.reportSchedule(context.oThermostatEP, context.reporter, oSchedule)

        # Sets the mode to Auto
        if not boolViaHub:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting Schedule Mode")
            context.oThermostatEP.setMode('AUTO')
            time.sleep(10)
            try:
                context.oThermostatEP.update()
            except:
                pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            if context.oThermostatEP.type == 'WATER':
                context.WeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converWaterStateForSchedule(context.oSchedDict)
            elif context.oThermostatEP.type == 'PLUG':
                context.WeeklyScheduleBefore = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converPlugStateForSchedule(context.oSchedDict)
            oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                     context.WeeklyScheduleAfter)

    def delSchedule(self, context, oSchedule, boolStandaloneMode=False, boolViaHub=False, nodeId=""):
        context.oThermostatEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oThermostatEP.getSchedule()
        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Deleting the given Schedule")

        context.oThermostatEP.delSchedule(context)
        # Check if action status is True. If False then skip Scenario

        if not context.reporter.ActionStatus: return False
        try:
            context.oThermostatEP.update()
        except:
            pass

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Schedule is set as below')
        context.reporter.ReportEvent('Test Validation', 'The Schedule that has been set as below', 'DONE',
                                     'CENTER')
        # if context.oThermostatEP.type == 'WATER':
        # oSchedule = oSchdUt.converWaterStateForSchedule(oSchedule)


        if context.oThermostatEP.type == 'PLUG':
            oSchedule = oSchdUt.converPlugStateForSchedule(oSchedule)
        oSchdUt.reportSchedule(context.oThermostatEP, context.reporter, oSchedule)

        # Sets the mode to Auto
        if not boolViaHub:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting Schedule Mode")
            context.oThermostatEP.setMode('AUTO')
            time.sleep(10)
            try:
                context.oThermostatEP.update()
            except:
                pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            if context.oThermostatEP.type == 'WATER':
                context.WeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converWaterStateForSchedule(context.oSchedDict)
            elif context.oThermostatEP.type == 'PLUG':
                context.WeeklyScheduleBefore = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converPlugStateForSchedule(context.oSchedDict)
            oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                     context.WeeklyScheduleAfter)

    # resetting schedule for a given day
    def resetSchedule(self, context, oSchedule, boolViaHub=False, nodeId=""):
        context.oThermostatEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oThermostatEP.getSchedule()
        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Resetting the given Schedule for the day")
        context.oThermostatEP.resetSchedule(context, oSchedule)

        if not context.reporter.ActionStatus: return False

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Schedule is reset as below')
        context.reporter.ReportEvent('Test Validation', 'The Schedule that has been set as below', 'DONE', 'CENTER')
        if context.oThermostatEP.type == 'WATER':
            oSchedule = oSchdUt.converWaterStateForSchedule(oSchedule)
        elif context.oThermostatEP.type == 'PLUG':
            oSchedule = oSchdUt.converPlugStateForSchedule(oSchedule)

        oSchdUt.reportSchedule(context.oThermostatEP, context.reporter, oSchedule)

        # Sets the mode to Auto
        if not boolViaHub:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting Schedule Mode")
            context.oThermostatEP.setMode('AUTO')
            time.sleep(10)
            try:
                context.oThermostatEP.update()
            except:
                pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            if context.oThermostatEP.type == 'WATER':
                context.WeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converWaterStateForSchedule(context.oSchedDict)
            elif context.oThermostatEP.type == 'PLUG':
                context.WeeklyScheduleBefore = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converPlugStateForSchedule(context.oSchedDict)
            oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                     context.WeeklyScheduleAfter)

    # For copying the schedule
    def copySchedule(self, context, oSchedule, boolViaHub=False, nodeId=""):
        context.oThermostatEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oThermostatEP.getSchedule()
        # Sets the schedule
        context.oThermostatEP.copySchedule(context)

        if not context.reporter.ActionStatus: return False

        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Schedule is copied as below')
        context.reporter.ReportEvent('Test Validation', 'The Schedule that has been set as below', 'DONE', 'CENTER')
        if context.oThermostatEP.type == 'PLUG':
            oSchedule = oSchdUt.converPlugStateForSchedule(oSchedule)

        oSchdUt.reportSchedule(context.oThermostatEP, context.reporter, oSchedule)

        # Sets the mode to Auto
        if not boolViaHub:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting Schedule Mode")
            context.oThermostatEP.setMode('AUTO')
            time.sleep(10)
            try:
                context.oThermostatEP.update()
            except:
                pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            if context.oThermostatEP.type == 'WATER':
                context.WeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converWaterStateForSchedule(context.oSchedDict)
            elif context.oThermostatEP.type == 'PLUG':
                context.WeeklyScheduleBefore = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converPlugStateForSchedule(context.oSchedDict)
            oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                     context.WeeklyScheduleAfter)

    def setLightSchedule(self, context, oDeviceName, oSchedule):
        context.oLightEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oLightEP.getSchedule()
        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting the given Schedule")
        context.oLightEP.setLightSchedule(oDeviceName, oSchedule)
        # Check if action status is True. If False then skip Scenario

        if not context.reporter.ActionStatus: return False
        try:
            context.oLightEP.update()
        except:
            pass

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.ReportEvent('Test Validation', 'Please find below the Schedule that has been set', 'DONE',
                                     'CENTER')
        oSchdUt.reportSchedule(context.oLightEP, context.reporter, oSchedule)

        # Sets the mode to Auto

        context.oLightEP.setLightMode(oDeviceName, 'SCHEDULE')
        time.sleep(10)
        try:
            context.oLightEP.update()
        except:
            pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oLightEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            oSchdUt.validateLightSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                          context.WeeklyScheduleAfter)

    def resetLightSchedule(self, context, oDeviceName, oSchedule):
        context.oLightEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oLightEP.getSchedule()
        # resets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Resetting the given Schedule")
        context.oLightEP.resetLightSchedule(oDeviceName, oSchedule)
        # Check if action status is True. If False then skip Scenario

        if not context.reporter.ActionStatus: return False
        try:
            context.oLightEP.update()
        except:
            pass

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.ReportEvent('Test Validation', 'Please find below the Schedule that has been set', 'DONE',
                                     'CENTER')
        oSchdUt.reportSchedule(context.oLightEP, context.reporter, oSchedule)

        # Sets the mode to Auto

        context.oLightEP.setLightMode(oDeviceName, 'SCHEDULE')
        time.sleep(10)
        try:
            context.oLightEP.update()
        except:
            pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oLightEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            oSchdUt.validateLightSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                          context.WeeklyScheduleAfter)

    def addLightSchedule(self, context, oDeviceName, oSchedule):
        context.oLightEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oLightEP.getSchedule()
        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Adding the given Schedule")

        context.oLightEP.addLightSchedule(context, oDeviceName)
        # Check if action status is True. If False then skip Scenario

        if not context.reporter.ActionStatus: return False
        try:
            context.oLightEP.update()
        except:
            pass

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.ReportEvent('Test Validation', 'Please find below the Schedule that has been set', 'DONE',
                                     'CENTER')
        oSchdUt.reportSchedule(context.oLightEP, context.reporter, oSchedule)

        # Sets the mode to Auto

        context.oLightEP.setLightMode(oDeviceName, 'SCHEDULE')
        time.sleep(10)
        try:
            context.oLightEP.update()
        except:
            pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oLightEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            oSchdUt.validateLightSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                          context.WeeklyScheduleAfter)

    def delLightSchedule(self, context, oDeviceName, oSchedule):
        context.oLightEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oLightEP.getSchedule()
        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Deleting the given Schedule slot")

        context.oLightEP.delLightSchedule(context, oDeviceName)
        # Check if action status is True. If False then skip Scenario

        if not context.reporter.ActionStatus: return False
        try:
            context.oLightEP.update()
        except:
            pass

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.ReportEvent('Test Validation', 'Please find below the Schedule that has been set', 'DONE',
                                     'CENTER')
        oSchdUt.reportSchedule(context.oLightEP, context.reporter, oSchedule)

        # Sets the mode to Auto

        context.oLightEP.setLightMode(oDeviceName, 'SCHEDULE')
        time.sleep(10)
        try:
            context.oLightEP.update()
        except:
            pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oLightEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            oSchdUt.validateLightSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                          context.WeeklyScheduleAfter)

    def copyLightSchedule(self, context, oDeviceName, oSchedule):
        context.oLightEP.update()
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oLightEP.getSchedule()
        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Copying the given Schedule")

        context.oLightEP.copyLightSchedule(context, oDeviceName)
        # Check if action status is True. If False then skip Scenario

        if not context.reporter.ActionStatus: return False
        try:
            context.oLightEP.update()
        except:
            pass

        # print(context.oThermostatEP.getSchedule())
        # Reporting the Schedule that is set
        context.reporter.ReportEvent('Test Validation', 'Please find below the Schedule that has been set', 'DONE',
                                     'CENTER')
        oSchdUt.reportSchedule(context.oLightEP, context.reporter, oSchedule)

        # Sets the mode to Auto

        context.oLightEP.setLightMode(oDeviceName, 'SCHEDULE')
        time.sleep(10)
        try:
            context.oLightEP.update()
        except:
            pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oLightEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            oSchdUt.validateLightSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                          context.WeeklyScheduleAfter)

    def setScheduleViaHub(self, context, oSchedule):
        # Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oThermostatEP.getSchedule()

        # Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting the given Schedule")

        context.oThermostatEP.setSchedule(oSchedule)

        # Check if action status is True. If False then skip Scenario
        if not context.reporter.ActionStatus: return False

        # Reporting the Schedule that is set
        context.reporter.ReportEvent('Test Validation', 'Please find below the Schedule that has been set', 'DONE',
                                     'CENTER')
        if context.oThermostatEP.type == 'WATER':
            oSchedule = oSchdUt.converWaterStateForSchedule(oSchedule)
        elif context.oThermostatEP.type == 'PLUG':
            oSchedule = oSchdUt.converPlugStateForSchedule(oSchedule)
        oSchdUt.reportSchedule(context.oThermostatEP, context.reporter, oSchedule)

        # Sets the mode to Auto
        context.oThermostatEP.setMode('AUTO')
        time.sleep(10)
        try:
            context.oThermostatEP.update()
        except:
            pass

        # Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        # Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            if context.oThermostatEP.type == 'WATER':
                context.WeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converWaterStateForSchedule(context.oSchedDict)
            if context.oThermostatEP.type == 'PLUG':
                context.WeeklyScheduleBefore = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converPlugStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converPlugStateForSchedule(context.oSchedDict)
            oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore,
                                                     context.WeeklyScheduleAfter)

    # Function to get Ep for given deviceTypes
    def get_ZbType_for_deviceType(self, strDeviceType):
        strPath = ""
        for deviceTypeDict in ota.deviceTypes:
            if deviceTypeDict['type'].upper() == strDeviceType.upper():
                strPath = deviceTypeDict['zbType']
                break
        return strPath

    # function to upgrade the firmware version
    def upgrade_or_downgrade_firmware(self, reporter, strUpgradeOrDowngrade, fullPath, nodeId, ep, strDeviceType,
                                      DeviceVersion, reboot=False, plugMacId=None):
        print(strUpgradeOrDowngrade, fullPath, nodeId, ep, '\n')
        strExpectedFWVersion = str(DeviceVersion).replace(".", "")
        reporter.HTML_TC_BusFlowKeyword_Initialize(
            strUpgradeOrDowngrade.upper() + ' Firmware for : ' + strDeviceType.upper())

        _, _, strTHVersion = utils.get_device_version(nodeId, ep)
        reporter.ReportEvent("Test Validation", "The Current version on the device before the upgrade: " + strTHVersion,
                             "DONE")
        print(strExpectedFWVersion, str(strTHVersion)[:4])
        if (strExpectedFWVersion in str(strTHVersion)[:4]) or (str(strTHVersion)[:4] in strExpectedFWVersion):
            reporter.ReportEvent("Test Validation",
                                 "The Device : " + strDeviceType + " is already in version : " + strTHVersion + "<p>Hence skipping the " + strUpgradeOrDowngrade + "  process.",
                                 "PASS")
            return

        # Upgrade or Downgrade Firmware
        reporter.ReportEvent('Test Validation',
                             'The Firmware for ' + strDeviceType.upper() + ' is set to ' + strUpgradeOrDowngrade.upper() + ' to verion ' + str(
                                 DeviceVersion), "Done")
        _, strFileName = os.path.split(fullPath)
        reporter.ReportEvent('Test Validation',
                             'The ' + strUpgradeOrDowngrade.upper() + ' Firmware OTA file download has started. <p> File Name : ' + strFileName,
                             "Done")

        # Check if action status is True. If False then skip Scenario
        if not reporter.ActionStatus: return False

        '''# Open the image file
        if os.path.isfile(fullPath):
            f = open(fullPath, "rb")
        else:
            print("File not found {}".format(fullPath))
            reporter.ReportEvent('Test Validation', 'The Firmware file is not found: '  + fullPath, "Done")
            return False
        print('FW File = {0}\r\n'.format(fullPath))'''

        '''# Read header from the file
        header = ota.myOtaHeader()
        ota.readHeader(header,f)        '''
        # upgrade firmware
        zbType = self.get_ZbType_for_deviceType(strDeviceType)
        print(nodeId, ep, zbType, fullPath)
        imageFile = fullPath
        header = ota.myOtaHeader(fullPath, printData=ota.PRINT_DATA)
        if reboot == True or reboot == None:
            result = Deviceota.firmwareUpgrade(nodeId, ep, zbType, imageFile, header, reboot, plugMacId, printData=True)
        else:
            result = ota.firmwareUpgrade(nodeId, ep, zbType, imageFile, header, printData=True)
        print(result)
        print('All Done. {}'.format(time.strftime("%H:%M:%S", time.gmtime())))
        reporter.ReportEvent('Test Validation',
                             'The Firmware ' + strUpgradeOrDowngrade.upper() + ' OTA file download completed', "Done")

        reporter.ReportEvent("Test Validation", "Firmware Install Started", "DONE")
        if 'SLT3' in strDeviceType.upper():
            intTCStartTime = time.monotonic()
            respState, _, resp = utils.check_device_back_after_restart(nodeId, ep)
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            reporter.ReportEvent("Test Validation", "Time taken for IMGQUERY response : " + strTCDuration, "DONE")
            reporter.ReportEvent("Test Validation", "Current Firmware version reported by IMGQUERY response : " + resp,
                                 "DONE")
            if not respState: reporter.ReportEvent("Test Validation", "IMGQUERY response failed with error" + resp,
                                                   "FAIL")
            intCtr = 0
            '''while intCtr < 20:
                resp = utils.waitForMessage("SED:", 600)
                if resp is not None:
                    if "SED:" in resp and str(nodeId) in resp:
                        reporter.ReportEvent("Test Validation", "The Device announce is received from the stat", "PASS")
                    else:
                        reporter.ReportEvent("Test Validation", "No Device announce from the stat", "FAIL")
                else:
                    reporter.ReportEvent("Test Validation", "No Device announce from the stat", "FAIL")
                intCtr += + 1
            time.sleep(5)
            intCtr = 0
            while intCtr < 5:
                resp = utils.waitForMessage("CHECKIN:{},{}".format(nodeId, ep), 600)
                if resp is not None:
                    if "CHECKIN:" in resp and str(nodeId) in resp:
                        reporter.ReportEvent("Test Validation", "The Device checkin is received from the stat", "PASS")
                    else:
                        reporter.ReportEvent("Test Validation", "No Device checkin from the stat", "FAIL")
                else:
                    reporter.ReportEvent("Test Validation", "No Device checkin from the stat", "FAIL")
                    intCtr += + 1
            time.sleep(5)'''
        else:
            time.sleep(500)
        reporter.ReportEvent("Test Validation", "Firmware Install Completed", "DONE")

    # Validating the Firmware version
    def validate_firmware_version(self, reporter, strUpgradeOrDowngrade, nodeId, ep, strDeviceType, DeviceVersion):
        try:
            reporter.HTML_TC_BusFlowKeyword_Initialize(
                'Validate ' + strUpgradeOrDowngrade.upper() + ' for Device : ' + strDeviceType)
            strExpectedFWVersion = str(DeviceVersion).replace(".", "")

            _, _, strTHVersion = utils.get_device_version(nodeId, ep)

            if (strExpectedFWVersion in str(strTHVersion)[:4]) or (str(strTHVersion)[:4] in strExpectedFWVersion):
                reporter.ReportEvent("Test Validation",
                                     "The Device : " + strDeviceType + " is successfully " + strUpgradeOrDowngrade + " to " + strTHVersion,
                                     "PASS")
            else:
                reporter.ReportEvent("Test Validation",
                                     "The Device : " + strDeviceType + " is <B>NOT</B> " + strUpgradeOrDowngrade + " to " + DeviceVersion + "<br> Current version on the device : " + strTHVersion,
                                     "FAIL")
                exit()
        except:
            reporter.ReportEvent("Test Validation", 'Exception in validate_firmware_version Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')), "FAIL")

    # function to upgrade the firmware version
    def upgrade_or_downgrade_firmwareViaHUB(self, context, reporter, strUpgradeOrDowngrade, strDeviceType,
                                            DeviceVersion, strPlugMac=None, strType=None):
        print(strUpgradeOrDowngrade, strDeviceType, DeviceVersion, '\n')
        if str(strType).upper() == "ROUTER":
            strType = "NANO2"
        reporter.HTML_TC_BusFlowKeyword_Initialize(
            strUpgradeOrDowngrade.upper() + ' Firmware for : ' + strDeviceType.upper())

        strTHVersion = dutils.getFWversion()[strDeviceType]

        reporter.ReportEvent("Test Validation", "The Current version on the device before the upgrade: " + strTHVersion,
                             "DONE")
        # Upgrade or Downgrade Firmware
        reporter.ReportEvent('Test Validation',
                             'The Firmware for ' + strDeviceType.upper() + ' is set to ' + strUpgradeOrDowngrade.upper() + ' to verion ' + str(
                                 DeviceVersion), "Done")

        if strTHVersion != str(DeviceVersion):
            # Check if action status is True. If False then skip Scenario
            if not reporter.ActionStatus: return False
            dutils.upgradeFirware(strDeviceType, DeviceVersion)
            # oThermostatEP.upgradeFirware(strDeviceType, DeviceVersion)
            print('All Done. {}'.format(time.strftime("%H:%M:%S", time.gmtime())))
            reporter.ReportEvent('Test Validation', 'The Firmware ' + strUpgradeOrDowngrade.upper() + ' is Started',
                                 "Done")

            intTCStartTime = time.monotonic()
            time.sleep(300)
            respState, errorMsg = self.wait_for_upgrade_completion(strDeviceType, reporter,
                                                                   strUpgradeOrDowngrade.upper(), strPlugMac, strType)
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            reporter.ReportEvent("Test Validation",
                                 "Time taken for " + strUpgradeOrDowngrade.upper() + " : " + strTCDuration, "DONE")
            if not respState:
                reporter.ReportEvent("Test Validation",
                                     strUpgradeOrDowngrade.upper() + " Failed with error: " + errorMsg, "FAIL")
                time.sleep(300)
                if "CL" in strDeviceType.upper():
                    exit()
            else:
                reporter.ReportEvent("Test Validation", "Firmware Install Completed", "DONE")
            time.sleep(60)
            if "CL" in strDeviceType.upper() or "PIR" in strDeviceType.upper() or "WDS" in strDeviceType.upper(): time.sleep(
                600)

        else:
            print('The test step is skipped - Same Version')
            reporter.ReportEvent('Test Validation', 'The test step is skipped - Same Version', "Done")

    # Wait for upgrade/downgrade
    def wait_for_upgrade_completion(self, DeviceType, reporter, strUpgradeOrDowngrade, strPlugMac=None,
                                    strDeviceType=None, boolChangeRouterState=False, routerModelId=None):
        if "NANO" in DeviceType.upper():
            time.sleep(900)
            return True, ""

        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'), username=utils.getAttribute('common', strAttributeName='superusername'), password=utils.getAttribute('common', strAttributeName='superuserpwd'))
        session = ALAPI.superUserSessionObject()

        hubIDResp = ALAPI.getHubIdV6(session, username=utils.getAttribute('common', strAttributeName='username'))
        hubID = hubIDResp[0]["internalHubState"]["id"]
        strModel = DeviceType

        boolCompleted = False
        boolOneTimeRestartDone = False
        strErrorMsg = ""
        strUpgradeStatus = ""
        fltProgress = 0.0
        intCntr = 1
        intPercentagePrintCntr = 1.0
        flagReboot = False

        # print("CurrentStatus: ", strUpgradeStatus)
        while strUpgradeStatus != "COMPLETE":
            boolNodeExisit = False
            boolUpgradeExist = False
            strLastRevceivedFailTimestamp = ""
            strFailLog = ""
            time.sleep(2)
            hubLogJson = ALAPI.getHubLogsV6(session, hubID)
            for oDict in hubLogJson["internalNodeStates"]:
                if 'model' in oDict:
                    '''strActualModel = oDict["model"]
                elif  'hardwareVersion' in oDict:
                    strActualModel = oDict["hardwareVersion"]
                else:
                    strActualModel = ""
                    break'''

                    if strModel == oDict["model"]:
                        boolNodeExisit = True
                        if "upgradeState" in oDict:
                            boolUpgradeExist = True
                            strUpgradeStatus = oDict["upgradeState"]["status"]
                            # print(strUpgradeStatus)
                            if "FAIL" in strUpgradeStatus.upper():
                                if "lastReceived" in oDict["upgradeState"]:
                                    strLastRevceivedFailTimestamp = oDict["upgradeState"]["lastReceived"]
                                if "log" in oDict["upgradeState"]:
                                    strFailLog = oDict["upgradeState"]["log"]
                                return False, strFailLog + "@ ==>" + strLastRevceivedFailTimestamp
                            if "progress" in oDict["upgradeState"]:
                                fltProgress = float(oDict["upgradeState"]["progress"])
                        else:
                            #print("Upgrade not happenning")
                            break

            if not boolNodeExisit:
                strErrorMsg = "Device Node is missing"
                print(strErrorMsg)
                break

            if not boolUpgradeExist:
                strErrorMsg = "Device " + strUpgradeOrDowngrade.upper() + " NOT triggered"
                print(strErrorMsg)
                break

            if fltProgress >= intPercentagePrintCntr * 10.0:
                print(intCntr, strUpgradeStatus, fltProgress)
                reporter.ReportEvent("Test Validation",
                                     "Current " + strUpgradeOrDowngrade.upper() + " progress: " + str(
                                         fltProgress) + "%", "DONE")
                print("Current " + strUpgradeOrDowngrade.upper() + " progress: " + str(fltProgress) + "%")
                intPercentagePrintCntr = intPercentagePrintCntr + 1.0

            if fltProgress >= 10.0 and flagReboot == False:
                if strPlugMac is not None and strDeviceType is not None:
                    dutils.putZigbeeDevicesJson(dutils.getNodes(False))
                    try:
                        AT.stopThreads()
                        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                    except:
                        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                    deviceType = dutils.getModelIdWithMAC(strPlugMac)
                    NodeId = dutils.getDeviceNodeWithMAC(deviceType, strPlugMac)
                    utils.setSPOnOff(myNodeId=NodeId, strOnOff='OFF', boolZigbee=True)
                    reporter.ReportEvent("Test Validation", strDeviceType + " is turned OFF", "DONE")
                    time.sleep(300)
                    global oDevicePresenceJson
                    oDevicePresenceJson = {}
                    deviceType = strDeviceType
                    oDevicePresenceJson[deviceType] = {}
                    oDevicePresenceJson[deviceType]["presence"] = False
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = ""
                    while True:
                        if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                            time.sleep(60)
                            reporter.ReportEvent("Test Validation",
                                                 "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                     deviceType).upper() + "</B>", "Done")
                        else:
                            oDevicePresenceJson[deviceType]["presence"] = True
                            reporter.ReportEvent("Test Validation",
                                                 "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                     deviceType).upper() + "</B>", "Done")
                            break
                    utils.setSPOnOff(myNodeId=NodeId, strOnOff='ON', boolZigbee=True)
                    reporter.ReportEvent("Test Validation", strDeviceType + " is turned ON", "DONE")
                    while True:
                        if "ABSENT" in pUtils.getDevicePresence(deviceType).upper():
                            time.sleep(60)
                            reporter.ReportEvent("Test Validation",
                                                 "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                     deviceType).upper() + "</B>", "Done")
                        else:
                            oDevicePresenceJson[deviceType]["presence"] = True
                            reporter.ReportEvent("Test Validation",
                                                 "Device Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                     deviceType).upper() + "</B>", "Done")
                            if deviceType == "NANO2":
                                while True:
                                    if "ABSENT" in pUtils.getDevicePresence("CL01").upper():
                                        time.sleep(60)
                                        reporter.ReportEvent("Test Validation",
                                                             "CL01 Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                                 "CL01").upper() + "</B>", "Done")
                                    else:
                                        reporter.ReportEvent("Test Validation",
                                                             "CL01 Presence at this time is : <B>" + pUtils.getDevicePresence(
                                                                 "CL01").upper() + "</B>", "Done")
                                        break
                            break
                    time.sleep(10)
                    AT.stopThreads()
                    time.sleep(60)
                    flagReboot = True

                if boolChangeRouterState and routerModelId is not None:
                    if 'SLP2' in str(routerModelId).upper():
                        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
                        sessionObj = ALAPI.createCredentials()

            '''if "CL" in DeviceType.upper():
                if fltProgress > 50.0 <80.0:
                    if not boolOneTimeRestartDone:
                        oNodeList = pUtils.getNodeAndDeviceVersionID()
                        hubID = oNodeList["NANO2"]["nodeID"]
                        ALAPI.rebootHubV6(session, hubID)
                        time.sleep(300)
                        boolOneTimeRestartDone = True'''

            intCntr = intCntr + 1
            if intCntr > 7200:
                break

        ALAPI.deleteSessionV6(session)
        if "COMPLETE" in strUpgradeStatus.upper():
            print("Firmware downgrade/upgrade successful.", strUpgradeStatus)
            boolCompleted = True
        else:
            print("Firmware downgrade/upgrade unsuccessful.", strUpgradeStatus)

        return boolCompleted, strErrorMsg

    # function to check if both the versions are same to stop waiting for validation
    def verifyfirmwareVersionsViaHUB(self, oThermostatEP, reporter, strUpgradeOrDowngrade, strDeviceType,
                                     DeviceVersion):
        strTHVersion = dutils.getFWversion()[strDeviceType]
        # Flag to check if both the versions are same to stop waiting for validation
        strFlag = True
        if strTHVersion != str(DeviceVersion):
            strFlag = True
            # Check if action status is True. If False then skip Scenario
            if not reporter.ActionStatus: return False
            dutils.upgradeFirware(strDeviceType, DeviceVersion)
        else:
            strFlag = False
        return strFlag

    # Validating the Firmware version
    def validate_firmware_versionViaHUB(self, oThermostatEP, reporter, strUpgradeOrDowngrade, strDeviceType,
                                        DeviceVersion):
        strTHVersion = ""
        while DeviceVersion not in str(strTHVersion):
            try:
                reporter.HTML_TC_BusFlowKeyword_Initialize(
                    'Validate ' + strUpgradeOrDowngrade.upper() + ' for Device : ' + strDeviceType)
                strExpectedFWVersion = str(DeviceVersion).replace(".", "")
                strTHVersion = dutils.getFWversion()[strDeviceType]
                if DeviceVersion in str(strTHVersion):
                    reporter.ReportEvent("Test Validation",
                                         "The Device : " + strDeviceType + " is successfully " + strUpgradeOrDowngrade + " to " + strTHVersion,
                                         "PASS")
                    break
                else:
                    reporter.ReportEvent("Test Validation",
                                         "The Device : " + strDeviceType + " is <B>NOT</B> " + strUpgradeOrDowngrade + " to " + DeviceVersion + "<br> Current version on the device : " + strTHVersion,
                                         "FAIL")
                    print(
                        "The Device : " + strDeviceType + " is <B>NOT</B> " + strUpgradeOrDowngrade + " to " + DeviceVersion + "<br> Current version on the device : " + strTHVersion)
                    print(strUpgradeOrDowngrade, "FAILED. Test Exited")
                    time.sleep(60)
            except:
                reporter.ReportEvent("Test Validation", 'Exception in validate_firmware_version Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')), "FAIL")
                break

    # Validates the system mode for the given duration and logs the validation in check interval time
    def validateSysmode(self, reporter, boolAutoMode, oThermostatEP, strSysMode, strExpectedTemperature,
                        intCheckDuration=600, intCheckTImeInterval=30, strExpextedHolidayStart="",
                        strExpectedHolidayEnd="", nextEventStartTime=None, nextEventDay='Today'):
        strSysMode = str(strSysMode).split(" ")[0]
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strSysMode + ' Mode')
        if not (oThermostatEP.type == 'WATER' or oThermostatEP.type == 'PLUG'):
            strTarg = 'Target Temperature'
        elif oThermostatEP.type == 'WATER':
            strTarg = 'Hot Water State'
        elif oThermostatEP.type == 'PLUG':
            strTarg = 'Active Plug State'
        reporter.ReportEvent('Test Validation',
                             'Validating <B>' + strSysMode + ' </B>Mode with ' + strTarg + ' as <B>' + str(
                                 strExpectedTemperature) + \
                             '</B> for every <B>' + str(
                                 intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(
                                 round(intCheckDuration / 60, 2)) + ' minute(s)', 'Done')

        # Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration / intCheckTImeInterval)):
            # Log the Validation of current attributes with Expected Test and Model Attribute values
            if boolAutoMode and reporter.APIType != 'PLATFORM': self.validateAndUpdateLog(reporter, oThermostatEP,
                                                                                          'Model')
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strSysMode, strExpectedTemperature,
                                      strExpextedHolidayStart, strExpectedHolidayEnd)

            # Wait for the Check Time interval
            time.sleep(intCheckTImeInterval)
            if intCntr == int(intCheckDuration / intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration % intCheckTImeInterval)
            if not nextEventStartTime is None:
                if not oSchdUt.checkGuardTime(nextEventStartTime, nextEventDay): return

    # Validates the SP system mode for the given duration and logs the validation in check interval time
    def validateSPSysmode(self, context, boolAutoMode, SPNodeID, strSysMode, strExpectedState="OFF", intBrightness=0,
                          intCheckDuration=600, intCheckTImeInterval=30, strExpextedHolidayStart="",
                          strExpectedHolidayEnd="", nextEventStartTime=None, nextEventDay='Today'):

        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strSysMode + ' Mode')
        context.reporter.ReportEvent('Test Validation',
                                     'Validating <B>' + strSysMode + ' </B>Mode with Device State as <B>' + str(
                                         strExpectedState) + \
                                     '</B> for every <B>' + str(
                                         intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(
                                         round(intCheckDuration / 60, 2)) + ' minute(s)', 'Done')

        # Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration / intCheckTImeInterval)):
            # Log the Validation of current attributes with Expected Test and Model Attribute values
            if boolAutoMode and context.reporter.APIType != 'PLATFORM': self.validateAndUpdateLog(context.reporter,
                                                                                                  'Model')
            self.validateAndUpdateSPLog(context.reporter, 'Test', SPNodeID, strSysMode, strExpectedState, intBrightness,
                                        strExpextedHolidayStart, strExpectedHolidayEnd)

            # Wait for the Check Time interval
            time.sleep(intCheckTImeInterval)
            if intCntr == int(intCheckDuration / intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration % intCheckTImeInterval)
            if not nextEventStartTime is None:
                if not oSchdUt.checkGuardTime(nextEventStartTime, nextEventDay): return

    def validateSysmodeWithoutTargTemp(self, reporter, boolAutoMode, oThermostatEP, strSysMode, intCheckDuration=30,
                                       intCheckTImeInterval=10):
        if 'with Target Temperature' in strSysMode:
            strSysMode = strSysMode.split(" ")[0]

        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strSysMode + ' Mode')
        reporter.ReportEvent('Test Validation', 'Validating <B>' + strSysMode + ' </B>Mode for every <B>' + str(
            intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(
            round(intCheckDuration / 60, 2)) + ' minute(s)', 'Done')

        # Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration / intCheckTImeInterval)):
            # Log the Validation of current attributes with Expected Test and Model Attribute values
            if boolAutoMode and 'PLATFORM' not in reporter.APIType.upper():
                self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strSysMode)

            # Wait for the Check Time interval
            time.sleep(intCheckTImeInterval)
            if intCntr == int(intCheckDuration / intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration % intCheckTImeInterval)

    def validateSysState(self, reporter, boolAutoMode, oThermostatEP, strExpectedState, strExpectedMode,
                         intCheckDuration=30, intCheckTImeInterval=10):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate Plug for' + strExpectedState + ' State')
        reporter.ReportEvent('Test Validation',
                             'Validating Plug for <B>' + strExpectedState + ' </B>State for every <B>' + str(
                                 intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(
                                 round(intCheckDuration / 60, 2)) + ' minute(s)', 'Done')

        # Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration / intCheckTImeInterval)):
            # Log the Validation of current attributes with Expected Test and Model Attribute values
            if boolAutoMode and 'PLATFORM' not in reporter.APIType.upper():  self.validateAndUpdateLog(reporter,
                                                                                                       oThermostatEP,
                                                                                                       'Model')
            self.validateAndUpdateStateLog(reporter, oThermostatEP, 'Test', strExpectedState, strExpectedMode)

            # Wait for the Check Time interval
            time.sleep(intCheckTImeInterval)
            if intCntr == int(intCheckDuration / intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration % intCheckTImeInterval)

    # Gets the log and validates the same and updates the report
    def validateAndUpdateLog(self, reporter, oThermostatEP, strValidationType, strExpectedMode='AUTO',
                             strExpectedTemperature=1.0, strExpextedHolidayStart="", strExpectedHolidayEnd=""):
        if strValidationType.upper() == "MODEL":
            strLog, strStatus = self.getLog(oThermostatEP, strValidationType)
            reporter.ReportEvent('Model Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "TEST":
            strLog, strStatus = self.getLog(oThermostatEP, strValidationType, strExpectedMode, strExpectedTemperature,
                                            strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "MAIN CLIENT":
            strLog, strStatus = self.getLog(oThermostatEP, strValidationType, strExpectedMode, strExpectedTemperature,
                                            strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Main Client Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "SECONDARY CLIENT":
            strLog, strStatus = self.getLog(oThermostatEP, strValidationType, strExpectedMode, strExpectedTemperature,
                                            strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Secondary Client Validation', strLog, strStatus, 'Center')

    def validateLight(self, reporter, oLightEP, strExpectedMode, strExpectedStatus, strExpectedBrightness=None,
                      strExpectedTone=None):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strExpectedMode + ' mode ')
        if strExpectedTone:
            if 'WHITE' in strExpectedTone:
                reporter.ReportEvent('Test Validation', 'Validating <B>' + strExpectedMode + ' </B>Mode with <B>' + str(
                    strExpectedTone) + '</B> tone', 'Done')
            else:
                reporter.ReportEvent('Test Validation', 'Validating <B>' + strExpectedMode + ' </B>Mode with <B>' + str(
                    strExpectedTone) + '</B> Colour', 'Done')
            self.validateLightLog(reporter, oLightEP, 'Test', strExpectedMode, strExpectedStatus, strExpectedBrightness,
                                  strExpectedTone)
        else:
            if strExpectedBrightness:
                reporter.ReportEvent('Test Validation', 'Validating <B>' + strExpectedMode + ' </B>Mode with <B>' + str(
                    strExpectedBrightness).replace('.0', '') + '%</B> brightness', 'Done')
                self.validateLightLog(reporter, oLightEP, 'Test', strExpectedMode, strExpectedStatus,
                                      strExpectedBrightness)
            else:
                reporter.ReportEvent('Test Validation', 'Validating <B>' + strExpectedMode + ' </B>Mode with <B>' + str(
                    strExpectedStatus) + '</B> status', 'Done')
                self.validateLightLog(reporter, oLightEP, 'Test', strExpectedMode, strExpectedStatus)

    def validateLightLog(self, reporter, oLightEP, strValidationType, strExpectedMode, strExpectedStatus,
                         strExpectedBrightness=None, strExpectedTone=None):
        if strValidationType.upper() == "MAIN CLIENT":
            strLog, strStatus = self.getLightLog(oLightEP, strValidationType, strExpectedMode, strExpectedStatus,
                                                 strExpectedBrightness)
            reporter.ReportEvent('Client Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "TEST":
            if strExpectedTone:
                strLog, strStatus = self.getLightLog(oLightEP, strValidationType, strExpectedMode, strExpectedStatus,
                                                     strExpectedBrightness, strExpectedTone)
                reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
            else:
                if strExpectedBrightness:
                    strLog, strStatus = self.getLightLog(oLightEP, strValidationType, strExpectedMode,
                                                         strExpectedStatus, strExpectedBrightness)
                    reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
                else:
                    strLog, strStatus = self.getLightLog(oLightEP, strValidationType, strExpectedMode,
                                                         strExpectedStatus)
                    reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

    # Gets the SP log and validates the same and updates the report
    def validateAndUpdateSPLog(self, reporter, strValidationType, SPNodeID, strExpectedMode='AUTO',
                               strExpectedState="OFF", intBrightness=0, strExpextedHolidayStart="",
                               strExpectedHolidayEnd=""):
        if strValidationType.upper() == "TEST":
            strLog, strStatus = self.getSPLog(strValidationType, SPNodeID, strExpectedMode, strExpectedState,
                                              intBrightness, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
            strLog, strStatus = self.getBrightnessALLog(strValidationType, SPNodeID, strExpectedMode, strExpectedState,
                                                        intBrightness, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "MAIN CLIENT":
            strLog, strStatus = self.getSPLog(strValidationType, strExpectedMode, strExpectedState, intBrightness,
                                              strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Main Client Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "SECONDARY CLIENT":
            strLog, strStatus = self.getSPLog(strValidationType, strExpectedMode, strExpectedState, intBrightness,
                                              strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Secondary Client Validation', strLog, strStatus, 'Center')

    # Get the log for state and updates in the report
    def validateAndUpdateStateLog(self, reporter, oThermostatEP, strValidationType, strExpectedState, strExpectedMode,
                                  strExpectedTemperature=1.0, strExpextedHolidayStart="", strExpectedHolidayEnd=""):

        if strValidationType.upper() == "TEST":
            strLog, strStatus = self.getStateLog(oThermostatEP, strValidationType, strExpectedState, strExpectedMode,
                                                 strExpectedTemperature, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "MAIN CLIENT":
            strLog, strStatus = self.getStateLog(oThermostatEP, strValidationType, strExpectedState, strExpectedMode,
                                                 strExpectedTemperature, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Main Client Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "SECONDARY CLIENT":
            strLog, strStatus = self.getStateLog(oThermostatEP, strValidationType, strExpectedState, strExpectedMode,
                                                 strExpectedTemperature, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Secondary Client Validation', strLog, strStatus, 'Center')

            # Get the client status of hive devices

        def getClientStatusHiveDevices(self, context, oThermostatEP, strStatus, deviceName=None):
            Dict = {'0000': 'OFF', '': 'ON', '0001': 'ON', 'ON': 'ON', 'OFF': 'OFF'}
            oThermostatEP.deviceName = deviceName
            oThermostatEP.getAttributesFromClient()

            # Client Values
            strMode = oThermostatEP.mode
            stRunningState = Dict[oThermostatEP.thermostatRunningState]
            if oThermostatEP.type == 'HEAT':
                strTemp = oThermostatEP.occupiedHeatingSetpoint

            if strStatus == stRunningState:
                print("Staus is same")
                context.reporter.ReportEvent('Client Validation', 'STATUS IS ' + stRunningState, 'PASS', 'Center')
            else:
                self.setClientStatusHiveDevice(oThermostatEP, strStatus, deviceName)

            # API Values
            oThermostatEP.update()
            strMode = oThermostatEP.mode
            stRunningState = Dict[oThermostatEP.thermostatRunningState]
            if oThermostatEP.type == 'HEAT':
                strTemp = oThermostatEP.occupiedHeatingSetpoint

            if strStatus == stRunningState:
                print("Status is same for API")
                context.reporter.ReportEvent('Platform Validation', 'STATUS IS ' + stRunningState, 'PASS', 'Center')

        def getStatusHiveDevices(self, context, oThermostatEP, strExpectedStatus, deviceName=None):
            Dict = {'0000': 'OFF', '': 'ON', '0001': 'ON', 'ON': 'ON', 'OFF': 'OFF'}
            oThermostatEP.deviceName = deviceName
            oThermostatEP.getAttributesFromClient()

            # Client Values
            strMode = oThermostatEP.mode
            stRunningState = Dict[oThermostatEP.thermostatRunningState]

            if strExpectedStatus == stRunningState:
                context.reporter.ReportEvent('Client Validation', 'STATUS IS ' + stRunningState, 'PASS', 'Center')

            # API Values
            oThermostatEP.update()
            strMode = oThermostatEP.mode
            stRunningState = Dict[oThermostatEP.thermostatRunningState]
            if oThermostatEP.type == 'HEAT':
                strTemp = oThermostatEP.occupiedHeatingSetpoint

            if strExpectedStatus == stRunningState:
                context.reporter.ReportEvent('Platform Validation', 'STATUS IS ' + stRunningState, 'PASS', 'Center')

    def setClientStatusHiveDevice(self, oThermostatEP, strMode, deviceName=''):
        oThermostatEP.deviceName = deviceName
        if oThermostatEP.type == 'PLUG':
            oThermostatEP.setState(strMode)
        else:
            oThermostatEP.setMode(strMode)

    # Gets the Log to be updated in the Report
    def getStateLog(self, oThermostatEP, strValidationType, strExpectedState, strExpectedMode, strExpectedSPTemp=1.0,
                    strExpextedHolidayStart="", strExpectedHolidayEnd=""):

        strLocalTemperature = 0.0
        strActualTSEPSPTemp = 0.0
        strExpectedTHRunState = ''
        if 'CLIENT' in strValidationType.upper():
            oThermostatEP.update_attributes_from_client()
        else:
            try:
                oThermostatEP.update()
            except:
                pass
        strActualTSEPMode = oThermostatEP.mode
        strActualTSRunState = oThermostatEP.thermostatRunningState
        if strActualTSRunState == '0000':
            strActualTSRunState = 'OFF'
        else:
            strActualTSRunState = 'ON'

        # For both modes, state changes should always come from Feature file, as mode change will verify the expected state for plug when changed from manual to schedule.
        # But need to write for change from scehdule to manual checcking if it stays as it is
        strExpectedTHRunState = strExpectedState
        strTempCompLog = ''
        boolStatus = 'PASS'

        # Running State
        if strExpectedTHRunState == strActualTSRunState:
            strActualTSRunState = '$$' + strActualTSRunState
        else:
            strActualTSRunState = '$$||' + strActualTSRunState
            boolStatus = 'FAIL'

        '''
        # Adding C
        if not oThermostatEP.type == 'PLUG':
            if not oThermostatEP.type == 'WATER':
                strExpectedSPTemp = str(strExpectedSPTemp) + 'C'
                strActualTSEPSPTemp = str(strActualTSEPSPTemp) + 'C'

        # Holiday Mode
        if strExpectedMode is not None:
            if 'HOLIDAY' in strExpectedMode:
                if str(strExpextedHolidayStart) == str(strActualHolidayStart):
                    strActualHolidayStart = '$$' + str(strActualHolidayStart)
                else:
                    strActualHolidayStart = '$$||' + str(strActualHolidayStart)
                    boolStatus = 'FAIL'
                if str(strExpectedHolidayEnd) == str(strActualHolidayEnd):
                    strActualHolidayEnd = '$$' + str(strActualHolidayEnd)
                else:
                    strActualHolidayEnd = '$$||' + str(strActualHolidayEnd)
                    boolStatus = 'FAIL'
        '''

        # Setting the Header for Pass and Fail
        if boolStatus == 'PASS':
            if oThermostatEP.type == 'PLUG':
                strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-Plug Values" + "@@@"
                strActualTSEPMode = ''
                strActualTSEPSPTemp = ''
                strActualTSRunState = ''
                strActualHolidayStart = ''
                strActualHolidayEnd = ''
            else:
                strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-Thermostat Values" + "@@@"
                strActualTSEPMode = ''
                strActualTSEPSPTemp = ''
                strActualTSRunState = ''
                strActualHolidayStart = ''
                strActualHolidayEnd = ''
        else:
            if oThermostatEP.type == 'PLUG':
                strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Plug Values" + "@@@"
            else:
                strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Thermostat Values" + "@@@"

        strLog = ''
        if strExpectedTHRunState is not None:

            if oThermostatEP.type == 'HEAT':
                strTempCompLog = '$~Current Setpoint Temperature$$' + strExpectedSPTemp + strActualTSEPSPTemp
            if not oThermostatEP.type == 'PLUG':
                strLog = strHeader + \
                         'Current System mode$$' + strExpectedMode + strActualTSEPMode + strTempCompLog + \
                         '$~Current Thermostat Running State$$' + strExpectedTHRunState + strActualTSRunState
            elif oThermostatEP.type == 'PLUG':
                strLog = strHeader + \
                         'Current Active Plug Running State$$' + strExpectedTHRunState + strActualTSRunState
            '''
            if 'HOLIDAY' in strExpectedMode:
                strLog = strLog + '$~Holiday Mode Start Date$$' + str(strExpextedHolidayStart) + str(
                    strActualHolidayStart) + \
                         '$~Holiday Mode End Date$$' + str(strExpectedHolidayEnd) + str(strActualHolidayEnd)
            '''
        return strLog, boolStatus

    def getLightLog(self, oLightEP, strValidationType, strExpectedMode, strExpectedStatus, strExpectedBrightness=None,
                    strExpectedTone=None):
        if 'MAIN CLIENT' in strValidationType.upper():
            strActualMode, strActualStatus, strActualBrightness = oLightEP.update_attributes_from_client()
        else:
            try:
                oLightEP.update()
                strActualMode = oLightEP.mode
                strActualStatus = oLightEP.CurrentDeviceState

                if strActualMode.upper().find('AUTO') >= 0:
                    strActualMode = 'SCHEDULE'
                else:
                    strActualMode = strActualMode.upper()
                strActualBrightness = oLightEP.lightBrightness
                if oLightEP.type != 'WARMWHITE':
                    strActualTone = oLightEP.floatColourTemperature
            except:
                pass

        strActualMode = oLightEP.mode
        strActualStatus = oLightEP.CurrentDeviceState

        if strActualMode.upper().find('AUTO') >= 0:
            strActualMode = 'SCHEDULE'
        else:
            strActualMode = strActualMode.upper()
        strActualBrightness = str(oLightEP.lightBrightness).replace('.0', '')
        if oLightEP.type != 'WARMWHITE':
            strActualTone = str(oLightEP.floatColourTemperature)

        boolStatus = 'PASS'
        if str(strActualMode) == str(strExpectedMode):
            strActualMode = '$$' + str(strActualMode)
        else:
            strActualMode = '$$||' + strActualMode
            boolStatus = 'FAIL'

        if str(strActualStatus) == str(strExpectedStatus):
            strActualStatus = '$$' + str(strActualStatus)
        else:
            strActualStatus = '$$||' + strActualStatus
            boolStatus = 'FAIL'

        if strExpectedBrightness:
            strExpectedBrightness = str(strExpectedBrightness).replace('.0', '')
            if str(strActualBrightness) == str(strExpectedBrightness):
                strActualBrightness = '$$' + str(strActualBrightness) + '%'
            else:
                strActualBrightness = '$$||' + str(strActualBrightness) + '%'
                boolStatus = 'FAIL'

        if strExpectedTone:
            if strActualTone == strExpectedTone:
                strActualTone = '$$' + strActualTone
            else:
                strActualTone = '$$||' + strActualTone
                boolStatus = 'FAIL'

        if boolStatus == 'PASS':
            if strValidationType.upper() == 'TEST':
                strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-Light Values" + "@@@"
            else:
                strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-MAIN CLIENT Values" + "@@@"
            strActualMode = ''
            strActualStatus = ''
            if strExpectedBrightness:
                strActualBrightness = ''
            if strExpectedTone:
                strActualTone = ''
        else:
            if strValidationType.upper() == 'TEST':
                strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Light Values" + "@@@"
            else:
                strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-MAIN CLIENT Values" + "@@@"

        strBrightnessCompLog = ''
        strToneCompLog = ''
        if strExpectedMode is not None:
            if strExpectedBrightness is not None:
                if not strExpectedStatus == 'OFF':
                    strBrightnessCompLog = '$~Current light Brightness$$' + str(strExpectedBrightness) + '%' + str(
                        strActualBrightness)
            if strExpectedTone is not None:
                strToneCompLog = '$~Current light Tone/Colour$$' + strExpectedTone + strActualTone
            strLog = strHeader + \
                     'Current System mode$$' + strExpectedMode + strActualMode + \
                     '$~Current Light Running State$$' + strExpectedStatus + strActualStatus + \
                     strBrightnessCompLog + strToneCompLog

        return strLog, boolStatus

    # Gets the Log to be updated in the Report
    def getLog(self, oThermostatEP, strValidationType, strExpectedMode='', strExpectedSPTemp=1.0,
               strExpextedHolidayStart="", strExpectedHolidayEnd=""):
        """
        strStatusCode = str(oThermostatEP.model.statusCode)
        print(strStatusCode)
        if len(strStatusCode.split(":"))>1:
            strStatusCode = strStatusCode[1] + ' for: <br>'
        print(strStatusCode)
        """
        strLocalTemperature = 0.0
        strActualTSEPSPTemp = 0.0
        strExpectedTHRunState = ''
        if 'CLIENT' in strValidationType.upper():
            oThermostatEP.update_attributes_from_client()
        else:
            try:
                '''try:
                    AT.stopThreads()
                    AT.startAttributeListener(printStatus=False)
                    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                except:
                    AT.startAttributeListener(printStatus=False)
                    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)'''
                oThermostatEP.update()
                oThermostatEP.model.checkModel()
            except:
                pass
        print(oThermostatEP.mode + "===========\n")
        strActualTSEPMode = oThermostatEP.mode
        if not oThermostatEP.type == 'WATER' and not oThermostatEP.type == 'PLUG':
            strExpectedSPTemp = self.convertHexTemp(oThermostatEP.model.occupiedHeatingSetpoint, False)
        if not oThermostatEP.type == 'PLUG':
            if not oThermostatEP.type == 'WATER':
                strActualTSEPSPTemp = self.convertHexTemp(oThermostatEP.occupiedHeatingSetpoint, False)
                strLocalTemperature = self.convertHexTemp(oThermostatEP.localTemperature, False)
        strActualTSRunState = oThermostatEP.thermostatRunningState
        if strActualTSRunState == '0000':
            strActualTSRunState = 'OFF'
        else:
            strActualTSRunState = 'ON'

        # Setting Expected Thermostat run state for Test Validation
        if oThermostatEP.type == 'WATER' and strValidationType.upper() != "MODEL":
            if self.getWaterModes[strExpectedMode] == 'Always OFF':
                strExpectedTHRunState = 'OFF'
            elif self.getWaterModes[strExpectedMode] == 'AUTO':
                print('Current Event ', oSchdUt.getCurrentTempFromSchedule(oThermostatEP.getSchedule()))
                if 0.0 in oSchdUt.getCurrentTempFromSchedule(oThermostatEP.getSchedule()):
                    strExpectedTHRunState = 'OFF'
                else:
                    strExpectedTHRunState = 'ON'
            elif self.getWaterModes[strExpectedMode] == 'BOOST' or self.getWaterModes[strExpectedMode] == 'Always ON':
                strExpectedTHRunState = 'ON'

        elif oThermostatEP.type == 'PLUG' and strValidationType.upper() != "MODEL":
            # if self.getPlugModes[strExpectedMode]== 'Always ON': strExpectedTHRunState = 'ON'
            if self.getPlugModes[strExpectedMode] == 'MANUAL':
                strExpectedTHRunState = 'ON'
            elif self.getPlugModes[strExpectedMode] == 'AUTO':
                print('Current Event, Time remaining ', oSchdUt.getCurrentTempFromSchedule(oThermostatEP.getSchedule()))
                if 'OFF' in oSchdUt.getCurrentTempFromSchedule(oThermostatEP.getSchedule()):
                    strExpectedTHRunState = 'OFF'
                else:
                    strExpectedTHRunState = 'ON'
                    # elif self.getWaterModes[strExpectedMode]=='BOOST' or self.getWaterModes[strExpectedMode]=='Always ON':  strExpectedTHRunState = 'ON'

        # For Heating
        else:
            if float(strLocalTemperature) < float(strActualTSEPSPTemp):
                strExpectedTHRunState = 'ON'
            else:
                strExpectedTHRunState = 'OFF'

        # Get Expected values from Thermostat Model Validation
        if strValidationType.upper() == "MODEL":
            strExpectedMode = oThermostatEP.model.mode
            if not oThermostatEP.type == 'WATER':
                strExpectedSPTemp = oThermostatEP.model.occupiedHeatingSetpoint
                if not isinstance(strExpectedSPTemp, float): strExpectedSPTemp = self.convertHexTemp(strExpectedSPTemp,
                                                                                                     False)
            # Setting Expected Thermostat run state for Model validation
            strExpectedTHRunState = oThermostatEP.model.thermostatRunningState
            if strExpectedTHRunState == '0000':
                strExpectedTHRunState = 'OFF'
            else:
                strExpectedTHRunState = 'ON'
            # Holiday Mode
            if 'HOLIDAY' in strExpectedMode:
                strExpextedHolidayStart = oThermostatEP.model.holidayModeStart
                strExpectedHolidayEnd = oThermostatEP.model.holidayModeEnd

        # Set Water Mode Format
        if oThermostatEP.type == 'WATER':
            strActualTSEPMode = self.getWaterModes[strActualTSEPMode]
            strExpectedMode = self.getWaterModes[strExpectedMode]
            if strActualTSEPMode == 'AUTO': strActualTSEPMode = 'AUTO-' + strActualTSRunState
            if strExpectedMode == 'AUTO': strExpectedMode = 'AUTO-' + strExpectedTHRunState

        # Set Plug Mode Format
        if oThermostatEP.type == 'PLUG':
            strActualTSEPMode = self.getPlugModes[strActualTSEPMode]
            strExpectedMode = self.getPlugModes[strExpectedMode]
            if strActualTSEPMode == 'AUTO': strActualTSEPMode = 'AUTO-' + strActualTSRunState
            if strExpectedMode == 'AUTO': strExpectedMode = 'AUTO-' + strExpectedTHRunState

        # Holiday Mode
        if strExpectedMode is not None:
            if 'HOLIDAY' in strExpectedMode:
                strActualHolidayStart = oThermostatEP.holidayStart
                strActualHolidayEnd = oThermostatEP.holidayEnd

        strTempCompLog = ''
        boolStatus = 'PASS'
        # Mode
        if not oThermostatEP.type == 'PLUG':
            if not oThermostatEP.type == 'WATER':
                if not isinstance(strActualTSEPSPTemp, str): strActualTSEPSPTemp = str(strActualTSEPSPTemp)
        if str(strExpectedMode) == str(strActualTSEPMode):
            strActualTSEPMode = '$$' + str(strActualTSEPMode)
        else:
            strActualTSEPMode = '$$||' + strActualTSEPMode
            boolStatus = 'FAIL'
        # Temperature
        if not oThermostatEP.type == 'PLUG':
            if not oThermostatEP.type == 'WATER':
                if str(strExpectedSPTemp) == str(strActualTSEPSPTemp):
                    strActualTSEPSPTemp = '$$' + strActualTSEPSPTemp
                else:
                    strActualTSEPSPTemp = '$$||' + strActualTSEPSPTemp
                    boolStatus = 'FAIL'
        # Running State
        if not oThermostatEP.type == 'PLUG':
            if strExpectedTHRunState == strActualTSRunState:
                strActualTSRunState = '$$' + strActualTSRunState
            else:
                strActualTSRunState = '$$||' + strActualTSRunState
                boolStatus = 'FAIL'

        elif oThermostatEP.type == 'PLUG':
            if strExpectedMode == 'AUTO-' + strExpectedTHRunState:
                if strExpectedTHRunState == strActualTSRunState:
                    strActualTSRunState = '$$' + strActualTSRunState
                else:
                    strActualTSRunState = '$$||' + strActualTSRunState
                    boolStatus = 'FAIL'

        # Adding C
        if not oThermostatEP.type == 'PLUG':
            if not oThermostatEP.type == 'WATER':
                strExpectedSPTemp = str(strExpectedSPTemp) + 'C'
                strActualTSEPSPTemp = str(strActualTSEPSPTemp) + 'C'

        # Holiday Mode
        if strExpectedMode is not None:
            if 'HOLIDAY' in strExpectedMode:
                if str(strExpextedHolidayStart) == str(strActualHolidayStart):
                    strActualHolidayStart = '$$' + str(strActualHolidayStart)
                else:
                    strActualHolidayStart = '$$||' + str(strActualHolidayStart)
                    boolStatus = 'FAIL'
                if str(strExpectedHolidayEnd) == str(strActualHolidayEnd):
                    strActualHolidayEnd = '$$' + str(strActualHolidayEnd)
                else:
                    strActualHolidayEnd = '$$||' + str(strActualHolidayEnd)
                    boolStatus = 'FAIL'

        # Setting the Header for Pass and Fail
        if boolStatus == 'PASS':
            if oThermostatEP.type == 'PLUG':
                strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-Plug Values" + "@@@"
                strActualTSEPMode = ''
                strActualTSEPSPTemp = ''
                strActualTSRunState = ''
                strActualHolidayStart = ''
                strActualHolidayEnd = ''
            else:
                strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-Thermostat Values" + "@@@"
                strActualTSEPMode = ''
                strActualTSEPSPTemp = ''
                strActualTSRunState = ''
                strActualHolidayStart = ''
                strActualHolidayEnd = ''
        else:
            if oThermostatEP.type == 'PLUG':
                strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Plug Values" + "@@@"
            else:
                strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Thermostat Values" + "@@@"

        strLog = ''
        if strExpectedMode is not None:
            if not oThermostatEP.type == 'PLUG':
                if not oThermostatEP.type == 'WATER':
                    strTempCompLog = '$~Current Setpoint Temperature$$' + strExpectedSPTemp + strActualTSEPSPTemp

                strLog = strHeader + \
                         'Current System mode$$' + strExpectedMode + strActualTSEPMode + strTempCompLog + \
                         '$~Current Thermostat Running State$$' + strExpectedTHRunState + strActualTSRunState

            if oThermostatEP.type == 'PLUG':
                if strExpectedMode == 'AUTO-' + strExpectedTHRunState:
                    strLog = strHeader + \
                             'Current Plug mode$$' + strExpectedMode + strActualTSEPMode + strTempCompLog + \
                             '$~Current Plug State$$' + strExpectedTHRunState + strActualTSRunState
                else:
                    strLog = strHeader + \
                             'Current Plug mode$$' + strExpectedMode + strActualTSEPMode

            if 'HOLIDAY' in strExpectedMode:
                strLog = strLog + '$~Holiday Mode Start Date$$' + str(strExpextedHolidayStart) + str(
                    strActualHolidayStart) + \
                         '$~Holiday Mode End Date$$' + str(strExpectedHolidayEnd) + str(strActualHolidayEnd)

        return strLog, boolStatus



        # Gets the SP Log to be updated in the Report

    def getSPLog(self, strValidationType, SPNodeID, strExpectedMode='', strExpectedState="OFF", intBrightness=0,
                 strExpextedHolidayStart="", strExpectedHolidayEnd=""):

        strActualSPMode, strActualSPState, intActualBrightness = getSPAttributes(SPNodeID)

        strStateCompLog = ''
        boolStatus = 'PASS'
        # Mode
        if str(strExpectedMode) == str(strActualSPMode):
            strActualSPMode = '$$' + str(strActualSPMode)
        else:
            strActualSPMode = '$$||' + strActualSPMode
            boolStatus = 'FAIL'
        # State
        if str(strExpectedState) == str(strActualSPState):
            strActualSPState = '$$' + strActualSPState
        else:
            strActualSPState = '$$||' + strActualSPState
            boolStatus = 'FAIL'

        # Setting the Header for Pass and Fail
        if boolStatus == 'PASS':
            strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-SP Values" + "@@@"
            strActualSPMode = ''
            strActualSPState = ''
        else:
            strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-SP Values" + "@@@"

        strStateCompLog = '$~Current State$$' + strExpectedState + strActualSPState

        strLog = strHeader + \
                 'Current System mode$$' + strExpectedMode + strActualSPMode + strStateCompLog

        return strLog, boolStatus

    def getBrightnessALLog(self, strValidationType, SPNodeID, strExpectedMode='', strExpectedState="OFF",
                           intBrightness=0, strExpextedHolidayStart="", strExpectedHolidayEnd=""):
        boolStatus = 'PASS'
        strActualSPMode, strActualSPState, intActualBrightness = getSPAttributes(SPNodeID)
        print("Brightness : " + str(intBrightness) + "\n")
        print("Actual Brightness : " + str(intActualBrightness) + "\n")

        # Brightness
        if intBrightness == intActualBrightness:
            strActualBrightness = '$$' + str(intActualBrightness)
        else:
            strActualBrightness = '$$||' + str(intActualBrightness)
            boolStatus = 'FAIL'

        # Setting the Header for Pass and Fail
        strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-SP Values" + "@@@"

        strStateCompLog = '$~Current Brightness$$' + str(intBrightness) + strActualBrightness
        strLog = strHeader + \
                 strStateCompLog

        return strLog, boolStatus

    # Converts the Report log format to Console print log
    def conertToPrintLog(self, strReportLog):
        arrReportLog = strReportLog.split("@@@")
        strPrintLog = arrReportLog[0].split("$$")[0] + ': ===>> Expected Thermostat Values:\n'
        for strRow in arrReportLog[1].split("$~"):
            strPrintLog = strPrintLog + strRow.split("$$")[0] + ' ===>> ' + strRow.split("$$")[1] + '\n'

        return strPrintLog

    # Converts the hex value of the retrieved temperature
    def convertHexTemp(self, hexTemperature, booWithCentigradeSymbol=True):
        if isinstance(hexTemperature, str):
            if booWithCentigradeSymbol:
                strTemperature = str(int(hexTemperature, 16) / 100) + 'C'
            else:
                strTemperature = str(int(hexTemperature, 16) / 100)
            return strTemperature
        else:
            return hexTemperature

    # initializes the required Client Drivers for the test
    def intializeDrivers(self, context):
        if 'PLATFORM' in context.APIType.upper():

            strUserName = utils.getAttribute('common', 'userName')
            strPassword = utils.getAttribute('common', 'password')
            boolAndroidDriverSetUp = False
            boolIOSDriverSetUp = False
            boolWebDriverSetUp = False
            boolLoadSecondaryClient = False

            # strMainClient = utils.getAttribute('common', 'mainClient')
            # strSecondaryClient = utils.getAttribute('common', 'secondClient')
            # if not 'WEB' in  strMainClient.upper(): boolLoadSecondaryClient = True
            print(context.oScenarioClientsDict)
            for strClient in context.oScenarioClientsDict.keys():
                if strClient.upper().find('ANDROID') >= 0 and (not boolAndroidDriverSetUp):
                    oBasePage = paygeAndroid.BasePage(None, context.reporter)
                    strAppPath = utils.getAttribute('android', 'appFileName')
                    strAndroidPlatformVersion = utils.getAttribute('android', 'platformVersion')
                    strDeviceName = utils.getAttribute('android', 'deviceName')
                    context.oThermostatEP.AndroidDriver = oBasePage.setup_android_driver(strAndroidPlatformVersion,
                                                                                         strDeviceName, strAppPath)
                    oLoginPage = paygeAndroid.LoginPage(context.oThermostatEP.AndroidDriver, context.reporter)
                    oLoginPage.login_hive_app(strUserName, strPassword)
                    boolAndroidDriverSetUp = True
                elif (strClient.upper().find('WEB') >= 0 and (not boolWebDriverSetUp)) or boolLoadSecondaryClient:
                    boolLoadSecondaryClient = False
                    strURL = utils.getAttribute('web', 'loginURL')
                    strBrowserName = utils.getAttribute('web', 'browserName')
                    oBasePage = paygeWeb.BasePage(None, context.reporter)
                    context.oThermostatEP.WebDriver = oBasePage.setup_Selenium_driver(strBrowserName, strURL)
                    oLoginPage = paygeWeb.LoginPage(context.oThermostatEP.WebDriver, context.reporter)
                    oLoginPage.login_hive_app(strUserName, strPassword)
                    boolWebDriverSetUp = True
                elif strClient.upper().find('IOS') >= 0 and (not boolIOSDriverSetUp):
                    strAppPath = utils.getAttribute('iOS', 'appFileName')
                    strDeviceName = utils.getAttribute('iOS', 'deviceName')
                    oBasePage = paygeiOS.BasePage(None, context.reporter)
                    context.oThermostatEP.iOSDriver = oBasePage.setup_ios_driver(strDeviceName, strAppPath)
                    oLoginPage = paygeiOS.LoginPage(context.oThermostatEP.iOSDriver, context.reporter)
                    oLoginPage.login_hive_app(strUserName, strPassword)
                    boolIOSDriverSetUp = True
                    '''
                    oHomePage = paygeiOS.HomePage(context.oThermostatEP.iOSDriver, context.reporter)
                    oHomePage.navigate_to_heating_control_page()
                    oHeatingControlPage = paygeiOS.HeatingControlPage(context.oThermostatEP.iOSDriver, context.reporter)
                    oHeatingControlPage.set_heat_mode('AUTO')
                    oBasePage.refresh_page()
                    context.oThermostatEP.iOSDriver.quit()
                    exit()
                    '''

    # Kills the required Client Drivers for the test
    def quitDrivers(self, context):
        if not context.AndroidDriver is None: context.AndroidDriver.quit()
        if not context.WebDriver is None: context.WebDriver.quit()
        if not context.iOSDriver is None: context.iOSDriver.quit()

    def navigateToScreen(self, reporter, oThermostatEP, strPage):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Navigate to : ' + str(strPage) + ' screen')
        # Set the page to navigate
        oThermostatEP.navigateToScreen(strPage)
        reporter.ReportEvent('Test Validation', 'navigate to <B>' + str(strPage), 'PASS')
        if not reporter.ActionStatus: return False

    def changePassword(self, reporter, oThermostatEP, strPage):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Navigate to : ' + str(strPage) + ' screen')
        # Set the page to navigate
        oThermostatEP.changePasswordScreen(strPage)
        reporter.ReportEvent('Test Validation', 'navigate to <B>' + str(strPage), 'PASS')
        if not reporter.ActionStatus: return False

    def validateNotification(self, reporter, boolAutoMode, oThermostatEP, strExpectedTemp, strRuleType):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strRuleType + ' Notification Alert')
        reporter.ReportEvent('Test Validation',
                             'Validating <B>' + strRuleType + '</B> Notification Alert with Temperature set to <B>' + str(
                                 strExpectedTemp) + '</B>', 'Done')
        self.validateAndUpdateRulesLog(reporter, oThermostatEP, 'TEST', strExpectedTemp, strRuleType)

    def validateNotificationOnOff(self, reporter, boolAutoMode, oThermostatEP, strExpectedTemp, strRuleType,
                                  strExpectedRuleStatus):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strExpectedRuleStatus + ' Notification Alert')
        reporter.ReportEvent('Test Validation', 'Validating Notification Alert as <B>' + strExpectedRuleStatus + '</B>',
                             'Done')
        self.validateAndUpdateRulesLog(reporter, oThermostatEP, 'TEST', strExpectedTemp, strRuleType,
                                       strExpectedRuleStatus)

    def validateAndUpdateRulesLog(self, reporter, oThermostatEP, strValidationType, strExpectedTemp, strRuleType,
                                  strExpectedRuleStatus='ACTIVE'):
        if strValidationType.upper() == 'TEST':
            strLog, strStatus = self.getRulesLog(oThermostatEP, strValidationType, strExpectedTemp, strRuleType,
                                                 strExpectedRuleStatus)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

    def getTableLogs(self, strLog, strColumnOne, strColumnTwo, strColumnThree, strValidation):

        if strLog == "":
            if strValidation.lower() == "deviceproperties":
                strLog = "Attribute $$ Expected Value $$Actual Value@@@"
            if strValidation.lower() == "devicehierarchy":
                strLog = "Device Name $$ Device Type $$Position@@@"
        else:
            strLog = strLog + "$~"
        strLog = strLog + strColumnOne + "$$" + strColumnTwo + "$$" + strColumnThree

        return strLog

    def intendedUsage(self, context):
        context.leakSensorEP.intendedUsage()

    # Validate leak status
    def validateLeakStatus(self, context):
        """Add Target Status"""
        context.leakSensorEP.getLeakSensorNode()
        boolStatus = True
        strStatus = 'PASS'
        dictLeak = {False: "ABSENT", True: 'PRESENT', 'NONE': 'All OK', 'LOW': 'Low water flow',
                    'HIGH': 'Large water flow alert', 'USER_INTENDED_USAGE': 'All OK',
                    'LEAK_FIXED': 'All OK', 'USER_OVERRIDE_HIGH': 'Large water flow alert',
                    'USER_OVERRIDE_LOW': 'Low water flow'}
        # actualStatus = context.leakSensorEP.clientLeakStatus
        # actualCalibration = dictLeak[context.leakSensorEP.blnClientCalibrationAt]
        #
        # expectedStatus = dictLeak[context.leakSensorEP.leakStatus]
        # expectedCalibration = dictLeak[context.leakSensorEP.blnCalibrationAt]
        #
        # if actualStatus == expectedStatus:
        #     actualStatus = '$$'+ actualStatus
        # else:
        #     actualStatus = '$$||'+ actualStatus
        #     boolStatus = False
        #
        # if actualCalibration == expectedCalibration:
        #     actualCalibration = '$$'+ actualCalibration
        # else:
        #     actualCalibration = '$$||'+ actualCalibration
        #     boolStatus = False
        #
        # if boolStatus:
        #     strHeader = "Attributes$$" + "Expected and Actual- API Values" + "@@@"
        #     actualStatus = ''
        #     actualCalibration = ''
        # else:
        #     strHeader = "Attributes$$" + "Expected-  API Values$$ Actual- Client Values" + "@@@"
        #     strStatus = "FAIL"
        #
        # strLog = strHeader + \
        #          'Current Leak Status$$' + context.leakSensorEP.leakStatus + actualStatus + '$~Current Calibration Appearance$$' \
        #          + expectedCalibration + actualCalibration

        expectedDict = {'Expected Values': {'is Leaking Attribute': context.strNotification}}
        actualDict = {'API Values': {'is Leaking Attribute': context.leakSensorEP.leakStatus}}
        log, status = context.reporter.logCreation(actualDict, expectedDict)
        context.reporter.ReportEvent('Platform Validation', log, status, 'Center')

        expectedDict = {'Expected Values': {'status': dictLeak[context.strNotification]}}
        actualDict = {'Client Values': {'status': context.leakSensorEP.clientLeakStatus}}
        log, status = context.reporter.logCreation(actualDict, expectedDict)
        context.reporter.ReportEvent('Client Validation', log, status, 'Center')

    # Fetch Leak satus at client
    def update_clientleakStatus(self, context):
        # context.leakSensorEP.leak_control_navigation()
        context.leakSensorEP.fetch_leak_status()

    # Generate and validate leak notification
    def leakNotification(self, context):
        try:

            boolStatus = True
            boolEmailStatus = True
            strStatus = 'PASS'
            blnRuleStatus = False
            emailText = ''
            boolSMSStatus = True
            notificationTypeDict = {'SMALL LEAK': "Low water flow",
                                    'LARGE FLOW': 'High water usage',
                                    'FLOW NONE': 'All sorted',
                                    'PRESS BUTTON': 'Confirmation',
                                    'LOW BATTERY': 'Battery low',
                                    'OFFLINE': 'Device offline'}
            notificationContentDict = {'SMALL LEAK': "Low water flow detected. Open the app to check it out.",
                                       'LARGE FLOW': 'High water usage detected. Open the app to check it out.',
                                       'FLOW NONE': "We are no longer seeing a water flow. We'll let you know if anything changes.",
                                       'PRESS BUTTON': 'The <deviceName> is communicating properly. We will notify you '
                                                       'if it detects anything out of the ordinary.',
                                       'LOW BATTERY': 'Battery low: <deviceName>',
                                       'OFFLINE': '<deviceName> is offline'}

            # Flow None needs to be added
            notificationRuleDict = {'SMALL LEAK': 'RULE_LEAK_DETECTED',
                                    'LARGE FLOW': 'RULE_FLOW_DETECTED',
                                    'FLOW NONE': 'RULE_NO_LEAK',
                                    'PUSH': 'PushNotification',
                                    'EMAIL': 'SendEmail',
                                    'SMS': 'SendSubscriptionSMS'}

            emaildict = {'SMALL LEAK': ['Low water flow',
                                        ["We have detected a low water flow in your home."
                                         "This could be a dripping tap or toilet."
                                         "Don't worry, we can help you find the issue.",
                                         "Just go to the Hive app to check it out."]],
                         'LARGE FLOW': ['High water usage',
                                        [
                                            "We have detected a High water usage in your home. This might be because someone has been using water. Open the Hive app to check it out.",
                                            "You can also change your notification settings from the Leak Sensor page in the Hive app."]],
                         'FLOW NONE': ["All sorted, we're no longer seeing a water flow",
                                       ["Great news! Looks like the water flow has stopped.",
                                        "We'll let you know if anything changes.",
                                        "Check out the Leak Sensor page in the Hive app for more information."]],
                         False: 'Email is not displaying',
                         True: 'Email is Displaying'
                         }

            SMSContentDict = {
                'SMALL LEAK': "We have detected a low water flow in your home. This could be a dripping tap. Open the Hive app to check it out.",
                'LARGE FLOW': 'We have detected high water usage in your home. This might be because someone has been using water. Open the Hive app to check it out.',
                'FLOW NONE': "We are no longer seeing a water flow. We'll let you know if anything changes."}
            SMSDict = {
                False: 'SMS is not displaying',
                True: 'SMS is Displaying'}

            context.leakSensorEP.getLeakRules()

            if context.strNotification in notificationRuleDict:
                blnPushRuleStatus = context.leakSensorEP.getRuleDict(notificationRuleDict[context.strNotification],
                                                                     notificationRuleDict['PUSH'])
                blnEmailRuleStatus = context.leakSensorEP.getRuleDict(notificationRuleDict[context.strNotification],
                                                                      notificationRuleDict['EMAIL'])
                blnSMSRuleStatus = context.leakSensorEP.getRuleDict(notificationRuleDict[context.strNotification],
                                                                    notificationRuleDict['SMS'])
            else:
                blnPushRuleStatus = True
                blnEmailRuleStatus = True
                blnSMSRuleStatus = False
            # only Push is written as of now
            ################Add clear Email################
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Alert settings for - ' + context.strNotification)
            strLog = "Alert Type$$Status@@@"
            context.ExpectedContent = notificationContentDict[context.strNotification]
            context.ExpectedContent = context.ExpectedContent.replace \
                ('<ExtendedUsageThreshold>', str(context.leakSensorEP.minLeakDuration))
            context.ExpectedContent = context.ExpectedContent.replace \
                ('<deviceName>', str(context.leakSensorEP.leakSensorName))
            if blnPushRuleStatus:
                context.ExpectedNotificationContent = context.ExpectedContent
                context.ExpectedNotificationText = notificationTypeDict[context.strNotification]
                strLog = strLog + 'Push Alert$$Active'
            else:
                context.ExpectedNotificationText = 'Notification subject is not displayed'
                context.ExpectedNotificationContent = 'Notification content is not displayed'
                strLog = strLog + 'Push Alert$$Inactive'
            emailText = emaildict[blnEmailRuleStatus]
            if blnEmailRuleStatus:
                context.ExpectedEmailText = emaildict[context.strNotification][0]
                blnSubject, blnContent = True, True
                strLog = strLog + '$~Email Alert$$Active'

            else:
                strLog = strLog + '$~Email Alert$$Inactive'
                blnSubject, blnContent = False, False

            if blnSMSRuleStatus:
                strLog = strLog + '$~Text Alert$$Active'
                blnSMSContent = True
            else:
                strLog = strLog + '$~Text Alert$$Inactive'
                blnSMSContent = False

            context.reporter.ReportEvent('Test Validation', strLog, 'DONE', 'Center')
            if context.strNotification == 'FLOW NONE': context.leakSensorEP.fix_leak()
            context.leakSensorEP.clear_notification()
            emails.readAllExistingEmails()
            unixtriggerTime = context.leakSensorEP.trigger_notification(context.strNotification)
            context.leakSensorEP.getEvents()
            context.ExpectedSMSContent = SMSContentDict[context.strNotification]
            blnSMSResp, blnSMSContentResp = self.findSMSEvent(context.leakSensorEP.events,
                                                              unixtriggerTime, context.ExpectedSMSContent)
            context.leakSensorEP.validate_notification()
            blnEmailFound, blnSubjectResp, blnContentResp = emails.findEmail(emaildict, context.strNotification)
            emailResp = emaildict[blnEmailFound]
            SMSResp = SMSDict[blnSMSResp]
            SMSText = SMSDict[blnSMSRuleStatus]

            strActualNotificationText = context.leakSensorEP.notificationText
            strActualNotificationContent = context.leakSensorEP.notificationContent
            if strActualNotificationText == '': strActualNotificationText = 'Notification subject is not displayed'
            if strActualNotificationContent == '': strActualNotificationContent = 'Notification content is not displayed'

            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validation for alerts Presence and Content')

            if strActualNotificationText == context.ExpectedNotificationText:
                strActualNotificationText = '$$' + strActualNotificationText
            else:
                strActualNotificationText = '$$||' + strActualNotificationText
                boolStatus = False

            if strActualNotificationContent == context.ExpectedNotificationContent:
                strActualNotificationContent = '$$' + strActualNotificationContent
            else:
                strActualNotificationContent = '$$||' + strActualNotificationContent
                boolStatus = False

            if boolStatus:
                strHeader = "Notification Text and Content$$" + "Expected and Actual" + "@@@"
                strActualNotificationText = ''
                strActualNotificationContent = ''
                strStatus = "PASS"
            else:
                strHeader = "Notification Text and Content$$" + "Expected $$ Actual" + "@@@"
                strStatus = "FAIL"

            strLog = strHeader + \
                     'NotificationText$$' + context.ExpectedNotificationText + strActualNotificationText \
                     + '$~Notification Content$$' \
                     + context.ExpectedNotificationContent + strActualNotificationContent

            context.reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

            if emailResp == emailText:
                emailResp = '$$' + emailResp
            else:
                emailResp = '$$||' + emailResp
                boolEmailStatus = False
            strSubject = 'Subject is expected'
            strContent = 'Content is expected'
            if blnSubject != blnSubjectResp:
                boolEmailStatus = False
                strSubjectResp = '$$||' + 'Subject is not as expected, Please view emails'
            else:
                strSubjectResp = '$$' + 'Subject is as expectd'

            if blnContent != blnContentResp:
                boolEmailStatus = False
                strContentResp = '$$||' + 'Content is not as expected, Please view emails'
            else:
                strContentResp = '$$' + 'Content is as expected'

            if boolEmailStatus:
                strHeader = "Email Text and Content$$" + "Expected and Actual" + "@@@"
                emailResp = ''
                strSubjectResp = ''
                strContentResp = ''
                strStatus = "PASS"
            else:
                strHeader = "Email Text and Content$$" + "Expected $$ Actual" + "@@@"
                strStatus = "FAIL"

            strLog = strHeader + 'Email Presence$$' + emailText + emailResp + \
                     '$~Email Subject$$' + strSubject + strSubjectResp \
                     + '$~Email Content$$' \
                     + strContent + strContentResp
            context.reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

            if SMSResp == SMSText:
                SMSResp = '$$' + SMSResp
            else:
                SMSResp = '$$||' + SMSResp
                boolSMSStatus = False
            if blnSMSRuleStatus:
                strSMSContent = 'SMS Content is expected'
            else:
                strSMSContent = 'SMS Content is not expected'

            if blnSMSContent != blnSMSContentResp:
                boolSMSStatus = False
                strContentResp = '$$||' + 'SMS Content is not as expected, Please view Texts'
            else:
                strContentResp = '$$' + 'SMS Content is as expected'

            if boolSMSStatus:
                strHeader = "SMS Content$$" + "Expected and Actual" + "@@@"
                SMSResp = ''
                strContentResp = ''
                strStatus = "PASS"
            else:
                strHeader = "SMS Content$$" + "Expected $$ Actual" + "@@@"
                strStatus = "FAIL"

            strLog = strHeader + 'SMS Presence$$' + SMSText + SMSResp + \
                     '$~SMS Content$$' \
                     + strSMSContent + strContentResp
            context.reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
        except:
            context.reporter.ReportEvent('Test Exception',
                                         'Exception  in rFM.leakNotification \n {0}'.format(
                                             traceback.format_exc().replace('File', '$~File')), 'FAIL', 'CENTER')

    # Validate the events
    def findSMSEvent(self, events, unixtriggerTime, AlertContent):
        boolSMSFound, boolSMSContent = False, False
        for eachevent in events['events']:
            eventTime = eachevent['time'].split('+')[0]
            tdeventTime = datetime.strptime(eventTime, '%Y-%m-%dT%H:%M:%S.%f')
            unixeventTime = int(time.mktime(tdeventTime.timetuple()) * 1000) + 15000
            if unixeventTime >= unixtriggerTime:
                if 'channel' in eachevent['properties']:
                    if eachevent['properties']['channel'] == 'SMS':
                        boolSMSFound = True
                        if eachevent['properties']['smsBody'] == AlertContent:
                            boolSMSContent = True
                            break
        return boolSMSFound, boolSMSContent

    # Update alert settings and validate
    def alertSettings(self, context):
        context.leakSensorEP.getLeakRules()
        context.currentRuleDict = {'PushNotification': 'INACTIVE',
                                   'SendSubscriptionSMS': 'INACTIVE', 'SendEmail': 'INACTIVE'}
        if len(context.leakSensorEP.leakRules) is not 0:
            oDict = context.leakSensorEP.leakRules
            for oDictItem in oDict:
                context.currentRuleDictTemp = oDict[oDictItem]
                break
        context.leakSensorEP.leak_control_navigation()
        context.leakSensorEP.fetch_alertSettings()
        oClientAlertDict = context.leakSensorEP.oClientAlertDict
        for oKeyAPI in context.currentRuleDictTemp.keys():
            context.currentRuleDict[oKeyAPI] = context.currentRuleDictTemp[oKeyAPI]
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate Notification Alert setting before changes')
        self.alertLog(context, context.currentRuleDict, oClientAlertDict, 'Platform', 'Client')

        context.leakSensorEP.set_alertSettings(context.oDictTargetAlertSettings)

    # Alert log validation
    def validateAlertLog(self, context):
        context.leakSensorEP.getLeakRules()
        context.currentRuleDict = {'PushNotification': 'INACTIVE',
                                   'SendSubscriptionSMS': 'INACTIVE', 'SendEmail': 'INACTIVE'}
        context.leakSensorEP.getLeakRules()
        if len(context.leakSensorEP.leakRules) is not 0:
            oDict = context.leakSensorEP.leakRules
            for oDictItem in oDict:
                context.currentRuleDictTemp = oDict[oDictItem]
                break
        for oKeyAPI in context.currentRuleDictTemp.keys():
            context.currentRuleDict[oKeyAPI] = context.currentRuleDictTemp[oKeyAPI]
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate Notification Alert setting after changes')
        self.alertLog(context, context.oDictTargetAlertSettings, context.currentRuleDict, 'Target', 'Platform')

    # Alert log reporter
    def alertLog(self, context, ExpectedDict, ActualDict, strExpected, strActual):
        boolStatus = True
        ActualTextStatus = ActualDict['SendSubscriptionSMS'].upper()
        ActualPushStatus = ActualDict['PushNotification'].upper()
        ActualEmailStatus = ActualDict['SendEmail'].upper()
        strStatus = 'PASS'

        ExpectedTextStatus = ExpectedDict['SendSubscriptionSMS'].upper()
        ExpectedPushStatus = ExpectedDict['PushNotification'].upper()
        ExpectedEmailStatus = ExpectedDict['SendEmail'].upper()

        if ActualTextStatus == ExpectedTextStatus:
            ActualTextStatus = '$$' + ActualTextStatus
        else:
            ActualTextStatus = '$$||' + ActualTextStatus
            boolStatus = False

        if ActualPushStatus == ExpectedPushStatus:
            ActualPushStatus = '$$' + ActualPushStatus
        else:
            ActualPushStatus = '$$||' + ActualPushStatus
            boolStatus = False

        if ActualEmailStatus == ExpectedEmailStatus:
            ActualEmailStatus = '$$' + ActualEmailStatus
        else:
            ActualEmailStatus = '$$||' + ActualEmailStatus
            boolStatus = False

        if boolStatus:
            strHeader = "Alert Settings$$" + "Expected - " + strExpected + " and Actual - " + strActual + "@@@"
            ActualEmailStatus = ''
            ActualPushStatus = ''
            ActualTextStatus = ''
        else:
            strHeader = "Alert Settings$$" + "Expected " + strExpected + "$$ Actual" + strActual + "@@@"
            strStatus = "FAIL"

        strLog = strHeader + \
                 'Push Alerts$$' + ExpectedPushStatus + ActualPushStatus \
                 + '$~SMS Alerts$$' \
                 + ExpectedTextStatus + ActualTextStatus + '$~Email Alerts$$' \
                 + ExpectedEmailStatus + ActualEmailStatus

        context.reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

    # Min leak functions
    def minLeak(self, context):

        strTargetduration = context.TargetminLeakDuration
        context.leakSensorEP.leak_control_navigation()
        context.leakSensorEP.min_leakduration()
        strClientLeakDuartion = context.leakSensorEP.oClientminLeak
        strPlatformLeakDuration = context.leakSensorEP.minLeakDuration
        self.minLeakLog(context, strClientLeakDuartion, strPlatformLeakDuration, 'Client', 'Platform')
        context.leakSensorEP.set_leakduration(strTargetduration)

    # Min leak validates
    def validateMinLeakLog(self, context):
        strTargetduration = context.TargetminLeakDuration
        context.leakSensorEP.getLeakSensorNode()
        strPlatformLeakDuration = context.leakSensorEP.minLeakDuration
        self.minLeakLog(context, strTargetduration, strPlatformLeakDuration, 'Target', 'Platform')

    # Min leak reporter
    def minLeakLog(self, context, ExpectedLeakDuration, ActualLeakDuartion, strExpected, strActual):
        boolStatus = True
        strStatus = 'PASS'
        if ActualLeakDuartion == ExpectedLeakDuration:
            ActualLeakDuartion = '$$' + ActualLeakDuartion
        else:
            ActualLeakDuartion = '$$||' + ActualLeakDuartion
            boolStatus = False

        if boolStatus:
            strHeader = "Min Leak Duaration Setting$$" + "Expected - " + strExpected + " and Actual - " + strActual + "@@@"
            ActualLeakDuartion = ''
        else:
            strHeader = "Min Leak Duaration Setting$$" + "Expected " + strExpected + "$$ Actual" + strActual + "@@@"
            strStatus = "FAIL"

        strLog = strHeader + \
                 'Min Leak Duaration$$' + ExpectedLeakDuration + ActualLeakDuartion

        context.reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

    def getRulesLog(self, oThermostatEP, strValidationType, strExpectedTemp, strRuleType, strExpectedRuleStatus):
        oThermostatEP.update()
        formattedRules = oThermostatEP.getHeatRule()
        boolStatus = 'PASS'
        strActualRules = []
        strRulesAvailable = ('TooHot', 'TooCold')
        # RuleNameList = sorted(formattedRules)



        if strRuleType.upper().find('HIGH') >= 0:
            strExpRuleName = strRulesAvailable[0]
        else:
            strExpRuleName = strRulesAvailable[1]

        if strExpRuleName in formattedRules:

            strActualRuleName = strExpRuleName
            strActualRuleName = '$$' + strActualRuleName

            strActualRules = formattedRules[strExpRuleName]
            intIndex = strActualRules.index("SendEmail")
            strActualRuleStatus = strActualRules[intIndex + 1]
            if strExpectedRuleStatus == strActualRuleStatus:
                strActualRuleStatus = '$$' + strActualRuleStatus
            else:
                strActualRuleStatus = '$$||' + strActualRuleStatus
                boolStatus = 'FAIL'

            strActualNotiTemp = strActualRules[0]
            print(strActualNotiTemp)
            if float(strActualNotiTemp) == float(strExpectedTemp):
                strActualNotiTemp = '$$' + strActualNotiTemp

            else:
                strActualNotiTemp = '$$||' + strActualNotiTemp
                boolStatus = 'FAIL'

        else:
            strActualRuleName = '$$' + 'No ' + strExpRuleName + ' rule set'
            boolStatus = 'FAIL'

        if boolStatus == 'PASS':
            strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-Rule Values" + "@@@"
            strActualNotiTemp = ''
            strActualRuleName = ''
            strActualRuleStatus = ''
        else:
            strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Rule Values" + "@@@"

        strLog = ''
        strTempCompLog = '$~Current Rule Temperature$$' + str(strExpectedTemp) + str(strActualNotiTemp)
        strLog = strHeader + \
                 'Current Rule name$$' + strExpRuleName + strActualRuleName + strTempCompLog + \
                 '$~Current Rule Status$$' + strExpectedRuleStatus + strActualRuleStatus

        return strLog, boolStatus
        #
        # print()

    def validateBanner(self, context):
        try:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating Product screen')
            bannerTextDict = {'LARGE FLOW': 'We detected High water usage at 7:34am in your home.'
                                            ' Have you recently used a large amount of water?',
                              'SMALL LEAK': 'We detected a Low water flow at 5:27am. Want us to help you find it?'}

            expectedBannerText = bannerTextDict[context.strNotification]
            context.leakSensorEP.fetch_Banner(context.strNotification)
            actualBannetText = context.leakSensorEP.bannerText
            expectedDict = {'Expected': {'Banner Text': expectedBannerText}}
            actualDict = {'Client': {'Banner Text': actualBannetText}}
            # Need to updare timing here
            # log, status = context.reporter.logCreation(actualDict, expectedDict)
            # context.reporter.ReportEvent('Banner Text validation at client', log, status, 'Center')

        except:
            context.reporter.ReportEvent('Exception', "Exception at function validateBanner {0}".format(
                traceback.format_exc().replace('File', '$~File')), 'FAIL')

    def load_trobleshootingScreen(self, context):
        try:

            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating troubleshooting screen')
            context.leakSensorEP.load_troubleshootingScreen(context.strNotification)

        except:
            context.reporter.ReportEvent('Exception', "Exception at function load_trobleshootingScreen {0}".format(
                traceback.format_exc().replace('File', '$~File')), 'FAIL')

    def troublshooting_navigation(self, context):
        try:

            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Navigating troubleshooting screen')
            expectedAnswers = []
            expectedQuestions = []
            responseString = ''
            for eachItem in context.navigationList:
                expectedAnswers.append(eachItem['answer'])
                expectedQuestions.append(eachItem['question'])
                responseString += '-' + eachItem['answer']
            context.reporter.ReportEvent('Responses to be', responseString[1:], 'Done',
                                         'Center')

            clientQuestions = context.leakSensorEP.troubleshootingNavigation(expectedAnswers, expectedQuestions)
            counter = 0
            expectedlist, actuallist = {}, {}
            for eachItem in context.navigationList:
                counter += 1
                expectedlist.update({'Question Text': eachItem['question'].replace("'", "").replace("'", ""),
                                     'Response': eachItem['answer']})
                actuallist.update(
                    {'Question Text': clientQuestions[counter - 1]['question'].replace("'", "").replace("'", ""),
                     'Response': eachItem['answer']})
                log, status = context.reporter.logCreation({'Client': actuallist}, {'Expected': expectedlist})
                context.reporter.ReportEvent('Question ' + str(counter) + ' Response ' + eachItem['answer'], log,
                                             status, 'Center')


        except:
            context.reporter.ReportEvent('Exception', "Exception at function troublshooting_navigation {0}".format(
                traceback.format_exc().replace('File', '$~File')), 'FAIL')

    def validate_plumberScreen(self, context):
        try:

            context.reporter.HTML_TC_BusFlowKeyword_Initialize('validating plumber screen')
            context.leakSensorEP.plumberScreen()

        except:
            context.reporter.ReportEvent('Exception', "Exception at function validate_plumberScreen {0}".format(
                traceback.format_exc().replace('File', '$~File')), 'FAIL')

    # Set thermostat mode and Temp
    def setThemostatModeAndTemp(self, context):

        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set ' + context.strOperatingMode + ' Mode')
        context.oNaThermostatEP.set_NAT_Mode(context.strThermostatTargetedChannel, context.strOperatingMode)

        if context.strTargetedTemp != '':
            context.oNaThermostatEP.set_NAT_Temp(context.strTargetedTemp)
            context.oNaThermostatEP.updateV6point5()
        else:
            context.oNaThermostatEP.updateV6point5()
            context.strExpectedTemp = context.oNaThermostatEP.occupiedHeatingSetpoint
        context.insideTemp = self.convertCelToFarnTemp(context.oNaThermostatEP.localTemperature)
        context.oNaThermostatEP.blnFlameIconAppearance = self.determineFlameIconAppearance(
            context.strThermostatTargetedChannel, context.insideTemp, context.strExpectedTemp)

        context.oNaThermostatEP.update_NAT_clientOperatingAttributes()
        if context.oNaThermostatEP.blnFlameIconAppearance == '':
            context.oNaThermostatEP.blnFlameIconAppearance = context.oNaThermostatEP.clientFlameIconApperance

    def determineFlameIconAppearance(self, strStatChannel, fltInsidetemp, fltExpectedTemp):

        if '--' in fltExpectedTemp:
            fltInsidetemp = float(fltInsidetemp)
            fltExpectedTempSplitted = fltExpectedTemp.split('--')
            fltMaxTemp = float(fltExpectedTempSplitted[0])
            fltminTemp = float(fltExpectedTempSplitted[1])

            if fltInsidetemp > fltMaxTemp:
                return 'COOL'
            elif fltInsidetemp < fltminTemp:
                return 'HEAT'
            elif (fltInsidetemp == fltMaxTemp) or (fltInsidetemp == fltminTemp):
                return ''
            else:
                return False

        else:
            absDiff = float(fltInsidetemp) - float(fltExpectedTemp)

            if "COOL" in strStatChannel and absDiff > 0:
                return True
            elif "HEAT" in strStatChannel and absDiff < 0:
                return True
            elif absDiff == 0:
                return ''
            else:
                return False

    def setThermostatSchedule(self, context):
        context.oNaThermostatEP.set_NAT_Mode(context.strThermostatTargetedChannel, context.strOperatingMode)
        context.oNaThermostatEP.set_NA_schedule(context)
        time.sleep(15)
        context.oNaThermostatEP.updateV6point5()
        context.WeeklyScheduleAfter = context.oNaThermostatEP._weeklySchedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating schedule for other days')
        oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, context.oSchedDict, context.WeeklyScheduleBefore,
                                                 context.WeeklyScheduleAfter)

    # Set thermostat mode
    def validateThemostatMode(self, context):
        context.oNaThermostatEP.updateV6point5()
        self.validateNATstatus(context, context.reporter, context.oNaThermostatEP, context.strOperatingMode,
                               context.strExpectedTemp, context.strThermostatTargetedChannel)

    # Validate NAT current status
    def validateNATstatus(self, context, reporter, oNaThermostatEP, strMode, strExpectedTemperature,
                          strExpectedStatChannel, intCheckDuration=60, intCheckTImeInterval=30, nextEventStartTime=None,
                          nextEventDay='Today'):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strMode + ' Mode')
        ############################The code needs to be updated, just put as temp since the temperature is not being set at the time of writing ##########################################

        if strMode.upper() == 'OFF':
            strText = ''
        else:
            strText = ' </B> Mode as ' + strMode + ' with Temperature as <B>' + str(
                strExpectedTemperature)

        reporter.ReportEvent('Client Validation',
                             'Validating <B>' + strMode + strText + ' and the flame/flake Icon', 'Done')

        ############################

        self.validateAndUpdateNALog(reporter, oNaThermostatEP, 'Client', strMode, strExpectedTemperature,
                                    strExpectedStatChannel)

        reporter.ReportEvent('Test Validation',
                             'Validating <B>' + strMode + strText + \
                             '</B> for every <B>' + str(
                                 intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(
                                 round(intCheckDuration / 60, 2)) + ' minute(s)', 'Done')
        # Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration / intCheckTImeInterval)):
            self.validateAndUpdateNALog(reporter, oNaThermostatEP, 'Test', strMode, strExpectedTemperature,
                                        strExpectedStatChannel)
            # Wait for the Check Time interval
            time.sleep(intCheckTImeInterval)
            if intCntr == int(intCheckDuration / intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration % intCheckTImeInterval)
            if not nextEventStartTime is None:
                if not oSchdUt.checkGuardTime(nextEventStartTime, nextEventDay): return

    def validateAndUpdateNALog(self, reporter, oNaThermostatEP, strValidationType, strExpectedMode,
                               strExpectedTemperature, strExpectedStatChannel):
        strLog, strStatus = self.getNALog(reporter, oNaThermostatEP, strValidationType, strExpectedMode,
                                          strExpectedTemperature, strExpectedStatChannel.upper())
        reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

    def getMaxMinTemp(self, strTemp):
        strTempSplit = strTemp.split('--')
        return strTempSplit[0], strTempSplit[1]

    def getNALog(self, reporter, oNaThermostatEP, strValidationType, strExpectedStatMode, strExpectedStatTemp,
                 strExpectedStatChannel):
        oNaThermostatEP.updateV6point5()
        boolStatus = True
        dictFlamePresence = {True: 'PRESENT', False: 'ABSENT', 'COOL': 'PRESENT-COOL', 'HEAT': 'PRESENT-HEAT', '': ''}

        if 'CLIENT' in strValidationType.upper():
            strActualStatMode = oNaThermostatEP.clientThermostatOperatingMode
            strActualStatTemp = oNaThermostatEP.clientCurrentTargetTemp
            strActualTSRunState = dictFlamePresence[oNaThermostatEP.clientFlameIconApperance]
            strExpectedTSRunState = dictFlamePresence[oNaThermostatEP.blnFlameIconAppearance]
            strActualStatChannel = oNaThermostatEP.statChannel.upper()
            strHeaderText = 'Flame/Flake ICON Presence'
            if strExpectedStatMode == "OFF" and strExpectedTSRunState != 'ABSENT':
                strExpectedTSRunState = 'ABSENT'
        else:
            strActualStatMode = oNaThermostatEP.mode
            strActualStatTemp = str(oNaThermostatEP.occupiedHeatingSetpoint)
            strActualTSRunState = oNaThermostatEP.thermostatRunningState
            strActualStatChannel = oNaThermostatEP.statChannel.upper()
            strHeaderText = 'Current Thermostat Running State'
            if strExpectedStatMode == "OFF":
                strExpectedTSRunState = "OFF"
            else:
                strExpectedTSRunState = "ON"
        if strExpectedStatMode == "OFF":
            strActualStatTemp = "NOT REQUIRED"
            strExpectedStatTemp = "NOT REQUIRED"
            strExpectedStatChannel = "NOT REQUIRED"
            strActualStatChannel = "NOT REQUIRED"

        if strActualStatMode == strExpectedStatMode:
            strActualStatMode = '$$' + strActualStatMode
        else:
            strActualStatMode = '$$||' + strActualStatMode
            boolStatus = False

        if strActualStatChannel == strExpectedStatChannel:
            strActualStatChannel = '$$' + strActualStatChannel
        else:
            strActualStatChannel = '$$||' + strActualStatChannel
            boolStatus = False

        if strActualStatTemp == strExpectedStatTemp:
            strActualStatTemp = '$$' + strActualStatTemp
        else:
            strActualStatTemp = '$$||' + strActualStatTemp
            boolStatus = False

        if strActualTSRunState == strExpectedTSRunState:
            strActualTSRunState = '$$' + strActualTSRunState
        else:
            strActualTSRunState = '$$||' + strActualTSRunState
            boolStatus = False

        if boolStatus:
            strHeader = "Attributes$$" + "Expected- " + strValidationType + "  and Actual-Thermostat Values" + "@@@"
            strActualStatMode = ''
            strActualStatTemp = ''
            strActualTSRunState = ''
            strActualStatChannel = ''
            strStatus = "PASS"
        else:
            strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Thermostat Values" + "@@@"
            strStatus = "FAIL"

        strLog = strHeader + \
                 'Current System mode$$' + strExpectedStatMode + strActualStatMode + '$~Current Setpoint Temperature$$' \
                 + strExpectedStatTemp + strActualStatTemp + \
                 '$~' + strHeaderText + '$$' + strExpectedTSRunState + strActualTSRunState + \
                 '$~Current Thermostat Running Channel$$' + strExpectedStatChannel + strActualStatChannel

        return strLog, strStatus

    def convertCelToFarnTemp(self, strCelTemp):
        if "--" in strCelTemp:
            strCelTempSplitted = strCelTemp.split('--')
            strCoolTargTemp = strCelTempSplitted[0]
            strCoolTargTemp = self.convertCelToFarnTemp(strCoolTargTemp)
            strHeatTargTemp = strCelTempSplitted[1]
            strHeatTargTemp = self.convertCelToFarnTemp(strHeatTargTemp)
            return strCoolTargTemp + '--' + strHeatTargTemp
        else:
            dblCel = float(strCelTemp)
            dblRoundedCel = self.roundCeltoCel(dblCel)
            return str(self.CelToFarh(dblRoundedCel))

    def roundCeltoCel(self, dblCel):
        if abs(dblCel - math.trunc(dblCel)) < 0.001 or abs(dblCel - math.trunc(dblCel) - 0.5) < 0.001:
            absdblC = dblCel
        else:
            dblFarh = self.CelToFarh(dblCel)
            absdblC = self.FarhToCel(dblFarh)
        return absdblC

    def CelToFarh(self, dblCel):
        return round(dblCel * 1.8 + 32)

    def FarhToCel(self, dblFarh):
        dblCel = (dblFarh - 32) * 5.0 / 9.0
        return round(dblCel * 2) / 2.0

    def callUtterance(self, oLightEP, strAlexa, strUtterance):
        alexaResponse = ''
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # os.system("say " + strAlexa)
            call(["espeak", strAlexa])
            time.sleep(0.5)
            os.system("say " + strUtterance)
            time.sleep(5)
            audio = r.listen(source)
            try:
                alexaResponse = r.recognize_google(audio)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        print(alexaResponse)
        print('\n\n\n')

        oLightEP.updateAlexaResponse(alexaResponse)

    def validateResponse(self, reporter, oLightEP, strExpectedResponse, strActualResponse):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate SmartHome Skill')
        reporter.ReportEvent('Test Validation', 'Validating SmartHome Skill Active Light Utterance', 'Done')
        self.validateAlexaLog(reporter, oLightEP, 'ALEXA', strExpectedResponse, strActualResponse)

    def validatePlugResponse(self, reporter, oLightEP, strExpectedResponse, strActualResponse):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate SmartHome Skill')
        reporter.ReportEvent('Test Validation', 'Validating SmartHome Skill Active Plug Utterance', 'Done')
        self.validateAlexaLog(reporter, oLightEP, 'ALEXA', strExpectedResponse, strActualResponse)

    def validateHeatingResponse(self, reporter, oThermostatEP, strExpectedResponse, strActualResponse):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate SmartHome Skill')
        reporter.ReportEvent('Test Validation', 'Validating SmartHome Skill Active Heating Utterance', 'Done')
        self.validateAlexaLog(reporter, oThermostatEP, 'ALEXA', strExpectedResponse, strActualResponse)

    def validateAlexaLog(self, reporter, oLightEP, strValidationType, strExpectedResponse, strActualResponse):
        strLog, strStatus = self.getAlexaLog(oLightEP, strValidationType, strExpectedResponse, strActualResponse)
        reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

    def getAlexaLog(self, oLightEP, strValidationType, strExpectedResponseDict, strActualResponse):
        boolStatus = 'PASS'
        strExpectedRespList = []
        strExpectedResp = ''
        for oKey in strExpectedResponseDict:
            print(strExpectedResponseDict[oKey])
            if strActualResponse.upper() == strExpectedResponseDict[oKey].upper():
                boolStatus = 'PASS'
                strExpectedResp = strExpectedResponseDict[oKey]
                break
            else:
                boolStatus = 'FAIL'

        if boolStatus == 'PASS':
            strActualResponse = '$$' + strActualResponse
        else:
            strActualResponse = '$$||' + strActualResponse
            strExpectedResp = strExpectedRespList

        for oKey in strExpectedResponseDict:
            strExpectedRespList.append(strExpectedResponseDict[oKey])

        if boolStatus == 'PASS':
            strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-Alexa Response" + "@@@"
            strActualResponse = ''
        else:
            strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Alexa Response" + "@@@"

        strLog = strHeader + \
                 '$~Current Alexa Response$$' + str(strExpectedResp) + str(strActualResponse)

        # print(strLog, boolStatus)
        # print('\n\n')
        return strLog, boolStatus

    def setMimic(self, context):
        try:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Setting up mimic')
            device = random.choice(list(context.devicesDict.keys()))
            strHeader = 'Light$$ Mimic Status@@@'
            for eachlight in context.targetlightsConfig:
                strHeader += eachlight + '$$' + context.targetlightsConfig[eachlight] + '$~'
            context.reporter.ReportEvent('Target Mimic Lights Matrics', strHeader[:-2], 'PASS', 'Center')
            if context.oMimicEP.navigateToLight(device):
                context.oMimicEP.setMimic(context.lstTargetTime, context.targetlightsConfig)
            else:
                context.reporter.ReportEvent('Test Validation', ' Light ' + device + ' could not be located', 'FAIL',
                                             'Center')
                context.reporter.ActionStatus = False
        except:
            context.reporter.ReportEvent('Exception', "Exception at function setMimic {0}".format(
                traceback.format_exc().replace('File', '$~File')), 'FAIL')

    def verifyMimic(self, context):
        try:
            deviceName = ''
            for eachlight in context.devicesDict.keys():
                if context.targetlightsConfig[eachlight] == 'true':
                    deviceName = eachlight
                    break
            context.oMimicEP.navigateToLight(deviceName)
            context.oMimicEP.getClientSelectedHours()
            context.oMimicEP.getClientSelectedCount()
            self.reportVerifyMimictLogs(context)
        except:
            context.reporter.ReportEvent('Exception', "Exception at function verifyMimic"
                                                      " {0}".format(traceback.format_exc().replace('File', '$~File')),
                                         'FAIL')

    def reportVerifyMimictLogs(self, context):
        try:
            expectedDict = {'Expected Values': {'Selected Start Time': context.lstTargetTime[0],
                                                'Selected End Time': context.lstTargetTime[1],
                                                'Selected Number of Devices': str(context.numberOfLights)}}

            actualDict = {'Client Values': {'Selected Start Time': context.oMimicEP.selectedHours.split(' to ')[0],
                                            'Selected End Time': context.oMimicEP.selectedHours.split(' to ')[1],
                                            'Selected Number of Devices': str(context.oMimicEP.selectedCount)}}

            log, status = context.reporter.logCreation(actualDict, expectedDict)
            context.reporter.ReportEvent('Test Validation at client', log, status, 'Center')

            actualDict = {'API Values': {'Selected Start Time': context.oMimicEP.selectedHoursPF[0],
                                         'Selected End Time': context.oMimicEP.selectedHoursPF[1],
                                         'Selected Number of Devices': str(context.oMimicEP.selectedCountPF)}}

            log, status = context.reporter.logCreation(actualDict, expectedDict)
            context.reporter.ReportEvent('Test Validation at platform', log, status, 'Center')
        except:
            context.reporter.ReportEvent('Exception', "Exception at function reportVerifyMimictLogs {0}".format
            (traceback.format_exc().replace('File', '$~File')), 'FAIL')

    def verifyLightMimicStatus(self, context):
        try:
            context.oMimicEP.updateMimic()
            self.verifyMimic(context)
            expectedMimicDict = context.oMimicLogic.updateMimicExpected(context)
            platformMimicDict = context.oMimicLogic.get_platform_dict(context.oMimicEP.devicesDict)
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Client Screenshot for each light')
            context.oMimicEP.getClientLightsStatus()
            clientMimicDict = {'Client Values': context.oMimicEP.clientDevicesStatus}
            for eachlight in expectedMimicDict['Target Values']:
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating Attribute for Light - ' + eachlight)
                expectedLightDict = expectedMimicDict['Target Values'][eachlight]
                clientLightDict = clientMimicDict['Client Values'][eachlight]
                log, status = context.oMimicLogic.logCreation(clientLightDict, expectedLightDict)
                context.reporter.ReportEvent('Client Validation', log, status, 'Center')
                expectedLightDict.pop('textStatus', None)
                platformLightDict = platformMimicDict['Platform Values'][eachlight]
                log, status = context.oMimicLogic.logCreation(platformLightDict, expectedLightDict)
                context.reporter.ReportEvent('Platform Validation', log, status, 'Center')
        except:
            context.reporter.ReportEvent('Exception', "Exception at function verifyLightMimicStatus {0}".format
            (traceback.format_exc().replace('File', '$~File')), 'FAIL')

    def reportverifyLightMimicStatusLogs(self, context):
        try:
            devicesStatus = context.oMimicEP.devicesDict
            clientDevicesStatus = context.oMimicEP.clientDevicesStatus
            dictMimic = {'true': 'ACTIVE', 'false': 'INACTIVE'}
            presenceDict = {'OFFLINE': 'ABSENT', 'ON': 'PRESENT', 'OFF': 'PRESENT'}
            actualDict = {}

            for eachDevice in context.expectedDict.keys():
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating Mimic Behaviour for - ' + eachDevice)
                # Add client validation for Icon and text
                if eachDevice in clientDevicesStatus.keys():
                    if clientDevicesStatus[eachDevice]['presence'] == 'OFFLINE':
                        actualDict = {'API Values': {'Presence': 'OFFLINE'}}
                    else:
                        actualDict = {'API Values': {'Mimic': clientDevicesStatus[eachDevice]['mimicStatus'],
                                                     'Device State': clientDevicesStatus[eachDevice]['IconStatus']}}
                    expectedDict = context.expectedDict[eachDevice]
                    log, status = context.reporter.logCreation(actualDict, expectedDict)
                    context.reporter.ReportEvent('Test Validation at Client', log, status, 'Center')
                else:
                    context.reporter.ReportEvent('Test Validation at Client', 'Device ' + eachDevice + 'not found',
                                                 'FAIL',
                                                 'Center')

                if eachDevice in devicesStatus.keys():
                    if devicesStatus[eachDevice]['deviceState'] == 'ABSENT':
                        actualDict = {'API Values': {'Presence': 'OFFLINE'}}
                    else:
                        actualDict = {'API Values': {'Mimic': dictMimic[devicesStatus[eachDevice]['mimic']],
                                                     'Device State': devicesStatus[eachDevice]['deviceState']}}
                    expectedDict = context.expectedDict[eachDevice]
                    log, status = context.reporter.logCreation(actualDict, expectedDict)
                    context.reporter.ReportEvent('Test Validation at platform', log, status, 'Center')
                else:
                    context.reporter.ReportEvent('Test Validation at platform', 'Device ' + eachDevice + 'not found',
                                                 'FAIL', 'Center')
        except:
            context.reporter.ReportEvent('Exception',
                                         "Exception at function reportverifyLightMimicStatusLogs {0}".format
                                         (traceback.format_exc().replace('File', '$~File')), 'FAIL')

    def updateLights(self, context):
        try:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                'Mode and State for lights are updated and acheived as listed in the table below')
            lights = context.targetlightsState
            strHeader = 'Light$$ Mode $$ State@@@'
            for eachlight in lights:
                if context.targetlightsState[eachlight] != context.oMimicEP.devicesDict[eachlight]['deviceState'] \
                        or context.targetlightsMode[eachlight] != context.oMimicEP.devicesDict[eachlight]['deviceMode']:
                    context.oMimicEP.updateLightState(context.oMimicEP.devicePositionDict[eachlight],
                                                      context.targetlightsState[eachlight], eachlight,
                                                      context.targetlightsMode[eachlight])
                strHeader += eachlight + '$$' + context.targetlightsMode[eachlight] + '$$' + context.targetlightsState[
                    eachlight] \
                             + '$~'
            context.reporter.ReportEvent('Final Status', strHeader[:-2], 'PASS', 'Center')
        except:
            context.reporter.ReportEvent('Exception', "Exception at function updateLights {0}".format
            (traceback.format_exc().replace('File', '$~File')), 'FAIL')


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
    intBrightness = 0
    syntheticNodeID = getSyntheticDeviceID(nodeID)
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            strState = getAttribute(oNode["attributes"], "state")
            if 'brightness' in oNode["attributes"]:
                intBrightness = int(getAttribute(oNode["attributes"], "brightness"))
        elif oNode["id"] in syntheticNodeID:
            oJson = oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
            if isinstance(oJson, str): oJson = json.loads(oJson)
            if oJson["enabled"]:
                strMode = "AUTO"
            else:
                strMode = "MANUAL"
                # oNode["attributes"]
    return strMode, strState, intBrightness

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


def getLightAttributes(deviceType):
    currentDeviceNodeId = pUtils.getDeviceNodeID(deviceType)
    print(currentDeviceNodeId)
    mode, currentDeviceState, activeLightBrightness = pUtils.getLightAttributes(currentDeviceNodeId)
    return mode, currentDeviceState, activeLightBrightness


