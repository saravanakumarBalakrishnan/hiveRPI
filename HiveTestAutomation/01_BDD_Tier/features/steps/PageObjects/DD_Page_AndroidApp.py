"""
Created on 16 Jun 2015

@author: ranganathan.veluswamy
"""

import os
import time
import traceback

#from appium import webdriver
#from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
#from appium.webdriver.common.touch_action import TouchAction
import FF_Platform_Utils as Putils
import json
import FF_Beekeeper as Beeutils

from EE_Locators_AndroidApp import LoginPageLocators, HomePageLocators, HeatingControlPageLocators, \
    HotWaterControlPageLocators, SchedulePageLocators, EditTimeSlotPageLocators, EditBoostTimePageLocators, \
    AccountDetailsLocators, HeatingHomePageLocators, HotWaterHomePageLocators, HolidayModeLocators, \
    ChangePasswordLocators, LogoutLocators, TextControlLocators, HoneycombDasbordLocators, HeatingNotificationsLocators, \
    PinLock, MotionSensorLocators, LightBulbLocators, MainMenuLocators, PlugLocators, ActionsScreenLocators, \
    HoneycombDashboardLocators, PlugScheduleLocators, DashboardCustomizationLocators, ContactSensorLocators, \
    NAThermostatLocators
from EE_Locators_AndroidApp import LeakSensorLocators as HLS
from EE_Locators_AndroidApp import MimicLocators as MML
import FF_utils as utils
import FF_ScheduleUtils as oSchedUtils
from datetime import timedelta
from datetime import datetime
import FF_Platform_Utils as pUtils
import math
from selenium.webdriver.common.by import By


class BasePage(object):
    # Contructor for BasePage
    def __init__(self, driver, reporter):
        self.driver = driver
        self.reporter = reporter
        self.EXPLICIT_WAIT_TIME = 25
        self.currentAppVersion = utils.getAttribute('common', 'currentAppVersion').upper()
        # Set the object property value based on app veersion
        if self.currentAppVersion == 'V6':
            self.REFRESH_BUTTON = HomePageLocators.REFRESH_BUTTON_V6
            self.MENU_BUTTON = HomePageLocators.MENU_BUTTON_V6
            self.OFF_MODE_LINK = HeatingControlPageLocators.OFF_MODE_LINK_V6
            self.RUNNING_STATE_CIRCLE = HotWaterControlPageLocators.RUNNING_STATE_CIRCLE_V6
            self.CH_BOOST_MODE_LINK = HeatingControlPageLocators.BOOST_MODE_LINK_V6
            self.HW_BOOST_MODE_LINK = HotWaterControlPageLocators.BOOST_MODE_LINK_V6
            self.ADD_BUTTON = EditTimeSlotPageLocators.ADD_BUTTON_V6
            self.HW_STATUS = HotWaterControlPageLocators.HOTWATER_STATUS

        else:
            self.REFRESH_BUTTON = HomePageLocators.REFRESH_BUTTON
            self.MENU_BUTTON = HomePageLocators.MENU_BUTTON
            self.OFF_MODE_LINK = HeatingControlPageLocators.OFF_MODE_LINK
            self.RUNNING_STATE_CIRCLE = HotWaterControlPageLocators.RUNNING_STATE_CIRCLE
            self.CH_BOOST_MODE_LINK = HeatingControlPageLocators.BOOST_MODE_LINK
            self.HW_BOOST_MODE_LINK = HotWaterControlPageLocators.BOOST_MODE_LINK
            self.ADD_BUTTON = EditTimeSlotPageLocators.ADD_BUTTON

    # Check for the given element existence
    def is_element_present(self, by, value=None):
        # Return a boolean value for an  element presence
        try:
            self.driver.find_element(by, value)

        except NoSuchElementException as e:
            return False
        return True

    # Waits for the given element exists for EXPLICIT_WAIT_TIME
    def wait_for_element_exist(self, by, value, intWaitTime=0):
        if intWaitTime == 0: intWaitTime = self.EXPLICIT_WAIT_TIME
        try:
            wait = WebDriverWait(self.driver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            time.sleep(1)
            return True
        except TimeoutException:
            print(by, value, 'element not found')
            return False

    # Waits for the given element exists for EXPLICIT_WAIT_TIME
    def wait_for_element_exist_for_given_time(self, by, value, intWaitTime=0):
        if intWaitTime == 0: intWaitTime = self.EXPLICIT_WAIT_TIME
        intWaitTime = 4
        intCntr = 0
        boolElementExist = False
        while not (intCntr > intWaitTime or boolElementExist):
            try:
                # oElement = self.driver.find_element(by, value)
                boolElementExist = True
            except:
                boolElementExist = False
                intCntr += 1
                time.sleep(1)
        if boolElementExist:
            return True
        else:
            return False

    # Initializes the Appium Android Web Driver
    def setup_android_driver(self, strAndroidPlatformVersion, strDeviceName, strAppPath):
        desired_caps = {'appium-version': '1.5.03', 'platformName': 'Android',
                        'platformVersion': strAndroidPlatformVersion, 'deviceName': strDeviceName,
                        'app': os.path.abspath(strAppPath), 'appPackage': utils.getAttribute('android', 'appPackage'),
                        'appActivity': utils.getAttribute('android', 'appActivity'),
                        'udid': utils.getAttribute('android', 'appium_udid'), 'noReset': True,
                        'newCommandTimeout': 9000}
        strPort = utils.getAttribute('common', 'appium_port')
        if strPort == "": strPort = "4723"
        print('using Port', strPort)
        intNumb = strPort[3:]
        print('http://127.0.0.' + intNumb + ':' + strPort + '/wd/hub')
        # oAndroidDriver = webdriver.Remote('http://127.0.0.' + intNumb + ':' + strPort + '/wd/hub', desired_caps)
        oAndroidDriver = webdriver.Remote('http://127.0.0.1:' + strPort + '/wd/hub', desired_caps)

        '''desired_caps = {}
        desired_caps['browserName'] = ""
        desired_caps['appiumVersion'] = "1.4.13"
        desired_caps['deviceName'] = "LG Nexus 4 Emulator"
        desired_caps['deviceOrientation'] = "portrait"
        desired_caps['platformVersion'] = "4.4"
        desired_caps['platformName'] = "Android"
        desired_caps['app'] = "sauce-storage:intProd46.apk"
        desired_caps["noReset"] = True
    
        oAndroidDriver = webdriver.Remote(command_executor="http://BGCHIS:3c0fd44d-951a-48b4-aa77-80fe20904233@ondemand.saucelabs.com:80/wd/hub", desired_capabilities = desired_caps)
        '''
        oAndroidDriver.implicitly_wait(15)

        return oAndroidDriver

    # Report the Failure step the HTML report
    def report_fail(self, strFailDescription):
        self.reporter.ActionStatus = False
        self.reporter.ReportEvent('Test Validation', strFailDescription, "FAIL", 'Center', True, self.driver)

    # Report the Pass step the HTML report
    def report_pass(self, strPassDescription):
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strPassDescription, "PASS", 'Center', True, self.driver)

    # Report the Done step the HTML report
    def report_done(self, strStepDescription):
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strStepDescription, "DONE", 'Center', True, self.driver)

    # Report the Done step the HTML report
    def report_step(self, strStepDescription):
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strStepDescription, "DONE", 'Center', True)

    # Scrolls on the Scrollable element to set the specific value passed
    def scroll_element_to_value(self, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision, fltScrolPrecesion):
        intLeftX = oScrolElement.location['x']
        intUpperY = oScrolElement.location['y']
        intWidth = oScrolElement.size['width']
        intHieght = oScrolElement.size['height']
        intStX = intLeftX + intWidth / 2
        intStY = intUpperY + fltScrolPrecesion * (intHieght / 4)
        intEndX = intStX
        intEndY = intUpperY + 3 * (intHieght / 4)
        if not float(fltSetValue) == float(fltCurrentValue):
            if float(fltSetValue) < float(fltCurrentValue):
                intTemp = intEndY
                intEndY = intStY
                intStY = intTemp
            intIterCount = int(abs(float(fltSetValue) - float(fltCurrentValue)) / float(fltPrecision))
            if intIterCount == 0: intIterCount = 1
            for intCnt in range(intIterCount):
                self.driver.swipe(intStX, intEndY, intEndX, intStY, 1000)
                time.sleep(0.8)

    # Scrolls on the Scrollable element to set the specific value passed
    def scroll_element_to_value_NA(self, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision,
                                   fltScrolPrecesion):
        intLeftX = oScrolElement.location['x']
        intUpperY = oScrolElement.location['y']
        intWidth = oScrolElement.size['width']
        intHieght = oScrolElement.size['height']
        intStX = intLeftX + intWidth / 2
        intStY = intUpperY + 3 * (intHieght / 10)
        intEndX = intStX
        intEndY = intUpperY + 7 * (intHieght / 10)
        if not float(fltSetValue) == float(fltCurrentValue):
            if float(fltSetValue) < float(fltCurrentValue):
                intTemp = intEndY
                intEndY = intStY
                intStY = intTemp
            intIterCount = int(abs(float(fltSetValue) - float(fltCurrentValue)) / float(fltPrecision))
            if intIterCount == 0: intIterCount = 1
            for intCnt in range(intIterCount):
                self.driver.swipe(intStX, intEndY, intEndX, intStY, 500)
                time.sleep(1)

    # Add/Delete Events to match the expected count
    def add_or_remove_events(self, intExpectedEventCount):
        if self.reporter.ActionStatus:
            try:
                self.report_done('ScreenShot of existing schedule')
                # Get Event Count
                lstMoreOptions = self.driver.find_elements(*SchedulePageLocators.EVENT_OPTIONS_BUTTON)
                intActualCount = len(lstMoreOptions)
                print(intActualCount, intExpectedEventCount)

                self.reporter.HTML_TC_BusFlowKeyword_Initialize(
                    'Expected and Actual Number of Events')

                strLog = "Expected Events $$Actual Events$$Events to be Added or Deleted @@@" + str(
                    intExpectedEventCount) + "$$" + str(intActualCount) + "$$" + str(
                    intActualCount - intExpectedEventCount)
                if intActualCount > intExpectedEventCount:
                    # Delete Event
                    strLog = "Expected Events $$Actual Events$$Events to be Deleted @@@" + str(
                        intExpectedEventCount) + "$$" + str(intActualCount) + "$$" + str(
                        intActualCount - intExpectedEventCount)
                    self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                    for intCntr in range((intActualCount - 1), intExpectedEventCount - 1, -1):
                        # input('KK')
                        lstMoreOptions[intCntr].click()
                        self.report_done('Deleting additional event number : ' + str(intCntr + 1))
                        if self.wait_for_element_exist(*SchedulePageLocators.DELETE_EVENT_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.DELETE_EVENT_SUBMENU).click()
                            time.sleep(2)
                            if self.is_element_present(*SchedulePageLocators.SCHEDULE_YES_BUTTON):
                                self.driver.find_element(*SchedulePageLocators.SCHEDULE_YES_BUTTON).click()
                        else:
                            self.report_fail('Element DELETE_EVENT_SUBMENU is not found')
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                elif intActualCount < intExpectedEventCount:
                    # Add Event
                    strLog = "Expected Events $$Actual Events$$Events to be Added @@@" + str(
                        intExpectedEventCount) + "$$" + str(intActualCount) + "$$" + str(
                        intExpectedEventCount - intActualCount)
                    self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                    for intCntr in range((intExpectedEventCount - 1), intActualCount - 1, -1):
                        if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                            self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        else:
                            self.report_fail('Element SCHEDULE_OPTIONS_BUTTON is not found')
                        if self.wait_for_element_exist(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU).click()
                        else:
                            self.report_fail('Element ADD_TIME_SLOT_SUBMENU is not found')

                        self.report_done('Adding additional event number : ' + str(intCntr + 1))
                        if self.wait_for_element_exist(*self.ADD_BUTTON):
                            self.driver.find_element(*self.ADD_BUTTON).click()
                        else:
                            self.report_fail('Element ADD_BUTTON is not found')

                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                else:
                    self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                self.driver.find_element(*self.REFRESH_BUTTON).click()
                time.sleep(5)
                self.wait_for_element_exist(*self.REFRESH_BUTTON)
                self.report_pass('ScreenShot after all additional events are added/removed')
            except:
                self.report_fail('Android App : NoSuchElementException: in add_or_remove_events Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
                # Navigate to the Day of the Week

    def _navigate_to_day(self, strDay):
        if self.reporter.ActionStatus:
            try:
                self.reporter.HTML_TC_BusFlowKeyword_Initialize("Navigating to day - " + strDay.upper())
                if strDay.upper() == 'MON':
                    self.driver.find_element(*SchedulePageLocators.MON_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'TUE':
                    self.driver.find_element(*SchedulePageLocators.TUE_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'WED':
                    self.driver.find_element(*SchedulePageLocators.WED_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'THU':
                    self.driver.find_element(*SchedulePageLocators.THU_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'FRI':
                    self.driver.find_element(*SchedulePageLocators.FRI_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'SAT':
                    self.driver.find_element(*SchedulePageLocators.SAT_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'SUN':
                    self.driver.find_element(*SchedulePageLocators.SUN_SCHEDULE_BUTTON).click()

                self.driver.find_element(*self.REFRESH_BUTTON).click()
                time.sleep(5)
                self.wait_for_element_exist(*self.REFRESH_BUTTON)

            except:
                self.report_fail('Android App : NoSuchElementException: in _navigate_to_day Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set the Even Target temperature
    def set_schedule_event_hour(self, intSetHour, intScrollPrecision=1.8, intCurrentHour=None):
        if self.reporter.ActionStatus:
            try:

                if self.is_element_present(*EditTimeSlotPageLocators.FORMAT_SCROLL):
                    blnPMflag = False
                    oFormatScrollElement = self.driver.find_element(*EditTimeSlotPageLocators.FORMAT_SCROLL)
                    if int(intSetHour) > 11:
                        blnPMflag = True
                        intSetHour = int(intSetHour) % 12
                    strText = oFormatScrollElement.find_element(
                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                        'name').upper()
                    if 'A' in strText and blnPMflag:
                        self.scroll_element_to_value(oFormatScrollElement, 1, 2, 1, intScrollPrecision)
                    elif 'P' in strText and not blnPMflag:
                        self.scroll_element_to_value(oFormatScrollElement, 2, 1, 1, intScrollPrecision)

                if self.wait_for_element_exist(*EditTimeSlotPageLocators.HOUR_SCROLL):

                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                    intSetHour = int(intSetHour)
                    if intCurrentHour is None:
                        intCurrentHour = int(
                            oScrolElement.find_element(
                                *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                'name'))
                    else:
                        intCurrentHour = int(intCurrentHour)

                    self.scroll_element_to_value(oScrolElement, intCurrentHour, intSetHour, 1, intScrollPrecision)
                else:
                    self.report_fail(
                        "Android-App : Control not active on the Edit Time Slot for schedule Page to set the Event start time Hour")

            except:
                self.report_fail('Android App : NoSuchElementException: in set_schedule_event_hour Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set the Boost Time
    def set_boost_time_duration(self, intSetHour):
        if self.reporter.ActionStatus:
            try:

                self.driver.find_element(*HeatingControlPageLocators.BOOST_TIMER).click()
                time.sleep(2)
                if self.wait_for_element_exist(*EditBoostTimePageLocators.BOOST_TIME_SCROLL):
                    oScrolElement = self.driver.find_element(*EditBoostTimePageLocators.BOOST_TIME_SCROLL)
                    intSetHour = int(intSetHour)
                    if intSetHour == 0.5: intSetHour = 0
                    intCurrentHour = oScrolElement.find_element(
                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute('name')
                    if '30' in intCurrentHour:
                        intCurrentHour = 0
                    else:
                        intCurrentHour = int(intCurrentHour.split(' ')[0])
                    self.scroll_element_to_value(oScrolElement, intCurrentHour, intSetHour, 1, 1.8)
                    self.driver.find_element(*EditBoostTimePageLocators.SAVE_BUTTON).click()

                else:
                    self.report_fail(
                        "Android-App : Control not active on the Edit Boost Time for schedule Page to set the Boost duration Hour")

            except:
                self.report_fail('Android App : Exception: in set_boost_time_duration Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set the Event Target temperature
    def set_schedule_event_minute(self, intSetMinute, intScrollPrecision=1.8, intPrecision=15, intCurrentMinute=None):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                    intSetMinute = int(intSetMinute)
                    if intCurrentMinute is None:
                        intCurrentMinute = int(
                            oScrolElement.find_element(
                                *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                'name'))
                    else:
                        intCurrentMinute = int(intCurrentMinute)

                    self.scroll_element_to_value(oScrolElement, intCurrentMinute, intSetMinute, intPrecision,
                                                 intScrollPrecision)

                else:
                    self.report_fail(
                        "Android-App : Control not active on the Edit Time Slot for Heating schedule Page to set the Event start time Minute")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_schedule_event_minute Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

                # Set the Even Target temperature

    def set_schedule_target_temperature(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try:
                fltSetTargTemp = float(fltSetTargTemp)
                if fltSetTargTemp == 1.0: fltSetTargTemp = 7.0
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.EVENT_TARGET_TEMPERATURE_SCROLL):
                    oScrolElement = self.driver.find_element(
                        *EditTimeSlotPageLocators.EVENT_TARGET_TEMPERATURE_SCROLL)
                    strContent = oScrolElement.get_attribute('name')
                    fltCurrentTargTemp = float(self.get_TempFromElement(strContent))
                    intCntrIter = 1
                    if fltCurrentTargTemp != fltSetTargTemp:
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5,
                                                     2)
                    self.report_done(
                        "Screenshot after target Temp is set")
                else:
                    self.report_fail(
                        "Control not active on the Edit Time Slot for Heating schedule Page to set the Event Target Temperature")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_schedule_target_temperature Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def set_NA_schedule_target_temerature(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try:
                if '--' in fltSetTargTemp:
                    intCount = 1
                    fltCoolTemp = float(fltSetTargTemp.split('--')[0])
                    fltHeatTemp = float(fltSetTargTemp.split('--')[1])
                    while intCount < 3:
                        if intCount == 1:
                            fltSetTargTemp = fltHeatTemp
                            objProperty = NAThermostatLocators.THERMOSTAT_HEATWHEEL_LAYOUT
                        else:
                            fltSetTargTemp = fltCoolTemp
                            objProperty = NAThermostatLocators.THERMOSTAT_COOLWHEEL_LAYOUT

                        if self.wait_for_element_exist(*objProperty):
                            oScrolElement = self.driver.find_element(
                                *objProperty)
                            strContent = self.driver.find_element(
                                *objProperty).get_attribute('name').split(' ')[2]
                            fltCurrentTargTemp = float(strContent)
                            if fltCurrentTargTemp != fltSetTargTemp:
                                self.scroll_element_to_value_NA(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 1,
                                                                2)

                            self.report_done('Screenshot after setting up the temp')
                        else:
                            self.report_fail(
                                "Control not active on the Edit Time Slot for schedule Page to set the Event Target Temperature")
                        intCount = intCount + 1
                else:
                    fltSetTargTemp = float(fltSetTargTemp)
                    if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_TEMP_PICKER):
                        oScrolElement = self.driver.find_element(
                            *NAThermostatLocators.THERMOSTAT_TEMP_PICKER)
                        strContent = self.driver.find_element(
                            *NAThermostatLocators.THERMOSTAT_TEMP_VALUE).get_attribute('text')
                        fltCurrentTargTemp = float(strContent[:2])
                        intCntrIter = 1
                        if fltCurrentTargTemp != fltSetTargTemp:
                            self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 1,
                                                         2)

                        self.report_done('Screenshot after setting up the temp')
                    else:
                        self.report_fail(
                            "Control not active on the Edit Time Slot for schedule Page to set the Event Target Temperature")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_NA_schedule_target_temerature Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def set_holiday_target_temp(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HolidayModeLocators.TEMP_PICKER):
                    oScrolElement = self.driver.find_element(
                        *HolidayModeLocators.TEMP_PICKER)
                    strContent = oScrolElement.get_attribute('name')
                    fltCurrentTargTemp = float(self.get_TempFromElement(strContent))
                    intCntrIter = 1
                    self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5,
                                                 2)
                else:
                    self.report_fail(
                        "Control not active on holiday Target Temperature")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_schedule_target_temperature Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Refresh Page
    def refresh_page(self):
        try:
            self.driver.find_element(*self.REFRESH_BUTTON).click()
            time.sleep(5)
            self.wait_for_element_exist(*self.REFRESH_BUTTON)
        except:
            self.report_fail('Android App : NoSuchElementException: in refresh_page Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # replace a object's xpath value in runtime
    def set_TO_property(self, tplObject, propName, propValue):
        lst = list(tplObject)
        lst[1] = str(lst[1]).replace(propName, propValue)
        return tuple(lst)

    # function to navigate to the Control page
    def click_controlicon(self):
        try:
            self.reporter.HTML_TC_BusFlowKeyword_Initialize('Control Page Navigation')
            time.sleep(5)
            self.wait_for_element_exist(*self.REFRESH_BUTTON)
            if self.wait_for_element_exist(*SchedulePageLocators.CONTROL_ICON):
                self.report_pass('Control icon found')
                self.driver.find_element(*SchedulePageLocators.CONTROL_ICON).click()
                self.report_done('Control Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('Control icon is not present')
        except:
            self.report_fail('Android-App : NoSuchElementException: in click_controlicon Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Verify the dashboard screen
    def honeycomb_verify(self):
        try:
            blnFlag = False
            if not self.is_element_present(*HoneycombDashboardLocators.DASHBOARD_ICON):
                if self.is_element_present(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                    self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                    time.sleep(3)
                    if not self.is_element_present(*HoneycombDashboardLocators.DASHBOARD_ICON):
                        self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                        time.sleep(5)
                        blnFlag = True

                else:
                    self.report_fail('Android-App Honeycomb Dashboard : Dashboard icon is not displayed ')
                    return

            if blnFlag:
                self.dashboardSwipe()
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in honeycomb_verify Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # For performing swipe at the dashboard
    def dashboardSwipe(self, blnLeftNavigation=True):
        try:
            if self.wait_for_element_exist(*HoneycombDashboardLocators.DASHBOARD_ICON):
                oLeftElement = self.driver.find_element(*HoneycombDashboardLocators.DASHBOARD_LEFT_ICON)
                oRightElement = self.driver.find_element(*HoneycombDashboardLocators.DASHBOARD_RIGHT_ICON)
                intLeftX = oLeftElement.location['x']
                intLeftY = oLeftElement.location['y']
                intRightX = oRightElement.location['x']
                intRightY = oRightElement.location['y']
                if blnLeftNavigation:
                    self.driver.swipe(intLeftX, intLeftY, intRightX, intRightY, 5000)
                else:
                    self.driver.swipe(intRightX, intRightY, intLeftX, intLeftY, 5000)

                time.sleep(2)
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in dashboardSwipe: Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Device list Navigation
    def device_list_navigation(self):
        try:
            self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
            time.sleep(4)
            if self.is_element_present(*HoneycombDashboardLocators.DASHBOARD_ICON):
                self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
            time.sleep(4)

        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function device_list_navigation \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def get_TempFromElement(self, strContent):
        strTemp = ' '
        strTargetTempSplitted = strContent.upper().split(' ')
        if 'TEMPERATURE,' in strTargetTempSplitted:
            intTempPositionCounter = strTargetTempSplitted.index('TEMPERATURE,') + 1
        else:
            intTempPositionCounter = strTargetTempSplitted.index('NOTIFICATION,') + 1
        if intTempPositionCounter >= 0:
            strTemp = strTargetTempSplitted[intTempPositionCounter]
            if strTemp.upper() == 'FROST':
                strTemp = '7.0'
        return strTemp

    def find_device_on_dashboard(self, devicePosition):
        flag = False
        try:
            count = int(devicePosition['nodePage'])
            while count > 1:
                self.dashboardSwipe(False)
                count -= 1

            lstDeviceNameProperty = list(HoneycombDashboardLocators.DASHBOARD_ICON_SLOT)
            lstDeviceNameProperty[1] = lstDeviceNameProperty[1] + str(devicePosition['nodePosition'])
            objDeviceNameProperty = tuple(lstDeviceNameProperty)

            if self.wait_for_element_exist(*objDeviceNameProperty):
                self.driver.find_element(*objDeviceNameProperty).click()
                flag = True
                time.sleep(4)

            self.refresh_page()
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function find_device_on_dashboard \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
        return flag


# Page Class for Login page. Has all the methods for the Login page
class LoginPage(BasePage):
    # Log in to the Hive Mobile App
    def login_hive_app(self, strUserName, strPassword):
        if self.reporter.ActionStatus:
            # self.driver.reset()
            try:
                if self.is_element_present(*HomePageLocators.SKIP_BUTTON):
                    self.driver.find_element(*HomePageLocators.SKIP_BUTTON).click()
                if self.is_element_present(*LoginPageLocators.TITLE_LABEL):
                    if self.is_element_present(*LoginPageLocators.USERNAME_EDTBOX):
                        self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys(strUserName)
                        self.driver.hide_keyboard()
                        self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys(strPassword)
                        self.driver.hide_keyboard()
                        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                if self.is_element_present(*HoneycombDasbordLocators.HONEYCOMB_SHOW_DASHBOARD):
                    self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_SHOW_DASHBOARD).click()

                    if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                        self.report_pass('Android-App : The Hive App is successfully Logged in')
                    else:
                        self.report_fail(
                            'Android App : The Hive App is not logged in. Please check the Login credentials and re-execute test.')

                        # else:
                        # self.report_fail('Android App : The Hive App is either not Launched or the Login screen is not displayed. Please check and re-execute test.')

            except:
                self.report_fail('Android App : NoSuchElementException: in login_hive_app Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def enter_credentials(self, Username, Password):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*LoginPageLocators.TITLE_LABEL):
                    self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys(Username)
                    self.driver.hide_keyboard()
                    self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys(Password)
                    self.driver.hide_keyboard()
            except:
                self.report_fail('Android App : NoSuchElementException: in login_hive_app Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def login_click(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*LoginPageLocators.TITLE_LABEL):
                    self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                    #    if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_SHOW_DASHBOARD):
                    #    self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_SHOW_DASHBOARD).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in login_hive_app Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def login_verify(self):

        if self.wait_for_element_exist(*self.REFRESH_BUTTON):
            self.report_pass('Android-App : The Hive App is successfully Logged in')
        else:
            self.report_fail(
                'Android App : The Hive App is not logged in. Please check the Login credentials and re-execute test.')
        print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper)

        # Page Class for Home page. Has all the methods for the Home page


class HomePage(BasePage):
    # Navigates to the Heating Home Page
    def navigate_to_heating_home_page(self):
        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        'HEATING') >= 0:
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).text)
                    # Verify Dashboard
                    self.honeycomb_verify()
                    # Click on Dashboad icon of heating i.e. 1st one
                    if self.wait_for_element_exist(*HomePageLocators.HEATING_DASHBOARD_ICON):
                        self.driver.find_element(*HomePageLocators.HEATING_DASHBOARD_ICON).click()
                        if self.is_element_present(*HomePageLocators.HEATING_NEWLOOK_OKbutton):
                            self.driver.find_element(*HomePageLocators.HEATING_NEWLOOK_OKbutton).click()
                        time.sleep(3)
                    elif self.currentAppVersion == 'V6':
                        time.sleep(2)
                        self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                        if self.wait_for_element_exist(*HomePageLocators.HEAT_WATER_MAIN_MENU):
                            self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                            time.sleep(2)
                            if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_HEATING_ON):
                                self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_HEATING_ON).click()
                            elif self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_HEATING_OFF):
                                self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_HEATING_OFF).click()
                                time.sleep(2)
                    self.report_done('Screen shot after navigation')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_heating_homepage Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Navigates to the Hot water Home Page
    def navigate_to_hot_water_home_page(self):
        if self.reporter.ActionStatus:
            try:
                print("1")
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        'HOT WATER') >= 0:
                    print("2")
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))

                    # Verify Dashboard
                    self.honeycomb_verify()
                    # Click on Dashboad icon of heating i.e. 1st one
                    if self.wait_for_element_exist(*HomePageLocators.HOTWATER_DASHBOARD_ICON):
                        self.driver.find_element(*HomePageLocators.HOTWATER_DASHBOARD_ICON).click()
                        time.sleep(3)
                        self.report_pass('Successfully navigated to the Hot Water Home Page')
                    elif self.currentAppVersion == 'V6':
                        print("3")
                        time.sleep(2)
                        self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                        if self.wait_for_element_exist(*HomePageLocators.HEAT_WATER_MAIN_MENU):
                            print("4")
                            self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                            time.sleep(2)
                            print("5")
                            time.sleep(2)
                            if self.wait_for_element_exist(*HomePageLocators.HOT_WATER_SUBMENU):
                                self.driver.find_element(*HomePageLocators.HOT_WATER_SUBMENU).click()
                                time.sleep(3)
                                if self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute(
                                        'name').upper().find('HOT WATER') >= 0:
                                    self.report_pass('Successfully navigated to the Hot Water Home Page')
                    else:
                        self.report_fail('Android App : Unable to navigate to Hot Water Home Page')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_hot_water_homepage Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    """ def navigate_to_screen(self, strPageName):
        if self.reporter.ActionStatus:
            try: 
                print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                if self.wait_for_element_exist(*self.MENU_BUTTON):
                    self.driver.find_element(*self.MENU_BUTTON).click()
                    time.sleep(2)
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass("Android App :")
                    if strPageName == "account details":
                        time.sleep(2)
                        self.driver.find_element(*AccountDetailsLocators.ACCOUNT_SUB_MENU).click()
                    if strPageName == "holiday mode":
                        time.sleep(2)
                        self.driver.find_element(*HomePageLocators.HOLIDAY_SUB_MENU).click()
                        time.sleep(2)
                        self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
                        time.sleep(2)
                        print("\n *****************************"+ time.strftime("%d")+"\n ")
                        if self.driver.wait_for_element_exist(*HolidayModeLocators.START_DATE_TIME):
                            print("\n *****************************"+ time.strftime("%d")+"\n ")
                            self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
                            print("\n *****************************"+ time.strftime("%d")+"\n ")
                        else:
                            print("\n *****************************"+ time.strftime("%d")+"\n ")
                            self.driver.find_element_by_id(*HolidayModeLocators.TITLE).click()
                            time.sleep(2)
                        self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
                        print("\n *****************************"+ time.strftime("%d")+"\n ")
                        
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
"""

    # Log out of the Hive Mobile App
    def logout_hive_app(self):
        # self.driver.reset()
        try:
            if not 'LOGIN' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper():
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_SHOW):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.wait_for_element_exist(*LogoutLocators.LOGOUT_OPTION)
                    self.driver.find_element(*LogoutLocators.LOGOUT_OPTION).click()
                    time.sleep(5)
                    if 'LOGIN' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute(
                            'name').upper():
                        self.report_pass('Android-App: The Hive Android App is successfully Logged out')

        except:
            self.report_fail('Android-App: Exception in logout_hive_app Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def logout_hive(self):

        try:
            if not 'LOG IN' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper():
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_SHOW):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                if self.wait_for_element_exist(*LogoutLocators.LOGOUT_OPTION):
                    self.driver.find_element(*LogoutLocators.LOGOUT_OPTION).click()
                    time.sleep(5)
                    if 'LOGIN' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute(
                            'name').upper():
                        self.report_pass('Android-App: The Hive Android App is successfully Logged out')

        except:
            self.report_fail('Android-App: Exception in logout_hive Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def verify_dashboardscreen(self):

        if self.wait_for_element_exist(*HomePageLocators.DASHBOARD_TITLE) and \
                self.wait_for_element_exist(*HomePageLocators.SwitchOver_Button):
            self.report_done('User is in Dashboard Screen')

        elif self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
            self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
            time.sleep(2)
            self.report_done(
                'User is now on Dashboard screen ')
        else:
            self.report_fail(
                'Dashboard is not displayed, unable to proceed with scenaio')

    def verify_emptyslots(self):
        nodes = Putils.getNodes()
        count = 0
        for oNode in nodes['nodes']:
            if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.thermostatui.json#':
                receiverid = oNode["relationships"]["boundNodes"][0]["id"]
                receiver = Putils.getNodeByID(receiverid)
                if receiver["nodes"][0]["attributes"]["model"]["reportedValue"] == 'SLR2':
                    count += 2
                elif receiver["nodes"][0]["attributes"]["model"]["reportedValue"] == 'SLR1':
                    count += 1
            elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.smartplug.json#':
                count += 1
            elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.motion.sensor.json#':
                count += 1
            elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.contact.sensor.json#':
                count += 1
            elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.light.json#':
                count += 1
            elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.tunable.light.json#':
                count += 1
            elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.colour.tunable.light.json#':
                count += 1
        print(count)
        self.report_done('No of devices in the kit is ' + str(count))
        if count <= 7:
            result = 7 - count
            if result == 0:
                if not self.driver.find_element(*HomePageLocators.EmptySlots_Dashboard):
                    self.report_pass('All slots are filled by 7 devices')
                else:
                    self.report_fail('Empty slots should not be present')
            else:
                if self.wait_for_element_exist(*HomePageLocators.EmptySlots_Dashboard):
                    size = self.driver.find_elements(*HomePageLocators.EmptySlots_Dashboard).len()
                    if size == result:
                        self.report_pass(str(result) + ' Empty slots are present.')
                    else:
                        self.report_fail(str(size) + ' Empty slots are present only which is less.')
                else:
                    self.report_fail('Empty slots are not present.')
        else:
            if count <= 14:
                result = 14 - count

                self.dashboardSwipe(False)
            else:
                result = 21 - count
                self.dashboardSwipe(False)

            if self.wait_for_element_exist(*HomePageLocators.EmptySlots_Dashboard):
                size = len(self.driver.find_elements(*HomePageLocators.EmptySlots_Dashboard))
                if size == result:
                    self.report_pass(str(result) + ' Empty slots are present.')
                else:
                    self.report_fail(str(size) + ' Empty slots are present only which is less.')
            else:
                self.report_fail('Empty slots are not present.')

    def navigation_to_devicepage(self, deviceName):
        self.honeycomb_verify()
        device_icon_on_dashboard = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
        device_icon_on_dashboard = device_icon_on_dashboard.replace("deviceName", deviceName)
        time.sleep(3)
        if 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('text').upper():

            if self.wait_for_element_exist(By.XPATH, device_icon_on_dashboard):
                if deviceName.upper() in self.driver.find_element(By.XPATH, device_icon_on_dashboard).get_attribute(
                        'text').upper():
                    self.driver.find_element(By.XPATH, device_icon_on_dashboard).click()
                    self.report_pass(deviceName + ' is found and clicked')
                else:
                    self.report_fail(deviceName + ' and Locators are not matched')
            else:

                self.dashboardSwipe(False)
                if self.wait_for_element_exist(By.XPATH, device_icon_on_dashboard):
                    if deviceName.upper() in self.driver.find_element(By.XPATH, device_icon_on_dashboard).get_attribute(
                            'text').upper():
                        self.driver.find_element(By.XPATH, device_icon_on_dashboard).click()
                        self.report_pass(deviceName + ' is found and clicked')
                    else:
                        self.report_fail(deviceName + ' and Locators are not matched')
                else:
                    self.report_fail(deviceName + ' is not found')
        else:
            # making to be on dashboard screen
            self.wait_for_element_exist(*HoneycombDasbordLocators.HONEY_DASHBOARD_HOME_BUTTON)
            self.driver.find_element(*HoneycombDasbordLocators.HONEY_DASHBOARD_HOME_BUTTON).click()
            self.wait_for_element_exist(*HomePageLocators.REFRESH_BUTTON_V6)

            if self.wait_for_element_exist(By.XPATH, device_icon_on_dashboard):
                self.driver.find_element(By.XPATH, device_icon_on_dashboard).click()
                time.sleep(2)
                if self.wait_for_element_exist(By.XPATH, device_icon_on_dashboard):
                    if deviceName.upper() in self.driver.find_element(By.XPATH, device_icon_on_dashboard).get_attribute(
                            'text').upper():
                        # self.driver.find_element(By.XPATH, device_icon_on_dashboard).click()
                        self.report_pass(deviceName + ' is found and clicked')
                    else:
                        self.report_fail(deviceName + ' and Locators are not matched')
                else:

                    self.dashboardSwipe(False)
                    if self.wait_for_element_exist(By.XPATH, device_icon_on_dashboard):
                        if deviceName.upper() in self.driver.find_element(By.XPATH,
                                                                          device_icon_on_dashboard).get_attribute(
                            'text').upper():
                            self.driver.find_element(By.XPATH, device_icon_on_dashboard).click()
                            self.report_pass(deviceName + ' is found and clicked')
                        else:
                            self.report_fail(deviceName + ' and Locators are not matched')
                    else:
                        self.report_fail(deviceName + ' is not found')

            else:
                self.report_fail('User is not inside the app')


# class for checking menu options..
class MainMenuPage(BasePage):
    # clicks the menu option
    def click_menuicon(self):

        if not 'LOG IN' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_SHOW):
                self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                self.report_done('Menu Button Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('Menu Button Icon is not present.')
        else:
            self.report_fail('Android-App: The Hive Android App is Logged out')

            # to verify all the menu options in the app.

    def verify_main_menu(self):

        try:
            if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
                if self.wait_for_element_exist(*MainMenuLocators.MYHIVEHOME_MAIN_MENU):
                    self.report_pass('MyHiveHome option is present')
                else:
                    self.report_fail('MyHiveHome option is not present')
                if self.wait_for_element_exist(*MainMenuLocators.MANAGEDEVICES_MAIN_MENU):
                    self.report_pass('ManageDevices option is present')
                else:
                    self.report_fail('ManageDevices option is not present')
                if self.wait_for_element_exist(*MainMenuLocators.INSTALLDEVICES_MAIN_MENU):
                    self.report_pass('InstallDevices option is present')
                else:
                    self.report_fail('InstallDevices option is not present')
                if self.wait_for_element_exist(*MainMenuLocators.ACTIONS_MAIN_MENU):
                    self.report_pass('AllRecipes option is present')
                else:
                    self.report_fail('AllRecipes option is not present')
                if self.wait_for_element_exist(*MainMenuLocators.SETTINGS_MAIN_MENU):
                    self.report_pass('Settings option is present')
                else:
                    self.report_fail('Settings option is not present')
                if self.wait_for_element_exist(*MainMenuLocators.HELP_MAIN_MENU):
                    self.report_pass('Help & Support option is present')
                else:
                    self.report_fail('Help & Support option is not present')
                if self.wait_for_element_exist(*MainMenuLocators.LOGOUT_MAIN_MENU):
                    self.report_pass('Logout option is present')
                else:
                    self.report_fail('Logout option is not present')
            else:
                self.report_fail('Android-App: The Hive Android App is not in Home page.')
        except:

            self.report_fail('Android-App: Exception in verify_main_menu Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

            # to click the managedevice option

    def click_managedeviceicon(self):
        if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.MANAGEDEVICES_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.MANAGEDEVICES_MAIN_MENU).click()
                self.report_done('Manage Devices Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('Managedevice option is not found')
        else:
            self.report_fail('Android-App: The Hive Android App is not on Menu Page.')

            # to verify the managedevice screen

    def click_verify_managedevicescreen(self):
        if 'MANAGE DEVICES' in self.driver.find_element(*MainMenuLocators.MANAGEDEVICE_TITLE).get_attribute(
                'name').upper():
            self.report_pass('App is navigated to Managedevice Screen')
        else:
            self.report_fail('Android-App: The Hive Android App is not on manage device screen')

    # to click the install devices screen
    def click_installdevice(self):
        if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.INSTALLDEVICES_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.INSTALLDEVICES_MAIN_MENU).click()
                self.report_done('Install devices Icon is clicked')
                time.sleep(5)

            else:
                self.report_fail('Install option is not found')
        else:
            self.report_fail('Android-App: The Hive Android App is not on Menu Page.')

            # to verify the install device navigation

    def click_verify_installdevicescreen(self):
        if 'INSTALL DEVICES' in self.driver.find_element(*MainMenuLocators.INSTALLDEVICE_TITLE).get_attribute(
                'name').upper():
            self.report_pass('App is navigated to Installdevice Screen')
        else:
            self.report_fail('Android-App: The Hive Android App is not on install device screen')

            # to verify the install options..

    def click_verifyoptions_installdevicescreen(self):
        if 'INSTALL DEVICES' in self.driver.find_element(*MainMenuLocators.INSTALLDEVICE_TITLE).get_attribute(
                'name').upper():
            nodes = Putils.getNodes()
            presenthub = ''
            for oNode in nodes['nodes']:
                if oNode['name'].upper() == 'HUB':
                    if oNode["attributes"]["hardwareVersion"]["reportedValue"] == 'NANO2':
                        presenthub = 'NANO2'
                    elif oNode["attributes"]["hardwareVersion"]["reportedValue"] == 'NANO1':
                        presenthub = 'NANO1'
            print(presenthub)
            if presenthub == 'NANO2':
                if self.wait_for_element_exist(*MainMenuLocators.ADDZONE_INSTALLDEVICE):
                    self.report_pass('Add zone option is present')
                else:
                    self.report_fail('Add zone option is not present')
            elif presenthub == 'NANO1':
                self.report_pass('Add zone option is not available for NANO1 HUB')

            else:
                self.report_fail('Error in checking add heating zone option')

            if self.wait_for_element_exist(*MainMenuLocators.UPGRADE_INSTALLDEVICE):
                self.report_pass('Upgrade to Hive 2 option is present')
            else:
                self.report_fail('Upgrade to Hive 2 option is not present.')
            if self.wait_for_element_exist(*MainMenuLocators.ADDANOTHERDEVICE_INSTALLDEVICE):
                self.report_pass('Add another Device option is present')
            else:
                self.report_fail('Add another Device option is not present.')
        else:
            self.report_fail('Android-App: The Hive Android App is not on install device screen')

            # to click all recepies

    def click_allrecipes(self):
        if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.ACTIONS_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.ACTIONS_MAIN_MENU).click()
                self.report_done('All Recipes Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('All Recipes Icon is not found')

        else:
            self.report_fail('Android-App: The Hive Android App is not on Menu Page.')

    def verify_allrecepiescreen(self):
        if 'ALL RECIPES' in self.driver.find_element(*MainMenuLocators.ACTIONS_TITLE).get_attribute('name').upper():
            self.report_pass('App is navigated to All Recipes Screen')
        else:
            self.report_fail('Android-App: The Hive Android App is not on all recipes screen')

    def click_settings(self):
        if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.SETTINGS_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.SETTINGS_MAIN_MENU).click()
                self.report_done('Setting Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('Setting Icon is not found')
        else:
            self.report_fail('Android-App: The Hive Android App is not on Menu Page.')

    def verify_settingsoptions(self):
        if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            self.driver.swipe(199.4, 996.2, 202.2, 422.9, 2000)
            time.sleep(2)
            if self.wait_for_element_exist(*MainMenuLocators.GEOLOCATION_SETTINGS):
                self.report_pass('Geolocation is present')
            else:
                self.report_fail('Geolocation is not present')
            if self.wait_for_element_exist(*MainMenuLocators.HOLIDAYMODE_SETTINGS):
                self.report_pass('Holidaymode is present')
            else:
                self.report_fail('Holidaymode is not present')

            if self.wait_for_element_exist(*MainMenuLocators.HEATINGNOTIFICATIONS_SETTINGS):
                self.report_pass('Heating notifications is present')
            else:
                self.report_fail('Heating notifications is not present')

            if self.wait_for_element_exist(*MainMenuLocators.ACCOUNTDETAILS_SETTINGS):
                self.report_pass('Accountdetails is present')
            else:
                self.report_fail('Accountdetails is not present')

            if self.wait_for_element_exist(*MainMenuLocators.PINLOCK_SETTINGS):
                self.report_pass('Pinlock is present')
            else:
                self.report_fail('Pinlock is not present')

            if self.wait_for_element_exist(*MainMenuLocators.CHANGEPASSWORD_SETTINGS):
                self.report_pass('Changepassword is present')
            else:
                self.report_fail('Changepassword is not present')
        else:
            self.report_fail('Android-App: The Hive Android App is not on Menu Page.')

    def click_help(self):
        if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.HELP_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.HELP_MAIN_MENU).click()
                self.report_done('Help Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('Help Icon is not found')
        else:
            self.report_fail('Android-App: The Hive Android App is not on Menu Page.')

    def verify_helpoptions(self):
        if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            self.driver.swipe(316.8, 1389.5, 318.2, 656, 2000)
            time.sleep(2)
            if self.wait_for_element_exist(*MainMenuLocators.FAQ_HELP):
                self.report_pass('FAQs is present')
            else:
                self.report_fail('FAQs is not present.')
            if self.wait_for_element_exist(*MainMenuLocators.HELPIMPROVEHIVE_HELP):
                self.report_pass('Help improve Hive icon is present')
            else:
                self.report_fail('Help improve Hive icon is not present.')

            if self.wait_for_element_exist(*MainMenuLocators.SERVICESTATUS_HELP):
                self.report_pass('Service Status icon is present')
            else:
                self.report_fail('Service status icon is not present.')

            nodes = Putils.getNodes()
            count = 0
            for oNode in nodes['nodes']:
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.thermostatui.json#':
                    count += 1
            print(count)
            if count == 1:
                if self.wait_for_element_exist(*MainMenuLocators.TEXTCONTROL_HELP):
                    self.report_pass('TextControl option is present')
                else:
                    self.report_fail('TextControl option is not present')
            else:
                self.report_pass('TextControl Option is not available for PMZ')
        else:
            self.report_fail('Android-App: The Hive Android App is not on Menu Page.')

    def click_logout(self):
        if 'HOME' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*LogoutLocators.LOGOUT_OPTION):
                self.driver.find_element(*LogoutLocators.LOGOUT_OPTION).click()
                self.report_done('Logout Icon is clicked')
            time.sleep(5)
        else:
            self.report_fail('Android-App: The Hive Android App is not on Menu Page.')

    def verify_logout(self):
        if 'LOG IN' in self.driver.find_element(*MainMenuLocators.LOGINPAGE_TITLE).get_attribute('name').upper():
            self.report_pass('Android-App: The Hive Android App is successfully Logged out')
        else:
            self.report_fail('Android-App: The Hive Android App is not logged out.')


# Page Class for Heating Home page. Has all the methods for the Heating Home page
class HeatingHomePage(BasePage):
    # Navigates to the Heating Control Page
    def navigate_to_heating_control_page(self, boolStopBoost=True):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingHomePageLocators.HEAT_CONTROL_TAB):
                    self.driver.find_element(*HeatingHomePageLocators.HEAT_CONTROL_TAB).click()
                    if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):
                        self.report_pass('Android-App : Successfully navigated to the Heating Control Page')
                    else:
                        if not boolStopBoost:
                            self.report_pass('Android-App: Successfully navigated to the Heating Control Page -')
                            return True
                        if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_STOP_BUTTON):
                            self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP_BUTTON).click()
                            time.sleep(3)
                        if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):
                            self.report_pass('Android-App : Successfully navigated to the Heating Control Page')
                        else:
                            self.report_fail('Android App : Unable to navigate to Heating Control Page')
                else:
                    self.report_fail(
                        "Android-App : Control not active on the Heating Home Page to Navigate to Heating Control Page")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_heating_control_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Navigates to the Hot water Home Page
    def navigate_to_heating_schedule_page(self):
        if self.reporter.ActionStatus:
            try:
                if self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        'HEATING') >= 0:
                    time.sleep(5)
                    if self.wait_for_element_exist(*HeatingHomePageLocators.HEAT_SCHEDULE_TAB):
                        self.driver.find_element(*HeatingHomePageLocators.HEAT_SCHEDULE_TAB).click()
                        self.report_done('The Heating Schedule tab is clicked')
                    else:
                        self.report_fail('Unable to find the Heating Schedule tab')

                    if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL):
                        self.report_pass('Successfully navigated to the Heating Schedule Page')
                    else:
                        self.report_fail('Unable to navigate to Heating Schedule Page')
                else:
                    self.report_fail(
                        "Control not active on the Heating Home Page to Navigate to Heating Schedule Page")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_heating_schedule_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


# Page Class for Hot Water Home page. Has all the methods for the Hot Water Home page
class HotWaterHomePage(BasePage):
    # Navigates to the Hot Water Control Page
    def navigate_to_hot_water_control_page(self, boolStopBoost=True):
        if self.reporter.ActionStatus:
            try:

                if self.wait_for_element_exist(*HotWaterHomePageLocators.TITLE_LABEL):
                    self.driver.find_element(*HotWaterHomePageLocators.HOT_WATER_CONTROL_TAB).click()

                    if not boolStopBoost:
                        self.report_pass('Successfully navigated to the Hot Water Control Page -')
                        return True
                    if self.is_element_present(*HotWaterControlPageLocators.MANUAL_MODE_LINK):
                        self.report_pass('Successfully navigated to the Hot Water Control Page')

                    elif self.wait_for_element_exist(*HotWaterControlPageLocators.OFF_MODE_LINK):
                        self.report_pass('Successfully navigated to the Hot Water Control Page')
                    else:
                        if not boolStopBoost:
                            self.report_pass('Android-App: Successfully navigated to the Hot Water Control Page -')
                            return True
                        if self.wait_for_element_exist_for_given_time(*HotWaterControlPageLocators.BOOST_STOP_BUTTON):
                            self.driver.find_element(*HotWaterControlPageLocators.BOOST_STOP_BUTTON).click()
                            time.sleep(3)
                        if self.wait_for_element_exist(*HotWaterControlPageLocators.OFF_MODE_LINK):
                            self.report_pass('Successfully navigated to the Hot Water Control Page')
                        else:
                            self.report_fail('Android App : Unable to navigate to Hot Water Control Page')

                elif self.wait_for_element_exist(*HotWaterHomePageLocators.TITLE_LABEL_BOOST):
                    self.driver.find_element(*HotWaterHomePageLocators.HOT_WATER_CONTROL_TAB).click()

                    if not boolStopBoost:
                        self.report_pass('Successfully navigated to the Hot Water Control Page -')
                        return True
                    if self.wait_for_element_exist_for_given_time(*HotWaterControlPageLocators.BOOST_STOP_BUTTON):
                        self.driver.find_element(*HotWaterControlPageLocators.BOOST_STOP_BUTTON).click()
                        time.sleep(3)
                    else:
                        self.report_fail('Android App : Unable to navigate to Hot Water Control Page')

                else:
                    self.report_fail(
                        "Android-App : Control not active on the Hot Water Home Page to Navigate to Hot Water Control Page")
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_hot_water_control_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Navigates to the Hot water Home Page
    def navigate_to_hot_water_schedule_page(self):
        if self.reporter.ActionStatus:
            try:
                if self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        'HOT WATER') >= 0:
                    time.sleep(5)
                    if self.wait_for_element_exist(*HotWaterHomePageLocators.HOT_WATER_SCHEDULE_TAB):
                        self.driver.find_element(*HotWaterHomePageLocators.HOT_WATER_SCHEDULE_TAB).click()
                        self.report_done('The hot water Schedule tab is clicked')
                    else:
                        self.report_fail('Unable to find the hot water Schedule tab')

                    if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL):
                        self.report_pass('Successfully navigated to the Hot Water Schedule Page')
                    else:
                        self.report_fail('Unable to navigate to Hot Water Schedule Page')
                else:
                    self.report_fail(
                        "Control not active on the Hot Water Home Page to Navigate to Hot Water Schedule Page")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_hot_water_schedule_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


# Page Class for Heating Control page. Has all the methods for the Heating Control page
class HeatingControlPage(BasePage):
    # Set Heat mode
    def set_heat_mode(self, strMode, intTemperature=None, intDuration=1):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    if strMode.upper() == 'AUTO':
                        if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_STOP_BUTTON):
                            self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP_BUTTON).click()
                            time.sleep(2)
                        self.driver.find_element(*HeatingControlPageLocators.SCHEDULE_MODE_LINK).click()
                    elif strMode.upper() == 'MANUAL':
                        if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_STOP_BUTTON):
                            self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP_BUTTON).click()
                            time.sleep(2)
                        self.driver.find_element(*HeatingControlPageLocators.MANUAL_MODE_LINK).click()
                    elif 'OFF' in strMode.upper():
                        if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_STOP_BUTTON):
                            self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP_BUTTON).click()
                            time.sleep(2)
                        if self.wait_for_element_exist(*self.OFF_MODE_LINK):
                            self.driver.find_element(*self.OFF_MODE_LINK).click()
                    elif strMode.upper() == 'BOOST':
                        if self.is_element_present(*HeatingControlPageLocators.BOOST_STOP_BUTTON):
                            self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP_BUTTON).click()
                            time.sleep(2)
                        if self.wait_for_element_exist(*self.CH_BOOST_MODE_LINK):
                            self.driver.find_element(*self.CH_BOOST_MODE_LINK).click()
                            time.sleep(2)
                            # Set Boost Duration
                        if intDuration != 1:
                            intHour = int(
                                self.driver.find_element(*HeatingControlPageLocators.BOOST_CURRENT_HOUR).text.split(
                                    ':')[0])
                            intMinute = int(self.driver.find_element(
                                *HeatingControlPageLocators.BOOST_CURRENT_MINUTE).text.split(':')[0])
                            intCurrentDuration = utils.round_up((intHour * 60 + intMinute) / 60)
                            print('intCurrentDuration', intCurrentDuration)
                            print('intDuration', intDuration)
                            intCntrIter = 0
                            while (intCurrentDuration != intDuration) and (intCntrIter < 3):
                                time.sleep(2)
                                self.set_boost_time_duration(intDuration)
                                intHour = int(self.driver.find_element(
                                    *HeatingControlPageLocators.BOOST_CURRENT_HOUR).text.split(':')[0])
                                intMinute = int(self.driver.find_element(
                                    *HeatingControlPageLocators.BOOST_CURRENT_MINUTE).text.split(':')[0])
                                intCurrentDuration = utils.round_up((intHour * 60 + intMinute) / 60)
                                intCntrIter += 1
                        # Set Boost Target temperature
                        if intTemperature is not None:
                            oScrolElement = self.driver.find_element(*HeatingControlPageLocators.BOOST_TEMP_SCROLL)
                            strContent = oScrolElement.get_attribute('name')
                            fltCurrentTemp = float(self.get_TempFromElement(strContent))
                            intCntrIter = 1
                            while (fltCurrentTemp != intTemperature) and (intCntrIter < 3):
                                self.scroll_element_to_value(oScrolElement, fltCurrentTemp, intTemperature, 0.5,
                                                             2)
                                time.sleep(5)
                                oScrolElement = self.driver.find_element(*HeatingControlPageLocators.BOOST_TEMP_SCROLL)
                                strContent = oScrolElement.get_attribute('name')
                                fltCurrentTemp = float(self.get_TempFromElement(strContent))

                                intCntrIter = intCntrIter + 1

                    self.report_pass('Screenshot after the mode is updated')
                    time.sleep(10)
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                        self.report_pass('Android-App : Successfully Heat mode is set to <B>' + strMode)
                    else:
                        self.report_fail('Android App : Unable to set Heat mode to <B>' + strMode)
                else:
                    self.report_fail(
                        "Android-App : Control not active on the Heating Control Page to set the Heat Mode")

            except:
                self.report_fail('Android App : NoSuchElementException: in set_heat_mode Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set Target Temperature
    def set_target_temperature(self, fltTargetTemperature):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    self.driver.find_element(*HeatingControlPageLocators.PRESET_TEMP_BUTTON).click()
                    time.sleep(2)
                    oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                    strContent = oScrolElement.get_attribute('name')
                    fltCurrentTargTemp = float(self.get_TempFromElement(strContent))
                    intCntrIter = 1
                    if fltTargetTemperature == 1.0: fltTargetTemperature = 7.0
                    self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltTargetTemperature, 0.5, 2)
                    time.sleep(5)
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)

                else:
                    self.report_fail(
                        "Android-App : Control not active on the Heating Control Page to set the Target Temperature")

            except:
                self.report_fail('Android App : NoSuchElementException: in set_target_temperature Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Get Attributes for Heating Controls
    def get_heating_attribute(self, strBeforeHeatingMode):
        if self.reporter.ActionStatus:
            try:
                fltCurrentTargTemp = 0.0
                strRunningState = 'OFF'
                strMode = ""
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(3)
                if self.wait_for_element_exist(*HeatingHomePageLocators.HEAT_CONTROL_TAB):
                    print("==================first===if========\n")
                    self.driver.find_element(*HeatingHomePageLocators.HEAT_CONTROL_TAB).click()
                    time.sleep(5)
                    if self.wait_for_element_exist(*HeatingControlPageLocators.SELECTED_MODE_LINK):
                        print("=====================if========\n")
                        strMode = self.driver.find_element(*HeatingControlPageLocators.SELECTED_MODE_LINK).text.upper()
                        print(strMode, 'strMode')
                        if 'SCHEDULE' in strMode:
                            if strBeforeHeatingMode:
                                if 'AUTO' in strBeforeHeatingMode:
                                    strMode = 'OVERRIDE'
                                else:
                                    strMode = 'AUTO'
                            else:
                                strMode = 'AUTO'
                        if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_FLAME_ICON):
                            strHeatingState = self.driver.find_element(
                                *HeatingControlPageLocators.BOOST_FLAME_ICON).text.upper()
                            if strHeatingState == 'NOW\nHEATING':
                                strRunningState = 'ON'
                    else:
                        strMode = 'BOOST'
                        print("===========else==================\n")
                        if self.wait_for_element_exist(
                                *HeatingControlPageLocators.BOOST_FLAME_ICON):
                            strHeatingState = self.driver.find_element(
                                *HeatingControlPageLocators.BOOST_FLAME_ICON).text.upper()
                            if strHeatingState == 'NOW\nHEATING':
                                strRunningState = 'ON'
                    oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                    strContent = oScrolElement.get_attribute('name')
                    fltCurrentTargTemp = float(self.get_TempFromElement(strContent))
                else:
                    print("=====ifelse========================\n")
                    self.report_fail(
                        "Android-App : Control not active on the Heating Control Page to set the Target Temperature")

                self.report_done('Android App : Screenshot while getting attributes')
                if strRunningState == 'OFF':
                    strRunningState = '0000'
                else:
                    strRunningState = '0001'
                if fltCurrentTargTemp == 7.0: fltCurrentTargTemp = 1.0
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                print("=========exception====================\n")
                self.report_fail('Android App : NoSuchElementException: in get_heating_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Class for comman scheuling page
class SchedulePage(BasePage):
    COPYSCHEDAY = "csi_"
    COPYSCHEDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    SCHEDULEDAY = "_single_weekday"
    SCHEDULEDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    SCHEDULEICONSTATUSTEXT = ["o", "p"]
    SCHEDULETEXTSTATUSTEXT = ["off", "on"]

    # for reseting the schedule
    def reset_schedule(self, oSchedule):
        if self.reporter.ActionStatus:
            try:
                for oKey in oSchedule.keys():
                    self._navigate_to_day(oKey)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    self.reporter.HTML_TC_BusFlowKeyword_Initialize('Reset Schedule')
                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        time.sleep(2)
                        self.report_done("Add Icon is found and clicked sucessfully")
                    else:
                        self.report_fail("Add Icon is not found on schedule screen, Exit condition")
                        exit()
                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU).click()
                        time.sleep(2)
                        self.report_done("Reset Icon is found and clicked sucessfully")
                    else:
                        self.report_fail("Reset Icon is not found on schedule screen, Exit condition")
                        exit()
                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON).click()
                        time.sleep(2)
                        self.report_done("Reset OK Button is found and clicked sucessfully")
                    else:
                        self.report_fail("Reset OK Button is not found on schedule screen, Exit condition")
                        exit()
            except:
                self.report_fail('Android-App : NoSuchElementException: in reset_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # for copying a schedule
    def copy_schedule(self, strToDay, strFromDay):
        if self.reporter.ActionStatus:
            try:
                self._navigate_to_day(strFromDay)

                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                    time.sleep(2)
                    self.report_done("Add Icon is found and clicked sucessfully")
                else:
                    self.report_fail("Add Icon is not found on schedule screen, Exit condition")
                    exit()
                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_COPYSCHE_TEXTVIEW):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_COPYSCHE_TEXTVIEW).click()
                    time.sleep(2)
                    self.report_done("Copy schedule Icon is found and clicked sucessfully")
                else:
                    self.report_fail("Copy schedule is not found on schedule screen, Exit condition")
                    exit()

                listCopyScheProperty = list(SchedulePageLocators.SCHEDULE_COPYSCHEDAY_LAYOUT)
                listCOPYSCHEDAYS = self.SCHEDULEDAYS
                intIndex = listCOPYSCHEDAYS.index(strToDay.lower())
                strCopyScheProperty = self.COPYSCHEDAY + self.COPYSCHEDAYS[intIndex]
                listCopyScheProperty[1] = listCopyScheProperty[1].replace("COPYSCHEDAY", strCopyScheProperty)
                listCopySchePropertytuple = tuple(listCopyScheProperty)

                if self.wait_for_element_exist(*listCopySchePropertytuple):
                    self.driver.find_element(*listCopySchePropertytuple).click()
                    time.sleep(2)
                    self.report_done("The given day is found and clicked sucessfully")
                else:
                    self.report_fail(
                        "the given day, " + strToDay + " is not found on schedule screen, Exit condition")
                    exit()

                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON).click()
                    time.sleep(2)
                    self.report_done("Save OK Button is found and clicked sucessfully")
                else:
                    self.report_fail("Save OK Button is not found on schedule screen, Exit condition")
                    exit()
            except:
                self.report_fail('Android-App : NoSuchElementException: in copySchedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # for Adding a schedule
    def add_schedule(self, context, strType):
        strSetStartTime = context.addSlotTime
        strTarget = context.addSlotState
        if self.reporter.ActionStatus:

            try:
                self._navigate_to_day(context.strDay)
                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                    time.sleep(2)
                    self.report_done("Add Icon is found and clicked sucessfully")
                else:
                    self.report_fail("Add Icon is not found on schedule screen, Exit condition")
                    exit()
                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_ADDTIMESLOT_TEXTVIEW):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_ADDTIMESLOT_TEXTVIEW).click()
                    time.sleep(2)
                    self.report_done("Add schedule Icon is found and clicked sucessfully")
                    self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                    self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                    strLog = ""
                    if strType == 'HEAT':
                        if strTarget == "1.0": strTarget = "7.0"
                        self.set_schedule_target_temperature(float(strTarget))
                        strLog = "Slot Start Time $$ Temparature@@@" + \
                                 strSetStartTime + "$$" + strTarget
                    elif strType == 'PLUG' or strType == 'WATER':
                        strLog = "Slot Start Time $$ State@@@" + \
                                 strSetStartTime + "$$" + strTarget
                        if self.wait_for_element_exist(*EditTimeSlotPageLocators.TOGGLE_BUTTON):
                            if self.driver.find_element(
                                    *EditTimeSlotPageLocators.TOGGLE_BUTTON).get_attribute(
                                'name').find(
                                'ON') >= 0:
                                strCurrentState = 'ON'
                            else:
                                strCurrentState = 'OFF'

                            if strTarget != strCurrentState:
                                self.driver.find_element(
                                    *EditTimeSlotPageLocators.TOGGLE_BUTTON).click()

                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Below Time Slot is added')
                    self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                else:
                    self.report_fail("Add schedule is not found on schedule screen, Exit condition")
                    exit()

                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON).click()
                    time.sleep(3)
                    self.report_done("Save OK Button is found and clicked sucessfully")
                if self.wait_for_element_exist(*HomePageLocators.REFRESH_BUTTON_V6):
                    self.driver.find_element(*HomePageLocators.REFRESH_BUTTON_V6).click()
                    time.sleep(3)
                elif self.wait_for_element_exist(*EditTimeSlotPageLocators.CANCEL_BUTTON):
                    self.driver.find_element(*EditTimeSlotPageLocators.CANCEL_BUTTON).click()
                    time.sleep(2)
                    self.report_fail("refresh button is not found, existing the scenario")
                else:
                    self.report_fail("Save OK Button is not found on schedule screen, Exit condition")
                    exit()
            except:
                self.report_fail('Android-App : NoSuchElementException: in addSchedules Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # for deleting schedules
    def delete_schedule(self, context):
        if self.reporter.ActionStatus:
            try:
                if context.intEvent > 0:
                    self._navigate_to_day(context.strDay)
                    self.reporter.HTML_TC_BusFlowKeyword_Initialize('Deleting existing time slot')
                    strProperty = list(SchedulePageLocators.SCHEDULE_TIMESLOTOPTION_ICON)
                    strProperty[1] = strProperty[1].replace("INDEX", str(context.intEvent))
                    strPropertyTuple = tuple(strProperty)

                    if self.wait_for_element_exist(*strPropertyTuple):
                        self.driver.find_element(*strPropertyTuple).click()
                        time.sleep(2)
                        if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_DELETETIMESLOT_ICON):
                            self.driver.find_element(*SchedulePageLocators.SCHEDULE_DELETETIMESLOT_ICON).click()
                            time.sleep(4)
                            if self.is_element_present(*SchedulePageLocators.SCHEDULE_YES_BUTTON):
                                self.driver.find_element(*SchedulePageLocators.SCHEDULE_YES_BUTTON).click()

                            self.report_pass("Below Time slot has been deleted")
                            strLog = "Event Number $$Event Time @@@" + str(
                                context.intEvent) + "$$" + context.addSlotTime
                            self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                            time.sleep(2)
                        else:
                            self.report_fail("Delete option is not found at time slot option menu")

                    else:
                        self.report_fail("Time schedule is not found for the given day, Exit condition")
                        exit()

            except:
                self.report_fail(
                    'Android-App : NoSuchElementException: in deleteSchedules Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


# Page Class for Heating Schedule page. Has all the methods for the Heating Schedule page
class HeatingSchedulePage(BasePage):
    # Set Heating Schedule
    def set_heating_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                blnFlagFormat = False
                if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL) and self.wait_for_element_exist(
                        *self.REFRESH_BUTTON):

                    lstAMelements = self.driver.find_elements(*EditTimeSlotPageLocators.EDIT_TIMESLOT_AM_FORMAT)
                    if len(lstAMelements) > 0: blnFlagFormat = True

                    for oKey in oScheduleDict.keys():
                        print('m here')
                        print(oKey)
                        self._navigate_to_day(oKey)
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        # Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                        intCurrentEventCount = len(lstStartTime)
                        if self.reporter.platformVersion == 'V6':
                            self.add_or_remove_events(len(oScheduleList))
                        else:
                            if len(oScheduleList) > 4:
                                if not intCurrentEventCount == 6:
                                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()
                                    self.driver.find_element(*SchedulePageLocators.SIX_EVENT_SUBMENU).click()
                            else:
                                if not intCurrentEventCount == 4:
                                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()
                                    self.driver.find_element(*SchedulePageLocators.FOUR_EVENT_SUBMENU).click()

                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                        for intCntr in range((len(lstStartTime) - 1), -1, -1):
                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetTargTemp = oScheduleList[intCntr][1]
                            if fltSetTargTemp == 1.0: fltSetTargTemp = 7.0
                            intCntrIter = 0
                            strCurrentStartTIme = ''
                            if blnFlagFormat:
                                strSetToTime = ('0' + str(int(strSetStartTime.split(':')[0]) % 12))[-2:] + ":" + \
                                               strSetStartTime.split(':')[1]
                            else:
                                strSetToTime = strSetStartTime

                            while (strCurrentStartTIme != strSetToTime) and (intCntrIter < 3):
                                time.sleep(3)
                                lstStartTime[intCntr].click()

                                time.sleep(3)
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.HOUR_SCROLL):
                                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                                    strCurrentHour = oScrolElement.find_element(
                                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                        'name')
                                    strCurrentHour = ('0' + strCurrentHour)[-2:]
                                else:
                                    self.report_fail('Element HOUR_SCROLL is not found')
                                    exit()
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                                    strCurrentMinute = oScrolElement.find_element(
                                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                        'name')
                                else:
                                    self.report_fail('Element MINUTE_SCROLL is not found')
                                    exit()
                                strCurrentTime = strCurrentHour + ':' + strCurrentMinute
                                self.set_schedule_target_temperature(fltSetTargTemp)
                                self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                                self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                                strLog = "Event Number $$Before Change$$After Change $$ Updated Temparature@@@" + \
                                         str(
                                             intCntr + 1) + "$$" + strCurrentTime + "$$" + strSetStartTime + "$$" + str(
                                    fltSetTargTemp)
                                self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                                intCntrIter = intCntrIter + 1
                                time.sleep(5)
                                self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                                time.sleep(5)
                                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                                    time.sleep(7)
                                    self.report_pass("Refresh button is found and clicked")
                                elif self.wait_for_element_exist(*EditTimeSlotPageLocators.CANCEL_BUTTON):
                                    self.driver.find_element(*EditTimeSlotPageLocators.CANCEL_BUTTON).click()
                                    time.sleep(2)
                                    self.report_fail("Refresh button is not found, existing the scenario")
                                    break
                                self.wait_for_element_exist(*self.REFRESH_BUTTON)
                                strCurrentStartTIme = lstStartTime[intCntr].get_attribute('text')
                            self.report_pass(
                                'Main Screen after Event number : ' + str(intCntr + 1) + ' is changed')
                        self.report_pass('Main Screen after all Events are changed')
                else:
                    self.report_fail(
                        "Android-App : Control not active on the Heating Schedule Page to set the Heating Schedule")

            except:
                self.report_fail('Android App : NoSuchElementException: in set_heating_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Page Class for Hot Water Control page. Has all the methods for the Hot Water Control page
class HotWaterControlPage(BasePage):
    # Set Heat mode
    def set_hot_water_mode(self, strMode, intDuration=1):
        if self.reporter.ActionStatus:
            try:
                time.sleep(5)
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    if strMode.upper() == 'AUTO':
                        self.driver.find_element(*HotWaterControlPageLocators.SCHEDULE_MODE_LINK).click()
                    elif 'ON' in strMode.upper() or 'MANUAL' in strMode.upper() or 'OFF' in strMode.upper():
                        if not self.driver.find_element(
                                *HotWaterControlPageLocators.HOTWATER_STATUS_V6).text.upper() == strMode.upper():
                            self.driver.find_element(*HotWaterControlPageLocators.HOTWATER_STATUS_V6).click()
                    elif strMode.upper() == 'BOOST':
                        self.driver.find_element(*self.HW_BOOST_MODE_LINK).click()
                        print('intDuration', intDuration)
                        if self.currentAppVersion == 'V6':
                            # Set Boost Duration
                            if intDuration != 1:
                                intHour = int(self.driver.find_element(
                                    *HotWaterControlPageLocators.BOOST_CURRENT_HOUR).text.split(':')[0])
                                intMinute = int(self.driver.find_element(
                                    *HotWaterControlPageLocators.BOOST_CURRENT_MINUTE).text.split(':')[0])
                                intCurrentDuration = utils.round_up((intHour * 60 + intMinute) / 60)
                                print('intCurrentDuration', intCurrentDuration)
                                print('intDuration', intDuration)
                                intCntrIter = 0
                                while (intCurrentDuration != intDuration) and (intCntrIter < 3):
                                    time.sleep(2)
                                    self.set_boost_time_duration(intDuration)
                                    intHour = int(self.driver.find_element(
                                        *HotWaterControlPageLocators.BOOST_CURRENT_HOUR).text.split(':')[0])
                                    intMinute = int(self.driver.find_element(
                                        *HotWaterControlPageLocators.BOOST_CURRENT_MINUTE).text.split(':')[0])
                                    intCurrentDuration = utils.round_up((intHour * 60 + intMinute) / 60)
                                    intCntrIter += 1

                    time.sleep(5)
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                        self.report_pass('Successfully Hot Water mode is set to <B>' + strMode)
                    else:
                        self.report_fail('Android App : Unable to set Hot Water mode to <B>' + strMode)
                else:
                    self.report_fail(
                        "Android-App : Control not active on the Hot Water Control Page to set the Hot Water Mode")

            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_mode Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Get Attributes for HotWater Controls
    def get_hotwater_attribute(self):
        if self.reporter.ActionStatus:
            fltCurrentTargTemp = 0.0
            strRunningState = 'OFF'
            strMode = ""
            currentRunningState = ""
            try:
                if self.wait_for_element_exist(*self.RUNNING_STATE_CIRCLE):
                    self.refresh_page()
                    if self.wait_for_element_exist(*HotWaterControlPageLocators.SELECTED_MODE_LINK):
                        strMode = self.driver.find_element(*HotWaterControlPageLocators.SELECTED_MODE_LINK).text.upper()
                        currentRunningState = self.driver.find_element(
                            *HotWaterControlPageLocators.HOTWATER_STATUS).text.upper()
                        if 'SCHEDULE' in strMode:
                            strMode = 'AUTO'
                        if "ON" in currentRunningState:
                            strRunningState = 'ON'
                        if "OFF" in currentRunningState:
                            strMode = 'OFF'
                    else:
                        strMode = 'BOOST'
                        if self.driver.find_element(*HotWaterControlPageLocators.BOOST_ACTIVE).get_attribute(
                                'text').upper().find('ON') >= 0:
                            strRunningState = 'ON'

                else:
                    self.report_fail(
                        "Android-App : Control not active on the Hot Water Control Page to get Heating Attributes")

                self.report_done('Android App : Screenshot while getting attributes')
                if strRunningState == 'OFF':
                    strRunningState = '0000'
                else:
                    strRunningState = '0001'
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('Android App : NoSuchElementException: in get_hotwater_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

                # Page Class for Hot Water Schedule page. Has all the methods for the Hot Water Schedule page


class HotWaterSchedulePage(BasePage):
    def set_hot_water_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                blnFlagFormat = False
                lstAMelements = self.driver.find_elements(*EditTimeSlotPageLocators.EDIT_TIMESLOT_AM_FORMAT)
                if len(lstAMelements) > 0: blnFlagFormat = True
                if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL) and self.wait_for_element_exist(
                        *self.REFRESH_BUTTON):
                    if self.wait_for_element_exist(*EditTimeSlotPageLocators.FORMAT_SCROLL):
                        blnFlagFormat = True
                    for oKey in oScheduleDict.keys():
                        print('m here')
                        print(oKey)
                        self._navigate_to_day(oKey)
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        # Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                        intCurrentEventCount = len(lstStartTime)
                        if self.reporter.platformVersion == 'V6':
                            self.add_or_remove_events(len(oScheduleList))
                        else:
                            if len(oScheduleList) > 4:
                                if not intCurrentEventCount == 6:
                                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()
                                    self.driver.find_element(*SchedulePageLocators.SIX_EVENT_SUBMENU).click()
                            else:
                                if not intCurrentEventCount == 4:
                                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()
                                    self.driver.find_element(*SchedulePageLocators.FOUR_EVENT_SUBMENU).click()

                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                        for intCntr in range((len(lstStartTime) - 1), -1, -1):
                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetTargTemp = oScheduleList[intCntr][1]
                            if fltSetTargTemp == 1.0: fltSetTargTemp = 7.0
                            intCntrIter = 0
                            strCurrentStartTIme = ''
                            if blnFlagFormat:
                                strSetToTime = str(int(strSetStartTime.split(':')[0]) % 12) + ":" + \
                                               strSetStartTime.split(':')[1]
                            else:
                                strSetToTime = strSetStartTime
                            while (strCurrentStartTIme != strSetToTime) and (intCntrIter < 3):
                                time.sleep(3)
                                lstStartTime[intCntr].click()
                                time.sleep(3)
                                print(fltSetTargTemp)
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON):
                                    if self.driver.find_element(
                                            *EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).get_attribute(
                                        'name').find(
                                        'ON') >= 0:
                                        strCurrentState = 'ON'
                                    else:
                                        strCurrentState = 'OFF'

                                if (fltSetTargTemp == 99.0 and strCurrentState == 'OFF') or (
                                                fltSetTargTemp == 0.0 and strCurrentState == 'ON'):
                                    self.driver.find_element(*EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).click()
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.HOUR_SCROLL):
                                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                                    strCurrentHour = oScrolElement.find_element(
                                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                        'name')
                                    strCurrentHour = ('0' + strCurrentHour)[-2:]
                                else:
                                    self.report_fail('Element HOUR_SCROLL is not found')
                                    exit()
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                                    strCurrentMinute = oScrolElement.find_element(
                                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                        'name')
                                else:
                                    self.report_fail('Element MINUTE_SCROLL is not found')
                                    exit()
                                strCurrentTime = strCurrentHour + ':' + strCurrentMinute
                                self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                                self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                                if fltSetTargTemp == 99.0:
                                    strSetState = "ON"
                                else:
                                    strSetState = "OFF"

                                strLog = "Event Number $$Previous Time $$ Previous State$$ Update Time$$ Updated State@@@" + \
                                         str(
                                             intCntr + 1) + "$$" + strCurrentTime + "$$" + strCurrentState + "$$" + strSetStartTime + "$$" + strSetState
                                self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                                intCntrIter = intCntrIter + 1
                                self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                                time.sleep(2)
                                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                                    time.sleep(7)
                                    self.report_pass("Refresh button is found and clicked")
                                elif self.wait_for_element_exist(*EditTimeSlotPageLocators.CANCEL_BUTTON):
                                    self.driver.find_element(*EditTimeSlotPageLocators.CANCEL_BUTTON).click()
                                    time.sleep(2)
                                    self.report_fail("Refresh button is not found, existing the scenario")
                                    break
                                strCurrentStartTIme = lstStartTime[intCntr].get_attribute('text')
                            self.report_pass(
                                'Main Screen after Event number : ' + str(intCntr + 1) + ' is changed')
                        self.report_pass('Main Screen after all Events are changed')
                else:
                    self.report_fail(
                        "Android-App : Control not active on the Hot Water Schedule Page to set the Hot Water Schedule")

            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Page Class for account details page. Has all the methods for the account details page
class AccountDetails(BasePage):
    def open_acc_details(self, strPageName):
        if self.reporter.ActionStatus:
            try:
                print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                if self.wait_for_element_exist(*self.MENU_BUTTON):
                    self.driver.find_element(*self.MENU_BUTTON).click()
                    time.sleep(2)
                    self.driver.find_element(*AccountDetailsLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass("Android App :")
                    if strPageName == "account details":
                        time.sleep(2)
                        self.driver.find_element(*AccountDetailsLocators.ACCOUNT_SUB_MENU).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def validate_acc_details(self, context):
        print("hi")


class HolidayMode(BasePage):
    """Navigates to Holiday screen"""

    def navigateToHoildayScreen(self, context):
        # strHolidayStart = "+2"
        # strHolidayStartTime = "+120"
        # strDuration = "120"
        try:
            if self.wait_for_element_exist(*HomePageLocators.CURRENT_TITLE):
                print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                    print('\n Start \n')
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                    time.sleep(2)
                    if not self.wait_for_element_exist(*HomePageLocators.HOLIDAY_SUB_MENU):
                        if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                            self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                            time.sleep(3)
                            if self.wait_for_element_exist(*HomePageLocators.HOLIDAY_SUB_MENU):
                                self.driver.find_element(*HomePageLocators.HOLIDAY_SUB_MENU).click()
                                print('\n done \n')
                            else:
                                self.report_fail('Error in finding Holiday mode menu item.')
                    else:
                        self.driver.find_element(*HomePageLocators.HOLIDAY_SUB_MENU).click()
                else:
                    self.report_fail('Error in finding Setting menu item.')
        except:
            self.report_fail(' Exception in navigateToHoildayScreen {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def activateHolidaymode(self):
        if self.wait_for_element_exist(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON):
            self.driver.find_element(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON).click()
            time.sleep(2)

    def setHoildayMode(self, context, strHolidayStart, strHolidayStartTime, strDuration):
        print("^^^^^^^^^^^" + str(datetime.now()))
        if "+" in strHolidayStart:
            dtDate = datetime.now() + timedelta(days=int(strHolidayStart.split(sep="+", maxsplit=1)[1]))

            strSetMonth = dtDate.strftime("%B").upper()
            strSetDate = dtDate.day
            strSetYear = dtDate.year
            if "+" in strHolidayStartTime:
                dtDate = datetime.now() + timedelta(seconds=int(strHolidayStartTime.split(sep="+", maxsplit=1)[1]))
                strSetHour = dtDate.hour
                strSetMin = dtDate.minute
            else:
                if "-" in strHolidayStartTime:
                    dtDate = datetime.now() - timedelta(seconds=int(strHolidayStartTime.split(sep="-", maxsplit=1)[1]))
                    strSetHour = dtDate.hour
                    strSetMin = dtDate.minute
        else:
            if "-" in strHolidayStart:
                dtDate = datetime.now() - timedelta(days=int(strHolidayStart.split(sep="-", maxsplit=1)[1]))
                strSetMonth = dtDate.strftime("%B").upper()
                strSetDate = dtDate.day
                strSetYear = dtDate.year
            if "+" in strHolidayStartTime:
                dtDate = datetime.now() + timedelta(seconds=int(strHolidayStartTime.split(sep="+", maxsplit=1)[1]))
                strSetHour = dtDate.hour
                strSetMin = dtDate.minute
            else:
                if "-" in strHolidayStartTime:
                    dtDate = datetime.now() - timedelta(seconds=int(strHolidayStartTime.split(sep="-", maxsplit=1)[1]))
                    strSetHour = dtDate.hour
                    strSetMin = dtDate.minute

        dtDate = dtDate + timedelta(seconds=int(strDuration))
        strSetEndDate = dtDate.day
        strSetEndMonth = dtDate.strftime("%B").upper()
        strSetEndYear = dtDate.year
        strSetEndHour = dtDate.hour
        strSetEndMin = dtDate.minute
        self.verifyHolidayModeSettingPage("First")
        self.setHolidayTargetTemperature(9)
        time.sleep(2)
        self.setHolidayStartDate(str(strSetYear), strSetMonth, str(strSetDate), str(strSetHour), str(strSetMin))
        strSetYear = 2015
        strSetMonth = "OCTOBER"
        strSetDate = "20"
        self.setHolidayEndTime(str(strSetEndYear), strSetEndMonth, str(strSetEndDate), str(strSetEndHour),
                               str(strSetEndMin))
        time.sleep(2)
        self.driver.find_element(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON).click()

    # Set Holiday Mode
    def set_Holiday_Mode(self, context, actionType, strHolidayModeType, targetTemperature, daysFromNow, duration):
        if self.reporter.ActionStatus:
            try:
                if not "NEW" in strHolidayModeType.upper() and not "CANCEL" in actionType.upper() and not "STOP" in actionType.upper():
                    if self.wait_for_element_exist(*HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON):
                        self.driver.find_element(*HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON).click()
                        time.sleep(2)

                if "CANCEL" in actionType.upper():
                    self.cancelHolidayMode(context)

                if "STOP" in actionType.upper():
                    print("******************Waiting for Holiday mode to start**********************")
                    time.sleep(300)
                    print("******************Wait for Holiday mode is ended**********************")
                    self.refresh_page()
                    time.sleep(5)
                    self.report_done('ScreenShot of active Holiday Mode')
                    self.stopHolidayMode(context)

                if "DEFAULT" in strHolidayModeType.upper() and not "CANCEL" in actionType.upper() and not "STOP" in actionType.upper():
                    self.set_holiday_target_temperature(context, targetTemperature)
                    self.activateHolidayMode(context, targetTemperature)

                if "FUTURE" in strHolidayModeType.upper() or "NEW" in strHolidayModeType.upper() or "EDIT" in strHolidayModeType.upper():
                    if "NEW" in strHolidayModeType.upper():
                        if self.wait_for_element_exist(*HolidayModeLocators.EDIT_HOLIDAYMODE_BUTTON):
                            self.driver.find_element(*HolidayModeLocators.EDIT_HOLIDAYMODE_BUTTON).click()
                            time.sleep(3)
                        else:
                            self.report_fail(' Couldn\'t edit Holiday Mode')
                    self.setHolidayStartEndDate(daysFromNow, duration)
                    self.set_holiday_target_temperature(context, targetTemperature)

                    self.activateHolidayMode(context, targetTemperature)
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    if "NEW" in strHolidayModeType.upper():
                        print("******************Waiting for Holiday mode to start**********************")
                        time.sleep(300)
                        print("******************Wait for Holiday mode is ended**********************")

                    if self.is_element_present(*HolidayModeLocators.HOLIDAY_TITLE):
                        strText = self.driver.find_element(*HolidayModeLocators.HOLIDAY_TITLE).get_attribute('text')

                        if daysFromNow is None:
                            strDay = 'today'
                        elif daysFromNow == 1:
                            strDay = 'tomorrow'
                        else:
                            strDay = str(daysFromNow)

                        strExpectedText = "Holiday Mode starts in " + strDay + " days!"

                        if strExpectedText == strText:
                            self.report_pass("The Holiday mode title appeared successfully as - " + strExpectedText)
                        else:
                            self.report_fail(
                                "The Holiday mode title not appeared successfully as - " + strExpectedText + " Actual - " + strText)


            except:
                self.report_fail(' Exception in setting Holiday Mode Time {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Cancel future Holiday Mode
    def cancelHolidayMode(self, context):
        try:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Cancel Holiday Mode')
            if self.wait_for_element_exist(
                    *HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON) and self.wait_for_element_exist(
                *HolidayModeLocators.EDIT_HOLIDAYMODE_BUTTON):

                self.driver.find_element(*HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON).click()
                time.sleep(2)
                if self.wait_for_element_exist(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON):
                    self.report_pass(' Canceled the Holiday Mode')
                else:
                    self.report_fail(' Couldn\'t cancel Holiday Mode, ACTIVATE_HOLIDAY_BUTTON not found')
            else:
                self.report_pass(' Holiday Mode is not scheduled for future')
        except:
            self.report_fail(' Exception in cancelHolidayMode method {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Stop Holiday Mode
    def stopHolidayMode(self, context):
        try:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Stop Holiday Mode')
            if self.wait_for_element_exist(*HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON):
                if self.wait_for_element_exist(*HolidayModeLocators.EDIT_HOLIDAYMODE_BUTTON):
                    self.report_fail('Holiday mode is Active')
                self.driver.find_element(*HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON).click()
                time.sleep(2)
                if self.wait_for_element_exist(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON):
                    self.report_pass(' Stopped the Holiday Mode')
                else:
                    self.report_fail(' Couldn\'t stop Holiday Mode')
            else:
                self.report_fail(' Couldn\'t stop Holiday Mode, Holiday Mode is not active')
        except:
            self.report_fail(' Exception in stopHolidayMode method {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Set the Holiday Target temperature
    def set_holiday_target_temperature(self, context, targetTemp):
        if self.reporter.ActionStatus:
            try:
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set target temperature')
                if self.wait_for_element_exist(*HolidayModeLocators.TEMP_PICKER):
                    oScrolElement = self.driver.find_element(*HolidayModeLocators.TEMP_PICKER)
                    strContent = oScrolElement.get_attribute('name')
                    fltCurrentTargTemp = float(self.get_TempFromElement(strContent))
                    fltSetTargTemp = float(targetTemp)
                    if not fltCurrentTargTemp == fltSetTargTemp:
                        self.set_holiday_target_temp(fltSetTargTemp)
                        self.report_done(
                            " Screenshot after the temp is set")
                else:
                    self.report_fail(
                        " Control not active to set the Holiday Target Temperature")
            except:
                self.report_fail(' Exception in set_holiday_target_temperature Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Activate Holiday mode temperature
    def activateHolidayMode(self, context, targetTemperature, blnStop=True):
        try:

            blnPopUpFlag, blnPopUpFlagAppear = False, False
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Activate Holiday Mode')
            if self.wait_for_element_exist(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON):
                self.driver.find_element(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON).click()
                time.sleep(2)
                if float(targetTemperature) > 12.5:
                    blnPopUpFlag = True

                if self.wait_for_element_exist(*HolidayModeLocators.CONFIRM_CHECKBOX):
                    blnPopUpFlagAppear = True
                    self.driver.find_element(*HolidayModeLocators.CONFIRM_CHECKBOX).click()
                    time.sleep(2)
                    self.driver.find_element(*HolidayModeLocators.SAVE_BUTTON).click()
                    time.sleep(2)

                if blnPopUpFlag == blnPopUpFlagAppear:
                    self.report_pass(' The pop up has behaved successfully for temp - ' + str(targetTemperature))
                else:
                    self.report_fail(' The pop up has not behaved successfully for temp - ' + str(targetTemperature))

                if self.wait_for_element_exist(*HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON):
                    self.report_pass(' Activated Holiday Mode')
                else:
                    self.report_fail(' Couldn\'t activate Holiday Mode')
            else:
                self.report_fail(' Activate Holiday Mode control couldn\'t be found')
        except:
            self.report_fail(' Exception: in activateHolidayMode method \n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Set Start time and end time
    def setHolidayStartEndDate(self, daysFromNow, duration):
        if self.reporter.ActionStatus:
            try:
                daysFromNow = int(daysFromNow)
                duration = int(duration)
                modTime = (datetime.now() + timedelta(days=daysFromNow, hours=0, minutes=duration))

                'Setting Departure date-time for Holiday Mode'
                strStartHoliday = (modTime.strftime("%c"))
                if "  " in strStartHoliday:  # To replace the additional space due to single digit date
                    strStartHoliday = strStartHoliday.replace("  ", " ")
                intDDate = (strStartHoliday.split(' ')[0]) + ' ' + (strStartHoliday.split(' ')[2]) + ' ' + (
                    strStartHoliday.split(' ')[1])
                strDTime = (strStartHoliday.split(' ')[3])
                intDSetHour = (strDTime.split(':')[0])
                intDSetMin = (strDTime.split(':')[1])
                if self.wait_for_element_exist(*HolidayModeLocators.DEPARTURE_TIME):
                    self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).click()
                    time.sleep(2)
                    self.wait_for_element_exist(*HolidayModeLocators.DEPARTURE_TITLE)
                    # Setting Day in Holiday mode
                    self.set_holiday_date(daysFromNow)
                    self.set_schedule_event_hour(intDSetHour)
                    self.set_schedule_event_minute(intDSetMin)
                    if self.wait_for_element_exist(*HolidayModeLocators.DEPARTURE_SAVE):
                        self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
                        time.sleep(2)
                        self.wait_for_element_exist(*HolidayModeLocators.DEPARTURE_TIME)
                elif self.wait_for_element_exist(*HolidayModeLocators.DEPARTURE_CANCEL):
                    self.driver.find_element(*HolidayModeLocators.DEPARTURE_CANCEL).click()
                    self.report_fail(" The Departure Date-Time couldn't be set")
                else:
                    self.report_fail(" The Departure Date-Time couldn't be set")

                'Setting Return date-time for Holiday Mode'

                modTime1 = (modTime + timedelta(days=duration, hours=0, minutes=30))
                strStopHoliday = (modTime1.strftime("%c"))
                if "  " in strStopHoliday:  # To replace the additional space due to single digit date
                    strStopHoliday = strStopHoliday.replace("  ", " ")

                intRDate = (strStopHoliday.split(' ')[0]) + ' ' + (strStopHoliday.split(' ')[2]) + ' ' + (
                    strStopHoliday.split(' ')[1])
                strRTime = (strStopHoliday.split(' ')[3])
                intRSetHour = (strRTime.split(':')[0])
                intRSetMin = (strRTime.split(':')[1])

                if self.wait_for_element_exist(*HolidayModeLocators.ARRIVAL_TIME):
                    self.driver.find_element(*HolidayModeLocators.ARRIVAL_TIME).click()
                    time.sleep(3)
                    # Setting Day in Holiday mode
                    if self.wait_for_element_exist(*HolidayModeLocators.RETURN_TITLE):
                        # #this is used since this PICKER's 'value' property doesn't update
                        self.set_holiday_date(int(daysFromNow) + int(duration))

                    self.set_schedule_event_hour(int(intRSetHour))
                    self.set_schedule_event_minute(intRSetMin)

                    # Collapse the return picker
                    self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
                    time.sleep(2)
                    self.wait_for_element_exist(*HolidayModeLocators.DEPARTURE_TIME)
                else:
                    self.report_fail(" The Return Date-Time couldn't be set")
            except:
                self.report_fail(' Exception in setHolidayStartEndDate method {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # set Date for holiday mode
    def set_holiday_date(self, daysFromNow):
        if daysFromNow is None: daysFromNow = 0

        startDay = datetime.now() + timedelta(days=daysFromNow)
        currentDay = datetime.now()

        currentMonth = int(currentDay.strftime("%m"))
        targetMonth = int(startDay.strftime("%m"))
        if targetMonth != currentMonth:
            monthdiff = targetMonth - currentMonth
            intcounter = 1
            if monthdiff < 0: monthdiff = monthdiff + 12

            for intcounter in range(monthdiff):
                self.driver.find_element(*HolidayModeLocators.RIGHT_ARROW).click()
                time.sleep(4)

        targetDay = int(startDay.strftime("%d"))
        strPropertylist = list(HolidayModeLocators.DAY_PICKER)
        strPropertylist[1] = strPropertylist[1].replace('DAY', str(targetDay))
        strProperty = tuple(strPropertylist)

        oElements = self.driver.find_elements(*strProperty)
        if len(oElements) > 0:
            if len(oElements) == 1:
                oElements[0].click()
            else:
                if targetDay < 23:
                    oElements[0].click()
                else:
                    oElements[1].click()
        else:
            self.report_fail("Day" + str(targetDay) + " is not found")

    # Fetch the holidy mode details for validation
    def get_Holiday_DetailsApp(self, actionType, strHolidayModeType):
        try:
            enabled, strHolidayStartDate, strHolidayStartTime, strHolidayEndDate, strHolidayEndTime, strHolidayTemp = None, None, None, None, None, None
            blnFlag = True
            intCounter = 1
            '''while blnFlag and intCounter < 60:
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    if self.wait_for_element_exist(*HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON) and not self.wait_for_element_exist(*HolidayModeLocators.EDIT_HOLIDAYMODE_BUTTON):
                        blnFlag = False
                    time.sleep(5)
                    intCounter = intCounter +1'''
            if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                self.driver.find_element(*self.REFRESH_BUTTON).click()
                self.wait_for_element_exist(*self.REFRESH_BUTTON)
            if self.wait_for_element_exist(*HolidayModeLocators.STOP_HOLIDAYMODE_BUTTON):
                enabled = 'true'
                if self.is_element_present(*HolidayModeLocators.FROST_TEMP):
                    strHolidayTemp = "FROST"
                elif self.is_element_present(*HolidayModeLocators.TARGET_TEMP):
                    strTemp = self.driver.find_element(*HolidayModeLocators.TARGET_TEMP).get_attribute('text')
                    if self.is_element_present(*HolidayModeLocators.DECIMAL_TEMP):
                        strDecimal = self.driver.find_element(*HolidayModeLocators.DECIMAL_TEMP).get_attribute('text')
                        strTemp = strTemp + strDecimal

                    strHolidayTemp = strTemp
                else:
                    self.report_fail('Error in finding Holiday mode temp icon.')

                oDayElements = self.driver.find_elements(*HolidayModeLocators.DAY_ICON)
                oMonth_Year_TimeElements = self.driver.find_elements(*HolidayModeLocators.MONTH_YEAR_TIME)
                objStartMonthYearTime = oMonth_Year_TimeElements[0].get_attribute('text').split('\n')
                strHolidayStartDate = oDayElements[0].get_attribute('text') + " " + objStartMonthYearTime[0]
                strHolidayStartTime = str(objStartMonthYearTime[1])

                objEndMonthYearTime = oMonth_Year_TimeElements[1].get_attribute('text').split('\n')
                strHolidayEndDate = oDayElements[1].get_attribute('text') + " " + objEndMonthYearTime[0]
                strHolidayEndTime = str(objEndMonthYearTime[1])

                Header = "Departure Date $$ Departure Time $$ Return Date $$ Return Time $$ Target Temperature @@@"

                tableRow1 = strHolidayStartDate + "$$" + strHolidayStartTime + "$$" + strHolidayEndDate + "$$" + strHolidayEndTime + "$$" + strHolidayTemp

                StrLog = Header + tableRow1
                self.reporter.ReportEvent("Test Validation : App ", StrLog, "DONE")

                return enabled, strHolidayStartDate, strHolidayStartTime, strHolidayEndDate, strHolidayEndTime, strHolidayTemp
            elif 'CANCELLED' in actionType.upper() or 'STOPPED' in actionType.upper():
                enabled = 'false'
                self.reporter.ReportEvent("Test Validation : App ", 'Holiday mode is not active', "PASS")
                return None, None, None, None, None, enabled
            else:
                self.reporter.ReportEvent("Test Validation : App ", 'Holiday mode is not active', "FAIL")
                return enabled, strHolidayStartDate, strHolidayStartTime, strHolidayEndDate, strHolidayEndTime, strHolidayTemp
        except:
            self.report_fail(' Exception in get_Holiday_DetailsApp Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Validate Holiday mode details against API
    def validateHolidayModeDetails(self, departureDateUI, departureTimeUI, returnDateUI, returnTimeUI, targetTempUI,
                                   departureDateAPI, departureTimeAPI, returnDateAPI, returnTimeAPI, targetTempAPI,
                                   targetTemperature):
        try:
            Header = "Expected $$ Actual @@@"

            dTimeAPI = datetime.strptime(departureTimeAPI, "%H:%M")
            rTimeAPI = datetime.strptime(returnTimeAPI, "%H:%M")
            dDateAPI = datetime.strptime(departureDateAPI, "%d%b %Y")
            rDateAPI = datetime.strptime(returnDateAPI, "%d%b %Y")
            targetTempUI = targetTempUI.replace('°', '')
            targetTempAPI = targetTempUI.replace('.0', '')

            if departureDateUI != departureDateAPI:
                dHourAPI = str(departureTimeAPI).split(':')[0]
                if dHourAPI == '23':
                    dDateAPI = dDateAPI + timedelta(days=1)
                    dDateAPI = dDateAPI.strftime('%d%b %Y')
                    if departureDateUI != dDateAPI:
                        tableRow1 = departureDateUI + "$$" + departureDateAPI
                        StrLog = Header + tableRow1
                        self.reporter.ReportEvent("Test Validation Departure Date", StrLog, "FAIL")

            if departureTimeUI != departureTimeAPI:
                dTimeAPI = dTimeAPI + timedelta(hours=1)
                dTimeAPI = dTimeAPI.strftime('%H:%M')
                if departureTimeUI != dTimeAPI:
                    tableRow1 = departureTimeUI + "$$" + departureTimeAPI
                    StrLog = Header + tableRow1
                    self.reporter.ReportEvent("Test Validation Departure Time", StrLog, "FAIL")

            if returnDateUI != returnDateAPI:
                rHourAPI = str(returnTimeAPI).split(':')[0]
                if rHourAPI == '23':
                    rDateAPI = rDateAPI + timedelta(days=1)
                    rDateAPI = rDateAPI.strftime('%d%b %Y')
                    if returnDateUI != rDateAPI:
                        tableRow1 = returnDateUI + "$$" + returnDateAPI
                        StrLog = Header + tableRow1
                        self.reporter.ReportEvent("Test Validation Return Date", StrLog, "FAIL")

            if returnTimeUI != returnTimeAPI:
                rTimeAPI = rTimeAPI + timedelta(hours=1)
                rTimeAPI = rTimeAPI.strftime('%H:%M')
                if returnTimeUI != rTimeAPI:
                    tableRow1 = returnTimeUI + "$$" + returnTimeAPI
                    StrLog = Header + tableRow1
                    self.reporter.ReportEvent("Test Validation Return Time ", StrLog, "FAIL")

            if (targetTemperature != targetTempUI) or (targetTemperature != targetTempAPI):
                if targetTempUI != "FROST" and targetTempAPI != "1":
                    tableRow1 = str(targetTemperature) + "$$ App : " + str(targetTempUI) + " API : " + str(
                        targetTempAPI)
                    StrLog = Header + tableRow1
                    self.reporter.ReportEvent("Test Validation Target Temperature", StrLog, "FAIL", "CENTER")
        except:
            self.report_fail(' Exception in validateHolidayModeDetails method {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Set Target temperature
    def setHolidayTargetTemperature(self, fltSetTargTemp):
        time.sleep(2)
        oScrolElement = self.driver.find_element(*HolidayModeLocators.TARGET_TEMPERATURE)
        strContent = oScrolElement.get_attribute('name')
        fltCurrentTargTemp = float(self.get_TempFromElement(strContent))
        self.setScrollValue(self.driver, oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)

    # Validate Holiday mode at control screen
    def validate_holiday_control_screen(self, actionType):
        try:
            blnHolidayMode, blnHolidayModeScreen = False, False
            if self.reporter.ActionStatus:
                if actionType.upper() != "CANCEL" and actionType.upper() != "STOP" and actionType.upper() != "FUTURE":
                    blnHolidayMode = False
                else:
                    blnHolidayMode = True

                if self.is_element_present(*HolidayModeLocators.HOLIDAY_TITLE):
                    blnHolidayModeScreen = True
                else:
                    blnHolidayModeScreen = False

                if blnHolidayModeScreen == blnHolidayMode:
                    self.report_pass('Control screen is as expected')
                else:
                    self.report_fail('Control screen is not as expected')

        except:
            self.report_fail(' Exception in validate_holiday_control_screen method {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Set Scroll Value
    ''' def setScrollValue(self,wd, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision, fltScrolPrecesion):
        intLeftX = oScrolElement.location['x']
        intUpperY = oScrolElement.location['y']
        intWidth = oScrolElement.size['width']
        intHieght = oScrolElement.size['height']
        intStX = intLeftX + intWidth/2
        intStY = intUpperY + fltScrolPrecesion* (intHieght/4)
        intEndX = intStX
        intEndY = intUpperY + 3*(intHieght/4)
        if not fltSetValue==fltCurrentValue:
            if fltSetValue < fltCurrentValue:
                intTemp = intEndY
                intEndY = intStY
                intStY = intTemp
            intIterCount = int(abs(fltSetValue-fltCurrentValue)/fltPrecision)
            for intCnt in range(intIterCount):
                wd.swipe(intStX, intEndY, intEndX, intStY, 1000)
                time.sleep(0.5)
            time.sleep(10)
'''

    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                  "Nov": 11, "Dec": 12}

    def to_dict(self, name):
        return self.month_dict[name]

    def to_if(self, name):
        if name == "JANUARY":
            return 1
        elif name == "FEBRUARY":
            return 2
        elif name == "MARCH":
            return 3
        elif name == "APRIL":
            return 4
        elif name == "MAY":
            return 5
        elif name == "JUNE":
            return 6
        elif name == "JULY":
            return 7
        elif name == "AUGUST":
            return 8
        elif name == "SEPTEMBER":
            return 9
        elif name == "OCTOBER":
            return 10
        elif name == "NOVEMBER":
            return 11
        elif name == "DECEMBER":
            return 12
        else:
            raise ValueError

    def selectHolidayStartTime(self, strStartHour, strStartMin):
        strSetStartTime = strStartHour + ":" + strStartMin
        intCntrIter = 0
        strCurrentStartTIme = self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).get_attribute("text")
        self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).get_attribute("text")
        self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
        time.sleep(2)
        if int(strSetStartTime.split(':')[0]) > 11:
            strSetToTime = str(int(strSetStartTime.split(':')[0]) % 12) + ":" + strSetStartTime.split(':')[1]
        else:
            strSetToTime = strSetStartTime
        while (strCurrentStartTIme != strSetToTime) and (intCntrIter < 3):
            # self.set_schedule_target_temperature(fltSetTargTemp)
            self.set_schedule_event_hour(strStartHour)
            print(strStartMin, '\n')
            input('')
            self.set_schedule_event_minute(int(strStartMin), 1)
            intCntrIter = intCntrIter + 1
            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
            # self.wait_for_element_exist(*self.REFRESH_BUTTON)
            strCurrentStartTIme = self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).get_attribute("text")
            self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
        self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()

    def selectHolidayEndTime(self, strEndHour, strEndMin):
        strSetEndTime = strEndHour + ":" + strEndMin
        intCntrIter = 0
        strCurrentEndTIme = self.driver.find_element(*HolidayModeLocators.ARRIVAL_TIME).get_attribute("text")
        self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).get_attribute("text")
        self.driver.find_element(*HolidayModeLocators.END_DATE_TIME).click()
        time.sleep(2)
        if int(strSetEndTime.split(':')[0]) > 11:
            strSetToTime = str(int(strSetEndTime.split(':')[0]) % 12) + ":" + strSetEndTime.split(':')[1]
        else:
            strSetToTime = strSetEndTime
        while (strCurrentEndTIme != strSetToTime) and (intCntrIter < 3):
            # self.set_schedule_target_temperature(fltSetTargTemp)
            self.set_schedule_event_hour(strEndHour)
            self.set_schedule_event_minute(strEndMin, 1)
            intCntrIter = intCntrIter + 1
            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
            # self.wait_for_element_exist(*self.REFRESH_BUTTON)
            strCurrentEndTIme = self.driver.find_element(*HolidayModeLocators.ARRIVAL_TIME).get_attribute("text")
            self.driver.find_element(*HolidayModeLocators.END_DATE_TIME).click()
        self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()

        # Set the Even Target temperature

    def set_schedule_event_minute(self, intSetMinute, intPrecession=15):
        try:
            if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                intSetMinute = int(intSetMinute)
                intCurrentMinute = int(
                    oScrolElement.find_element(*EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                        'name'))
                self.scroll_element_to_value(oScrolElement, intCurrentMinute, intSetMinute, intPrecession, 1.4)

            else:
                print(
                    "Android-App : Control not active on the Edit Time Slot for Heating schedule Page to set the Event start time Minute")

        except:
            print('Android App : NoSuchElementException: in set_schedule_event_minute Method\n {0}' + format(
                traceback.format_exc().replace('File', '$~File')))

    '''def setHolidayYearAndMonth(self,strSetDate,strMonthName,strYearName,strSetYear,strSetMonth):
        if (int(strYearName) - int(strSetYear)) < 0:
            if (self.to_if(strSetMonth)-self.to_if(strMonthName)) > 0:
                if int(strSetYear) != int(strYearName):
                    if (12-self.to_if(strMonthName) + self.to_if(strSetMonth)) < 12 :
                        for i in range(1,(12-self.to_if(strMonthName) + self.to_if(strSetMonth))):
                            self.driver.find_element(*HolidayModeLocators.DEPARTURE_ADD_MONTH).click()
                    else:
                        if (12-self.to_if(strMonthName) + self.to_if(strSetMonth)) > 12 :
                            for i in range(0,(12+(self.to_if(strSetMonth) - self.to_if(strMonthName)))):
                                self.driver.find_element(*HolidayModeLocators.DEPARTURE_ADD_MONTH).click()
                        else:
                            for i in range(0,12):
                                self.driver.find_element(*HolidayModeLocators.DEPARTURE_ADD_MONTH).click()
                strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_MONTH_YEAR).get_attribute("text")
                strMonthName = strMonthYearName.split(sep=" ", maxsplit=1)[0]
                if self.to_if(strSetMonth) != self.to_if(strMonthName):
                    print("\n ***********Fail")
                else:
                    print("\n ***********Pass")
                    time.sleep(2)
                    self.clickHolidayDate(strSetDate)
        else:
            if (int(strYearName) - int(strSetYear)) == 0:
                if int(self.to_if(strSetMonth)) - int(self.to_if(strMonthName)) > 0:
                    for i in range(0,(self.to_if(strSetMonth) - self.to_if(strMonthName))):
                        self.driver.find_element(*HolidayModeLocators.DEPARTURE_ADD_MONTH).click()
                else:
                    if int(self.to_if(strSetMonth)) - int(self.to_if(strMonthName)) < 0:
                        for i in range(0,(self.to_if(strMonthName) - self.to_if(strSetMonth))):
                            self.driver.find_element(*HolidayModeLocators.DEPARTURE_DEL_MONTH).click()
            else:
                if(int(strYearName) - int(strSetYear)) < 0:
                    for i in range(0,(12-self.to_if(strSetMonth) + self.to_if(strMonthName))-12+(((int(strYearName) - int(strSetYear)) * 12)-12)):
                        self.driver.find_element(*HolidayModeLocators.DEPARTURE_DEL_MONTH).click()
                else:
                    for i in range(0,12):
                        self.driver.find_element(*HolidayModeLocators.DEPARTURE_DEL_MONTH).click()
            strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_MONTH_YEAR).get_attribute("text")
            strMonthName = strMonthYearName.split(sep=" ", maxsplit=1)[0]
            if self.to_if(strSetMonth) != self.to_if(strMonthName):
                print("\n ***********Fail")
            else:
                print("\n ***********Pass")
                time.sleep(2)
                self.clickHolidayDate(strSetDate)'''

    def setHolidayStartDate(self, strSetYear, strSetMonth, strSetDate, strSetHour, strSetMin):
        # self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
        time.sleep(2)
        self.selectHolidayStartTime(strSetHour, strSetMin)
        time.sleep(2)
        self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
        time.sleep(2)
        strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_MONTH_YEAR).get_attribute("text")
        strMonthName = strMonthYearName.split(sep=" ", maxsplit=1)[0]
        strYearName = strMonthYearName.split(sep=" ", maxsplit=1)[1]
        print("@@@@@@@@@@@@@@@@@@@@" + str(int(strSetDate)))
        if (self.to_if(strSetMonth) != self.to_if(strMonthName)) | (int(strSetYear) != int(strYearName)):
            self.setHolidayYearAndMonth(strSetDate, strMonthName, strYearName, strSetYear, strSetMonth)
        else:
            if self.to_if(strSetMonth) != self.to_if(strMonthName):
                print("\n ***********Fail")
            else:
                print("\n ***********Pass")
                time.sleep(2)
                print("HolidayModeLocators.DEPARTURE_DATE")
                self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
                time.sleep(2)
                self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
                time.sleep(2)
                self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
                time.sleep(2)
                print("\n ***********Pass")
                self.clickHolidayDate(strSetDate)
        self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
        time.sleep(2)

    def clickHolidayDate(self, strSetDate):
        oDayElLoc = self.set_TO_property(HolidayModeLocators.DEPARTURE_DATE, "CHANGE", str(int(strSetDate)))
        self.driver.find_element(*oDayElLoc).click()
        time.sleep(2)

    def clickHolidayDates(self, strSetDate):
        oDayElLoc = self.set_TO_property(HolidayModeLocators.DEPARTURE_DATES, "CHANGE", str(int(strSetDate)))
        self.driver.find_element(*oDayElLoc).click()
        time.sleep(2)

    def setHolidayEndTime(self, strSetYear, strSetMonth, strSetDate, strSetHour, strSetMin):
        # self.driver.find_element(*HolidayModeLocators.END_DATE_TIME).click()
        self.selectHolidayEndTime(strSetHour, strSetMin)
        time.sleep(2)
        self.driver.find_element(*HolidayModeLocators.END_DATE_TIME).click()
        time.sleep(2)
        print("@@@@@@@@@@@@@@@@@@@@" + str(int(strSetDate)))
        strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_MONTH_YEAR).get_attribute("text")
        strMonthName = strMonthYearName.split(sep=" ", maxsplit=1)[0]
        strYearName = strMonthYearName.split(sep=" ", maxsplit=1)[1]
        if (self.to_if(strSetMonth) != self.to_if(strMonthName)) | (int(strSetYear) != int(strYearName)):
            self.setHolidayYearAndMonth(strSetDate, strMonthName, strYearName, strSetYear, strSetMonth)
        else:
            if self.to_if(strSetMonth) != self.to_if(strMonthName):
                print("\n ***********Fail")
            else:
                print("\n ***********Pass")
                time.sleep(2)
                self.clickHolidayDate(strSetDate)
            self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
            time.sleep(2)
            # self.driver.find_element(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON).click()
            time.sleep(2)

    def verifyHolidayModeSettingPage(self, strVisitingTime):
        if str(strVisitingTime).upper() == "FIRST":
            strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_DATE).get_attribute("text")
            strDateName = strMonthYearName.split(sep=" ", maxsplit=2)[0]
            strMonthName = strMonthYearName.split(sep=" ", maxsplit=2)[1]
            strYearName = strMonthYearName.split(sep=" ", maxsplit=2)[2]
            print('----' + strDateName + '====' + strMonthName + '"""""""' + strYearName)
            if int(strDateName) == int(datetime.now().day):
                print("Pass")
            else:
                print("Fail")

            if self.to_if(strMonthName.upper()) == int(datetime.now().month):
                print("Pass")
            else:
                print("Fail")
            if int(strYearName) == int(datetime.now().year):
                print("Pass")
            else:
                print("Fail")
            strMonthYearName = self.driver.find_element(*HolidayModeLocators.ARRIVAL_DATE).get_attribute("text")
            strDateName = strMonthYearName.split(sep=" ", maxsplit=2)[0]
            strMonthName = strMonthYearName.split(sep=" ", maxsplit=2)[1]
            strYearName = strMonthYearName.split(sep=" ", maxsplit=2)[2]
            print('----' + strDateName + '====' + strMonthName + '"""""""' + strYearName)
            dtDate = datetime.now() + timedelta(days=7)
            if int(strDateName) == int(dtDate.day):
                print("Pass")
            else:
                print("Fail")

            if self.to_if(strMonthName.upper()) == int(dtDate.month):
                print("Pass")
            else:
                print("Fail")
            if int(strYearName) == int(dtDate.year):
                print("Pass")
            else:
                print("Fail")


class SetChangePassword(BasePage):
    def change_password_screen(self):
        if self.reporter.ActionStatus:
            try:
                strPassword = utils.getAttribute('common', 'password')
                if self.wait_for_element_exist(*ChangePasswordLocators.OLD_PASSWORD_EDITTEXT):
                    self.driver.find_element(*ChangePasswordLocators.OLD_PASSWORD_EDITTEXT).send_keys(strPassword)
                    self.report_pass('Android APP: Change Password Screen: Old password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password Screen: Old password is entered successfully')

                if self.wait_for_element_exist(*ChangePasswordLocators.NEW_PASSWORD_EDITTEXT):
                    self.driver.find_element(*ChangePasswordLocators.NEW_PASSWORD_EDITTEXT).send_keys('Password1' + "a")
                    self.report_pass('Android APP: Change Password Screen: New password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password Screen: New password is entered successfully')

                if self.wait_for_element_exist(*ChangePasswordLocators.CONF_PASSWORD_EDITTEXT):
                    self.driver.find_element(*ChangePasswordLocators.CONF_PASSWORD_EDITTEXT).send_keys(
                        'Password1' + "a")
                    self.report_pass('Android APP: Change Password Screen: Retype password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password Screen: Retype password is entered successfully')

                if self.wait_for_element_exist(*ChangePasswordLocators.SAVE_PASSWORD):
                    self.driver.find_element(*ChangePasswordLocators.SAVE_PASSWORD).click()
                    self.report_pass('Android APP: Change Password Screen:  Password is set successfully')
                    time.sleep(2)
                else:
                    self.report_fail(
                        'Android APP: Change Password Screen: Password is not set ,Save button is not clicked')


            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

                # Navigate To ChangePassword Screen

    def navigate_to_change_password(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                    self.report_pass('Android APP: Change Password : Navigated to Menu Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password : Menu is not selected Successfully')

                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass('Android APP: Navigated to Settings Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password : Settings is selected Successfully')

                print('settings clicked')
                self.driver.swipe(200, 800, 220, 500, 1000)
                time.sleep(2)
                if self.wait_for_element_exist(*HomePageLocators.CHANGE_PASSWORD_SUBMENU):
                    self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUBMENU).click()
                    self.report_pass('Android APP: Navigated to Change Password screen Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password : is not selected Successfully')


            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def login_change_password(self):
        if self.reporter.ActionStatus:
            try:
                strUserName = utils.getAttribute('common', 'userName')
                strPassword = utils.getAttribute('common', 'password')

                if self.wait_for_element_exist(*LoginPageLocators.LOGIN_BUTTON):
                    print("am in")
                    self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys(strUserName)
                    self.driver.hide_keyboard()
                    self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys('Password1' + "a")
                    self.driver.hide_keyboard()
                    self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                if self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6):
                    self.report_pass(
                        'Android-App: The Hive Android App is successfully Logged in with the Changed Password')
                else:
                    self.report_fail(
                        'Android-App: The Hive Android App is not logged in. Please check the Login credentials and re-execute test.')

                    # else:
                # self.report_fail('The Hive App is either not Launched or the Login screen is not displayed. Please check and re-execute test.')

                self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.driver.swipe(200, 800, 220, 500, 1000)
                    time.sleep(2)
                self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUBMENU).click()

                self.driver.find_element(*ChangePasswordLocators.OLD_PASSWORD_EDITTEXT).send_keys('Password1' + "a")
                self.driver.find_element(*ChangePasswordLocators.NEW_PASSWORD_EDITTEXT).send_keys(strPassword)
                self.driver.find_element(*ChangePasswordLocators.CONF_PASSWORD_EDITTEXT).send_keys(strPassword)
                self.driver.find_element(*ChangePasswordLocators.SAVE_PASSWORD).click()
                # self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()

            except:
                self.report_fail('Android-App: Exception in login_hive_app Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class TextControl(BasePage):
    def textControlOptions(self, context):
        if self.reporter.ActionStatus:
            for oRow in context.table:
                strusername = oRow['UserName']
                strMobileNo = oRow['MobileNo']
                print(strusername, strMobileNo)
                try:
                    if self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed():
                        self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).click()
                        self.driver.find_element(*TextControlLocators.NAME_EDTBOX).send_keys(strusername)
                        self.driver.find_element(*TextControlLocators.MOBILE_EDTBOX).send_keys(strMobileNo)
                        self.driver.find_element(*TextControlLocators.SAVE_BUTTON).click()
                        time.sleep(5)
                        try:
                            if self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed():
                                self.report.done("Android App:Maximum user limit reached in TextControl Page")

                            else:
                                self.driver.find_element(*TextControlLocators.SAVE_BUTTON).is_displayed()
                                self.report_fail("Android App:This number is already registered to a Hive Account")
                        except:
                            self.report_pass("Android App:User added to Text Control successfully")


                except:
                    self.report_fail("Android App:Maximum user limit reached in TextControl Options")

    def textControlValidation(self, context):
        if self.reporter.ActionStatus:
            try:
                '''strUserCount=self.driver.find_element(*TextControlLocators.USER_TABLE).text
                intRowCount=int(strUserCount[(len(strUserCount)-1)])'''
                try:

                    self.report_done("Android App:More users can be added in TextControl Page")
                except:

                    self.report_pass("Android App:Text Control Options reached Maximum user limits")
                else:
                    self.report_done("Android App:More users can be added in TextControl Page")
            except:
                self.report_fail('Android App : NoSuchElementException: in textControlValidation\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_TextControl_page(self):

        if self.reporter.ActionStatus:
            try:
                rowcount = 1
                if rowcount <= 6:
                    if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                        self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                        print('finished clicking home')
                        time.sleep(2)
                        self.driver.find_element(*HomePageLocators.HELP_SUPPORT_SUBMENU).click()
                        print('clicked help menu')
                    if self.wait_for_element_exist(*TextControlLocators.TEXTCONTROL_SUBMENU):
                        self.driver.find_element(*TextControlLocators.TEXTCONTROL_SUBMENU).click()
                        rowcount = rowcount + 1
                        time.sleep(2)
                        self.report_pass('Android-App : Successfully navigated to the Change Password Page')

                    else:
                        self.report_fail("Android-App : Control not active on the Change Password Page")
                else:
                    self.report_fail("Android-App : Control not active on the Menu Button")
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_change_password_screen\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


class SaveHeatingNotification(BasePage):
    # Navigates to Notification screen
    def naivgate_to_ZoneNotificaiton(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                    self.report_pass('Hive user is able access Menu successfully')
                    time.sleep(2)
                else:
                    self.report_fail('What went wrong -> Opps! Hive user is not able to access Menu')

                if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_NOTIFICATION):
                    self.driver.find_element(*HeatingNotificationsLocators.HEATING_NOTIFICATION).click()
                    self.report_pass(
                        'Hive user is able to access sub menu item Heating notification successfully')
                elif self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_NOTIFICATION):
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_NOTIFICATION).click()
                        self.report_pass(
                            'Hive user is able to access sub menu item Heating notification successfully')
                    else:
                        self.report_fail('Android APP: Hive user is not able to navigate to Heating notification ')
                else:
                    self.report_fail('Android APP: Hive user is not able to navigate to Heating notification ')

            except:
                self.report_fail('Android App : NoSuchElementException: in Heating Notification Screen\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # updates high temperature threshold
    def setHighTemperature(self, oTargetHighTemp):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MAX_SWITCH):

                    if self.driver.find_element(*HeatingNotificationsLocators.HEATING_MAX_SWITCH).get_attribute(
                            "text") == "OFF":
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_MAX_SWITCH).click()
                        time.sleep(3)
                        self.report_done(
                            'Hive user is able to click on switch button')
                if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MAX_SWITCH) and \
                                self.driver.find_element(
                                    *HeatingNotificationsLocators.HEATING_MAX_SWITCH).get_attribute("text") == "ON":
                    self.report_pass(
                        'Hive user is able to navigate to Maximum temperature screen successfully')
                    time.sleep(2)
                    if self.driver.find_element(*HeatingNotificationsLocators.HEATING_MAXTEMP_ICON):
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_MAXTEMP_ICON).click()
                        time.sleep(3)
                        self.set_schedule_target_temperature(oTargetHighTemp)
                        time.sleep(3)
                        if self.wait_for_element_exist(*HeatingNotificationsLocators.SAVE_BUTTON):
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_BUTTON).click()
                            time.sleep(2)
                        else:
                            self.report_fail(' Save Button is not displayed')
                            self.clickCancelButton()
                            self.clickCancelButton()
                        if self.wait_for_element_exist(*HeatingNotificationsLocators.SAVE_BUTTON):
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_BUTTON).click()
                            time.sleep(5)
                        else:
                            self.report_fail(' Save Button is not displayed')
                            self.clickCancelButton()
                            self.clickCancelButton()
                    else:
                        self.report_fail(' State of Maximum temperature switch is not updated to ON')
                        self.clickCancelButton()
                else:
                    self.report_fail(' Maximum temperature switch is not displayed')
                    self.clickCancelButton()
            except:
                self.report_fail('Android APP: Exception in setHighTemperature Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # updates Low temperature threshold
    def setLowTemperature(self, oTargetLowTemp):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MIN_SWITCH):

                    if self.driver.find_element(*HeatingNotificationsLocators.HEATING_MIN_SWITCH).get_attribute(
                            "text") == "OFF":
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_MIN_SWITCH).click()
                        time.sleep(3)
                        self.report_done(
                            'Hive user is able to click on switch button')
                if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MIN_SWITCH) and \
                                self.driver.find_element(
                                    *HeatingNotificationsLocators.HEATING_MIN_SWITCH).get_attribute("text") == "ON":
                    self.report_pass(
                        'Hive user is able to navigate to Minimum temperature screen successfully')
                    time.sleep(2)
                    if self.driver.find_element(*HeatingNotificationsLocators.HEATING_MINTEMP_ICON):
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_MINTEMP_ICON).click()
                        time.sleep(3)
                        self.set_schedule_target_temperature(oTargetLowTemp)
                        time.sleep(3)
                        if self.wait_for_element_exist(*HeatingNotificationsLocators.SAVE_BUTTON):
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_BUTTON).click()
                            time.sleep(2)
                        else:
                            self.report_fail(' Save Button is not displayed')
                            self.clickCancelButton()
                            self.clickCancelButton()
                        if self.wait_for_element_exist(*HeatingNotificationsLocators.SAVE_BUTTON):
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_BUTTON).click()
                            time.sleep(5)
                        else:
                            self.report_fail(' Save Button is not displayed')
                            self.clickCancelButton()
                            self.clickCancelButton()
                    else:
                        self.report_fail(' State of Minimum temperature switch is not updated to ON')
                        self.clickCancelButton()
                else:
                    self.report_fail(' Minimum temperature switch is not displayed')
                    self.clickCancelButton()
            except:
                self.report_fail('Android APP: Exception in setLowTemperature Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # updates Warning switch
    def receiveWarnings(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotificationsLocators.WARNING_OFF):
                    time.sleep(2)
                    self.driver.find_element(*HeatingNotificationsLocators.WARNING_OFF).click()
                    self.report_pass(' Hive user enabled the Receive Warnings')
                    if self.wait_for_element_exist(*HeatingNotificationsLocators.SAVE_BUTTON):
                        self.driver.find_element(*HeatingNotificationsLocators.SAVE_BUTTON).click()
                        time.sleep(2)
                        self.report_pass('The SAVE_BUTTON is found and Clicked')
                    else:
                        self.report_fail('The SAVE_BUTTON is not found')
                        self.clickCancelButton()
                else:
                    self.report_pass('Hive user has already enabled Receive Warnings')

            except:
                self.report_fail('Android APP: Exception in receiveWarnings Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Sets the target temp
    def set_schedule_target_temperature(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotificationsLocators.EVENT_TARGET_TEMPERATURE_SCROLL):
                    oScrolElement = self.driver.find_element(
                        *HeatingNotificationsLocators.EVENT_TARGET_TEMPERATURE_SCROLL)
                    strContent = oScrolElement.get_attribute('name')
                    fltCurrentTargTemp = float(self.get_TempFromElement(strContent))
                    strIntialTemp = str(fltCurrentTargTemp)
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5,
                                                     2)
                        strContent = oScrolElement.get_attribute('name')
                        fltCurrentTargTemp = float(self.get_TempFromElement(strContent))
                        intCntrIter = intCntrIter + 1
                    if fltCurrentTargTemp == fltSetTargTemp:
                        strLog = "Inital Temperature $$ Final Temperature@@@" + \
                                 strIntialTemp + "$$" + str(fltSetTargTemp)
                        self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                        self.report_pass(
                            'The Target Temperature is successfully set to : ' + str(
                                fltSetTargTemp))
                    else:
                        self.report_fail(
                            'Unable to set the Target Temperature to : ' + str(
                                fltSetTargTemp))
                else:
                    self.report_fail(
                        "Control not active on the Edit Temp Slot for Heating Notification Page to set the Target Temperature")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_schedule_target_temperature Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Sets the notification
    def setNotificationONtoOFF(self, strNotificationState):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MAX_ON):
                    self.report_pass(
                        'Hive user is able to navigate to Maximum temperature screen successfully')
                    time.sleep(2)
                    if strNotificationState == 'OFF':
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_MAX_ON).click()
                        time.sleep(2)
                        # self.driver.find_element(*HeatingNotificationsLocators.SAVE_HEATING_NOTIFICATION).click()
                        self.report_pass('Hive user turnes off the Maximum Temperature')
                    else:
                        self.clickCancelButton()
                elif self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MAX_OFF):
                    self.report_pass('Hive user has been already set as Inactive for Maximum Temperature')
                else:
                    self.report_fail('The Switch for Max Temp is not found')
                    self.clickCancelButton()

                if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MIN_ON):
                    self.report_pass(
                        'Hive user is able to navigate to Minimum temperature screen successfully')
                    time.sleep(2)
                    if strNotificationState == 'OFF':
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_MIN_ON).click()
                        time.sleep(2)
                        # self.driver.find_element(*HeatingNotificationsLocators.SAVE_HEATING_NOTIFICATION).click()
                        self.report_pass('Hive user turnes off the Minimum Temperature')
                    else:
                        self.clickCancelButton()
                elif self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MIN_OFF):
                    self.report_pass('Hive user has been already set as Inactive for Minimum Temperature')
                else:
                    self.report_fail('The Switch for Min Temp is not found')
                    self.clickCancelButton()

                if self.wait_for_element_exist(*HeatingNotificationsLocators.WARNING_ON):
                    self.driver.find_element(*HeatingNotificationsLocators.WARNING_ON).click()
                    time.sleep(2)
                    self.report_fail('The Warning Switch is found and Clicked')
                elif self.wait_for_element_exist(*HeatingNotificationsLocators.WARNING_OFF):
                    self.report_pass('The WARNING switch is already in Inactive state')
                else:
                    self.report_fail('The Warning Switch is not found')
                    self.clickCancelButton()

                if self.wait_for_element_exist(*HeatingNotificationsLocators.SAVE_BUTTON):
                    self.driver.find_element(*HeatingNotificationsLocators.SAVE_BUTTON).click()
                    time.sleep(2)
                    self.report_pass('The SAVE_BUTTON is found and Clicked')
                else:
                    self.report_fail('The SAVE_BUTTON is not found')
                    self.clickCancelButton()

            except:
                self.report_fail('Android APP: Exception in heating schedule on to off Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Click on Cancel button
    def clickCancelButton(self):
        if self.driver.find_element(*HeatingNotificationsLocators.CANCEL_HEATING_NOTIFICATION):
            self.driver.find_element(*HeatingNotificationsLocators.CANCEL_HEATING_NOTIFICATION)
            time.sleep(2)

    # Fetch Temp from UI
    def getNotificationTempFromUI(self, strNotificationType='Both'):

        self.naivgate_to_ZoneNotificaiton()
        oCurrentHighTemp = oCurrentLowTemp = "0.0"
        if strNotificationType == 'Both' or strNotificationType == 'High':
            if self.wait_for_element_exist(*HeatingNotificationsLocators.HIGH_TEMP_ICON):
                tempHighUpDown = self.driver.find_element(*HeatingNotificationsLocators.HIGH_TEMP_ICON)
                oCurrentHighTemp = tempHighUpDown.get_attribute('text')
                oCurrentHighTemp = float(oCurrentHighTemp[:-1])
            else:
                self.report_fail(
                    'Unable to Locate Element HIGH_TEMP_IT')
        if strNotificationType == 'Both' or strNotificationType == 'Low':
            if self.wait_for_element_exist(*HeatingNotificationsLocators.LOW_TEMP_ICON):
                tempLowUpDown = self.driver.find_element(*HeatingNotificationsLocators.LOW_TEMP_ICON)
                oCurrentLowTemp = tempLowUpDown.get_attribute('text')
                oCurrentLowTemp = float(oCurrentLowTemp[:-1])
            else:
                self.report_fail(
                    'Unable to Locate Element LOW_TEMP_IT')

        if self.wait_for_element_exist(*HeatingNotificationsLocators.SAVE_BUTTON):
            self.driver.find_element(*HeatingNotificationsLocators.SAVE_BUTTON).click()
            time.sleep(2)
            self.report_pass('The SAVE_BUTTON is found and Clicked')
        else:
            self.clickCancelButton()

        return oCurrentHighTemp, oCurrentLowTemp


class SetPinLock(BasePage):
    def navigate_to_pin_lock(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                    self.report_pass('Android APP :  Hive user is able access Menu successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: What went wrong -> Opps! Hive user is not able to access Menu')

                if self.wait_for_element_exist(*PinLock.PINLOCK_SUB_MENU):
                    self.driver.find_element(*PinLock.PINLOCK_SUB_MENU).click()
                    self.report_pass('Android APP: Hive user is able to access sub menu item Pinlock successfully')
                elif self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.driver.find_element(*PinLock.PINLOCK_SUB_MENU).click()
                    self.report_pass('Android APP: Hive user is able to access sub menu item Pinlock successfully')
                else:
                    self.report_pass('Android APP: Hive user is not able to navigate to Pinlock ')

            except:
                self.report_fail('Android App : NoSuchElementException: in Pinlock Screen\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_pinlock(self):

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_STATUS_OFF):
                    self.report_pass('Android APP: Navigated to Set Pin Lock screen Successfully')
                    time.sleep(2)
                    self.driver.find_element(*PinLock.PINLOCK_STATUS_OFF).click()

                elif self.wait_for_element_exist(*PinLock.PINLOCK_STATUS_ON):
                    time.sleep(2)
                    self.report_pass('Android APP: Hive user has set pin lock already')
                else:
                    self.report_fail('Android APP: Pin Lock Screen is not selected Successfully')

                if self.wait_for_element_exist(*PinLock.ENTER_NEW_PIN):
                    self.driver.find_element(*PinLock.ENTER_NEW_PIN).send_keys("1234")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.REENTER_NEW_PIN).send_keys("1234")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.SAVE_NEW_PIN).click()
                    self.report_pass('Android APP: Pin lock set pin is selected screen Successfully')
                else:
                    self.report_fail('Android APP: Pin Lock Not set')

            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def validate_pin(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_CHANGE_PIN):
                    self.report_pass('Android APP: Pin lock is set successfully')
                else:
                    self.wait_for_element_exist(*PinLock.PINLOCK_STATUS_OFF)
                    self.driver.find_element(*PinLock.PINLOCK_STATUS_OFF).click()
                    self.wait_for_element_exist(*PinLock.PINLOCK_STATUS_ON)
                    self.report_pass('Android APP:Pin lock is not set successfully')
            except:
                self.report_fail('Android-App: Exception in login_hive_app Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def change_pin(self):

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_CHANGE_PIN):
                    self.driver.find_element(*PinLock.PINLOCK_CHANGE_PIN).click()
                    self.report_pass('Android APP: Change Pin Screen is entered successfully')
                else:
                    self.report_fail('Android APP: Change Pin Screen is not entered successfully')

                if self.wait_for_element_exist(*PinLock.ENTER_CURRENT_PIN_CHANGE):
                    self.driver.find_element(*PinLock.ENTER_CURRENT_PIN_CHANGE).send_keys("1234")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.ENTER_NEW_PIN_CHANGE).send_keys("4321")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.CONFIRM_NEW_PIN_CHANGE).send_keys("4321")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.SAVE_CHANGE_PIN).click()
                    self.report_pass('Android APP: Old Pin is entered success')
                else:
                    self.report_fail('Android APP: Enter new pin is not entered entered')

            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def forgot_pin_lock(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_FORGOT_PIN):
                    time.sleep(2)
                    self.driver.find_element(*PinLock.PINLOCK_FORGOT_PIN).click()
                    self.report_pass('Android APP: Forgot Pin is selected Successfully')

                else:
                    self.report_fail('Android APP: Forgot Pin is not selected Successfully')

            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def forgot_validate_pin(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_LOGOUT):
                    self.report_pass('Android APP: Forgot PIN is selected Successfully')
                    self.driver.find_element(*PinLock.PINLOCK_CANCEL).click()
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Forgot Pin is not done Successfully')

            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class MotionSensor(BasePage):
    # navigates to the event log of the motion sensor by clicking the Todays logs's button
    def navigateToEventLogs(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                elif self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS):
                    # clicks the todays logs button
                    self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS).click()
                    self.report_pass('Android App : Navigated to event logs of Motion Sensor screen')

                else:
                    self.report_fail('Android App : Navigation to event log failed')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_eventlogs Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # checks for event logs on the log screen
    def validateEventLogs(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:

                    Motion_Event_Logs = self.driver.find_elements(*MotionSensorLocators.MOTION_EVENT_LOG)

                    if len(Motion_Event_Logs) > 0:
                        self.report_pass('There is/are ' + str(len(Motion_Event_Logs)) + ' events displayed')
                    else:
                        self.report_pass('There are no events displayed')

                    if self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE):
                        self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in validation event logs \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # checks for current status of the motion sensor
    def checkCurrentStatus(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    time.sleep(1)
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:
                    self.wait_for_element_exist(*MotionSensorLocators.MOTION_STATUS)
                    if "Motion" == self.driver.find_element(*MotionSensorLocators.MOTION_STATUS).get_attribute(
                            "text"):
                        self.report_pass('Android App : Current motion status verified as in motion')

                    elif "No Motion" == self.driver.find_element(*MotionSensorLocators.MOTION_STATUS).get_attribute(
                            'text'):
                        self.report_pass('Android App : Current motion status verified as no motion')
                        time.sleep(5)
                    else:
                        self.report_fail('Android App : The given Motion Sensor does not exist in the kit')
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # navigates to the selected day of the log screen, to validate the event log
    def navigateToSelectedDayOfLog(self, intNumberOf):

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:

                    totalNoOfDays = 7
                    dayToSeeTheLogs = (totalNoOfDays - int(intNumberOf)) + 1

                    if self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS):
                        self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS).click()
                        self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE)

                    if (dayToSeeTheLogs == 7) & (self.wait_for_element_exist(*MotionSensorLocators.DAY1_LOG)):
                        self.driver.find_element(*MotionSensorLocators.DAY1_LOG).click()
                        self.report_pass('Navigated to event logs for given day of Motion Sensor screen')
                    elif (dayToSeeTheLogs == 6) & (self.wait_for_element_exist(*MotionSensorLocators.DAY2_LOG)):
                        self.driver.find_element(*MotionSensorLocators.DAY2_LOG).click()
                        self.report_pass('Navigated to event logs for given day of Motion Sensor screen')
                    elif (dayToSeeTheLogs == 5) & (self.wait_for_element_exist(*MotionSensorLocators.DAY3_LOG)):
                        self.driver.find_element(*MotionSensorLocators.DAY3_LOG).click()
                        self.report_pass('Navigated to event logs for given day of Motion Sensor screen')
                    elif (dayToSeeTheLogs == 4) & (self.wait_for_element_exist(*MotionSensorLocators.DAY4_LOG)):
                        self.driver.find_element(*MotionSensorLocators.DAY4_LOG).click()
                        self.report_pass('Navigated to event logs for given day of Motion Sensor screen')
                    elif (dayToSeeTheLogs == 3) & (self.wait_for_element_exist(*MotionSensorLocators.DAY5_LOG)):
                        self.driver.find_element(*MotionSensorLocators.DAY5_LOG).click()
                        self.report_pass('Navigated to event logs for given day of Motion Sensor screen')
                    elif (dayToSeeTheLogs == 2) & (self.wait_for_element_exist(*MotionSensorLocators.DAY6_LOG)):
                        self.driver.find_element(*MotionSensorLocators.DAY6_LOG).click()
                        self.report_pass('Navigated to event logs for given day of Motion Sensor screen')
                    elif (dayToSeeTheLogs == 1) & (self.wait_for_element_exist(*MotionSensorLocators.DAY6_LOG)):
                        self.driver.find_element(*MotionSensorLocators.DAY6_LOG).click()
                        self.report_pass('Navigated to event logs for given day of Motion Sensor screen')
                    else:
                        self.report_fail('Android App : Invalid number of days')
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class ContactSensor(BasePage):
    def navigate_to_contact_sensor(self, nameContactSensor):
        if self.reporter.ActionStatus:
            try:
                strProperty = ""
                if self.wait_for_element_exist(*HomePageLocators.CURRENT_TITLE):
                    strTitle = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    if nameContactSensor in strTitle.upper():
                        self.report_pass('Navigated to event logs of Contact Sensor screen')
                    else:

                        if not self.wait_for_element_exist(*HoneycombDashboardLocators.DASHBOARD_ICON):
                            if self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                                self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                                time.sleep(2)

                        if self.wait_for_element_exist(*HoneycombDashboardLocators.DASHBOARD_ICON):
                            strDeviceName = list(HoneycombDashboardLocators.HONEYCOMB_ICON)
                            strDeviceName[1] = strDeviceName[1].replace("DEVICENAME", nameContactSensor)
                            strProperty = tuple(strDeviceName)

                        if self.wait_for_element_exist(*strProperty):
                            self.driver.find_element(*strProperty).click()
                            time.sleep(2)
                            self.report_pass('Navigated to event logs of Contact Sensor screen')
                        else:
                            self.dashboardSwipe(False)

                            time.sleep(2)
                            if self.wait_for_element_exist(*strProperty):
                                self.driver.find_element(*strProperty).click()
                                time.sleep(2)
                                self.report_pass(
                                    'Navigated to event logs of Contact Sensor screen - ' + nameContactSensor)
                            else:
                                self.report_fail('Not able to find Contact Sensor on dashboard- ' + nameContactSensor)
                else:
                    self.report_fail('Unable to navigate to Contact Sensor screen')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_contact_sensor Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def contactSensorCurrentStatus(self):
        if self.reporter.ActionStatus:
            try:
                strStatus = ""
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(2)

                    if self.wait_for_element_exist(*ContactSensorLocators.CONTACTSENSOR_CONTROL_STATUS):
                        strStatus = self.driver.find_element(
                            *ContactSensorLocators.CONTACTSENSOR_CONTROL_STATUS).get_attribute('text')
                        self.report_pass('Control Icon is found status - ' + strStatus)

                    else:
                        self.report_fail('Control Icon is not found')
                    return strStatus
                else:
                    self.report_fail('Refresh Icon is not found')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in contactSensorCurrentStatus Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def todaysLog(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*ContactSensorLocators.CONTACTSENSOR_LOGS_BUTTON):
                    self.driver.find_element(*ContactSensorLocators.CONTACTSENSOR_LOGS_BUTTON).click()
                    time.sleep(2)
                    self.report_pass('Navigated to today event logs of Contact Sensor screen')

                else:
                    self.report_fail('Navigation to today event log failed')
            except:
                self.report_fail('Android App : NoSuchElementException: in todaysLog Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verify_todayevent_logs(self):
        if self.reporter.ActionStatus:
            try:
                objlist = list(ContactSensorLocators.CONTACTSENSOR_DAY_SELECT)
                objlist[1] = objlist[1].replace("DEVICEINDEX", "7")
                strProperty = tuple(objlist)
                if self.wait_for_element_exist(*strProperty):
                    self.driver.find_element(*strProperty).click()
                    time.sleep(2)
                    self.report_pass('Navigated to selected day event logs of Contact Sensor screen')
                    objElements = self.driver.find_elements(*ContactSensorLocators.CONTACTSENSOR_EVENT_INFO)
                    if len(objElements) > 0:
                        self.report_pass('There is/are ' + str(len(objElements)) + ' events displayed')
                    else:
                        self.report_pass('There are no events displayed')
                else:
                    self.report_fail('Navigation to today event log failed')
                if self.wait_for_element_exist(*ContactSensorLocators.CONTACTSENSOR_CLOSEEVENT_LOGS):
                    self.driver.find_element(*ContactSensorLocators.CONTACTSENSOR_CLOSEEVENT_LOGS).click()
                    time.sleep(2)
                    self.honeycomb_verify()
            except:
                self.report_fail('Android App : NoSuchElementException: in todaysLog Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_selected_weekday_log(self, selectWeekDay):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(2)
                    objlist = list(ContactSensorLocators.CONTACTSENSOR_DAY_SELECT)
                    objlist[1] = objlist[1].replace("DEVICEINDEX", str(7 - int(selectWeekDay.split()[0])))
                    strProperty = tuple(objlist)
                    if self.wait_for_element_exist(*strProperty):
                        self.driver.find_element(*strProperty).click()
                        time.sleep(2)
                        self.report_pass('Navigated to selected day event logs of Contact Sensor screen')
                    else:
                        self.report_fail('Navigation to selected day event log failed, The day is not found')
                else:
                    self.report_fail('Navigation to selected day event log failed')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_selected_weekday_log Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def verify_event_logs(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY):
                        self.report_pass(
                            'Android App : Verified there are no logs present in Motion Sensor screen currently')
                    elif self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY):
                        self.report_pass(
                            'Android App : Verified there is current motion log present in Motion Sensor screen')
                    elif self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY):
                        self.report_pass(
                            'Android App : Verified there are multiple logs present in Motion Sensor screen')
                    else:
                        self.report_fail('Android App : Unexpected logs found')

                if self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE):
                    self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verify_current_status(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY):
                        print("Motion Sensor has detected motion. Call API validation")
                        self.report_pass('Android App : Current motion status verified as in motion')
                        time.sleep(5)
                    elif self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY):
                        print("Motion Sensor has not detected motion. Call API validation")
                        self.report_pass('Android App : Current motion status verified as no motion')
                        time.sleep(5)
                    else:
                        self.report_fail('Android App : The given Motion Sensor does not exist in the kit')
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class ActiveLights(BasePage):
    # Local Variables
    SETTINGS_LOCAL = ""
    VALUE_LOCAL = ""
    SWITCH_ON = 0
    BULB_TYPE = ""
    BULB_MODEL = ""

    # Store the bulb settings ( brightness or tone or colour etc... ) and its value ( 30% or warmest white or Orange etc...)
    def setValues(self, Settings, Value):
        ActiveLights.SETTINGS_LOCAL = Settings
        ActiveLights.VALUE_LOCAL = Value

    # Sets bulb model value for respective bulb
    def setBulbModelandName(self, lightName):
        ActiveLights.BULB_TYPE = lightName.upper()
        if lightName.upper() == "WARM WHITE LIGHT":
            ActiveLights.BULB_MODEL = "FWBulb01"
        elif lightName.upper() == "TUNEABLE LIGHT":
            ActiveLights.BULB_MODEL = "TWBulb01UK"
        elif lightName.upper() == "COLOUR LIGHT":
            ActiveLights.BULB_MODEL = "RGBBulb01UK"
        else:
            return False

    # Checks the presence of Bulb icon on Honeycomb Dashboard
    def checkHoneycombBulbIconPresense(self, lighttype):
        activeLightName = str(HoneycombDasbordLocators.HONEYCOMB_LIGHT)
        activeLightName = activeLightName.replace("lightName", lighttype)
        if self.wait_for_element_exist(By.XPATH, activeLightName):
            return True
        else:
            return False

    # Clicks on the Bulb icon on Honeycomb Dashboard
    def clickBulbHoneycombBulbIcon(self, lighttype):
        activeLightName = str(HoneycombDasbordLocators.HONEYCOMB_LIGHT)
        activeLightName = activeLightName.replace("lightName", lighttype)
        if self.wait_for_element_exist(By.XPATH, activeLightName):
            self.driver.find_element(By.XPATH, activeLightName).click()
        else:
            return False

    # Navigates to respective Light Bulb Control Page
    def navigate_to_active_light_page(self, nameActiveLight):
        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        nameActiveLight.upper()) >= 0:
                    pagePresense = False
                    if self.currentAppVersion == 'V6':
                        time.sleep(2)
                        self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                        if pagePresense == False:
                            self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                            time.sleep(2)
                            pagePresense = ActiveLights.checkHoneycombBulbIconPresense(self, nameActiveLight)
                            if pagePresense == True:
                                print("Page 1")
                                ActiveLights.clickBulbHoneycombBulbIcon(self, nameActiveLight)
                                self.report_step(
                                    "Android App : Clicked on the  " + nameActiveLight + " icon from Honeycomb Dashboard")
                                self.report_pass(
                                    "Android App : Navigated to " + nameActiveLight + " page successfully ")
                            elif pagePresense == False:
                                self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                                print("page going to scroll")
                                self.dashboardSwipe(False)
                                time.sleep(5)
                                print("page scrolled")
                                pagePresense = ActiveLights.checkHoneycombBulbIconPresense(self, nameActiveLight)
                                if pagePresense == True:
                                    print("Page 2")
                                    ActiveLights.clickBulbHoneycombBulbIcon(self, nameActiveLight)
                                    self.report_step(
                                        "Android App : Clicked on the  " + nameActiveLight + "icon from Honeycomb Dashboard")
                                    self.report_pass(
                                        "Android App : Navigated to " + nameActiveLight + " page successfully ")
                            elif pagePresense == False:
                                self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                                print("page going to scroll")
                                self.dashboardSwipe(False)
                                time.sleep(2)
                                print("page scrolled")
                                pagePresense = ActiveLights.checkHoneycombBulbIconPresense(self, nameActiveLight)
                                if pagePresense == True:
                                    print("Back to Page 1")
                                    ActiveLights.clickBulbHoneycombBulbIcon(self, nameActiveLight)
                                    self.report_step(
                                        "Android App : Clicked on the  " + nameActiveLight + "icon from Honeycomb Dashboard")
                                    self.report_pass(
                                        "Android App : Navigated to " + nameActiveLight + " page successfully ")
                    else:
                        self.report_fail("Android-App : Active Light not found")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_active_light_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Navigates to respective Bulb Ring ( Dimmer Ring or Tone Ring or Colour Ring)
    def navigateToSettings(self, Settings):
        if self.reporter.ActionStatus:
            try:
                if ("WARM WHITE LIGHT" in ActiveLights.BULB_TYPE) & ("brightness" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.WHITE_BULB_DIMMER_RING):
                        print("White Bulb 'Dimmer Ring' is visible")
                    else:
                        self.report_fail('Android App : Warm White Bulb Dimmer Ring was not displayed')

                elif ("TUNEABLE LIGHT" in ActiveLights.BULB_TYPE) & ("brightness" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.TUNEABLE_BULB_DIMMER_RING):
                        print("Tuneable Bulb 'Dimmer Ring' is visible")
                    elif self.wait_for_element_exist(*LightBulbLocators.TUNEABLE_BULB_DIMMER_BUTTON):
                        self.driver.find_element(*LightBulbLocators.TUNEABLE_BULB_DIMMER_BUTTON).click()
                        print("Tuneable Bulb 'Dimmer Ring' was not visible , hence clicked dimmer button")
                    elif self.wait_for_element_exist(*LightBulbLocators.TUNEABLE_BULB_DIMMER_RING):
                        print("Tuneable Bulb 'Dimmer Ring' is visible")
                    else:
                        self.report_fail('Android App : Tuneable Bulb Dimmer Ring was not displayed')

                elif ("TUNEABLE LIGHT" in ActiveLights.BULB_TYPE) & ("tone" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.TUNEABLE_BULB_TONE_RING):
                        print("Tuneable Bulb 'Tone Ring' is visible")
                    elif self.wait_for_element_exist(*LightBulbLocators.TUNEABLE_BULB_TONE_BUTTON):
                        print("Tuneable Bulb 'Tone Ring' was not visible , hence clicked tone button")
                        self.driver.find_element(*LightBulbLocators.TUNEABLE_BULB_TONE_BUTTON).click()
                    elif self.wait_for_element_exist(*LightBulbLocators.TUNEABLE_BULB_TONE_RING):
                        print("Tuneable Bulb 'Tone Ring' is visible")
                    else:
                        self.report_fail('Android App : Tuneable Bulb Tone Ring was not displayed')

                elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("brightness" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_DIMMER_RING):
                        print("Colour Bulb 'Dimmer Ring' is visible")
                    elif self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_DIMMER_BUTTON):
                        self.driver.find_element(*LightBulbLocators.COLOUR_BULB_DIMMER_BUTTON).click()
                        print("Colour Bulb 'Dimmer Ring' was not visible , hence clicked dimmer button")
                    else:
                        self.report_fail('Android App : Colour Bulb Dimmer Ring was not displayed')

                elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("tone" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_TONE_RING):
                        print("Colour Bulb 'Tone Ring' is visible")
                    elif self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_COLOUR_BUTTON):
                        self.driver.find_element(*LightBulbLocators.COLOUR_BULB_COLOUR_BUTTON).click()
                        self.driver.find_element(*LightBulbLocators.COLOUR_BULB_TONE_BUTTON).click()
                        print("Colour Bulb 'Tone Ring' was not visible , hence clicked colour and tone buttons")
                    elif self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_TONE_BUTTON):
                        self.driver.find_element(*LightBulbLocators.COLOUR_BULB_TONE_BUTTON).click()
                        print("Colour Bulb 'Tone Ring' was not visible , hence clicked tone button")
                    elif self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_TONE_RING):
                        print("Colour Bulb 'Tone Ring' is visible")
                    else:
                        self.report_fail('Android App : Colour Bulb Tone Ring was not displayed')

                elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("colour" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_COLOUR_RING):
                        print("Colour Bulb 'Colour Ring' is visible")
                    elif self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_COLOUR_BUTTON):
                        self.driver.find_element(*LightBulbLocators.COLOUR_BULB_COLOUR_BUTTON).click()
                        print("Colour Bulb 'Colour Ring' was not visible , hence clicked colour button")
                    elif self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_TONE_BUTTON):
                        self.driver.find_element(*LightBulbLocators.COLOUR_BULB_TONE_BUTTON).click()
                        self.driver.find_element(*LightBulbLocators.COLOUR_BULB_COLOUR_BUTTON).click()
                        print("Colour Bulb 'Colour Ring' was not visible , hence clicked tone and colour button")
                    elif self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_COLOUR_BUTTON):
                        self.driver.find_element(*LightBulbLocators.COLOUR_BULB_COLOUR_BUTTON).click()
                        print("Colour Bulb 'Colour Ring' was not visible , hence clicked colour button")
                    else:
                        self.report_fail('Android App : Colour Bulb Color Ring was not displayed')
            except:
                self.report_fail('Android App : NoSuchElementException: in navigateToSettings Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Sets the bulb value to the expected values by swiping the bulb ring UI
    def setValueForBulb(self, Settings, verifyValue):
        if self.reporter.ActionStatus:
            try:
                ActiveLights.makeLightOnOff(self, 'ON')
                angleStep = 0
                oBulb = None
                if ("WARM WHITE LIGHT" in ActiveLights.BULB_TYPE) & ("brightness" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.WHITE_BULB_DIMMER_RING):
                        oBulb = self.driver.find_element(*LightBulbLocators.WHITE_BULB_DIMMER_RING)
                        ActiveLights.makeLightOnOff(self, 'ON')
                        angleStep = 18
                    else:
                        self.report_fail('Android App : White Light Brightness settings was not displayed')
                elif ("TUNEABLE LIGHT" in ActiveLights.BULB_TYPE) & ("brightness" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.TUNEABLE_BULB_DIMMER_RING):
                        oBulb = self.driver.find_element(*LightBulbLocators.TUNEABLE_BULB_DIMMER_RING)
                        ActiveLights.makeLightOnOff(self, 'ON')
                        angleStep = 18
                    else:
                        self.report_fail('Android App : Tuneable Light Brightness settings was not displayed')
                elif ("TUNEABLE LIGHT" in ActiveLights.BULB_TYPE) & ("tone" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.TUNEABLE_BULB_TONE_RING):
                        oBulb = self.driver.find_element(*LightBulbLocators.TUNEABLE_BULB_TONE_RING)
                        ActiveLights.makeLightOnOff(self, 'ON')
                        angleStep = 27
                    else:
                        self.report_fail('Android App : Tuneable Light Tone settings was not displayed')
                elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("brightness" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_DIMMER_RING):
                        oBulb = self.driver.find_element(*LightBulbLocators.COLOUR_BULB_DIMMER_RING)
                        ActiveLights.makeLightOnOff(self, 'ON')
                        angleStep = 15
                    else:
                        self.report_fail('Android App : Colour Light Brightness settings was not displayed')
                elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("tone" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_TONE_RING):
                        oBulb = self.driver.find_element(*LightBulbLocators.COLOUR_BULB_TONE_RING)
                        ActiveLights.makeLightOnOff(self, 'ON')
                        angleStep = 20
                    else:
                        self.report_fail('Android App : Colour Light Tone settings was not displayed')
                elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("colour" in Settings):
                    if self.wait_for_element_exist(*LightBulbLocators.COLOUR_BULB_COLOUR_RING):
                        oBulb = self.driver.find_element(*LightBulbLocators.COLOUR_BULB_COLOUR_RING)
                        if verifyValue == 'Red Orange':
                            angleStep = 5
                        else:
                            angleStep = 8
                    else:
                        self.report_fail('Android App : Colour Light Colour settings was not displayed')

                currentValue = ActiveLights.getLightCurrentValue(self)
                if currentValue.upper() == "OFF":
                    ActiveLights.makeLightOnOff(self, 'ON')
                self.report_step(
                    ActiveLights.BULB_TYPE + "'s" + " current " + ActiveLights.SETTINGS_LOCAL + " is " + str(
                        currentValue))

                # Bulb Ring swiping logic starts here
                intLeftX = oBulb.location['x']
                intUpperY = oBulb.location['y']
                intSide = oBulb.size['width']
                intSideT = (intSide / 2)
                intCenterX = intLeftX + intSideT
                intCenterY = intUpperY + intSideT

                # Calculate Radius for other screen sizes
                intRadius = intCenterX - 160
                intTempStartX = intCenterX + intRadius * math.cos(180)
                intTempStartY = intCenterY + intRadius * math.sin(180)

                for angle in range(165, 375, angleStep):
                    intTempNewStartX = intCenterX + intRadius * math.cos(angle * math.pi / 180)
                    intTempNewStartY = intCenterY + intRadius * math.sin(angle * math.pi / 180)
                    intTempNewStartX = int(intTempNewStartX)
                    intTempNewStartY = int(intTempNewStartY)
                    self.driver.swipe(intTempStartX, intTempStartY, intTempNewStartX, intTempNewStartY)
                    time.sleep(5)

                    currentValue = ActiveLights.getLightCurrentValue(self)
                    if (str(verifyValue)) == currentValue:
                        print(
                            "Android App : Your favourite " + Settings + " " + "'" + currentValue + "'" + " is set now" + "\n")
                        self.report_pass(ActiveLights.BULB_TYPE + "'s " + Settings + " is set to " + currentValue)
                        break

                    intTempStartX = intTempNewStartX
                    intTempStartY = intTempNewStartY
                    print(
                        "Bulb Type is" + "  " + "'" + ActiveLights.BULB_TYPE + "'" + "  Bulb" + "  ,  " + 'Need to set ' + "'" + str(
                            verifyValue) + "'" + " as " + Settings + "    but    " + 'Current' + "  is  " + str(
                            currentValue) + " ... " + "swiping again")
            except:
                self.report_fail('Android App : NoSuchElementException: in setValueForBulb Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Gets Light current value from UI
    def getLightCurrentValue(self):

        if ("WARM WHITE LIGHT" in ActiveLights.BULB_TYPE.upper()) & (
                    "BRIGHTNESS" in ActiveLights.SETTINGS_LOCAL.upper()):
            currentValue = self.driver.find_element(*LightBulbLocators.WARM_DIMMER_CURRENT_VALUE).get_attribute('text')
            currentValue = currentValue.replace("%", "")
            currentValue = currentValue.replace("On ", "")
            return currentValue

        elif ("TUNEABLE LIGHT" in ActiveLights.BULB_TYPE) & ("brightness" in ActiveLights.SETTINGS_LOCAL):
            currentValue = self.driver.find_element(*LightBulbLocators.TUNEABLE_DIMMER_CURRENT_VALUE).get_attribute(
                'text')
            currentValue = currentValue.replace("%", "")
            currentValue = currentValue.replace("On ", "")
            return currentValue

        elif ("TUNEABLE LIGHT" in ActiveLights.BULB_TYPE) & ("tone" in ActiveLights.SETTINGS_LOCAL):
            currentValue = self.driver.find_element(*LightBulbLocators.TUNEABLE_TONE_CURRENT_VALUE).get_attribute(
                'text')
            return currentValue

        elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("brightness" in ActiveLights.SETTINGS_LOCAL):
            currentValue = self.driver.find_element(*LightBulbLocators.COLOUR_DIMMER_CURRENT_VALUE).get_attribute(
                'text')
            currentValue = currentValue.replace("%", "")
            currentValue = currentValue.replace("On ", "")
            return currentValue

        elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("tone" in ActiveLights.SETTINGS_LOCAL):
            currentValue = self.driver.find_element(*LightBulbLocators.COLOUR_TONE_CURRENT_VALUE).get_attribute('text')
            return currentValue

        elif ("COLOUR LIGHT" in ActiveLights.BULB_TYPE) & ("colour" in ActiveLights.SETTINGS_LOCAL):
            currentValue = self.driver.find_element(*LightBulbLocators.COLOUR_COLOUR_CURRENT_VALUE).get_attribute(
                'text')
            return currentValue

    # Verifies the Bulbs value in the API
    def verifyLightAPI(self):
        if self.reporter.ActionStatus:
            try:
                attributeVerify = ""
                attributeName = ""
                if "tone" in ActiveLights.SETTINGS_LOCAL:
                    attributeVerify = "colourTemperature"
                    attributeName = "reportedValue"
                elif "colour" in ActiveLights.SETTINGS_LOCAL:
                    attributeVerify = "hsvHue"
                    attributeName = "targetValue"
                elif "brightness" in ActiveLights.SETTINGS_LOCAL:
                    attributeVerify = "brightness"
                    attributeName = "reportedValue"

                # Getting vlaues from API call
                nodeID = pUtils.getDeviceNodeID(ActiveLights.BULB_MODEL)
                attributeValue = pUtils.getColourBulbValues(nodeID, attributeVerify, attributeName)
                attributeValue = int(attributeValue)

                # Asserting the values in API
                if attributeValue != "":

                    # Asserting the Tone values in API
                    if "tone" in ActiveLights.SETTINGS_LOCAL:
                        if "coolest white" in ActiveLights.VALUE_LOCAL:
                            if attributeValue >= 5471 & attributeValue <= 6535:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for tone ' + attributeValue + 'for given tone' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif "cool white" in ActiveLights.VALUE_LOCAL:
                            if attributeValue >= 4981 & attributeValue <= 5740:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for tone ' + attributeValue + 'for given tone' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif "mid white" in ActiveLights.VALUE_LOCAL:
                            if attributeValue >= 4221 & attributeValue <= 4980:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for tone ' + attributeValue + 'for given tone' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif "warm white" in ActiveLights.VALUE_LOCAL:
                            if attributeValue >= 3461 & attributeValue <= 4220:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for tone ' + attributeValue + 'for given tone' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif "warmest white" in ActiveLights.VALUE_LOCAL:
                            if attributeValue >= 2700 & attributeValue <= 3460:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for tone ' + attributeValue + 'for given tone' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        else:
                            attributeValue = str(attributeValue)
                            self.report_fail(
                                'Android App : The value for tone is updated in the API as ' + attributeValue + ' for given tone ' + ActiveLights.VALUE_LOCAL)

                    # Asserting the Colour values in API
                    elif "colour" in ActiveLights.SETTINGS_LOCAL:
                        if ActiveLights.VALUE_LOCAL == "Red":
                            if attributeValue <= 6:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Red Orange":
                            if attributeValue >= 11 & attributeValue <= 20:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Orange":
                            if attributeValue >= 21 & attributeValue <= 40:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Orange Yellow":
                            if attributeValue >= 41 & attributeValue <= 50:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Yellow":
                            if attributeValue >= 51 & attributeValue <= 60:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Yellow Green":
                            if attributeValue >= 61 & attributeValue <= 80:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Green":
                            if attributeValue >= 81 & attributeValue <= 140:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Green Cyan":
                            if attributeValue >= 141 & attributeValue <= 169:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Cyan":
                            if attributeValue >= 170 & attributeValue <= 200:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ActiveLights.VALUE_LOCAL)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Cyan Blue":
                            if attributeValue >= 201 & attributeValue <= 220:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Blue":
                            if attributeValue >= 221 & attributeValue <= 240:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Blue Magenta":
                            if attributeValue >= 241 & attributeValue <= 280:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Magenta":
                            if attributeValue >= 281 & attributeValue <= 320:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Magenta Pink":
                            if attributeValue >= 321 & attributeValue <= 330:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Pink":
                            if attributeValue >= 331 & attributeValue <= 345:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')
                        elif ActiveLights.VALUE_LOCAL == "Pink Red":
                            if attributeValue >= 346 & attributeValue <= 355:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                            else:
                                self.report_fail(
                                    'Android App : The value for colour ' + attributeValue + 'for given colour' + ActiveLights.VALUE_LOCAL + 'is not matching')

                    # Asserting the Brightness values in API
                    elif "brightness" in ActiveLights.SETTINGS_LOCAL:
                        if int(ActiveLights.VALUE_LOCAL) == attributeValue:
                            attributeValue = str(attributeValue)
                            self.report_pass(
                                'Android App : The value for ' + ActiveLights.SETTINGS_LOCAL + '  is set in  API as  ' + attributeValue)
                        else:
                            attributeValue = str(attributeValue)
                            self.report_fail(
                                'Android App : The value for brightness ' + attributeValue + ' for given brightness ' + ActiveLights.VALUE_LOCAL + 'is not matching')
                else:
                    self.report_fail('Android App : API validation failed for ' + ActiveLights.SETTINGS_LOCAL)

            except:
                self.report_fail('Android App : NoSuchElementException: in verifyLightAPI Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_active_light_mode(self, modeValue):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingHomePageLocators.HEAT_CONTROL_TAB):
                    self.driver.find_element(*HeatingHomePageLocators.HEAT_CONTROL_TAB).click()
                    time.sleep(5)
                else:
                    self.report_fail('Problem in setting Light mode, control icon not found')
                print('Setting Mode for light')
                if self.wait_for_element_exist(*LightBulbLocators.MODE_TEXT):
                    if 'MANUAL' in modeValue:
                        if 'MANUAL' in self.driver.find_element(*LightBulbLocators.MODE_TEXT).get_attribute(
                                "text").upper():
                            self.report_pass('MANUAL mode is already selected')
                        else:
                            self.driver.find_element(*LightBulbLocators.MODE_RIGHT_ARROW).click()
                            time.sleep(2)
                    elif 'SCHEDULE' in modeValue:
                        if 'SCHEDULE' in self.driver.find_element(*LightBulbLocators.MODE_TEXT).get_attribute(
                                "text").upper():
                            self.report_pass('SCHEDULE mode is already selected')
                        else:
                            self.driver.find_element(*LightBulbLocators.MODE_RIGHT_ARROW).click()
                            time.sleep(2)
                else:
                    self.report_fail('Problem in setting Light mode')

            except:
                self.report_fail('Android App : NoSuchElementException: in set_active_light_mode Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Gets Light current value from UI
    def makeLightOnOff(self, setValue):
        currentValue = ActiveLights.getLightCurrentValue(self)

        if "ON" in setValue.upper():
            tempValue = "%"
        else:
            tempValue = "OFF"

        if not tempValue.upper() in currentValue.upper():
            if "WARM WHITE LIGHT" in ActiveLights.BULB_TYPE:
                self.driver.find_element(*LightBulbLocators.WARM_DIMMER_CURRENT_VALUE).click()
            elif "TUNEABLE LIGHT" in ActiveLights.BULB_TYPE:
                self.driver.find_element(*LightBulbLocators.TUNEABLE_TONE_CURRENT_VALUE).click()
            elif "COLOUR LIGHT" in ActiveLights.BULB_TYPE:
                self.driver.find_element(*LightBulbLocators.COLOUR_COLOUR_CURRENT_VALUE).click()

    # Navigate to light schedule page
    def naviagate_active_light_schedule(self):
        if self.reporter.ActionStatus:
            try:
                self.wait_for_element_exist(*self.REFRESH_BUTTON)
                time.sleep(7)
                if self.wait_for_element_exist(*LightBulbLocators.SCHEDULE_TAB_ICON):
                    self.driver.find_element(*LightBulbLocators.SCHEDULE_TAB_ICON).click()
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in naviagate_active_light_schedule Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

                # Sets the schedule passed from the feature file for the particular light on the app

    def setActiveLightSchedule(self, strDeviceType, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                blnFlagFormat = False
                self.report_pass("Setting " + strDeviceType + " Schedule now")
                strTone = 'null'
                strColour = 'null'
                if self.wait_for_element_exist(*LightBulbLocators.SCHEDULE_TAB_ICON):
                    self.driver.find_element(*LightBulbLocators.SCHEDULE_TAB_ICON).click()
                    time.sleep(3)
                lstAMelements = self.driver.find_elements(*EditTimeSlotPageLocators.EDIT_TIMESLOT_AM_FORMAT)
                if len(lstAMelements) > 0: blnFlagFormat = True
                if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL) and self.wait_for_element_exist(
                        *self.REFRESH_BUTTON):
                    for oKey in oScheduleDict.keys():
                        self._navigate_to_day(oKey)
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        # Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                        intCurrentEventCount = len(lstStartTime)

                        if self.reporter.platformVersion == 'V6':
                            self.add_or_remove_events(len(oScheduleList))
                        else:
                            if len(oScheduleList) > 4:
                                if not intCurrentEventCount == 6:
                                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_SPINNER_MENU):
                                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()
                                    else:
                                        self.report_fail('Element SCHEDULE_SPINNER_MENU is not found')
                                    if self.wait_for_element_exist(*SchedulePageLocators.SIX_EVENT_SUBMENU):
                                        self.driver.find_element(*SchedulePageLocators.SIX_EVENT_SUBMENU).click()
                                    else:
                                        self.report_fail('Element SIX_EVENT_SUBMENU is not found')
                            else:
                                if not intCurrentEventCount == 4:
                                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_SPINNER_MENU):
                                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()
                                    else:
                                        self.report_fail('Element SCHEDULE_SPINNER_MENU is not found')
                                    if self.wait_for_element_exist(*SchedulePageLocators.FOUR_EVENT_SUBMENU):
                                        self.driver.find_element(*SchedulePageLocators.FOUR_EVENT_SUBMENU).click()
                                    else:
                                        self.report_fail('Element FOUR_EVENT_SUBMENU is not found')

                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                        for intCntr in range((len(lstStartTime) - 1), -1, -1):

                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetState = oScheduleList[intCntr][1]
                            strBrightness = str(oScheduleList[intCntr][2])
                            if 'TUNEABLE LIGHT' in strDeviceType.upper():
                                strTone = str(oScheduleList[intCntr][3])
                            if 'COLOUR LIGHT' in strDeviceType.upper():
                                strColour = str(oScheduleList[intCntr][3])

                            intCntrIter = 0
                            strCurrentStartTIme = ''
                            if blnFlagFormat:
                                strSetToTime = str(int(strSetStartTime.split(':')[0]) % 12) + ":" + \
                                               strSetStartTime.split(':')[1]
                            else:
                                strSetToTime = strSetStartTime
                            while (strCurrentStartTIme != strSetToTime) and (intCntrIter < 3):
                                lstStartTime[intCntr].click()

                                # Sets the On/Off status
                                if 'WARM WHITE LIGHT' in strDeviceType.upper():
                                    if self.wait_for_element_exist(
                                            *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_WARM_WHITE):
                                        if self.driver.find_element(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_WARM_WHITE).get_attribute(
                                            'name').find('ON') >= 0:
                                            strCurrentState = 'ON'
                                        else:
                                            strCurrentState = 'OFF'

                                        if fltSetState != strCurrentState:
                                            self.driver.find_element(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_WARM_WHITE).click()
                                    else:
                                        self.report_fail("EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_WARM_WHITE is not found")
                                elif 'TUNEABLE LIGHT' in strDeviceType.upper():
                                    if self.wait_for_element_exist(
                                            *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_TUNEABLE):
                                        if self.driver.find_element(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_TUNEABLE).get_attribute(
                                            'name').find('ON') >= 0:
                                            strCurrentState = 'ON'
                                        else:
                                            strCurrentState = 'OFF'

                                        if fltSetState != strCurrentState:
                                            self.driver.find_element(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_TUNEABLE).click()
                                    else:
                                        self.report_fail("EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_TUNEABLE is not found")
                                elif 'COLOUR LIGHT' in strDeviceType.upper():
                                    if self.wait_for_element_exist(
                                            *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_COLOUR):
                                        if self.driver.find_element(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_COLOUR).get_attribute(
                                            'name').find('ON') >= 0:
                                            strCurrentState = 'ON'
                                        else:
                                            strCurrentState = 'OFF'

                                        if fltSetState != strCurrentState:
                                            self.driver.find_element(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_COLOUR).click()
                                    else:
                                        self.report_fail("EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_COLOUR is not found")

                                # Setting seekbar values for active light
                                # Sets the Dimming value
                                if 'ON' in fltSetState:
                                    if strBrightness != 'null':
                                        if self.wait_for_element_exist(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR):
                                            ActiveLights.set_brightness_on_edit_timeslot_page(self, strBrightness)
                                        else:
                                            self.report_fail("Problem in setting brightnessValue")
                                    if strTone != 'null':
                                        if self.wait_for_element_exist(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR):
                                            ActiveLights.set_tone_on_edit_timeslot_page(self, strTone)
                                        else:
                                            self.report_fail("Problem in setting ToneValue")
                                    if strColour != 'null':
                                        if self.wait_for_element_exist(
                                                *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR):
                                            ActiveLights.set_colour_on_edit_timeslot_page(self, strColour)
                                        else:
                                            self.report_fail("Problem in setting colourValue")
                                else:
                                    self.report_pass(
                                        'No need to set brightness as Light status value for timeslot is OFF')

                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.HOUR_SCROLL):
                                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                                    strCurrentHour = oScrolElement.find_element(
                                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute('name')
                                    strCurrentHour = ('0' + strCurrentHour)[-2:]
                                else:
                                    self.report_fail('Element HOUR_SCROLL is not found')
                                    exit()
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                                    strCurrentMinute = oScrolElement.find_element(
                                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute('name')
                                else:
                                    self.report_fail('Element MINUTE_SCROLL is not found')
                                    exit()
                                strCurrentTime = strCurrentHour + ':' + strCurrentMinute
                                self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                                self.set_schedule_event_minute(strSetStartTime.split(':')[1])

                                intCntrIter = intCntrIter + 1
                                strLog = "Event Number $$Before Change$$After Change @@@" + str(
                                    intCntr + 1) + "$$" + strCurrentTime + "$$" + strSetStartTime
                                self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.SAVE_BUTTON):
                                    self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                                    time.sleep(2)
                                else:
                                    self.report_fail(' SAVE_BUTTON is not found')
                                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                                    time.sleep(2)
                                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                                else:
                                    self.report_fail('REFRESH_BUTTON is not found')

                                strCurrentStartTIme = lstStartTime[intCntr].get_attribute('text')
                            self.report_pass('Main Screen after Event number : ' + str(intCntr + 1) + ' is changed')
                        self.reporter.HTML_TC_BusFlowKeyword_Initialize('All Events Updated')
                        self.report_pass('Main Screen after all Events are changed')
                else:
                    self.report_fail("Control not active on the Light Schedule Page to set the Plug Schedule")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_active_light_schedule Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Add a time slot for schedule
    def add_light_schedule(self, context, strDeviceType):
        strBrightness, strSecondoryAttribute = "", ""
        strSetStartTime = str((list(context.oAddSchedule[context.strDay]))[0][0])
        strSetState = str((list(context.oAddSchedule[context.strDay]))[0][1])

        if 'WARM WHITE LIGHT' in strDeviceType.upper():
            objSwitch = EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_WARM_WHITE
        elif 'TUNEABLE LIGHT' in strDeviceType.upper():
            objSwitch = EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_TUNEABLE
        elif 'COLOUR LIGHT' in strDeviceType.upper():
            objSwitch = EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_COLOUR
        if self.reporter.ActionStatus:
            try:
                self._navigate_to_day(context.strDay)
                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                    time.sleep(2)
                    self.report_done("Add Icon is found and clicked sucessfully")
                else:
                    self.report_fail("Add Icon is not found on schedule screen, Exit condition")
                    exit()
                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_ADDTIMESLOT_TEXTVIEW):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_ADDTIMESLOT_TEXTVIEW).click()
                    time.sleep(2)
                    self.report_done("Add schedule Icon is found and clicked sucessfully")
                    self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                    self.set_schedule_event_minute(strSetStartTime.split(':')[1])

                    strLog = ""

                    if self.wait_for_element_exist(*objSwitch):
                        if self.driver.find_element(*objSwitch).get_attribute(
                                'name').find('ON') >= 0:
                            strCurrentState = 'ON'
                        else:
                            strCurrentState = 'OFF'

                        if strSetState != strCurrentState:
                            self.driver.find_element(*objSwitch).click()
                            time.sleep(2)

                        strLog = "Slot Start Time $$ State@@@" + \
                                 strSetStartTime + "$$" + strSetState
                    else:
                        self.report_fail(str(objSwitch) + " is not found")

                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Below Time Slot is added')
                    self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                else:
                    self.report_fail("Add schedule is not found on schedule screen, Exit condition")
                    exit()

                if 'ON' in strSetState:
                    strBrightness = str((list(context.oAddSchedule[context.strDay]))[0][2])
                    if len(list(context.oAddSchedule[context.strDay])[0]) > 3:
                        strSecondoryAttribute = str((list(context.oAddSchedule[context.strDay]))[0][3])
                    if strBrightness != "":
                        if self.wait_for_element_exist(*EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR):
                            ActiveLights.set_brightness_on_edit_timeslot_page(self, strBrightness)
                        else:
                            self.report_fail("Problem in setting brightnessValue")
                    if strSecondoryAttribute != "":
                        if self.wait_for_element_exist(*EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR):
                            ActiveLights.set_tone_on_edit_timeslot_page(self, strSecondoryAttribute)
                        else:
                            self.report_fail("Problem in setting ToneValue")
                else:
                    self.report_pass('No need to set brightness as Light status value for timeslot is OFF')

                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON).click()
                    time.sleep(3)
                    self.report_done("Save OK Button is found and clicked sucessfully")
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(3)
                elif self.wait_for_element_exist(*EditTimeSlotPageLocators.CANCEL_BUTTON):
                    self.driver.find_element(*EditTimeSlotPageLocators.CANCEL_BUTTON).click()
                    time.sleep(2)
                    self.report_fail("refresh button is not found, existing the scenario")
                else:
                    self.report_fail("Save OK Button is not found on schedule screen, Exit condition")
                    exit()
            except:
                self.report_fail('Android-App : NoSuchElementException: in add_light_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_brightness_on_edit_timeslot_page(self, brightnessValue):
        if self.reporter.ActionStatus:
            try:
                currentBrightness = self.driver.find_element(
                    *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR).get_attribute('name')

                if str(brightnessValue) == str(currentBrightness):
                    self.report_pass("Brightness value already as needed " + brightnessValue)
                elif str(brightnessValue) != str(currentBrightness):
                    seek_bar = self.driver.find_element(*EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR)
                    intX = seek_bar.location['x']
                    intY = seek_bar.location['y']
                    intWidth = seek_bar.size['width']

                    if int(brightnessValue) == 5:
                        intTargetValue = 0
                    else:
                        intTargetValue = int(brightnessValue) / 10
                    if intTargetValue == 10:
                        intClickCordinateX = intWidth + intX - 10
                    elif intTargetValue > 5:
                        intClickCordinateX = intWidth + intX - int(round(((10 - intTargetValue) * intWidth) / 11))
                    else:
                        intClickCordinateX = intX + int(round((intTargetValue * intWidth) / 11))

                    print("Setting " + brightnessValue)
                    positions = [(intClickCordinateX, intY)]
                    self.driver.tap(positions)
                    currentBrightness = self.driver.find_element(
                        *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR).get_attribute('name')
                    if (str(brightnessValue) == str(currentBrightness)) or ((str(brightnessValue) == '5') and (
                                    str(currentBrightness) == '' or str(currentBrightness) == '5')):
                        self.report_pass("Brightness value set as needed " + brightnessValue)
                    else:
                        self.report_fail("Problem in setting " + brightnessValue)
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_brightness_on_edit_timeslot_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def set_tone_on_edit_timeslot_page(self, toneValue):
        if self.reporter.ActionStatus:
            try:

                seek_bar = self.driver.find_element(*EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_TONE_SEEKBAR)
                intX = seek_bar.location['x']
                intY = seek_bar.location['y']
                intWidth = seek_bar.size['width']
                offset = round(intWidth / 5)

                print("Setting " + toneValue)

                if 'COOLEST WHITE' == toneValue:
                    x = intX
                elif 'COOL WHITE' == toneValue:
                    x = intX + (2 * offset)
                elif 'MID WHITE' == toneValue:
                    x = intX + (2.5 * offset)
                elif 'WARM WHITE' == toneValue:
                    x = intX + (3.5 * offset)
                elif 'WARMEST WHITE' == toneValue:
                    x = intX + (4.5 * offset)

                positions = [(x, intY)]
                self.driver.tap(positions)
                currentTone = self.driver.find_element(
                    *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_TONE_SEEKBAR).get_attribute('name').upper()
                if toneValue in currentTone:
                    self.report_pass("Tone value set to " + toneValue)
                else:
                    self.report_fail("Problem in setting Tone to " + toneValue)
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_tone_on_edit_timeslot_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def set_colour_on_edit_timeslot_page(self, colourValue):
        if self.reporter.ActionStatus:
            try:

                seek_bar = self.driver.find_element(*EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_COLOUR_SEEKBAR)
                intX = seek_bar.location['x']
                intY = seek_bar.location['y']
                intWidth = seek_bar.size['width']
                offset = round(intWidth / 16)

                if 'RED' == colourValue:
                    x = intX
                elif 'RED ORANGE' == colourValue:
                    x = intX + (1 * offset)
                elif 'ORANGE' == colourValue:
                    x = intX + (2 * offset)
                elif 'ORANGE YELLOW' == colourValue:
                    x = intX + (3 * offset)
                elif 'YELLOW' == colourValue:
                    x = intX + (4 * offset)
                elif 'YELLOW GREEN' == colourValue:
                    x = intX + (5 * offset)
                elif 'GREEN' == colourValue:
                    x = intX + (6 * offset)
                elif 'GREEN CYAN' == colourValue:
                    x = intX + (7 * offset)
                elif 'CYAN' == colourValue:
                    x = intX + (8 * offset)
                elif 'CYAN BLUE' in colourValue:
                    x = intX + (9 * offset)
                elif 'BLUE' in colourValue:
                    x = intX + (10 * offset)
                elif 'BLUE MAGENTA' in colourValue:
                    x = intX + (11 * offset)
                elif 'MAGENTA' in colourValue:
                    x = intX + (12 * offset)
                elif 'MAGENTA PINK' in colourValue:
                    x = intX + (13 * offset)
                elif 'PINK' in colourValue:
                    x = intX + (14 * offset)
                elif 'PINK RED' in colourValue:
                    x = intX + (15 * offset)

                print("Arrow co-ordinates are : ", x, intY)
                print("Setting Colour as " + colourValue + " now")
                positions = [(x, intY)]
                self.driver.tap(positions)
                currentColour = self.driver.find_element(
                    *EditTimeSlotPageLocators.EDIT_TIMESLOT_PAGE_TONE_SEEKBAR).get_attribute('name')
                if colourValue in currentColour:
                    self.report_pass("Colour value set to " + colourValue)
                    print("Set " + currentColour)
                else:
                    self.report_fail("Problem in setting Colour to " + colourValue)
                    print("Need to set" + colourValue + " but current is " + currentColour)
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_colour_on_edit_timeslot_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


class PlugsPage(BasePage):
    beforeoffmode = ""
    afteroffmode = ""
    beforeonmode = ""
    afteronmode = ""
    currentstate = ""
    afterstate = ""
    finalstate = ""

    # check Plug model and status in APi
    def set_up(self, PlugName, ModelNo):
        nodes = pUtils.getNodes()
        count = 0
        plug = False
        presence = False
        for oNode in nodes['nodes']:
            if oNode['name'].upper() == PlugName.upper():
                count = count + 1
            if 'nodeType' in oNode and 'attributes' in oNode:
                if '.json' in oNode["nodeType"] and "model" in oNode["attributes"] and "presence" in oNode[
                    "attributes"]:
                    if oNode["attributes"]["model"]["reportedValue"].upper()[:4] == ModelNo.upper():
                        if oNode['name'].upper() == PlugName.upper():
                            Plug = True
                            if oNode["attributes"]["presence"]["reportedValue"].upper() == 'PRESENT':
                                presence = True
        if count != 1:
            if count > 1:
                self.report_fail('Kit has more devices with same mentioned PluName- ' + PlugName)
            else:
                self.report_fail('Kit has no device with mentioned PluName- ' + PlugName)
        else:
            if Plug == True and presence == True:
                self.report_pass('Plug is available and online in Kit')
            elif Plug == True and presence == False:
                self.report_fail('Plug is available in Kit but it is offline')
            else:
                self.report_fail('Plug is not available in the Kit with the mentioned PlugName- ' + PlugName)

    # navigation to the plug page from dashboard
    def navigation_to_plugpage(self, PlugName):

        Plug_Dashboard = str(HomePageLocators.Plug_runtime_Dashboard)
        Plug_Dashboard = Plug_Dashboard.replace("devicename", PlugName)
        if 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(By.XPATH, Plug_Dashboard):
                if PlugName.upper() in self.driver.find_element(By.XPATH, Plug_Dashboard).get_attribute(
                        'name').upper():
                    self.driver.find_element(By.XPATH, Plug_Dashboard).click()
                    self.report_pass('Plug is found in Dashboard and clicked')
                else:
                    self.report_fail('plugName and Locators are not matched')
            else:

                self.dashboardSwipe(False)
                if self.wait_for_element_exist(By.XPATH, Plug_Dashboard):
                    if PlugName.upper() in self.driver.find_element(By.XPATH, Plug_Dashboard).get_attribute(
                            'name').upper():
                        self.driver.find_element(By.XPATH, Plug_Dashboard).click()
                        self.report_pass('Plug is found in Dashboard and clicked')
                    else:
                        self.report_fail('plugName and Locators are not matched')
                else:
                    self.report_fail('Plug is not found in Dashboard')
        else:
            if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                time.sleep(2)
                if self.wait_for_element_exist(By.XPATH, Plug_Dashboard):
                    if PlugName.upper() in self.driver.find_element(By.XPATH, Plug_Dashboard).get_attribute(
                            'name').upper():
                        self.driver.find_element(By.XPATH, Plug_Dashboard).click()
                        self.report_pass('Plug is found in Dashboard and clicked')
                    else:
                        self.report_fail('plugName and Locators are not matched')
                else:

                    self.dashboardSwipe(False)
                    if self.wait_for_element_exist(By.XPATH, Plug_Dashboard):
                        if PlugName.upper() in self.driver.find_element(By.XPATH, Plug_Dashboard).get_attribute(
                                'name').upper():
                            self.driver.find_element(By.XPATH, Plug_Dashboard).click()
                            self.report_pass('Plug is found in Dashboard and clicked')
                        else:
                            self.report_fail('plugName and Locators are not matched')
                    else:
                        self.report_fail('Plug is not found in Dashboard')

            else:
                self.report_fail('User is not inside the app')

    # function to verify the plugs screen title
    def verify_plugstitle(self, PlugName):
        if PlugName.upper() in self.driver.find_element(*PlugLocators.PLUG_TITLE).get_attribute('name').upper():
            self.report_pass('PlugTitle is same as name which user have given -' + PlugName)
        else:
            if not 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute(
                    'name').upper():
                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                    PlugsPage.navigation_to_plugpage(self, PlugName)
                    if PlugName.upper() in self.driver.find_element(*PlugLocators.PLUG_TITLE).get_attribute(
                            'name').upper():
                        self.report_pass('PlugTitle is same as name which user have given -' + PlugName)
                    else:
                        self.report_fail('PlugTitle and Plugname are not same.')
                else:
                    self.report_fail('User is not inside the app')
            else:
                PlugsPage.navigation_to_plugpage(self, PlugName)
                if PlugName.upper() in self.driver.find_element(*PlugLocators.PLUG_TITLE).get_attribute('name').upper():
                    self.report_pass('PlugTitle is same as name which user have given -' + PlugName)
                else:
                    self.report_fail('PlugTitle and Plugname are not same.')

    # function to set the plug state
    def set_state(self, strState):
        if self.reporter.ActionStatus:
            try:
                strText = ""
                if self.wait_for_element_exist(*PlugLocators.PLUG_STATUS):
                    strText = self.driver.find_element(*PlugLocators.PLUG_STATUS).get_attribute("text")
                    self.report_pass('Plug control is located')
                if not strText.upper() == strState.upper():
                    self.driver.find_element(*PlugLocators.PLUG_STATUS).click()
                    time.sleep(3)
                    self.report_done('Plug Control is clicked')
                    if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                        self.driver.find_element(*self.REFRESH_BUTTON).click()
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
            except:
                self.report_fail('Android-App : NoSuchElementException: in set_state Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # function to change the plug state
    def click_plugs_toggle(self, PlugName):
        apimode = self.verify_plugstate_api(PlugName)
        if self.wait_for_element_exist(*PlugLocators.PLUG_OFF_TEXT):
            self.report_pass('Toggle Button is found')
            if apimode == "OFF":
                self.report_pass('Plug is currently in OFF state in both api and app.')
            elif apimode == "ON":
                self.report_fail('Plug is currently in ON state in api but off in app.')
            else:
                self.report_fail('Not able to get the Plug state from api.')

            self.driver.find_element(*PlugLocators.PLUG_OFF_TEXT).click()
            self.report_done('Toggle Button for changing Plugs state is clicked')
            PlugsPage.beforeoffmode = "off"
            if self.wait_for_element_exist(*PlugLocators.PLUG_ON_TEXT):
                PlugsPage.afteroffmode = "on"
        elif self.wait_for_element_exist(*PlugLocators.PLUG_ON_TEXT):
            self.report_pass('Toggle Button is found')
            if apimode == "OFF":
                self.report_fail('Plug is currently in OFF state in api but ON in app.')
            elif apimode == "ON":
                self.report_pass('Plug is currently in ON state in both api and app.')
            else:
                self.report_fail('Not able to get the Plug state from api.')
            self.driver.find_element(*PlugLocators.PLUG_ON_TEXT).click()
            self.report_done('Toggle Button for changing Plugs state is clicked')
            PlugsPage.beforeonmode = "on"
            if self.wait_for_element_exist(*PlugLocators.PLUG_OFF_TEXT):
                PlugsPage.afteronmode = "off"
        else:
            self.report_fail('Toggle button not found.')

    # function to verify the state of the plugs
    def verify_plugs_on_off(self, PlugName):
        apimode = self.verify_plugstate_api(PlugName)
        if PlugsPage.beforeoffmode == "off" and PlugsPage.afteroffmode == "on":
            if apimode == "OFF":
                self.report_fail('Plug is currently in OFF state in api but ON in app.')
            elif apimode == "ON":
                PlugsPage.finalstate = "ON"
                self.report_pass('Plug is changed to ON state in both api and app.')
            else:
                self.report_fail('Not able to get the Plug state from api.')
        elif PlugsPage.beforeonmode == "on" and PlugsPage.afteronmode == "off":
            if apimode == "OFF":
                PlugsPage.finalstate = "OFF"
                self.report_pass('Plug is changed to OFF state in both api and app.')
            elif apimode == "ON":
                self.report_fail('Plug is currently in ON state in api but OFF in app.')
            else:
                self.report_fail('Not able to get the Plug state from api.')
        else:
            self.report_fail('Plug state is not changed in the app.')

    # function to verify the status of plugs in Dashboard.
    def verify_plugstate_dashboard(self, PlugName):
        PLUG_ON_DASH = PlugLocators.PLUG_ON_DASH
        PLUG_ON_DASH = PLUG_ON_DASH.replace("devicename", PlugName)
        PLUG_OFF_DASH = PlugLocators.PLUG_OFF_DASH
        PLUG_OFF_DASH = PLUG_OFF_DASH.replace("devicename", PlugName)
        if self.driver.find_element(*PlugLocators.DASHBOARD_ICON):
            self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            self.report_done('Dashboard Icon is clicked.')
            time.sleep(5)
            if self.wait_for_element_exist(By.XPATH, PLUG_ON_DASH):
                if PlugsPage.finalstate == "ON":
                    self.report_pass('Plug is on in Dashboard Screen and Api.')
                elif PlugsPage.finalstate == "OFF":
                    self.report_fail('Plug is on in Dashboard Screen but off in Api.')
            elif self.wait_for_element_exist(By.XPATH, PLUG_OFF_DASH):
                if PlugsPage.finalstate == "OFF":
                    self.report_pass('Plug is off in Dashboard Screen and Api.')
                elif PlugsPage.finalstate == "ON":
                    self.report_fail('Plug is off in Dashboard Screen but on in Api.')
            else:
                self.report_fail('Error in finding the exact state in Dashboard.')
        else:
            self.report_fail('Error in finding the PlugLocators for Dashboard button.')

    # function to verify the status of plugs in Dashboard.
    def verify_plugstate_devicelist(self, PlugName):
        PLUG_ON_DASH = PlugLocators.PLUG_ON_DASH
        PLUG_ON_DASH = PLUG_ON_DASH.replace("devicename", PlugName)
        PLUG_OFF_DASH = PlugLocators.PLUG_OFF_DASH
        PLUG_OFF_DASH = PLUG_OFF_DASH.replace("devicename", PlugName)
        if self.driver.find_element(*PlugLocators.DASHBOARD_ICON):
            self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            self.report_done('Device Screen Icon is clicked.')
            time.sleep(5)
            if self.wait_for_element_exist(By.XPATH, PLUG_ON_DASH):
                if PlugsPage.finalstate == "ON":
                    self.report_pass('Plug is on in DeviceList Screen and Api.')
                    self.driver.find_element(By.XPATH, PLUG_ON_DASH).click()
                elif PlugsPage.finalstate == "OFF":
                    self.report_fail('Plug is on in DeviceList Screen but off in Api.')
            elif self.wait_for_element_exist(By.XPATH, PLUG_OFF_DASH):
                if PlugsPage.finalstate == "OFF":
                    self.report_pass('Plug is off in DeviceList Screen and Api.')
                    self.driver.find_element(By.XPATH, PLUG_OFF_DASH).click()
                elif PlugsPage.finalstate == "ON":
                    self.report_fail('Plug is off in DeviceList Screen but on in Api.')
            else:
                self.driver.swipe(794.9, 1714.1, 912.8, 327.4, 2000)
                if self.wait_for_element_exist(By.XPATH, PLUG_ON_DASH):
                    if PlugsPage.finalstate == "ON":
                        self.report_pass('Plug is on in DeviceList Screen and Api.')
                        self.driver.find_element(By.XPATH, PLUG_ON_DASH).click()
                    elif PlugsPage.finalstate == "OFF":
                        self.report_fail('Plug is on in DeviceList Screen but off in Api.')
                elif self.wait_for_element_exist(By.XPATH, PLUG_OFF_DASH):
                    if PlugsPage.finalstate == "OFF":
                        self.report_pass('Plug is off in DeviceList Screen and Api.')
                        self.driver.find_element(By.XPATH, PLUG_OFF_DASH).click()
                    elif PlugsPage.finalstate == "ON":
                        self.report_fail('Plug is off in DeviceList Screen but on in Api.')
                else:
                    self.report_fail('Error in getting the exact state in Device screen.')
            time.sleep(5)
        else:
            self.report_fail('Error in finding the PlugLocators for DeviceList Screen button.')

    # to check whether plug is in off state or on state
    def verify_plugstate_api(self, PlugName):
        nodes = Putils.getNodes()
        apimode = ""
        for oNode in nodes['nodes']:
            if oNode['name'] == PlugName:

                if oNode['attributes']['state']['reportedValue'] == 'ON':
                    apimode = "ON"
                elif oNode['attributes']['state']['reportedValue'] == 'OFF':
                    apimode = "OFF"
                else:
                    apimode = "ERROR"
        return apimode

    # to check the mode of the Plugs(Manual or Schedule)
    def verify_plugmode_api(self, PlugName):
        nodes = Putils.getNodes()
        apimode = ""
        plugid = ""
        for oNode in nodes['nodes']:
            if oNode['name'] == PlugName:
                plugid = oNode["id"]
                break

        for oNode in nodes['nodes']:
            if "nodeType" in oNode:
                if '.json' in oNode["nodeType"] and "consumers" in oNode["attributes"]:
                    synval = oNode['attributes']['consumers']['reportedValue']
                    for char in '["]':
                        synval = synval.replace(char, '')

                    if synval == plugid:
                        sched = json.loads(oNode['attributes']['syntheticDeviceConfiguration']['reportedValue'])
                        if not sched['enabled']:
                            apimode = "Manual"
                            break
                        elif sched['enabled']:
                            apimode = "Schedule"
                            break
                        else:
                            apimode = "Error"
                            break

        return apimode

    # function to change the mode of the plugs.
    def click_plugs_arrow(self, PlugName):
        apimode = self.verify_plugmode_api(PlugName)
        if self.wait_for_element_exist(*PlugLocators.BUTTON_MODE):
            if self.wait_for_element_exist(*PlugLocators.MANUAL_MODE):
                PlugsPage.currentstate = "Manual"
                if apimode == "Manual":
                    self.report_pass('Plug is currently in manual mode in both api and app.')
                elif apimode == "Schedule":
                    self.report_fail('Plug is currently in Schedule mode in api but Manual in app.')
                else:
                    self.report_fail('Not able to get the Plug mode from api.')
            elif self.wait_for_element_exist(*PlugLocators.SCHEDULE_MODE):
                PlugsPage.currentstate = "Schedule"
                if apimode == "Manual":
                    self.report_fail('Plug is currently in Manual mode in api but Schedule in app.')
                elif apimode == "Schedule":
                    self.report_pass('Plug is currently in Schedule mode in both api and app.')
                else:
                    self.report_fail('Not able to get the Plug mode from api.')
            else:
                self.report_fail('error in getting the current mode of Plugs from the app.')
            self.driver.find_element(*PlugLocators.BUTTON_MODE).click()
            self.report_done('Button for changing mode is clicked')
            time.sleep(5)
            if self.wait_for_element_exist(*PlugLocators.MANUAL_MODE):
                PlugsPage.afterstate = "Manual"
            elif self.wait_for_element_exist(*PlugLocators.SCHEDULE_MODE):
                PlugsPage.afterstate = "Schedule"
            else:
                self.report_fail('error in getting the current mode of Plugs from the app.')
        else:
            self.report_fail('Not able to find the Plugs mode arrow')

    # function to verify the mode of the plugs
    def verify_modechange(self, PlugName):
        apimode = self.verify_plugmode_api(PlugName)
        if PlugsPage.currentstate == "Manual" and PlugsPage.afterstate == "Schedule":
            if apimode == "Manual":
                self.report_fail('Plug is currently in manual mode in api but Schedule in app.')
            elif apimode == "Schedule":
                self.report_pass('Plug is changed to Schedule mode in both api and app.')
            else:
                self.report_fail('Not able to get the Plug mode from api.')
        elif PlugsPage.currentstate == "Schedule" and PlugsPage.afterstate == "Manual":
            if apimode == "Manual":
                self.report_pass('Plug is changed to manual mode in both api and app.')
            elif apimode == "Schedule":
                self.report_fail('Plug is currently in Schedule mode in api but Manual in app.')
            else:
                self.report_fail('Not able to get the Plug mode from api.')
        else:
            self.report_fail('Mode is not changed')

    # function to navigate to Plug Schedule Screen
    def click_scheduleicon(self):
        if self.wait_for_element_exist(*PlugLocators.SCHEDULE_ICON):
            self.report_pass('Schedule icon found')
            self.driver.find_element(*PlugLocators.SCHEDULE_ICON).click()
            self.report_done('Schedule Icon is clicked')
            time.sleep(5)
        else:
            self.report_fail('Schedule icon is not present')

    # function to verify to Plug Schedule Screen
    def verify_schedulescreen(self):
        if self.wait_for_element_exist(*PlugLocators.ADD_ICON):
            self.report_pass('User is navigated to Schedule Screen.')
        else:
            self.report_fail('User is not navigated to Schedule screen as add image is not found.')

    # function to navigate to Plug Recipe Screen
    def click_recipesicon(self):
        if self.wait_for_element_exist(*PlugLocators.ACTIONS_ICON):
            self.report_pass('recipes icon found')
            self.driver.find_element(*PlugLocators.ACTIONS_ICON).click()
            self.report_done('Recipes Icon is clicked')
            time.sleep(5)

        else:
            self.report_fail('Recipes icon is not present')

    # function to verify to Plug recipe Screen
    def verify_recipesscreen(self):
        if self.wait_for_element_exist(*PlugLocators.Recipes_verifytext):
            self.report_pass('User is navigated to Recipes Screen.')
        else:
            self.report_fail('User is not navigated to recipes screen as text is not found.')

    # function to verify the control screen.
    def verify_controlscreen(self):
        if self.wait_for_element_exist(*PlugLocators.BUTTON_MODE):
            self.report_pass('User is navigated to control Screen.')
        else:
            self.report_fail('User is not navigated to control screen as arrow button is not found.')

    def get_plug_attribute(self):
        if self.reporter.ActionStatus:
            try:
                strMode = ""
                strState = ""
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    time.sleep(3)
                if self.wait_for_element_exist(*SchedulePageLocators.CONTROL_ICON):
                    self.driver.find_element(*SchedulePageLocators.CONTROL_ICON).click()
                    time.sleep(5)
                    if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_MODE_VIEW):
                        strMode = self.driver.find_element(*PlugScheduleLocators.PLUG_MODE_VIEW). \
                            get_attribute("text").upper()
                        print(strMode, 'strMode')
                        if 'SCHEDULE' in strMode:
                            strMode = 'AUTO'
                        else:
                            strMode = 'MANUAL'
                    if self.is_element_present(*PlugLocators.PLUG_STATUS):
                        strStatus = self.driver.find_element(*PlugLocators.PLUG_STATUS). \
                            get_attribute("text").upper()
                        if strStatus == 'OFF':
                            strState = "0000"

                else:
                    self.report_fail(
                        "Android-App : Control not active on the Plug Control Page to fetch the mode")

                self.report_done('Android App : Screenshot while getting attributes')
                return strMode, strState
            except:
                self.report_fail('Android App : NoSuchElementException: in get_plug_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class AllRecipes(BasePage):
    # Static variables
    DEVICE_NAME = ""
    DEVICE_STATE = ""
    DEVICE_DURATION = ""
    SENSOR_NAME = ""
    SENSOR_STATE = ""

    MS_AVAILABLE = 0
    MS_DEVICE_AVAILABLE = 0

    CSO_AVAILABLE = 0
    CSC_AVAILABLE = 0
    CS_DEVICE_AVAILABLE = 0

    PLUG_MS_AVAILABLE = 0
    PLUG_CSO_AVAILABLE = 0
    PLUG_CSC_AVAILABLE = 0
    PLUG_DEVICE_AVAILABLE = 0

    WARM_MS_AVAILABLE = 0
    WARM_CSO_AVAILABLE = 0
    WARM_CSC_AVAILABLE = 0
    WARM_DEVICE_AVAILABLE = 0

    TUNEABLE_MS_AVAILABLE = 0
    TUNEABLE_CSO_AVAILABLE = 0
    TUNEABLE_CSC_AVAILABLE = 0
    TUNEABLE_DEVICE_AVAILABLE = 0

    COLOUR_MS_AVAILABLE = 0
    COLOUR_CSO_AVAILABLE = 0
    COLOUR_CSC_AVAILABLE = 0
    COLOUR_DEVICE_AVAILABLE = 0

    BULB_DEVICE_AVAILABLE = 0

    HEATING_AVAILABLE = 0

    # Sets Recipe Variables
    def setRecipeVariables(self, strDevice, strDeviceState, strDuration, strSensor, strSensorState):
        AllRecipes.DEVICE_NAME = strDevice
        AllRecipes.DEVICE_STATE = strDeviceState
        AllRecipes.DEVICE_DURATION = strDuration
        AllRecipes.SENSOR_NAME = strSensor
        AllRecipes.SENSOR_STATE = strSensorState

    # Checks/Verfies the model value for the given device from API
    def checkModelValue(self, deviceName, deviceModel):
        AllRecipes.DEVICE_NAME = deviceName
        if ("Motion sensor" in deviceName) and ("PIR00140005" in deviceModel):
            AllRecipes.MS_DEVICE_AVAILABLE = 1
            return True
        elif "Win/door sensor" in deviceName:
            if "WDS00140002" in deviceModel:
                AllRecipes.CS_DEVICE_AVAILABLE = 1
                return True
            elif "DWS003" in deviceModel:
                AllRecipes.CS_DEVICE_AVAILABLE = 1
                return True
        elif "Plug" in deviceName:
            if "SLP2" in deviceModel:
                AllRecipes.PLUG_DEVICE_AVAILABLE = 1
                return True
            elif "SLP2b" in deviceModel:
                AllRecipes.PLUG_DEVICE_AVAILABLE = 1
                return True
        elif ("Warm white light" in deviceName) and ("FWBulb01" in deviceModel):
            AllRecipes.BULB_DEVICE_AVAILABLE = 1
            return True
        elif ("Tuneable light" in deviceName) and ("TWBulb01UK" in deviceModel):
            AllRecipes.BULB_DEVICE_AVAILABLE = 1
            return True
        elif ("Colour light" in deviceName) and ("RGBBulb01UK" in deviceModel):
            AllRecipes.BULB_DEVICE_AVAILABLE = 1
            return True
        elif (("Heating" in deviceName) and ("SLT3" in deviceModel)) or (
                    ("Heating" in deviceName) and ("SLT2" in deviceModel)) or (
                    ("Heating" in deviceName) and ("SLT3b" in deviceModel)):
            AllRecipes.HEATING_AVAILABLE = 1
            return True
        else:
            self.report_fail('Device and Model are not matching')
            return False

    # Checks whether device is present in user account
    def check_the_device_with_hub(self, nameDevice):
        if self.reporter.ActionStatus:
            try:
                AllRecipes.DEVICE = nameDevice
                deviceModel = pUtils.getDeviceModel(nameDevice)
                modelValue = AllRecipes.checkModelValue(self, nameDevice, deviceModel)
                if modelValue:
                    print("Device model for " + nameDevice + " is " + str(
                        deviceModel) + " , and is available in the user account")
                    self.report_pass(nameDevice + " , is available in the user account")
                else:
                    self.report_fail('Android App : The given device is not paired with the hub')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in check_the_device_with_hub Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Navigates to All Recipes page
    def navigate_to_allrecipes(self):
        if self.reporter.ActionStatus:
            try:
                time.sleep(2)
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_SHOW):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                    if self.wait_for_element_exist(*HomePageLocators.ACTIONS_MENU):
                        self.driver.find_element(*HomePageLocators.ACTIONS_MENU).click()
                        if self.wait_for_element_exist(*ActionsScreenLocators.ALL_RECIPES_SCREEN_HEADER):
                            self.report_pass('Android App : Navigated to All Recipes screen successfully')
                        else:
                            self.report_fail('Android App : All Recipes header is not as expected')
                    else:
                        self.report_fail('Android App : All Recipes menu option is not displayed')
                else:
                    self.report_fail('Android App : Main Menu button is not displayed')
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_allrecipes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Navigates to Actions page
    def navigate_to_actions(self):
        if self.reporter.ActionStatus:
            try:
                time.sleep(2)
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_SHOW):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                    if self.wait_for_element_exist(*HomePageLocators.MY_ACTIONS_MENU):
                        self.driver.find_element(*HomePageLocators.MY_ACTIONS_MENU).click()
                        if self.wait_for_element_exist(*ActionsScreenLocators.ACTIONS_SCREEN_HEADER):
                            self.report_pass('Android App : Navigated to Actions screen successfully')
                        else:
                            self.report_fail('Android App : Actions header is not as expected')
                    else:
                        self.report_fail('Android App : Actions menu option is not displayed')
                else:
                    self.report_fail('Android App : Main Menu button is not displayed')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_actions Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Navigates to specific category page
    def navigate_to_action_category(self, Category):
        if self.reporter.ActionStatus:
            try:
                time.sleep(2)
                if self.is_element_present(*ActionsScreenLocators.DISCOVERY_TITLE):
                    self.report_pass('Android App : Already on Discover Actions screen successfully')
                elif not self.is_element_present(*HomePageLocators.MY_ACTIONS_MENU):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                    self.driver.find_element(*HomePageLocators.MY_ACTIONS_MENU).click()
                    self.driver.find_element(*ActionsScreenLocators.DISCOVERY_FAB).click()

                elif not self.is_element_present(*ActionsScreenLocators.ACTIONS_SCREEN_HEADER):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                    self.driver.find_element(*HomePageLocators.MY_ACTIONS_MENU).click()
                    self.driver.find_element(*ActionsScreenLocators.DISCOVERY_FAB).click()

                elif not self.is_element_present(*ActionsScreenLocators.DISCOVERY_TITLE):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                    self.driver.find_element(*HomePageLocators.MY_ACTIONS_MENU).click()
                    self.driver.find_element(*ActionsScreenLocators.DISCOVERY_FAB).click()
                else:
                    self.report_fail('Android App : Discover Actions header is not as expected')

                categorytobeseen = ""
                if "WELCOME HOME" in Category.upper():
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_WELCOME_HOME_BANNER
                elif Category.upper() == "COMFORT":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_COMFORT_ICON
                elif Category.upper() == "REASSURANCE":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_REASSURANCE_ICON
                elif Category.upper() == "EFFICIENCY":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_EFFICIENCY_ICON
                elif Category.upper() == "THERMOSTAT":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_THERMOSTAT_ICON
                elif Category.upper() == "PLUGS":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_PLUGS_ICON
                elif Category.upper() == "LIGHTS":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_LIGHTS_ICON
                elif Category.upper() == "MOTION SENSOR":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_MOTION_SENSOR_ICON
                elif Category.upper() == "WIN/DOOR SENSOR":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_DOOR_SENSOR_ICON
                elif Category.upper() == "HOT WATER":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_HOT_WATER_SENSOR_ICON
                elif Category.upper() == "ALL ACTIONS":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_ALL_ACTIONS_ICON
                elif Category.upper() == "BUILD YOUR OWN":
                    categorytobeseen = ActionsScreenLocators.DISCOVERY_BUILD_YOUR_OWN_ICON

                if self.is_element_present(*categorytobeseen):
                    self.driver.find_element(*categorytobeseen).click()
                    time.sleep(2)
                else:
                    AllRecipes.scroll_on_Browse_By_device(self)
                    self.driver.find_element(*categorytobeseen).click()
                    time.sleep(2)

                categoy_page_title_on_discover_actions = str(ActionsScreenLocators.CATEGORY_PAGE_TITLE)
                if Category.upper() == "ALL ACTIONS":
                    categoy_page_title_on_discover_actions = categoy_page_title_on_discover_actions.replace(
                        "categoryName", Category)
                else:
                    categoy_page_title_on_discover_actions = categoy_page_title_on_discover_actions.replace(
                        "categoryName", Category + ' actions')

                if self.wait_for_element_exist(By.NAME, categoy_page_title_on_discover_actions):
                    print('\n Navigated to ' + Category + ' actions template screen successfully')
                    self.report_pass('Android App : Navigated to ' + Category + ' actions template screen successfully')
                else:
                    self.report_fail('Android App : ' + Category + 'actions template screen is not as expected')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_action_category Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Horizontal Scroll on discover actions 'Browse by device' section ( 4 elements at once )
    def scroll_on_Browse_By_device(self):
        if self.reporter.ActionStatus:
            try:
                element_to_tap = self.driver.find_element(*ActionsScreenLocators.DEVICE_FOURTH_ELEMENT)
                element_to_drag_to = self.driver.find_element(*ActionsScreenLocators.DEVICE_FIRST_ELEMENT)
                time.sleep(2)
                start_x = element_to_tap.location['x']
                start_y = element_to_tap.location['y']
                end_x = element_to_drag_to.location['x']
                end_y = element_to_drag_to.location['y']
                self.driver.swipe(start_x, start_y, end_x, end_y)

                time.sleep(2)
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in scroll_on_Browse_By_device Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Navigates to 1 level back page
    def navigate_to_back_page(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*ActionsScreenLocators.DISCOVERY_BACK_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.DISCOVERY_BACK_BUTTON).click()
                    self.report_pass('Android App : Navigated to Back screen successfully')
                else:
                    self.report_fail('Android App : Problem in navigating back')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigate_to_back_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Verify the templates on the specific category page
    def verify_the_action_templates_category(self, categoryTemplates, Category, userLocale):
        if self.reporter.ActionStatus:
            try:
                nonfoundTemplates = []
                # Checks the templates on UI
                templateCountAPI = len(categoryTemplates)
                templateCountUI = 0
                print('\nChecking templates for ' + Category)
                print('#####################################')
                for oTemplate in categoryTemplates:
                    categoy_template_name = str(ActionsScreenLocators.CATEGORY_TEMPLATE_NAME)
                    categoy_template_name = categoy_template_name.replace("templateName", oTemplate['meta'][
                        userLocale.replace('_', '-')]['name'])
                    print('\nChecking ' + '" ' + categoy_template_name + ' "' + ' template on UI')
                    if self.is_element_present(By.NAME, categoy_template_name):
                        template_text = self.driver.find_element(By.NAME, categoy_template_name).text
                        print('\n' + template_text + ' "' + ' template is present on UI')
                        print(
                            '-------------------------------------------------------------------------------------------------')
                        self.report_pass('Android App : "' + template_text + '" template is present on App UI')
                        templateCountUI = templateCountUI + 1
                    else:
                        AllRecipes.scroll_on_templates_view(self, categoy_template_name)
                        if self.is_element_present(By.NAME, categoy_template_name):
                            template_text = self.driver.find_element(By.NAME, categoy_template_name).text
                            print('\n' + template_text + ' "' + ' template is present on UI')
                            print(
                                '-------------------------------------------------------------------------------------------------')
                            self.report_pass('Android App : "' + template_text + '" template is present on App UI')
                            templateCountUI = templateCountUI + 1
                        else:
                            nonfoundTemplates.append(categoy_template_name)
                            continue

                if templateCountUI > 0:
                    if templateCountUI == templateCountAPI:
                        self.report_pass('Android App : All templates are present')
                        print('...................................................')
                        print('All templates are present')
                    else:
                        print('\n' + str(templateCountUI) + " templates are present out of " + str(
                            len(categoryTemplates)))
                        self.report_done("\n Below are non found templates ")
                        print("\n Below are non found templates ")
                        i = 1
                        for oTemplate in nonfoundTemplates:
                            print("\n " + str(i) + " . " + str(oTemplate))
                            self.report_done("\n " + str(i) + " . " + str(oTemplate))
                            i = i + 1
                else:
                    self.report_fail('Android App : Unable to find atleast one template')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in verify_the_action_templates_category Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Vertical Scroll on actions templates for any category ( scrolls until template is seen )
    def scroll_on_templates_view(self, categoy_template_name):
        try:
            time.sleep(1)
            script = 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().textContains("' + categoy_template_name + '").instance(0))'
            self.driver.find_element_by_android_uiautomator(script)
            time.sleep(1)
        except:
            self.report_fail('Android App : NoSuchElementException: in scroll_on_templates_view Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Removes/Deletes all the recipes on All Recipes page
    def remove_existing_recipes(self):
        if self.reporter.ActionStatus:
            try:
                if not self.wait_for_element_exist(*ActionsScreenLocators.NO_RECIPES_PRESENT):

                    count = 0
                    while True:
                        recipe = self.driver.find_element(*ActionsScreenLocators.ARROW_RECIPE_LIST)
                        recipe.click()
                        count = count + 1
                        CURRENT_RECIPE = self.driver.find_element(*ActionsScreenLocators.RECIPE_TEXT_ON_EDIT_PAGE).text
                        self.driver.find_element(*ActionsScreenLocators.RECIPE_DELETE_BUTTON).click()
                        time.sleep(5)
                        self.driver.find_element(*ActionsScreenLocators.REMOVE_BUTTON_POP_UP).click()
                        time.sleep(5)
                        print('Deleted :     ' + ' " ' + CURRENT_RECIPE + ' " ')
                        self.report_done(
                            'Recipe : ' + ' " ' + CURRENT_RECIPE + ' " ' + ' has been removed successfully')
                        if not self.wait_for_element_exist(*ActionsScreenLocators.ARROW_RECIPE_LIST):
                            break
                    self.report_pass('Android App :  All ' + str(count) + " recipes are deleted successfully ")
                    print("Number of recipes successfully deleted are : " + str(count))
                elif self.wait_for_element_exist(*ActionsScreenLocators.NO_RECIPES_PRESENT):
                    print("There are no recipes in the user account , so nothing available for delete")
                    self.report_pass(
                        'Android App : There are no recipes in the user account , so nothing available for delete ')
                else:
                    self.report_fail('Problem in removing existing recipes')
            except:
                self.report_fail('Android App : NoSuchElementException: in remove_existing_recipes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Finds existing recipe on recipe list page ( Checks 5 recipes at once )
    def find_existing_recipe_all_recipes_page(self, recipe_to_find):
        if self.reporter.ActionStatus:
            try:
                count = pUtils.getAllRecipesCount()
                seen = 0
                print("Total Recipe Present are : " + str(count))
                self.report_pass('Total Recipe Present are : ' + str(count))
                while count > 0:
                    for num in range(0, count):
                        if self.wait_for_element_exist(By.XPATH, recipe_to_find):
                            reci_temp = self.driver.find_element(By.XPATH, recipe_to_find)
                            print("Recipe found : " + reci_temp.text)
                            return True
                            break
                        else:
                            count = count - 1
                            seen = seen + 1
                            if seen >= 5:
                                AllRecipes.scroll_on_recipe_list(self)
                            else:
                                continue
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in find_existing_recipe_all_recipes_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Finds existing recipe on sensor recipe list page ( Checks 4 recipes at once )
    def find_existing_recipe_on_sensor_recipes_page(self, Sensor, recipe_to_find):
        if self.reporter.ActionStatus:
            try:
                count = pUtils.getSensorRecipeCount(Sensor)
                seen = 0
                print("Total " + Sensor + " Recipe Present are : " + str(count))
                while count > 0:
                    for num in range(0, count):
                        if self.wait_for_element_exist(By.XPATH, recipe_to_find):
                            reci_temp = self.driver.find_element(By.XPATH, recipe_to_find)
                            print("Recipe found : " + reci_temp.text)
                            return True
                            break
                        else:
                            count = count - 1
                            seen = seen + 1
                            if seen >= 4:
                                AllRecipes.scroll_on_sensor_page_recipe_list(self)
                            else:
                                continue
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in find_existing_recipe_on_sensor_recipes_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Scrolls on recipe templates page ( 6 elements at once )
    def scroll_on_recipe_templates(self):
        if self.reporter.ActionStatus:
            try:
                element_to_tap = self.driver.find_element(*ActionsScreenLocators.SIXTH_ELEMENT)
                element_to_drag_to = self.driver.find_element(*ActionsScreenLocators.FIRST_ELEMENT)
                time.sleep(2)
                self.driver.scroll(element_to_tap, element_to_drag_to)
                time.sleep(2)
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in scroll_on_recipe_templates Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Scrolls on recipe list page ( 5 elements at once )
    def scroll_on_recipe_list(self):
        if self.reporter.ActionStatus:
            try:
                element_to_tap = self.driver.find_element(*ActionsScreenLocators.FIFTH_ELEMENT)
                element_to_drag_to = self.driver.find_element(*ActionsScreenLocators.FIRST_ELEMENT)
                time.sleep(2)
                self.driver.scroll(element_to_tap, element_to_drag_to)
                time.sleep(2)
            except:
                self.report_fail('Android App : NoSuchElementException: in scroll_on_recipe_list Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Scrolls on recipe list on sensor recipes tab ( 4 elements at once )
    def scroll_on_sensor_page_recipe_list(self):
        if self.reporter.ActionStatus:
            try:
                element_to_tap = self.driver.find_element(*ActionsScreenLocators.FOURTH_ELEMENT)
                element_to_drag_to = self.driver.find_element(*ActionsScreenLocators.FIRST_ELEMENT)
                time.sleep(2)
                self.driver.scroll(element_to_tap, element_to_drag_to)
                time.sleep(2)
            except:
                self.report_fail('Android App : NoSuchElementException: in scroll_on_recipe_list Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Selects when and then for a new NotifyMe recipe
    def select_create_when_then_notify(self, Sensor, TypeOf):
        if self.reporter.ActionStatus:
            try:
                # Selects the when
                if self.wait_for_element_exist(*ActionsScreenLocators.MULTI_WHEN_PICKER):
                    if Sensor in self.driver.find_element(*ActionsScreenLocators.MULTI_WHEN_PICKER).text:
                        self.report_pass("When part is preselected")
                    elif self.wait_for_element_exist(*ActionsScreenLocators.NOTIFY_WHEN_PICKER):
                        self.driver.find_element(*ActionsScreenLocators.NOTIFY_WHEN_PICKER).click()
                        device = str(ActionsScreenLocators.WHEN_CHOOSE_DEVICE)
                        devicetoselect = device.replace("device", Sensor)
                        if self.wait_for_element_exist(By.XPATH, devicetoselect):
                            self.driver.find_element(By.XPATH, devicetoselect).click()
                            self.report_done('Selected  ' + Sensor)
                            self.driver.find_element(*ActionsScreenLocators.WHEN_OK_BUTTON).click()
                        else:
                            self.report_fail('Unable to select the device')
                    else:
                        self.report_fail("Problem in When part selection")

                # Selects the then
                if self.wait_for_element_exist(*ActionsScreenLocators.NOTIFY_THEN_PICKER):
                    self.driver.find_element(*ActionsScreenLocators.NOTIFY_THEN_PICKER).click()
                    if "Push" in TypeOf:
                        if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).text:
                            self.report_done('Push Notification is already selected')
                        else:
                            self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).click()
                            self.report_done('Selected Push option')
                    elif "Email" in TypeOf:
                        if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).text:
                            self.report_done('Email Notification is already selected')
                        else:
                            self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).click()
                            self.report_done('Selected Email option')
                    elif "Text" in TypeOf:
                        if self.wait_for_element_exist(*ActionsScreenLocators.THEN_TEXT_BUTTON):
                            self.report_done('User has HIVE LIVE subscription')
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).text:
                                self.report_done('Text Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).click()
                                self.report_done('Selected Text option')
                        else:
                            self.report_done('User does not have HIVE LIVE subscription')
                    elif "Push & Email" in TypeOf:
                        if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).text:
                            self.report_done('Push Notification is already selected')
                        else:
                            self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).click()
                            self.report_done('Selected Push option')
                        if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).text:
                            self.report_done('Email Notification is already selected')
                        else:
                            self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).click()
                            self.report_done('Selected Email option')
                    elif "Push & Text" in TypeOf:
                        if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).text:
                            self.report_done('Push Notification is already selected')
                        else:
                            self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).click()
                            self.report_done('Selected Push option')
                        if self.wait_for_element_exist(*ActionsScreenLocators.THEN_TEXT_BUTTON):
                            self.report_done('User has HIVE LIVE subscription')
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).text:
                                self.report_done('Text Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).click()
                                self.report_done('Selected Text option')
                        else:
                            self.report_done('User does not have HIVE LIVE subscription')
                    elif "Email & Text" in TypeOf:
                        if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).text:
                            self.report_done('Email Notification is already selected')
                        else:
                            self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).click()
                            self.report_done('Selected Email option')
                        if self.wait_for_element_exist(*ActionsScreenLocators.THEN_TEXT_BUTTON):
                            self.report_done('User has HIVE LIVE subscription')
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).text:
                                self.report_done('Text Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).click()
                                self.report_done('Selected Text option')
                        else:
                            self.report_done('User does not have HIVE LIVE subscription')
                else:
                    print("Problem in then picker")
                if self.wait_for_element_exist(*ActionsScreenLocators.THEN_BACK_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.THEN_BACK_BUTTON).click()
                if self.wait_for_element_exist(*ActionsScreenLocators.SAVE_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.SAVE_BUTTON).click()
                self.report_pass('Android App : Recipe created successfully')
                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in select_create_when_then_notify Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Edits then part of NotifyMe recipe
    def select_edit_then_notify(self, TypeOf):
        if self.reporter.ActionStatus:
            try:
                if not self.wait_for_element_exist(*ActionsScreenLocators.MULTI_THEN_PICKER):
                    print("Then part is preselected")
                else:
                    # Selects the then
                    if self.wait_for_element_exist(*ActionsScreenLocators.NOTIFY_THEN_PICKER):
                        self.driver.find_element(*ActionsScreenLocators.NOTIFY_THEN_PICKER).click()
                        if "Push" in TypeOf:
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).text:
                                self.report_done('Push Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).click()
                                self.report_done('Selected Push option')
                        elif "Email" in TypeOf:
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).text:
                                self.report_done('Email Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).click()
                                self.report_done('Selected Email option')
                        elif "Text" in TypeOf:
                            if self.wait_for_element_exist(*ActionsScreenLocators.THEN_TEXT_BUTTON):
                                self.report_done('User has HIVE LIVE subscription')
                                if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).text:
                                    self.report_done('Text Notification is already selected')
                                else:
                                    self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).click()
                                    self.report_done('Selected Text option')
                            else:
                                self.report_done('User does not have HIVE LIVE subscription')
                        elif "Push & Email" in TypeOf:
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).text:
                                self.report_done('Push Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).click()
                                self.report_done('Selected Push option')
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).text:
                                self.report_done('Email Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).click()
                                self.report_done('Selected Email option')
                        elif "Push & Text" in TypeOf:
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).text:
                                self.report_done('Push Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_PUSH_BUTTON).click()
                                self.report_done('Selected Push option')
                            if self.wait_for_element_exist(*ActionsScreenLocators.THEN_TEXT_BUTTON):
                                self.report_done('User has HIVE LIVE subscription')
                                if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).text:
                                    self.report_done('Text Notification is already selected')
                                else:
                                    self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).click()
                                    self.report_done('Selected Text option')
                            else:
                                self.report_done('User does not have HIVE LIVE subscription')
                        elif "Email & Text" in TypeOf:
                            if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).text:
                                self.report_done('Email Notification is already selected')
                            else:
                                self.driver.find_element(*ActionsScreenLocators.THEN_EMAIL_BUTTON).click()
                                self.report_done('Selected Email option')
                            if self.wait_for_element_exist(*ActionsScreenLocators.THEN_TEXT_BUTTON):
                                self.report_done('User has HIVE LIVE subscription')
                                if "ON" in self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).text:
                                    self.report_done('Text Notification is already selected')
                                else:
                                    self.driver.find_element(*ActionsScreenLocators.THEN_TEXT_BUTTON).click()
                                    self.report_done('Selected Text option')
                            else:
                                self.report_done('User does not have HIVE LIVE subscription')
                    else:
                        print("Problem in then picker")
                if self.wait_for_element_exist(*ActionsScreenLocators.THEN_BACK_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.THEN_BACK_BUTTON).click()
                if self.wait_for_element_exist(*ActionsScreenLocators.SAVE_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.SAVE_BUTTON).click()
                self.report_pass('Android App : Recipe updated successfully')
                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in select_edit_then_notify Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Creates a new NotifyMe Recipe
    def create_new_notification_recipe(self, TypeOf, Sensor, SensorState):
        if self.reporter.ActionStatus:
            try:
                # Checks presence and Selects the template if needed
                if ("Motion sensor" in Sensor) & ("detects motion" in SensorState):
                    ms_recipe = str(ActionsScreenLocators.MS_NOTIFY_RECIPE)
                    ms_recipe_created = ms_recipe.replace("sensorname", Sensor)
                    if not AllRecipes.find_existing_recipe_all_recipes_page(self, ms_recipe_created):
                        self.report_step('Creating new Recipe')
                        if self.wait_for_element_exist(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON):
                            self.driver.find_element(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON).click()
                        if self.wait_for_element_exist(*ActionsScreenLocators.MS_NOT_RECIPE):
                            self.driver.find_element(*ActionsScreenLocators.MS_NOT_RECIPE).click()
                            self.report_done('Selected Recipe Template')
                            AllRecipes.select_create_when_then_notify(self, Sensor, TypeOf)
                    else:
                        self.report_pass(
                            'Android App : Such Recipe already exists , cannot create again : edited as needed')
                        print('Android App : Such Recipe already exists , cannot create again : editing now as needed')
                        self.driver.find_element(By.XPATH, ms_recipe_created).click()
                        AllRecipes.select_edit_then_notify(self, TypeOf)
                elif ("Win/door sensor" in Sensor) & ("opened" in SensorState):
                    cso_recipe = str(ActionsScreenLocators.CSO_NOTIFY_RECIPE)
                    cso_recipe_created = cso_recipe.replace("sensorname", Sensor)
                    if not AllRecipes.find_existing_recipe_all_recipes_page(self, cso_recipe_created):
                        self.report_step('Creating new Recipe')
                        if self.wait_for_element_exist(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON):
                            self.driver.find_element(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON).click()
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSO_NOT_RECIPE):
                            self.driver.find_element(*ActionsScreenLocators.CSO_NOT_RECIPE).click()
                            self.report_done('Selected Recipe Template')
                            AllRecipes.select_create_when_then_notify(self, Sensor, TypeOf)
                    else:
                        self.report_pass(
                            'Android App : Such Recipe already exists , cannot create again : edited as needed')
                        print('Android App : Such Recipe already exists , cannot create again : editing now as needed')
                        self.driver.find_element(By.XPATH, cso_recipe_created).click()
                        AllRecipes.select_edit_then_notify(self, TypeOf)
                elif ("Win/door sensor" in Sensor) & ("closed" in SensorState):
                    csc_recipe = str(ActionsScreenLocators.CSC_NOTIFY_RECIPE)
                    csc_recipe_created = csc_recipe.replace("sensorname", Sensor)
                    if not AllRecipes.find_existing_recipe_all_recipes_page(self, csc_recipe_created):
                        self.report_step('Creating new Recipe')
                        if self.wait_for_element_exist(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON):
                            self.driver.find_element(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON).click()
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSC_NOT_RECIPE):
                            self.driver.find_element(*ActionsScreenLocators.CSC_NOT_RECIPE).click()
                            self.report_done('Selected Recipe Template')
                            AllRecipes.select_create_when_then_notify(self, Sensor, TypeOf)
                    else:
                        self.report_pass(
                            'Android App : Such Recipe already exists , cannot create again : edited as needed')
                        print('Android App : Such Recipe already exists , cannot create again : editing now as needed')
                        self.driver.find_element(By.XPATH, csc_recipe_created).click()
                        AllRecipes.select_edit_then_notify(self, TypeOf)
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in create_new_notification_recipe Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Verifies created NotifyMe recipe on All Recipes page
    def verify_notifyme_recipe_all_recipes(self, Sensor, SensorState):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*ActionsScreenLocators.ALL_RECIPES_SCREEN_HEADER):

                    # Checks presence of created recipe
                    if ("Motion sensor" in Sensor) & ("detects motion" in SensorState):
                        ms_recipe = str(ActionsScreenLocators.MS_NOTIFY_RECIPE)
                        ms_recipe = ms_recipe.replace("sensorname", Sensor)
                        if self.wait_for_element_exist(By.XPATH, ms_recipe):
                            self.report_pass(
                                "Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                            print("Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                        else:
                            AllRecipes.scroll_on_recipe_list(self)
                            if self.wait_for_element_exist(By.XPATH, ms_recipe):
                                self.report_pass(
                                    "Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                                print("Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                            else:
                                self.report_fail(
                                    "Android App : Created " + Sensor + " recipe is not visible on All Recipes page")

                    elif ("Win/door sensor" in Sensor) & ("opened" in SensorState):
                        cso_recipe = str(ActionsScreenLocators.CSO_NOTIFY_RECIPE)
                        cso_recipe = cso_recipe.replace("sensorname", Sensor)
                        if self.wait_for_element_exist(By.XPATH, cso_recipe):
                            self.report_pass(
                                "Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                            print("Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                        else:
                            AllRecipes.scroll_on_recipe_list(self)
                            if self.wait_for_element_exist(By.XPATH, cso_recipe):
                                self.report_pass(
                                    "Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                                print("Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                            else:
                                self.report_fail(
                                    "Android App : Created " + Sensor + " recipe is not visible on All Recipes page")

                    elif ("Win/door sensor" in Sensor) & ("closed" in SensorState):
                        csc_recipe = str(ActionsScreenLocators.CSC_NOTIFY_RECIPE)
                        csc_recipe = csc_recipe.replace("sensorname", Sensor)
                        if self.wait_for_element_exist(By.XPATH, csc_recipe):
                            self.report_pass(
                                "Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                            print("Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                        else:
                            AllRecipes.scroll_on_recipe_list(self)
                            if self.wait_for_element_exist(By.XPATH, csc_recipe):
                                self.report_pass(
                                    "Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                                print("Android App : Created " + Sensor + " recipe is visible on All Recipes page")
                            else:
                                self.report_fail(
                                    "Android App : Created " + Sensor + " recipe is not visible on All Recipes page")
                else:
                    self.report_fail('All Recipes page is not visible')
                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_notifyme_recipe Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Verifies created NotifyMe recipe on Device Recipes page
    def verify_notifyme_recipe_sensor_page(self, Sensor, SensorState):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*ActionsScreenLocators.RECIPES_TAB):
                    if self.wait_for_element_exist(*ActionsScreenLocators.RECIPES_TAB):
                        self.driver.find_element(*ActionsScreenLocators.RECIPES_TAB).click()
                    self.report_pass('Android App : Navigated to Device Control Page Recipes screen successfully')

                    # Checks presence of created recipe
                    if ("Motion sensor" in Sensor) & ("detects motion" in SensorState):
                        ms_recipe = str(ActionsScreenLocators.MS_NOTIFY_RECIPE)
                        ms_recipe = ms_recipe.replace("sensorname", Sensor)
                        if AllRecipes.find_existing_recipe_on_sensor_recipes_page(self, Sensor, ms_recipe):
                            self.report_pass(
                                "Android App : Created " + Sensor + " recipe is visible on Device Control Page Recipes screen")
                        else:
                            self.report_fail(
                                "Android App : Created " + Sensor + " recipe is not visible on Device Control Page Recipes screen")

                    elif ("Win/door sensor" in Sensor) & ("opened" in SensorState):
                        cso_recipe = str(ActionsScreenLocators.CSO_NOTIFY_RECIPE)
                        cso_recipe = cso_recipe.replace("sensorname", Sensor)
                        if AllRecipes.find_existing_recipe_on_sensor_recipes_page(self, Sensor, cso_recipe):
                            self.report_pass(
                                "Android App : Created " + Sensor + " recipe is visible on Device Control Page Recipes screen")
                        else:
                            self.report_fail(
                                "Android App : Created " + Sensor + " recipe is not visible Device Control Page Recipes screen")

                    elif ("Win/door sensor" in Sensor) & ("closed" in SensorState):
                        csc_recipe = str(ActionsScreenLocators.CSC_NOTIFY_RECIPE)
                        csc_recipe = csc_recipe.replace("sensorname", Sensor)
                        if AllRecipes.find_existing_recipe_on_sensor_recipes_page(self, Sensor, csc_recipe):
                            self.report_pass(
                                "Android App : Created " + Sensor + " recipe is visible on Device Control Page Recipes screen")
                        else:
                            self.report_fail(
                                "Android App : Created " + Sensor + " recipe is not visible on Device Control Page Recipes screen")
                    else:
                        self.report_fail('Problem while searching recipe on ' + Sensor + ' screen')

                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_notifyme_recipe Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Verifies created OnOff recipe on Sensor Recipes page
    def verify_on_off_recipe_sensor_page(self, Sensor):
        if self.reporter.ActionStatus:
            try:
                time.sleep(3)
                if self.wait_for_element_exist(*ActionsScreenLocators.RECIPES_TAB):
                    self.driver.find_element(*ActionsScreenLocators.RECIPES_TAB).click()
                    self.report_pass('Android App : Navigated to Device Control Page Recipes screen successfully')

                # Checks presence of created recipe
                if ("Motion sensor" in Sensor) & ("detects motion" in AllRecipes.SENSOR_STATE):
                    ms_device_recipe_created = str(ActionsScreenLocators.DEVICE_TURN_MS_RECIPE)
                    ms_device_recipe_created = ms_device_recipe_created.replace("devicename", AllRecipes.DEVICE_NAME)
                    ms_device_recipe_created = ms_device_recipe_created.replace("devicestate", AllRecipes.DEVICE_STATE)
                    ms_device_recipe_created = ms_device_recipe_created.replace("sensor", Sensor)

                    if AllRecipes.find_existing_recipe_on_sensor_recipes_page(self, Sensor, ms_device_recipe_created):
                        print("Android App :  " + Sensor + " recipe is visible on Sensor Control Page Recipes screen")
                        self.report_pass(
                            "Android App :  " + Sensor + " recipe is visible on Sensor Control Page Recipes screen")
                    else:
                        self.report_fail(
                            "Android App :  " + Sensor + " recipe is not visible on Sensor Control Page Recipes screen")

                elif ("Win/door sensor" in Sensor) & ("opened" in AllRecipes.SENSOR_STATE):
                    cso_device_recipe_created = str(ActionsScreenLocators.DEVICE_TURN_CSO_RECIPE)
                    cso_device_recipe_created = cso_device_recipe_created.replace("devicename", AllRecipes.DEVICE_NAME)
                    cso_device_recipe_created = cso_device_recipe_created.replace("devicestate",
                                                                                  AllRecipes.DEVICE_STATE)
                    cso_device_recipe_created = cso_device_recipe_created.replace("sensor", Sensor)

                    if AllRecipes.find_existing_recipe_on_sensor_recipes_page(self, Sensor, cso_device_recipe_created):
                        print(
                            "Android App : Created " + Sensor + " recipe is visible on Sensor Control Page Recipes screen")
                        self.report_pass(
                            "Android App :  " + Sensor + " recipe is visible on Sensor Control Page Recipes screen")
                    else:
                        self.report_fail(
                            "Android App :  " + Sensor + " recipe is not visible Sensor Control Page Recipes screen")

                elif ("Win/door sensor" in Sensor) & ("closed" in AllRecipes.SENSOR_STATE):
                    csc_device_recipe_created = str(ActionsScreenLocators.DEVICE_TURN_CSC_RECIPE)
                    csc_device_recipe_created = csc_device_recipe_created.replace("devicename", AllRecipes.DEVICE_NAME)
                    csc_device_recipe_created = csc_device_recipe_created.replace("devicestate",
                                                                                  AllRecipes.DEVICE_STATE)
                    csc_device_recipe_created = csc_device_recipe_created.replace("sensor", Sensor)
                    if AllRecipes.find_existing_recipe_on_sensor_recipes_page(self, Sensor, csc_device_recipe_created):
                        print(
                            "Android App : Created " + Sensor + " recipe is visible on Sensor Control Page Recipes screen")
                        self.report_pass(
                            "Android App :  " + Sensor + " recipe is visible on Sensor Control Page Recipes screen")
                    else:
                        self.report_fail(
                            "Android App :  " + Sensor + " recipe is not visible on Sensor Control Page Recipes screen")
                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in verify_on_off_recipe_sensor_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Verifies the Recipe Templates on All Recipes Page
    def verify_recipe_template(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*ActionsScreenLocators.ALL_RECIPES_SCREEN_HEADER):
                    self.report_pass('Android App : Navigated to All Recipes screen successfully')
                    if self.wait_for_element_exist(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON):
                        self.driver.find_element(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON).click()

                    # Checks NotifyMe Recipes Templates
                    if AllRecipes.MS_DEVICE_AVAILABLE != 0:
                        if self.wait_for_element_exist(*ActionsScreenLocators.MS_NOT_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.MS_NOT_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as motion sensor is present in user account')
                        else:
                            self.report_fail('Android App : MS_NOTIFY_ME_RECIPE template is not present')
                    else:
                        self.report_fail('Android App : Motion Sensor not present in user account')

                    if AllRecipes.CS_DEVICE_AVAILABLE != 0:
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSO_NOT_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.CSO_NOT_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as Window/Door sensor is present in user account')
                        else:
                            self.report_fail('Android App : CSO_NOTIFY_ME_RECIPE template is not present')
                    else:
                        self.report_fail('Android App : Win/door Sensor not present in user account')

                    if AllRecipes.CS_DEVICE_AVAILABLE != 0:
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSC_NOT_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.CSC_NOT_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as Window/Door sensor is present in user account')
                        else:
                            self.report_fail('Android App : CSC_NOTIFY_ME_RECIPE template is not present')
                    else:
                        self.report_fail('Android App : Win/door Sensor not present in user account')

                    # Checks Plug Recipes Templates
                    if (AllRecipes.MS_DEVICE_AVAILABLE != 0) & (AllRecipes.PLUG_DEVICE_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.MS_PL_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.MS_PL_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as motion sensor and plug are present in user account')
                        else:
                            self.report_fail('Android App : MS_PLUG_RECIPE template is not present ')
                    else:
                        self.report_fail('Android App : Motion Sensor and Plug are not present in user account')

                    if (AllRecipes.CS_DEVICE_AVAILABLE != 0) & (AllRecipes.PLUG_DEVICE_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSO_PL_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.CSO_PL_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as Window/door sensor and plug are present in user account')
                        else:
                            self.report_fail('Android App : CSO_PLUG_RECIPE template is not present')
                    else:
                        self.report_fail('Android App : Win/door Sensor and Plug are not present in user account')

                    if (AllRecipes.CS_DEVICE_AVAILABLE != 0) & (AllRecipes.PLUG_DEVICE_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSC_PL_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.CSC_PL_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as Window/door sensor and plug are present in user account')
                        else:
                            self.report_fail('Android App : CSC_PLUG_RECIPE template is not present ')
                    else:
                        self.report_fail('Android App : Win/door Sensor and Plug are not present in user account')

                    AllRecipes.scroll_on_recipe_templates(self)

                    # Checks Light Recipes Templates
                    if (AllRecipes.MS_DEVICE_AVAILABLE != 0) & (AllRecipes.BULB_DEVICE_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.MS_BU_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.MS_BU_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as motion sensor and bulb is present in user account')
                        else:
                            self.report_fail('Android App : MS_BULB_RECIPE template is not present')
                    else:
                        self.report_fail('Android App : Motion Sensor and Bulb are not present in user account')

                    if (AllRecipes.CS_DEVICE_AVAILABLE != 0) & (AllRecipes.BULB_DEVICE_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSO_BU_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.CSO_BU_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as Window/door sensor and bulb is present in user account')
                        else:
                            self.report_fail('Android App : CSO_BULB_RECIPE template is not present')
                    else:
                        self.report_fail('Android App : Win/door Sensor and Bulb are not present in user account')

                    if (AllRecipes.CS_DEVICE_AVAILABLE != 0) & (AllRecipes.BULB_DEVICE_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSC_BU_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.CSC_BU_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as Window/door sensor and bulb is present in user account')
                        else:
                            self.report_fail('Android App : CSC_BULB_RECIPE template is not present ')
                    else:
                        self.report_fail('Android App : Win/door Sensor and Bulb are not present in user account')

                        # Checks Heating Recipes Templates
                    if (AllRecipes.MS_DEVICE_AVAILABLE != 0) & (AllRecipes.HEATING_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.MS_HEAT_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.MS_HEAT_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as motion sensor and heating is present in user account')
                        else:
                            self.report_fail('Android App : MS_HEAT_RECIPE template is not present')
                    else:
                        self.report_done('Android App : Motion Sensor and Heating are not present in user account')

                    if (AllRecipes.CS_DEVICE_AVAILABLE != 0) & (AllRecipes.HEATING_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSO_HEAT_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.CSO_HEAT_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as Window/door sensor and heating is present in user account')
                        else:
                            self.report_fail('Android App : CSO_HEAT_RECIPE template is not present')
                    else:
                        self.report_done('Android App : Win/door Sensor and Heating are not present in user account')

                    if (AllRecipes.CS_DEVICE_AVAILABLE != 0) & (AllRecipes.HEATING_AVAILABLE != 0):
                        if self.wait_for_element_exist(*ActionsScreenLocators.CSC_HEAT_RECIPE):
                            recipe_text = self.driver.find_element(*ActionsScreenLocators.CSC_HEAT_RECIPE).text
                            self.report_pass(
                                'Android App : "' + recipe_text + '" template is present as Window/door sensor and heating is present in user account')
                        else:
                            self.report_fail('Android App : CSC_HEAT_RECIPE template is not present')
                    else:
                        self.report_done('Android App : Win/door Sensor and Heating are not present in user account')

                if self.wait_for_element_exist(*ActionsScreenLocators.THEN_BACK_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.THEN_BACK_BUTTON).click()
                print("All Templates are available as expected")
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_recipe_template Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Creates a new OnOff Recipe
    def createNewOnOffRecipe(self, strDevice, strDeviceState, strDuration, strSensor, strSensorState):
        if self.reporter.ActionStatus:
            try:
                # Checks presence and Selects the template as if needed
                if ("Motion sensor" in strSensor) & ("detects motion" in strSensorState):
                    ms_device_recipe_created = str(ActionsScreenLocators.DEVICE_TURN_MS_RECIPE)
                    ms_device_recipe_created = ms_device_recipe_created.replace("devicename", strDevice)
                    ms_device_recipe_created = ms_device_recipe_created.replace("devicestate", AllRecipes.DEVICE_STATE)
                    ms_device_recipe_created = ms_device_recipe_created.replace("sensor", strSensor)

                    # Checks presense of recipe if already created
                    if not AllRecipes.find_existing_recipe_all_recipes_page(self, ms_device_recipe_created):
                        self.report_step('Creating new Recipe')
                        if self.wait_for_element_exist(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON):
                            self.driver.find_element(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON).click()
                        # Selects the necessary template
                        if "Plug" in strDevice:
                            if self.wait_for_element_exist(*ActionsScreenLocators.MS_PL_RECIPE):
                                recipe_template = self.driver.find_element(*ActionsScreenLocators.MS_PL_RECIPE).text
                                self.driver.find_element(*ActionsScreenLocators.MS_PL_RECIPE).click()
                                self.report_done('Selected ' + recipe_template + ' Template')
                                AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState, strDuration,
                                                                          strSensor, strSensorState)
                        if ("Warm white light" in strDevice) or ("Tuneable light" in strDevice) or (
                                    "Colour light" in strDevice):
                            if self.wait_for_element_exist(*ActionsScreenLocators.MS_BU_RECIPE):
                                recipe_template = self.driver.find_element(*ActionsScreenLocators.MS_BU_RECIPE).text
                                self.driver.find_element(*ActionsScreenLocators.MS_BU_RECIPE).click()
                                self.report_done('Selected ' + recipe_template + ' Template')
                                AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState, strDuration,
                                                                          strSensor, strSensorState)
                            else:
                                AllRecipes.scroll_on_recipe_templates(self)
                                if self.wait_for_element_exist(*ActionsScreenLocators.MS_BU_RECIPE):
                                    recipe_template = self.driver.find_element(*ActionsScreenLocators.MS_BU_RECIPE).text
                                    self.driver.find_element(*ActionsScreenLocators.MS_BU_RECIPE).click()
                                    self.report_done('Selected ' + recipe_template + ' Template')
                                    AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                              strDuration, strSensor, strSensorState)
                                else:
                                    AllRecipes.scroll_on_recipe_templates(self)
                                    if self.wait_for_element_exist(*ActionsScreenLocators.MS_BU_RECIPE):
                                        recipe_template = self.driver.find_element(
                                            *ActionsScreenLocators.MS_BU_RECIPE).text
                                        self.driver.find_element(*ActionsScreenLocators.MS_BU_RECIPE).click()
                                        self.report_done('Selected ' + recipe_template + ' Template')
                                        AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                                  strDuration, strSensor,
                                                                                  strSensorState)
                    else:
                        self.report_pass(
                            'Android App : Such Recipe already exists , cannot create again : edited as needed')
                        print('Android App : Such Recipe already exists , cannot create again : editing now as needed')
                        self.driver.find_element(By.XPATH, ms_device_recipe_created).click()
                        AllRecipes.edit_then_on_off_recipe(self, strDevice, strDeviceState, strDuration)
                elif ("Win/door sensor" in strSensor) & ("opened" in strSensorState):
                    cso_device_recipe_created = str(ActionsScreenLocators.DEVICE_TURN_CSO_RECIPE)
                    cso_device_recipe_created = cso_device_recipe_created.replace("devicename", strDevice)
                    cso_device_recipe_created = cso_device_recipe_created.replace("devicestate",
                                                                                  AllRecipes.DEVICE_STATE)
                    cso_device_recipe_created = cso_device_recipe_created.replace("sensor", strSensor)

                    # Checks presense of recipe if already created
                    if not AllRecipes.find_existing_recipe_all_recipes_page(self, cso_device_recipe_created):
                        self.report_step('Creating new Recipe')
                        if self.wait_for_element_exist(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON):
                            self.driver.find_element(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON).click()
                            # Selects the necessary template
                            if "Plug" in strDevice:
                                if self.wait_for_element_exist(*ActionsScreenLocators.CSO_PL_RECIPE):
                                    recipe_template = self.driver.find_element(
                                        *ActionsScreenLocators.CSO_PL_RECIPE).text
                                    self.driver.find_element(*ActionsScreenLocators.CSO_PL_RECIPE).click()
                                    self.report_done('Selected ' + recipe_template + ' Template')
                                    AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                              strDuration, strSensor, strSensorState)
                            if ("Warm White light" in strDevice) or ("Tuneable light" in strDevice) or (
                                        "Colour light" in strDevice):
                                if self.wait_for_element_exist(*ActionsScreenLocators.CSO_BU_RECIPE):
                                    recipe_template = self.driver.find_element(
                                        *ActionsScreenLocators.CSO_BU_RECIPE).text
                                    self.driver.find_element(*ActionsScreenLocators.CSO_BU_RECIPE).click()
                                    self.report_done('Selected ' + recipe_template + ' Template')
                                    AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                              strDuration, strSensor, strSensorState)
                                else:
                                    AllRecipes.scroll_on_recipe_templates(self)
                                    if self.wait_for_element_exist(*ActionsScreenLocators.CSO_BU_RECIPE):
                                        recipe_template = self.driver.find_element(
                                            *ActionsScreenLocators.CSO_BU_RECIPE).text
                                        self.driver.find_element(*ActionsScreenLocators.CSO_BU_RECIPE).click()
                                        self.report_done('Selected ' + recipe_template + ' Template')
                                        AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                                  strDuration, strSensor,
                                                                                  strSensorState)
                                    else:
                                        AllRecipes.scroll_on_recipe_templates(self)
                                        if self.wait_for_element_exist(*ActionsScreenLocators.CSO_BU_RECIPE):
                                            recipe_template = self.driver.find_element(
                                                *ActionsScreenLocators.CSO_BU_RECIPE).text
                                            self.driver.find_element(*ActionsScreenLocators.CSO_BU_RECIPE).click()
                                            self.report_done('Selected ' + recipe_template + ' Template')
                                            AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                                      strDuration, strSensor,
                                                                                      strSensorState)
                    else:
                        self.report_pass(
                            'Android App : Such Recipe already exists , cannot create again : edited as needed')
                        print('Android App : Such Recipe already exists , cannot create again : editing now as needed')
                        self.driver.find_element(By.XPATH, cso_device_recipe_created).click()
                        AllRecipes.edit_then_on_off_recipe(self, strDevice, strDeviceState, strDuration)
                elif ("Win/door sensor" in strSensor) & ("closed" in strSensorState):
                    csc_device_recipe_created = str(ActionsScreenLocators.DEVICE_TURN_CSC_RECIPE)
                    csc_device_recipe_created = csc_device_recipe_created.replace("devicename", strDevice)
                    csc_device_recipe_created = csc_device_recipe_created.replace("devicestate",
                                                                                  AllRecipes.DEVICE_STATE)
                    csc_device_recipe_created = csc_device_recipe_created.replace("sensor", strSensor)
                    # Checks presense of recipe if already created
                    if not AllRecipes.find_existing_recipe_all_recipes_page(self, csc_device_recipe_created):
                        self.report_step('Creating new Recipe')
                        if self.wait_for_element_exist(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON):
                            self.driver.find_element(*ActionsScreenLocators.ADD_A_NEW_RECIPE_BUTTON).click()
                            # Selects the necessary template
                            if "Plug" in strDevice:
                                if self.wait_for_element_exist(*ActionsScreenLocators.CSC_PL_RECIPE):
                                    recipe_template = self.driver.find_element(
                                        *ActionsScreenLocators.CSC_PL_RECIPE).text
                                    self.driver.find_element(*ActionsScreenLocators.CSC_PL_RECIPE).click()
                                    self.report_done('Selected ' + recipe_template + ' Template')
                                    AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                              strDuration, strSensor, strSensorState)
                            if ("Warm white light" in strDevice) or ("Tuneable light" in strDevice) or (
                                        "Colour light" in strDevice):
                                if self.wait_for_element_exist(*ActionsScreenLocators.CSC_BU_RECIPE):
                                    recipe_template = self.driver.find_element(
                                        *ActionsScreenLocators.CSC_BU_RECIPE).text
                                    self.driver.find_element(*ActionsScreenLocators.CSC_BU_RECIPE).click()
                                    AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                              strDuration, strSensor, strSensorState)
                                    self.report_done('Selected ' + recipe_template + ' Template')
                                else:
                                    AllRecipes.scroll_on_recipe_templates(self)
                                    if self.wait_for_element_exist(*ActionsScreenLocators.CSC_BU_RECIPE):
                                        recipe_template = self.driver.find_element(
                                            *ActionsScreenLocators.CSC_BU_RECIPE).text
                                        self.driver.find_element(*ActionsScreenLocators.CSC_BU_RECIPE).click()
                                        self.report_done('Selected ' + recipe_template + ' Template')
                                        AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                                  strDuration, strSensor,
                                                                                  strSensorState)
                                    else:
                                        AllRecipes.scroll_on_recipe_templates(self)
                                        if self.wait_for_element_exist(*ActionsScreenLocators.CSC_BU_RECIPE):
                                            recipe_template = self.driver.find_element(
                                                *ActionsScreenLocators.CSC_BU_RECIPE).text
                                            self.driver.find_element(*ActionsScreenLocators.CSC_BU_RECIPE).click()
                                            self.report_done('Selected ' + recipe_template + ' Template')
                                            AllRecipes.select_create_when_then_on_off(self, strDevice, strDeviceState,
                                                                                      strDuration, strSensor,
                                                                                      strSensorState)
                    else:
                        self.report_pass(
                            'Android App : Such Recipe already exists , cannot create again : edited as needed')
                        print('Android App : Such Recipe already exists , cannot create again : editing now as needed')
                        self.driver.find_element(By.XPATH, csc_device_recipe_created).click()
                        AllRecipes.edit_then_on_off_recipe(self, strDevice, strDeviceState, strDuration)
            except:
                self.report_fail('Android App : NoSuchElementException: in createNewOnOffRecipe Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

            # Selects when and then for a new OnOff recipe

    def select_create_when_then_on_off(self, strDevice, strDeviceState, strDuration, strSensor, strSensorState):
        if self.reporter.ActionStatus:
            try:
                # Selects the when
                if self.wait_for_element_exist(*ActionsScreenLocators.MULTI_WHEN_PICKER):
                    if strSensor in self.driver.find_element(*ActionsScreenLocators.MULTI_WHEN_PICKER).text:
                        self.report_pass("When part is preselected")
                    elif self.wait_for_element_exist(*ActionsScreenLocators.NOTIFY_WHEN_PICKER):
                        self.driver.find_element(*ActionsScreenLocators.NOTIFY_WHEN_PICKER).click()
                        device = str(ActionsScreenLocators.WHEN_CHOOSE_DEVICE)
                        devicetoselect = device.replace("device", strSensor)
                        if self.wait_for_element_exist(By.XPATH, devicetoselect):
                            self.driver.find_element(By.XPATH, devicetoselect).click()
                            self.report_done('Selected  ' + strSensor)
                            self.driver.find_element(*ActionsScreenLocators.WHEN_OK_BUTTON).click()
                        else:
                            self.report_fail('Unable to select the device')
                    else:
                        self.report_fail("Problem in When part selection")

                # Selects the then variables

                if not self.wait_for_element_exist(*ActionsScreenLocators.MULTI_THEN_PICKER):
                    print("Then part is preselected , now setting the other details as needed")

                elif self.wait_for_element_exist(*ActionsScreenLocators.NOTIFY_THEN_PICKER):
                    self.driver.find_element(*ActionsScreenLocators.NOTIFY_THEN_PICKER).click()
                else:
                    self.report_fail('Problem while selecting then picker')

                # Selects the device
                if self.wait_for_element_exist(*ActionsScreenLocators.THEN_SCREEN_DEVICE_NAME_PRESELECTED):
                    if strDevice in self.driver.find_element(
                            *ActionsScreenLocators.THEN_SCREEN_DEVICE_NAME_PRESELECTED).text:
                        print(strDevice + " is already selected")
                    else:
                        if self.wait_for_element_exist(*ActionsScreenLocators.THEN_SCREEN_DEVICE_NAME):
                            self.driver.find_element(*ActionsScreenLocators.THEN_SCREEN_DEVICE_NAME).click()
                        then_screen_device_name_value = str(ActionsScreenLocators.THEN_SCREEN_DEVICE_NAME_VALUE)
                        then_screen_device_name_value = then_screen_device_name_value.replace("value", strDevice)
                        if self.wait_for_element_exist(By.XPATH, then_screen_device_name_value):
                            self.driver.find_element(By.XPATH, then_screen_device_name_value).click()
                            self.report_done('Selected ' + strDevice)
                            if self.wait_for_element_exist(*ActionsScreenLocators.OK_BUTTON):
                                self.driver.find_element(*ActionsScreenLocators.OK_BUTTON).click()
                            else:
                                self.report_fail('Ok button not found')
                        else:
                            print("Problem selecting device")

                # Selects the On/Off
                self.driver.find_element(*ActionsScreenLocators.THEN_SCREEN_DEVICE_STATE).click()
                then_device_state_value = str(ActionsScreenLocators.THEN_SCREEN_DEVICE_STATE_VALUE)
                then_device_state_value = then_device_state_value.replace("value", strDeviceState)
                if self.wait_for_element_exist(By.XPATH, then_device_state_value):
                    self.driver.find_element(By.XPATH, then_device_state_value).click()
                    self.report_done('Selected  ' + strDeviceState)
                    self.driver.find_element(*ActionsScreenLocators.OK_BUTTON).click()
                else:
                    print("Problem selecting device state")

                # Selects the duration
                self.driver.find_element(*ActionsScreenLocators.THEN_SCREEN_DEVICE_DURATION).click()
                then_device_duration_value = str(ActionsScreenLocators.THEN_SCREEN_DEVICE_DURATION_VALUE)
                then_device_duration_value = then_device_duration_value.replace("value", strDuration)
                if self.wait_for_element_exist(By.XPATH, then_device_duration_value):
                    self.driver.find_element(By.XPATH, then_device_duration_value).click()
                    self.report_done('Selected  ' + strDuration)
                    self.driver.find_element(*ActionsScreenLocators.OK_BUTTON).click()
                else:
                    print("Problem selecting device duration")

                # Saving activities
                if self.wait_for_element_exist(*ActionsScreenLocators.THEN_BACK_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.THEN_BACK_BUTTON).click()
                if self.wait_for_element_exist(*ActionsScreenLocators.SAVE_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.SAVE_BUTTON).click()
                    time.sleep(3)
                    print("Recipe created successfully")
                self.report_pass('Android App : Recipe created successfully')
                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in select_create_when_then_notify Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

            # Edits then for a existing OnOff recipe

    def edit_then_on_off_recipe(self, strDevice, strDeviceState, strDuration):
        if self.reporter.ActionStatus:
            try:
                # Edits then part
                if not self.wait_for_element_exist(*ActionsScreenLocators.MULTI_THEN_PICKER):
                    print("Then part is preselected , now setting the other details as needed")
                elif self.wait_for_element_exist(*ActionsScreenLocators.NOTIFY_THEN_PICKER):
                    self.driver.find_element(*ActionsScreenLocators.NOTIFY_THEN_PICKER).click()
                else:
                    self.report_fail('Problem while selecting then picker')

                # Selects the On/Off

                self.driver.find_element(*ActionsScreenLocators.THEN_SCREEN_DEVICE_STATE).click()
                then_device_state_value = str(ActionsScreenLocators.THEN_SCREEN_DEVICE_STATE_VALUE)
                then_device_state_value = then_device_state_value.replace("value", strDeviceState)
                if self.wait_for_element_exist(By.XPATH, then_device_state_value):
                    self.driver.find_element(By.XPATH, then_device_state_value).click()
                    self.report_done('Selected ' + strDeviceState)
                    self.driver.find_element(*ActionsScreenLocators.OK_BUTTON).click()
                else:
                    print("Problem selecting device state")

                # Selects the duration
                if self.wait_for_element_exist(*ActionsScreenLocators.THEN_SCREEN_DEVICE_DURATION):
                    self.driver.find_element(*ActionsScreenLocators.THEN_SCREEN_DEVICE_DURATION).click()
                    then_device_duration_value = str(ActionsScreenLocators.THEN_SCREEN_DEVICE_DURATION_VALUE)
                    then_device_duration_value = then_device_duration_value.replace("value", strDuration)
                if self.wait_for_element_exist(By.XPATH, then_device_duration_value):
                    self.driver.find_element(By.XPATH, then_device_duration_value).click()
                    self.report_done('Selected ' + strDuration)
                    self.driver.find_element(*ActionsScreenLocators.OK_BUTTON).click()
                else:
                    print("Problem selecting recipe duration")

                # Saving activities
                if self.wait_for_element_exist(*ActionsScreenLocators.THEN_BACK_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.THEN_BACK_BUTTON).click()
                if self.wait_for_element_exist(*ActionsScreenLocators.SAVE_BUTTON):
                    self.driver.find_element(*ActionsScreenLocators.SAVE_BUTTON).click()
                self.report_pass('Android App : Recipe updated successfully')
                print("Android App : Recipe updated successfully")
                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in edit_then_on_off_recipe Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class HoneyComb(BasePage):
    def honeycomb_preview_verify(self):
        intCounter = 0
        strSubtitleText = ""
        strTitleText = ""
        strMainText = ""
        strText = ""

        if self.wait_for_element_exist(*HoneycombDashboardLocators.PREVIEW_HONEYCOMB_SUBTITLE_TEXTVIEW):
            strSubtitleText = self.driver.find_element(
                *HoneycombDashboardLocators.PREVIEW_HONEYCOMB_SUBTITLE_TEXTVIEW).get_attribute("text")
            if strSubtitleText == "Welcome to your":
                intCounter += 1

        if self.wait_for_element_exist(*HoneycombDashboardLocators.PREVIEW_HONEYCOMB_TITLETEXT_TEXTVIEW):
            strTitleText = self.driver.find_element(
                *HoneycombDashboardLocators.PREVIEW_HONEYCOMB_TITLETEXT_TEXTVIEW).get_attribute("text")
            if strTitleText == "Hive Dashboard!":
                intCounter += 1

        if self.wait_for_element_exist(*HoneycombDashboardLocators.PREVIEW_HONEYCOMB_MAINTEXT_TEXTVIEW):
            strMainText = self.driver.find_element(
                *HoneycombDashboardLocators.PREVIEW_HONEYCOMB_MAINTEXT_TEXTVIEW).get_attribute("text")
            if strMainText == "Here you can take a glance at the status of your home. Easily control and navigate between devices with one tap.":
                intCounter += 1

        if self.wait_for_element_exist(*HoneycombDashboardLocators.PREVIEW_HONEYCOMB_GETSTARTED_BUTTON):
            strText = self.driver.find_element(
                *HoneycombDashboardLocators.PREVIEW_HONEYCOMB_GETSTARTED_BUTTON).get_attribute("text")
            if strText == "Show me my dashboard":
                intCounter += 1

        if intCounter == 4:
            self.report_pass('Android-App Honeycomb Preview : The honeycpmb preview is successfully displayed')
            print(strSubtitleText + " " + strTitleText + " " + strMainText + " " + strText)
        else:
            self.report_fail('Android-App Honeycomb Preview : The honeycpmb preview is not successfully displayed')
            print(strSubtitleText + " " + strTitleText + " " + strMainText + " " + strText)

    def honeycomb_preview_click(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDashboardLocators.PREVIEW_HONEYCOMB_GETSTARTED_BUTTON):
                    self.driver.find_element(*HoneycombDashboardLocators.PREVIEW_HONEYCOMB_GETSTARTED_BUTTON).click()

            except:
                self.report_fail('Android-App : NoSuchElementException: in Honeycomb Preview Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def honeycomb_validate_status(self, strDevice, strDeviceType, strStatus):
        self.strDevice = strDevice
        self.strDeviceType = strDeviceType
        self.strStatus = strStatus
        strDesc = ""
        blnFlag = False
        strElement = ""
        DEVICE_ID = "deviceSlot"
        try:
            if self.wait_for_element_exist(*HoneycombDashboardLocators.REFRESH_BUTTON_V6):

                self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()

                print("refreshing")
                time.sleep(15)

                strDeviceName = list(HoneycombDashboardLocators.DASHBOARD_ICON_FRAME_LAYOUT)
                strExpected = self.strDevice + ". Your " + self.strDeviceType + " is currently " + self.strStatus + "."

                strElement = DEVICE_ID
                strElementID = DEVICE_ID + "1"

                print(strDeviceName)
                strDeviceName[1] = strDeviceName[1].replace("DEVICENAME", strElementID)
                strProperty = tuple(strDeviceName)

                intRange = 15
                for intCounter in range(1, intRange):

                    if intCounter == 8:
                        self.dashboardSwipe(False)

                    oElement = self.driver.find_element(*strProperty)
                    strDesc = oElement.get_attribute('name')
                    strDescDeviceName = strDesc.split(".")
                    if self.strDevice.lower() == strDescDeviceName[0].lower():
                        self.report_pass(
                            'Android-App Honeycomb Dashboard : Element is found for device - ' + self.strDevice)

                        blnFlag = True
                        if strExpected.lower() in strDesc.lower():

                            self.report_pass(
                                'Android-App Honeycomb Dashboard : The honeycomb Dashboard is successfully displayed '
                                'for - ' + self.strDevice + " " + strExpected)
                            print(strDesc)

                        else:
                            self.report_fail(
                                'Android-App Honeycomb Dashboard : The honeycomb Dashboard is not successfully '
                                'displayed for - ' + self.strDevice + " Expected - " + strExpected + " Actual " + strDesc)
                            print(strDesc)
                        if intCounter > 7:
                            self.dashboardSwipe()
                        break

                    if intCounter == 7:
                        strElementID = strElement + str(intCounter)
                    else:
                        strElementID = strElement + str(intCounter % 7)
                    strNextElementID = strElement + str((intCounter % 7) + 1)
                    print(strDeviceName)
                    strDeviceName[1] = strDeviceName[1].replace(strElementID, strNextElementID)
                    strProperty = tuple(strDeviceName)

                if blnFlag is False:
                    self.dashboardSwipe()
                    self.report_fail(
                        'Android-App Honeycomb Dashboard : Element is not found for device - ' + self.strDevice)
                    print(strDesc)

        except:

            self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Verify Icon in Dashboard
    def honeycomb_verifyIconHierarchy(self, context):
        listDevice = []
        self.strDeviceType = []
        self.strStatus = []
        strElement = ""
        blnFlag = False
        strDevice = ""
        listDeviceType = []
        listDeviceName = []
        strPreviousDeviceName = ""
        strPreviousDeviceType = ""
        strFirstIcon = ""
        intCounter = 1
        DEVICE_ID = "deviceSlot"
        try:
            if self.wait_for_element_exist(*HoneycombDashboardLocators.REFRESH_BUTTON_V6):

                self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()

                print("refreshing")
                time.sleep(7)
                self.dashboardSwipe()

                time.sleep(7)

                for intCounter in range(1, 29):

                    strElement = DEVICE_ID
                    if intCounter == 7:
                        strElementID = strElement + str(intCounter)
                    else:
                        strElementID = strElement + str(intCounter % 7)

                    strDeviceName = list(HoneycombDashboardLocators.DASHBOARD_ICON_FRAME_LAYOUT)
                    strDeviceName[1] = strDeviceName[1].replace("DEVICENAME", strElementID)
                    strProperty = tuple(strDeviceName)

                    if intCounter > 7 and (intCounter % 7) == 1:
                        self.dashboardSwipe(False)
                        time.sleep(7)
                        self.report_done(
                            'Dashboard : The swipe action is triggered ')
                    if not self.wait_for_element_exist(*strProperty):
                        break
                    oElement = self.driver.find_element(*strProperty)
                    strDesc = oElement.get_attribute('name')

                    if intCounter == 8 and strDesc in strFirstIcon:
                        break

                    if (intCounter % 7) == 1:
                        strFirstIcon = strFirstIcon + strDesc

                    if '.' in strDesc:
                        strDevice = strDesc.split('.')[0]
                        strDeviceType = (strDesc.split('Your ')[1]).split(' is')[0]
                        strDeviceStatus = (strDesc.split('currently ')[1]).split('.')[0]

                        strText = strDevice + ";" + strDeviceType + ";" + strDeviceStatus
                    else:
                        break

                    listDeviceType.append(strDeviceType)
                    listDevice.append(strText.lower())
                    listDeviceName.append(strDevice)

                for intCount in range(0, int(intCounter / 7)):
                    self.dashboardSwipe()
                    time.sleep(5)

                for intCounter in range(0, len(listDeviceName)):

                    if intCounter > 0:
                        strPreviousDeviceType = listDeviceType[intCounter - 1]
                        strPreviousDeviceName = listDeviceName[intCounter - 1]

                    if listDeviceType[intCounter].lower() == 'heating':
                        if intCounter == 0:
                            self.report_pass(
                                'Android-App Honeycomb Dashboard : The heating is displayed at central as expected ')
                        elif listDeviceType[intCounter - 1].lower() == 'heating' and listDeviceName[intCounter - 1] \
                                <= listDeviceName[intCounter]:
                            self.report_pass(
                                'Android-App Honeycomb Dashboard : The heating is displayed at central as expected ')
                        else:
                            self.report_fail(
                                'Android-App Honeycomb Dashboard : The heating is not displayed as expected ')

                    if listDeviceType[intCounter].lower() == 'boiler':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         [''], strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'hot water':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler'], strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'active plug':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water'], strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'warm white light':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug'], strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'tunable light':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug', 'warm white light'],
                                                         strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'colour Light':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug', 'warm white light',
                                                          'tunable light'],
                                                         strPreviousDeviceName, strPreviousDeviceType,
                                                         str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'motion sensor':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug', 'warm white light',
                                                          'tunable light', 'colour Light'],
                                                         strPreviousDeviceName, strPreviousDeviceType,
                                                         str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'window or door sensor':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug', 'warm white light',
                                                          'tunable light', 'colour Light', 'motion sensor'],
                                                         strPreviousDeviceName, strPreviousDeviceType,
                                                         str(intCounter + 1), context)

            else:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

        except:

            self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Verify the device list screen
    def devicelist_verify(self):

        if self.wait_for_element_exist(*HoneycombDashboardLocators.DASHBOARD_ICON):
            self.report_done(' User is on Dashboard screen ')
            if self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                time.sleep(2)
                self.report_pass(' User is now on Device list screen ')
            else:
                self.report_fail(
                    'Exit Condition: Not able to Navigate to Device list screen, Dashboard icon is not displayed')
                exit()

        elif self.wait_for_element_exist(*HoneycombDashboardLocators.DEVICELIST_NAMEICON_VIEW):
            self.report_pass(' User is already on Device list screen ')
        elif self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
            self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
            self.report_done(' User is on Dashboard screen ')
            time.sleep(2)
            self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
            self.report_pass(' User is now on Device list screen ')
        else:
            self.report_fail('Exit Condition: Not able to Navigate to Device list screen')
            exit()

    # Verify title bar in dashboard
    def honeycomb_verifyTitle(self):

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDashboardLocators.REFRESH_BUTTON_V6):
                    self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()
                    time.sleep(4)

                if self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_TITLE_VIEW):

                    self.reporter.HTML_TC_BusFlowKeyword_Initialize(
                        'Validate Title')
                    self.report_done('Title is displayed ')

                    strDesc = self.driver.find_element(*HoneycombDashboardLocators.
                                                       HONEYCOMB_TITLE_VIEW).get_attribute('text')

                    if strDesc == 'My Hive Home':
                        self.report_pass('Title is displayed succesfully as - ' + strDesc)
                    else:
                        self.report_fail(' Title is not displayed succesfully '
                                         ' Actual - ' + strDesc + ' Expected - My Hive Home')

                    self.reporter.HTML_TC_BusFlowKeyword_Initialize(
                        'Validate SubTitle ')

                    if self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_SUBBARTITLE_VIEW):
                        self.report_pass(' Sub Title element is displayed succesfully')
                    else:
                        self.report_fail(' Sub Title element is not displayed succesfully')

                    strDesc = self.driver.find_element(*HoneycombDashboardLocators.
                                                       HONEYCOMB_SUBBARTITLE_VIEW).get_attribute('text')

                    if strDesc == "Last updated: Less than 1m ago":
                        self.report_pass(' Sub Title is displayed succesfully as - ' + strDesc)
                    else:
                        self.report_fail(' Sub Title is not displayed succesfully  Actual - ' + strDesc)

                    blnFlag = False
                    self.reporter.HTML_TC_BusFlowKeyword_Initialize(
                        'Validate SubTitle Auto refresh')
                    for intCounter in range(1, 90):
                        time.sleep(2)
                        if not self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_SUBBARTITLE_VIEW):
                            break

                        strDesc = self.driver.find_element(*HoneycombDashboardLocators.
                                                           HONEYCOMB_SUBBARTITLE_VIEW).get_attribute('text')
                        if strDesc == "Last updated: 2m ago":
                            self.report_pass(' Sub Title is auto updated succesfully as - ' + strDesc)
                            blnFlag = True
                            time.sleep(2)
                            break

                    if not blnFlag:
                        self.report_fail('Sub Title is not auto updated succesfully Actual - '
                                         + strDesc + ' Expected - Last updated: 2m ago')

                else:
                    self.report_fail(' Title is not displayed ')

            except:
                self.report_fail('Android-App : NoSuchElementException: in Honeycomb Preview Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

        time.sleep(5)

    # Fetch status and verify for dashboard icons
    def honeycomb_fetch_status(self, listDeviceExpected, context):
        listDevice = []
        self.strDeviceType = []
        self.strStatus = []
        strFirstIcon = ""
        intCounter = 1
        intTotalDevice = len(listDeviceExpected)
        strLog = ""
        strDesc = ""
        blnResult = True
        strStatus = ""
        blnSwipe = False
        DEVICE_ID = "deviceSlot"

        try:
            if self.wait_for_element_exist(*HoneycombDashboardLocators.REFRESH_BUTTON_V6):

                self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()
                print("refreshing")
                time.sleep(15)

                self.dashboardSwipe()
                time.sleep(2)
                self.reporter.HTML_TC_BusFlowKeyword_Initialize(
                    'Additional Dashboard Screen ')
                for intCounter in range(1, 29):

                    strElement = DEVICE_ID
                    if intCounter == 7:
                        strElementID = strElement + str(intCounter)
                    else:
                        strElementID = strElement + str(intCounter % 7)

                    strDeviceName = list(HoneycombDashboardLocators.DASHBOARD_ICON_FRAME_LAYOUT)
                    strDeviceName[1] = strDeviceName[1].replace("DEVICENAME", strElementID)
                    strProperty = tuple(strDeviceName)

                    if (intCounter % 7) == 1 and intCounter > 7:
                        self.dashboardSwipe(False)
                        time.sleep(2)
                        self.report_done('Swipe action is triggerd on Dashboard')
                        blnSwipe = True

                    if not self.wait_for_element_exist(*strProperty):
                        break

                    oElement = self.driver.find_element(*strProperty)
                    strDesc = oElement.get_attribute('name')

                    if intCounter > 7 and (intCounter % 7) == 1:

                        if strDesc in strFirstIcon:
                            if intTotalDevice == 7:
                                self.report_pass('Devices are equal to 7, Additional Screen is not created as Expected')
                            else:
                                self.report_fail(
                                    'Devices more than 7, Additional Screen is not created, not as Expected')
                            break
                        else:
                            self.report_pass('Another dashboard screen is created once it got full as Expected')

                        strFirstIcon = strFirstIcon + strDesc

                    if '.' in strDesc:
                        strDevice = strDesc.split('.')[0]
                        strDeviceType = (strDesc.split('Your ')[1]).split(' is')[0]
                        strDeviceStatus = (strDesc.split('currently ')[1]).split('.')[0]

                        strText = strDevice + ";" + strDeviceType + ";" + strDeviceStatus

                    else:
                        break

                    listDevice.append(strText.lower())

                for intCount in range(0, int(intCounter / 7)):
                    self.dashboardSwipe()
                    time.sleep(2)

                if intTotalDevice < 7:
                    self.dashboardSwipe(False)
                    time.sleep(2)
                    if not self.wait_for_element_exist(*HoneycombDashboardLocators.DASHBOARD_ICON):
                        self.report_fail('Swiping has made the icons disappear')
                    else:
                        oElement = self.driver.find_element(*HoneycombDashboardLocators.DASHBOARD_ICON)
                        strDesc = oElement.get_attribute('name')
                        if strFirstIcon == strDesc:
                            self.report_pass('Devices Less than 7, Additional Screen is not created as Expected')
                        else:
                            self.report_fail('Devices Less than 7, Additional Screen is created not as Expected')
                    self.dashboardSwipe()
                    time.sleep(2)

                self.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate number of devices and empty slots ')
                self.report_done('Total Number of devices - ' + str(intTotalDevice))
                strLog = context.rFM.getTableLogs("", "Number of devices", str(len(listDeviceExpected)),
                                                  str(len(listDevice)), "deviceproperties")
                if len(listDeviceExpected) == len(listDevice):

                    context.reporter.ReportEvent('Test Validation', strLog, "Pass", "Center")
                else:
                    context.reporter.ReportEvent('Test Validation', strLog, "Fail", "Center")

                if intCounter == intTotalDevice + 1:
                    if intTotalDevice % 7 == 0 and strDesc in strFirstIcon:
                        strLog = context.rFM.getTableLogs("", "Number of Empty Slots", "0",
                                                          "0", "deviceproperties")
                        strStatus = "PASS"
                    elif intTotalDevice % 7 != 0 and ('.' in strDesc) == False:
                        strLog = context.rFM.getTableLogs("", "Number of Empty Slots", str(7 - (intTotalDevice % 7)),
                                                          str(7 - (intTotalDevice % 7)), "deviceproperties")
                        strStatus = "PASS"

                    else:
                        strLog = context.rFM.getTableLogs("", "Number of Empty Slots",
                                                          str(7 - (intTotalDevice % 7)),
                                                          "||Less Than " + str(7 - (intTotalDevice % 7)),
                                                          "deviceproperties")
                        strStatus = "FAIL"

                else:
                    strStatus = "FAIL"
                    strLog = context.rFM.getTableLogs("", "Number of Empty Slots",
                                                      str(7 - (intTotalDevice % 7)),
                                                      "||More Than " + str(7 - (intTotalDevice % 7)),
                                                      "deviceproperties")

                context.reporter.ReportEvent('Test Validation', strLog, strStatus, "Center")

                for strExpectedItem in listDeviceExpected:

                    strDevice, strDeviceType, strDeviceStatus = strExpectedItem.split(';')
                    self.reporter.HTML_TC_BusFlowKeyword_Initialize('Device Status - ' + strDevice)
                    blnFlag = False

                    for strItem in listDevice:

                        if strDevice in strItem:

                            strActualDevice, strActualDeviceType, strActualStatus = strItem.split(';')
                            if strActualDevice == strDevice:
                                strLog = context.rFM.getTableLogs("", "Icon ", "Displayed",
                                                                  "Displayed", "deviceproperties")

                                strStatus = "PASS"

                                if strActualDeviceType == strDeviceType:
                                    strStatus = "PASS"

                                else:
                                    strStatus = "FAIL"
                                    strActualDeviceType = "||" + strActualDeviceType

                                if strActualStatus.split('.')[0] == strDeviceStatus.split('.')[0]:
                                    strStatus = "PASS"
                                else:
                                    strStatus = "FAIL"
                                    strActualStatus = "||" + strActualStatus

                                strLog = context.rFM.getTableLogs(strLog, "Type ",
                                                                  strDeviceType,
                                                                  strActualDeviceType, "deviceproperties")
                                strLog = context.rFM.getTableLogs(strLog, "Status ",
                                                                  strDeviceStatus,
                                                                  strActualStatus, "deviceproperties")
                                blnFlag = True
                    if not blnFlag:
                        strStatus = "FAIL"
                        strLog = context.rFM.getTableLogs("", "Icon", "Displayed", "||Not Displayed",
                                                          "deviceproperties")

                    context.reporter.ReportEvent('Test Validation', strLog, strStatus, "Center")

            else:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

        except:

            self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Validate hierarchy in dashboard
    def honeycomb_ValidateHierarchy(self, strDeviceName, strDeviceType, listPreviousDevices, strPreviousDeviceName,
                                    strPreviousDeviceType, strPosition, context):
        strStatus = ""
        self.reporter.HTML_TC_BusFlowKeyword_Initialize('Postion of Device - ' + strDeviceName)
        strLog = context.rFM.getTableLogs("", strDeviceName, strDeviceType, strPosition, "devicehierarchy")
        if strPreviousDeviceType.lower() in listPreviousDevices or strPreviousDeviceType == '':
            strStatus = "PASS"
        elif strPreviousDeviceType.lower() == strDeviceType.lower() and strPreviousDeviceName <= strDeviceName:
            strStatus = "PASS"
        else:
            strStatus = "FAIL"
        context.reporter.ReportEvent('Test Validation', strLog, strStatus, "Center")

    # Fetch status and verify for device list icons
    def devicelist_fetch_status(self, listDeviceExpected, context):
        listDevice = []
        self.strDeviceType = []
        self.strStatus = []
        intCount = 1
        strStatus = ""
        intElement = 1
        try:
            if self.wait_for_element_exist(*HoneycombDashboardLocators.REFRESH_BUTTON_V6):

                self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()

                print("refreshing")
                time.sleep(15)

                for intCounter in range(1, 29):
                    strDeviceName = list(HoneycombDashboardLocators.DEVICELIST_NAME_VIEW)
                    if intCounter > 8:
                        intElement = 8
                    else:
                        intElement = intCounter
                    strElementID = str(intElement)
                    strDeviceName[1] = strDeviceName[1].replace("DEVICEINDEX", strElementID)

                    strProperty = tuple(strDeviceName)

                    if not self.wait_for_element_exist(*strProperty):
                        break

                    oElement = self.driver.find_element(*strProperty)
                    strDesc = oElement.get_attribute('name')

                    if self.wait_for_element_exist(*strProperty):
                        strDevice = strDesc.split('.')[0]
                        strDeviceType = (strDesc.split('Your ')[1]).split(' is')[0]
                        strDeviceStatus = (strDesc.split('currently ')[1]).split('.')[0]

                        strText = strDevice + ";" + strDeviceType + ";" + strDeviceStatus

                    else:
                        break

                    if intCounter > 7:
                        self.driver.swipe(288, 629, 288, 384, 1000)
                        time.sleep(3)

                    if strText.lower() in listDevice:
                        break
                    else:
                        listDevice.append(strText.lower())

                    intCount = intCounter

                self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()
                time.sleep(3)

                strLog = context.rFM.getTableLogs("", "Number of devices", str(len(listDeviceExpected)),
                                                  str(len(listDevice)), "deviceproperties")
                if len(listDeviceExpected) == len(listDevice):

                    context.reporter.ReportEvent('Test Validation', strLog, "Pass", "Center")
                else:
                    context.reporter.ReportEvent('Test Validation', strLog, "Fail", "Center")

                for strExpectedItem in listDeviceExpected:

                    strDevice, strDeviceType, strDeviceStatus = strExpectedItem.split(';')
                    self.reporter.HTML_TC_BusFlowKeyword_Initialize('Device Status - ' + strDevice)
                    blnFlag = False

                    for strItem in listDevice:

                        if strDevice in strItem:

                            strActualDevice, strActualDeviceType, strActualStatus = strItem.split(';')
                            if strActualDevice == strDevice:
                                strLog = context.rFM.getTableLogs("", "Icon ", "Displayed",
                                                                  "Displayed", "deviceproperties")

                                strStatus = "PASS"

                                if strActualDeviceType == strDeviceType:
                                    strStatus = "PASS"

                                else:
                                    strStatus = "FAIL"
                                    strActualDeviceType = "||" + strActualDeviceType

                                if strActualStatus.split('.')[0] == strDeviceStatus.split('.')[0]:
                                    strStatus = "PASS"
                                else:
                                    strStatus = "FAIL"
                                    strActualStatus = "||" + strActualStatus

                                strLog = context.rFM.getTableLogs(strLog, "Type ",
                                                                  strDeviceType,
                                                                  strActualDeviceType, "deviceproperties")
                                strLog = context.rFM.getTableLogs(strLog, "Status ",
                                                                  strDeviceStatus,
                                                                  strActualStatus, "deviceproperties")
                                blnFlag = True
                    if not blnFlag:
                        strStatus = "FAIL"
                        strLog = context.rFM.getTableLogs("", "Icon", "Displayed", "||Not Displayed",
                                                          "deviceproperties")

                    context.reporter.ReportEvent('Test Validation', strLog, strStatus, "Center")

                self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()

            else:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

        except:

            self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Validate hierarchy in devicelist
    def deviceList_verifyIconHierarchy(self, context):
        listDevice = []
        self.strDeviceType = []
        self.strStatus = []
        strElement = ""
        blnFlag = False
        strDevice = ""
        listDeviceType = []
        listDeviceName = []
        strPreviousDeviceName = ""
        strPreviousDeviceType = ""
        strFirstIcon = ""
        intCounter = 1
        intElement = 1
        try:
            if self.wait_for_element_exist(*HoneycombDashboardLocators.REFRESH_BUTTON_V6):

                self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()

                print("refreshing")
                time.sleep(15)

                for intCounter in range(1, 29):
                    strDeviceName = list(HoneycombDashboardLocators.DEVICELIST_NAME_VIEW)
                    if intCounter > 8:
                        intElement = 8
                    else:
                        intElement = intCounter
                    strElementID = str(intElement)
                    strDeviceName[1] = strDeviceName[1].replace("DEVICEINDEX", strElementID)

                    strProperty = tuple(strDeviceName)

                    if not self.wait_for_element_exist(*strProperty):
                        break

                    oElement = self.driver.find_element(*strProperty)
                    strDesc = oElement.get_attribute('name')

                    strDevice = strDesc.split('.')[0]
                    strDeviceType = (strDesc.split('Your ')[1]).split(' is')[0]
                    strDeviceStatus = (strDesc.split('currently ')[1]).split('.')[0]

                    strText = strDevice + ";" + strDeviceType + ";" + strDeviceStatus

                    if intCounter > 7:
                        self.driver.swipe(288, 629, 288, 384, 1000)
                        time.sleep(3)

                    if strText.lower() in listDevice:
                        break
                    else:
                        listDeviceType.append(strDeviceType)
                        listDevice.append(strText.lower())
                        listDeviceName.append(strDevice)

                self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()
                time.sleep(3)

                for intCounter in range(0, len(listDeviceName)):

                    if intCounter > 0:
                        strPreviousDeviceType = listDeviceType[intCounter - 1]
                        strPreviousDeviceName = listDeviceName[intCounter - 1]

                    if listDeviceType[intCounter].lower() == 'heating':
                        if intCounter == 0:
                            self.report_pass(
                                'Android-App Honeycomb Dashboard : The heating is displayed at central as expected ')
                        elif listDeviceType[intCounter - 1].lower() == 'heating' and listDeviceName[intCounter - 1] \
                                <= listDeviceName[intCounter]:
                            self.report_pass(
                                'Android-App Honeycomb Dashboard : The heating is displayed at central as expected ')
                        else:
                            self.report_fail(
                                'Android-App Honeycomb Dashboard : The heating is not displayed as expected ')

                    if listDeviceType[intCounter].lower() == 'boiler':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         [''], strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'hot water':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler'], strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'active plug':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water'], strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'warm white light':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug'], strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'tunable light':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug', 'warm white light'],
                                                         strPreviousDeviceName,
                                                         strPreviousDeviceType, str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'colour Light':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug', 'warm white light',
                                                          'tunable light'],
                                                         strPreviousDeviceName, strPreviousDeviceType,
                                                         str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'motion sensor':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug', 'warm white light',
                                                          'tunable light', 'colour Light'],
                                                         strPreviousDeviceName, strPreviousDeviceType,
                                                         str(intCounter + 1), context)

                    if listDeviceType[intCounter].lower() == 'window or door sensor':
                        self.honeycomb_ValidateHierarchy(listDeviceName[intCounter], listDeviceType[intCounter],
                                                         ['boiler', 'hot water', 'active plug', 'warm white light',
                                                          'tunable light', 'colour Light', 'motion sensor'],
                                                         strPreviousDeviceName, strPreviousDeviceType,
                                                         str(intCounter + 1), context)

            else:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

        except:

            self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Navigates to a particular screen

    def navigationTo_screen(self, context, strScreenName):

        self.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate Dashboard Icon at - ' + strScreenName + ' Screen')

        if self.wait_for_element_exist(*HoneycombDashboardLocators.DASHBOARD_ICON):
            self.report_pass(
                'User is on Dashboard screen ')

        elif self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
            self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
            self.report_pass(
                'User is now on Dashboard screen ')
        else:
            self.report_fail(
                'Dashboard icon is not displayed, unable to proceed with scenaio')
            exit()

        time.sleep(2)

        if strScreenName == "Heating":
            if self.wait_for_element_exist(*HoneycombDashboardLocators.DASHBOARD_ICON):
                self.driver.find_element(*HoneycombDashboardLocators.DASHBOARD_ICON).click()
                self.report_pass('Device Icon is clicked')
                time.sleep(2)
                if self.wait_for_element_exist(*HoneycombDashboardLocators.CONTROL_TEXTVIEW):
                    self.report_pass('Control screen is displayed')
                    if self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                        self.report_pass('Dashboard icon is displayed')
                        self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                        time.sleep(2)

                    else:
                        context.reporter.ReportEvent('Test Validation', 'Dashboard icon is not displayed', "FAIL",
                                                     "Center")
                        exit()
                else:
                    context.reporter.ReportEvent('Test Validation', 'Control screen is not displayed', "FAIL",
                                                 "Center")
            else:
                context.reporter.ReportEvent('Test Validation', 'Device icon is not displayed', "FAIL",
                                             "Center")

        elif strScreenName in ["Manage devices", "Install devices", "All Recipes", "Geolocation", "Holiday mode"]:
            if self.wait_for_element_exist(*HoneycombDashboardLocators.MENU_ITEMS_VIEW):
                self.driver.find_element(*HoneycombDashboardLocators.MENU_ITEMS_VIEW).click()
                context.reporter.ReportEvent('Test Validation', 'Menu icon is displayed', "PASS",
                                             "Center")
                time.sleep(2)
                strList = list(HoneycombDashboardLocators.MENU_ITEMS_TEXTVIEW)
                if strScreenName in ["Geolocation", "Holiday mode"]:
                    strList[1] = strList[1].replace("MENUITEMNAME", strScreenName)
                    strProperty = tuple(strList)
                    if not self.wait_for_element_exist(*strProperty):
                        strList[1] = strList[1].replace("MENUITEMNAME", 'Settings')
                        strPropertyMenu = tuple(strList)
                        strList[1] = strList[1].replace('Settings', "MENUITEMNAME")
                        if self.wait_for_element_exist(*strPropertyMenu):
                            self.report_pass('Settings, Menu item is displayed')
                            self.driver.find_element(*strPropertyMenu).click()
                            time.sleep(2)

                strList[1] = strList[1].replace("MENUITEMNAME", strScreenName)
                strProperty = tuple(strList)

                if self.wait_for_element_exist(*strProperty):
                    self.report_pass(strScreenName + ', Menu item is displayed')
                    self.driver.find_element(*strProperty).click()
                    time.sleep(2)
                    self.report_pass('Menu Icon ' + strScreenName + ' is clicked')
                    if self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                        context.reporter.ReportEvent('Test Validation', 'Dashboard icon is displayed', "PASS",
                                                     "Center")
                        self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                        time.sleep(2)

                    else:
                        context.reporter.ReportEvent('Test Validation', 'Dashboard icon is not displayed', "FAIL",
                                                     "Center")
                        exit()
                else:

                    context.reporter.ReportEvent('Test Validation', strScreenName + ' menu item is not displayed',
                                                 "FAIL", "Center")

            else:
                context.reporter.ReportEvent('Test Validation', 'menu icon is not displayed', "FAIL",
                                             "Center")


class LeakSensor(BasePage):
    # Leak Navigation
    def leak_control_navigation(self):
        try:
            if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                self.driver.find_element(*self.REFRESH_BUTTON).click()
                time.sleep(5)
                self.wait_for_element_exist(*self.REFRESH_BUTTON)

            self.device_list_navigation()

            if self.wait_for_element_exist(*HLS.HLS_LEAK_ICON):
                self.driver.find_element(*HLS.HLS_LEAK_ICON).click()
                time.sleep(2)
                self.report_pass("Leak Icon element is found")
            else:
                self.report_fail("Leak Icon element is not found")
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function leak_control_navigation \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # get leak Status
    def get_leak_status(self):
        strStatus = ''
        blnCalibrationAt = False
        try:
            self.refresh_page()
            if self.is_element_present(*HLS.HLS_PROGRESS_BAR):
                blnCalibrationAt = True
                self.device_list_navigation()
                if self.wait_for_element_exist(*HLS.HLS_LEAK_ICON):
                    strXPATH = self.driver.find_element(*HLS.HLS_LEAK_ICON).get_attribute('xpath')
                    indexLeak = self.get_leak_index(strXPATH)
                    tupleProperty = HLS.HLS_DEVICELIST_STATUS.replace('index', indexLeak)

                    if self.wait_for_element_exist(*tupleProperty):
                        strStatus = self.driver.find_element(*tupleProperty).get_attribute('text')
                        self.report_pass("Calibration is running status is fetched from device list")
                    else:
                        self.report_fail("Unable to fetch status from Device list")
                else:
                    self.report_fail("Leak is not found at Device list when calibration is running")
            elif self.wait_for_element_exist(*HLS.HLS_STATUS):
                strStatus = self.driver.find_element(*HLS.HLS_STATUS).get_attribute('text')
                self.report_pass("Leak Status element is found")
            else:
                self.report_fail("Leak Status element is not found")
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function get_leak_status \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
        return strStatus, blnCalibrationAt

    # get leak index at the device list, this function is subject to change if any property changes are done at app level
    def get_leak_index(self, strXPATH):
        indexLeak = ''
        try:
            indexLeak = strXPATH.split('//')[1].split('/')[11].split('[')[1].split(']')[0]
        except:
            self.report_fail(
                'Android App : No Index Found: in function get_leak_index \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
        return indexLeak

    def validate_notification(self):
        try:

            lstNotificationText = ['battery low', 'low water flow', 'high water usage',
                                   'all sorted', 'confirmation', 'flow alerts', 'device offline']
            eleStart = self.driver.find_element(*HLS.HLS_ANDROID_STATUSBAR)
            intleftX = eleStart.location['x']
            intUpperY = eleStart.location['y']
            intWidth = eleStart.size['width']
            intheight = eleStart.size['height']
            intStartX = intleftX + intWidth / 2
            intStartY = intUpperY + intheight / 2
            intEndY = intStartY + 250
            time.sleep(10)
            blnFound = False
            self.driver.swipe(intStartX, intStartY, intStartX, intEndY)
            strTitletextFound = ''
            strContentText = ''
            time.sleep(15)
            allnotificationsColumn = self.driver.find_elements(*HLS.HLS_MAINCOLUMN)

            for notificationColumn in allnotificationsColumn:
                notificationItem = notificationColumn.find_element(*HLS.HLS_TITLE)
                strTitletext = notificationItem.get_attribute('text')

                if 'flow alerts' in strTitletext.lower(): strTitletext = 'flow alerts'
                if strTitletext.lower() in lstNotificationText:
                    self.report_done('Flow alerts are displayed and tapped')
                    time.sleep(3)
                    objContent = notificationColumn.find_elements(*HLS.HLS_CONTENT_TEXT)
                    if len(objContent) > 0:
                        strContentText = objContent[0].get_attribute('text')
                        objContent[0].click()
                    time.sleep(5)
                    blnFound = True
                    strTitletextFound = strTitletext
                    break

            if not blnFound:
                self.report_done('Flow alerts are not displayed')
                time.sleep(3)
                self.driver.swipe(intStartX, intEndY + 50, intStartX, intStartY)

            return strTitletextFound, strContentText
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function validate_notification \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def clear_notification(self):
        try:
            eleStart = self.driver.find_element(*HLS.HLS_ANDROID_STATUSBAR)
            intleftX = eleStart.location['x']
            intUpperY = eleStart.location['y']
            intWidth = eleStart.size['width']
            intheight = eleStart.size['height']
            intStartX = intleftX + intWidth / 2
            intStartY = intUpperY + intheight / 2
            intEndY = intStartY + 250

            self.driver.swipe(intStartX, intStartY, intStartX, intEndY)
            time.sleep(5)
            if self.is_element_present(*HLS.HLS_CLEARTEXT):
                self.driver.find_element(*HLS.HLS_CLEARTEXT).click()

            time.sleep(3)

            self.driver.swipe(intStartX, intEndY + 50, intStartX, intStartY)
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function clear_notification \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def fetchCurrentAlertSettings(self):
        oDict = {'true': 'ACTIVE', 'false': 'INACTIVE'}
        strPushStatus, strEmailStatus, strTextStatus = 'false', 'false', 'false'
        try:
            if self.reporter.ActionStatus:
                blnFlag = True

                if self.is_element_present(*HLS.HLS_SETTINGS_ICON):
                    self.driver.find_element(*HLS.HLS_SETTINGS_ICON).click()
                    time.sleep(4)
                if self.wait_for_element_exist(*HLS.HLS_LEAK_NOTIFICATIONS_LAYOUT):
                    self.driver.find_element(*HLS.HLS_LEAK_NOTIFICATIONS_LAYOUT).click()
                    time.sleep(4)
                    if self.wait_for_element_exist(*HLS.HLS_PUSH_CHECK):
                        strPushStatus = str(self.driver.find_element(*HLS.HLS_PUSH_CHECK).get_attribute('checked'))
                    else:
                        blnFlag = False
                    if self.is_element_present(*HLS.HLS_EMAIL_CHECK):
                        strEmailStatus = str(self.driver.find_element(*HLS.HLS_EMAIL_CHECK).get_attribute('checked'))
                    else:
                        blnFlag = False
                    if self.is_element_present(*HLS.HLS_TEXT_CHECK):
                        strTextStatus = str(self.driver.find_element(*HLS.HLS_TEXT_CHECK).get_attribute('checked'))
                    else:
                        blnFlag = False
                    if not blnFlag:
                        self.report_fail('Alert setting screen is not as expected')
                    if self.is_element_present(*HLS.HLS_BACK_ICON):
                        self.driver.find_element(*HLS.HLS_BACK_ICON).click()
                        time.sleep(2)
                    else:
                        self.report_fail('Back Button at Alert settings is not found ')
                    if self.is_element_present(*HLS.HLS_BACK_ICON):
                        self.driver.find_element(*HLS.HLS_BACK_ICON).click()
                        time.sleep(2)
                    else:
                        self.report_fail('Back Button at leak settings is not found ')
                else:
                    self.report_fail('Leak Notification layout is not found')
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function fetchCurrentAlertSettings \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
        return {'SendSubscriptionSMS': oDict[strTextStatus], 'SendEmail': oDict[strEmailStatus],
                'PushNotification': oDict[strPushStatus]}

    def setAlertSettings(self, oTargetDict):
        oDict = {'SendSubscriptionSMS': HLS.HLS_TEXT_CHECK, 'SendEmail': HLS.HLS_EMAIL_CHECK,
                 'PushNotification': HLS.HLS_PUSH_CHECK}

        blnFlag = True
        blnClick = False
        try:
            if self.reporter.ActionStatus:
                blnFlag = True
                if self.is_element_present(*HLS.HLS_SETTINGS_ICON):
                    self.driver.find_element(*HLS.HLS_SETTINGS_ICON).click()
                    time.sleep(4)
                if self.wait_for_element_exist(*HLS.HLS_LEAK_NOTIFICATIONS_LAYOUT):
                    self.driver.find_element(*HLS.HLS_LEAK_NOTIFICATIONS_LAYOUT).click()
                    time.sleep(4)

                    for oKey in oDict.keys():
                        oProperty = oDict[oKey]
                        if self.wait_for_element_exist(*oProperty):
                            strTextStatus = str(self.driver.find_element(*oProperty).get_attribute('checked'))
                            if strTextStatus == 'false':
                                self.driver.find_element(*oProperty).click()
                                blnClick = True
                                time.sleep(2)

                    for oKey in oDict.keys():
                        if oKey in oTargetDict.keys():
                            oProperty = oDict[oKey]
                            if not oTargetDict[oKey].upper() == 'ACTIVE':
                                if self.wait_for_element_exist(*oProperty):
                                    self.driver.find_element(*oProperty).click()
                                    time.sleep(2)
                                    blnClick = True
                                else:
                                    blnFlag = False

                    if not blnFlag:
                        self.report_fail('Alert setting screen is not as expected')

                    if blnClick:
                        if self.is_element_present(*HLS.HLS_SAVE):
                            time.sleep(3)
                            self.report_pass('Save button is found and clicked')
                            self.driver.find_element(*HLS.HLS_SAVE).click()
                        else:
                            self.report_fail('Save button is not found')
                    if self.is_element_present(*HLS.HLS_BACK_ICON) and not \
                            self.is_element_present(*HLS.HLS_LEAK_NOTIFICATIONS_LAYOUT):
                        if blnClick:
                            self.report_fail('The app is not navigated back to settings after clicking Save')
                        self.driver.find_element(*HLS.HLS_BACK_ICON).click()
                    if not self.is_element_present(*HLS.HLS_LEAK_NOTIFICATIONS_LAYOUT):
                        self.report_fail('The app is not navigated back to settings after clicking Save')
                    else:
                        if self.is_element_present(*HLS.HLS_BACK_ICON):
                            self.driver.find_element(*HLS.HLS_BACK_ICON).click()

                else:
                    self.report_fail('Leak Notification layout is not found')
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function fetchCurrentAlertSettings \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def fetchMinLeakDuration(self):

        strMin = ''
        try:
            if self.reporter.ActionStatus:
                blnFlag = True
                if self.is_element_present(*HLS.HLS_SETTINGS_ICON):
                    self.driver.find_element(*HLS.HLS_SETTINGS_ICON).click()
                    time.sleep(4)
                if self.wait_for_element_exist(*HLS.HLS_LEAK_NOTIFICATIONS_LAYOUT):
                    self.driver.find_element(*HLS.HLS_LEAK_FLOWALERT_LAYOUT).click()
                    time.sleep(4)

                    if self.wait_for_element_exist(*HLS.HLS_LEAK_TIME):
                        strText = self.driver.find_element(*HLS.HLS_LEAK_TIME).get_attribute('text')
                        strMin = strText.split(' ')[0]
                        self.report_pass('Minimum leak duration value is displayed')
                else:
                    self.report_fail('Leak Notification layout is not found')

                if self.is_element_present(*HLS.HLS_BACK_ICON):
                    self.driver.find_element(*HLS.HLS_BACK_ICON).click()
                    time.sleep(2)
                else:
                    self.report_fail('Back Button at duration settings is not found ')
                if self.is_element_present(*HLS.HLS_BACK_ICON):
                    self.driver.find_element(*HLS.HLS_BACK_ICON).click()
                    time.sleep(2)
                else:
                    self.report_fail('Back Button at leak settings is not found ')

        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function fetchMinLeakDuration \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

        return strMin

    def setMniLeakDuration(self, strTarget):
        try:
            if self.reporter.ActionStatus:
                blnFlag = False
                strMin = ''
                intCounter = 1
                if self.is_element_present(*HLS.HLS_SETTINGS_ICON):
                    self.driver.find_element(*HLS.HLS_SETTINGS_ICON).click()
                    time.sleep(4)
                if self.wait_for_element_exist(*HLS.HLS_LEAK_NOTIFICATIONS_LAYOUT):
                    self.driver.find_element(*HLS.HLS_LEAK_FLOWALERT_LAYOUT).click()
                    time.sleep(4)
                    while strMin != strTarget and intCounter < 3:
                        if self.wait_for_element_exist(*HLS.HLS_LEAK_TIME):
                            strText = self.driver.find_element(*HLS.HLS_LEAK_TIME).get_attribute('text')
                            strMin = strText.split(' ')[0]

                            if not strTarget == strMin:
                                self.driver.find_element(*HLS.HLS_LEAK_TIME).click()
                                if self.wait_for_element_exist(*HLS.HLS_FLOW_SCROLL):
                                    oScrollElement = self.driver.find_element(*HLS.HLS_FLOW_SCROLL)
                                    self.scroll_element_to_value(oScrollElement, int(strMin), int(strTarget), 5,
                                                                 2)
                                    self.driver.find_element(*HLS.HLS_SET_BUTTON).click()
                                    strText = self.driver.find_element(*HLS.HLS_LEAK_TIME).get_attribute('text')
                                    strMin = strText.split(' ')[0]
                                    if strText == strTarget:
                                        self.report_pass('Minimum leak duration is set')
                                        blnFlag = True
                                        time.sleep(5)
                            else:
                                self.report_pass('Minimum leak duration is set')
                                blnFlag = True

                        else:
                            self.report_fail('Duration scroll is not found')
                        intCounter = intCounter + 1
                    if not blnFlag:
                        self.report_fail('Minimum leak duration is not set')
                        time.sleep(5)

                else:
                    self.report_fail('Leak Notification layout is not found')

                if self.wait_for_element_exist(*HLS.HLS_BACK_ICON):
                    self.driver.find_element(*HLS.HLS_BACK_ICON).click()
                    time.sleep(2)
                else:
                    self.report_fail('Back Button at duration settings is not found ')
                if self.is_element_present(*HLS.HLS_BACK_ICON):
                    self.driver.find_element(*HLS.HLS_BACK_ICON).click()
                    time.sleep(2)
                else:
                    self.report_fail('Back Button at leak settings is not found ')

        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function setMniLeakDuration \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def startCalibration(self):
        try:
            self.leak_control_navigation()
            if self.wait_for_element_exist(*HLS.HLS_LOWFLOW_OK_BUTTON):
                self.driver.find_element(*HLS.HLS_LOWFLOW_OK_BUTTON).click()
            elif self.wait_for_element_exist(*HLS.HLS_WATERUSAGE_NO_BUTTON):
                self.driver.find_element(*HLS.HLS_WATERUSAGE_NO_BUTTON).click()

            else:
                self.report_fail('unable to navigate to troubleshooting')

            if self.reporter.ActionStatus:
                time.sleep(10)
                self.driver.swipe(100, 600, 100, 100, 1000)
                if self.wait_for_element_exist(*HLS.HLS_TROUBLESHOOT_YES_BUTTON):
                    self.driver.find_element(*HLS.HLS_TROUBLESHOOT_YES_BUTTON).click()
                    if self.wait_for_element_exist(*HLS.HLS_FIX_DIALOG_YES_BUTTON):
                        self.driver.find_element(*HLS.HLS_FIX_DIALOG_YES_BUTTON).click()
                        self.report_pass('Calibration screenshot')
                        time.sleep(10)
                    else:
                        self.report_fail('unable to start calibration')
                else:
                    self.report_fail('unable to do the troubleshooting')


        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function startCalibration \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def bannerText(self, alert):
        try:
            dict = {'SMALL LEAK': HLS.HLS_BANNER_LOW,
                    'LARGE FLOW': HLS.HLS_BANNER_HIGH}
            if self.reporter.ActionStatus:
                if self.wait_for_element_exist(*dict[alert]):
                    text = self.driver.find_element(*dict[alert]).get_attribute('text')
                    return text
                else:
                    self.report_fail('HLS_BANNER is not found')
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function bannerText \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def bannerDisappear(self, alert):
        try:
            dict = {'SMALL LEAK': HLS.HLS_BANNER_LOW,
                    'LARGE FLOW': HLS.HLS_BANNER_HIGH}
            if self.reporter.ActionStatus:
                if self.is_element_present(*dict[alert]):
                    self.report_fail('HLS_BANNER is  displayed again')
                else:
                    self.report_pass('Banner has disappeared')
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function bannerDisappear \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def load_troubleshootingScreen(self, status):
        try:
            if 'SMALL' in status.upper():
                objProperty = HLS.HLS_LOW_YES_BUTTON
                button = 'HLS.HLS_LOW_YES_BUTTON'
                objBanner = HLS.HLS_BANNER_LOW
            else:
                objProperty = HLS.HLS_HIGH_NO_BUTTON
                button = 'HLS.HLS_HIGH_NO_BUTTON'
                objBanner = HLS.HLS_BANNER_HIGH

            if self.reporter.ActionStatus:
                if self.wait_for_element_exist(*objBanner):
                    self.report_pass('Banner is found for ' + status + ' leak')

                    if self.is_element_present(*objProperty):
                        self.driver.find_element(*objProperty).click()
                    else:
                        self.report_fail('The ' + button + ' button is not found')
                else:
                    self.report_fail('HLS_BANNER is not found')
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function load_troubleshootingScreen \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def intendedUsage(self):
        try:
            if self.reporter.ActionStatus:
                if self.wait_for_element_exist(*HLS.HLS_BANNER_HIGH):
                    self.report_pass('Banner is displayed succesfully')
                    objProperty = HLS.HLS_HIGH_YES_BUTTON
                    button = 'HLS.HLS_HIGH_YES_BUTTON'
                    if self.is_element_present(*objProperty):
                        self.driver.find_element(*objProperty).click()
                    else:
                        self.report_fail('The ' + button + ' button is not found')
                else:
                    self.report_fail('HLS_BANNER_HIGH is not found')
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function intendedUsage \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def remindLater(self):
        try:
            if self.reporter.ActionStatus:
                if self.wait_for_element_exist(*HLS.HLS_BANNER_LOW):
                    self.report_pass('Banner is displayed succesfully')
                    objProperty = HLS.HLS_LOW_REMINDLATER_BUTTON
                    button = 'HLS.HLS_LOW_REMINDLATER_BUTTON'
                    if self.is_element_present(*objProperty):
                        self.driver.find_element(*objProperty).click()
                    else:
                        self.report_fail('The ' + button + ' button is not found')
                else:
                    self.report_fail('HLS_BANNER_LOW is not found')
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function remindLater \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class PlugSchedule(BasePage):
    # for updating schedule
    def UpdateSchedule(self, intScheduleSlot, strStartTime, strEndTime, strState):

        if self.reporter.ActionStatus:
            try:
                self.reporter.HTML_TC_BusFlowKeyword_Initialize('Updating Time slots')

                strProperty = list(PlugScheduleLocators.PLUG_TIMESLOTOPTION_ICON)
                strProperty[1] = strProperty[1].replace("INDEX", str(intScheduleSlot))
                strPropertyTuple = tuple(strProperty)

                if self.wait_for_element_exist(*strPropertyTuple):
                    self.driver.find_element(*strPropertyTuple).click()
                    time.sleep(2)
                    if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_EDITTIMESLOT_ICON):
                        self.driver.find_element(*PlugScheduleLocators.PLUG_EDITTIMESLOT_ICON).click()
                        time.sleep(2)
                    else:
                        self.report_fail("Edit time slot option is not found in time slot option menu, exit condtion")
                        exit()
                    if strStartTime != "":
                        strHour, strMinutes = strStartTime.split(":")
                        if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_SCHEDULEHOURPICKER_LAYOUT):
                            strSetHourValue = self.driver.find_element(*PlugScheduleLocators.
                                                                       PLUG_SCHEDULEHOURPICKER_LAYOUT).get_attribute(
                                'text')
                        else:
                            self.report_fail(
                                "Hour Picker end time slot couldnt be found, exit condtion")
                            if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_CANCEL_BUTTON):
                                self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()

                        if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_SCHEDULEMINUTEPICKER_LAYOUT):
                            strSetMinValue = self.driver.find_element(*PlugScheduleLocators.
                                                                      PLUG_SCHEDULEMINUTEPICKER_LAYOUT).get_attribute(
                                'text')
                        else:
                            self.report_fail(
                                "Min Picker end time slot couldnt be found, exit condtion")
                            if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_CANCEL_BUTTON):
                                self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()
                        intCounter = 0
                        while (int(strHour) == int(strSetHourValue) is False) or intCounter < 25:

                            if int(strHour) > int(strSetHourValue):
                                self.driver.swipe(162, 900, 162, 950, 1000)
                                time.sleep(1)
                            if int(strHour) < int(strSetHourValue):
                                self.driver.swipe(162, 950, 162, 900, 1000)
                                time.sleep(1)

                            strSetHourValue = self.driver.find_element(*PlugScheduleLocators.
                                                                       PLUG_SCHEDULEHOURPICKER_LAYOUT).get_attribute(
                                'text')
                            intCounter += 1
                        if intCounter == 25:
                            self.report_fail(
                                "Desired Hour time slot couldnt be selected, exit condtion")
                            if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_CANCEL_BUTTON):
                                self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()
                        else:
                            self.report_done(
                                "Desired Hour time slot is selected")

                        intCounter = 0
                        while (int(strMinutes) == int(strSetMinValue) is False) or intCounter < 6:

                            if int(strMinutes) > int(strSetMinValue):
                                self.driver.swipe(600, 900, 600, 950, 1000)
                                time.sleep(1)

                            if int(strMinutes) < int(strSetMinValue):
                                self.driver.swipe(600, 950, 600, 900, 1000)
                                time.sleep(1)

                            strSetMinValue = self.driver.find_element(*PlugScheduleLocators.
                                                                      PLUG_SCHEDULEMINUTEPICKER_LAYOUT).get_attribute(
                                'text')
                            intCounter += 1
                        if intCounter == 6:
                            self.report_fail(
                                "Desired Min time slot couldnt be selected, exit condtion")
                            self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()
                        else:
                            self.report_done(
                                "Desired Min time slot is selected")

                    if strEndTime != "":
                        strHour, strMinutes = strEndTime.split(":")
                        if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_ENDTIME_BUTTON):
                            self.driver.find_element(*PlugScheduleLocators.PLUG_ENDTIME_BUTTON).click()
                            time.sleep(2)
                            self.report_done("End time Button is found and clicked sucessfully")
                        else:
                            self.report_fail("End time Button is not found on edit screen, Exit condition")
                            if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_CANCEL_BUTTON):
                                self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()
                        if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_SCHEDULEHOURPICKER_LAYOUT):
                            strSetHourValue = self.driver.find_element(*PlugScheduleLocators.
                                                                       PLUG_SCHEDULEHOURPICKER_LAYOUT).get_attribute(
                                'text')
                        else:
                            self.report_fail(
                                "Hour Picker end time slot couldnt be found, exit condtion")
                            if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_CANCEL_BUTTON):
                                self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()

                        if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_SCHEDULEMINUTEPICKER_LAYOUT):
                            strSetMinValue = self.driver.find_element(*PlugScheduleLocators.
                                                                      PLUG_SCHEDULEMINUTEPICKER_LAYOUT).get_attribute(
                                'text')
                        else:
                            self.report_fail(
                                "Min Picker end time slot couldnt be found, exit condtion")
                            if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_CANCEL_BUTTON):
                                self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()
                        intCounter = 0
                        while (int(strHour) == int(strSetHourValue) is False) or intCounter < 25:

                            if int(strHour) > int(strSetHourValue):
                                self.driver.swipe(162, 900, 162, 950, 1000)
                                time.sleep(1)
                            if int(strHour) < int(strSetHourValue):
                                self.driver.swipe(162, 950, 162, 900, 1000)
                                time.sleep(1)

                            strSetHourValue = self.driver.find_element(*PlugScheduleLocators.
                                                                       PLUG_SCHEDULEHOURPICKER_LAYOUT).get_attribute(
                                'text')
                            intCounter += 1
                        if intCounter == 25:
                            self.report_fail(
                                "Desired Hour time slot couldnt be selected, exit condtion")
                            self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()
                        else:
                            self.report_done(
                                "Desired Hour time slot is selected")

                        intCounter = 0
                        while (int(strMinutes) == int(strSetMinValue) is False) or intCounter < 6:

                            if int(strMinutes) > int(strSetMinValue):
                                self.driver.swipe(600, 900, 600, 950, 1000)
                                time.sleep(1)

                            if int(strMinutes) < int(strSetMinValue):
                                self.driver.swipe(600, 950, 600, 900, 1000)
                                time.sleep(1)

                            strSetMinValue = self.driver.find_element(*PlugScheduleLocators.
                                                                      PLUG_SCHEDULEMINUTEPICKER_LAYOUT).get_attribute(
                                'text')
                            intCounter += 1
                        if intCounter == 6:
                            self.report_fail(
                                "Desired Min time slot couldnt be selected, exit condtion")
                            self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()
                        else:
                            self.report_done(
                                "Desired Min time slot is selected")

                        if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_SCHEDULESTATUS_BUTTON):
                            strPresentstate = self.driver.find_element(*PlugScheduleLocators.
                                                                       PLUG_SCHEDULESTATUS_BUTTON).get_attribute('text')
                            if strPresentstate != strState.upper():
                                self.driver.find_element(*PlugScheduleLocators.PLUG_SCHEDULESTATUS_BUTTON).click()
                        else:
                            self.report_fail(
                                "State toggler button couldnt be found, exit condtion")
                            if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_CANCEL_BUTTON):
                                self.driver.find_element(*PlugScheduleLocators.PLUG_CANCEL_BUTTON).click()
                            exit()
                else:
                    self.report_fail("The given Time slot schedule is not found, Exit condition")
                    exit()

            except:
                self.report_fail('Android-App : NoSuchElementException: in deleteSchedules Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def VerifySchedule(self, listSchedulesExpected):
        if self.reporter.ActionStatus:
            try:
                self.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying Time slots')

                strSCHEDULETEXTSTATUS = PlugScheduleLocators.PLUG_SCHEDULETEXTSTATUS_ICON
                strSCHEDULEICONSTATUS = PlugScheduleLocators.PLUG_SCHEDULEICONSTATUS_ICON
                strFROMTIME = PlugScheduleLocators.PLUG_FROMTIME_TEXTVIEW
                strTOTIME = PlugScheduleLocators.PLUG_TOTIME_TEXTVIEW

                listSchedules = []
                for intIndex in range(1, 6):

                    strIndex = str(intIndex)
                    strSCHEDULETEXTSTATUSproperty = strSCHEDULETEXTSTATUS.replace("INDEX", strIndex)
                    strSCHEDULEICONSTATUSproperty = strSCHEDULEICONSTATUS.replace("INDEX", strIndex)
                    strFROMTIMEproperty = strFROMTIME.replace("INDEX", strIndex)
                    strTOTIMEproperty = strTOTIME.replace("INDEX", strIndex)

                    if self.wait_for_element_exist(*strFROMTIMEproperty):
                        strFromTimeText = self.driver.find_element(*strFROMTIMEproperty).get_attribute('text')
                    else:
                        break

                    if self.wait_for_element_exist(*strTOTIMEproperty):
                        strToTimeText = self.driver.find_element(*strTOTIMEproperty).get_attribute('text')
                    else:
                        break

                    if self.wait_for_element_exist(*strSCHEDULETEXTSTATUS):
                        strTextStatus = self.driver.find_element(*strSCHEDULETEXTSTATUS).get_attribute('text')
                    else:
                        break

                    if self.wait_for_element_exist(*strSCHEDULEICONSTATUS):
                        strIconStatus = self.driver.find_element(*strSCHEDULEICONSTATUS).get_attribute('text')
                    else:
                        break

                    listSchedules = listSchedules.append(
                        strIconStatus + "," + strTextStatus + "," + strFromTimeText + "-" + strToTimeText)

                return listSchedules

            except:
                self.report_fail('Android-App : NoSuchElementException: in deleteSchedules Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set Plug Schedule
    def set_plug_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                blnFlagFormat = False
                if self.wait_for_element_exist(
                        *SchedulePageLocators.START_TIME_LABEL) and self.wait_for_element_exist(
                    *self.REFRESH_BUTTON):
                    lstAMelements = self.driver.find_elements(*EditTimeSlotPageLocators.EDIT_TIMESLOT_AM_FORMAT)
                    if len(lstAMelements) > 0: blnFlagFormat = True
                    for oKey in oScheduleDict.keys():

                        self._navigate_to_day(oKey)
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        # Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                        intCurrentEventCount = len(lstStartTime)

                        if self.reporter.platformVersion == 'V6':
                            self.add_or_remove_events(len(oScheduleList))
                        else:
                            if len(oScheduleList) > 4:
                                if not intCurrentEventCount == 6:
                                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_SPINNER_MENU):
                                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()
                                    else:
                                        self.report_fail('Element SCHEDULE_SPINNER_MENU is not found')
                                    if self.wait_for_element_exist(*SchedulePageLocators.SIX_EVENT_SUBMENU):
                                        self.driver.find_element(*SchedulePageLocators.SIX_EVENT_SUBMENU).click()
                                    else:
                                        self.report_fail('Element SIX_EVENT_SUBMENU is not found')
                            else:
                                if not intCurrentEventCount == 4:
                                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_SPINNER_MENU):
                                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()
                                    else:
                                        self.report_fail('Element SCHEDULE_SPINNER_MENU is not found')
                                    if self.wait_for_element_exist(*SchedulePageLocators.FOUR_EVENT_SUBMENU):
                                        self.driver.find_element(*SchedulePageLocators.FOUR_EVENT_SUBMENU).click()
                                    else:
                                        self.report_fail('Element FOUR_EVENT_SUBMENU is not found')

                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                        for intCntr in range((len(lstStartTime) - 1), -1, -1):

                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetState = oScheduleList[intCntr][1]

                            intCntrIter = 0
                            strCurrentStartTIme = ''
                            if blnFlagFormat:
                                strSetToTime = str(int(strSetStartTime.split(':')[0]) % 12) + ":" + \
                                               strSetStartTime.split(':')[1]
                            else:
                                strSetToTime = strSetStartTime
                            while (strCurrentStartTIme != strSetToTime) and (intCntrIter < 3):
                                time.sleep(3)
                                lstStartTime[intCntr].click()
                                time.sleep(3)
                                # self.reporter.HTML_TC_BusFlowKeyword_Initialize('Updating Event - ' + str(intCntr + 1))

                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.TOGGLE_BUTTON):
                                    if self.driver.find_element(
                                            *EditTimeSlotPageLocators.TOGGLE_BUTTON).get_attribute(
                                        'name').find(
                                        'ON') >= 0:
                                        strCurrentState = 'ON'
                                    else:
                                        strCurrentState = 'OFF'

                                    if fltSetState != strCurrentState:
                                        self.driver.find_element(
                                            *EditTimeSlotPageLocators.TOGGLE_BUTTON).click()
                                else:
                                    self.report_fail('Element TOGGLE_BUTTON is not found')
                                # self.UpdateHourAndMinute(strSetStartTime.split(':')[0],strSetStartTime.split(':')[1])


                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.HOUR_SCROLL):
                                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                                    if self.wait_for_element_exist(*EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM):
                                        strCurrentHour = oScrolElement.find_element(
                                            *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                            'name')
                                        strCurrentHour = ('0' + strCurrentHour)[-2:]
                                    else:
                                        self.report_fail('Element NUMBER_INSDE_SCROLL_ITEM is not found')
                                else:
                                    self.report_fail('Element HOUR_SCROLL is not found')
                                    exit()
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                                    strCurrentMinute = oScrolElement.find_element(
                                        *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                        'name')
                                else:
                                    self.report_fail('Element MINUTE_SCROLL is not found')
                                    exit()
                                strCurrentTime = strCurrentHour + ':' + strCurrentMinute
                                self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                                self.set_schedule_event_minute(strSetStartTime.split(':')[1])

                                intCntrIter = intCntrIter + 1
                                strLog = "Event Number $$Before Change$$After Change $$ Updated State@@@" + \
                                         str(
                                             intCntr + 1) + "$$" + strCurrentTime + "$$" + strSetStartTime + "$$" + fltSetState
                                self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.SAVE_BUTTON):
                                    self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                                    time.sleep(2)
                                else:
                                    self.report_fail('Element SAVE_BUTTON is not found')
                                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                                    time.sleep(2)
                                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                                else:
                                    self.report_fail('Element REFRESH_BUTTON is not found')

                                strCurrentStartTIme = lstStartTime[intCntr].get_attribute('text')
                            self.report_pass(
                                'Main Screen after Event number : ' + str(
                                    intCntr + 1) + ' is changed')
                        self.reporter.HTML_TC_BusFlowKeyword_Initialize('All Events Updated')
                        self.report_pass('Main Screen after all Events are changed')
                else:
                    self.report_fail(
                        "Control not active on the Plug Schedule Page to set the Plug Schedule")

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in set_plug_schedule Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # plug page navigation
    def navigation_to_plugpage(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HoneycombDashboardLocators.DASHBOARD_ICON):
                    self.report_pass(
                        'Honeycomb Dashboard : User is on Dashboard screen ')

                elif self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                    self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                    self.report_pass(
                        'Honeycomb Dashboard : User is now on Dashboard screen ')
                else:
                    self.report_fail(
                        'Honeycomb Dashboard : Dashboard icon is not displayed ')
                    exit()

                if self.wait_for_element_exist(*HomePageLocators.CURRENT_TITLE):
                    if self.wait_for_element_exist(*HoneycombDashboardLocators.PLUG_ICON_VIEW):

                        self.driver.find_element(*HoneycombDashboardLocators.PLUG_ICON_VIEW).click()
                        self.report_done('Plug is found in Dashboard and clicked')

                    else:

                        self.dashboardSwipe(False)
                        if self.wait_for_element_exist(*HoneycombDashboardLocators.PLUG_ICON_VIEW):
                            if self.wait_for_element_exist(*HoneycombDashboardLocators.PLUG_ICON_VIEW):
                                self.driver.find_element(*HoneycombDashboardLocators.PLUG_ICON_VIEW).click()
                                self.report_pass('Plug is found in Dashboard and clicked')
                            else:
                                self.report_fail('plugName and Locators are not matched')
                        else:
                            self.report_fail('Plug is not found in Dashboard')
                else:
                    if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                        self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                        time.sleep(2)
                        if self.wait_for_element_exist(*HoneycombDashboardLocators.PLUG_ICON_VIEW):

                            self.driver.find_element(*HoneycombDashboardLocators.PLUG_ICON_VIEW).click()
                            self.report_done('Plug is found in Dashboard and clicked')

                        else:

                            self.dashboardSwipe(False)
                            if self.wait_for_element_exist(*HoneycombDashboardLocators.PLUG_ICON_VIEW):

                                self.driver.find_element(*HoneycombDashboardLocators.PLUG_ICON_VIEW).click()
                                self.report_pass('Plug is found in Dashboard and clicked')

                            else:
                                self.report_fail('Plug is not found in Dashboard')

                    else:
                        self.report_fail('User is not inside the app')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: in navigation_to_plugpage Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # set plug mode
    def set_plug_mode(self, strMode):
        blnFlag = False
        if self.reporter.ActionStatus:
            try:
                self.reporter.HTML_TC_BusFlowKeyword_Initialize('Set Plug Mode')
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_MODE_VIEW):
                        strModeText = self.driver.find_element(*PlugScheduleLocators.PLUG_MODE_VIEW).get_attribute(
                            'text')

                        if "AUTO" in strMode.upper(): strMode = "Schedule Active"
                        if strMode.upper() != strModeText.upper():
                            if self.wait_for_element_exist(*PlugScheduleLocators.PLUG_MODECHANGE_ICON):
                                self.driver.find_element(*PlugScheduleLocators.PLUG_MODECHANGE_ICON).click()
                                self.wait_for_element_exist(*self.REFRESH_BUTTON)
                                blnFlag = True
                            time.sleep(5)
                        else:
                            blnFlag = True
                    if blnFlag:
                        self.report_pass('Successfully Plug Mode is set to <B>' + strMode)
                    else:
                        self.report_fail('Unable to set Plug Mode to <B>' + strMode)
                else:
                    self.report_fail(
                        "Control not active on the Plug Control Page to set the Hot Water Mode")

            except:
                self.report_fail('Android App : NoSuchElementException: in set_plug_mode Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class DashboardCustomization(BasePage):
    DEVICE_NAME = ""
    DEVICES_INDASHBOARDSCREEN = []
    DEVICES_POSITION_BEFORESWAPING = {}
    DEVICES_POSITION_AFTERSWAPING = {}
    DEVICENODEID = ""
    SWAPINGDEVICENODEID = ""

    # This method is to check the parameterized device has been paired with the user account
    def checkDeviceOnDashboardScreen(self, deviceName):

        if self.reporter.ActionStatus:
            try:
                self.honeycomb_verify()
                DashboardCustomization.DEVICE_NAME = deviceName

                deviceElement = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                deviceElement = deviceElement.replace("deviceName", DashboardCustomization.DEVICE_NAME)
                deviceInDashboard = self.is_element_present(By.XPATH, deviceElement)
                deviceInAddScreen = False

                if not deviceInDashboard:
                    self.driver.find_element(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON).click()
                    self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_LISTVIEW_LAYOUT,
                                                15)
                    deviceInAddScreen = self.is_element_present(By.XPATH, deviceElement)
                    self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()
                    time.sleep(5)
                if (deviceInDashboard == False) and (deviceInAddScreen == False):
                    self.report_fail(
                        'Android App : Device ' + DashboardCustomization.DEVICE_NAME + ' not paired to the user account')
                else:
                    self.report_pass(
                        'Android App : Device ' + DashboardCustomization.DEVICE_NAME + ' paired to the user account')
            except:
                self.report_fail('Android App : Problem might be in accessing the API values \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # navigate to the device in dashboard screen and long press on the device
    def navigateAndLongPressCellOnDevice(self):

        if self.reporter.ActionStatus:
            try:

                # calling the pre requistie method
                cus = DashboardCustomization(self.driver, self.reporter)
                cus.checkDeviceInDSAndMoveFromListView(DashboardCustomization.DEVICE_NAME)

                DashboardCustomization.DEVICES_INDASHBOARDSCREEN = self.driver.find_elements(
                    *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_FILLEDSLOTS)

                deviceElement = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                deviceElement = deviceElement.replace("deviceName", DashboardCustomization.DEVICE_NAME)

                elementToLongPress = self.driver.find_element(By.XPATH, deviceElement)

                # long press on the element
                action = TouchAction(self.driver)
                action.long_press(elementToLongPress).release().perform()

                time.sleep(5)

                if self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON,
                                               15):
                    self.report_pass(
                        'Android App : long pressed on the ' + DashboardCustomization.DEVICE_NAME + ' in the Dashboard screen')

                else:
                    self.report_fail('Android App : Long press mode not enabled in dashboard screen')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: long press mode is not enabled in Dashboard Screen, so save button not appeared in screen \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def validateEditModeIcon(self):

        if self.reporter.ActionStatus:
            try:

                if "Edit" == self.driver.find_element(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_TITLE).text:
                    self.report_pass('Android App : Edit mode enabled and Edit title displayed in the screen')
                else:
                    self.report_pass('Android App : Edit mode not enabled in the screen')

                if self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_DELETE_ICON):
                    self.report_pass('Android App : Remove delete Icon is displayed in the Dashboard screen')

                else:
                    self.report_fail('Android App : Remove delete Icon is not displayed in the Dashboard screen')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: Remove Delete icon is not displayed in Dashboard Screen \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # tap on button
    def tapButton(self, buttonType):

        if self.reporter.ActionStatus:
            try:

                if 'Add' in buttonType:
                    if self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON,
                                                   15):
                        self.driver.find_element(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON).click()

                        if self.is_element_present(
                                *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_DEVICE_POPUP):
                            self.driver.find_element(
                                *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_DEVICE_POPUP).click()
                            self.report_pass(
                                'Android App : Add device pop up displayed and no devices in add list screen and clicked Ok button')
                        else:
                            self.wait_for_element_exist(
                                *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_LISTVIEW_LAYOUT)
                            self.report_pass('Android App : Device add screen displayed ')
                    else:
                        self.report_fail('Android App : Device add screen not displayed ')
                elif 'Cancel' in buttonType:

                    if self.wait_for_element_exist(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_CANCEL_BUTTON, 15):
                        self.driver.find_element(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_CANCEL_BUTTON).click()
                        self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON)
                        self.report_pass('Android App : Clicked on Cancel button and user in the dashboard screen ')
                    else:
                        self.report_fail('Android App : Unable to click on Cancel button or edit mode not enabled ')
                elif 'Save' in buttonType:
                    if self.wait_for_element_exist(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON, 15):
                        self.driver.find_element(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON).click()
                        self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON)
                        self.report_pass('Android App : Clicked on Save button and user in the dashboard screen ')
                    else:
                        self.report_fail('Android App : Unable to click on Save button or edit mode not enabled ')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException:' + buttonType + '  is not displayed in the Screen \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # In order to validate the parameterized device, removing from dashboard screen and adding to list view and selecting form listview to dashboard screen and saving the same.
    def addDeviceFromListViewAndSave(self):

        if self.reporter.ActionStatus:
            try:

                self.report_pass(
                    'Android App : ' + DashboardCustomization.DEVICE_NAME + ' removing from dashboard screen and adding to List view')

                if self.wait_for_element_exist(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_CANCEL_BUTTON, 30):
                    self.driver.find_element(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_CANCEL_BUTTON).click()
                self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON, 30)
                if self.wait_for_element_exist(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_CANCEL_BUTTON, 30):
                    self.driver.find_element(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_CANCEL_BUTTON).click()

                if len(self.driver.find_elements(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_FILLEDSLOTS)) > 1:
                    deviceElement = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                    deviceElement = deviceElement.replace("deviceName", DashboardCustomization.DEVICE_NAME)

                    elementToLongPress = self.driver.find_element(By.XPATH, deviceElement)
                    # long press on the element
                    action = TouchAction(self.driver)
                    action.long_press(elementToLongPress).release().perform()
                    time.sleep(4)
                    self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_DELETE_ICON)

                    # for android, the devices should be dragged to the remove device icon to remove from dashboard
                    cus = DashboardCustomization(self.driver, self.reporter)
                    cus.removeDevice()
                    time.sleep(4)
                    if self.is_element_present(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_DEVICE_POPUP):
                        self.driver.find_element(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_DEVICE_POPUP).click()
                        self.report_pass(
                            'Android App : Add device pop up displayed while removing and clicked Ok button')

                    if self.wait_for_element_exist(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON, 30):
                        self.driver.find_element(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON).click()
                        time.sleep(4)
                    filledDevices = self.driver.find_elements(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_FILLEDSLOTS)
                    # long press on the element
                    action.long_press(filledDevices[0]).release().perform()
                    self.wait_for_element_exist(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_CANCEL_BUTTON)
                    self.report_pass(
                        'Android App : ' + DashboardCustomization.DEVICE_NAME + ' removed from dashboard and added to list view')

                    if self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON,
                                                   30):
                        self.driver.find_element(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON).click()
                    if self.wait_for_element_exist(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_DEVICE_ADDSCREEN, 15):
                        self.report_pass('Android App : Add screen displayed')

                    addElement = str(DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_DEVICE_IN_LISTVIEW)
                    addElement = addElement.replace("deviceName", DashboardCustomization.DEVICE_NAME)

                    self.driver.find_element(By.XPATH, addElement).click()

                    self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON)

                    self.report_pass(
                        'Android App : ' + DashboardCustomization.DEVICE_NAME + ' device selected from list view')

                    if self.wait_for_element_exist(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON, 30):
                        self.driver.find_element(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON).click()
                        time.sleep(4)
                    device_icon_on_dashboard = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                    device_icon_on_dashboard = device_icon_on_dashboard.replace("deviceName",
                                                                                DashboardCustomization.DEVICE_NAME)
                    if self.wait_for_element_exist(By.XPATH, device_icon_on_dashboard, 30):
                        self.report_pass(
                            'Android App : ' + DashboardCustomization.DEVICE_NAME + ' is added from list view ')
                    else:
                        self.report_fail(
                            'Android App : ' + DashboardCustomization.DEVICE_NAME + ' is not added from list view')
                else:
                    self.report_fail(
                        'Android App : Removing from dashboard screen is not possible because atleast one device should be available in dashboard screen')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: List view element is not displayed in the Screen \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # removing the parameterized device from dashboard screen
    def removeDeviceFromDashboard(self):
        if self.reporter.ActionStatus:
            try:
                removeElement = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                removeElement = removeElement.replace("deviceName", DashboardCustomization.DEVICE_NAME)

                cus = DashboardCustomization(self.driver, self.reporter)
                cus.removeDevice()

                if not self.is_element_present(By.XPATH, removeElement):

                    # self.driver.find_element(By.XPATH, removeElement).click()
                    time.sleep(5)
                    self.report_pass(
                        'Android App : ' + DashboardCustomization.DEVICE_NAME + ' dragged to remove device icon')
                else:

                    self.report_fail(
                        'Android App : ' + DashboardCustomization.DEVICE_NAME + ' not dragged to remove device icon')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: remove device icon ' + DashboardCustomization.DEVICE_NAME + ' \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def removeDevice(self):

        if self.reporter.ActionStatus:
            try:
                device_icon_on_dashboard = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                device_icon_on_dashboard = device_icon_on_dashboard.replace("deviceName",
                                                                            DashboardCustomization.DEVICE_NAME)
                deviceElement = self.driver.find_element(By.XPATH, device_icon_on_dashboard)

                xDeviceElement = deviceElement.location['x']
                yDeviceElement = deviceElement.location['y']

                intDeviceElementWidth = deviceElement.size['width']
                intDeviceElementHeight = deviceElement.size['height']

                intDeviceElementCenterXValue = xDeviceElement + intDeviceElementWidth / 2
                intDeviceElementCenterYValue = yDeviceElement + intDeviceElementHeight / 2

                removeDeviceElement = self.driver.find_element(
                    *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_DELETE_ICON)

                xRemoveElement = removeDeviceElement.location['x']
                yRemoveElement = removeDeviceElement.location['y']

                intRemoveElementWidth = removeDeviceElement.size['width']
                intRemoveElementHeight = removeDeviceElement.size['height']

                intElementCenterXValue = xRemoveElement + intRemoveElementWidth / 2
                intElementCenterYValue = yRemoveElement + intRemoveElementHeight / 2

                self.driver.swipe(int(intDeviceElementCenterXValue), int(intDeviceElementCenterYValue),
                                  int(intElementCenterXValue), int(intElementCenterYValue))
                time.sleep(4)

                self.report_pass(
                    'Android App : ' + DashboardCustomization.DEVICE_NAME + ' removed from the dashboard screen')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: Element issue in removing the device in the dashboard screen \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def validateDeviceInListView(self):

        if self.reporter.ActionStatus:

            try:

                afterDeviceRemovalFromDS = self.driver.find_elements(
                    *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_FILLEDSLOTS)

                if len(afterDeviceRemovalFromDS) == (len(DashboardCustomization.DEVICES_INDASHBOARDSCREEN) - 1):
                    self.report_pass(
                        'Android App : ' + DashboardCustomization.DEVICE_NAME + ' removed from the dashboard screen')
                else:
                    self.report_fail(
                        'Android App : ' + DashboardCustomization.DEVICE_NAME + ' unable to remove from the dashboard screen')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: finding issue in filledslots elements ' + DashboardCustomization.DEVICE_NAME + ' \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # validate position changes
    def validateChangesPostExit(self, type):

        if self.reporter.ActionStatus:

            try:
                if "reverted" in type:

                    deleteIcons = self.driver.find_elements(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_DELETE_ICON)

                    if len(deleteIcons) > 0:
                        self.report_fail('Android App : Edit mode not exited')

                    else:
                        self.report_pass('Android App : Edit mode exited')

                    afterClickingCancelButton = self.driver.find_elements(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_FILLEDSLOTS)

                    if len(afterClickingCancelButton) == len(DashboardCustomization.DEVICES_INDASHBOARDSCREEN):
                        self.report_pass(
                            'Android App : ' + DashboardCustomization.DEVICE_NAME + ' not removed from the dashboard screen')

                    else:
                        self.report_fail(
                            'Android App : ' + DashboardCustomization.DEVICE_NAME + ' removed from the dashboard screen')

                elif "saved" in type:

                    deleteIcons = self.driver.find_elements(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_DELETE_ICON)

                    if len(deleteIcons) > 0:
                        self.report_fail('Android App : Edit mode not exited')

                    else:
                        self.report_pass('Android App : Edit mode exited')

                    afterClickingSaveButton = self.driver.find_elements(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_FILLEDSLOTS)

                    if len(afterClickingSaveButton) == (len(DashboardCustomization.DEVICES_INDASHBOARDSCREEN) - 1):
                        self.report_pass(
                            'Android App : ' + DashboardCustomization.DEVICE_NAME + ' removed from the dashboard screen')

                    else:
                        self.report_fail(
                            'Android App : ' + DashboardCustomization.DEVICE_NAME + ' not removed from the dashboard screen')

                elif "swapped" in type:

                    deleteIcons = self.driver.find_elements(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_EDIT_DELETE_ICON)

                    if len(deleteIcons) > 0:
                        self.report_fail('Android App : Edit mode not exited')

                    else:
                        self.report_pass('Android App : Edit mode exited')

                    afterClickingSaveButton = self.driver.find_elements(
                        *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_FILLEDSLOTS)

                    if len(afterClickingSaveButton) == (len(DashboardCustomization.DEVICES_INDASHBOARDSCREEN)):
                        self.report_pass(
                            'Android App : ' + DashboardCustomization.DEVICE_NAME + ' swapped in the dashboard screen')

                    else:
                        self.report_fail(
                            'Android App : ' + DashboardCustomization.DEVICE_NAME + ' not swapped in the dashboard screen')

                    cus = DashboardCustomization(self.driver, self.reporter)
                    cus.validateDeviceIndex()


            except:
                self.report_fail(
                    'Android App : NoSuchElementException: finding issue in delete icon id/filledslots elements ' + DashboardCustomization.DEVICE_NAME + ' \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # swapping the parameterized devices
    def swapDevicesOnDashboard(self, SwapDeviceName):

        if self.reporter.ActionStatus:
            try:
                device_icon_on_dashboard = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                device_icon_on_dashboard = device_icon_on_dashboard.replace("deviceName",
                                                                            DashboardCustomization.DEVICE_NAME)
                deviceElement = self.driver.find_element(By.XPATH, device_icon_on_dashboard)

                xDeviceElement = deviceElement.location['x']
                yDeviceElement = deviceElement.location['y']

                intDeviceElementWidth = deviceElement.size['width']
                intDeviceElementHeight = deviceElement.size['height']

                intDeviceElementCenterXValue = xDeviceElement + intDeviceElementWidth / 2
                intDeviceElementCenterYValue = yDeviceElement + intDeviceElementHeight / 2

                swapDeviceElement = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                swapDeviceElement = swapDeviceElement.replace("deviceName", SwapDeviceName)

                swapElement = self.driver.find_element(By.XPATH, swapDeviceElement)

                xSwapElement = swapElement.location['x']
                ySwapElement = swapElement.location['y']

                intSwapElementWidth = swapElement.size['width']
                intSwapElementHeight = swapElement.size['height']

                intElementCenterXValue = xSwapElement + intSwapElementWidth / 2
                intElementCenterYValue = ySwapElement + intSwapElementHeight / 2

                DashboardCustomization.DEVICENODEID = Putils.getDeviceNodeByName(DashboardCustomization.DEVICE_NAME)
                DashboardCustomization.SWAPINGDEVICENODEID = Putils.getDeviceNodeByName(SwapDeviceName)

                DashboardCustomization.DEVICES_POSITION_BEFORESWAPING = Putils.getDeviceIDsAndPositionsByBeekeeper()

                self.driver.swipe(int(intDeviceElementCenterXValue), int(intDeviceElementCenterYValue),
                                  int(intElementCenterXValue), int(intElementCenterYValue))
                time.sleep(4)

                self.report_pass('Android App : ' + DashboardCustomization.DEVICE_NAME + ' moved to the new position')

            except:
                self.report_fail(
                    'Android App : NoSuchElementException: Element issue in swaping the device in the dashboard screen \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # validating the devices swapping position by beekeeper
    def validateDeviceIndex(self):

        if self.reporter.ActionStatus:
            try:
                DashboardCustomization.DEVICES_POSITION_AFTERSWAPING = Putils.getDeviceIDsAndPositionsByBeekeeper()
                if DashboardCustomization.DEVICES_POSITION_BEFORESWAPING.get(
                        DashboardCustomization.DEVICENODEID) == DashboardCustomization.DEVICES_POSITION_AFTERSWAPING.get(
                    DashboardCustomization.SWAPINGDEVICENODEID):
                    self.report_pass(
                        'Android App : ' + DashboardCustomization.DEVICE_NAME + ' moved to the new position it is validated by Beekeepeer')
                else:
                    self.report_fail(
                        'Android App : ' + DashboardCustomization.DEVICE_NAME + ' not moved to the new position')
            except:
                self.report_fail('Android App : Problem might be in validating the values from API \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # pre request method for dashboard customization screen tests, this will be called in given method, to ensure Parameter device available in DS or get from LV
    def checkDeviceInDSAndMoveFromListView(self, deviceName):

        if self.reporter.ActionStatus:
            try:

                device_icon_on_dashboard = str(HomePageLocators.DEVICE_ICON_DASHBOARD)
                device_icon_on_dashboard = device_icon_on_dashboard.replace("deviceName", deviceName)

                if self.wait_for_element_exist(By.XPATH, device_icon_on_dashboard):
                    self.report_pass(
                        'Android App : In Pre request method ' + deviceName + ' is available in the Dashboard screen, no action required')
                else:
                    self.report_pass(
                        'Android App : In Pre request method ' + deviceName + ' is not available in the Dashboard screen, so get from List view to availabe DS')

                    if self.wait_for_element_exist(*HoneycombDashboardLocators.REFRESH_BUTTON_V6):
                        self.driver.find_element(*HoneycombDashboardLocators.REFRESH_BUTTON_V6).click()
                        time.sleep(5)
                    if self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON,
                                                   30):
                        self.driver.find_element(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_ADD_BUTTON).click()
                    self.wait_for_element_exist(*DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_LISTVIEW_LAYOUT,
                                                15)

                    if len(self.driver.find_elements(
                            *DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_LISTVIEW_DEVICES)) > 0:
                        self.report_pass(
                            'Android App : In Pre request method, device available in the List view screen to proceed test')

                        deviceElement = str(DashboardCustomizationLocators.DASHBOARDCUSTOMIZATION_DEVICE_IN_LISTVIEW)
                        deviceElement = deviceElement.replace("deviceName", deviceName)

                        if self.wait_for_element_exist(By.XPATH, deviceElement, 30):
                            self.driver.find_element(By.XPATH, deviceElement).click()
                            time.sleep(5)
                        self.report_pass(
                            'Android App : In Pre request method,' + deviceName + 'is moved to the dashboard screen')
            except:
                self.report_fail(
                    'Android App : NoSuchElementException: facing no such element in getting device in dashboard screen and some in list view \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


class NAT(BasePage):
    """To Update Thermostat working mode and operating mode"""

    def NAT_ChangeModeAndOperatingMode(self, strMode, strOperatingMode):
        if self.reporter.ActionStatus:
            try:
                blnModeFound = False
                blnOperatingMode = False
                if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_SETTINGS_ICON):
                    self.driver.find_element(*NAThermostatLocators.THERMOSTAT_SETTINGS_ICON).click()
                    time.sleep(3)
                if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_SETTINGS_TITLE):
                    self.report_pass('Settings Page Displayed')

                strModeUpdated = self.UpdateModeScreenEquivalent(strMode.upper())
                if strOperatingMode == "OFF":
                    if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_MODE_OFF_ICON):
                        self.driver.find_element(*NAThermostatLocators.THERMOSTAT_MODE_OFF_ICON).click()
                        time.sleep(3)
                        blnOperatingMode = True
                else:
                    if strModeUpdated == "heat":
                        if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_MODE_HEAT_ICON):
                            self.driver.find_element(*NAThermostatLocators.THERMOSTAT_MODE_HEAT_ICON).click()
                            time.sleep(3)
                            blnModeFound = True

                    elif strModeUpdated == "cool":
                        if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_MODE_COOL_ICON):
                            self.driver.find_element(*NAThermostatLocators.THERMOSTAT_MODE_COOL_ICON).click()
                            time.sleep(3)
                            blnModeFound = True
                    elif strModeUpdated == "dual":
                        if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_MODE_DUAL_ICON):
                            self.driver.find_element(*NAThermostatLocators.THERMOSTAT_MODE_DUAL_ICON).click()
                            time.sleep(3)
                            blnModeFound = True
                    if blnModeFound:
                        self.report_pass('Mode ' + strMode + ' is clicked')
                        time.sleep(3)
                    else:
                        self.report_fail('ICON for the mode ' + strMode + ' is not found')

                    if self.reporter.ActionStatus:
                        if strOperatingMode == "HOLD":
                            if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_MODE_HOLD_ICON):
                                self.driver.find_element(*NAThermostatLocators.THERMOSTAT_MODE_HOLD_ICON).click()
                                time.sleep(3)
                                blnOperatingMode = True
                        elif strOperatingMode == "SCHEDULE":
                            if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_MODE_SCHEDULE_ICON):
                                self.driver.find_element(*NAThermostatLocators.THERMOSTAT_MODE_SCHEDULE_ICON).click()
                                time.sleep(3)
                                blnOperatingMode = True

                if blnOperatingMode:
                    self.report_pass('Operating Mode ' + strOperatingMode + ' is clicked')
                    time.sleep(3)
                else:
                    self.report_fail('Operating mode ' + strOperatingMode + ' is not set')

                if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_SETTINGS_TITLE):
                    self.driver.back()
                    time.sleep(6)
                if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)

            except:
                self.report_fail('Android-App : NoSuchElementException: in NAThermostat Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # For fetching the screen equivalent of mode
    def UpdateModeScreenEquivalent(self, strMode):
        ModeDictionary = {"HEATING": "heat", "COOLING": "cool", "DUAL": "dual", "OFF": "off", "COOL": "cool",
                          "HEAT": "heat"}
        return ModeDictionary[strMode]

    # Set Thermostat
    def thermostat_selection(self, strThermostatName, strMode):
        if self.wait_for_element_exist(*self.REFRESH_BUTTON):
            self.driver.find_element(*self.REFRESH_BUTTON).click()
            time.sleep(5)
            self.wait_for_element_exist(*self.REFRESH_BUTTON)
        self.device_list_navigation()

        lstThermostatProperty = list(NAThermostatLocators.THERMOSTAT_NAME)
        lstSecondaryProperty = list(NAThermostatLocators.THERMOSTAT_ICON_PROPERTY)
        if strMode == 'OFF':
            lstSecondaryProperty[1] = lstSecondaryProperty[1].replace('ThermostatName', strThermostatName + ', OFF')
            objAltThermostat = tuple(lstSecondaryProperty)
            if self.wait_for_element_exist(*objAltThermostat):
                self.driver.find_element(*objAltThermostat).click()
                self.report_pass("Thermostat - " + strThermostatName + " found")
            else:
                self.report_fail("Thermostat - " + strThermostatName + " is not found")
        else:

            lstThermostatProperty[1] = lstThermostatProperty[1].replace('ThermostatName', strThermostatName)
            lstSecondaryProperty[1] = lstSecondaryProperty[1].replace('ThermostatName', strThermostatName + ',')
            objThermostat = tuple(lstThermostatProperty)
            objAltThermostat = tuple(lstSecondaryProperty)

            if self.wait_for_element_exist(*objThermostat):
                self.driver.find_element(*objThermostat).click()
                self.report_pass("Thermostat - " + strThermostatName + " found")
            elif self.wait_for_element_exist(*objAltThermostat):
                self.driver.find_element(*objAltThermostat).click()
                self.report_pass("Thermostat - " + strThermostatName + " found")
            else:
                self.report_fail("Thermostat - " + strThermostatName + " is not found")

    def NAT_setTemp(self, strExpectedTemp, objTempPicker=None):

        try:
            if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                if '--' in strExpectedTemp:

                    strTempSplitted = strExpectedTemp.split('--')
                    strMinTemp = strTempSplitted[1]
                    strMaxTemp = strTempSplitted[0]
                    self.NAT_setTemp(strMinTemp, NAThermostatLocators.THERMOSTAT_CONTROL_SECONDARY)
                    self.NAT_setTemp(strMaxTemp, NAThermostatLocators.THERMOSTAT_CONTROL)

                else:
                    if objTempPicker is None:
                        objTempPicker = NAThermostatLocators.THERMOSTAT_CONTROL
                    if self.wait_for_element_exist(*objTempPicker):
                        oScrolElement = ''
                        oScrolElement = self.driver.find_element(*objTempPicker)
                        strTargetTempSplitted = oScrolElement.get_attribute('name').upper().split()
                        intTempPositionCounter = strTargetTempSplitted.index('TEMPERATURE,') + 1
                        fltCurrentTargTemp = int(strTargetTempSplitted[intTempPositionCounter])
                        intCntrIter = 1
                        fltTargetTemperature = int(strExpectedTemp)
                        while True:
                            self.scroll_element_to_value_NA(oScrolElement, fltCurrentTargTemp, fltTargetTemperature, 1,
                                                            2.5)
                            self.report_done('Screen shot for temp that is set before a refresh')
                            time.sleep(10)
                            self.wait_for_element_exist(*self.REFRESH_BUTTON)
                            self.driver.find_element(*self.REFRESH_BUTTON).click()
                            time.sleep(10)
                            self.wait_for_element_exist(*self.REFRESH_BUTTON)
                            oScrolElement = ''
                            self.wait_for_element_exist(*objTempPicker)
                            oScrolElement = self.driver.find_element(*objTempPicker)
                            strTargetTempSplitted = oScrolElement.get_attribute('name').upper().split()
                            intTempPositionCounter = strTargetTempSplitted.index('TEMPERATURE,') + 1
                            fltCurrentTargTemp = int(strTargetTempSplitted[intTempPositionCounter])
                            print(str(fltCurrentTargTemp))
                            intCntrIter = intCntrIter + 1
                            if fltCurrentTargTemp == fltTargetTemperature or intCntrIter == 4: break

                        if fltCurrentTargTemp == fltTargetTemperature:
                            self.report_pass('The Target Temperature is successfully set to : ' + str(
                                fltTargetTemperature))
                        else:
                            self.report_fail(
                                'Unable to set the Target Temperature to : ' + str(fltTargetTemperature))
                    else:
                        self.report_fail('The temp scroll icon is not found')
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function NAT_setTemp \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def updateStatOperatingAttributes(self):
        clientCurrentTargetTemp = ''
        clientFlameIconApperance = False
        clientThermostatOperatingMODE = ''
        clientNextScheduleSlot = ''
        try:
            if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                if self.is_element_present(*NAThermostatLocators.THERMOSTAT_OFF_MODE_ICON):
                    clientThermostatOperatingMODE = 'OFF'
                else:

                    if self.is_element_present(*NAThermostatLocators.THERMOSTAT_CONTROL):
                        oScrolElement = self.driver.find_element(*NAThermostatLocators.THERMOSTAT_CONTROL)
                        clientCurrentTargetTempSplitted = (oScrolElement.get_attribute('name').upper().split())
                        clientCurrentTargetTemp = clientCurrentTargetTempSplitted[
                            clientCurrentTargetTempSplitted.index('TEMPERATURE,') + 1]

                    if self.is_element_present(*NAThermostatLocators.THERMOSTAT_CONTROL_SECONDARY):
                        oScrolElement = self.driver.find_element(*NAThermostatLocators.THERMOSTAT_CONTROL_SECONDARY)
                        clientCurrentTargetTempSplitted = oScrolElement.get_attribute('name').upper().split()
                        strTargetTemp = clientCurrentTargetTempSplitted[
                            clientCurrentTargetTempSplitted.index('TEMPERATURE,') + 1]
                        if clientCurrentTargetTemp == '':
                            clientCurrentTargetTemp = strTargetTemp
                        else:
                            clientCurrentTargetTemp = str(clientCurrentTargetTemp) + '--' + strTargetTemp

                    if '--' in str(clientCurrentTargetTemp):
                        if self.is_element_present(*NAThermostatLocators.THERMOSTAT_FLAKEICON):
                            clientFlameIconApperance = 'COOL'
                        elif self.is_element_present(*NAThermostatLocators.THERMOSTAT_FLAMEICON):
                            clientFlameIconApperance = 'HEAT'
                        else:
                            clientFlameIconApperance = False
                    else:
                        if self.is_element_present(*NAThermostatLocators.THERMOSTAT_HEATINGCOOLING):
                            oHeatCoolElement = self.driver.find_element(*NAThermostatLocators.THERMOSTAT_HEATINGCOOLING)
                            oHeatCoolChildElements = oHeatCoolElement.find_elements(By.XPATH,
                                                                                    ".//android.widget.TextView")
                            if len(oHeatCoolChildElements) == 0:
                                clientFlameIconApperance = False
                            else:
                                clientFlameIconApperance = True
                    if self.is_element_present(*NAThermostatLocators.THERMOSTAT_SCHEDULE_MODE_ICON):
                        clientThermostatOperatingMODE = 'SCHEDULE'
                        clientNextScheduleSlot = self.driver.find_element(
                            *NAThermostatLocators.THERMOSTAT_SCHEDULE_MODE_SLOT_ICON).get_attribute('text')
                    elif self.is_element_present(*NAThermostatLocators.THERMOSTAT_MANUAL_MODE_ICON):
                        clientThermostatOperatingMODE = 'HOLD'
                    else:
                        clientThermostatOperatingMODE = 'OFF'

        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function NAT_setTemp \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
        self.report_done('Screen shot after Temp and mode updates')
        return clientCurrentTargetTemp, clientFlameIconApperance, clientThermostatOperatingMODE

    def set_NA_schedule(self, oScheduleDict):
        try:
            blnElement = False
            if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                objElements = self.driver.find_elements(*NAThermostatLocators.THERMOSTAT_TAB_TITLE)
                if len(objElements) > 1:
                    for objElement in objElements:
                        strText = objElement.get_attribute('text')
                        if 'SCHEDULE' in strText.upper():
                            objElement.click()
                            blnElement = True

            if blnElement:
                for oKey in oScheduleDict.keys():
                    print('m here')
                    blnFlagFormat = False
                    print(oKey)
                    self._navigate_to_day(oKey)
                    oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                    lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                    intCurrentEventCount = len(lstStartTime)
                    self.add_or_remove_events(len(oScheduleList))
                    intScrollPrecision = 1.8
                    lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)
                    for intCntr in range((len(lstStartTime) - 1), -1, -1):
                        strSetStartTime = oScheduleList[intCntr][0]
                        fltSetTargTemp = oScheduleList[intCntr][1]
                        intCntrIter = 0
                        strCurrentStartTIme = ''
                        if blnFlagFormat:
                            strSetToTime = ('0' + str(int(strSetStartTime.split(':')[0]) % 12))[-2:] + ":" + \
                                           strSetStartTime.split(':')[1]
                        else:
                            strSetToTime = strSetStartTime

                        while (strCurrentStartTIme != strSetToTime) and (intCntrIter < 3):
                            time.sleep(3)
                            lstStartTime[intCntr].click()

                            time.sleep(3)

                            self.set_NA_schedule_target_temerature(fltSetTargTemp)
                            if '--' in fltSetTargTemp:
                                intScrollPrecision = 1
                                if self.is_element_present(*NAThermostatLocators.THERMOSTAT_STARTTIME_BUTTON):
                                    self.driver.find_element(*NAThermostatLocators.THERMOSTAT_STARTTIME_BUTTON).click()
                                else:
                                    self.report_fail('Element THERMOSTAT_STARTTIME_BUTTON is not found')
                                    return
                            if self.wait_for_element_exist(*EditTimeSlotPageLocators.HOUR_SCROLL):
                                oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                                strCurrentHour = oScrolElement.find_element(
                                    *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                    'name')
                                strCurrentHour = ('0' + strCurrentHour)[-2:]
                            else:
                                self.report_fail('Element HOUR_SCROLL is not found')
                                break
                            if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                                oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                                strCurrentMinute = oScrolElement.find_element(
                                    *EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute(
                                    'name')
                            else:
                                self.report_fail('Element MINUTE_SCROLL is not found')
                                break
                            strCurrentTime = strCurrentHour + ':' + strCurrentMinute

                            self.set_schedule_event_hour(strSetStartTime.split(':')[0], intScrollPrecision)
                            self.set_schedule_event_minute(strSetStartTime.split(':')[1], intScrollPrecision)
                            strLog = "Event Number $$Before Change$$After Change $$ Updated Temparature@@@" + \
                                     str(
                                         intCntr + 1) + "$$" + strCurrentTime + "$$" + strSetStartTime + "$$" + str(
                                fltSetTargTemp)
                            self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                            intCntrIter = intCntrIter + 1
                            time.sleep(5)
                            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                            time.sleep(5)
                            if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                                self.driver.find_element(*self.REFRESH_BUTTON).click()
                                time.sleep(7)
                                self.report_pass("Refresh button is found and clicked")
                            elif self.is_element_present(*EditTimeSlotPageLocators.CANCEL_BUTTON):
                                self.driver.find_element(*EditTimeSlotPageLocators.CANCEL_BUTTON).click()
                                time.sleep(2)
                                self.report_fail("Refresh button is not found, existing the scenario")
                                break
                            self.wait_for_element_exist(*self.REFRESH_BUTTON)
                            strCurrentStartTIme = lstStartTime[intCntr].get_attribute('text')
                        self.report_pass(
                            'Main Screen after Event number : ' + str(intCntr + 1) + ' is changed')
                    self.report_pass('Main Screen after all Events are changed')
            if self.is_element_present(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                time.sleep(4)
            elif self.is_element_present(*EditTimeSlotPageLocators.CANCEL_BUTTON):
                self.driver.find_element(*EditTimeSlotPageLocators.CANCEL_BUTTON).click()
                if self.wait_for_element_exist(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                    self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                    time.sleep(4)
        except:
            self.report_fail(
                'Android App : NoSuchElementException: in function set_NA_schedule \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def validateFeatureSettingsAndMode(self, feature, featureSettingMode, operatingMode):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_SETTINGS_ICON):
                    self.report_done('In Thermostat control screen, click on to navigate to setting page')
                    self.driver.find_element(*NAThermostatLocators.THERMOSTAT_SETTINGS_ICON).click()
                    if self.wait_for_element_exist(*NAThermostatLocators.THERMOSTAT_OFF_MODE_ICON):
                        self.report_done('In Thermostat setting page')

                if "FAN" in feature.upper():

                    if "OFF" in operatingMode.upper():
                        self.report_done('The Thermostat operating mode is OFF')
                        if self.driver.find_element(*NAThermostatLocators.NA_FAN_ALWAYSON_TEXT).get_attribute(
                                'enabled') == "false":
                            self.report_pass(
                                'The Thermostat setting page is disabled and Fan settings are disabled, since it is in Off operating mode')
                        else:
                            self.report_fail(
                                'The Thermostat setting page is not disbaled, there is some issues in disabling the thermostat setting page')

                    elif "HOLD" in operatingMode.upper():
                        self.report_done('The Thermostat operating mode is HOLD')
                        if self.driver.find_element(*NAThermostatLocators.NA_FAN_ALWAYSON_TEXT).get_attribute(
                                'enabled') == "true":
                            self.report_pass(
                                'The Thermostat setting page is enabled and Fan settings are enabled, since it is in Off operating mode')
                        else:
                            self.report_fail(
                                'The Thermostat setting page is not enabled, there is some issues in enabling the thermostat setting page')

                    else:
                        self.report_done('The operating mode not matches the specified OFF/HOLD for Fan ')

                elif "HUMIDITY" in feature.upper():

                    if "OFF" in operatingMode.upper():
                        self.report_done('The Thermostat operating mode is OFF')
                        if self.driver.find_element(*NAThermostatLocators.NA_HUMIDITY_SEEKBAR).get_attribute(
                                'enabled') == "false":
                            self.report_pass(
                                'The Thermostat setting page is disabled, since it is in Off operating mode')
                        else:
                            self.report_fail(
                                'The Thermostat setting page is not disbaled, there is some issues in disabling the thermostat setting page')

                    elif "HOLD" in operatingMode.upper():
                        self.report_done('The Thermostat operating mode is HOLD')
                        if self.driver.find_element(*NAThermostatLocators.NA_HUMIDITY_SEEKBAR).get_attribute(
                                'enabled') == "true":
                            self.report_pass(
                                'The Thermostat setting page is enabled, since it is in Off operating mode')
                        else:
                            self.report_fail(
                                'The Thermostat setting page is not enabled, there is some issues in enabling the thermostat setting page')

                    else:
                        self.report_done('The operating mode not matches the specified OFF/HOLD for Humidity')

            except:
                self.report_fail('Android-App : NoSuchElementException: in NAThermostat Setting page\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def select_NA_FanSetting(self, context, fanSettingOption):
        if self.reporter.ActionStatus:
            try:
                if "Auto" in fanSettingOption:
                    self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_AUTO)
                    self.driver.find_element(*NAThermostatLocators.NA_FAN_AUTO).click()
                    self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_AUTO_TEXT)
                    if self.driver.find_element(*NAThermostatLocators.NA_FAN_AUTO_TEXT).get_attribute(
                            'enabled') == "true":
                        self.report_pass('Fan is enabled and Auto option has been selected')
                    else:
                        self.report_fail('Fan is not enabled and Auto option has not been selected')

                elif "Circulate" in fanSettingOption:

                    if "Circulate" == fanSettingOption:

                        self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_CIRCULATE)
                        self.driver.find_element(*NAThermostatLocators.NA_FAN_CIRCULATE).click()
                        self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_CIRCULATE_TEXT)
                        if self.driver.find_element(*NAThermostatLocators.NA_FAN_CIRCULATE_TEXT).get_attribute(
                                'enabled') == "true":
                            self.report_pass('Fan is enabled and Circulate option has been selected')
                        else:
                            self.report_fail('Fan is not enabled and Circulate option has not been selected')

                    elif "15mins" in fanSettingOption:
                        self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_CIRCULATE_LOW)
                        self.driver.find_element(*NAThermostatLocators.NA_FAN_CIRCULATE_LOW).click()
                        time.sleep(4)
                        self.report_pass('15 mins is selected as Fan Option')

                    elif "30mins" in fanSettingOption:
                        self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_CIRCULATE_MEDIUM)
                        self.driver.find_element(*NAThermostatLocators.NA_FAN_CIRCULATE_MEDIUM).click()
                        time.sleep(4)
                        self.report_pass('30 mins is selected as Fan Option')

                    elif "45mins" in fanSettingOption:
                        self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_CIRCULATE_HIGH)
                        self.driver.find_element(*NAThermostatLocators.NA_FAN_CIRCULATE_HIGH).click()
                        time.sleep(4)
                        self.report_pass('45 mins is selected as Fan Option')

                elif "Always on" in fanSettingOption:

                    self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_ALWAYSON_TEXT)
                    self.driver.find_element(*NAThermostatLocators.NA_FAN_ALWAYSON_TEXT).click()
                    time.sleep(4)
                    self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_ALWAYSON_TEXT)
                    if self.driver.find_element(*NAThermostatLocators.NA_FAN_ALWAYSON_TEXT).get_attribute(
                            'enabled') == "true":
                        self.report_pass('Fan is enabled and Always on option has been selected')
                    else:
                        self.report_fail('Fan is not enabled and Always on option has not been selected')

            except:
                self.report_fail('Android-App : NoSuchElementException: in NAThermostat Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def validateCirculateOption(self, context):
        if self.reporter.ActionStatus:
            try:

                self.wait_for_element_exist(*NAThermostatLocators.NA_FAN_CIRCULATE_LOW)
                circulateOption1 = self.driver.find_element(*NAThermostatLocators.NA_FAN_CIRCULATE_LOW).is_displayed()
                circulateOption2 = self.driver.find_element(
                    *NAThermostatLocators.NA_FAN_CIRCULATE_MEDIUM).is_displayed()
                circulateOption3 = self.driver.find_element(*NAThermostatLocators.NA_FAN_CIRCULATE_HIGH).is_displayed()

                if True in (circulateOption1, circulateOption2, circulateOption3):
                    self.report_pass('Thermostat Fan Circulate options 15, 30 and 45 mins displayed')
                else:
                    self.report_fail('Thermostat Fan Circulate options 15, 30 and 45 mins not displayed')

            except:
                self.report_fail('Android-App : NoSuchElementException: in NAThermostat Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # check fan circulate options are selected
    def validateCirculateOptionSelected(self, context, selectedMins):
        if self.reporter.ActionStatus:
            try:

                selectedMins_InSeconds = int(selectedMins) * 60

                thermostatName = context.oNaThermostatEP.strThermostatName
                # Getting the value from api to validate
                naThermostatNodes = Putils.getNAThermostat_Nodes(thermostatName)
                fanScheduleValue = \
                    naThermostatNodes['features']['fan_controller_v1']['schedule']['targetValue']['setpoints'][1][
                        'secondsPastHour']

                if selectedMins_InSeconds == int(fanScheduleValue):
                    self.report_pass('The Fan circulate Value is set to ' + selectedMins + 'mins')
                else:
                    self.report_fail('The Fan circulate Value is not set to ' + selectedMins + 'mins')

            except:
                self.report_fail('Android-App : NoSuchElementException: in NAThermostat Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # check fan setting options are selected
    def validateFanSettingSelected(self, context, fanSettingOption):
        if self.reporter.ActionStatus:
            try:

                thermostatName = context.oNaThermostatEP.strThermostatName
                # Getting the value from api to validate
                naThermostatNodes = Putils.getNAThermostat_Nodes(thermostatName)
                selectedFanOption = naThermostatNodes['features']['fan_controller_v1']['operatingMode']['targetValue']

                fanOption = ""

                if "Auto" in fanSettingOption:
                    fanOption = "AUTO"
                elif "Circulate" in fanSettingOption:
                    fanOption = "SCHEDULE"
                elif "Always on" in fanSettingOption:
                    fanOption = "ALWAYS_ON"

                if fanOption == str(selectedFanOption):
                    self.report_pass('The Fan opton ' + fanOption + 'is enabled')
                else:
                    self.report_fail('The Fan opton ' + fanOption + 'is not enabled')

            except:
                self.report_fail('Android-App : NoSuchElementException: in NAThermostat Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def setHumidity_Value(self, humidityValue):
        if self.reporter.ActionStatus:
            try:

                seek_bar = self.driver.find_element(*NAThermostatLocators.NA_HUMIDITY_SEEKBAR)
                # get start co ordinate of seekbar
                start = seek_bar.location['x']
                # get width of seekbar
                end = seek_bar.size['width']

                # get location of seekbar vertically

                y = seek_bar.location['y']

                action = TouchAction(self.driver)

                moveTo = int(int(end) * float(int(humidityValue) / 100))

                action.press(seek_bar, start, y).move_to(seek_bar, moveTo, y).release().perform()
                self.report_done('Humidity value is configured to ' + humidityValue)


            except:
                self.report_fail('Android-App : NoSuchElementException: in NAThermostat Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def validate_Humidity_Value(self, context, humidityValue):
        if self.reporter.ActionStatus:
            try:
                thermostatName = context.oNaThermostatEP.strThermostatName
                # Getting the value from api to validate
                naThermostatNodes = Putils.getNAThermostat_Nodes(thermostatName)
                humidityTargetValue = naThermostatNodes['features']['humidity_controller_v1']['targetHumidity'][
                    'targetValue']

                if humidityValue == str(int(humidityTargetValue)):
                    self.report_pass('The Humidity Value is set to ' + humidityValue)
                else:
                    self.report_fail('The Humidity Value is not set to ' + humidityValue)

            except:
                self.report_fail('Android-App : NoSuchElementException: in NAThermostat Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class DYNAMIC_TROUBLESHOOTING(BasePage):
    objAnswers = None

    def navigate_questions(self, navigationlist, expectedQuestions):
        try:
            questions = []
            if self.reporter.ActionStatus:
                counter = 0
                for eachResponse in navigationlist:
                    counter += 1
                    bool = False
                    self.report_done('Screenshot for the question number - ' + str(counter))
                    question = self.get_question(expectedQuestions[counter - 1])
                    questions.append(question)
                    responses = question['responses']
                    for itemResponse in responses:
                        temp = itemResponse
                        if eachResponse.replace("'", "").replace("’", "") == temp.replace("’", "").replace("'", ""):
                            bool = True
                            index = responses.index(itemResponse)
                            objResponse = self.objAnswers[index]
                            objResponse.click()
                            time.sleep(5)
                            break
                    if not bool:
                        self.report_fail(
                            'The response, ' + eachResponse + ' is not seen for the question, ' + question['question'])
                        break
            return questions
        except:
            self.report_fail('Android-App : NoSuchElementException: in navigate_questions Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def get_question(self, question):
        try:
            boolean = False
            if self.reporter.ActionStatus:
                time.sleep(2)
                objElements = self.driver.find_elements(*HLS.HLS_TS_QUESTIONS)
                count = 0
                for objElement in objElements:
                    questionText = objElement.get_attribute('text')
                    if question.replace("'", "").replace("’", "") == questionText.replace("’", "").replace("'", ""):
                        boolean = True

                        objAnswerContainers = self.driver.find_elements(*HLS.HLS_BUTTON_CONTAINERS)
                        objAnswerContainer = objAnswerContainers[count]
                        self.objAnswers = objAnswerContainer.find_elements(By.XPATH, ".//android.widget.Button")
                        responses = []
                        for objAnswer in self.objAnswers:
                            text = objAnswer.get_attribute('text')
                            responses.append(text)
                        return {'question': questionText, 'responses': responses}
                    count += 1
                if not boolean: self.report_fail("Question " + question + " is not found")

        except:
            self.report_fail('Android-App : NoSuchElementException: in get_question Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def call_plumber(self):
        try:
            if self.reporter.ActionStatus:

                if self.wait_for_element_exist(*HLS.HLS_CALL_EXPERT_TITLE):
                    text = self.driver.find_element(*HLS.HLS_CALL_EXPERT_TITLE).get_attribute('text')
                    if text == 'Call an expert':
                        self.report_pass('Call a plumber screen - Title text is displayed')
                    else:
                        self.report_fail('Call a plumber screen - Title text is not correctly displayed ')
                else:
                    self.report_fail('Call a plumber screen - Title is not displayed')

                if self.is_element_present(*HLS.HLS_DONE_BUTTON):
                    self.report_pass('Call a plumber screen - Done Button is displayed')
                    self.driver.find_element(*HLS.HLS_DONE_BUTTON).click()
                else:
                    self.report_fail('Call a plumber screen - Done Button is not displayed')


        except:
            self.report_fail('Android-App : NoSuchElementException: in call_plumber Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def close_troubleshooting(self):
        try:
            if self.reporter.ActionStatus:

                if self.is_element_present(*HLS.HLS_DONE_BUTTON):
                    self.report_done('Done Button is displayed')
                    self.driver.find_element(*HLS.HLS_DONE_BUTTON).click()


        except:
            self.report_fail('Android-App : NoSuchElementException: in close_troubleshooting Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))


class MIMIC(BasePage):
    counter = 0

    def navigate_to_controlPage(self):
        if self.is_element_present(*MML.MMC_DEVICE):
            self.driver.find_element(*MML.MMC_DEVICE).click()

    def device_mimic_status(self):
        if self.reporter.ActionStatus:
            try:
                self.refresh_page()

                if self.is_element_present(*MML.MMC_CONTROL):
                    self.driver.find_element(*MML.MMC_CONTROL).click()
                    time.sleep(3)
                    if self.is_element_present(*MML.MMC_ANIMATION):
                        return 'ACTIVE'
                    else:
                        return 'INACTIVE'
                elif self.is_element_present(*MML.LIGHT_OFFLINE):
                    return 'OFFLINE'
                else:
                    self.report_fail('The control icon is not found')
                    return 'UNABLE TO FETCH STATUS'


            except:
                self.report_fail('Android-App : NoSuchElementException: in device_mimic_status Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def device_mimic_light_status(self):
        if self.reporter.ActionStatus:
            TextStatus, IconStatus = '', ''
            try:

                if self.is_element_present(*MML.MMC_LIGHTSTATUS_SUBTITLE):
                    strText = self.driver.find_element(*MML.MMC_LIGHTSTATUS_SUBTITLE).get_attribute('text')
                    TextStatus = strText

                if self.is_element_present(*MML.MMC_LIGHTSTATUS_ICON):
                    strICON = self.driver.find_element(*MML.MMC_LIGHTSTATUS_ICON).get_attribute('text')
                    if strICON == 'v':
                        IconStatus = 'ON'
                    else:
                        IconStatus = 'OFF'

                if IconStatus == '': self.report_fail('The MMC_LIGHTSTATUS_ICON is not found')
                if TextStatus == '':
                    self.report_fail('The MMC_LIGHTSTATUS_SUBTITLE is not found')
                elif self.is_element_present(*MML.LIGHT_OFFLINE):
                    TextStatus, IconStatus = 'OFFLINE', 'OFFLINE'
            except:
                self.report_fail('Android-App : NoSuchElementException: in device_mimic_light_status Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))
            return TextStatus, IconStatus

    def device_selected_count(self):
        if self.reporter.ActionStatus:
            intCount = ''
            try:
                if self.is_element_present(*MML.MMC_SELECTEDDEVICES_TEXT):
                    intCount = self.driver.find_element(*MML.MMC_SELECTEDDEVICES_TEXT).get_attribute('text').split(' ')[
                        0]
                else:
                    self.report_fail('The MMC_SELECTEDDEVICES_TEXT is not found')

            except:
                self.report_fail('Android-App : NoSuchElementException: in device_selected_count Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))
            return intCount

    def device_selected_hours(self):
        if self.reporter.ActionStatus:
            strHours = ''
            try:
                if self.is_element_present(*MML.MMS_SELECTEDHOURS_TEXT):
                    strHours = self.driver.find_element(*MML.MMS_SELECTEDHOURS_TEXT).get_attribute('text')
                else:
                    self.report_fail('The MMS_SELECTEDHOURS_TEXT is not found')

            except:
                self.report_fail('Android-App : NoSuchElementException: in device_selected_hours Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))
            return strHours

    def stop_mimic(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*MML.MMC_STOP_BUTTON):
                    self.driver.find_element(*MML.MMC_STOP_BUTTON).click()
                    time.sleep(3)
                    if self.wait_for_element_exist(*MML.MMC_POSIIVE):
                        self.driver.find_element(*MML.MMC_POSIIVE).click()
                        time.sleep(3)
                    self.refresh_page()
                    self.report_done('Screenshot after mimic stopped')
                    return 'PRESENT'
                else:
                    self.report_done('Mimic was already stopped')
                    return 'ABSENT'
            except:
                self.report_fail('Android-App : NoSuchElementException: in device_mimic_status Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def initiate_Mimic(self, lstDevice, lstHours):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*MML.MMC_ICON):
                    self.driver.find_element(*MML.MMC_ICON).click()
                    time.sleep(5)
                    if self.is_element_present(*MML.MMC_SETUP):
                        self.driver.find_element(*MML.MMC_SETUP).click()
                        time.sleep(3)
                        self.report_done('Mimic is initiated')
                        self.select_checkbox(lstDevice)
                        self.select_Hours(lstHours)
                        time.sleep(5)

                        if self.wait_for_element_exist(*MML.MMS_START_BUTTON):
                            self.driver.find_element(*MML.MMS_START_BUTTON).click()
                            time.sleep(5)
                        else:
                            self.report_fail('MMS_START_BUTTON is not found')
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                        self.refresh_page()
                        self.report_pass('Screenshot after mimic is started')
                    else:
                        self.report_fail('MMC_SETUP is not found')
                else:
                    self.report_fail('MMC_ICON is not found')
            except:
                self.report_fail('Android-App : NoSuchElementException: in set_mimic Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def set_mimic(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*MML.MMC_ICON):
                    self.driver.find_element(*MML.MMC_ICON).click()
                    time.sleep(3)
                    if self.wait_for_element_exist(*MML.MMC_POSIIVE):
                        self.driver.find_element(*MML.MMC_POSIIVE).click()
                        time.sleep(3)
                    self.report_done('Mimic is initiated')

                else:
                    self.report_fail('MMC_ICON is not found')
            except:
                self.report_fail('Android-App : NoSuchElementException: in set_mimic Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def select_checkbox(self, lstDevice):
        try:
            lstDeviceTemp = sorted(lstDevice)

            intCount = 2
            for eachItem in lstDeviceTemp:
                strLightName = eachItem
                blnLightStatus = lstDevice[eachItem]

                if intCount > 3:
                    lstLightsProperty = list(MML.MMC_LIGHTS_NAME)
                    lstLightsProperty[1] = lstLightsProperty[1].replace('index', str(intCount - 1))
                    swipeFromElementProperty = tuple(lstLightsProperty)
                    lstLightsProperty = list(MML.MMC_LIGHTS_NAME)
                    lstLightsProperty[1] = lstLightsProperty[1].replace('index', str(intCount - 2))
                    swipeToElementProperty = tuple(lstLightsProperty)
                    objLowerElement = self.driver.find_element(*swipeFromElementProperty)
                    objUpperElement = self.driver.find_element(*swipeToElementProperty)
                    intX = objLowerElement.location['x']
                    intLowerY = objLowerElement.location['y']
                    intUpperY = objUpperElement.location['y']
                    self.driver.swipe(intX, intLowerY, intX, intUpperY, 1000)

                lstLightNameProperty = list(MML.MMC_LIGHTS_NAME)
                lstLightCheckBoxProperty = list(MML.MMC_LIGHTS_CHECKBOX)
                lstLightNameProperty[1] = lstLightNameProperty[1].replace('index', str(intCount))
                objLightNameProperty = tuple(lstLightNameProperty)

                lstLightCheckBoxProperty[1] = lstLightCheckBoxProperty[1].replace('index', str(intCount))
                objLightCheckBoxProperty = tuple(lstLightCheckBoxProperty)

                strLightNameUI = self.driver.find_element(*objLightNameProperty).get_attribute('text')
                if strLightNameUI.upper() == strLightName.upper():
                    blnCheckBox = self.driver.find_element(*objLightCheckBoxProperty).get_attribute('checked')
                    if str(blnCheckBox).upper() != str(blnLightStatus).upper():
                        self.driver.find_element(*objLightCheckBoxProperty).click()
                else:
                    self.report_fail('Lights not displayed correctly')

                intCount += 1
            self.report_done('Screenshot after devices selected')
            if self.wait_for_element_exist(*MML.MMC_SAVE_BUTTON):
                self.driver.find_element(*MML.MMC_SAVE_BUTTON).click()
                time.sleep(3)
        except:
            self.report_fail('Android-App : NoSuchElementException: in select_checkbox Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def select_devices(self, lstDevice):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*MML.MMC_SELECTEDDEVICES_BUTTON):
                    self.driver.find_element(*MML.MMC_SELECTEDDEVICES_BUTTON).click()
                    time.sleep(3)

                    if self.is_element_present(*MML.MMC_SELECT_TITLE):
                        self.driver.find_element(*MML.MMC_SELECT_TITLE).click()
                        time.sleep(3)

                        self.select_checkbox(lstDevice)
                        self.report_done('Screenshot after Mimic is initiated')
                    else:
                        self.report_fail('MMC_SELECT_TITLE is not found')
                else:
                    self.report_fail('MMC_SELECTEDDEVICES_BUTTON is not found')
            except:
                self.report_fail('Android-App : NoSuchElementException: in select_devices Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def restart_Mimic(self):
        if self.reporter.ActionStatus:
            try:
                self.reporter.HTML_TC_BusFlowKeyword_Initialize("Restarting Mimic to accomadate the changes")
                time.sleep(3)
                self.stop_mimic()
                self.set_mimic()
                time.sleep(3)
                self.report_done('Screenshot after Mimic is restarted')
            except:
                self.report_fail('Android-App : NoSuchElementException: in restart_Mimic Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def select_Hours(self, lstHours, counter=0, blnNextDay=None):
        if self.reporter.ActionStatus:
            try:
                for each in range(0, len(lstHours)):
                    if counter == 0:
                        objProperty = MML.MMC_STARTTIME_BUTTON
                        objTextProperty = MML.MMC_STARTTIME_TEXT
                        objTextValidationProperty = MML.MMC_STARTTIME_TEXT
                    elif counter == 1:
                        objProperty = MML.MMC_ENDTIME_BUTTON
                        objTextProperty = MML.MMC_ENDTIME_TEXT
                        objTextValidationProperty = MML.MMC_ENDTIME_TEXT
                    else:
                        break
                    if self.is_element_present(*objProperty):
                        self.driver.find_element(*objProperty).click()
                        strTargetHour = lstHours[counter].split(':')[0]
                        strTargetMin = lstHours[counter].split(':')[1]
                        self.set_schedule_event_hour(strTargetHour)
                        self.set_schedule_event_minute(strTargetMin, 1.8, 1)

                        time.sleep(5)

                        while True:
                            if self.is_element_present(*objTextValidationProperty):
                                strTimeText = self.driver.find_element(*objTextValidationProperty).get_attribute('text')
                                if strTimeText != strTargetHour + ':' + strTargetMin:
                                    if self.counter < 3:
                                        self.counter += 1
                                        self.set_schedule_event_hour(strTargetHour, 1.8, strTimeText.split(':')[0])
                                        self.set_schedule_event_minute(strTargetMin, 1.8, 1, strTimeText.split(':')[1])
                                        time.sleep(5)
                                    else:
                                        self.report_fail('Unable to set The target time ' + strTimeText)
                                        return None
                                else:
                                    break
                            else:
                                self.report_fail('Unable to find objTextValidationProperty')
                                break

                    counter += 1

                    if self.wait_for_element_exist(*objTextValidationProperty):
                        strTimeText = self.driver.find_element(*objTextValidationProperty).get_attribute('text')
                        self.report_done('The target time ' + strTimeText + 'is set')
                self.report_done('Screenshot after hours selected')
                if self.is_element_present(*MML.MMC_NEXTDAY_TEXT):
                    blnNextDay = True
                else:
                    blnNextDay = False

                if self.wait_for_element_exist(*MML.MMC_SAVE_BUTTON):
                    self.driver.find_element(*MML.MMC_SAVE_BUTTON).click()
                    time.sleep(3)
            except:
                self.report_fail('Android-App : NoSuchElementException: in select_Hours Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))
        return blnNextDay

    def set_Hours(self, lstHours, blnNextDay=None):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*MML.MMC_SELECTEDHOURS_BUTTON):
                    self.driver.find_element(*MML.MMC_SELECTEDHOURS_BUTTON).click()
                    time.sleep(3)
                    if self.is_element_present(*MML.MMC_TIMES_TITLE):
                        self.driver.find_element(*MML.MMC_TIMES_TITLE).click()
                        time.sleep(3)
                        blnNextDay = self.select_Hours(lstHours)
                    else:
                        self.report_fail('MMC_TIMES_TITLE is not found')
                else:
                    self.report_fail('MMC_SELECTEDHOURS_BUTTON is not found')
            except:
                self.report_fail('Android-App : NoSuchElementException: in set_Hours Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))

            return blnNextDay

    def get_client_lights_status(self, devicelist, devicePositionDict, beekeeperDashboards):
        if self.reporter.ActionStatus:
            devicesStatusDict = {}
            try:
                self.honeycomb_verify()
                for eachDevice in devicelist:
                    self.honeycomb_verify()
                    if self.find_device_on_dashboard(devicePositionDict[eachDevice]):
                        deviceStatusDict = self.get_client_light_status(eachDevice)
                        devicesStatusDict.update(deviceStatusDict)
                    else:
                        self.report_fail(eachDevice + ' is not found at the given dashboard position, page - ' +
                                         str(devicePositionDict[eachDevice]['nodePage']) +
                                         ' postion- ' + str(devicePositionDict[eachDevice]['nodePosition']))

                    count = int(devicePositionDict[eachDevice]['nodePage'])
                    while count > 1:
                        self.dashboardSwipe()
                        count -= 1
            except:
                self.report_fail('Android-App : NoSuchElementException: in get_client_lights_status Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))
            return devicesStatusDict

    def set_light_state(self, devicePosition, state, deviceName, deviceMode=None):
        try:
            self.honeycomb_verify()
            time.sleep(5)
            if self.find_device_on_dashboard(devicePosition):
                mode = None
                if deviceMode is not None: mode = self.light_mode()
                if not (deviceMode in mode) and mode is not None:
                    if self.wait_for_element_exist(*MML.LIGHT_MODECHANGE_ICON):
                        self.driver.find_element(*MML.LIGHT_MODECHANGE_ICON).click()
                        time.sleep(5)
                TextStatus, IconStatus = self.light_status()
                if state != IconStatus:
                    if self.is_element_present(*MML.LIGHT_STATUS_TEXT):
                        self.driver.find_element(*MML.LIGHT_STATUS_TEXT).click()
                        time.sleep(5)
                self.report_done('Light ' + deviceName + ' is turned ' + state)
                if self.is_element_present(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON):
                    self.driver.find_element(*HoneycombDashboardLocators.HONEYCOMB_ICON_BUTTON).click()
                count = int(devicePosition['nodePage'])
                while count > 1:
                    self.dashboardSwipe()
                    count -= 1


        except:
            self.report_fail('Android-App : NoSuchElementException: in set_light_state Method\n '
                             '{0}'.format(traceback.format_exc().replace('File', '$~File')))

    def light_mode(self):
        if self.reporter.ActionStatus:
            mode = ''
            try:
                if self.wait_for_element_exist(*MML.LIGHT_MODE_VIEW):
                    mode = self.driver.find_element(*MML.LIGHT_MODE_VIEW).get_attribute('text')
                elif self.is_element_present(*MML.LIGHT_OFFLINE):
                    mode = 'OFFLINE'
                else:
                    self.report_fail('The LIGHT_MODE_VIEW is not found')
            except:
                self.report_fail('Android-App : NoSuchElementException: in light_mode Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))
            return mode

    def light_status(self):
        if self.reporter.ActionStatus:
            TextStatus, IconStatus = '', ''
            try:
                if self.is_element_present(*MML.LIGHT_OFFLINE):
                    TextStatus, IconStatus = 'OFFLINE', 'OFFLINE'
                else:
                    if self.is_element_present(*MML.LIGHT_STATUS_TEXT):
                        strText = self.driver.find_element(*MML.LIGHT_STATUS_TEXT).get_attribute('text')
                        TextStatus = strText.split(' ')[0].upper()
                    else:
                        self.report_fail('The LIGHT_STATUS_TEXT is not found')

                    if self.is_element_present(*MML.MMC_LIGHTSTATUS_ICON):
                        strICON = self.driver.find_element(*MML.MMC_LIGHTSTATUS_ICON).get_attribute('text')
                        if strICON == 'v':
                            IconStatus = 'ON'
                        else:
                            IconStatus = 'OFF'
                    else:
                        self.report_fail('The MMC_LIGHTSTATUS_ICON is not found')
            except:
                self.report_fail('Android-App : NoSuchElementException: in get_light_status Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))
            return TextStatus, IconStatus

    def get_client_light_status(self, deviceName):
        if self.reporter.ActionStatus:
            deviceStatusDict = {}
            TextStatus, IconStatus, mimicStatus = '', '', ''
            try:

                displayedDeviceName = self.driver.find_element(*MML.MMC_TITLE).get_attribute('text')
                if deviceName == displayedDeviceName:
                    mimicStatus = self.device_mimic_status()
                    self.report_done('Light ' + deviceName)
                    if mimicStatus == 'ACTIVE':
                        TextStatus, IconStatus = self.device_mimic_light_status()
                    else:
                        TextStatus, IconStatus = self.light_status()
                    if TextStatus == 'OFFLINE':   self.report_done(deviceName + ' is offlnie')
                else:
                    self.report_fail(deviceName + ' is not found')

                deviceStatusDict = {
                    deviceName: {'mimicStatus': mimicStatus, 'textStatus': TextStatus, 'IconStatus': IconStatus}}
            except:
                self.report_fail('Android-App : NoSuchElementException: in get_client_lights_status Method\n '
                                 '{0}'.format(traceback.format_exc().replace('File', '$~File')))
            return deviceStatusDict

    def GotoMimicFlowScreeninApp(self, ScreenName):
        if self.reporter.ActionStatus:
            print("Mimic page navigations are yet to be done")

    def verifyLocalisedCopyTextAndroid(self, Language):
        if self.reporter.ActionStatus:
            print("Localiased copy text validation is yet to be done")
