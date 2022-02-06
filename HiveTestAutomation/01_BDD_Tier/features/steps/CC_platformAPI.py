"""
Created on 12 Jun 2015

@author: ranganathan.veluswamy

@author: : Hitesh Sharma - 15 July 2016
@note: created function setLowNotification and setHighNotification to add logic for iOS to set the heating notifications
@note: 10 Aug 2016 - Added function navigatetoContactSensor and currentCSStatus to navigate to contact sensor screen and get the current status for given CS status resp
"""
import json
import time
import random
import traceback
import DD_Page_AndroidApp as androidPage
import DD_Page_WebApp as webPage
import DD_Page_iOSApp as iOSPage
import FF_alertmeApi as ALAPI
import FF_Beekeeper as ALBKP
import FF_Platform_Utils as pUtils
import FF_utils as utils
from random import randint
from datetime import datetime, timedelta
import math
import FF_ScheduleUtils as oSchdUtil
import FF_timeZone as TZ


class platformAPIClass(object):
    def __init__(self, strServerName):
        self.AndroidDriver = None
        self.WebDriver = None
        self.iOSDriver = None
        self.reporter = None
        self.heatEP = thermostatEndpoint(self, strServerName, 'HEAT')
        self.waterEP = thermostatEndpoint(self, strServerName, 'WATER')
        self.sensorEP = thermostatEndpoint(self, strServerName, 'SENSOR')
        self.plugEP = thermostatEndpoint(self, strServerName, 'PLUG')
        self.holidayEP = thermostatEndpoint(self, strServerName, 'HOLIDAY')
        self.beekeeperEP = thermostatEndpoint(self, strServerName, 'BEEKEEPER')
        self.warmWhiteLightEP = lightEndPoint(self, strServerName, 'WARMWHITELIGHT')
        self.tuneableLightEP = lightEndPoint(self, strServerName, 'TUNEABLELIGHT')
        self.colourLightEP = lightEndPoint(self, strServerName, 'COLOURLIGHT')
        self.motionSensorEP = sensorEndPoint(self, strServerName, 'MOTIONSENSOR')
        self.contactSensorEP = sensorEndPoint(self, strServerName, 'CONTACTSENSOR')
        self.naThermostatEP = naThermostatEndpoint(self, strServerName)
        self.leakSensorEP = leakSensorEndPoint(self, strServerName)
        self.mimicEP = mimicEndPoint(self, strServerName)
        self.ActionsEP = Actions(self, strServerName)
        return

    def update(self):
        """
        """
        self.heatEP.update()
        self.waterEP.update()
        self.plugEP.update()
        self.holidayEP.update()

        return 0

    def beeUpdate(self, context):
        self.beekeeperEP.beeUpdate(context)
        self.beekeeperEP.makeRequest()
        self.warmWhiteLightEP.update()
        return 0


class thermostatEndpoint(object):
    def __init__(self, platAPI, strServerName, epType):
        # Parent Tstat
        self.parentAPI = platAPI
        self.type = epType
        self.serverName = strServerName
        self.client = None
        self.mode = None
        self.localTemperature = 0.0
        self.occupiedHeatingSetpoint = 0.0
        self.thermostatRunningState = ''
        self._weeklySchedule = {}
        self.AndroidDriver = platAPI.AndroidDriver
        self.WebDriver = platAPI.WebDriver
        self.iOSDriver = platAPI.iOSDriver
        self.reporter = platAPI.reporter
        self.Web_ManualModeTargTemp = 20.0
        self.platformVersion = None
        self.occupiedHeatingSetpointChanged = False

        self.deviceType = ""
        self.currentDeviceNodeId = ""
        self.currentDeviceSDNodeId = ""
        self.CurrentDeviceState = ""
        self.activeLightBrightness = 0

        self.HolidayStartTime = ''
        self.HolidayEndTime = ''

        # Variables for Beekeeper to compare against API
        # User Variables
        self.BEEsession = ''
        self.BeeUsername = ''
        self.BeeUserid = ''

        self.BeeFirstName = ''
        self.BeeLastName = ''
        self.BeePostcode = ''
        self.BeeEmail = ''
        self.BeeMobile = ''
        self.BeePhone = ''
        self.BeeTimeZone = ''
        self.BeeCountry = ''
        self.BeeCountryCode = ''
        self.BeeLocale = ''
        self.BeeTemperatureUnit = ''
        # self.BeeStatus = ''
        self.BeeFailuresEmail = False
        self.BeeFailuresSMS = False
        self.BeeWarningsEmail = False
        self.BeeWarningsSMS = False
        self.BeeNightAlerts = False

        # Product Variables
        self.BeeProductID = ''
        self.BeeProductType = ''
        self.BeeParentNodeID = ''
        self.BeePresenceStatus = ''
        self.BeeDeviceModel = ''
        self.BeeDeviceVersion = ''
        self.BeeProdStatus = ''
        self.BeeDeviceManufacturer = ''
        # Need to check for capabilities
        # Holiday mode
        self.BeeHolidayEnabled = False
        self.BEEHolidayStart = ''
        self.BeeHolidayEnd = ''
        self.BeeHolidayTemp = ''
        self.BeeMaxEvents = ''
        self.BeePMZ = ''
        # previous
        self.BeePreviousMode = ''

        self.BeeScheduleOverride = False
        self.BeeInsidetemperature = 0.0
        self.BeeZoneid = ''
        # state
        self.BeeZoneName = ''
        self.BeeBoost = ''
        self.BeeFrostProtection = ''
        self.BeeDeviceMode = ''

        # Schedule to be done here
        self.BeeTargTemp = None
        self.BeeSchedule = ''

        self.BeeHeatingID = ''

        self.BeeTypeCount = 0
        self.oTypeList1Count = 0
        self.BeeAllProductsDict = {}

        # Variables for Beekeeper to compare against API
        self.APIsession = ''
        self.APIUsername = ''
        self.APIUserid = ''

        self.APIFirstName = ''
        self.APILastName = ''
        self.APIPostcode = ''
        self.APIEmail = ''
        self.APIMobile = ''
        self.APIPhone = ''
        self.APITimeZone = ''
        self.APICountry = ''
        self.APICountryCode = ''
        self.APILocale = ''
        self.APITemperatureUnit = ''
        # self.APIStatus = ''
        self.APIFailuresEmail = False
        self.APIFailuresSMS = False
        self.APIWarningsEmail = False
        self.APIWarningsSMS = False
        self.APINightAlerts = False

        # Product Variables
        self.APIProductID = ''
        self.APIProductType = ''
        self.APIParentNodeID = ''
        self.APIPresenceStatus = ''
        self.APIDeviceModel = ''
        self.APIDeviceVersion = ''
        self.APIProdStatus = ''
        self.APIDeviceManufacturer = ''
        # Need to check for capabilities
        # Holiday mode
        self.APIHolidayEnabled = False
        self.APIHolidayStart = ''
        self.APIHolidayEnd = ''
        self.APIHolidayTemp = ''
        self.APIMaxEvents = ''
        self.APIPMZ = ''
        # previous
        self.APIPreviousMode = ''

        self.APIScheduleOverride = False
        self.APIInsidetemperature = 0.0
        self.APIZoneid = ''
        # state
        self.APIZoneName = ''
        self.APIBoost = ''
        self.APIFrostProtection = ''
        self.APIDeviceMode = ''

        # Schedule to be done here
        self.APITargTemp = None
        self.BeeSchedule = ''
        self.APIHeatingID = ''
        self.oSetList = []
        self.oAllProdDictAPI = {}
        self.oAllProdDictBEE = {}
        self.oAllContacsAPI = {}
        self.oAllContacsBEE = {}
        self.oAllContactsDict = {}
        self.HolidayModeDictBEE = {}
        self.HolidayModeDictAPI = {}
        self.deviceName = None

        # Common for both
        self.nodeTypeDict = {'hub': 'class.hub',
                             'boilermodule': 'class.thermostat.json',
                             'thermostatui': 'class.thermostatui.json',
                             'activeplug': 'class.smartplug.json',
                             'contactsensor': 'class.contact.sensor',
                             'motionsensor': 'class.motion.sensor',
                             'warmwhitelight': 'class.light.json',
                             'tuneablelight': 'class.tunable.light.json',
                             'colourtuneablelight': 'class.colour.tunable.light.json',
                             'signalbooster': 'class.zigbee.range.extender',
                             'smartplug': 'class.smartplug.json'
                             }

    def update(self):
        self.AndroidDriver = self.parentAPI.AndroidDriver
        self.WebDriver = self.parentAPI.WebDriver
        self.iOSDriver = self.parentAPI.iOSDriver
        self.reporter = self.parentAPI.reporter
        if self.platformVersion == 'V5':
            self._updateV5()
        else:
            if not self._updateV6():
                self._updateV5()

                # adding for alexa

    def updateAlexaResponse(self, resp):
        self.alexaResponse = resp

    def update_attributes_from_client(self):
        self.getAttributesFromClient()

    def _updateV6(self, nodeID=None):
        # Updating attributes for Light
        print("self.deviceType.upper()", self.deviceType.upper())
        if "FWBULB" in self.deviceType.upper():
            self.currentDeviceNodeId = pUtils.getDeviceNodeID(self.deviceType)
            self.mode, self.CurrentDeviceState, self.activeLightBrightness, self.activeLightTone = pUtils.getLightAttributes(
                self.currentDeviceNodeId)
            self._weeklySchedule = pUtils.getDeviceScheduleInStandardFormat(self.deviceType)
            print(self._weeklySchedule)
            return True

        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        if session.latestSupportedApiVersion != '6':
            self.platformVersion = 'V5'
            print("V5")
            return False
        else:
            self.platformVersion = 'V6'

            resp = ALAPI.getNodesV6(session)
            if self.type == 'HEAT':
                boolWater = False
            else:
                boolWater = True

            # If loop and content added - Holiday mode changes:
            if self.type == 'HOLIDAY':
                for oNode in resp['nodes']:
                    # if not nodeID is None:
                    #    if not oNode['parentNodeId'] == nodeID: continue
                    if 'http://alertme.com/schema/json/node.class.thermostat.json#' in oNode['nodeType'] and \
                            not 'supportsHotWater' in oNode['attributes']:
                        # if 'enabled' in oNode['holidayMode']['reportedValue']:
                        print('Holiday mode test')
                        oAttributeList = oNode['attributes']
                        oJson = self.getAttribute(oAttributeList, 'holidayMode')
                        if isinstance(oJson, str): oJson = json.loads(oJson)
                        boolHolidayMode = oJson['enabled']
                        self.occupiedHeatingSetpoint = float('{:.1f}'.format(oJson['targetHeatTemperature']))
                        if boolHolidayMode:
                            print('User is in Holiday mode now')
                            self.mode = 'HOLIDAY'
                        else:
                            print('User has not activated the holiday mode holiday mode')

                            self.HolidayStartTime = oJson['startDateTime']
                        self.HolidayEndTime = oJson['endDateTime']
                        print(boolHolidayMode, self.occupiedHeatingSetpoint, self.HolidayStartTime, self.HolidayEndTime)

                        # struct_time = time.strptime("30 Nov 00", "%d %b %y")
                        # print ("returned tuple: %s " % struct_time)

                        # STRING TO BE CONVERTED INTO PROPER TIME FOR THIS PROJECT


            # If loop and content added - active plug changes:
            elif self.type == 'PLUG':
                plugNodID = None
                strRunningState = ''
                for oNod in resp['nodes']:
                    if 'nodeType' in oNod:
                        if 'http://alertme.com/schema/json/node.class.smartplug.json#' in oNod['nodeType']:
                            # if 'model' in oNod:
                            #    if 'SLP2' in oNod['model']:
                            if self.deviceName is None or self.deviceName in oNod['name']:
                                plugNodID = oNod['id']
                                oPlugAttributeList = oNod['attributes']
                                strRunningState = self.getAttribute(oPlugAttributeList, 'state')
                                self.deviceName = oNod['name']
                                break
                if strRunningState == 'OFF':
                    self.thermostatRunningState = '0000'
                else:
                    self.thermostatRunningState = '0001'
                plugNodeID = '["' + plugNodID + '"]'
                for oNode in resp['nodes']:
                    if not nodeID is None:
                        # Or we can do the loop by checking directly if consumers attribute is available, then get into the loop and do furthur checks
                        # if 'synthetic.binary.control.device.uniform.scheduler' in oNode['nodeType']:
                        if not oNode['attributes']['consumers']['reportedValue'] == nodeID: continue
                    # if oNode['attributes']['consumers']['reportedValue'] == nodeID:
                    if 'syntheticDeviceConfiguration' in oNode['attributes'] and \
                                    'http://alertme.com/schema/json/node.class.synthetic.binary.control.device.uniform.scheduler.json' in \
                                    oNode['nodeType']:
                        if oNode['attributes']['consumers']['reportedValue'] == plugNodeID:
                            if boolWater:
                                print('plug')
                                oAttributeList = oNode['attributes']
                                oJson = self.getAttribute(oAttributeList, 'syntheticDeviceConfiguration')
                                if isinstance(oJson, str): oJson = json.loads(oJson)
                                strActivePlugMode = oJson['enabled']
                                self._weeklySchedule = self._formatScheduleV6insideSD(oJson)
                                if strActivePlugMode:
                                    self.mode = 'AUTO'
                                elif not strActivePlugMode:
                                    self.mode = 'MANUAL'

            # Else loop added - for heating and hotwater validations:
            else:

                for oNode in resp['nodes']:
                    if not nodeID is None:
                        if not oNode['parentNodeId'] == nodeID: continue
                    if 'supportsHotWater' in oNode['attributes']:
                        if oNode['attributes']['supportsHotWater']['reportedValue'] == True and 'stateHotWaterRelay' in \
                                oNode['attributes']:
                            if boolWater:
                                print("water")
                                oAttributeList = oNode['attributes']
                                # oJson = oAttributeList['schedule']['reportedValue']
                                oJson = self.getAttribute(oAttributeList, 'schedule')
                                if isinstance(oJson, str): oJson = json.loads(oJson)
                                self._weeklySchedule = self._formatScheduleV6(oJson)
                                # print('%%%%%%%%%%%^^^^^^^^^^^^^^^^^', oJson)
                                strRunningState = self.getAttribute(oAttributeList, 'stateHotWaterRelay')
                                if strRunningState == 'OFF':
                                    self.thermostatRunningState = '0000'
                                else:
                                    self.thermostatRunningState = '0001'

                                strActiveHeatCoolMode = self.getAttribute(oAttributeList, 'activeHeatCoolMode')
                                boolActiveScheduleLock = self.getAttribute(oAttributeList, 'activeScheduleLock')
                                lstActiveOverrides = self.getAttribute(oAttributeList, 'activeOverrides')

                                if len(lstActiveOverrides) > 0 and lstActiveOverrides == '["TARGET_HEAT_TEMPERATURE"]':
                                    self.mode = 'OVERRIDE'
                                elif strActiveHeatCoolMode == 'OFF':
                                    self.mode = 'OFF'
                                elif strActiveHeatCoolMode == 'HEAT' and boolActiveScheduleLock:
                                    self.mode = 'MANUAL'
                                elif strActiveHeatCoolMode == 'HEAT' and not boolActiveScheduleLock:
                                    self.mode = 'AUTO'
                                elif strActiveHeatCoolMode == 'BOOST':
                                    self.mode = 'BOOST'
                                '''
                                print(self._weeklySchedule)
                                print(self.mode)
                                print(self.thermostatRunningState)
                                '''
                        else:
                            if not boolWater and 'stateHeatingRelay' in oNode['attributes']:
                                print('Heat')
                                oAttributeList = oNode['attributes']
                                # oJson = oAttributeList['schedule']['reportedValue']
                                oJson = self.getAttribute(oAttributeList, 'schedule')
                                if isinstance(oJson, str): oJson = json.loads(oJson)
                                self._weeklySchedule = self._formatScheduleV6(oJson)
                                strRunningState = self.getAttribute(oAttributeList, 'stateHeatingRelay')
                                if strRunningState == 'OFF':
                                    self.thermostatRunningState = '0000'
                                else:
                                    self.thermostatRunningState = '0001'
                                if self.occupiedHeatingSetpointChanged: occupiedHeatingSetpoint = self.getAttribute(
                                    oAttributeList, 'targetHeatTemperature')
                                self.occupiedHeatingSetpoint = float(
                                    '{:.1f}'.format(oAttributeList['targetHeatTemperature']['reportedValue']))

                                self.localTemperature = self.getAttribute(oAttributeList, 'temperature')

                                strActiveHeatCoolMode = self.getAttribute(oAttributeList, 'activeHeatCoolMode')
                                boolActiveScheduleLock = self.getAttribute(oAttributeList, 'activeScheduleLock')
                                lstActiveOverrides = self.getAttribute(oAttributeList, 'activeOverrides')

                                if len(lstActiveOverrides) > 0 and lstActiveOverrides == '["TARGET_HEAT_TEMPERATURE"]':
                                    if strActiveHeatCoolMode == 'BOOST':
                                        self.mode = 'BOOST'
                                    else:
                                        self.mode = 'OVERRIDE'
                                elif strActiveHeatCoolMode == 'OFF':
                                    self.mode = 'OFF'
                                elif strActiveHeatCoolMode == 'HEAT' and boolActiveScheduleLock:
                                    self.mode = 'MANUAL'
                                elif strActiveHeatCoolMode == 'HEAT' and not boolActiveScheduleLock:
                                    self.mode = 'AUTO'
                                elif strActiveHeatCoolMode == 'BOOST':
                                    self.mode = 'BOOST'

                                '''
                                print(self._weeklySchedule)
                                print(self.mode)
                                print(self.occupiedHeatingSetpoint)
                                print(self.thermostatRunningState)
                                print(self.localTemperature)
                                '''

            ALAPI.deleteSessionV6(session)
            return True

    def getAttribute(self, oAttributeList, strAttributeName):
        reported = oAttributeList[strAttributeName]['reportedValue']
        if 'targetValue' in oAttributeList[strAttributeName]:
            target = oAttributeList[strAttributeName]['targetValue']
            targetTime = oAttributeList[strAttributeName]['targetSetTime']
            currentTime = int(time.time() * 1000)
            if (currentTime - targetTime) < 20000:
                print('taken target value for', strAttributeName)
                return target
        return reported

    # Gets the attributes from SD (from the API) for Plug
    # strNeededAttribute is an attribute we are going to fetch from the SD
    def getAttributeFromSyntheticDevice(self, oAttributeList, strAttributeName, strNeededName):
        reported = oAttributeList['reportedValue'][strAttributeName]
        if 'targetValue' in oAttributeList:
            target = oAttributeList['targetValue'][strAttributeName]
            targetTime = oAttributeList['targetSetTime']
            currentTime = int(time.time() * 1000)
            if (currentTime - targetTime) < 20000:
                print('taken target value for', strNeededName)
                return target
        return reported

    def getAttributeFromSyntheticDeviceForSchedule(self, oScheduleList, strAttributeName):
        reported = oScheduleList['reportedValue']['schedule']
        if 'targetValue' in oScheduleList:
            target = oScheduleList['targetValue']['schedule']
            targetTime = oScheduleList[strAttributeName]['targetSetTime']
            currentTime = int(time.time() * 1000)
            if (currentTime - targetTime) < 20000:
                print('taken target value for', 'schedule')
                return target
        return reported

    def _updateV5(self):
        # print('update start ', datetime.today().strftime("%H:%M:%S" ))
        # Login and get HubID
        ALAPI.createCredentials(self.serverName, self.client)
        resp = ALAPI.login()
        strHubID = resp[1]
        # Get the Device ID
        resp = ALAPI.getDevices(ALAPI.API_CREDENTIALS.apiUsername, strHubID)
        respList = resp[0]
        for oDevice in respList:
            if oDevice['name'] == 'Your Receiver':
                strBMDeviceID = oDevice['id']

        # Create Myaccount Class
        myAccount = ALAPI.accountClass(ALAPI.API_CREDENTIALS.apiUsername)

        if self.type == 'HEAT':
            # Get Heat Schedule
            resp = ALAPI.getHeatSchedule(myAccount, strBMDeviceID)
            respDict = resp[0]
            self._weeklySchedule = self._formatSchedule(respDict)

            # Get Target Temperature
            resp = ALAPI.getTargetTemperature(ALAPI.API_CREDENTIALS.apiUsername)
            respDict = resp[0]
            if 'temperature' in respDict: self.occupiedHeatingSetpoint = respDict['temperature']

            # Get Heat Running State
            resp = ALAPI.getHeatDetails(ALAPI.API_CREDENTIALS.apiUsername)
            respDict = resp[0]
            if 'active' in respDict:
                boolRunningState = respDict['active']
            if not boolRunningState:
                self.thermostatRunningState = '0000'
            else:
                self.thermostatRunningState = '0001'

            # Get Local Temperature
            resp = ALAPI.getLocalTemperature(ALAPI.API_CREDENTIALS.apiUsername)
            respDict = resp[0]
            if 'inside' in respDict:
                self.localTemperature = respDict['inside']['now']

            # Get Heat Mode
            resp = ALAPI.getHeatModeNew(ALAPI.API_CREDENTIALS.apiUsername)
            respDict = resp[0]
            if 'control' in respDict:
                self.mode = respDict['control']
                if self.mode == 'SCHEDULE': self.mode = 'AUTO'

        elif self.type == 'WATER':
            # Get Water Schedule
            resp = ALAPI.getHotWaterSchedule(ALAPI.API_CREDENTIALS.apiUsername, strHubID, strBMDeviceID)
            respDict = resp[0]
            self._weeklySchedule = self._formatSchedule(respDict)

            resp = ALAPI.getHotWaterModeAndRunState(ALAPI.API_CREDENTIALS.apiUsername, strBMDeviceID)
            respDict = resp[0]
            if 'control' in respDict:
                self.mode = respDict['control']
                if self.mode == 'SCHEDULE': self.mode = 'AUTO'
            if 'onOffState' in respDict:
                self.thermostatRunningState = respDict['onOffState']
            if self.thermostatRunningState == 'OFF':
                self.thermostatRunningState = '0000'
            else:
                self.thermostatRunningState = '0001'
            if 'targetTemperature' in respDict:
                self.occupiedHeatingSetpoint = respDict['targetTemperature']
            if 'currentTemperature' in respDict:
                self.localTemperature = respDict['currentTemperature']


                # print('update stop ', datetime.today().strftime("%H:%M:%S" ))

    def _formatScheduleV6(self, respDict):
        oSchedDict = {}
        oNewSchedDict = {}

        for oDay in respDict.keys():
            oSchedList = []
            oEventList = respDict[oDay]
            for oEvent in oEventList:
                intHour = int(oEvent['time'].split(':')[0])
                intMin = int(oEvent['time'].split(':')[1])
                oSchedList.append(('{:02d}:{:02d}'.format(intHour, intMin), oEvent['targetHeatTemperature']))
            oSchedDict.update({oDay: oSchedList})

        if 'weekdays' in oSchedDict:
            oNewSchedDict['mon'] = oSchedDict['weekdays']
            oNewSchedDict['tue'] = oSchedDict['weekdays']
            oNewSchedDict['wed'] = oSchedDict['weekdays']
            oNewSchedDict['thu'] = oSchedDict['weekdays']
            oNewSchedDict['fri'] = oSchedDict['weekdays']
        else:
            oNewSchedDict['mon'] = oSchedDict['monday']
            oNewSchedDict['tue'] = oSchedDict['tuesday']
            oNewSchedDict['wed'] = oSchedDict['wednesday']
            oNewSchedDict['thu'] = oSchedDict['thursday']
            oNewSchedDict['fri'] = oSchedDict['friday']

        if 'weekend' in oSchedDict:
            oNewSchedDict['sat'] = oSchedDict['weekend']
            oNewSchedDict['sun'] = oSchedDict['weekend']
        elif 'weekends' in oSchedDict:
            oNewSchedDict['sat'] = oSchedDict['weekends']
            oNewSchedDict['sun'] = oSchedDict['weekends']
        else:
            oNewSchedDict['sat'] = oSchedDict['saturday']
            oNewSchedDict['sun'] = oSchedDict['sunday']

        return oNewSchedDict

    # Formatting the schedule as per our need from the SD
    def _formatScheduleV6insideSD(self, respDict):
        oSchedDict = {}
        oNewSchedDict = {}
        # oAttributesInsideTheDict = respDict.keys()

        for oDay in respDict['schedule']:
            oSchedList = []
            if 'dayIndex' and 'transitions' in oDay:
                for oEvent in oDay['transitions']:
                    intHour = int(oEvent['time'].split(':')[0])
                    intMin = int(oEvent['time'].split(':')[1])
                    oSchedList.append(('{:02d}:{:02d}'.format(intHour, intMin), oEvent['action']['state']))
                oDayIndex = "dayIndex:%d" % oDay['dayIndex']
                oSchedDict.update({oDayIndex: oSchedList})

        if 'dayIndex:1' in oSchedDict:
            oNewSchedDict['mon'] = oSchedDict['dayIndex:1']
            oNewSchedDict['tue'] = oSchedDict['dayIndex:2']
            oNewSchedDict['wed'] = oSchedDict['dayIndex:3']
            oNewSchedDict['thu'] = oSchedDict['dayIndex:4']
            oNewSchedDict['fri'] = oSchedDict['dayIndex:5']
            oNewSchedDict['sat'] = oSchedDict['dayIndex:6']
            oNewSchedDict['sun'] = oSchedDict['dayIndex:7']

        return oNewSchedDict

    # Formating the schedule dictionary as per Schedule dictionary used for Zigbee
    def _formatSchedule(self, respDict):
        oSchedDict = {}
        oNewSchedDict = {}
        if 'days' in respDict:
            for oDay in respDict['days'].keys():
                oSchedList = []
                for eventDict in respDict['days'][oDay]:
                    oSchedList.append((eventDict['time'], eventDict['temperature']))
                oSchedDict.update({oDay: oSchedList})

        if 'weekdays' in oSchedDict:
            oNewSchedDict['mon'] = oSchedDict['weekdays']
            oNewSchedDict['tue'] = oSchedDict['weekdays']
            oNewSchedDict['wed'] = oSchedDict['weekdays']
            oNewSchedDict['thu'] = oSchedDict['weekdays']
            oNewSchedDict['fri'] = oSchedDict['weekdays']
        else:
            oNewSchedDict['mon'] = oSchedDict['monday']
            oNewSchedDict['tue'] = oSchedDict['tuesday']
            oNewSchedDict['wed'] = oSchedDict['wednesday']
            oNewSchedDict['thu'] = oSchedDict['thursday']
            oNewSchedDict['fri'] = oSchedDict['friday']

        if 'weekend' in oSchedDict:
            oNewSchedDict['sat'] = oSchedDict['weekend']
            oNewSchedDict['sun'] = oSchedDict['weekend']
        else:
            oNewSchedDict['sat'] = oSchedDict['saturday']
            oNewSchedDict['sun'] = oSchedDict['sunday']

        return oNewSchedDict

    # Upgrade Firmware for the give device type
    def upgradeFirware(self, DeviceType, fwTargetVersion):
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(session)
        nodeIdList = self.getNodeID(resp)
        if DeviceType in nodeIdList:
            nodeId = nodeIdList[DeviceType]
            ALAPI.firmwareUpgrade(session, nodeId, fwTargetVersion)
        else:
            print("Unable to Fetch Node ID for the Given Device Type: " + DeviceType)
        ALAPI.deleteSessionV6(session)

    # Get the Node ID for the given device type
    def getNodeID(self, resp):
        oDeviceNodes = {}
        for oNode in resp['nodes']:
            if not ('supportsHotWater' or 'consumers' or 'producers') in oNode['attributes']:
                if 'nodeType' in oNode.keys():
                    if 'thermostatui.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif 'thermostat.json' in oNode["nodeType"]:
                        if 'reportedValue' not in oNode["attributes"]["model"]:
                            strModel = 'SLR2'
                        else:
                            strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif 'hub.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif 'smartplug.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif 'extender.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif '.light.json' in oNode["nodeType"]:  # LDS_DimmerLight
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif 'contact.sensor.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif 'motion.sensor.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif 'connected.boiler.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]

        return oDeviceNodes

    # Get the FirmwareVersion for the given device type
    def getFWversion(self):
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(session)
        oDeviceVersion = {}
        for oNode in resp['nodes']:
            if not 'supportsHotWater' in oNode['attributes']:
                if 'nodeType' in oNode.keys():
                    if 'thermostatui.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'thermostat.json' in oNode["nodeType"]:
                        if 'reportedValue' not in oNode["attributes"]["model"]:
                            strModel = 'SLR2'
                        else:
                            strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'hub.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'smartplug.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'extender.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'light.json' in oNode["nodeType"]:  # LDS_DimmerLight
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'contact.sensor.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'motion.sensor.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'connected.boiler.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
        ALAPI.deleteSessionV6(session)
        return oDeviceVersion

        # Fetch and Verify staus of devices

    def verifyStatus(self):

        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(session)
        strDeviceState = ""
        strDevice = ""
        strDeviceName = ""
        blnFlag = False

        listDevice = []

        for oNode in resp['nodes']:
            try:
                if 'nodeType' in oNode.keys() and not 'synthetic.rule' in oNode['name']:

                    strDeviceName = oNode['name']
                    if oNode["attributes"] is not None:

                        if 'smartplug.json' in oNode["nodeType"]:

                            strDeviceState = oNode["attributes"]["presence"]["reportedValue"]

                            if strDeviceState.upper() == 'ABSENT':
                                strDeviceState = "offline"
                            else:
                                strDeviceState = oNode["attributes"]["state"]["reportedValue"]

                            strDevice = "active Plug"
                            blnFlag = True
                        elif 'light.json' in oNode["nodeType"]:  # LDS_DimmerLight


                            strDeviceState = oNode["attributes"]["presence"]["reportedValue"]

                            if strDeviceState.upper() == 'ABSENT':
                                strDeviceState = "offline"
                            else:
                                strDeviceState = oNode["attributes"]["state"]["reportedValue"]

                            if 'tunable.light' in oNode["nodeType"]:
                                strDevice = "tunable light"
                            elif 'class.light.' in oNode["nodeType"]:
                                strDevice = "Warm White Light"
                            else:
                                strDevice = "Colour Light"
                            blnFlag = True
                        elif 'motion.sensor.json' in oNode["nodeType"]:

                            strDevice = "motion sensor"
                            if oNode["attributes"]["presence"]["reportedValue"] == 'ABSENT':
                                strDeviceState = "offline"
                            else:
                                blnDeviceState = oNode["attributes"]["inMotion"]["reportedValue"]
                                if not blnDeviceState:
                                    strDeviceState = "not detecting motion."
                                else:
                                    strDeviceState = "detecting motion."
                            blnFlag = True
                        elif 'contact.sensor.json' in oNode["nodeType"]:

                            strDevice = "window or door sensor"

                            if oNode["attributes"]["presence"]["reportedValue"] == 'ABSENT':
                                strDeviceState = "offline"
                            else:
                                if oNode["attributes"]["state"]["reportedValue"] == 'CLOSED':
                                    strDeviceState = "closed"

                                else:
                                    strDeviceState = "open"
                            blnFlag = True
                        elif 'thermostat.json' in oNode["nodeType"] and 'thermostat' in oNode["name"].lower():

                            if oNode["attributes"]["zone"]["reportedValue"] == 'HOT_WATER':
                                strDeviceName = "Hot water"
                                strDevice = "hot water"
                                strDeviceState = oNode["attributes"]["stateHotWaterRelay"]["reportedValue"]
                            else:
                                strDeviceState = oNode["attributes"]["stateHeatingRelay"]["reportedValue"]
                                strDevice = "boiler"
                                strDeviceName = "Heating"

                            if oNode["attributes"]["presence"]["reportedValue"] == 'ABSENT':
                                strDevice = "offline"
                            blnFlag = True
            except:
                print("exception caught in verifyStatus")
                self.reporter.ReportEvent('Exception in verifyStatus', traceback.format_exc().replace('File', '$~File'),
                                          "DONE", 'Center', True)

            if blnFlag:
                strDeviceState = strDeviceState.lower()

                strText = strDeviceName + ";" + strDevice + ";" + strDeviceState
                listDevice.append(strText.lower())

            blnFlag = False

        ALAPI.deleteSessionV6(session)
        return listDevice

    # Set Mode via platform API
    def setModeViaAPI(self, nodeId, setMode, targetHeatTemperature=None, scheduleLockDuration=60):
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        nodeId = self.getChildNodeForBM(ALAPI.getNodesV6(session), nodeId)
        ALAPI.setModeV6(session, nodeId, setMode, targetHeatTemperature, scheduleLockDuration)
        if not 'WATER' in self.type.upper() and 'MANUAL' in setMode:
            ALAPI.setTargTemperatureV6(session, nodeId, targetHeatTemperature)
        ALAPI.deleteSessionV6(session)

    # Set Schedule via platform API
    def setScheduleViaAPI(self, nodeId, payload):
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()

        ALAPI.setScheduleSP(session, nodeId, payload)

        '''if 'SLR' in deviceType.upper():
            nodeId = self.getChildNodeForBM(ALAPI.getNodesV6(session), nodeId)'''
        # elif 'SLP' in deviceType.upper() or ''
        '''if not 'WATER' in self.type.upper() and 'MANUAL' in setMode:
            ALAPI.setTargTemperatureV6(session, nodeId, targetHeatTemperature)'''
        ALAPI.deleteSessionV6(session)

    def getChildNodeForBM(self, resp, BMNodeId):
        strChildNodeID = BMNodeId
        for oNode in resp['nodes']:
            if oNode['parentNodeId'] == BMNodeId:
                if ('WATER' in self.type.upper() and oNode['attributes']['supportsHotWater'][
                    'reportedValue'] == True) or (
                                'WATER' not in self.type.upper() and oNode['attributes']['supportsHotWater'][
                            'reportedValue'] == False):
                    strChildNodeID = oNode['id']
                    print('strChildNodeID', strChildNodeID)
        return strChildNodeID

    def setMode(self, myMode, mySetpoint=None, myDuration=1):
        if 'ANDROID' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                # oHeatingHomePage.navigate_to_heating_control_page()
                oHeatControlPage = androidPage.HeatingControlPage(self.AndroidDriver, self.reporter)
                oHeatControlPage.set_heat_mode(myMode, mySetpoint, myDuration)
                oHeatControlPage.honeycomb_verify()
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_control_page()
                oHotWaterControlPage = androidPage.HotWaterControlPage(self.AndroidDriver, self.reporter)
                print('platform duration', myDuration)
                oHotWaterControlPage.set_hot_water_mode(myMode, myDuration)
            elif self.type == 'PLUG':
                oSchedPage = androidPage.PlugSchedule(self.AndroidDriver, self.reporter)
                oSchedPage.Navigation_to_plugpage()
                if self.deviceName is not None:
                    devicePosition = self.position_using_deviceName(self.deviceName)
                    oSchedPage.find_device_on_dashboard(devicePosition)
                oSchedPage.set_plug_mode(myMode)

        elif 'IOS' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_heating_control_page()
                oHeatControlPage = iOSPage.HeatingControlPage(self.iOSDriver, self.reporter)
                oHeatControlPage.set_heat_mode(myMode, mySetpoint, myDuration)
            elif self.type == 'WATER':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_hot_water_control_page()
                oHotWaterControlPage = iOSPage.HotWaterControlPage(self.iOSDriver, self.reporter)
                oHotWaterControlPage.set_hot_water_mode(myMode, myDuration)
            elif self.type == 'PLUG':
                oSchedPage = iOSPage.PlugSchedulePage(self.iOSDriver, self.reporter)
                oSchedPage.set_plug_mode(myMode)
        elif 'WEB' in self.client.upper():
            if self.type == 'HEAT':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_heating_product_page()
                oHeatingPayge = webPage.HeatingPage(self.WebDriver, self.reporter)
                fltTargTemp = oHeatingPayge.set_heat_mode(myMode)
                if myMode == 'MANUAL': self.Web_ManualModeTargTemp = fltTargTemp
            elif self.type == 'WATER':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_hot_water_product_page()
                oHotWaterPage = webPage.HotWaterPage(self.WebDriver, self.reporter)
                fltTargTemp = oHotWaterPage.set_hot_water_mode(myMode)
                if myMode == 'MANUAL': self.Web_ManualModeTargTemp = fltTargTemp
            elif self.type == 'PLUG':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                # oHoneycombDashboardPayge.navigate_to_active_plug_product_page()
                oHoneycombDashboardPayge.navigate_to_active_plug_product_page_V3()
                oActivePlugPage = webPage.ActivePlugPage(self.WebDriver, self.reporter)
                fltTargTemp = oActivePlugPage.set_active_plug_mode(myMode)
                if myMode == 'MANUAL': self.Web_ManualModeTargTemp = fltTargTemp
                # oActivePlugPage.set_active_plug_schedule_V3()
            elif self.type == 'HOLIDAY':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_holiday_mode_page()
                oHolidayModePage = webPage.HolidayModePage(self.WebDriver, self.reporter)
                fltTargTemp = oHolidayModePage.set_holiday_mode(self.HolidayStartTime, self.HolidayEndTime,
                                                                self.occupiedHeatingSetpoint)
        self.occupiedHeatingSetpointChanged = False

    # Sets the state to the device
    def setState(self, strExpectedState, mySetpoint=None, myDuration=1):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.AndroidDriver, self.reporter)
            if self.deviceName is not None:
                devicePosition = self.position_using_deviceName(self.deviceName)
                oPlugsPage.find_device_on_dashboard(devicePosition)
            oPlugsPage.set_state(strExpectedState)

        elif 'IOS' in self.client.upper():
            # iOS functions to be written
            print('iOS device to be connected')

        elif 'WEB' in self.client.upper():
            if self.type == 'PLUG':
                # oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                # oHoneycombDashboardPayge.navigate_to_active_plug_product_page()
                oActivePlugPage = webPage.ActivePlugPage(self.WebDriver, self.reporter)
                fltTargTemp = oActivePlugPage.set_activeplug_state(strExpectedState)
                if strExpectedState == 'MANUAL': self.Web_ManualModeTargTemp = fltTargTemp
        self.occupiedHeatingSetpointChanged = False

    def setSetpoint(self, strExpectedMode, mySetpoint):
        if 'ANDROID' in self.client.upper():
            oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
            oHomePage.navigate_to_heating_home_page()
            oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
            oHeatingHomePage.navigate_to_heating_control_page()
            oHeatControlPage = androidPage.HeatingControlPage(self.AndroidDriver, self.reporter)
            oHeatControlPage.set_target_temperature(mySetpoint)
        elif 'IOS' in self.client.upper():
            oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
            oHomePage.navigate_to_heating_control_page()
            oHeatControlPage = iOSPage.HeatingControlPage(self.iOSDriver, self.reporter)
            if strExpectedMode != '':
                oHeatControlPage.set_heat_mode(strExpectedMode, None)
            oHeatControlPage.set_target_temperature(mySetpoint)
        elif 'WEB' in self.client.upper():
            oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
            oHoneycombDashboardPayge.navigate_to_heating_product_page()
            oHeatingPayge = webPage.HeatingPage(self.WebDriver, self.reporter)
            oHeatingPayge.set_target_temperature(mySetpoint)
            self.Web_ManualModeTargTemp = mySetpoint
        self.occupiedHeatingSetpointChanged = True

    def getSchedule(self):
        return self._weeklySchedule

    def setSchedule(self, oSchedule):
        if 'ANDROID' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_schedule_page()
                oSchedPage = androidPage.HeatingSchedulePage(self.AndroidDriver, self.reporter)
                oSchedPage.set_heating_schedule(oSchedule)
                oSchedPage.click_controlicon()
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_schedule_page()
                oSchedPage = androidPage.HotWaterSchedulePage(self.AndroidDriver, self.reporter)
                oSchedPage.set_hot_water_schedule(oSchedule)
            elif self.type == 'PLUG':
                oSchedPage = androidPage.PlugSchedule(self.AndroidDriver, self.reporter)
                oPlugPage = androidPage.PlugsPage(self.AndroidDriver, self.reporter)
                oSchedPage.navigation_to_plugpage()
                oPlugPage.click_scheduleicon()
                oSchedPage.set_plug_schedule(oSchedule)
                oPlugPage.click_controlicon()

        elif 'IOS' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_heating_schedule_page()
                oSchedPage = iOSPage.HeatingSchedulePage(self.iOSDriver, self.reporter)
                oSchedPage.set_heating_schedule(oSchedule)
            elif self.type == 'WATER':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_hot_water_schedule_page()
                oSchedPage = iOSPage.HotWaterSchedulePage(self.iOSDriver, self.reporter)
                oSchedPage.set_hot_water_schedule(oSchedule)
            elif self.type == 'PLUG':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_plug_schedule_page()
                oSchedPage = iOSPage.PlugSchedulePage(self.iOSDriver, self.reporter)
                oSchedPage.set_plug_schedule(oSchedule)
        elif 'WEB' in self.client.upper():
            if self.type == 'HEAT':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_heating_product_page()
                oHeatingPayge = webPage.HeatingPage(self.WebDriver, self.reporter)
                oHeatingPayge.set_heating_schedule(self._weeklySchedule, oSchedule)
            elif self.type == 'WATER':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_hot_water_product_page()
                oHotWaterPage = webPage.HotWaterPage(self.WebDriver, self.reporter)
                oHotWaterPage.set_hot_water_schedule(self._weeklySchedule, oSchedule)
            elif self.type == 'PLUG':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_active_plug_product_page()
                oHoneycombDashboardPayge.navigate_to_active_plug_product_page_V3()
                oActivePlugPage = webPage.ActivePlugPage(self.WebDriver, self.reporter)
                # oActivePlugPage.set_active_plug_schedule(self._weeklySchedule, oSchedule)
                oActivePlugPage.set_active_plug_schedule_V3_new(self._weeklySchedule, oSchedule)

    def resetSchedule(self, context, oSchedule):
        if 'ANDROID' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_schedule_page()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.reset_schedule(oSchedule)
                oHeatingHomePage.click_controlicon()
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_schedule_page()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.reset_schedule(oSchedule)
                oSchedulePage.click_controlicon()
            elif self.type == 'PLUG':
                oSchedPage = androidPage.PlugSchedule(self.AndroidDriver, self.reporter)
                oPlugPage = androidPage.PlugsPage(self.AndroidDriver, self.reporter)
                oSchedPage.navigation_to_plugpage()
                oPlugPage.click_scheduleicon()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.reset_schedule(oSchedule)
                oSchedPage.click_controlicon()
        # Plug code - Rajesh
        elif 'IOS' in self.client.upper():
            if self.type == 'PLUG':
                oDeviceNavigation = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
                oDeviceNavigation.navigate_to_device_updated(self.deviceName)
                oPlugSchedule = iOSPage.PlugSchedulePage(self.iOSDriver, self.reporter)
                oPlugSchedule.resetPlugSchedule(context)
            elif self.type == 'WATER':
                oDeviceNavigation = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oDeviceNavigation.navigate_to_hot_water_schedule_page()
                oHotWaterSchedule = iOSPage.HotWaterSchedulePage(self.iOSDriver, self.reporter)
                oHotWaterSchedule.resetHotWaterSchedule(context)
            elif self.type == 'HEAT':
                oDeviceNavigation = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oDeviceNavigation.navigate_to_heating_schedule_page()
                oHeatingSchedule = iOSPage.HeatingSchedulePage(self.iOSDriver, self.reporter)
                oHeatingSchedule.resetHeatingSchedule(context)
        elif 'WEB' in self.client.upper():
            print('locators required')

    def addSchedule(self, context):
        if 'ANDROID' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_schedule_page()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.add_schedule(context, self.type)
                oHeatingHomePage.click_controlicon()
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_schedule_page()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.add_schedule(context, self.type)
                oSchedulePage.click_controlicon()
            elif self.type == 'PLUG':
                oSchedPage = androidPage.PlugSchedule(self.AndroidDriver, self.reporter)
                oPlugPage = androidPage.PlugsPage(self.AndroidDriver, self.reporter)
                oSchedPage.navigation_to_plugpage()
                oPlugPage.click_scheduleicon()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.add_schedule(context, self.type)
                oPlugPage.click_controlicon()

        elif 'IOS' in self.client.upper():
            if self.type == 'PLUG':
                oPlugSchedule = iOSPage.PlugSchedulePage(self.iOSDriver, self.reporter)
                oPlugSchedule.addschedule(context)

        elif 'WEB' in self.client.upper():
            print('locators required')

    def delSchedule(self, context):
        if 'ANDROID' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_schedule_page()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.delete_schedule(context)
                oHeatingHomePage.click_controlicon()
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_schedule_page()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.delete_schedule(context)
                oSchedulePage.click_controlicon()
            elif self.type == 'PLUG':
                oSchedPage = androidPage.PlugSchedule(self.AndroidDriver, self.reporter)
                oPlugPage = androidPage.PlugsPage(self.AndroidDriver, self.reporter)
                oSchedPage.navigation_to_plugpage()
                oPlugPage.click_scheduleicon()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.delete_schedule(context)
                oPlugPage.click_controlicon()

        elif 'IOS' in self.client.upper():
            if self.type == 'PLUG':
                oPlugSchedule = iOSPage.PlugSchedulePage(self.iOSDriver, self.reporter)
                oPlugSchedule.delete_schedule(context)

        elif 'WEB' in self.client.upper():
            print('locators required')

    def copySchedule(self, context):
        if 'ANDROID' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_schedule_page()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.copy_schedule(context.strDay2, context.strDay1)
                oHeatingHomePage.click_controlicon()
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_schedule_page()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.copy_schedule(context.strDay2, context.strDay1)
                oSchedulePage.click_controlicon()
            elif self.type == 'PLUG':
                oSchedPage = androidPage.PlugSchedule(self.AndroidDriver, self.reporter)
                oPlugPage = androidPage.PlugsPage(self.AndroidDriver, self.reporter)
                oSchedPage.navigation_to_plugpage()
                oPlugPage.click_scheduleicon()
                oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
                oSchedulePage.copy_schedule(context.strDay2, context.strDay1)
                oPlugPage.click_controlicon()

        elif 'IOS' in self.client.upper():
            if self.type == 'PLUG':
                oPlugSchedule = iOSPage.SchedulePage(self.iOSDriver, self.reporter)
                oPlugSchedule.copy_schedule(context.strDay2, context.strDay1)
            elif self.type == 'HEAT':
                oHeatingSchedule = iOSPage.SchedulePage(self.iOSDriver, self.reporter)
                oHeatingSchedule.copy_schedule(context.strDay2, context.strDay1)
            elif self.type == 'WATER':
                oHotWaterSchedule = iOSPage.SchedulePage(self.iOSDriver, self.reporter)
                oHotWaterSchedule.copy_schedule(context.strDay2, context.strDay1)
        elif 'WEB' in self.client.upper():
            print('locators required')

    def getAttributesFromClient(self):
        if 'ANDROID' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_control_page(False)
                oHeatControlPage = androidPage.HeatingControlPage(self.AndroidDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHeatControlPage.get_heating_attribute(
                    self.mode)
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_control_page(False)
                oHotWaterControlPage = androidPage.HotWaterControlPage(self.AndroidDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHotWaterControlPage.get_hotwater_attribute()
            elif self.type == 'PLUG':
                oPlugPage = androidPage.PlugsPage(self.AndroidDriver, self.reporter)
                if self.deviceName is not None:
                    devicePosition = self.position_using_deviceName(self.deviceName)
                    oPlugPage.find_device_on_dashboard(devicePosition)
                self.mode, self.thermostatRunningState = oPlugPage.get_plug_attribute()
        elif 'IOS' in self.client.upper():
            if self.type == 'HEAT':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_heating_control_page(False)
                oHeatControlPage = iOSPage.HeatingControlPage(self.iOSDriver, self.reporter)
                oHeatControlPage.stopBoost = False
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHeatControlPage.get_heating_attribute()
            if self.type == 'WATER':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_hot_water_control_page(False)
                oHotWaterControlPage = iOSPage.HotWaterControlPage(self.iOSDriver, self.reporter)
                oHotWaterControlPage.stopBoost = False
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHotWaterControlPage.get_hotwater_attribute()
        elif 'WEB' in self.client.upper():
            if self.type == 'HEAT':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_heating_product_page()
                oHeatingPayge = webPage.HeatingPage(self.WebDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHeatingPayge.get_heating_attribute()
            elif self.type == 'WATER':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_hot_water_product_page()
                oHotWaterPage = webPage.HotWaterPage(self.WebDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHotWaterPage.get_hotwater_attribute()
            elif self.type == 'PLUG':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_active_plug_product_page_V3()
                oActivePlugPage = webPage.ActivePlugPage(self.WebDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oActivePlugPage.get_activeplug_attribute()
            elif self.type == 'HOLIDAY':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_holiday_mode_page()
                oHolidayModePage = webPage.HolidayModePage(self.WebDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHolidayModePage.get_holiday_mode_attribute()

    def position_using_deviceName(self, deviceName):
        self.beekeeperEP = beekeeperEndPoint(self, self.serverName)
        self.beekeeperConfig = self.beekeeperEP.deviceConfig
        self.devicePositionDict = {}
        self.beekeeperTotalPages = self.beekeeperEP.totalPages
        devicePositionItem = ''

        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        self.platformVersion = 'V6'
        resp = ALAPI.getNodesV6(session)

        for eachNode in resp['nodes']:
            if 'name' in eachNode:
                if deviceName in eachNode['name']:
                    nodeID = eachNode['id']
                    devicePositionItem = self.beekeeperConfig[nodeID]

        return devicePositionItem

    def getHeatRule(self):

        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        if session.latestSupportedApiVersion != '6':
            self.platformVersion = 'V5'
            print("hello")
            return False
        else:
            self.platformVersion = 'V6'
            rules = ALAPI.getRulesV6(session)
        # print(rules)
        # print(rules['rules'])

        oHeatRuleDict = {}
        heatRuleCount = 0
        if rules['rules']:
            for oActions in rules['rules']:
                oRuleList = []
                if oActions['name'] in ('TooHot', 'TooCold'):
                    heatRuleCount = heatRuleCount + 1
                    # print('Rule : ' + oActions['name'])
                    # return oActions['name']
                    # print(" : ",end='')
                    for status in oActions['actions']:
                        # print(status['status'],end='')
                        # print(" : ",end='')
                        types = status['type']
                        for values in oActions['triggers']:
                            # print(values['value']+' : '+types)
                            # print('\n')
                            # oRuleList.append((values['value'],types,status['status']))
                            oRuleList.append(values['value'])
                            oRuleList.append(types)
                            oRuleList.append(status['status'])
                            oHeatRuleDict.update({oActions['name']: oRuleList})
                            if heatRuleCount == 0:
                                print('No Heating Rules are set')

        else:
            print('No rules are set')

        print(oHeatRuleDict)
        print('\n')

        return oHeatRuleDict

    def navigateToScreen(self, strPageName):
        oAccDetPage = androidPage.AccountDetails(self.AndroidDriver, self.reporter)
        oAccDetPage.open_acc_details(strPageName)

    def changePasswordScreen(self):
        if 'IOS' in self.client.upper():
            oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
            oHomePage.navigate_to_screen('Change Password')
            oChngPassPage = iOSPage.SetChangePassword(self.iOSDriver, self.reporter)
            oChngPassPage.change_password()
        if 'ANDROID' in self.client.upper():
            oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
            oHomePage.navigate_to_screen('Change Password')
            oChngPassPage = androidPage.SetChangePassword(self.AndroidDriver, self.reporter)
            oChngPassPage.change_password()

    def navigateToHolidayScreen(self, context, actionType, holidayModeType):
        if 'ANDROID' in self.client.upper():
            oHolidayPage = androidPage.HolidayMode(self.AndroidDriver, self.reporter)
            oHolidayPage.navigateToHoildayScreen(context)
        elif 'IOS' in self.client.upper():
            oHolidayPage = iOSPage.HolidayMode(self.iOSDriver, self.reporter)
            oHolidayPage.navigate_To_HolidayScreen(context, actionType, holidayModeType)

    def setHolidayMode(self, context, actionType, strHolidayModeType, targetTemperature, daysFromNow=None,
                       duration=None):
        if 'ANDROID' in self.client.upper():
            oHolidayPage = androidPage.HolidayMode(self.AndroidDriver, self.reporter)
            oHolidayPage.set_Holiday_Mode(context, actionType, strHolidayModeType, targetTemperature, daysFromNow,
                                          duration)
        elif 'IOS' in self.client.upper():
            oHolidayPage = iOSPage.HolidayMode(self.iOSDriver, self.reporter)
            oHolidayPage.set_Holiday_Mode(context, actionType, strHolidayModeType, targetTemperature, daysFromNow,
                                          duration)

    def verifyHolidayMode(self, context, actionType, strHolidayModeType, targetTemperature):
        if 'IOS' in self.client.upper():
            oHolidayPage = iOSPage.HolidayMode(self.iOSDriver, self.reporter)
            enabled, departureDateUI, departureTimeUI, returnDateUI, returnTimeUI, strTempUI = oHolidayPage.get_Holiday_DetailsApp(
                actionType, strHolidayModeType)
            time.sleep(20)
            if enabled:
                departureDateAPI, departureTimeAPI, returnDateAPI, returnTimeAPI, strTempAPI = self.getHolidayDetailsAPI(
                    context, actionType)
                oHolidayPage.validateHolidayModeDetails(departureDateUI, departureTimeUI, returnDateUI, returnTimeUI,
                                                        strTempUI, departureDateAPI, departureTimeAPI, returnDateAPI,
                                                        returnTimeAPI, strTempAPI, targetTemperature)
            else:
                self.getHolidayDetailsAPI(context, actionType)
        if 'ANDROID' in self.client.upper():
            oHolidayPage = androidPage.HolidayMode(self.AndroidDriver, self.reporter)
            enabled, departureDateUI, departureTimeUI, returnDateUI, returnTimeUI, strTempUI = oHolidayPage.get_Holiday_DetailsApp(
                actionType, strHolidayModeType)
            time.sleep(3)
            if enabled:
                departureDateAPI, departureTimeAPI, returnDateAPI, returnTimeAPI, strTempAPI = self.getHolidayDetailsAPI(
                    context, actionType)
                oHolidayPage.validateHolidayModeDetails(departureDateUI, departureTimeUI, returnDateUI, returnTimeUI,
                                                        strTempUI, departureDateAPI, departureTimeAPI, returnDateAPI,
                                                        returnTimeAPI, strTempAPI, targetTemperature)
            else:
                self.getHolidayDetailsAPI(context, actionType)
            oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
            oHomePage.navigate_to_heating_home_page()
            oHolidayPage.validate_holiday_control_screen(actionType)
            oHomePage.navigate_to_hot_water_home_page()
            oHolidayPage.validate_holiday_control_screen(actionType)

    def getHolidayDetailsAPI(self, context, actionType):
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        if session.latestSupportedApiVersion != '6':
            self.platformVersion = 'V5'
            print("V5")
            return False
        else:
            self.platformVersion = 'V6'
            resp = ALAPI.getNodesV6(session)

            for oNode in resp['nodes']:
                try:
                    if 'http://alertme.com/schema/json/node.class.thermostat.json#' in oNode['nodeType']:
                        oAttributeList = oNode['attributes']
                        oJson = self.getAttribute(oAttributeList, 'holidayMode')
                        if isinstance(oJson, str): oJson = json.loads(oJson)
                        boolHolidayMode = oJson['enabled']
                        strTemp = oJson['targetHeatTemperature']
                        print('Holiday mode test')
                        if boolHolidayMode:
                            print('Holiday mode is active now')
                            self.mode = 'HOLIDAY'
                            self.HolidayStartTime = oJson['startDateTime']
                            self.HolidayEndTime = oJson['endDateTime']

                            startTime = self.HolidayStartTime.replace(":00.000+0000", "")
                            startTime = datetime.strptime(startTime, "%Y-%m-%dT%H:%M")
                            departureDate = startTime.strftime('%d%b %Y')
                            departureTime = startTime.strftime('%H:%M')

                            endTime = self.HolidayEndTime.replace(":00.000+0000", "")
                            endTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M")
                            returnDate = endTime.strftime('%d%b %Y')
                            returnTime = endTime.strftime('%H:%M')

                            print(boolHolidayMode, strTemp, departureDate, departureTime, returnDate, returnTime)

                            Header = "Departure Date $$ Departure Time $$ Return Date $$ Return Time $$ Target Temperature @@@"

                            tableRow1 = departureDate + "$$" + departureTime + "$$" + returnDate + "$$" + returnTime + "$$" + str(
                                strTemp)

                            StrLog = Header + tableRow1
                            self.reporter.ReportEvent("Test Validation : API ", StrLog, "DONE")

                            return departureDate, departureTime, returnDate, returnTime, str(strTemp)

                        else:
                            if 'CANCELLED' in actionType.upper() or 'STOPPED' in actionType.upper():
                                strLog = 'Holiday mode is not active'
                                self.reporter.ReportEvent("Test Validation : API ", strLog, "PASS")
                            else:
                                strLog = 'Holiday mode is not active'
                                self.reporter.ReportEvent("Test Validation : API ", strLog, "FAIL")
                            break
                except:
                    print('')

    def navigate_to_settingScreen(self, strPageName):
        if 'WEB' in self.client.upper():
            oLandingPage = webPage.BasePage(self.WebDriver, self.reporter)
            oLandingPage.navigate_to_settingScreen(strPageName)
        if 'ANDROID' in self.client.upper():
            print('test successful')

    def setHighNotification(self, oTargetHighTemp, oTargetLowTemp='', oBothAlert='No'):
        if 'WEB' in self.client.upper():
            oAlertType = webPage.SetNotification(self.WebDriver, self.reporter)
            oAlertType.set_high_temperature(oTargetHighTemp, oTargetLowTemp, oBothAlert)
        if 'IOS' in self.client.upper():
            oLandingPage = iOSPage.SaveHeatingNotification(self.iOSDriver, self.reporter)
            oLandingPage.naivgate_to_ZoneNotificaiton()
            oLandingPage.setHighTemperature(oTargetHighTemp)
        if 'ANDROID' in self.client.upper():
            oLandingPage = androidPage.SaveHeatingNotification(self.AndroidDriver, self.reporter)
            oLandingPage.naivgate_to_ZoneNotificaiton()
            oLandingPage.setHighTemperature(oTargetHighTemp)

    def setLowNotification(self, oTargetLowTemp='', oBothAlert='No'):
        if 'WEB' in self.client.upper():
            oAlertType = webPage.SetNotification(self.WebDriver, self.reporter)
            oAlertType.set_low_temperature(oTargetLowTemp, 'Yes')
        if 'IOS' in self.client.upper():
            oLandingPage = iOSPage.SaveHeatingNotification(self.iOSDriver, self.reporter)
            oLandingPage.setLowTemperature(oTargetLowTemp)
            oLandingPage.receiveWarnings()
        if 'ANDROID' in self.client.upper():
            oLandingPage = androidPage.SaveHeatingNotification(self.AndroidDriver, self.reporter)
            oLandingPage.naivgate_to_ZoneNotificaiton()
            oLandingPage.setLowTemperature(oTargetLowTemp)
            oLandingPage.receiveWarnings()

    def setNotificationOnOff(self, strNotiState, strNotiType='Both'):
        if 'WEB' in self.client.upper():
            oAlertType = webPage.SetNotification(self.WebDriver, self.reporter)
            oAlertType.setNotificationOnOff(strNotiState)
        if 'IOS' in self.client.upper():
            oLandingPage = iOSPage.SaveHeatingNotification(self.iOSDriver, self.reporter)
            oLandingPage.setNotificationONtoOFF(strNotiState)
        if 'ANDROID' in self.client.upper():
            oLandingPage = androidPage.SaveHeatingNotification(self.AndroidDriver, self.reporter)
            oLandingPage.naivgate_to_ZoneNotificaiton()
            oLandingPage.setNotificationONtoOFF(strNotiState)

    def getNotificationTempFromUI(self):
        if 'WEB' in self.client.upper():
            oAlertType = webPage.SetNotification(self.WebDriver, self.reporter)
            strExpectedTemp = oAlertType.getNotificationTempFromUI()
        if 'ANDROID' in self.client.upper():
            oLandingPage = androidPage.SaveHeatingNotification(self.AndroidDriver, self.reporter)
            strExpectedTemp = oLandingPage.getNotificationTempFromUI()
        return strExpectedTemp

    def navigatetoContactSensor(self, nameContactSensor):
        if 'IOS' in self.client.upper():
            # if self.type == 'SENSOR':
            cLandingPage = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            print(self.reporter.strResultsPath)
            cLandingPage.navigate_to_device_updated(nameContactSensor)
        if 'ANDROID' in self.client.upper():
            # if self.type == 'SENSOR':
            cLandingPage = androidPage.HomePage(self.AndroidDriver, self.reporter)
            print(self.reporter.strResultsPath)
            cLandingPage.navigation_to_devicepage(nameContactSensor)

    def currentCSStatus(self, nameContactSensor):
        if 'IOS' in self.client.upper():
            cLandingPage = iOSPage.ContactSensors(self.iOSDriver, self.reporter)
            # print(self.reporter.strResultsPath)
            currentStatus = cLandingPage.contactSensorCurrentStatus(nameContactSensor)
            return currentStatus
        if 'ANDROID' in self.client.upper():
            cLandingPage = androidPage.ContactSensor(self.AndroidDriver, self.reporter)
            currentStatus = cLandingPage.contactSensorCurrentStatus()
            return currentStatus

    def accessTodaysLog(self):
        if 'IOS' in self.client.upper():
            oTodaysLogPage = iOSPage.ContactSensors(self.iOSDriver, self.reporter)
            oTodaysLogPage.todaysLog()
        if 'ANDROID' in self.client.upper():
            oTodaysLogPage = androidPage.ContactSensor(self.AndroidDriver, self.reporter)
            oTodaysLogPage.todaysLog()

    def eventLogScreen(self, selectWeekDay):
        if 'IOS' in self.client.upper():
            oEventLogScreen = iOSPage.ContactSensors(self.iOSDriver, self.reporter)
            oEventLogScreen.navigate_to_selected_weekday_log(selectWeekDay)
        if 'ANDROID' in self.client.upper():
            oEventLogScreen = androidPage.ContactSensor(self.AndroidDriver, self.reporter)
            oEventLogScreen.navigate_to_selected_weekday_log(selectWeekDay)

    def verfiyEventLogs(self):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ContactSensors(self.iOSDriver, self.reporter)
            oLogScreen.verify_todayevent_logs()
        if 'ANDROID' in self.client.upper():
            oLogScreen = androidPage.ContactSensor(self.AndroidDriver, self.reporter)
            oLogScreen.verify_todayevent_logs()

    def checkDeviceWithHub(self, strdeviceName):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            oLogScreen.navigate_to_motionsensor(strdeviceName)
            oBulbScreen = iOSPage.ColourLights(self.iOSDriver, self.reporter)
            oBulbScreen.updateBulbObjects(strdeviceName)
        if 'ANDROID' in self.client.upper():
            AllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            AllRecipes.check_the_device_with_hub(strdeviceName)

    def navigateToActiveLight(self, strdeviceName):
        if 'IOS' in self.client.upper():
            oBasePage = iOSPage.BasePage(self.iOSDriver, self.reporter)
            # oBasePage.skip_Dashboard_tutorial()
            oBasePage.navigate_to_device(strdeviceName)
            oBulbScreen = iOSPage.ColourLights(self.iOSDriver, self.reporter)
            oBulbScreen.updateBulbObjects(strdeviceName)
        if 'ANDROID' in self.client.upper():
            if "LIGHT" in str(strdeviceName).upper():
                oLogScreen = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
                oLogScreen.setBulbModelandName(strdeviceName)
                oLogScreen.navigate_to_active_light_page(str(strdeviceName))

    def removeAllActions(self):
        if 'IOS' in self.client.upper():
            print("TBD")
        if 'ANDROID' in self.client.upper():
            oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            oAllRecipes.navigate_to_allrecipes()
            oAllRecipes.remove_existing_recipes()

    def verifyRecipeTemplate(self):
        if 'IOS' in self.client.upper():
            print("TBD")
        if 'ANDROID' in self.client.upper():
            oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            oAllRecipes.verify_recipe_template()

    def setNotifyMeRecipe(self, TypeOf, Sensor, SensorState):
        if 'IOS' in self.client.upper():
            oDeviceRecipes = iOSPage.DeviceRecipes(self.iOSDriver, self.reporter)
            oMotionSensor = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            recipe_exists = 100
            if ('opened' in SensorState) or ('closed' in SensorState):
                oDeviceRecipes.navigate_to_device(Sensor, 'CS')
            else:
                oDeviceRecipes.navigate_to_device(Sensor, 'MS')
            oDeviceRecipes.TEXT_RECIPE_SET = 0
            oMotionSensor.navigate_to_recipes("device")
            recipe_exists = oDeviceRecipes.verify_notification_recipe_exists(Sensor, TypeOf, SensorState)
            oDeviceRecipes.set_sensor_recipe(recipe_exists, TypeOf, Sensor, SensorState)
        if 'ANDROID' in self.client.upper():
            oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            oAllRecipes.navigate_to_allrecipes()
            oAllRecipes.create_new_notification_recipe(TypeOf, Sensor, SensorState)

    def verifyNotifyMeRecipeAllRecipesPage(self, TypeOf, Sensor, SensorState, Location):
        if 'IOS' in self.client.upper():
            oDeviceRecipes = iOSPage.DeviceRecipes(self.iOSDriver, self.reporter)
            oMotionSensor = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            if oDeviceRecipes.SET_RECIPE_TRIGERRED == 1:
                recipe_exists = 100
                oMotionSensor.navigate_to_recipes(Location)
                recipe_exists = oDeviceRecipes.verify_notification_recipe_exists(Sensor, TypeOf, SensorState)
                oDeviceRecipes.report_recipe_exists(recipe_exists, TypeOf, Sensor, SensorState, "All Recipes")
            else:
                oDeviceRecipes.report_recipe_exists(1, TypeOf, Sensor, SensorState, "All Recipes")
                oDeviceRecipes.SET_RECIPE_TRIGERRED = 0
                oDeviceRecipes.TEXT_RECIPE_SET = 0
        if 'ANDROID' in self.client.upper():
            oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            oAllRecipes.navigate_to_allrecipes()
            oAllRecipes.verify_notifyme_recipe_all_recipes(Sensor, SensorState)

    def verifyOnOffRecipeSensorPage(self, Sensor):
        if 'IOS' in self.client.upper():
            print("TBD")
        if 'ANDROID' in self.client.upper():
            oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
            oHomePage.navigation_to_devicepage(Sensor)
            oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            oAllRecipes.verify_on_off_recipe_sensor_page(Sensor)

    def verifyNotifyMeRecipeDevicePage(self, TypeOf, Sensor, SensorState, Location):
        if 'IOS' in self.client.upper():
            oDeviceRecipes = iOSPage.DeviceRecipes(self.iOSDriver, self.reporter)
            oMotionSensor = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            if oDeviceRecipes.SET_RECIPE_TRIGERRED == 1:
                recipe_exists = 100
                if ('opened' in SensorState) or ('closed' in SensorState):
                    oDeviceRecipes.navigate_to_device(Sensor, 'CS')
                else:
                    oDeviceRecipes.navigate_to_device(Sensor, 'MS')
                oMotionSensor.navigate_to_recipes(Location)
                recipe_exists = oDeviceRecipes.verify_notification_recipe_exists(Sensor, TypeOf, SensorState)
                oDeviceRecipes.report_recipe_exists(recipe_exists, TypeOf, Sensor, SensorState, "Device Recipes")

        if 'ANDROID' in self.client.upper():
            if 'sensor' in Location:
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigation_to_devicepage(Sensor)
                oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
                oAllRecipes.verify_notifyme_recipe_sensor_page(Sensor, SensorState)
            if 'Actions' in Location:
                oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
                oAllRecipes.navigate_to_allrecipes()
                oAllRecipes.verify_notifyme_recipe_all_recipes(Sensor, SensorState)

    def setOnOffMeRecipe(self, strDevice, strDeviceState, strDuration, strSensor, strSensorState):
        if 'IOS' in self.client.upper():
            print("TBD")
        if 'ANDROID' in self.client.upper():
            oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            oAllRecipes.setRecipeVariables(strDevice, strDeviceState, strDuration, strSensor, strSensorState)
            oAllRecipes.navigate_to_allrecipes()
            oAllRecipes.createNewOnOffRecipe(strDevice, strDeviceState, strDuration, strSensor, strSensorState)

    def navigateToDeviceScreen(self, nameMotionSensor):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            oLogScreen.navigate_to_motionsensor(nameMotionSensor)

    def setLocalValues(self, Settings, Value):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver, self.reporter)
            oLogScreen.setValues(Settings, Value)
        if 'ANDROID' in self.client.upper():
            oLogScreen = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oLogScreen.setValues(Settings, Value)

    def navigateToDesiredSettings(self, Settings):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver, self.reporter)
            oLogScreen.navigateToSettings(Settings)
        if 'ANDROID' in self.client.upper():
            oLogScreen = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oLogScreen.navigateToSettings(Settings)

    def setValueForBulbBySwiping(self, Settings, Value):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver, self.reporter)
            oLogScreen.setValueForBulb(Settings, Value)
        if 'ANDROID' in self.client.upper():
            oLogScreen = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oLogScreen.setValueForBulb(Settings, Value)

    def verifyValueInAPI(self):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver, self.reporter)
            oLogScreen.verifyAPI()
        if 'ANDROID' in self.client.upper():
            oLogScreen = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oLogScreen.verifyLightAPI()

    def honeycombVerification(self):
        if 'ANDROID' in self.client.upper():
            oHoneycomb = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oHoneycomb.honeycomb_preview_verify()

    def DashboardStatusVerification(self, strDeviceName, strDeviceType, strStatus):
        if 'ANDROID' in self.client.upper():
            print('in Android')
            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.honeycomb_validate_status(strDeviceName, strDeviceType, strStatus)

    def DashboardFetchVerification(self, context):
        if 'ANDROID' in self.client.upper():
            listDevice = context.oThermostatEP.verifyStatus()
            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.honeycomb_fetch_status(listDevice, context)
        elif 'IOS' in self.client.upper():
            oDashboard = iOSPage.HoneyComb(self.iOSDriver, self.reporter)
            oDashboard.dashboard_device_status()

    def honeycomb_verify(self, context):
        if 'ANDROID' in self.client.upper():

            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.honeycomb_verify()
        elif 'IOS' in self.client.upper():

            oDashboard = iOSPage.HoneyComb(self.iOSDriver, self.reporter)
            oDashboard.honeycomb_verifyscreen()

    def devicelist_verify(self):
        if 'ANDROID' in self.client.upper():

            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.devicelist_verify()
        elif 'IOS' in self.client.upper():
            oDashboard = iOSPage.HoneyComb(self.iOSDriver, self.reporter)
            oDashboard.devicelist_verifyscreen()

    def honeycomb_verifyTitle(self, context):
        if 'ANDROID' in self.client.upper():

            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.honeycomb_verifyTitle()
        elif 'IOS' in self.client.upper():
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the Honeycomb Title')
            oDashboard = iOSPage.HoneyComb(self.iOSDriver, self.reporter)
            oDashboard.honeycomb_verify_Title()

    def honeycomb_verifyHierarchy(self, context):

        if 'ANDROID' in self.client.upper():

            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.honeycomb_verifyIconHierarchy(context)
        elif 'IOS' in self.client.upper():
            oDashboard = iOSPage.HoneyComb(self.iOSDriver, self.reporter)
            # oDashboard.honeycomb_verify_Title()

    def DeviceListFetchVerification(self, context):
        if 'ANDROID' in self.client.upper():
            listDevice = context.oThermostatEP.verifyStatus()
            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.devicelist_fetch_status(listDevice, context)
        elif 'IOS' in self.client.upper():
            oDashboard = iOSPage.HoneyComb(self.iOSDriver, self.reporter)
            oDashboard.devicelist_device_status()

    def deviceList_verifyHierarchy(self, context):

        if 'ANDROID' in self.client.upper():

            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.deviceList_verifyIconHierarchy()
        elif 'IOS' in self.client.upper():
            oDashboard = iOSPage.HoneyComb(self.iOSDriver, self.reporter)
            oDashboard.devicelist_verifyIconHierarchy()

    def navigationTo_screen(self, context, strScreenName):

        if 'ANDROID' in self.client.upper():

            oDashboard = androidPage.HoneyComb(self.AndroidDriver, self.reporter)
            oDashboard.navigationTo_screen(context, strScreenName)
        elif 'IOS' in self.client.upper():
            context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                'Validating the Honeycomb Dashboard Icon presence in screen: ' + strScreenName)
            oDashboard = iOSPage.HoneyComb(self.iOSDriver, self.reporter)
            oDashboard.navigation_to_screen(strScreenName)

    def verifyDeviceModeSettings(self, strdeviceName):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver, self.reporter)
            oLogScreen.verifyDeviceModes(strdeviceName)

    # Dashboard customization -------------

    def checkDeviceOnDashboard(self, deviceName):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.checkDeviceOnDashboardScreen(deviceName)
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.updateObjects(deviceName)

    def navigateAndLongPressCell(self):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.navigateAndLongPressCellOnDevice()
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.initiateEditMode()

    def validateEditMode(self):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.validateEditModeIcon()
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.verifyDashboardEditMode()

    def clickButton(self, buttonType):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.tapButton(buttonType)
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.tapButton(buttonType)

    def addDeviceFromList(self):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.addDeviceFromListViewAndSave()
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.addDeviceFromListOnDashboard()

    def deleteDeviceFromDashboard(self):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.removeDeviceFromDashboard()
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.tapButton("REMOVE")

    def validateDeviceOnDashboard(self):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.validateDeviceInListView()
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.validateDeletedDeviceInList()

    def validateChangesAfterExit(self, type):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.validateChangesPostExit(type)
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.validateChangesPostExit(type)

    def swapDevices(self, SwapDeviceName):

        if 'ANDROID' in self.client.upper():
            oDashboardCust = androidPage.DashboardCustomization(self.AndroidDriver, self.reporter)
            oDashboardCust.swapDevicesOnDashboard(SwapDeviceName)
        elif 'IOS' in self.client.upper():
            oDashboardCust = iOSPage.DashboardCustomisation(self.iOSDriver, self.reporter)
            oDashboardCust.swapDevicesOnDashboard(SwapDeviceName)

    # -------------- Dashboard Customisation ------------- #

    # -------------- Motion Sensor -----------------------#

    def validateDeviceWithHub(self, strdeviceName):

        if 'IOS' in self.client.upper():

            oMotionSensor = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            oMotionSensor.navigate_to_device_updated(strdeviceName)

        elif 'ANDROID' in self.client.upper():

            self.checkDeviceOnDashboard(strdeviceName)

    def navigate_ToDeviceScreen(self, nameMotionSensor):

        if 'IOS' in self.client.upper():

            oMotionSensor = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            oMotionSensor.navigate_to_device_updated(nameMotionSensor)

        elif 'ANDROID' in self.client.upper():

            oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
            oHomePage.navigation_to_devicepage(nameMotionSensor)

    def navigateTo_eventlogs(self):

        if 'ANDROID' in self.client.upper():
            oMotionSensor = androidPage.MotionSensor(self.AndroidDriver, self.reporter)
            oMotionSensor.navigateToEventLogs()

        elif 'IOS' in self.client.upper():

            oMotionSensor = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            oMotionSensor.navigate_to_eventlogs()

    def verifyEventLogs(self):

        if 'ANDROID' in self.client.upper():

            oMotionSensor = androidPage.MotionSensor(self.AndroidDriver, self.reporter)
            oMotionSensor.validateEventLogs()

        elif 'IOS' in self.client.upper():

            oMotionSensor = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            oMotionSensor.verify_event_logs()

    def validateCurrentStatus(self, nameMotionSensor):

        if 'ANDROID' in self.client.upper():
            oMotionSensor = androidPage.MotionSensor(self.AndroidDriver, self.reporter)
            oMotionSensor.checkCurrentStatus()

        elif 'IOS' in self.client.upper():

            oMotionSensor = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            currentStatus = oMotionSensor.verify_current_status(nameMotionSensor)
            return currentStatus

    def navigateToSelectDaysLogs(self, intNumberOf):

        if 'ANDROID' in self.client.upper():
            oMotionSensor = androidPage.MotionSensor(self.AndroidDriver, self.reporter)
            oMotionSensor.navigateToSelectedDayOfLog(intNumberOf)

        elif 'IOS' in self.client.upper():

            oMotionSensor = iOSPage.MotionSensor(self.iOSDriver, self.reporter)
            oMotionSensor.navigate_to_eventlogs()
            oMotionSensor.navigate_to_selected_day_log(intNumberOf)

            # -------------- Motion Sensor -----------------------#


class MainMenu:
    def __init__(self, driver, reporter):
        self.driver = driver
        self.reporter = reporter
        self.EXPLICIT_WAIT_TIME = 25
        self.client = utils.getAttribute('common', 'mainClient')

    def clickmainmenu(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_menuicon()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_menuicon()

    def verifymainmenuicons(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_main_menu()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_main_menu()

    def clickmanagedevices(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_managedeviceicon()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_managedeviceicon()

    def verifymanagedevicescreen(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_verify_managedevicescreen()
            oMenuPage.click_menuicon()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_verify_managedevicescreen()
            oMenuPage.click_menuicon()

    def clickinstalldevices(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_installdevice()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_installdevice()

    def verifyinstalldevicescreen(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_verify_installdevicescreen()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_verify_installdevicescreen()

    def verifyoptions_installdevices(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_verifyoptions_installdevicescreen()
            oMenuPage.click_menuicon()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_verifyoptions_installdevicescreen()
            oMenuPage.click_menuicon()

    def clickallrecipes(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_allrecipes()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_allrecipes()

    def verifyallrecipescreen(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_allrecepiescreen()
            oMenuPage.click_menuicon()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_allrecepiescreen()
            oMenuPage.click_menuicon()

    def clicksettings(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_settings()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_settings()

    def verifysettingsoptions(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_settingsoptions()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_settingsoptions()

    def clickhelp(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_help()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_help()

    def verifyhelpoptions(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_helpoptions()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_helpoptions()

    def clicklogout(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_logout()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.click_logout()

    def verifylogout(self):
        if 'ANDROID' in self.client.upper():
            oMenuPage = androidPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_logout()
        elif 'IOS' in self.client.upper():
            oMenuPage = iOSPage.MainMenuPage(self.driver, self.reporter)
            oMenuPage.verify_logout()

    def verifydashboardscreen(self):
        if 'ANDROID' in self.client.upper():
            oHomePage = androidPage.HomePage(self.driver, self.reporter)
            oHomePage.verify_dashboardscreen()

    def verifyemptyslots(self):
        if 'ANDROID' in self.client.upper():
            oHomePage = androidPage.HomePage(self.driver, self.reporter)
            oHomePage.verify_emptyslots()


class Plugs:
    def __init__(self, driver, reporter):
        self.driver = driver
        self.reporter = reporter
        self.EXPLICIT_WAIT_TIME = 25
        self.client = utils.getAttribute('common', 'mainClient')

    def setup_menu(self, PlugName, ModelNo):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.set_up(PlugName, ModelNo)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.set_up(PlugName, ModelNo)

    def plugnavigation(self, PlugName):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.navigation_to_plugpage(PlugName)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.navigation_to_plugpage(PlugName)

    def validate_title(self, PlugName):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_plugstitle(PlugName)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_plugstitle(PlugName)

    def verifyplugscreen(self, PlugName):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_plugstitle(PlugName)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_plugstitle(PlugName)

    def clickplug_toggle(self, PlugName):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_plugs_toggle(PlugName)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_plugs_toggle(PlugName)

    def verify_plugstate(self, PlugName):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_plugs_on_off(PlugName)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_plugs_on_off(PlugName)

    def verify_plugstate_dashboard_devicelist(self, PlugName):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_plugstate_dashboard(PlugName)
            oPlugsPage.verify_plugstate_devicelist(PlugName)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_plugstate_dashboard(PlugName)
            oPlugsPage.verify_plugstate_devicelist(PlugName)

    def click_plug_mode(self, PlugName):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_plugs_arrow(PlugName)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_plugs_arrow(PlugName)

    def verify_plugmode(self, PlugName):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_modechange(PlugName)
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_modechange(PlugName)

    def click_scheduleicon(self):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_scheduleicon()
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_scheduleicon()

    def verify_schedulescreen(self):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_schedulescreen()
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_schedulescreen()

    def click_recipesicon(self):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_recipesicon()
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_recipesicon()

    def verify_recipesscreen(self):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_recipesscreen()
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_recipesscreen()

    def click_controlicon(self):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_controlicon()
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.click_controlicon()

    def verify_controlscreen(self):
        if 'ANDROID' in self.client.upper():
            oPlugsPage = androidPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_controlscreen()
        elif 'IOS' in self.client.upper():
            oPlugsPage = iOSPage.PlugsPage(self.driver, self.reporter)
            oPlugsPage.verify_controlscreen()

    # Beekeeper Functions

    # Report the Failure step the HTML report
    def report_fail(self, strFailDescription, context):
        context.reporter.ActionStatus = False
        # self.reporter.ActionStatus = True
        context.reporter.ReportEvent('Test Validation', strFailDescription, "FAIL", 'Center', True)

    # Report the Pass step the HTML report
    def report_pass(self, strPassDescription, context):
        context.reporter.ActionStatus = True
        context.reporter.ReportEvent('Test Validation', strPassDescription, "PASS", 'Center', True)

    # Report the Done step the HTML report
    def report_done(self, strStepDescription, context):
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strStepDescription, "DONE", 'Center', True)

    # Report the Done step the HTML report
    def report_step(self, strStepDescription):
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strStepDescription, "DONE", 'Center', True)

    def beeUpdate(self, context):
        self.reporter = self.parentAPI.reporter
        self.apiLogin(context)
        self.beekeeperLogin(context)

    def makeRequest(self, oRequestList, strServerName, context, strRequest, strContact):

        for oRequest in oRequestList:
            oExtractReq = globals()['thermostatEndpoint'](context.oThermostatClass, strServerName,
                                                          context.oThermostatEP)
            oReq = getattr(oExtractReq, oRequest)
            self.reporter = self.parentAPI.reporter
            if oRequest.upper().find('API') >= 0:
                oReq(self, self.APIsession, context, strRequest)

            elif oRequest.upper().find('BEE') >= 0:
                oReq(self, self.BEEsession, context, strRequest, strContact)

    def validateBeekeeper(self, strRequest, strServerName, context):

        oFirstChar = strRequest[0].upper()
        oRemainingChar = strRequest[1:]
        oResponse = 'validate' + oFirstChar + oRemainingChar
        oExtractResp = globals()['thermostatEndpoint'](context.oThermostatClass, strServerName, context.oThermostatEP)
        # self.validateUserDetails(self, context)
        oResp = getattr(oExtractResp, oResponse)
        oResp(self, context, strRequest)

    # API Functions
    def apiLogin(self, context):
        ALAPI.createCredentials(self.serverName, self.client)
        self.APIsession = ALAPI.sessionObject()
        if not self.APIsession.sessionId is None:
            # self.reporter.ActionStatus = True
            self.report_done('API Login : Login the user via API and create a sessionID', context)
        else:
            self.report_fail('API Login : User session could not be created, please check API login', context)
        self.getUsersAPI(self.APIsession, context)
        return True

    def getUsersAPI(self, session, context):
        resp = ALAPI.getUsersV6(session)
        oNode = resp['users']
        try:
            for oNod in oNode:
                if 'https://api.prod.bgchprod.info:8443/omnia/users/' in oNod['href']:
                    # self.APIUsername = oNod['id']
                    self.APIUsername = oNod['username']
                    self.APIFirstName = oNod['firstName']
                    self.APICountryCode = oNod['countryCode']
                    self.APIUserid = oNod['id']
                    self.APILastName = oNod['lastName']
                    self.APIPostcode = oNod['postcode']
                    self.APIEmail = oNod['email']
                    self.APIMobile = oNod['mobile']
                    self.APIPhone = oNod['phone']
                    self.APITimeZone = oNod['timeZone']
                    self.APICountry = oNod['country']
                    self.APICountryCode = oNod['countryCode']
                    self.APILocale = oNod['locale']
                    self.APITemperatureUnit = oNod['temperatureUnit']
                    # self.APIStatus = ''
                    self.APIFailuresEmail = oNod['alertSettings']['failuresEmail']
                    self.APIFailuresSMS = oNod['alertSettings']['failuresSMS']
                    self.APIWarningsEmail = oNod['alertSettings']['warningsEmail']
                    self.APIWarningsSMS = oNod['alertSettings']['warningsSMS']
                    self.APINightAlerts = oNod['alertSettings']['nightAlerts']

                    # print(self.APIUsername, oFirstName, oCountryCode)
                    self.report_done('API Login : Fetch the User Details from API', context)
            return True
        except:
            self.report_fail('API Login : Exception thrown in getUsersAPI() method', context)

    def getNodesAPI(self, oself1, session, context, strRequest):

        resp = ALAPI.getNodesV6(session)

        oNodeTypeList = []
        oUniqueProdCountDict = {}
        # oAllProdDictAPI = {}

        for oNode in resp['nodes']:
            if 'nodeType' in oNode:
                print(oNode['nodeType'])

        for oNode in resp['nodes']:

            if 'nodeType' in oNode:
                if 'class.synthetic' in oNode['nodeType']:
                    print('It is a Synthetic device and hence removed from list - %s' % oNode['nodeType'])

                elif 'class.thermostatui.json' in oNode['nodeType']:
                    oNodeTypeList.append('thermostatui')
                elif 'class.smartplug.json' in oNode['nodeType']:
                    if 'model' in oNode['attributes']:
                        if 'SLP2' in oNode['attributes']['model']['reportedValue']:
                            oNodeTypeList.append('activeplug')
                        else:
                            oNodeTypeList.append('smartplug')
                    else:
                        oNodeTypeList.append('smartplug')
                elif 'class.light.json' in oNode['nodeType']:
                    oNodeTypeList.append('warmwhitelight')
                elif 'class.tunable.light.json' in oNode['nodeType']:
                    oNodeTypeList.append('tuneablelight')
                elif 'class.colour.tunable.light.json' in oNode['nodeType']:
                    oNodeTypeList.append('colourtuneablelight')
                elif 'class.motion.sensor.json' in oNode['nodeType']:
                    oNodeTypeList.append('motionsensor')
                elif 'class.contact.sensor' in oNode['nodeType']:
                    oNodeTypeList.append('contactsensor')
                elif 'class.zigbee.range.extender' in oNode['nodeType']:
                    oNodeTypeList.append('signalbooster')
                # Need to add old booster plug

                # if strRequest.upper().find('DEVICES') >= 0:
                elif 'class.thermostat.json#' in oNode['nodeType'] \
                        and 'supportsHotWater' not in oNode['attributes']:
                    oNodeTypeList.append('boilermodule')

                elif 'class.thermostat.json#' in oNode['nodeType'] \
                        and oNode['attributes']['supportsHotWater']['reportedValue'] == False:
                    # oNodeTypeList.append('heating')
                    print('It is a HEAT node and hence removed from list - %s' % oNode['nodeType'])
                elif 'class.thermostat.json#' in oNode['nodeType'] \
                        and oNode['attributes']['supportsHotWater']['reportedValue'] == True:
                    # oNodeTypeList.append('hotwater')
                    print('It is a Hot water node and hence removed from list - %s' % oNode['nodeType'])

                # if strRequest.upper().find('DEVICES') >= 0:
                elif 'class.hub' in oNode['nodeType']:
                    oNodeTypeList.append('hub')

        print(oNodeTypeList)
        oSortedNodeTypeList = sorted(oNodeTypeList)
        print(oSortedNodeTypeList)
        oSetNodeTypeList = set(oSortedNodeTypeList)
        oSortedSetNodeTypeList = sorted(set(oSortedNodeTypeList))
        oSortedSetNodeTypeListClone = sorted(set(oSortedNodeTypeList))

        if len(oSortedNodeTypeList) != len(oSetNodeTypeList):
            print('List has duplicate Values')
            # oSortedSetNodeTypeList = sorted(set(oSortedNodeTypeList))
            print(oSortedSetNodeTypeList)

            for oEachType in oSortedSetNodeTypeList:
                oCount = oSortedNodeTypeList.count(oEachType)
                oEachTypeCount = {oEachType: oCount}
                oUniqueProdCountDict.update(oEachTypeCount)
                # oSortedTypeList.
            print(oUniqueProdCountDict)

        else:
            for oEach in oSortedNodeTypeList:
                oCount = oSortedNodeTypeList.count(oEach)
                oEachCount = {oEach: oCount}
                oUniqueProdCountDict.update(oEachCount)
                # oSortedTypeList.
            print(oUniqueProdCountDict)

        oListLen = len(oSortedSetNodeTypeList)

        i = 0
        while i < oListLen:
            oType = oSortedSetNodeTypeList[i]
            if oUniqueProdCountDict[oType] != 1:
                oSortedSetNodeTypeList.remove(oType)
                oListLen = oListLen - 1
                # oSortedSetNodeTypeList[i] = oSortedSetNodeTypeList[i] + str(i+1)
                j = 0
                while j < oUniqueProdCountDict[oType]:
                    oTypeCount = oType + str(j + 1)
                    oSortedSetNodeTypeList.append(oTypeCount)
                    j = j + 1
                    print('First while done')
                    print(oSortedSetNodeTypeList)
                i = i - 1

            i = i + 1

        oAPIDeviceDictFresh = {  # "id": '',
            "type": '',
            "parent": '',
            # Props
            "online": '',
            "model": '',
            "version": '',
            "mcu": '',
            "zb": '',
            "ipAddress": '',
            "uptime": '',
            "connection": '',
            "power": '',
            "tui": '',

            # Need to check for capabilities
            # Holiday mode
            # "enabled(holiday)": oProduct.APIHolidayEnabled,
            # "start(holiday)": oProduct.APIHolidayStart,
            # "end(holiday)": oProduct.APIHolidayEnd,
            # "temperature(holiday)": oProduct.APIHolidayTemp,
            # "maxEvents": oProduct.APIMaxEvents,
            "pmz": '',
            # previous
            # "mode(previous)": oProduct.APIPreviousMode,
            # "scheduleOverride": oProduct.APIScheduleOverride,
            # "temperature(Inside)": oProduct.APIInsidetemperature,
            # "zone(id)": oProduct.APIZoneid,
            # state
            # "name": '',
            "zoneName": '',
            # "capabilities"
            # "boost": '',
            # "frostProtection": oProduct.APIFrostProtection,
            # "mode": oProduct.APIDeviceMode,
            # Schedule to be done here
            # "target(Targ)": oProduct.APITargTemp,
            # "status": oProduct.APIProdStatus,
            "manufacturer": '',
            "power": '',
            "signal": '',
            "battery": ''
        }

        print(oSortedSetNodeTypeList)
        # oAllProdDictAPI = dict([(key, oAPIDeviceDictFresh) for key in oSortedSetNodeTypeList])
        oself1.oAllProdDictAPI = dict([(key, {}) for key in oSortedSetNodeTypeList])
        print(oself1.oAllProdDictAPI)
        oSortedSetNodeTypeList = sorted(oSortedSetNodeTypeList)

        i = 0
        # oCountTracker = 0
        while i < len(oSortedSetNodeTypeListClone):
            oType = oSortedSetNodeTypeListClone[i]
            if oUniqueProdCountDict[oType] != 1:
                oDeviceNameList = []
                oDeviceIDList = []
                oDeviceNameDict = {}
                oDeviceIDDict = {}
                for oNode in resp['nodes']:
                    if 'nodeType' in oNode:
                        if oType in self.nodeTypeDict:
                            if self.nodeTypeDict[oType] in oNode['nodeType']:
                                if oType == 'boilermodule':
                                    if 'supportsHotWater' not in oNode['attributes']:
                                        oAPIDeviceName = oNode['name']
                                        oAPIDeviceID = oNode['id']

                                elif oType == 'activeplug':
                                    if 'model' in oNode['attributes']:
                                        if 'SLP2' in oNode['attributes']['model']['reportedValue']:
                                            oAPIDeviceName = oNode['name']
                                            oAPIDeviceID = oNode['id']

                                else:
                                    oAPIDeviceName = oNode['name']
                                    oAPIDeviceID = oNode['id']

                                oDeviceNameList.append(oAPIDeviceName)
                                oDeviceIDList.append(oAPIDeviceID)
                oDeviceNameList = sorted(oDeviceNameList)
                oDeviceIDList = sorted(oDeviceIDList)
                print(oDeviceNameList, oDeviceIDList)

                oCountTracker = 0
                for oName in oDeviceNameList:
                    oCount = oDeviceNameList.count(oName)
                    if oCount != 1: oCountTracker += 1
                    oEachNameCount = {oName: oCount}
                    oDeviceNameDict.update(oEachNameCount)
                print(oDeviceNameDict)

                if oCountTracker == 0:
                    print('No repeated names')
                    l = 0
                    while l < len(oDeviceNameList):
                        oTypeCount1 = oType + str(l + 1)
                        oself1.oAllProdDictAPI[oTypeCount1]['name'] = oDeviceNameList[l]
                        self.createAllProdDictAPI(oself1, resp, context, oTypeCount1, strRequest,
                                                  oName=oDeviceNameList[l])
                        # print(oAllProdDictAPI)
                        l = l + 1
                else:
                    print('Repeated names')
                    k = 0
                    while k < len(oDeviceIDList):
                        oTypeCount2 = oType + str(k + 1)
                        oCurrentProdDictAPI = oself1.oAllProdDictAPI[oTypeCount2]
                        oCurrentProdDictAPI['id'] = oDeviceIDList[k]
                        self.createAllProdDictAPI(oself1, resp, context, oTypeCount2, strRequest, oID=oDeviceIDList[k])
                        print(oself1.oAllProdDictAPI)
                        k = k + 1

                        # print (oAllProdDictAPI)


                        # oCallCounter = 0
                        # while (oCallCounter < oUniqueProdCountDict[oType])
                        #    self.createAllProdDictAPI(resp, oAllProdDictAPI, context, oType)
                        #    oCallCounter += 1


            else:
                print("Product is single")
                self.createAllProdDictAPI(oself1, resp, context, oType, strRequest)
                # print(oAllProdDictAPI)

            i = i + 1

        print(oself1.oAllProdDictAPI)

        oself1.report_done('Details fetched from API through getNodes()', context)

        oself1.APIAllProductsDict = oself1.oAllProdDictAPI
        return oself1

    def createAllProdDictAPI(self, oself1, resp, context, oTypeCount, strRequest, oName='', oID=''):

        oType = oTypeCount
        if not oName is '' or not oID is '':
            oType = oTypeCount[:(len(oTypeCount) - 1)]

        for oNode in resp['nodes']:

            if 'nodeType' in oNode:
                if oType in self.nodeTypeDict:
                    if self.nodeTypeDict[oType] in oNode['nodeType']:
                        if oType == 'smartplug':
                            if not 'model' in oNode['attributes'] or \
                                    not 'SLP2' in oNode['attributes']['model']['reportedValue']:
                                self.setNameAndID(oself1, oNode, context, oType, oTypeCount, strRequest, oName, oID)

                        elif oType == 'activeplug':
                            if 'model' in oNode['attributes']:
                                self.setNameAndID(oself1, oNode, context, oType, oTypeCount, strRequest, oName, oID)

                        else:
                            self.setNameAndID(oself1, oNode, context, oType, oTypeCount, strRequest, oName, oID)


            else:
                print('TYPE is missing for %s' % oTypeCount)

        return oself1

    def setNameAndID(self, oself1, oNode, context, oType, oTypeCount, strRequest, oName, oID):
        if not oName is '' and oID is '':
            if oName == oNode['name']:
                # oAPIDeviceID = oNode['id']
                oself1.oAllProdDictAPI[oTypeCount]['id'] = oNode['id']
                self.pendingDictAPI(oself1, oNode, context, oTypeCount, strRequest)

        elif oName is '' and not oID is '':
            if oID == oNode['id']:
                # oAPIDeviceID = oNode['id']
                oself1.oAllProdDictAPI[oTypeCount]['name'] = oNode['name']
                self.pendingDictAPI(oself1, oNode, context, oTypeCount, strRequest)

        elif oName is '' and oID is '':

            # oAPIDeviceName = oNode['name']
            oself1.oAllProdDictAPI[oType]['name'] = oNode['name']
            oself1.oAllProdDictAPI[oType]['id'] = oNode['id']
            self.pendingDictAPI(oself1, oNode, context, oType, strRequest)

        return oself1

    def pendingDictAPI(self, oself1, oNode, context, oType, strRequest):

        if 'parentNodeId' in oNode:
            # oAPIDeviceParentID = oNode['parentNodeId']
            oself1.oAllProdDictAPI[oType]['parent'] = oNode['parentNodeId']
        else:
            print('parentNodeID is missing')

        oAttributeList = oNode['attributes']

        # if not 'class.thermostat.json#' in oNode['nodeType']:


        if 'presence' in oAttributeList:
            oself1.oAllProdDictAPI[oType]['props[online]'] = oAttributeList['presence']['reportedValue']

        if 'softwareVersion' in oAttributeList:
            oself1.oAllProdDictAPI[oType]['props[version]'] = oAttributeList['softwareVersion']['reportedValue']
        if 'model' in oAttributeList:
            oself1.oAllProdDictAPI[oType]['props[model]'] = oAttributeList['model']['reportedValue']
        # if oType == 'motionsensor':
        #    if 'inMotion' in oAttributeList:
        #        oself1.oAllProdDictAPI[oType]['motion[status]'] = oAttributeList['inMotion']['reportedValue']
        # else:
        #    if 'state' in oAttributeList:
        #        oself1.oAllProdDictAPI[oType]['state'] = oAttributeList['state']['reportedValue']
        if 'manufacturer' in oAttributeList:
            oself1.oAllProdDictAPI[oType]['props[manufacturer]'] = oAttributeList['manufacturer']['reportedValue']

        if strRequest.upper().find('DEVICES') >= 0:

            if 'powerSupply' in oAttributeList:
                oself1.oAllProdDictAPI[oType]['props[power]'] = oAttributeList['powerSupply']['reportedValue']
            if 'batteryLevel' in oAttributeList:
                oself1.oAllProdDictAPI[oType]['props[battery]'] = oAttributeList['batteryLevel']['reportedValue']
            if 'LQI' in oAttributeList:
                oself1.oAllProdDictAPI[oType]['props[signal]'] = oAttributeList['LQI']['reportedValue']

            # Hub
            if oType == 'hub':
                if 'hardwareVersion' in oAttributeList:
                    oself1.oAllProdDictAPI[oType]['props[model]'] = oAttributeList['hardwareVersion']['reportedValue']

            if 'connection' in oAttributeList:
                oself1.oAllProdDictAPI[oType]['props[connection]'] = oAttributeList['connection']['reportedValue']
            if 'uptime' in oAttributeList:
                oself1.oAllProdDictAPI[oType]['props[uptime]'] = oAttributeList['uptime']['reportedValue']

        # thermostatui and boilermodule
        if 'relationships' in oAttributeList:
            oRelationshipAttribute = oAttributeList['relationships']['boundNodes']
            oself1.oAllProdDictAPI[oType]['props[zone]'] = oRelationshipAttribute['id']

        # boilermodule
        if 'zoneName' in oAttributeList:
            oself1.oAllProdDictAPI[oType]['state[zoneName]'] = oAttributeList['zoneName']['reportedValue']
            # oself1.oAllProdDictAPI[oType]['state[zone]'] = oNode['id']
















            # self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)


            # except:
            #    strException = 'Exception in ' + oself1.APIProductType + 'product node'
            #    print(strException)

        '''

        if 'class.thermostat.json#' in oNode['nodeType'] \
                and 'supportsHotWater' not in oAttributeList:
            # try:

            oself1.APIPresenceStatus = oAttributeList['presence']['reportedValue']
            oJson = oAttributeList['holidayMode']['reportedValue']
            if isinstance(oJson, str): oJson = json.loads(oJson)
            oself1.APIHolidayEnabled = oJson['enabled']
            oself1.APIHolidayTemp = oJson['targetHeatTemperature']
            oself1.APIHolidayStart = oJson['startDateTime']
            oself1.APIHolidayEnd = oJson['endDateTime']

            oself1.APIZoneName = oAttributeList['zoneName']['reportedValue']

            oself1.APIDeviceVersion = oAttributeList['softwareVersion']['reportedValue']
            oself1.APIDeviceModel = oNode['attributes']['model']['reportedValue']

            # oself1.APIProductType = 'heating'
            self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)

            # oself1.APIProductType = 'hotwater'
            self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)

            #                    except:
            #                       print ('Exception in General BM node')


            # self.createAPIProductDict(oself1, context, 'heating', oAPIAllProductsDict)
            # self.createAPIProductDict(oself1, context, 'hotwater', oAPIAllProductsDict)


        elif 'class.thermostat.json#' in oNode['nodeType'] \
                and oAttributeList['supportsHotWater']['reportedValue'] == False:
            try:
                oself1.APIProductID = oNode['id']
                oself1.APIParentNodeID = oNode['parentNodeId']
                oself1.APITargTemp = oAttributeList['targetHeatTemperature']['reportedValue']
                oself1.APIFrostProtection = oAttributeList['frostProtectTemperature']['reportedValue']
                oself1.APIScheduleOverride = oAttributeList['activeOverrides']['reportedValue']
                oself1.APIInsidetemperature = oAttributeList['temperature']['reportedValue']
                oJson = oAttributeList['previousConfiguration']['reportedValue']
                if isinstance(oJson, str): oJson = json.loads(oJson)
                oself1.APIPreviousMode = oJson['mode']

                oself1.APIZoneid = oself1.APIParentNodeID
                oself1.APIProdStatus = ''
                # oself1.APIProductType = 'heating'
                # Mode needs to be done yet
                # Boost

                self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)
            except:
                print('Exception in Heat node')




        elif 'class.thermostat.json#' in oNode['nodeType'] \
                and oAttributeList['supportsHotWater']['reportedValue'] == True:
            try:
                oself1.APIProductID = oNode['id']
                oself1.APIParentNodeID = oNode['parentNodeId']
                oself1.APIPreviousMode = oAttributeList['previousConfiguration']['reportedValue']  # ['mode']
                oself1.APIProdStatus = oAttributeList['stateHotWaterRelay']['reportedValue']
                oself1.APIHolidayTemp = ''

                oself1.APITargTemp = ''
                oself1.APIFrostProtection = ''
                oself1.APIScheduleOverride = ''
                oself1.APIInsidetemperature = ''
                oself1.APIZoneid = oself1.APIParentNodeID

                # oself1.APIProductType = 'hotwater'

                # Mode needs to be done yet
                # Boost
                self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)

        '''

        return oself1
        # print (oAllProdDictAPI)

    def getNodesAPIforGetProducts(self, oself1, session, context):

        resp = ALAPI.getNodesV6(session)

        oTypeList = []
        oUniqueProdCountDict = {}
        oAPIAllProductsDict = {}

        for oNode in resp['nodes']:
            if 'nodeType' in oNode:
                if 'class.synthetic' in oNode['nodeType']:
                    print(oNode['nodeType'])
                elif 'class.hub' in oNode['nodeType']:
                    print(oNode['nodeType'])
                elif 'thermostatui.json' in oNode['nodeType']:
                    print(oNode['nodeType'])
                elif 'class.zigbee.range.extender' in oNode['nodeType']:
                    print(oNode['nodeType'])
                elif 'class.thermostat.json#' in oNode['nodeType'] \
                        and 'supportsHotWater' not in oNode['attributes']:
                    print(oNode['nodeType'])

                elif 'class.smartplug.json' in oNode['nodeType']:
                    oTypeList.append('activeplug')
                    # oTypeList[oInvalid] = 'activeplug'
                elif 'class.light.json' in oNode['nodeType']:
                    oTypeList.append('warmwhitelight')
                elif 'class.tunable.light.json' in oNode['nodeType']:
                    oTypeList.append('tunablelight')
                elif 'class.colour.tunable.light.json' in oNode['nodeType']:
                    oTypeList.append('colourlight')
                elif 'class.motion.sensor.json' in oNode['nodeType']:
                    oTypeList.append('motionsensor')
                elif 'class.contact.sensor' in oNode['nodeType']:
                    oTypeList.append('contactsensor')
                elif 'class.thermostat.json#' in oNode['nodeType'] \
                        and oNode['attributes']['supportsHotWater']['reportedValue'] == False:
                    oTypeList.append('heating')
                elif 'class.thermostat.json#' in oNode['nodeType'] \
                        and oNode['attributes']['supportsHotWater']['reportedValue'] == True:
                    oTypeList.append('hotwater')

        print('----------------------')
        oSortedTypeList = sorted(oTypeList)
        print(oSortedTypeList)

        if len(oSortedTypeList) != len(set(oSortedTypeList)):
            print('List has duplicate Values')
            oSetList = sorted(set(oSortedTypeList))
            # oSortedSetList =
            print(oSetList)

            for oEach in oSetList:
                oCount = oSortedTypeList.count(oEach)
                oEachCount = {oEach: oCount}
                oUniqueProdCountDict.update(oEachCount)
                # oSortedTypeList.
            print(oUniqueProdCountDict)

        else:
            for oEach in oSortedTypeList:
                oCount = oSortedTypeList.count(oEach)
                oEachCount = {oEach: oCount}
                oUniqueProdCountDict.update(oEachCount)
                # oSortedTypeList.
            print(oUniqueProdCountDict)

        ApiTypeCount = 0
        oTypeListFinal = []
        oAPICurrentProductDict = {}

        while ApiTypeCount < (len(oSetList)):
            if oUniqueProdCountDict[oSetList[ApiTypeCount]] > 1:
                oCount1 = 0
                while oCount1 < oUniqueProdCountDict[oSetList[ApiTypeCount]]:
                    strTypeCount = oSetList[ApiTypeCount] + str(oCount1 + 1)
                    oTypeListFinal.append(strTypeCount)
                    oCount1 = oCount1 + 1

            else:
                oTypeListFinal.append(oSetList[ApiTypeCount])

            ApiTypeCount = ApiTypeCount + 1

        print(oTypeListFinal)

        oAPIAllProductsDict = dict.fromkeys(oTypeListFinal, oAPICurrentProductDict)
        print(oAPIAllProductsDict)

        print('----------------------')
        print('----------------------')

        for oKey in oTypeListFinal:
            if oKey in oself1.BeeAllProductsDict:
                for oNode in resp['nodes']:
                    oAttributeList = oNode['attributes']
                    oself1.APIProductType = oKey
                    # oNodeType = oNode['nodeType']
                    # if 'nodeType' in oNode:

                    if oself1.BeeAllProductsDict[oKey]['id'] == oNode['id']:

                        try:

                            self.createAPIAlldict(oself1, oNode, context, oAttributeList, oAPIAllProductsDict)

                            '''
                            oself1.APIProductID = oNode['id']
                            oself1.APIParentNodeID = oNode['parentNodeId']
                            oself1.APIPresenceStatus = oAttributeList['presence']['reportedValue']
                            oself1.APIDeviceVersion = oAttributeList['softwareVersion']['reportedValue']
                            oself1.APIZoneName = oNode['name']
                            oself1.APIZoneid = ''
                            oself1.APIDeviceModel = oAttributeList['model']['reportedValue']
                            if oself1.APIProductType == 'motionsensor':
                                oself1.APIProdStatus = oAttributeList['inMotion']['reportedValue']
                            else:
                                oself1.APIProdStatus = oAttributeList['state']['reportedValue']
                            oself1.APIDeviceManufacturer = oAttributeList['manufacturer']['reportedValue']

                            oself1.APIHolidayEnabled = ''
                            oself1.APIHolidayTemp = ''
                            oself1.APIHolidayStart = ''
                            oself1.APIHolidayEnd = ''

                            oself1.APITargTemp = ''
                            oself1.APIFrostProtection = ''
                            oself1.APIScheduleOverride = ''
                            oself1.APIInsidetemperature = ''
                            oself1.APIPreviousMode = ''

                            oself1.APIMaxEvents = ''
                            oself1.APIPMZ = ''
                            oself1.APIBoost = ''
                            '''


                        except:
                            strP = 'Issues in getting details from ' + oKey
                            print(strP)

                            self.createAPIProductDict(oself1, context, oKey, oAPIAllProductsDict)


                            # else:
                            #    print ('This product is not found in Beekeeper Dict')
                            # else:
                            #    print ('nodeType is not found in this node')

                            # self.createAPIProductDict(oself1, context, oKey, oAPIAllProductsDict)

    def createAPIAlldict(self, oself1, oNode, context, oAttributeList, oAPIAllProductsDict):

        if not 'class.thermostat.json#' in oNode['nodeType']:

            try:

                '''

                if 'class.smartplug.json' in oNode['nodeType']:
                    oself1.APIProductType = 'activeplug'
                elif 'class.light.json' in oNode['nodeType']:
                    oself1.APIProductType = 'warmwhitelight'
                elif 'class.tunable.light.json' in oNode['nodeType']:
                    oself1.APIProductType = 'tunablelight'
                elif 'class.colour.tunable.light.json' in oNode['nodeType']:
                    oself1.APIProductType = 'colourlight'
                elif 'class.motion.sensor' in oNode['nodeType']:
                    oself1.APIProductType = 'motionsensor'
                elif 'class.contact.sensor' in oNode['nodeType']:
                    oself1.APIProductType = 'contactsensor'

                '''

                oself1.APIProductID = oNode['id']
                oself1.APIParentNodeID = oNode['parentNodeId']
                oself1.APIPresenceStatus = oAttributeList['presence']['reportedValue']
                oself1.APIDeviceVersion = oAttributeList['softwareVersion']['reportedValue']
                oself1.APIZoneName = oNode['name']
                oself1.APIZoneid = ''
                oself1.APIDeviceModel = oAttributeList['model']['reportedValue']
                if oself1.APIProductType == 'motionsensor':
                    oself1.APIProdStatus = oAttributeList['inMotion']['reportedValue']
                else:
                    oself1.APIProdStatus = oAttributeList['state']['reportedValue']
                oself1.APIDeviceManufacturer = oAttributeList['manufacturer']['reportedValue']

                oself1.APIHolidayEnabled = ''
                oself1.APIHolidayTemp = ''
                oself1.APIHolidayStart = ''
                oself1.APIHolidayEnd = ''

                oself1.APITargTemp = ''
                oself1.APIFrostProtection = ''
                oself1.APIScheduleOverride = ''
                oself1.APIInsidetemperature = ''
                oself1.APIPreviousMode = ''

                oself1.APIMaxEvents = ''
                oself1.APIPMZ = ''
                oself1.APIBoost = ''

                # Mode

                self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)


            except:
                strException = 'Exception in ' + oself1.APIProductType + 'product node'
                print(strException)

        if 'class.thermostat.json#' in oNode['nodeType'] \
                and 'supportsHotWater' not in oAttributeList:
            # try:

            oself1.APIPresenceStatus = oAttributeList['presence']['reportedValue']
            oJson = oAttributeList['holidayMode']['reportedValue']
            if isinstance(oJson, str): oJson = json.loads(oJson)
            oself1.APIHolidayEnabled = oJson['enabled']
            oself1.APIHolidayTemp = oJson['targetHeatTemperature']
            oself1.APIHolidayStart = oJson['startDateTime']
            oself1.APIHolidayEnd = oJson['endDateTime']

            oself1.APIZoneName = oAttributeList['zoneName']['reportedValue']

            oself1.APIDeviceVersion = oAttributeList['softwareVersion']['reportedValue']
            oself1.APIDeviceModel = oNode['attributes']['model']['reportedValue']

            # oself1.APIProductType = 'heating'
            self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)

            # oself1.APIProductType = 'hotwater'
            self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)

        # except:
        #                       print ('Exception in General BM node')


        # self.createAPIProductDict(oself1, context, 'heating', oAPIAllProductsDict)
        # self.createAPIProductDict(oself1, context, 'hotwater', oAPIAllProductsDict)


        elif 'class.thermostat.json#' in oNode['nodeType'] \
                and oAttributeList['supportsHotWater']['reportedValue'] == False:
            try:
                oself1.APIProductID = oNode['id']
                oself1.APIParentNodeID = oNode['parentNodeId']
                oself1.APITargTemp = oAttributeList['targetHeatTemperature']['reportedValue']
                oself1.APIFrostProtection = oAttributeList['frostProtectTemperature']['reportedValue']
                oself1.APIScheduleOverride = oAttributeList['activeOverrides']['reportedValue']
                oself1.APIInsidetemperature = oAttributeList['temperature']['reportedValue']
                oJson = oAttributeList['previousConfiguration']['reportedValue']
                if isinstance(oJson, str): oJson = json.loads(oJson)
                oself1.APIPreviousMode = oJson['mode']

                oself1.APIZoneid = oself1.APIParentNodeID
                oself1.APIProdStatus = ''
                # oself1.APIProductType = 'heating'
                # Mode needs to be done yet
                # Boost

                self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)
            except:
                print('Exception in Heat node')




        elif 'class.thermostat.json#' in oNode['nodeType'] \
                and oAttributeList['supportsHotWater']['reportedValue'] == True:
            try:

                oself1.APIProductID = oNode['id']
                oself1.APIParentNodeID = oNode['parentNodeId']
                oself1.APIPreviousMode = oAttributeList['previousConfiguration']['reportedValue']  # ['mode']
                oself1.APIProdStatus = oAttributeList['stateHotWaterRelay']['reportedValue']
                oself1.APIHolidayTemp = ''

                oself1.APITargTemp = ''
                oself1.APIFrostProtection = ''
                oself1.APIScheduleOverride = ''
                oself1.APIInsidetemperature = ''
                oself1.APIZoneid = oself1.APIParentNodeID

                # oself1.APIProductType = 'hotwater'

                # Mode needs to be done yet
                # Boost
                self.createAPIProductDict(oself1, context, oself1.APIProductType, oAPIAllProductsDict)

            except:
                print('Exception in Hotwater node')









                # oself1.APIMaxEvents = ''
                # oself1.APIPMZ = ''
                # oself1.APIBoost = ''

        # print(oAPIAllProductsDict)

        print('-----------------------------------------')
        print('-----------------------------------------')
        print('-----------------------------------------')
        print('-----------------------------------------')
        print('-----------------------------------------')

        oself1.report_done('API Request : Getting all existing products detail from API through getNodes()', context)
        return oself1

    def createAPIProductDict(self, oProduct, context, productType, oAPIAllProductsDict):

        self.APIProductDict = {"id": oProduct.APIProductID,
                               "type": oProduct.APIProductType,
                               "parent": oProduct.APIParentNodeID,
                               # Props
                               "online": oProduct.APIPresenceStatus,
                               "model": oProduct.APIDeviceModel,
                               "version": oProduct.APIDeviceVersion,
                               # Need to check for capabilities
                               # Holiday mode
                               "enabled(holiday)": oProduct.APIHolidayEnabled,
                               "start(holiday)": oProduct.APIHolidayStart,
                               "end(holiday)": oProduct.APIHolidayEnd,
                               "temperature(holiday)": oProduct.APIHolidayTemp,
                               "maxEvents": oProduct.APIMaxEvents,
                               "pmz": oProduct.APIPMZ,
                               # previous
                               "mode(previous)": oProduct.APIPreviousMode,
                               "scheduleOverride": oProduct.APIScheduleOverride,
                               "temperature(Inside)": oProduct.APIInsidetemperature,
                               "zone(id)": oProduct.APIZoneid,
                               # state
                               "name": oProduct.APIZoneName,
                               "boost": oProduct.APIBoost,
                               "frostProtection": oProduct.APIFrostProtection,
                               "mode": oProduct.APIDeviceMode,
                               # Schedule to be done here
                               "target(Targ)": oProduct.APITargTemp,
                               "status": oProduct.APIProdStatus
                               }
        oAPICurrentProductDict = {productType: self.APIProductDict}
        oAPIAllProductsDict.update(oAPICurrentProductDict)
        print(oAPIAllProductsDict)
        print('-----------------------------------------')
        print('-----------------------------------------')
        print('-----------------------------------------')
        strDesciption = 'API Request : Getting' + productType + 'Product details'
        oProduct.report_done(strDesciption, context)
        oProduct.report_done('API Request : Getting all existing products detail from API through getNodes()', context)
        return oProduct, oAPIAllProductsDict

    # Beekeeper Functions:
    def beekeeperLogin(self, context):

        ALBKP.createCredentialsBeekeeper(self.serverName, self.client)
        self.BEEsession = ALBKP.sessionObject()
        if not self.BEEsession.sessionId is None:
            self.report_done('BEEKEEPER Login : Login the user via Beekeeper and create sessionID', context)
        else:
            self.report_fail('BEEKEEPER Login : User session could not be created, please check the Beekeeper login',
                             context)

        self.BeeUsername = self.BEEsession.userName
        self.BeeUserid = self.BEEsession.userId
        self.BeeFirstName = self.BEEsession.firstName
        self.BeeLastName = self.BEEsession.lastName
        self.BeePostcode = self.BEEsession.postcode
        self.BeeEmail = self.BEEsession.email
        self.BeeMobile = self.BEEsession.mobile
        self.BeePhone = self.BEEsession.phone
        self.BeeTimeZone = self.BEEsession.timezone
        self.BeeCountry = self.BEEsession.country
        self.BeeCountryCode = self.BEEsession.countryCode
        self.BeeLocale = self.BEEsession.locale
        self.BeeTemperatureUnit = self.BEEsession.temperatureUnit
        self.BeeFailuresEmail = self.BEEsession.failuresEmail
        self.BeeFailuresSMS = self.BEEsession.failuresSMS
        self.BeeWarningsEmail = self.BEEsession.warningsEmail
        self.BeeWarningsSMS = self.BEEsession.warningsSMS
        self.BeeNightAlerts = self.BEEsession.nightAlerts

        return True

    def getProductsBEE(self, oProduct, session, context, strRequest, strContact):
        # try:
        resp = ALBKP.getProductsBEE(session)
        self.getRequestStart(oProduct, session, context, strRequest, resp)

    def getDevicesBEE(self, oProduct, session, context, strRequest, strContact):

        resp = ALBKP.getDevicesBEE(session)
        self.getRequestStart(oProduct, session, context, strRequest, resp)

    def getCountForEachElement(self, oProduct, oSortedTypeList, oUniqueProdCountDict):

        if len(oSortedTypeList) != len(set(oSortedTypeList)):
            print('List has duplicate Values')
            oProduct.oSetList = sorted(set(oSortedTypeList))
            # oSortedSetList =
            print(oProduct.oSetList)
            for oEach in oProduct.oSetList:
                oCount = oSortedTypeList.count(oEach)
                oEachCount = {oEach: oCount}
                oUniqueProdCountDict.update(oEachCount)
                # oSortedTypeList.
            print(oUniqueProdCountDict)

        else:
            print('List does not have duplicate Values')
            oProduct.oSetList = sorted(set(oSortedTypeList))
            for oEach in oProduct.oSetList:
                oCount = oSortedTypeList.count(oEach)
                oEachCount = {oEach: oCount}
                oUniqueProdCountDict.update(oEachCount)
                # oSortedTypeList.
            print(oUniqueProdCountDict)
        oListLen = len(oProduct.oSetList)

        i = 0
        while i < oListLen:
            # oSetList = sorted(oSetList)
            oType = oProduct.oSetList[i]
            if oUniqueProdCountDict[oType] != 1:
                oProduct.oSetList.remove(oType)
                oListLen = oListLen - 1
                # oSortedSetNodeTypeList[i] = oSortedSetNodeTypeList[i] + str(i+1)
                j = 0
                while j < oUniqueProdCountDict[oType]:
                    oTypeCount = oType + str(j + 1)
                    oProduct.oSetList.append(oTypeCount)
                    j = j + 1
                    print('First while done')
                    print(oProduct.oSetList)
                i = i - 1

            i = i + 1

        return oListLen, oUniqueProdCountDict, oProduct

    def getRequestStart(self, oProduct, session, context, strRequest, resp):

        oProduct.BeeAllProductsDict = {}
        oProduct.BeeTypeCount = 0
        i = 0
        oTypeList = []
        oUniqueProdCountDict = {}
        # oSetList = []
        # oAllProdDictBEE = {}
        oTypeList1 = []

        for oNode in resp:
            if 'type' in oNode:
                oTypeList.append((oNode['type']))
            else:
                print('Node TYPE is missing in Beekeeper response for one of the products, please check')
        print(oTypeList)
        oSortedTypeList = sorted(oTypeList)
        print(oSortedTypeList)
        oSetListClone = sorted(set(oSortedTypeList))
        self.getCountForEachElement(oProduct, oSortedTypeList, oUniqueProdCountDict)

        oProduct.oAllProdDictBEE = dict([(key, {}) for key in oProduct.oSetList])
        print(oProduct.oAllProdDictBEE)

        oProduct.BeeTypeCount = 0

        # while (oProduct.BeeTypeCount < len(oSortedTypeList)):
        while oProduct.BeeTypeCount < len(oSetListClone):

            oType = oSetListClone[oProduct.BeeTypeCount]

            if oUniqueProdCountDict[oType] != 1:
                oNameList = []
                oIdList = []
                oDeviceNameDict = {}
                oDeviceIDDict = {}
                oTypeList1 = []
                oProdCount = oUniqueProdCountDict[oProduct.oSetList[oProduct.BeeTypeCount]]
                g = 1
                oProduct.oTypeList1Count = 0
                for oNode in resp:
                    if oSetListClone[oProduct.BeeTypeCount] == oNode['type']:
                        oProdName = oNode['state']['name']
                        oProdID = oNode['id']
                        oNameList.append(oProdName)
                        oIdList.append(oProdID)
                        # oType = oSetList[oProduct.BeeTypeCount] + str(g)
                        # oTypeList1.append(oType)
                        g = g + 1

                oNameList = sorted(oNameList)
                oTypeList1 = sorted(oTypeList1)
                oIdList = sorted(oIdList)

                print(oNameList)
                # print (oTypeList1)
                print(oIdList)

                oCountTracker = 0
                for oName in oNameList:
                    oCount = oNameList.count(oName)
                    if oCount != 1: oCountTracker += 1
                    oEachNameCount = {oName: oCount}
                    oDeviceNameDict.update(oEachNameCount)
                print(oDeviceNameDict)

                if oCountTracker == 0:
                    print('No repeated names')
                    l = 0
                    while l < len(oNameList):
                        oTypeCount1 = oType + str(l + 1)
                        oProduct.oAllProdDictBEE[oTypeCount1]['name'] = oNameList[l]
                        self.createAllProdDictBEE(oProduct, resp, context, oTypeCount1, oName=oNameList[l])
                        # print(oProduct.oAllProdDictBEE)
                        # print(oAllProdDictAPI)
                        l = l + 1
                else:
                    print('Repeated names')
                    k = 0
                    while k < len(oIdList):
                        oTypeCount2 = oType + str(k + 1)
                        oCurrentProdDictAPI = oProduct.oAllProdDictBEE[oTypeCount2]
                        oCurrentProdDictAPI['id'] = oIdList[k]
                        self.createAllProdDictBEE(oProduct, resp, context, oTypeCount2, oID=oIdList[k])

                        # print(oAllProdDictBEE)
                        k = k + 1



                        # for oName in oNameList:
                        #    self.creategetProductsBeeDict(oProduct, oSetList,  resp1, oUniqueProdCountDict, oTypeList1,  context, oName)
            else:
                #    self.creategetProductsBeeDict(oProduct, oSetList, resp1, oUniqueProdCountDict, oTypeList1,  context)
                self.createAllProdDictBEE(oProduct, resp, context, oType)
            oProduct.BeeTypeCount = oProduct.BeeTypeCount + 1

        print(oProduct.oAllProdDictBEE)
        print('Details fetched from Beekeeper for heating')
        oProduct.report_done('Details fetched from Beekeeper through getDevices()', context)

        oProduct.BEEAllProductsDict = oProduct.oAllProdDictBEE

        # print(oProduct.BeeAllProductsDict)

        return oProduct  # , oAllProductDict

    def createAllProdDictBEE(self, oProduct, resp, context, oTypeCount, oName='', oID=''):

        oType = oTypeCount
        if not oName is '' or not oID is '':
            oType = oTypeCount[:(len(oTypeCount) - 1)]

        for oNode in resp:

            if 'type' in oNode:
                if oType in oNode['type']:
                    if oType == oNode['type']:
                        if not oName is '' and oID is '':
                            if oName == oNode['state']['name']:
                                # oAPIDeviceID = oNode['id']
                                oProduct.oAllProdDictBEE[oTypeCount]['id'] = oNode['id']
                                self.pendingDictBEE(oProduct, oNode, context, oTypeCount)

                        elif oName is '' and not oID is '':
                            if oID == oNode['id']:
                                # oAPIDeviceID = oNode['id']
                                oProduct.oAllProdDictBEE[oTypeCount]['name'] = oNode['state']['name']
                                self.pendingDictBEE(oProduct, oNode, context, oTypeCount)

                        elif oName is '' and oID is '':

                            # oAPIDeviceName = oNode['name']
                            oProduct.oAllProdDictBEE[oType]['name'] = oNode['state']['name']
                            oProduct.oAllProdDictBEE[oType]['id'] = oNode['id']
                            self.pendingDictBEE(oProduct, oNode, context, oType)

            else:
                print('TYPE is missing for %s' % oTypeCount)

        return

    def pendingDictBEE(self, oProduct, oNode, context, oType):

        if 'parent' in oNode:
            # oAPIDeviceParentID = oNode['parentNodeId']
            oProduct.oAllProdDictBEE[oType]['parent'] = oNode['parent']
        else:
            print('parentNodeID is missing')

        oPropsList = oNode['props']
        oStateList = oNode['state']

        # if not 'boilermodule' in oNode['type'] or not 'thermostatui' in oNode['type']:
        if 'online' in oPropsList:
            if oPropsList['online']:

                oProduct.oAllProdDictBEE[oType]['props[online]'] = 'PRESENT'
            elif not oPropsList['online']:
                oProduct.oAllProdDictBEE[oType]['props[online]'] = 'ABSENT'

        if 'version' in oPropsList:
            oProduct.oAllProdDictBEE[oType]['props[version]'] = oPropsList['version']
        if 'model' in oPropsList:
            oProduct.oAllProdDictBEE[oType]['props[model]'] = oPropsList['model']
        # if oType == 'motionsensor':
        #    if 'inMotion' in oAttributeList:
        #        oProduct.oAllProdDictAPI[oType]['motion[status]'] = oAttributeList['inMotion']['reportedValue']
        # else:
        #    if 'state' in oAttributeList:
        #        oProduct.oAllProdDictAPI[oType]['state'] = oAttributeList['state']['reportedValue']
        if 'manufacturer' in oPropsList:
            oProduct.oAllProdDictBEE[oType]['props[manufacturer]'] = oPropsList['manufacturer']

        if 'power' in oPropsList:
            oProduct.oAllProdDictBEE[oType]['props[power]'] = oPropsList['power']
        if 'battery' in oPropsList:
            oProduct.oAllProdDictBEE[oType]['props[battery]'] = oPropsList['battery']
        if 'signal' in oPropsList:
            oProduct.oAllProdDictBEE[oType]['props[signal]'] = oPropsList['signal']

        # Hub
        if 'connection' in oPropsList:
            oProduct.oAllProdDictBEE[oType]['props[connection]'] = oPropsList['connection']
        if 'uptime' in oPropsList:
            oProduct.oAllProdDictBEE[oType]['props[uptime]'] = oPropsList['uptime']

        # thermostatui and boilermodule
        if 'zone' in oPropsList:
            # oRelationshipAttribute = oAttributeList['relationships']['boundNodes']
            oProduct.oAllProdDictBEE[oType]['props[zone]'] = oPropsList['zone']

            # boilermodule
            if 'zoneName' in oStateList:
                oProduct.oAllProdDictBEE[oType]['state[zoneName]'] = oStateList['zoneName']

    def creategetProductsBeeDict(self, oProduct, oSetList, resp1, oUniqueProdCountDict, oTypeList1, context, oName=''):

        for oNode in resp1:
            if oName != '':
                if oName == oNode['state']['name']:
                    self.creategetProductsBeeDictReal(oProduct, oSetList, oUniqueProdCountDict, oTypeList1, context,
                                                      oNode)
            else:
                self.creategetProductsBeeDictReal(oProduct, oSetList, oUniqueProdCountDict, oTypeList1, context, oNode)

    def creategetProductsBeeDictReal(self, oProduct, oSortedType, oUniqueProdCountDict, oTypeList1, context, oNode):

        if oSortedType[oProduct.BeeTypeCount] == oNode['type']:

            print('Product type is %s' % oSortedType[oProduct.BeeTypeCount])
            # if oNode['type'] == 'heating' or oNode['type'] == 'hotwater' or oNode['type'] == 'activeplug':

            oProduct.BeeProductID = oNode['id']
            oProduct.BeeProductType = oNode['type']
            oProduct.BeeParentNodeID = oNode['parent']
            oProduct.BeePresenceStatus = oNode['props']['online']
            # if oProduct.BeeDeviceStatus: oProduct.BeeDeviceStatus = 'PRESENT'
            # else: oProduct.BeeDeviceStatus = 'ABSENT'
            # oProduct.BeeDeviceModel = oNode['props']['model']
            oProduct.BeeDeviceVersion = oNode['props']['version']
            oProduct.BeeZoneName = oNode['state']['name']

            if oNode['type'] != 'motionsensor' and oNode['type'] != 'contactsensor':
                oProduct.BeeDeviceMode = oNode['state']['mode']
            else:
                oProduct.BeeDeviceMode = ''

            if oNode['type'] == 'heating' or oNode['type'] == 'hotwater':
                oProduct.BeeHolidayEnabled = oNode['props']['holidayMode']['enabled']
                oProduct.BeeHolidayStart = oNode['props']['holidayMode']['start']
                oProduct.BeeHolidayEnd = oNode['props']['holidayMode']['end']
                oProduct.BeeMaxEvents = oNode['props']['maxEvents']
                oProduct.BeePMZ = oNode['props']['pmz']
                oProduct.BeePreviousMode = oNode['props']['previous']['mode']
                oProduct.BeeZoneid = oNode['props']['zone']

                oProduct.BeeBoost = oNode['state']['boost']
            else:
                oProduct.BeeHolidayEnabled = False
                oProduct.BEEHolidayStart = ''
                oProduct.BeeHolidayEnd = ''
                oProduct.BeeMaxEvents = ''
                oProduct.BeePMZ = ''
                oProduct.BeePreviousMode = ''
                oProduct.BeeZoneid = ''

                oProduct.BeeBoost = ''

            if oNode['type'] == 'heating':
                oProduct.BeeTargTemp = oNode['state']['target']
                oProduct.frostProtection = oNode['state']['frostProtection']
                oProduct.BeeScheduleOverride = oNode['props']['scheduleOverride']
                oProduct.BeeInsidetemperature = oNode['props']['temperature']
                oProduct.BeeHolidayTemp = oNode['props']['holidayMode']['temperature']
            else:
                oProduct.BeeTargTemp = ''
                oProduct.frostProtection = ''
                oProduct.BeeScheduleOverride = False
                oProduct.BeeInsidetemperature = ''
                oProduct.BeeHolidayTemp = ''

            if oNode['type'] != 'heating' and oNode['type'] != 'motionsensor' and oNode['type'] != 'contactsensor':
                oProduct.BeeProdStatus = oNode['state']['status']
            else:
                oProduct.BeeProdStatus = ''

            self.BEEProductDict = {"id": oProduct.BeeProductID,
                                   "type": oProduct.BeeProductType,
                                   "parent": oProduct.BeeParentNodeID,
                                   # Props
                                   "online": oProduct.BeePresenceStatus,
                                   # "model": oProduct.BeeDeviceModel,
                                   "version": oProduct.BeeDeviceVersion,
                                   # Need to check for capabilities
                                   # Holiday mode
                                   "enabled(holiday)": oProduct.BeeHolidayEnabled,
                                   "start(holiday)": oProduct.BEEHolidayStart,
                                   "end(holiday)": oProduct.BeeHolidayEnd,
                                   "temperature(holiday)": oProduct.BeeHolidayTemp,
                                   "maxEvents": oProduct.BeeMaxEvents,
                                   "pmz": oProduct.BeePMZ,
                                   # previous
                                   "mode(previous)": oProduct.BeePreviousMode,
                                   "scheduleOverride": oProduct.BeeScheduleOverride,
                                   "temperature(Inside)": oProduct.BeeInsidetemperature,
                                   "zone(id)": oProduct.BeeZoneid,
                                   # state
                                   "name": oProduct.BeeZoneName,
                                   "boost": oProduct.BeeBoost,
                                   "frostProtection": oProduct.BeeFrostProtection,
                                   "mode": oProduct.BeeDeviceMode,
                                   # Schedule to be done here
                                   "target(Targ)": oProduct.BeeTargTemp,
                                   "status": oProduct.BeeProdStatus

                                   }

            if oUniqueProdCountDict[oSortedType[oProduct.BeeTypeCount]] != 1:
                # olen = len(oSortedType)
                # oMyProduct = oSortedType[oProduct.BeeTypeCount] + str(oProduct.BeeTypeCount + 1)
                # oSortedType[oProduct.BeeTypeCount] = oTypeList1[oProduct.oTypeList1Count]
                oCurrentProductDict = {oTypeList1[oProduct.oTypeList1Count]: self.BEEProductDict}
                oProduct.oTypeList1Count = oProduct.oTypeList1Count + 1

            else:
                oCurrentProductDict = {oSortedType[oProduct.BeeTypeCount]: self.BEEProductDict}
            # print (oCurrentProductDict)

            oProduct.BeeAllProductsDict.update(oCurrentProductDict)
            # print(oAllProductsDict)


            strDesciption = 'Beekeeper Request : Getting' + oSortedType[oProduct.BeeTypeCount] + 'Product details'

            oProduct.report_done(strDesciption, context)

            # elif oNode['type'] == 'hotwater':
            #    oProduct.report_done('Beekeeper Request : Getting Hot Water Product details', context)
        else:
            print('Product type not matching - so checking again')

        # oBeeTypeCount = oBeeTypeCount + 1

        return oProduct  # , oBeeTypeCount



        # except:
        #    oProduct.report_fail('Beekeeper Caller : Exception thrown in getProductsBEE() method', context)

    # Validation Functions
    def validateUserDetails(self, oself, context):

        # context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating User details')
        self.BEEUserDict = {"id": self.BeeUserid,
                            "username": self.BeeUsername,
                            "firstName": self.BeeFirstName,
                            "lastName": self.BeeLastName,
                            "postcode": self.BeePostcode,
                            "email": self.BeeEmail,
                            "mobile": self.BeeMobile,
                            "phone": self.BeePhone,
                            "timezone": self.BeeTimeZone,
                            "country": self.BeeCountry,
                            "countryCode": self.BeeCountryCode,
                            "locale": self.BeeLocale,
                            "temperatureUnit": self.BeeTemperatureUnit,
                            "failuresEmail": self.BeeFailuresEmail,
                            "failuresSMS": self.BeeFailuresSMS,
                            "warningsEmail": self.BeeWarningsEmail,
                            "warningsSMS": self.BeeWarningsSMS,
                            "nightAlerts": self.BeeNightAlerts
                            }

        self.APIUserDict = {"id": self.APIUserid,
                            "username": self.APIUsername,
                            "firstName": self.APIFirstName,
                            "lastName": self.APILastName,
                            "postcode": self.APIPostcode,
                            "email": self.APIEmail,
                            "mobile": self.APIMobile,
                            "phone": self.APIPhone,
                            "timezone": self.APITimeZone,
                            "country": self.APICountry,
                            "countryCode": self.APICountryCode,
                            "locale": self.APILocale,
                            "temperatureUnit": self.APITemperatureUnit,
                            "failuresEmail": self.APIFailuresEmail,
                            "failuresSMS": self.APIFailuresSMS,
                            "warningsEmail": self.APIWarningsEmail,
                            "warningsSMS": self.APIWarningsSMS,
                            "nightAlerts": self.APINightAlerts
                            }

        self.genericFunc(context, self.BEEUserDict, self.APIUserDict)

    def genericFunc(self, context, BEEUserDict, APIUserDict):

        BEEUserTup = sorted(BEEUserDict)
        APIUSerTup = sorted(APIUserDict)
        x = 0
        while x < len(BEEUserDict):
            try:
                if BEEUserDict[BEEUserTup[x]] == APIUserDict[APIUSerTup[x]]:

                    strHeader = "Attribute Validated$$" + "Value returned from Beekeeper and API response" + "@@@"
                    if not [APIUserDict[APIUSerTup[x]] == True and APIUserDict[APIUSerTup[x]] == False]:
                        strLog = strHeader + BEEUserTup[x] + '$$' + BEEUserDict[BEEUserTup[x]]
                    else:
                        strValue = str(BEEUserDict[BEEUserTup[x]])
                        strLog = strHeader + BEEUserTup[x] + '$$' + strValue
                    self.report_pass(strLog, context)
                else:
                    strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                    if not [APIUserDict[APIUSerTup[x]] == True and APIUserDict[APIUSerTup[x]] == False]:
                        strLog = strHeader + BEEUserTup[x] + '$$' + BEEUserDict[BEEUserTup[x]] + '$$' + \
                                 APIUserDict[APIUSerTup[x]]
                        self.report_fail(strLog, context)
                    else:
                        strBeeValue = str(BEEUserDict[BEEUserTup[x]])
                        strAPIValue = APIUserDict[APIUSerTup[x]]
                    strLog = strHeader + BEEUserTup[x] + '$$' + strBeeValue + '$$' + strAPIValue
                    self.report_fail(strLog, context)
                x = x + 1

            except:
                self.report_fail("Test Failed due to exception", context)
                x = x + 1

        return self

    def validateGetProducts(self, oProd, context, strRequest):
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating GetProducts() response from Beekeeper')

        x = oProd.APIAllProductsDict
        y = oProd.BEEAllProductsDict
        self.ValidateAndGetLog(oProd, strRequest, context, x, y)

    def validateGetDevices(self, oProd, context, strRequest):
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating GetDevices() response from Beekeeper')

        x = oProd.APIAllProductsDict
        y = oProd.BEEAllProductsDict
        oResponse = 'GetDevices'
        self.ValidateAndGetLog(oProd, strRequest, context, x, y)

        # x = {'hub': {'props[version]': '1.0.0-5222-2.0', 'name': 'Hub', 'id': '91a13336-34dc-4f7b-b921-6a467cfab01c', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'motionsensor': {'props[manufacturer]': 'AlertMe.com', 'name': 'shub/motion', 'id': '57394252-ade3-40a8-b988-b5a45c87af47', 'props[model]': 'PIR00140005', 'props[version]': '31005010', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'contactsensor2': {'props[manufacturer]': 'HiveHome.com', 'name': 'shub win/door', 'id': 'e61d60b4-f54b-4ab4-82b5-1d3505b36df3', 'props[model]': 'DWS003', 'props[version]': '01102603', 'props[online]': 'ABSENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'warmwhitelight': {'props[manufacturer]': 'Aurora', 'name': 'Shub wl', 'id': '177b9ab4-76c2-4d59-8d02-a04096a14cca', 'props[model]': 'FWBulb01', 'props[version]': '11250002', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'contactsensor1': {'a':'', 'props[manufacturer]': 'AlertM.com', 'name': 'Win/Door Sensor 2', 'id': 'e671e8eb-ba0d-46ff-bc14-4816ca909711', 'props[model]': 'WDS00140002', 'props[version]': '31005010', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'thermostatui': {}, 'boilermodule': {'name': 'Thermostat 2', 'id': 'f875bb4a-6748-435b-b279-a4149a8d7f73', 'parent': '24f0e38f-dae2-457f-a304-e4d34260f4a2'}, 'tunablelight': {'props[manufacturer]': 'Aurora', 'name': 'Shub Tl', 'id': 'ba5b5267-d509-40d7-b4e6-713eced775f5', 'props[model]': 'TWBulb01UK', 'props[version]': '11140002', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'activeplug': {'props[manufacturer]': 'Computime', 'name': 'Plug', 'id': '49227d93-87a1-498a-bfba-ce5ed82d96ea', 'props[model]': 'SLP2', 'props[version]': '02155120', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}}
        # y = {'tuneablelight': {'b' : True, 'props[manufacturer]': 'Aurora', 'name': 'Shub Tl', 'id': 'ba5b5267-d509-40d7-b4e6-713eced775f5', 'props[model]': 'TWBulb01UK', 'props[version]': '11140002', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'motionsensor': {'props[manufacturer]': 'AlertMe.com', 'name': 'shub/motion', 'id': '57394252-ade3-40a8-b988-b5a45c87af47', 'props[model]': 'PIR00140005', 'props[version]': '31005010', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'warmwhitelight': {'props[manufacturer]': 'Aurora', 'name': 'Shub wl', 'id': '177b9ab4-76c2-4d59-8d02-a04096a14cca', 'props[model]': 'FWBulb01', 'props[version]': '11250002', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'heating': {'props[manufacturer]': 'Computime', 'name': '', 'id': 'f875bb4a-6748-435b-b279-a4149a8d7f73', 'props[model]': 'SLR2', 'props[version]': '08054640', 'props[online]': 'PRESENT', 'parent': '24f0e38f-dae2-457f-a304-e4d34260f4a2'}, 'contactsensor1': {'props[manufacturer]': 'AlertMe.com', 'name': 'Win/Door Senso 2', 'id': 'e671e8eb-ba0d-46ff-bc14-4816ca909711', 'props[model]': 'WDS00140002', 'props[version]': '31005010', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'hotwater': {'props[manufacturer]': 'Computime', 'name': '', 'id': 'ef4187d7-9ec0-42f9-a941-97f594f1b28c', 'props[model]': 'SLR2', 'props[version]': '08054640', 'props[online]': 'PRESENT', 'parent': '24f0e38f-dae2-457f-a304-e4d34260f4a2'}, 'activeplug': {'props[manufacturer]': 'Computime', 'name': 'Plug', 'id': '49227d93-87a1-498a-bfba-ce5ed82d96ea', 'props[model]': 'SLP2', 'props[version]': '02155120', 'props[online]': 'PRESENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}, 'contactsensor2': {'props[manufacturer]': 'HiveHome.com', 'name': 'shub win/door', 'id': 'e61d60b4-f54b-4ab4-82b5-1d3505b36df3', 'props[model]': 'DWS003', 'props[version]': '01102603', 'props[online]': 'ABSENT', 'parent': '91a13336-34dc-4f7b-b921-6a467cfab01c'}}

    def validateGetContacts(self, oProd, context, strRequest):
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating GetContacts() response from Beekeeper')

        x = oProd.oAllContactsAPI
        y = oProd.oAllContactsBEE
        self.ValidateAndGetLog(oProd, strRequest, context, x, y)

    def validateGetHolidayMode(self, oProd, context, strRequest):
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating GetHolidayMode() response from Beekeeper')

        x = oProd.HolidayModeDictAPI
        y = oProd.HolidayModeDictBEE
        self.ValidateAndGetLog(oProd, strRequest, context, x, y)

    def ValidateAndGetLog(self, oProd, strRequest, context, x, y):

        EmptyList = set([])
        added, removed, modified, same = self.dict_compare(x, y)
        AddedList = added
        RemovedList = removed
        SameList = same

        print(added)
        if not added == EmptyList:
            print(list(AddedList))
            strDesc = 'Beekeeper Response is missing with these Attributes ' + str(list(AddedList))
            oProd.report_fail(strDesc, context)

        else:
            oProd.report_pass('Beekeeper Response has all Attributes which are returned in API Response', context)
        print('Added done ----------================---------------')

        print(removed)
        if not removed == EmptyList:
            print(list(RemovedList))
            strDesc = 'Beekeeper has these Attributes ' + str(list(RemovedList)) \
                      + ' which are not returned in API response'
            oProd.report_fail(strDesc, context)
        else:
            oProd.report_pass('No extra attributes noticed in Beekeeper apart from the ones returned by Honeycomb',
                              context)
        print('Removed done ----------================---------------')

        print(modified)
        if modified != {}:
            print('Now Validating the Modified product items')
            oModifiedDict = modified
            print(oModifiedDict)
            oModifiedAttributesDictKeysList = list(oModifiedDict.keys())
            print(oModifiedAttributesDictKeysList)
            strDesc = 'Beekeeper Response for ' + str(
                oModifiedAttributesDictKeysList) + ' do not match with API Response'
            oProd.report_fail(strDesc, context)

            for oEach in oModifiedAttributesDictKeysList:

                oAttributeDetailsTup = oModifiedDict[oEach]
                print(oAttributeDetailsTup)
                oAPIDict = oAttributeDetailsTup[0]
                oBEEDict = oAttributeDetailsTup[1]

                if type(oAPIDict) is dict and type(oBEEDict) is dict:
                    strDesc = 'Validating ' + strRequest + '() response for ' + str(oEach)
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize(strDesc)
                    added1, removed1, modified1, same1 = self.dict_compare(oAPIDict, oBEEDict)

                    oInsideAddedList = added1
                    if not oInsideAddedList == EmptyList:
                        print(list(oInsideAddedList))
                        for oEachAdded in list(oInsideAddedList):
                            strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                            strLog = strHeader + str(oEachAdded) + '$$' + '' + '$$' + str(oAPIDict[oEachAdded])
                            oProd.report_fail(strLog, context)

                    oInsideRemovedList = removed1
                    if not oInsideRemovedList == EmptyList:
                        print(list(oInsideRemovedList))
                        for oEachRemoved in list(oInsideRemovedList):
                            strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                            strLog = strHeader + str(oEachRemoved) + '$$' + str(oBEEDict[oEachRemoved]) + '$$' + ''
                            oProd.report_fail(strLog, context)

                    if modified1 != {}:
                        oInsideModifiedAttributesDict = modified1
                        print(oInsideModifiedAttributesDict)
                        oInsideModifiedAttributesDictKeysList = list(oInsideModifiedAttributesDict.keys())
                        print(oInsideModifiedAttributesDictKeysList)

                        for oEach1 in oInsideModifiedAttributesDictKeysList:
                            oInsideAttributesDetailsTuple = oInsideModifiedAttributesDict[oEach1]
                            print(oInsideAttributesDetailsTuple)

                            if oInsideAttributesDetailsTuple[0] != oInsideAttributesDetailsTuple[1]:
                                strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                                strLog = strHeader + str(oEach1) + '$$' + str(
                                    oInsideAttributesDetailsTuple[1]) + '$$' + str(oInsideAttributesDetailsTuple[0])
                                oProd.report_fail(strLog, context)

                    if not same1 == EmptyList:
                        print(list(same1))
                        oMatchingAttributes = list(same1)

                        '''
                        if strRequest.upper().find('CONTACTS') >= 0:
                            oProd.APIAllProductsDict = oProd.oAllContactsAPI
                            oProd.BEEAllProductsDict = oProd.oAllContactsBEE
                        '''

                        if strRequest.upper().find('DEVICES') >= 0 or strRequest.upper().find('PRODUCTS') >= 0:
                            for oEachAttribute in oMatchingAttributes:
                                if oProd.APIAllProductsDict[oEach][oEachAttribute] \
                                        != oProd.BEEAllProductsDict[oEach][oEachAttribute]:

                                    strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                                    strLog = strHeader + str(oEachAttribute) + '$$' + \
                                             oProd.BEEAllProductsDict[str(oEach)][
                                                 str(oEachAttribute)] + '$$' + \
                                             oProd.APIAllProductsDict[str(oEach)][str(oEachAttribute)]
                                    oProd.report_fail(strLog, context)

                                else:
                                    strHeader = "Attribute Validated$$" + "Value returned from Beekeeper and API response" + "@@@"
                                    strLog = strHeader + str(oEachAttribute) \
                                             + '$$' + str(oProd.APIAllProductsDict[str(oEach)][str(oEachAttribute)])
                                    oProd.report_pass(strLog, context)

                        elif strRequest.upper().find('CONTACTS') >= 0:
                            for oEachAttribute in oMatchingAttributes:
                                if oProd.oAllContactsAPI[oEach][oEachAttribute] \
                                        != oProd.oAllContactsBEE[oEach][oEachAttribute]:

                                    strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                                    strLog = strHeader + str(oEachAttribute) + '$$' + \
                                             oProd.oAllContactsBEE[str(oEach)][
                                                 str(oEachAttribute)] + '$$' + \
                                             oProd.oAllContactsAPI[str(oEach)][str(oEachAttribute)]
                                    oProd.report_fail(strLog, context)

                                else:
                                    strHeader = "Attribute Validated$$" + "Value returned from Beekeeper and API response" + "@@@"
                                    strLog = strHeader + str(oEachAttribute) \
                                             + '$$' + str(oProd.oAllContactsBEE[str(oEach)][str(oEachAttribute)])
                                    oProd.report_pass(strLog, context)

                    else:
                        oProd.report_fail(
                            'Beekeeper response does not match with that of API for any of the attributes for this product',
                            context)

                else:  # if a string
                    if oAPIDict == oBEEDict:
                        strHeader = "Attribute Validated$$" + "Value returned from Beekeeper and API response" + "@@@"
                        strLog = strHeader + str(oEach) \
                                 + '$$' + str(oBEEDict)

                        oProd.report_pass(strLog, context)
                    else:
                        strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                        strLog = strHeader + str(oEach) + '$$' + \
                                 str(oBEEDict) + '$$' + str(oAPIDict)
                        oProd.report_fail(strLog, context)

        print('Modified done ----------================---------------')

        if not same == EmptyList:
            print(list(SameList))
            self.oSameProductAttributesComparison(oProd, SameList, context, strRequest)

        elif added == EmptyList and removed == EmptyList and modified == {} and same == EmptyList:
            oProd.report_done('There are no values from both beekeeper and API to compare', context)


        elif same == EmptyList:
            oProd.report_fail('Beekeeper response does not match with that of API for any of the products', context)
        print(same)

        # strDesc = 'Beekeeper response matches with that of API for these products - ' + str(list(SameList))
        # oProd.report_pass(strDesc, context)

    def oSameProductAttributesComparison(self, oProd, SameList, context, strRequest):

        if strRequest.upper().find('CONTACTS') >= 0:
            oProd.APIAllProductsDict = oProd.oAllContactsAPI
            oProd.BEEAllProductsDict = oProd.oAllContactsBEE

        elif strRequest.upper().find('HOLIDAY') >= 0:
            oProd.APIAllProductsDict = oProd.HolidayModeDictAPI
            oProd.BEEAllProductsDict = oProd.HolidayModeDictBEE

        oMatchedProducts = list(SameList)
        for oEachProd in oMatchedProducts:

            if oEachProd in oProd.APIAllProductsDict and oEachProd in oProd.BEEAllProductsDict:
                if type(oEachProd) is dict:
                    strDesp = 'Validating ' + strRequest + '() response for ' + str(oEachProd)
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize(strDesp)
                    added1, removed1, modified1, same10 = self.dict_compare \
                        (oProd.APIAllProductsDict[oEachProd], oProd.BEEAllProductsDict[oEachProd])
                    print(same10)
                    oMatchedProductsAttributes = list(same10)
                    for oEachAttribute in oMatchedProductsAttributes:
                        if oProd.APIAllProductsDict[oEachProd][oEachAttribute] \
                                != oProd.BEEAllProductsDict[oEachProd][oEachAttribute]:

                            strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                            strLog = strHeader + str(oEachAttribute) + '$$' + str(oProd.BEEAllProductsDict[oEachProd][
                                                                                      oEachAttribute]) + '$$' + \
                                     str(oProd.APIAllProductsDict[oEachProd][oEachAttribute])
                            oProd.report_fail(strLog, context)

                        else:
                            strHeader = "Attribute Validated$$" + "Value returned from Beekeeper and API response" + "@@@"
                            strLog = strHeader + str(oEachAttribute) \
                                     + '$$' + str(oProd.APIAllProductsDict[oEachProd][oEachAttribute])
                            oProd.report_pass(strLog, context)
                else:
                    if oProd.APIAllProductsDict[oEachProd] == oProd.BEEAllProductsDict[oEachProd]:
                        strHeader = "Attribute Validated$$" + "Value returned from Beekeeper and API response" + "@@@"
                        strLog = strHeader + str(oEachProd) \
                                 + '$$' + str(oProd.BEEAllProductsDict[oEachProd])
                        oProd.report_pass(strLog, context)
                    else:
                        strHeader = "Attributes validated$$" + "Beekeeper Value$$" + "API Value" + "@@@"
                        strLog = strHeader + str(oEachProd) + '$$' + str(oProd.BEEAllProductsDict[oEachProd]) + '$$' + \
                                 str(oProd.APIAllProductsDict[oEachProd])
                        oProd.report_fail(strLog, context)

        print('Same done ----------================---------------')

        print('Comparision all done')
        print('Comparision all done')
        print('Comparision all done')
        print('Comparision all done')
        print('Comparision all done')
        print('Comparision all done')

    def dict_compare(self, d1, d2):

        d1_keys = set(list(d1.keys()))
        d2_keys = set(list(d2.keys()))
        intersect_keys = d1_keys.intersection(d2_keys)
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys
        modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        return added, removed, modified, same

    def validateGetProducts1(self, oProd, context):

        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating GetProducts() response from Beekeeper')
        self.BEEProductDict = {"id": oProd.BeeProductID,
                               "type": oProd.BeeProductType,
                               "parent": oProd.BeeParentNodeID,
                               # Props
                               "online": oProd.BeeDeviceStatus,
                               "model": oProd.BeeDeviceModel,
                               "version": oProd.BeeDeviceVersion,
                               # Need to check for capabilities
                               # Holiday mode
                               "enabled": oProd.BeeHolidayEnabled,
                               "start": oProd.BEEHolidayStart,
                               "end": oProd.BeeHolidayEnd,
                               "temperature(holiday)": oProd.BeeHolidayTemp,
                               "maxEvents": oProd.BeeMaxEvents,
                               "pmz": oProd.BeePMZ,
                               # previous
                               "mode(previous)": oProd.BeePreviousMode,
                               "scheduleOverride": oProd.BeeScheduleOverride,
                               "temperature": oProd.BeeInsidetemperature,
                               "zone": oProd.BeeZoneid,
                               # state
                               "name": oProd.BeeZoneName,
                               "boost": oProd.BeeBoost,
                               "frostProtection": oProd.BeeFrostProtection,
                               "mode": oProd.BeeDeviceMode,
                               # Schedule to be done here
                               "target": oProd.BeeTargTemp

                               }

        self.APIProductDict = {"id": oProd.APIProductID,
                               "type": oProd.APIProductType,
                               "parent": oProd.APIParentNodeID,
                               # Props
                               "online": oProd.APIDeviceStatus,
                               "model": oProd.APIDeviceModel,
                               "version": oProd.APIDeviceVersion,
                               # Need to check for capabilities
                               # Holiday mode
                               "enabled": oProd.APIHolidayEnabled,
                               "start": oProd.APIHolidayStart,
                               "end": oProd.APIHolidayEnd,
                               "temperature(holiday)": oProd.APIHolidayTemp,
                               "maxEvents": oProd.APIMaxEvents,
                               "pmz": oProd.APIPMZ,
                               # previous
                               "mode(previous)": oProd.APIPreviousMode,
                               "scheduleOverride": oProd.APIScheduleOverride,
                               "temperature": oProd.APIInsidetemperature,
                               "zone": oProd.APIZoneid,
                               # state
                               "name": oProd.APIZoneName,
                               "boost": oProd.APIBoost,
                               "frostProtection": oProd.APIFrostProtection,
                               "mode": oProd.APIDeviceMode,
                               # Schedule to be done here
                               "target": oProd.APITargTemp
                               }

        self.genericFunc(context, self.BEEProductDict, self.APIProductDict)

        if oProd.BeeHeatingID == oProd.APIHeatingID:
            # a = ("Report Pass wtih heating id %s" % oself.BeeHeatingID)
            # self.report_pass(a, context)
            print("Heating ID matching")
            print('Heating id is %s' % oProd.BeeHeatingID)
        else:
            print('Heating ID mismatch')
            # print ('API Heat id = %s' % oself.APIHeatingID)
            # print('Bee Heat id = %s' % oself.BeeHeatingID)
        if oProd.BeeParentNodeID == oProd.APIParentNodeID:
            print("Parent ID matching")
            # print('Parent id = %s' % oself.BeeHeatingID)
            print(oProd.BeeParentNodeID)
        else:
            print('Parent ID mismatch')
        if oProd.BeeDeviceStatus == oProd.APIDeviceStatus:
            print("Device Presence State matching")

            print(oProd.BeeDeviceStatus)
            # print('Device Presence = %s' % oself.BeeHeatingID)
        else:
            print('Device Presence mismatch')
        if oProd.BeeDeviceModel == oProd.APIDeviceModel:
            print("Device Model matching")
            # print('Device Model = %s' % oself.BeeHeatingID)
            print(oProd.BeeDeviceModel)
        else:
            print('Device Model mismatch')
        if oProd.BeeDeviceMode == oProd.APIDeviceMode:
            print("Heat Mode matching")

            print(oProd.BeeDeviceMode)

        else:
            print('Heat mode mismatch')
        if oProd.BeeTargTemp == oProd.APITargTemp:
            print("Target Temperature matching")
            print(oProd.BeeTargTemp)
        else:
            print('Target Temperature mismatch')

    # Holiday Mode
    def getHolidayModeBEE(self, oProduct, session, context, strRequest, strContact):
        resp = ALBKP.getHolidayModeBEE(session)
        oNode = resp
        oHolidayKeysList = list(oNode.keys())
        oHolidayModeDict = dict([(key, {}) for key in oHolidayKeysList])

        oCount = 0
        while oCount < len(sorted(oHolidayKeysList)):
            oKey = oHolidayKeysList[oCount]
            oHolidayModeDict[oKey] = oNode[oKey]
            if oKey == 'start' or oKey == 'end':
                oHolidayModeDict[oKey] = self.convertEpochToHumanTimeStamp(oNode[oKey] / 1000.0)
            oCount = oCount + 1
        print(oHolidayModeDict)
        oProduct.HolidayModeDictBEE = oHolidayModeDict

        return oProduct.HolidayModeDictBEE

    def getHolidayModeAPI(self, oProduct, session, context, strRequest):
        resp = ALAPI.getNodesV6(session)

        for oNode in resp['nodes']:
            if 'nodeType' in oNode:
                if 'http://alertme.com/schema/json/node.class.thermostat.json#' in oNode['nodeType'] and \
                        not 'supportsHotWater' in oNode['attributes']:
                    oAttributeList = oNode['attributes']
                    oJson = oAttributeList['holidayMode']['reportedValue']
                    if isinstance(oJson, str): oJson = json.loads(oJson)
                    oHolidayKeysList = list(oJson.keys())
                    oHolidayModeDictAPI = {'enabled': oJson['enabled']}
                    time.sleep(3)
                    oHolidayModeDictAPI['start'] = self.convertEpochToHumanTimeStamp(
                        self.convertIntoEpoch(oJson['startDateTime']))
                    oHolidayModeDictAPI['end'] = self.convertEpochToHumanTimeStamp(
                        self.convertIntoEpoch(oJson['endDateTime']))
                    oHolidayModeDictAPI['temperature'] = oJson['targetHeatTemperature']
                    oHolidayModeDictAPI['status'] = 'TBC with Peter'

        print(oHolidayModeDictAPI)
        oProduct.HolidayModeDictAPI = oHolidayModeDictAPI

    def convertIntoEpoch(self, oTime):
        dt = datetime.datetime.strptime(oTime[:-7], '%Y-%m-%dT%H:%M:%S.%f') + \
             datetime.timedelta(hours=int(oTime[-5:-3]),
                                minutes=int(oTime[-2:])) * int(oTime[-6:-5] + '1')
        seconds = time.mktime(dt.timetuple()) + dt.microsecond / 1000000.0
        return seconds

    def convertEpochToHumanTimeStamp(self, oTime):
        oTimeStamp = datetime.datetime.fromtimestamp(oTime).strftime("%Y-%m-%d %H:%M:%S.%f"[:-3])
        return oTimeStamp

    def endHolidayModeBEE(self, oProduct, session, context, strRequest, strContact):

        self.getHolidayModeBEE(oProduct, session, context, strRequest, strContact)
        if oProduct.HolidayModeDictBEE['enabled'] != 'false':
            oProduct.report_done("Holiday Mode not set already for user, so setting one before delete request", context)
            self.startHolidayMode(oProduct, session, context, strRequest, strContact)
        else:
            oProduct.report_done("Already Holiday Mode set for user, so deleting it for test", context)
        resp = ALBKP.endHolidayModeBEE(session)
        if resp['set']:
            self.getHolidayModeBEE(oProduct, session, context, strRequest, strContact)
            if not oProduct.HolidayModeDictBEE['enabled']:
                oProduct.report_done("Holiday Mode successfully deleted via Beekeeper", context)
            else:
                oProduct.report_fail("Delete Holiday Mode request not successful", context)
        else:
            oProduct.report_fail("Delete Holiday Mode request not successful", context)

    def startHolidayModeBEE(self, oProduct, session, context, strRequest, strContact):

        self.getHolidayModeBEE(oProduct, session, context, strRequest, strContact)
        if oProduct.HolidayModeDictBEE['enabled'] != 'false':
            oProduct.report_done("Holiday Mode not set already for user, so sending holiday mode request", context)
            self.startHolidayMode(oProduct, session, context, strRequest, strContact)
        else:
            oProduct.report_done("Holiday Mode already set for user, so deleting existing one before the test", context)
            self.endHolidayModeBEE(oProduct, session, context, strRequest, strContact)
            oProduct.report_done("Sending Holiday Mode request via beekeeper", context)
            self.startHolidayMode(oProduct, session, context, strRequest, strContact)

    def startHolidayMode(self, oProduct, session, context, strRequest, strContact):

        oUpdateReqDict = {"start": (int(time.time()) + (5 * 60)) * 1000,
                          "end": (int(time.time()) + (10 * 60)) * 1000}
        oTempList = [5.5, 7, 12.5, 20, 27.5, 32]
        oUpdateReqDict["temperature"] = random.choice(oTempList)
        print(oUpdateReqDict)

        try:
            ALBKP.startHolidayModeBEE(session, oUpdateReqDict)
            oProduct.report_done("Start Holiday Mode Request to Beekeeper is successful", context)

        except:
            print('Exception in startHolidayModeBEE')

    # Contacts
    def getContactsBEE(self, oProduct, session, context, strRequest, strContact):

        resp = ALBKP.getContactsBEE(session)
        # oAllContactsBEE = {}
        self.createContactsDict(oProduct, resp)
        oProduct.oAllContactsBEE = oProduct.oAllContactsDict
        print(oProduct.oAllContactsBEE)

    def getContactsAPI(self, oProduct, session, context, strRequest):

        resp = ALAPI.getContactsV6(session)
        resp = resp['contacts']
        # oAllContactsAPI = {}
        self.createContactsDict(oProduct, resp)
        oProduct.oAllContactsAPI = oProduct.oAllContactsDict
        print(oProduct.oAllContactsAPI)

    def updateContactsBEE(self, oProduct, session, context, strRequest, strContact):

        # try:
        oWholeUpdateReqList = []
        self.getContactsBEE(oProduct, session, context, strRequest, strContact)
        oNameList = list(oProduct.oAllContactsBEE.keys())
        for oEachName in oNameList:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize(
                "Contact Details for " + str(oEachName) + " before updating")
            oAttributeKeys = list(oProduct.oAllContactsBEE[oEachName].keys())
            for oKey in oAttributeKeys:
                strHeader = "Attribute" + '$$' + "Existing value before updating any detail" + "@@@"
                strLog = strHeader + str(oKey) + '$$' + str(oProduct.oAllContactsBEE[oEachName][oKey])
                oProduct.report_done(strLog, context)

        oNameList = sorted(oNameList)
        oNameCounter = 10
        oCount = 0
        oListLen = len(oNameList)
        if strContact:
            oListLen = 1
        elif not strContact:
            oListLen = 2
        elif strContact is None:
            oListLen = oListLen
        while oCount < oListLen:
            oUpdateReqDict = {}
            oName = oNameList[oCount]
            oUpdateReqDict["id"] = oProduct.oAllContactsBEE[oName]["id"]
            oUpdateReqDict["name"] = oProduct.oAllContactsBEE[oName]["name"] + str(oNameCounter)
            oRandom = self.randomNumberGeneration(8)
            oUpdateReqDict["mobile"] = '+4474' + str(oRandom)
            oWholeUpdateReqList.append(oUpdateReqDict)
            oCount = oCount + 1

        ALBKP.updateContactsBEE(session, oWholeUpdateReqList)
        oProduct.report_done("Update Request to Beekeeper is successful", context)

        # except:
        #    oProduct.report_fail("Exception thrown in updateContactsBEE() function", context)

    def addContactsBEE(self, oProduct, session, context, strRequest, strContact):
        oWholeUpdateReqList = []
        self.getContactsBEE(oProduct, session, context, strRequest, strContact)
        oNameList = list(oProduct.oAllContactsBEE.keys())
        oListLen = len(oNameList)
        if oListLen != 0:
            self.deleteContactsBEE(oProduct, session, context, strRequest, strContact)
            oProduct.report_done("Existing contacts deleted", context)
        if strContact:
            oListLen = 0
        elif not strContact:
            oListLen = 1
        elif strContact is None:
            oListLen = 4
        oCount = 0
        while oCount <= oListLen:
            print('into While')
            oUpdateReqDict = {"name": 'NewContact' + str(oCount + 1)}
            # oName = oNameList[oCount]
            # oUpdateReqDict["id"] = oProduct.oAllContactsBEE[oName]["id"]
            oRandom = self.randomNumberGeneration(8)
            oUpdateReqDict["mobile"] = '+4474' + str(oRandom)
            oWholeUpdateReqList.append(oUpdateReqDict)
            oCount = oCount + 1

        ALBKP.addContactsBEE(session, oWholeUpdateReqList)
        oProduct.report_done("AddContacts Request to Beekeeper is successful", context)
        strLog = ('Number of Contacts added is %d' % oCount)
        oProduct.report_done(strLog, context)

    def deleteContactsBEE(self, oProduct, session, context, strRequest, strContact):
        oWholeUpdateReqList = []
        self.getContactsBEE(oProduct, session, context, strRequest, strContact)
        oNameList = sorted(list(oProduct.oAllContactsBEE.keys()))
        oListLen = len(oNameList)
        oDelCount = 1
        while oDelCount <= oListLen:
            oName = oNameList[oDelCount - 1]
            oID = oProduct.oAllContactsBEE[oName]['id']
            oWholeUpdateReqList.append(oID)
            oDelCount = oDelCount + 1

        ALBKP.deleteContactsBEE(session, oWholeUpdateReqList)
        oProduct.report_done("Delete Contacts Request to Beekeeper is successful", context)

    def randomNumberGeneration(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    def createContactsDict(self, oProduct, resp):

        oNameList = []
        oUniqueNameCountDict = {}
        for oNode in resp:
            if 'name' in oNode:
                oNameList.append(oNode['name'])

        print(oNameList)
        oNameList = sorted(oNameList)
        oNameListClone = sorted(set(oNameList))
        oListLen = len(oNameList)
        self.getCountForEachElement(oProduct, oNameList, oUniqueNameCountDict)
        oProduct.oAllContactsDict = dict([(key, {}) for key in oProduct.oSetList])
        print(oProduct.oAllContactsDict)
        # Writing in Contacts Dict
        oNameCount = 0
        while oNameCount < len(oNameListClone):
            oContactIDList = []
            oName = oNameListClone[oNameCount]

            if oUniqueNameCountDict[oName] != 1:
                for oNode in resp:
                    if oName == oNode['name']:
                        oContactID = oNode['id']
                        oContactIDList.append(oContactID)

                print(oContactIDList)
                oSortedContactIDList = sorted(oContactIDList)
                oContactCount = 0
                while oContactCount < len(oSortedContactIDList):
                    # for oID in oContactIDList:
                    oID = oSortedContactIDList[oContactCount]
                    oNameFlag = oName + str(oContactCount + 1)
                    oProduct.oAllContactsDict[oNameFlag]['id'] = oID
                    oProduct.oAllContactsDict[oNameFlag]['name'] = oName
                    for oNode in resp:
                        if oID == oNode['id']:
                            if 'mobile' in oNode: oProduct.oAllContactsDict[oNameFlag]['mobile'] = oNode['mobile']
                    oContactCount = oContactCount + 1

            else:
                for oNode in resp:
                    if oName == oNode['name']:
                        if 'id' in oNode: oProduct.oAllContactsDict[oName]['id'] = oNode['id']
                        if 'mobile' in oNode: oProduct.oAllContactsDict[oName]['mobile'] = oNode['mobile']
                        oProduct.oAllContactsDict[oName]['name'] = oNode['name']

            oNameCount = oNameCount + 1

        return oProduct

    # Update Node - For Validation, getProductsBEE() needs to be completed - now it works only for get Devices.
    def updateNodeBEE(self, oProduct, session, context, strRequest, oUpdateDetails):

        oTargetDetailsList = oUpdateDetails

        print(oTargetDetailsList)
        oAttribute = oTargetDetailsList[0]
        oTargetValue = oTargetDetailsList[1]
        oType = oTargetDetailsList[2]

        ALBKP.getProductsBEE(session)
        # if oType in oProduct.oAllProdDictBEE:
        if oType == 'heating':
            # oID = oProduct.oAllProdDictBEE['']['id']
            oID = '34841749-cddb-44b3-af00-8e9b5c4ea523'
            oWholeUpdateReqBody = {}
            oWholeUpdateReqBody = {'mode': 'BOOST', oAttribute: oTargetValue}
            oUpdateNodeURL = '/nodes/' + oType + '/' + oID

            print(oWholeUpdateReqBody, oUpdateNodeURL)

            ALBKP.updateNodeBEE(session, oWholeUpdateReqBody, oUpdateNodeURL)
            print('Update Node for Boost changes successful')

        else:
            print('Type not found in the dict')
            # Beekeeper Functions


class leakSensorEndPoint(object):
    def __init__(self, platAPI, strServerName):
        # Parent Tstat
        self.parentAPI = platAPI
        self.type = None
        self.serverName = strServerName
        self.client = None
        self.mode = None
        self.AndroidDriver = platAPI.AndroidDriver
        self.WebDriver = platAPI.WebDriver
        self.iOSDriver = platAPI.iOSDriver
        self.reporter = platAPI.reporter
        self.platformVersion = None
        self.leakSensorName = ''
        self.leakStatus = ''
        self.blnCalibrationAt = ''
        self.minLeakDuration = ''
        self.batteryState = ''
        self.presence = ''
        self.nativeIdentifier = ''
        self.clientLeakStatus = ''
        self.blnClientCalibrationAt = False
        self.calibratedAt = ''
        self.notificationText = ''
        self.notificationContent = ''
        self.leakRules = []
        self.oClientAlertDict = {}
        self.oClientminLeak = ''
        self.bannerText = ''
        self.questions = None

    # For updating leak node
    def getLeakSensorNode(self):
        try:
            self.AndroidDriver = self.parentAPI.AndroidDriver
            self.WebDriver = self.parentAPI.WebDriver
            self.iOSDriver = self.parentAPI.iOSDriver
            self.reporter = self.parentAPI.reporter

            ALAPI.createCredentials(self.serverName, self.client)
            session = ALAPI.sessionObjectV6dot5()
            self.platformVersion = 'V6.5'
            resp = ALAPI.getNodesV6(session)

            for oNode in resp['nodes']:
                if 'water.leak.detector.json' in oNode['nodeType']:
                    self.leakSensorName = oNode['name']
                    self.leakStatus = oNode['features']['liquid_leak_detector_v1']['isLeaking']['reportedValue']
                    oCalibratedNode = oNode['features']['liquid_leak_detector_v1']['calibratedAt']
                    if 'reportedValue' in oCalibratedNode:
                        self.calibratedAt = oCalibratedNode['reportedValue']
                        self.blnCalibrationAt = True
                    else:
                        self.blnCalibrationAt = False
                    self.minLeakDuration = \
                        str(int(oNode['features']['liquid_leak_detector_configuration_v1']['minimumLeakDuration'][
                                    'reportedValue'] / 60))
                    self.batteryState = oNode['features']['battery_device_v1']['batteryState']['reportedValue']
                    self.presence = oNode['features']['physical_device_v1']['presence']['reportedValue']
                    self.nativeIdentifier = oNode['features']['physical_device_v1']['nativeIdentifier']['reportedValue']

        except:
            print('Platform API : NoSuchAttributeException: in getLeakSensorNode Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # for getting leak alert rules
    def getLeakRules(self) -> object:
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObjectV6dot5()
        self.platformVersion = 'V6.5'
        resp = ALAPI.getRulesV6(session)
        dictoRule = {}
        lstRule = []
        for oRule in resp['rules']:
            dictoRules = {}
            lstoRuleAction = []
            dictoRuleActions = {}
            oRuleName = oRule['name']
            oRuleActions = oRule['actions']
            for oRuleAction in oRuleActions:
                oRuleActionType = oRuleAction['type']
                if oRuleActionType == 'SendSMS':
                    oRuleActionType = 'PushNotification'
                oRuleActionStatus = oRuleAction['status']
                lstoRuleAction = {oRuleActionType: oRuleActionStatus}
                dictoRuleActions.update(lstoRuleAction)
            oRuleNameDict = {oRuleName: dictoRuleActions}
            dictoRule.update(oRuleNameDict)

        self.leakRules = dictoRule

    # for setting rules
    def setRules(self, dictPayload):
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObjectV6dot5()
        self.platformVersion = 'V6.5'
        blnSuccess = ALAPI.putAlertSettings(session, dictPayload)

        return blnSuccess

    # for getting events
    def getEvents(self):
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObjectV6dot5()
        self.platformVersion = 'V6.5'
        resp = ALAPI.getEvents(session)
        print(resp)
        self.events = resp

    # For getting rules set for a notification type
    def getRuleDict(self, strRuleType, strNotificationType):
        strStatus = 'INACTIVE'
        if strRuleType in self.leakRules.keys():
            if strNotificationType in self.leakRules[strRuleType].keys():
                strStatus = self.leakRules[strRuleType][strNotificationType]
        if strStatus == 'ACTIVE':
            return True
        else:
            return False

    # For generating notification
    def trigger_notification(self, notificationType):
        notificationTypeDict = {'SMALL LEAK': "LEAK_DETECTED", 'LARGE FLOW': 'FLOW_DETECTED', 'FLOW NONE': 'FLOW_NONE',
                                'PRESS BUTTON': 'BUTTON_PRESSED', 'LOW BATTERY': 'NODE_LOW_BATTERY',
                                'OFFLINE': 'ABSENT',
                                'HIGH WATER USAGE': 'FLOW_DETECTED', 'LOW WATER FLOW': 'LEAK_DETECTED'}
        notificationLPDict = {"LEAK_DETECTED": "LowLeak", 'FLOW_DETECTED': "HighLeak", 'FLOW_NONE': "NoLeak"}
        strNotification = notificationTypeDict[notificationType]
        triggerTime = datetime.utcnow() - timedelta(seconds=5)

        if strNotification in notificationLPDict.keys():
            strNotification = notificationLPDict[strNotification]
            triggerTime = ALAPI.updateLeakStatusFromLP(self.nativeIdentifier, strNotification)
        else:
            ALAPI.updateLeakStatus(self.nativeIdentifier, strNotification)

        unixtriggerTime = int(time.mktime(triggerTime.timetuple()) * 1000)
        time.sleep(20)
        self.getLeakSensorNode()
        return unixtriggerTime

    # For clearing generic notifications if any
    def clear_notification(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.clear_notification()

    # For leak control screen navigation
    def leak_control_navigation(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.leak_control_navigation()
        if 'IOS' in self.client.upper():
            iOSLeak = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            strDeviceName = self.leakSensorName
            iOSLeak.navigate_to_device_updated(strDeviceName)

    # for fetching leak status at client
    def fetch_leak_status(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            self.clientLeakStatus, self.blnClientCalibrationAt = objHLS.get_leak_status()
        if 'IOS' in self.client.upper():
            iOSLeak = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            self.clientLeakStatus, self.blnClientCalibrationAt = iOSLeak.getLeakStatus()

    # for validating leak notifications at client
    def validate_notification(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            self.notificationText, self.notificationContent = objHLS.validate_notification()

    # for validating leak notifications at client
    def swipeLeak(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.swipeLeak()

    # for fetching alert settings displayed at client
    def fetch_alertSettings(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            self.oClientAlertDict = objHLS.fetchCurrentAlertSettings()
        if 'IOS' in self.client.upper():
            iOSLeak = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            self.oClientAlertDict = iOSLeak.fetchCurrentAlertSettings()

    # for updating alert settings at client
    def set_alertSettings(self, oTargetDict):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.setAlertSettings(oTargetDict)
        if 'IOS' in self.client.upper():
            iOSLeak = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            iOSLeak.setAlertSettings(oTargetDict)

    # for fetching min leak settings at client
    def min_leakduration(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            self.oClientminLeak = objHLS.fetchMinLeakDuration()
        if 'IOS' in self.client.upper():
            iOSLeak = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            self.oClientminLeak = iOSLeak.fetchMinLeakDuration()

    # for updating min leak settings at client
    def set_leakduration(self, strTarget):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            self.oClientminLeak = objHLS.setMniLeakDuration(strTarget)
        if 'IOS' in self.client.upper():
            iOSLeak = iOSPage.LeakSensor(self.iOSDriver, self.reporter)
            if self.minLeakDuration != strTarget:
                self.oClientminLeak = iOSLeak.setMinLeakDuration(strTarget)

    def fix_leak(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.startCalibration()

    def fetch_Banner(self, alert):
        if 'ANDROID' in self.client.upper():
            self.leak_control_navigation()
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            self.bannerText = objHLS.bannerText(alert)

    def load_troubleshootingScreen(self, status):
        if 'ANDROID' in self.client.upper():
            self.leak_control_navigation()
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.load_troubleshootingScreen(status)

    def intendedUsage(self):
        if 'ANDROID' in self.client.upper():
            self.leak_control_navigation()
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.intendedUsage()

    def remindLater(self):
        if 'ANDROID' in self.client.upper():
            self.leak_control_navigation()
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.remindLater()

    def navigateToFroDashboard(self):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.honeycomb_verify()
            self.leak_control_navigation()

    def bannerDisappear(self, alert):
        if 'ANDROID' in self.client.upper():
            objHLS = androidPage.LeakSensor(self.AndroidDriver, self.reporter)
            objHLS.bannerDisappear(alert)

    def troubleshootingNavigation(self, navigationList, expectedQuestions):
        if 'ANDROID' in self.client.upper():
            objDYT = androidPage.DYNAMIC_TROUBLESHOOTING(self.AndroidDriver, self.reporter)
            self.questions = objDYT.navigate_questions(navigationList, expectedQuestions)
            return self.questions

    def plumberScreen(self):
        if 'ANDROID' in self.client.upper():
            objDYT = androidPage.DYNAMIC_TROUBLESHOOTING(self.AndroidDriver, self.reporter)
            objDYT.call_plumber()

    def close_troubleshooting(self):
        if 'ANDROID' in self.client.upper():
            objDYT = androidPage.DYNAMIC_TROUBLESHOOTING(self.AndroidDriver, self.reporter)
            objDYT.close_troubleshooting()


class sensorEndPoint(object):
    def __init__(self, platAPI, strServerName, epType):
        self.parentAPI = platAPI
        self.type = epType
        self.serverName = strServerName
        self.client = None
        self.platformVersion = None
        # self._weeklySchedule = {}
        self.eventLogs = None
        self.eventLogsFromApp = None
        self.AndroidDriver = platAPI.AndroidDriver
        self.WebDriver = platAPI.WebDriver
        self.iOSDriver = platAPI.iOSDriver
        self.reporter = platAPI.reporter
        # self.mode = None
        self.deviceName = None
        # self.lightBrightness = 0
        self.CurrentDeviceStateFromApp = ''
        self.CurrentDeviceStateFromHoneyComb = None
        self.BusiestPeriod = None
        self.NoOfTimesSensorTriggeredToday = 0
        self.LastDetected = None

        # self.floatColourTemperature = None
        # self.alexaResponse = ''

    # def update_attributes_from_client(self):
    #    self.CurrentDeviceStateFromApp = self.getAttributesFromClient()
    #   return self.CurrentDeviceStateFromApp

    def update(self):
        self.AndroidDriver = self.parentAPI.AndroidDriver
        self.WebDriver = self.parentAPI.WebDriver
        self.iOSDriver = self.parentAPI.iOSDriver
        self.reporter = self.parentAPI.reporter

        # if self.platformVersion == 'V6':
        self._updateV6()

    def _updateV6(self, nodeID=None):

        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        self.platformVersion = 'V6'

        if self.type == 'MOTIONSENSOR':
            self.deviceType = 'MOT003'
            # self.deviceType = 'PIR00140005_1'
        elif self.type == 'CONTACTSENSOR':
            self.deviceType = 'DWS003'

        self.currentDeviceNodeId = pUtils.getDeviceNodeID(self.deviceType)
        self.deviceName = pUtils.getDeviceName(self.deviceType)

        self.CurrentDeviceStateFromHoneyComb = pUtils.getMSAttributes(self.currentDeviceNodeId)
        # self.eventLogs = pUtils.getMotionSensorEventLogs(self.currentDeviceNodeId)
        return True

    def navigateToSensorScreen(self, strSensorType):

        self.client = 'WEB'
        if 'ANDROID' in self.client.upper():
            print('Navigate to sensor screen from Android UI')
        elif 'IOS' in self.client.upper():
            print('Navigate to sensor screen from IOS UI')
        elif 'WEB' in self.client.upper():
            if 'MOTION' in strSensorType.upper():
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_motion_sensor_product_page()
                # To be done for contact sensor as well here

    def getAttributesFromClient(self):
        self.client = 'WEB'
        if 'ANDROID' in self.client.upper():
            print('Get Client attributes from Android UI')
        elif 'IOS' in self.client.upper():
            print('Get Client attributes from IOS UI')
        elif 'WEB' in self.client.upper():
            if self.type == 'MOTIONSENSOR':
                oMotionSensorPage = webPage.motionSensorPage(self.WebDriver, self.reporter)
                self.CurrentDeviceStateFromApp, self.BusiestPeriod, self.LastDetected, self.NoOfTimesSensorTriggeredToday, \
                self.eventLogsFromApp = oMotionSensorPage.get_motion_sensor_attributes()
            if self.type == 'CONTACTSENSOR':
                print('Same as above')
                # Need to be done for contact sensor
                # return self.CurrentDeviceStateFromApp, self.eventLogs

    def getSchedule(self):
        return self._eventLogs

    def validateSensorState(self, strSensorType):
        self.client = 'WEB'
        if 'ANDROID' in self.client.upper():
            print("To be done")
        elif 'IOS' in self.client.upper():
            print("To be done")
        elif 'WEB' in self.client.upper():
            self.getAttributesFromClient()


class lightEndPoint(object):
    def __init__(self, platAPI, strServerName, epType):
        self.parentAPI = platAPI
        self.type = epType
        self.serverName = strServerName
        self.client = None
        self.platformVersion = None
        self._weeklySchedule = {}
        self.AndroidDriver = platAPI.AndroidDriver
        self.WebDriver = platAPI.WebDriver
        self.iOSDriver = platAPI.iOSDriver
        self.reporter = platAPI.reporter
        self.mode = None
        self.deviceName = None
        self.lightBrightness = 0
        self.CurrentDeviceState = None
        self.floatColourTemperature = None
        self.alexaResponse = ''
        self.currentDeviceNodeId = None

    def update_attributes_from_client(self):
        self.mode, self.CurrentDeviceState, self.warmWhiteLightBrightness = self.getAttributesFromClient()
        return self.mode, self.CurrentDeviceState, self.warmWhiteLightBrightness

    def update(self):
        self.AndroidDriver = self.parentAPI.AndroidDriver
        self.WebDriver = self.parentAPI.WebDriver
        self.iOSDriver = self.parentAPI.iOSDriver
        self.reporter = self.parentAPI.reporter

        # if self.platformVersion == 'V6':
        self._updateV6()

    def _updateV6(self, nodeID=None):

        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObject()
        self.platformVersion = 'V6'
        '''
        if session.latestSupportedApiVersion != '6':
            self.platformVersion = 'V5'
            print("V5")
            return False
        else:
            self.platformVersion = 'V6'

        '''

        if self.type == 'WARMWHITELIGHT':
            self.deviceType = 'FWBulb01'
        elif self.type == 'TUNEABLELIGHT':
            self.deviceType = 'TWBulb01'
        else:
            self.deviceType = 'RGBBulb01'

        self.currentDeviceNodeId = pUtils.getOnlineDeviceNodeID(self.deviceType)
        self.deviceName = pUtils.getDeviceName(self.deviceType)
        self.mode, self.CurrentDeviceState, self.lightBrightness, self.floatColourTemperature = pUtils.getLightAttributes(
            self.currentDeviceNodeId)

        self._weeklySchedule = pUtils.getDeviceScheduleInStandardFormat(self.deviceType)
        # print(self._weeklySchedule)
        return True

    def setDeviceName(self, myDeviceName, newDeviceName):
        strPageName = "Manage Device"
        if 'WEB' in self.client.upper():
            oLandingPage = webPage.BasePage(self.WebDriver, self.reporter)
            oLandingPage.navigate_to_settingScreen(strPageName)
            # oLandingPage.set_device_name(myDeviceName, newDeviceName)

    def updateAlexaResponse(self, resp):
        self.alexaResponse = resp

    def getSchedule(self):
        return self._weeklySchedule

    def setLightSchedule(self, myDeviceName, oSchedule):
        if 'ANDROID' in self.client.upper():
            print('Set Schedule in Android App')
            oActiveLights = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oActiveLights.setBulbModelandName(myDeviceName)
            oActiveLights.navigate_to_active_light_page(myDeviceName)
            oActiveLights.setActiveLightSchedule(myDeviceName, oSchedule)
        elif 'IOS' in self.client.upper():
            oActiveLights = iOSPage.ActiveLights(self.iOSDriver, self.reporter)
            oActiveLights.updateBulbObjects(myDeviceName)
            oActiveLights.navigateToActiveLightControl()
            oActiveLights.set_light_schedule(oSchedule)
        elif 'WEB' in self.client.upper():
            oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
            oHoneycombDashboardPayge.navigate_to_device_product_pageV3(myDeviceID)
            if self.type == 'WARMWHITELIGHT':
                # oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                # oHoneycombDashboardPayge.navigate_to_warm_white_light_product_pageV3(myDeviceID)
                oWarmWhiteLightPage = webPage.WarmWhiteLightPage(self.WebDriver, self.reporter)
                oWarmWhiteLightPage.set_light_schedule(self._weeklySchedule, oSchedule)
            elif self.type == 'TUNEABLELIGHT':
                # oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                # oHoneycombDashboardPayge.navigate_to_tuneable_light_product_page()
                oTuneableLightPage = webPage.TuneableLightPage(self.WebDriver, self.reporter)
                oTuneableLightPage.set_light_schedule(self._weeklySchedule, oSchedule)
            else:
                # oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                # oHoneycombDashboardPayge.navigate_to_colour_light_product_page()
                oColourLightPage = webPage.ColourLightPage(self.WebDriver, self.reporter)
                oColourLightPage.set_light_schedule(self._weeklySchedule, oSchedule)

    def setLightMode(self, myDeviceName, myDeviceID, myMode, propertyName=None, propertyValue=None):
        if 'WEB' in self.client.upper():
            oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
            oHoneycombDashboardPayge.navigate_to_device_product_pageV3(myDeviceID)
            if self.type == 'WARMWHITELIGHT':
                oWarmWhiteLightPage = webPage.WarmWhiteLightPage(self.WebDriver, self.reporter)
                oWarmWhiteLightPage.set_light_mode(myMode, propertyValue)
                if "BRIGHTNESS" in propertyName.upper():
                    oWarmWhiteLightPage.set_brightness(propertyValue)
            elif self.type == 'TUNEABLELIGHT':
                oTuneableLightPage = webPage.TuneableLightPage(self.WebDriver, self.reporter)
                oTuneableLightPage.set_light_mode(myMode, propertyValue)
                if "BRIGHTNESS" in propertyName.upper():
                    oTuneableLightPage.set_brightness(propertyValue)
                elif "TONE" in propertyName.upper:
                    oTuneableLightPage.set_tone(propertyValue)
            elif self.type == 'COLOURLIGHT':
                oColourLightPage = webPage.ColourLightPage(self.WebDriver, self.reporter)
                oColourLightPage.set_light_mode(myMode, propertyValue)
                if "BRIGHTNESS" in propertyName.upper():
                    oColourLightPage.set_brightness(propertyValue)
                elif "TONE" in propertyName.upper:
                    oColourLightPage.set_tone(propertyValue)
                elif "COLOUR" in propertyName.upper:
                    oColourLightPage.set_colour(propertyValue)
        elif 'ANDROID' in self.client.upper():
            oActiveLights = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oActiveLights.setBulbModelandName(myDeviceName)
            oActiveLights.navigate_to_active_light_page(myDeviceName)
            oActiveLights.set_active_light_mode(myMode)
            if propertyName is not None:
                oActiveLights.setValues(propertyName, propertyValue)
                oActiveLights.setValueForBulb(propertyName, propertyValue)
        elif 'IOS' in self.client.upper():
            oActiveLights = iOSPage.ActiveLights(self.iOSDriver, self.reporter)
            oActiveLights.updateBulbObjects(myDeviceName)
            oActiveLights.navigateToActiveLightControl()
            oActiveLights.setActiveLightMode(myMode)
            if propertyName:
                if "BRIGHTNESS" in propertyName.upper() or "TONE" in propertyName.upper() or "COLOUR" in propertyName.upper():
                    oActiveLights.setValues(propertyName, propertyValue)
                    oActiveLights.navigateToSettings(propertyName)
                    oActiveLights.setValueForBulb(propertyName, propertyValue)

    def getAttributesFromClient(self):
        if 'ANDROID' in self.client.upper():
            print('Get Client attributes from Android UI')
        elif 'IOS' in self.client.upper():
            print('Get Client attributes from IOS UI')
        elif 'WEB' in self.client.upper():
            if self.type == 'WARMWHITELIGHT':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_heating_product_page()
                oWarmWhiteLightPage = webPage.WarmWhiteLightPage(self.WebDriver, self.reporter)
                self.mode, self.CurrentDeviceState, self.warmWhiteLightBrightness = \
                    oWarmWhiteLightPage.get_light_attribute()
            if self.type == 'TUNEABLE':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver, self.reporter)
                oHoneycombDashboardPayge.navigate_to_tuneable_light_product_page()
                oTuneableLightPage = webPage.TuneableLightPage(self.WebDriver, self.reporter)
                self.mode, self.CurrentDeviceState, self.warmWhiteLightBrightness = \
                    oTuneableLightPage.get_light_attribute()
        return self.mode, self.CurrentDeviceState, self.warmWhiteLightBrightness

    def resetLightSchedule(self, myDeviceName, oSchedule):
        if 'ANDROID' in self.client.upper():
            oActiveLights = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oActiveLights.setBulbModelandName(myDeviceName)
            oActiveLights.navigate_to_active_light_page(myDeviceName)
            oActiveLights.naviagate_active_light_schedule()
            oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
            oSchedulePage.reset_schedule(oSchedule)
        elif 'IOS' in self.client.upper():
            oActiveLights = iOSPage.ActiveLights(self.iOSDriver, self.reporter)
            oActiveLights.updateBulbObjects(myDeviceName)
            oActiveLights.navigateToActiveLightControl()
            oActiveLights.reset_light_schedule(oSchedule)
        elif 'WEB' in self.client.upper():
            print('Yet to be done for WEB UI')

    def addLightSchedule(self, context, myDeviceName):
        if 'ANDROID' in self.client.upper():
            oActiveLights = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oActiveLights.setBulbModelandName(myDeviceName)
            oActiveLights.naviagate_active_light_schedule()
            oActiveLights.add_light_schedule(context, myDeviceName)
        elif 'IOS' in self.client.upper():
            oActiveLights = iOSPage.ActiveLights(self.iOSDriver, self.reporter)
            oActiveLights.updateBulbObjects(myDeviceName)
            oActiveLights.navigateToActiveLightControl()
            oActiveLights.add_light_schedule(context, myDeviceName)
        elif 'WEB' in self.client.upper():
            print('Yet to be done for WEB UI')

    def delLightSchedule(self, context, myDeviceName):
        if 'ANDROID' in self.client.upper():
            oActiveLights = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oActiveLights.setBulbModelandName(myDeviceName)
            oActiveLights.naviagate_active_light_schedule()
            oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
            oSchedulePage.delete_schedule(context)
        elif 'IOS' in self.client.upper():
            oActiveLights = iOSPage.ActiveLights(self.iOSDriver, self.reporter)
            oActiveLights.updateBulbObjects(myDeviceName)
            oActiveLights.navigateToActiveLightControl()
            oActiveLights.delete_light_schedule(context)
        elif 'WEB' in self.client.upper():
            print('Yet to be done for WEB UI')

    def copyLightSchedule(self, context, myDeviceName):
        if 'ANDROID' in self.client.upper():
            oActiveLights = androidPage.ActiveLights(self.AndroidDriver, self.reporter)
            oActiveLights.setBulbModelandName(myDeviceName)
            oActiveLights.naviagate_active_light_schedule()
            oSchedulePage = androidPage.SchedulePage(self.AndroidDriver, self.reporter)
            oSchedulePage.copy_schedule(context.strDay2, context.strDay1)
        elif 'IOS' in self.client.upper():
            oActiveLights = iOSPage.ActiveLights(self.iOSDriver, self.reporter)
            oActiveLights.updateBulbObjects(myDeviceName)
            oActiveLights.navigateToActiveLightControl()
            oActiveLights.copy_light_schedule(context.strDay2, context.strDay1)
        elif 'WEB' in self.client.upper():
            print('Yet to be done for WEB UI')

    def mimic(self):
        oMimic = androidPage.MIMIC(self.AndroidDriver, self.reporter)
        oMimic.navigate_to_controlPage()

        print(oMimic.set_Hours('13:00--23:00'))


class naThermostatEndpoint(object):
    def __init__(self, platAPI, strServerName):
        # Parent Tstat
        self.parentAPI = platAPI
        self.type = None
        self.serverName = strServerName
        self.client = None
        self.mode = None  # Hold, Auto ,OFF
        self.localTemperature = 0.0  # inside temp
        self.occupiedHeatingSetpoint = 0.0  # targettemp
        self.thermostatRunningState = ''  # ON , OFF for system
        self._weeklySchedule = {}
        self.AndroidDriver = platAPI.AndroidDriver
        self.WebDriver = platAPI.WebDriver
        self.iOSDriver = platAPI.iOSDriver
        self.reporter = platAPI.reporter
        self.Web_ManualModeTargTemp = 20.0
        self.platformVersion = None
        self.occupiedHeatingSetpointChanged = False
        self.strDeviceModeType = ""  # Dual,Hreating,Cooling for wiring
        self.deviceType = ""
        self.currentDeviceNodeId = ""
        self.currentDeviceSDNodeId = ""
        self.CurrentDeviceState = ""
        self.strThermostatName = ""
        self.oNodeScheduleType = ""  # autoschedule, heatschedule,coolschedule
        self.statChannel = None  # Dual,Heating, Cooling

    def updateV6point5(self, nodeID=None):
        try:
            self.AndroidDriver = self.parentAPI.AndroidDriver
            self.WebDriver = self.parentAPI.WebDriver
            self.iOSDriver = self.parentAPI.iOSDriver
            self.reporter = self.parentAPI.reporter

            ALAPI.createCredentials(self.serverName, self.client)
            session = ALAPI.sessionObjectV6dot5()
            self.platformVersion = 'V6.5'
            resp = ALAPI.getNodesV6(session)
            oNodeFeature = None
            oNodeScheduleType = None
            blnThermostatFound = False
            if self.strDeviceModeType.upper() == "HEATING":
                oNodeFeature = 'heating_thermostat_v1'
            elif self.strDeviceModeType.upper() == "COOLING":
                oNodeFeature = 'cooling_thermostat_v1'
            elif "DUAL" in self.strDeviceModeType.upper():
                oNodeFeature = 'heat_cool_thermostat_v1'

            for oNode in resp['nodes']:
                if 'node.class.thermostat.json' in oNode[
                    'nodeType'] and 'features' in oNode and self.strThermostatName.upper() in oNode['name'].upper():
                    if oNodeFeature in oNode['features']:
                        blnThermostatFound = True
                if blnThermostatFound:
                    if not oNode['features']['physical_device_v1']['presence']['reportedValue'] == 'PRESENT':
                        return
                    oFeatureList = oNode['features'][oNodeFeature]
                    strOperatingState = self.getStatOperatingStat(oNode, oNodeFeature)
                    oJson = self.getNASchedule(oFeatureList, self.oNodeScheduleType)
                    if len(oJson) == 1:
                        if isinstance(oJson, str): oJson = json.loads(oJson)
                        self._weeklySchedule = [self._formatScheduleV6dot5(oJson)][0]
                    else:
                        oCompleteSchedule = []
                        for intCounter in range(1, len(oJson) + 1):
                            if isinstance(oJson[intCounter - 1], str): oJson = json.loads(oJson[intCounter - 1])
                            oSchedule = self._formatScheduleV6dot5(oJson[intCounter - 1], intCounter - 1)
                            oCompleteSchedule.append(oSchedule)
                        self._weeklySchedule = oSchdUtil.getActiveSchedule(oCompleteSchedule, self.oNodeScheduleType)

                    strRunningState = self.getAttribute(oNode['features']['on_off_device_v1'], 'mode')
                    self.thermostatRunningState = strRunningState
                    if strOperatingState == 'AUTO':
                        self.occupiedHeatingSetpoint = self.getAutoModeTargetMinMaxTemp(oNode)
                    else:
                        self.occupiedHeatingSetpoint = '{:.1f}'.format(
                            float(oNode['features'][oNodeFeature][strOperatingState]['reportedValue']))
                    self.localTemperature = '{:.1f}'.format(
                        float(oNode['features']['temperature_sensor_v1']['temperature']['reportedValue']))
                    strActiveHeatCoolMode = self.getAttribute(oNode['features'][oNodeFeature],
                                                              'temporaryOperatingModeOverride')
                    strMode = self.getAttribute(oNode['features'][oNodeFeature], 'operatingMode')
                    if strMode == 'MANUAL':
                        strMode = 'HOLD'
                    if strRunningState == 'OFF':
                        self.mode = 'OFF'
                    elif strActiveHeatCoolMode == "TRANSIENT":
                        self.mode = 'BOOST'
                        self.occupiedHeatingSetpoint = '{:.1f}'.format(
                            float(oNode['features']['transient_mode_v1']['actions']['reportedValue'][0]['value']))
                    else:
                        self.mode = strMode
                    self.occupiedHeatingSetpoint = self.convertCelToFarnTemp(self.occupiedHeatingSetpoint)
                    break
        except:
            print('Platform API : NoSuchAttributeException: in updateV6point5 Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def getAutoModeTargetMinMaxTemp(self, oNode):
        strtargetCoolTemp = '{:.1f}'.format(
            float(oNode['features']['heat_cool_thermostat_v1']['targetCoolTemperature']['reportedValue']))
        strtargetHeatTemp = '{:.1f}'.format(
            float(oNode['features']['heat_cool_thermostat_v1']['targetHeatTemperature']['reportedValue']))
        return str(strtargetCoolTemp) + "--" + str(strtargetHeatTemp)

    def getStatType(self, strThermostatName):
        try:
            if strThermostatName == "":
                strThermostatName = "Thermostat 1"
            ALAPI.createCredentials(self.serverName, self.client)
            session = ALAPI.sessionObjectV6dot5()
            self.platformVersion = 'V6.5'
            resp = ALAPI.getNodesV6(session)
            oNodeFeature = None
            oNodeScheduleType = None
            self.reporter = self.parentAPI.reporter

            for oNode in resp['nodes']:
                if strThermostatName.upper() in oNode['name'].upper():
                    if 'heat_cool_thermostat_v1' in oNode['features']:
                        self.strDeviceModeType = "DUAL"
                    elif 'cooling_thermostat_v1' in oNode['features']:
                        self.strDeviceModeType = "COOLING"
                    elif 'heating_thermostat_v1' in oNode['features']:
                        self.strDeviceModeType = "HEATING"

            if self.strDeviceModeType == "":
                self.reporter.ActionStatus = False
                return

        except:
            print('Platform API : NoSuchAttributeException: in getStatType Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

            # For fetching the screen equivalent of mode

    def getStatOperatingStat(self, oNode, oNodeFeature):
        if oNodeFeature == 'heat_cool_thermostat_v1':
            strOperatingState = oNode['features'][oNodeFeature]['temperatureControlMode']['reportedValue']
        else:
            strOperatingState = oNode['features'][oNodeFeature]['operatingState']['reportedValue']

        if strOperatingState != "AUTO":
            self.statChannel = strOperatingState + 'ING'
            strOperatingState = self.UpdateModeScreenEquivalent(strOperatingState + 'ING')
            strTempFeatureAttribute = 'target' + strOperatingState + 'Temperature'
            if strOperatingState.upper() == 'HEAT':
                self.oNodeScheduleType = 'heatSchedule'
            else:
                self.oNodeScheduleType = 'coolSchedule'
        else:
            self.statChannel = 'DUAL'
            strTempFeatureAttribute = "AUTO"
            self.oNodeScheduleType = 'autoSchedule'

        return strTempFeatureAttribute

    def getSchedule(self):
        return self._weeklySchedule

    def getAttribute(self, oAttributeList, strAttributeName):
        reported = oAttributeList[strAttributeName]['reportedValue']
        if 'targetValue' in oAttributeList[strAttributeName]:
            target = oAttributeList[strAttributeName]['targetValue']
            targetTime = oAttributeList[strAttributeName]['targetSetTime']
            currentTime = int(time.time() * 1000)
            if (currentTime - targetTime) < 20000:
                print('taken target value for', strAttributeName)
                return target
        return reported

    def getNASchedule(self, oAttributeList, strAttributeName):
        if 'autoSchedule' in strAttributeName:
            autoSchedule = oAttributeList[strAttributeName]['reportedValue']['setpoints']
            heatSchedule = oAttributeList['heatSchedule']['reportedValue']['setpoints']
            coolSchedule = oAttributeList['coolSchedule']['reportedValue']['setpoints']
            # reported = [autoSchedule,coolSchedule,heatSchedule]

            reported = [autoSchedule]
        else:
            reported = oAttributeList[strAttributeName]['reportedValue']['setpoints']
            reported = [reported]
        return reported

    def _formatScheduleV6dot5(self, respDict, intCount=1):
        oSchedDict = {}
        oNewSchedDict = {}
        oTempDay = None
        oSchedList = []
        for oEvent in respDict[0]:
            oDay = str(oEvent['dayIndex'])
            intHour = int(oEvent['time'].split(':')[0])
            intMin = int(oEvent['time'].split(':')[1])
            if oTempDay is None:
                oTempDay = oDay
            if len(oEvent['actions']) == 1:
                strEvent = self.convertCelToFarnTemp(oEvent['actions'][0]['value'])
            else:
                strEvent = self.convertCelToFarnTemp(oEvent['actions'][1]['value'] + "--" + \
                                                     oEvent['actions'][0]['value'])
            if oTempDay == oDay:
                oSchedList.append(('{:02d}:{:02d}'.format(intHour, intMin), strEvent))
            else:
                oSchedDict.update({oTempDay: oSchedList})
                oTempDay = oDay
                oSchedList = [('{:02d}:{:02d}'.format(intHour, intMin), strEvent)]
        oSchedDict.update({oTempDay: oSchedList})
        oNewSchedDict['mon'] = oSchedDict['1']
        oNewSchedDict['tue'] = oSchedDict['2']
        oNewSchedDict['wed'] = oSchedDict['3']
        oNewSchedDict['thu'] = oSchedDict['4']
        oNewSchedDict['fri'] = oSchedDict['5']
        oNewSchedDict['sat'] = oSchedDict['6']
        oNewSchedDict['sun'] = oSchedDict['7']

        return oNewSchedDict

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

    def getTimeZone(self):
        ALAPI.createCredentials(self.serverName, self.client)
        session = ALAPI.sessionObjectV6dot5()
        self.platformVersion = 'V6.5'
        resp = ALAPI.getTimeZone(session)

        timeZone = resp['users'][0]['timeZone']

        return timeZone

    def UpdateModeScreenEquivalent(self, strMode):
        ModeDictionary = {"HEATING": "Heat", "COOLING": "Cool", "DUAL": "Dual", "OFF": "off", "COOL": "cool",
                          "HEAT": "heat"}
        return ModeDictionary[strMode]

    def setDeviceType(self, strDeviceType):
        if "HEATING" in strDeviceType:
            self.strDeviceModeType = "HEATING"
        elif "COOLING" in strDeviceType:
            self.strDeviceModeType = "COOLING"
        else:
            self.strDeviceModeType = "DUAL"

    def set_NA_schedule(self, context):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.set_NA_schedule(context.oSchedDict)

    def set_NAT_Mode(self, strStatTargChannel, strOperatingMode):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.NAT_ChangeModeAndOperatingMode(strStatTargChannel, strOperatingMode)
        elif 'IOS' in self.client.upper():
            objNATPage = iOSPage.NAT(self.iOSDriver, self.reporter)
            objNATPage.NAT_ChangeModeAndOperatingMode(strStatTargChannel, strOperatingMode, self.strThermostatName)

    def thermostat_selection(self, strThermostatName):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.thermostat_selection(strThermostatName, self.mode)
        elif 'IOS' in self.client.upper():
            objNATPage = iOSPage.NAT(self.iOSDriver, self.reporter)
            objNATPage.navigation_to_NATpage(strThermostatName, self.statChannel, self.thermostatRunningState)

    def set_NAT_Temp(self, strTargetedTemp):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.NAT_setTemp(strTargetedTemp)
        elif 'IOS' in self.client.upper():
            objNATPage = iOSPage.NAT(self.iOSDriver, self.reporter)
            objNATPage.NAT_setTemp(strTargetedTemp, self.strThermostatName)

    def update_NAT_clientOperatingAttributes(self):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            self.clientCurrentTargetTemp, self.clientFlameIconApperance, self.clientThermostatOperatingMode = objNATPage.updateStatOperatingAttributes()
        elif 'IOS' in self.client.upper():
            objNATPage = iOSPage.NAT(self.iOSDriver, self.reporter)
            self.clientCurrentTargetTemp, self.clientFlameIconApperance, self.clientThermostatOperatingMode = objNATPage.updateStatOperatingAttributes(
                self.strThermostatName)

    # Fan, Humdidity and boost

    def checkFeatureSettingsAndMode(self, context, feature, featureSettingMode, operatingMode):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.validateFeatureSettingsAndMode(feature, featureSettingMode, operatingMode)

    def setUserHumidityValue(self, context, humidityValue):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.setHumidity_Value(humidityValue)

    def validateHumidityValue(self, context, humidityValue):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.validate_Humidity_Value(context, humidityValue)

    def userSelectFanSetting(self, context, fanSettingOption):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.select_NA_FanSetting(context, fanSettingOption)

    def validateFanSetting(self, context, fanSettingOption):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.validateFanSettingSelected(context, fanSettingOption)

    def validateFanCirculateOptions(self, context):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.validateCirculateOption(context)

    def validateFanCirculateOptionsSelected(self, context, selectedMins):
        if 'ANDROID' in self.client.upper():
            objNATPage = androidPage.NAT(self.AndroidDriver, self.reporter)
            objNATPage.validateCirculateOptionSelected(context, selectedMins)


class beekeeperEndPoint(object):
    def __init__(self, platAPI, strServerName):

        self.parentAPI = platAPI
        self.reporter = platAPI.reporter
        self.serverName = strServerName
        self.deviceConfig = {}
        self.totalPages = 0
        try:
            ALBKP.createCredentialsBeekeeper(utils.getAttribute('common', 'currentEnvironment'))
            BEEsession = ALBKP.sessionObject()
            BeeUserid = BEEsession.userId
            resp = ALBKP.getAttributesBEE(BEEsession, BeeUserid, 'dashboard-config')
            intPage = 0
            nodesDict = {}
            for eachNode in resp['pages']:
                intPage += 1
                for eachItem in eachNode['items']:
                    nodeID = eachItem['id']
                    nodePos = eachItem['position']
                    nodePage = intPage
                    nodeDict = {nodeID: {'nodePage': intPage, 'nodePosition': nodePos}}
                    nodesDict.update(nodeDict)
            self.deviceConfig = nodesDict
            self.totalPages = intPage
        except:
            print('Exception', "Exception at function beekeeperEndPoint init"
                               " {0}".format(traceback.format_exc().replace('File', '$~File')), 'FAIL')


class Alexa(object):
    def __init__(self):
        self.response = ''

    def update(self, resp):
        self._updateResponse(resp)

    def _updateResponse(self, resp):
        self.response = resp


class mimicEndPoint(object):
    def __init__(self, platAPI, strServerName):
        self.parentAPI = platAPI
        self.serverName = strServerName
        self.client = None
        self.platformVersion = None
        self.AndroidDriver = platAPI.AndroidDriver
        self.WebDriver = platAPI.WebDriver
        self.iOSDriver = platAPI.iOSDriver
        self.reporter = platAPI.reporter
        self.devicesDict = {}
        self.selectedHoursPF = []
        self.selectedCountPF = ''
        self.selectedHours = ''
        self.selectedCount = ''
        self.beekeeperEP = beekeeperEndPoint(self, strServerName)
        self.beekeeperConfig = self.beekeeperEP.deviceConfig
        self.devicePositionDict = {}
        self.beekeeperTotalPages = self.beekeeperEP.totalPages
        self.FONode = False

    def gotoMimicFlowScreen(self, Screen_Name):
        if 'ANDROID' in self.client.upper():
            oMimic = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            oMimic.GotoMimicFlowScreeninApp(Screen_Name)
        elif 'IOS' in self.client.upper():
            print('Get Client attributes from IOS UI')
        elif 'WEB' in self.client.upper():
            print('Get Client attributes from WEB UI')

    def verifyLocalisedCopyText(self, Language):
        if 'ANDROID' in self.client.upper():
            oMimic = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            oMimic.verifyLocalisedCopyTextAndroid(Language)
        elif 'IOS' in self.client.upper():
            print('Get Client attributes from IOS UI')
        elif 'WEB' in self.client.upper():
            print('Get Client attributes from WEB UI')

    # for updating user details like Locale , timezone
    def setUserLocaleAndLanguage(self, Language):
        try:
            Locale = {'UK_English': {'locale': "en_GB", 'timeZone': "Europe/London", 'country': "United Kingdom"},
                      "US_English": {'locale': "en_US", 'timeZone': "America/New_York", 'country': "United States"},
                      "Canadian_English": {'locale': "en_CA", 'timeZone': "America/New_York", 'country': "Canada"},
                      "US_Spanish": {'locale': "en_US", 'timeZone': "America/Mexico_City", 'country': "United States"},
                      "Canadian_French": {'locale': "fr_CA", 'timeZone': "America/Toronto", 'country': "Canada"},
                      "Italian": {'locale': "it_IT", 'timeZone': "Europe/Rome", 'country': "Italy"},
                      "Irish": {'locale': "ga_IE", 'timeZone': "Europe/Dublin", 'country': "Ireland"}
                      }

            if Language == "":
                print("\n Language is not provided")

            ALAPI.createCredentials(self.serverName, self.client)
            session = ALAPI.sessionObjectV6dot5()
            self.platformVersion = 'V6.5'
            blnSuccess = ALAPI.updateUserDetails(session, Locale[Language])
            resp = ALAPI.getUsersV6(session)
            locale = resp['users'][0]['locale']
            if blnSuccess and locale == Locale[Language]['locale']:
                successMessage = '\n User Language is changed successfully to ' + Language
                print(successMessage)
                self.reporter.ReportEvent("Test Validation : API ", successMessage, "PASS")
            else:
                print('\n Problem in changing user locale')
                self.reporter.ReportEvent("Test Validation : API ", 'Problem in changing user locale', "FAIL")
        except:
            self.reporter.ReportEvent('Exception', "Exception at function setUserLocaleAndLanguage"
                                                   " {0}".format(traceback.format_exc().replace('File', '$~File')),
                                      'FAIL')

    # for updating user details like Locale , timezone
    def setUserSubcription(self, strSubscriptionStatus, strSubscription):
        try:
            blnSuccess = False
            ALAPI.createCredentials(self.serverName, self.client)
            session = ALAPI.sessionObject()
            ALBKP.createCredentialsBeekeeper(utils.getAttribute('common', 'currentEnvironment'))
            BEEsession = ALBKP.sessionObject()
            if 'not' in strSubscriptionStatus:
                blnSuccess = ALBKP.removeUserSubcription(session, BEEsession, strSubscription)
            else:
                blnSuccess = ALBKP.setUserSubcription(session, BEEsession, strSubscription)
            if blnSuccess:
                Message = strSubscription + " Subscription set successfully"
                self.reporter.ReportEvent("Test Validation : API ", Message, "PASS")
            else:
                Message = strSubscription + " Subscription setting not successful"
                self.reporter.ReportEvent("Test Validation : API ", Message, "PASS")
            print(Message)
        except:
            self.reporter.ReportEvent('Exception', "Exception at function setUserSubcription"
                                                   " {0}".format(traceback.format_exc().replace('File', '$~File')),
                                      'FAIL')

    def updateMimic(self):
        self.AndroidDriver = self.parentAPI.AndroidDriver
        self.WebDriver = self.parentAPI.WebDriver
        self.iOSDriver = self.parentAPI.iOSDriver
        self.reporter = self.parentAPI.reporter

        self._updateV6()

    def _updateV6(self, nodeID=None):
        try:
            self.FONode = False
            lstMimicConsumers, self.mimicEnabled = self.getMimicAttributes()
            self.selectedCountPF = len(lstMimicConsumers)
            ALAPI.createCredentials(self.serverName, self.client)
            session = ALAPI.sessionObject()
            self.platformVersion = 'V6'
            resp = ALAPI.getNodesV6(session)

            for eachNode in resp['nodes']:
                mimicFlag = False
                if 'nodeType' in eachNode:
                    strNodeType = eachNode['nodeType']
                    if 'light.json' in strNodeType:
                        deviceName = eachNode['name']
                        nodeID = eachNode['id']
                        lstNodeType = strNodeType.split('.')
                        deviceType = lstNodeType[len(lstNodeType) - 3] + ' ' + lstNodeType[len(lstNodeType) - 2]

                        if nodeID in lstMimicConsumers: mimicFlag = True
                        mode, CurrentDeviceState, lightBrightness, floatColourTemperature, weeklySchedule = \
                            pUtils.getLightAttributesFromNode(resp['nodes'], eachNode)
                        modedict = {'AUTO': 'Schedule', 'MANUAL': 'Manual'}
                        mode = modedict[mode]
                        lastChanged = float(str(eachNode['attributes']['state']['reportChangedTime'])[:-3])
                        tz = TZ.getTZ()
                        lastChanged = datetime.fromtimestamp(lastChanged, tz).replace(tzinfo=None)
                        presence = eachNode['attributes']['presence']['reportedValue']
                        nativeIdentifier = eachNode['attributes']['nativeIdentifier']['reportedValue']
                        deviceDict = {
                            deviceName: {'deviceType': deviceType, 'deviceMode': mode,
                                         'deviceState': CurrentDeviceState,
                                         'presence': presence, 'nodeID': nodeID, 'nativeIdentifier': nativeIdentifier,
                                         'mimic': mimicFlag, 'schedule': weeklySchedule,
                                         'lightBrightness': lightBrightness,
                                         'colourTemperature': floatColourTemperature,
                                         'triggerTime': lastChanged}}
                        devicePositionItem = {deviceName: self.beekeeperConfig[nodeID]}
                        self.devicePositionDict.update(devicePositionItem)
                        self.devicesDict.update(deviceDict)

            ALAPI.deleteSessionV6(session)
        except:
            self.reporter.ReportEvent('Exception', "Exception at function _updateV6"
                                                   " {0}".format(traceback.format_exc().replace('File', '$~File')),
                                      'FAIL')

        return True

    def getMimicAttributes(self):
        lstConsumers, enabled = None, None
        try:
            ALAPI.createCredentials(self.serverName, self.client)
            session = ALAPI.sessionObjectV6dot5()
            self.platformVersion = 'V6.5'
            resp = ALAPI.getNodesV6(session)
            lstConsumers = []
            enabled = ''
            for eachNode in resp['nodes']:
                if 'fake.occupancy' in eachNode['nodeType']:
                    self.FONode = True
                    links = eachNode['links']
                    lstConsumers = links['CONSUMER']
                    nodeSched = eachNode['features']['fake_occupancy_v1']['schedule']
                    enabled = eachNode['features']['enable_actions_v1']['enabled']['reportedValue']
                    state = nodeSched['reportedValue']['setpoints'][00]['actions'][0]['value']
                    if state == 'ON':
                        startIndex = 00
                        endIndex = 1
                    else:
                        startIndex = 1
                        endIndex = 1
                    startTime = nodeSched['reportedValue']['setpoints'][startIndex]['time']
                    endTime = nodeSched['reportedValue']['setpoints'][endIndex]['time']
                    self.selectedHoursPF = [startTime, endTime]
            ALAPI.deleteSessionV6(session)
        except:
            self.reporter.ReportEvent('Exception', "Exception at function getMimicAttributes"
                                                   " {0}".format(traceback.format_exc().replace('File', '$~File')),
                                      'FAIL')

        return lstConsumers, enabled

    def setMimic(self, lstHours, lightsConfig):
        if 'ANDROID' in self.client.upper():
            objMimicPage = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            if self.FONode:
                self.reporter.HTML_TC_BusFlowKeyword_Initialize('Fake Occupancy Node is already present')
                objMimicPage.set_mimic()
                objMimicPage.set_Hours(lstHours)
                objMimicPage.select_devices(lightsConfig)
                objMimicPage.restart_Mimic()
            else:
                objMimicPage.initiate_Mimic(lightsConfig, lstHours)
            objMimicPage.refresh_page()

    def stopMimic(self):
        session = ALAPI.sessionObjectV6dot5()
        self.platformVersion = 'V6.5'
        resp = ALAPI.stopMimic(session)
        if 'ANDROID' in self.client.upper():
            objMimicPage = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            objMimicPage.refresh_page()
        ALAPI.deleteSessionV6(session)

    def delMimic(self):
        try:
            session = ALAPI.sessionObjectV6dot5()
            self.platformVersion = 'V6.5'
            resp = ALAPI.delMimic(session)
            ALAPI.deleteSessionV6(session)
        except:
            self.reporter.ReportEvent('Exception', "Exception at function delMimic"
                                                   " {0}".format(traceback.format_exc().replace('File', '$~File')),
                                      'FAIL')

    def getClientSelectedHours(self):
        if 'ANDROID' in self.client.upper():
            objMimicPage = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            self.selectedHours = objMimicPage.device_selected_hours()

    def getClientSelectedCount(self):
        if 'ANDROID' in self.client.upper():
            objMimicPage = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            self.selectedCount = objMimicPage.device_selected_count()

    def getClientLightsStatus(self):
        if 'ANDROID' in self.client.upper():
            objMimicPage = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            self.clientDevicesStatus = objMimicPage.get_client_lights_status(self.devicesDict.keys(),
                                                                             self.devicePositionDict,
                                                                             self.beekeeperTotalPages)

    def updateLightState(self, devicePosition, deviceState, deviceName, deviceMode=None):
        if 'ANDROID' in self.client.upper():
            objMimicPage = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            objMimicPage.refresh_page()
            objMimicPage.set_light_state(devicePosition, deviceState, deviceName, deviceMode)

    def navigateToLight(self, deviceName):
        flag = False
        if 'ANDROID' in self.client.upper():
            objMimicPage = androidPage.MIMIC(self.AndroidDriver, self.reporter)
            objMimicPage.honeycomb_verify()
            devicePosition = self.devicePositionDict[deviceName]
            flag = objMimicPage.find_device_on_dashboard(devicePosition)

        return flag


class Actions(object):
    def __init__(self, platAPI, strServerName):
        self.parentAPI = platAPI
        self.serverName = strServerName
        self.client = None
        self.platformVersion = None
        self.AndroidDriver = platAPI.AndroidDriver
        self.WebDriver = platAPI.WebDriver
        self.iOSDriver = platAPI.iOSDriver
        self.reporter = None

    def updateActions(self):
        self.AndroidDriver = self.parentAPI.AndroidDriver
        self.WebDriver = self.parentAPI.WebDriver
        self.iOSDriver = self.parentAPI.iOSDriver
        self.reporter = self.parentAPI.reporter

    def countActionTemplates(self, Category):
        try:
            if 'ANDROID' in self.client.upper():
                blnSuccess = True
                counter = 0
                categoryTemplates = []
                userLocale = ""
                ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
                session = ALAPI.sessionObject()
                ALBKP.createCredentialsBeekeeper(utils.getAttribute('common', 'currentEnvironment'))
                BEEsession = ALBKP.sessionObject()
                blnSuccess, Counter, categoryTemplates, userLocale = ALBKP.getActionTemplatesAndCount(session,
                                                                                                      BEEsession,
                                                                                                      Category)
                return blnSuccess, str(Counter)
            elif 'IOS' in self.client.upper():
                print("TBD")
        except:
            self.reporter.ReportEvent('Exception', "Exception at function countActionTemplates"
                                                   " {0}".format(traceback.format_exc().replace('File', '$~File')),
                                      'FAIL')

    def countFreeOrPaidActionTemplates(self, templateprice):
        try:
            if 'ANDROID' in self.client.upper():
                blnSuccess = True
                counterFree = 0
                counterPaid = 0
                counterBuildYourOwn = 0
                counterWelcomeHome = 0
                ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
                session = ALAPI.sessionObject()
                ALBKP.createCredentialsBeekeeper(utils.getAttribute('common', 'currentEnvironment'))
                BEEsession = ALBKP.sessionObject()
                blnSuccess, counterFree, counterPaid, counterBuildYourOwn, counterWelcomeHome = ALBKP.countFreeOrPaidActionTemplates(
                    session, BEEsession, templateprice)
                return blnSuccess, str(counterFree), str(counterPaid), str(counterBuildYourOwn), str(counterWelcomeHome)
            elif 'IOS' in self.client.upper():
                print("TBD")
        except:
            self.reporter.ReportEvent('Exception', "Exception at function countFreeOrPaidActionTemplates"
                                                   " {0}".format(traceback.format_exc().replace('File', '$~File')),
                                      'FAIL')

    def navigateToTemplatesCategory(self, Category):
        if 'ANDROID' in self.client.upper():
            oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            oAllRecipes.navigate_to_action_category(Category)
        elif 'IOS' in self.client.upper():
            print("TBD")

    def verify_action_templates_category(self, Category):
        if 'ANDROID' in self.client.upper():
            oAllRecipes = androidPage.AllRecipes(self.AndroidDriver, self.reporter)
            blnSuccess = True
            counter = 0
            categoryTemplates = []
            userDeviceCount = []
            userLocale = ""
            ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
            session = ALAPI.sessionObjectV6dot5()
            ALBKP.createCredentialsBeekeeper(utils.getAttribute('common', 'currentEnvironment'))
            BEEsession = ALBKP.sessionObject()
            userDeviceCount = pUtils.getUserDevicesCount(session)
            categories = {
                'Welcome Home': 'Welcome Home', 'Comfort': 'Comfort', 'Reassurance': 'Reassurance',
                'Efficiency': 'Efficiency', 'Thermostat': 'thermostat', 'Plugs': 'plug',
                'Lights': 'lights', 'Motion Sensor': 'motion-sensor', 'Win/Door Sensor': 'contact-sensor',
                'Hot Water': 'hotwater', 'All actions': 'All actions',
                'Build Your Own': 'Build Your Own'

            }
            blnSuccess, Counter, categoryTemplates, userLocale = ALBKP.getActionTemplatesAndCount(session, BEEsession,
                                                                                                  categories[Category],
                                                                                                  userDeviceCount)
            oAllRecipes.verify_the_action_templates_category(categoryTemplates, Category, userLocale)
            oAllRecipes.navigate_to_back_page()
        elif 'IOS' in self.client.upper():
            print("TBD")

