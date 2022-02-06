"""
Created on 16 Jun 2015

@author: ranganathan.veluswamy

@author: Hitesh Sharma 15 July 2016
@note:
1. naivgate_to_ZoneNotificaiton function is used to navigate to Heating notification screen
2. setHighTemperature and setLowTemperature functions enables navigation to Maximum Temperature screen and Minimum Temperature respectively to validate that all elements are present correctly on screen
3. receiveWarnings function enable to set ON/OFF warnings.
4. setNotificationONtoOFF function reset the High and Low Target temperature and disable heating notification (warnings)
5. set_target_Heating_notification_temperature set the the desired temperature(Min and Max)
"""

from datetime import datetime, timedelta
import os
import time
import traceback
import math

#from appium import webdriver
#from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from EE_Locators_iOSApp import DashboardPageLocators, RecipeScreenLocators
from EE_Locators_iOSApp import DashboardTutorialPageLocators
from EE_Locators_iOSApp import ChangePasswordLocators
from EE_Locators_iOSApp import EditTimeSlotPageLocators, TextControlLocators, HolidayModePageLocators
from selenium.webdriver.common.by import By
from EE_Locators_iOSApp import HeatingControlPageLocators
from EE_Locators_iOSApp import HeatingNotification
from EE_Locators_iOSApp import HomePageLocators
from EE_Locators_iOSApp import HotWaterControlPageLocators
from EE_Locators_iOSApp import LoginPageLocators
from EE_Locators_iOSApp import PinLockPageLocators
from EE_Locators_iOSApp import SchedulePageLocators
from EE_Locators_iOSApp import MotionSensorPageLocators
from EE_Locators_iOSApp import BulbScreenLocators, LeakSensorPageLocators
from EE_Locators_iOSApp import PlugLocators, MainMenuLocators
from EE_Locators_iOSApp import DashboardCustomisationLocators, NATLocators
import json
import FF_Platform_Utils as oAPIValidations
import FF_ScheduleUtils as oSchedUtils
import FF_utils as utils
import calendar
from EE_Locators_iOSApp import ContactSensorLocators


class BasePage(object):
    # Contructor for BasePage
    def __init__(self, driver, reporter):
        self.driver = driver
        self.reporter = reporter
        self.currentAppVersion = utils.getAttribute('common', 'currentAppVersion').upper()
        self.EXPLICIT_WAIT_TIME = 25
        self.stopBoost = True

    # Waits for the given element exists for EXPLICIT_WAIT_TIME
    def wait_for_element_exist(self, by, value, intWaitTime=0):
        if intWaitTime == 0: intWaitTime = self.EXPLICIT_WAIT_TIME
        try:
            wait = WebDriverWait(self.driver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            time.sleep(1)
            return True
        except TimeoutException:
            return False

    # Initializes the Appium Android Web Driver
    def setup_ios_driver(self, strDeviceName, strAppPath, strDeviceLogger, strAutomationName):
        try:
            desired_caps = {}
            ''' Real device
            desired_caps['appium-version'] = '1.0'
            desired_caps['platformName'] = 'iOS'
            desired_caps['platformVersion'] = utils.getAttribute('iOS', 'platformVersion')
            desired_caps['udid'] = utils.getAttribute('iOS', 'udid')
            desired_caps['deviceName'] = strDeviceName
            desired_caps['app'] = os.path.abspath(strAppPath)
            desired_caps['fullReset'] = False
            desired_caps['realDeviceLogger'] = strDeviceLogger
            desired_caps['automationName'] = strAutomationName
            # desired_caps['app'] = '/Users/sbala/Documents/HiveTestAutomation/02_Manager_Tier/EnviromentFile/Apps/iOS/isoInterProd/Hive.app'
            desired_caps['noReset'] = True
            desired_caps['newCommandTimeout'] = 10000
            #desired_caps['realDeviceconsole'] = strRealDeviceconsole
            #desired_caps['automationName'] = strAutomationName'''

            # Simulator
            desired_caps['appium-version'] = '1.0'
            desired_caps['platformName'] = 'iOS'
            desired_caps['platformVersion'] = '10.2'
            # desired_caps['udid'] = utils.getAttribute('iOS', 'udid')
            desired_caps['deviceName'] = 'iPhone Simulator'
            desired_caps['app'] = '/Applications/Hive.app'
            desired_caps['fullReset'] = False
            # desired_caps['realDeviceLogger'] = strDeviceLogger
            desired_caps['automationName'] = strAutomationName
            # desired_caps['app'] = '/Users/sbala/Documents/HiveTestAutomation/02_Manager_Tier/EnviromentFile/Apps/iOS/isoInterProd/Hive.app'
            desired_caps['noReset'] = True
            desired_caps['newCommandTimeout'] = 0
            # desired_caps['realDeviceconsole'] = strRealDeviceconsole
            # desired_caps['automationName'] = strAutomationName

            iOSDriver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
            iOSDriver.implicitly_wait(5)

            return iOSDriver
        except:
            self.report_fail('Exception in setup_ios_driver Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

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
        intEndX = intStX
        intEndY = intUpperY + fltScrolPrecesion * (intHieght / 4)
        intStY = intUpperY + 3 * (intHieght / 4)
        intScrolTime = 500
        if fltPrecision != 0.5:
            intEndY = intUpperY + 2.2 * (intHieght / 4)
            intStY = intUpperY + 1.8 * (intHieght / 4)
            intScrolTime = 500
        if not fltSetValue == fltCurrentValue:
            if fltSetValue > fltCurrentValue:
                intTemp = intEndY
                intEndY = intStY
                intStY = intTemp
            intIterCount = int(abs(fltSetValue - fltCurrentValue) / fltPrecision)
            for intCnt in range(intIterCount):
                # self.driver.swipe(intStX, intEndY, intEndX, intStY, intScrolTime)
                TouchAction(self.driver).press(None, intStX, intStY).wait(1000).move_to(None, intEndX - intStX,
                                                                                        intEndY - intStY).release().perform()
                time.sleep(3)

    # Scrolls on the Scrollable element to set the specific value passed for HolidayMode Page
    def scroll_element_to_value_date(self, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision):
        intLeftX = oScrolElement.location['x']
        intUpperY = oScrolElement.location['y']
        intWidth = oScrolElement.size['width']
        intHieght = oScrolElement.size['height']
        intStX = intLeftX + intWidth / 2
        intStY = intUpperY + (intHieght / 4)
        intEndX = intStX
        intEndY = intUpperY + (intHieght / 8)
        intSize = len(fltSetValue)
        if intSize > 2:
            fltdate = fltSetValue.split(' ')[1]
            while not fltdate in fltCurrentValue:
                self.iOSDriver.swipe(intStX, intStY, intEndX, intEndY, 1000)
                fltCurrentValue = int(oScrolElement.get_attribute('value').split(' ')[0])
        else:
            if not fltSetValue == fltCurrentValue:
                intIterCount = int(abs(fltSetValue - fltCurrentValue) / fltPrecision)
                for intCnt in range(intIterCount):
                    print(intCnt)
                    self.iOSDriver.swipe(intStX, intStY, intEndX, intEndY, 1000)
                    time.sleep(0.5)

    def scroll_to_set_temp(self, oScrolElement, fltCurrentValue, fltSetValue, intIterCount):
        intLeftX = oScrolElement.location['x']
        intUpperY = oScrolElement.location['y']
        intWidth = oScrolElement.size['width']
        intHeight = oScrolElement.size['height']
        intStX = intLeftX + intWidth / 2
        intStY = intUpperY + intHeight / 2
        intEndX = intStX
        diff = (intHeight / 3)
        status = 'false'

        for intCnt in range(intIterCount):
            if fltSetValue < fltCurrentValue:
                TouchAction(self.driver).press(None, intStX, intStY).wait(1000).move_to(None, intEndX - intStX, -(
                    intStY - diff)).release().perform()
            elif fltSetValue > fltCurrentValue:
                TouchAction(self.driver).press(None, intStX, intStY).wait(1000).move_to(None, intEndX - intStX,
                                                                                        intStY - diff).release().perform()
            time.sleep(1)
            oScrolElementValue = oScrolElement.get_attribute('value')
            if 'point' in oScrolElementValue:
                fltCurrentValue = float(oScrolElementValue.split(' ')[4] + '.' + oScrolElementValue.split(' ')[6])
            else:
                fltCurrentValue = float(oScrolElementValue.split(' ')[4])
            print(fltCurrentValue, fltSetValue)
            if fltSetValue == fltCurrentValue:
                self.report_pass('iOS APP: The Target Temperature is successfully set to : ' + str(fltSetValue))
                status = 'true'
                break
        return status

    def trimHolidayString(self, value):
        if ',' in value:
            value = value.replace(",", "")
        if 'clock' in value:
            value = value.replace(" o’clock", "")
        if 'minutes' in value:
            value = value.replace(" minutes", "")
        elif 'minute' in value:
            value = value.replace(" minute", "")
        return value

    # Scrolls on the Scrollable element to set the specific value passed for HolidayMode Page
    def scroll_Date_Hour_Minute(self, oPicker, fltCurrentValue, fltSetValue, counter, pickerType):
        try:
            intLeftX = oPicker.location['x']
            intUpperY = oPicker.location['y']
            intWidth = oPicker.size['width']
            intHeight = oPicker.size['height']
            intStX = intLeftX + intWidth / 2
            intStY = intUpperY + (intHeight / 2)
            # intEndX = intStX
            # intEndY = intUpperY + (intHeight/2)
            intIterCount = 0
            fltCurrentValue = self.trimHolidayString(fltCurrentValue)
            while intIterCount < counter:
                if fltSetValue != fltCurrentValue:
                    if "DATE" not in pickerType.upper():
                        if int(fltSetValue) < int(fltCurrentValue):
                            diff = int(fltCurrentValue) - int(fltSetValue)
                        else:
                            diff = int(fltSetValue) - int(fltCurrentValue)
                        if "HOUR" in pickerType.upper():
                            standDiff = 12  # Hours
                        elif "MINUTE" in pickerType.upper():
                            standDiff = 30  # Minutes
                        if fltSetValue < fltCurrentValue and diff <= standDiff:
                            TouchAction(self.driver).press(None, intStX, intStY).wait(1000).move_to(None, intStX,
                                                                                                    40).release().perform()  # 40 is baseline to scroll one element down
                        elif fltSetValue < fltCurrentValue and diff > standDiff:
                            TouchAction(self.driver).press(None, intStX, intStY).wait(1000).move_to(None, intStX,
                                                                                                    -40).release().perform()  # -40 is baseline to scroll one element up
                        elif fltSetValue > fltCurrentValue and diff <= standDiff:
                            TouchAction(self.driver).press(None, intStX, intStY).wait(1000).move_to(None, intStX,
                                                                                                    -40).release().perform()  # -40 is baseline to scroll one element up
                        elif fltSetValue > fltCurrentValue and diff > standDiff:
                            TouchAction(self.driver).press(None, intStX, intStY).wait(1000).move_to(None, intStX,
                                                                                                    40).release().perform()  # 40 is baseline to scroll one element down
                    else:
                        TouchAction(self.driver).press(None, intStX, intStY).wait(1000).move_to(None, intStX,
                                                                                                -40).release().perform()  # -40 is baseline to scroll one element up
                    time.sleep(5)
                    fltCurrentValue = oPicker.get_attribute('value')
                    fltCurrentValue = self.trimHolidayString(fltCurrentValue)
                    intIterCount = (intIterCount + 1)
                else:
                    break
        except:
            self.report_fail('iOS-App: Exception in scroll_element_to_value_date method \n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Method for Skipping Dashboard Tutorial
    def skip_Dashboard_tutorial(self):
        try:
            time.sleep(3)
            self.driver.find_element(*DashboardTutorialPageLocators.ALLOW_BUTTON).click()
            time.sleep(5)
            self.driver.find_element(*DashboardTutorialPageLocators.NEXT_BUTTON).click()
            time.sleep(5)
            self.driver.find_element(*DashboardTutorialPageLocators.NEXT_BUTTON).click()
            time.sleep(5)
            self.driver.find_element(*DashboardTutorialPageLocators.NEXT_BUTTON).click()
            time.sleep(5)
            self.driver.find_element(*DashboardTutorialPageLocators.NEXT_BUTTON).click()
            time.sleep(5)
            self.driver.find_element(*DashboardTutorialPageLocators.DONE_BTN).click()
            time.sleep(5)

            if self.driver.find_element(*HomePageLocators.MENU_BUTTON):
                self.report_pass('iOS-App: The Hive iOS App is successfully Logged in')

        except:
            self.report_fail('iOS-App: Exception in skip_Dashboard_tutorial\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def is_element_present(self, by, value=None):
        # Return a boolean value for an  element presence
        try:
            self.driver.find_element(by, value)

        except NoSuchElementException as e:
            return False
        return True
        # Refresh Page

    def refresh_page(self):
        # self.driver.swipe(200, 200, 200, 500, 500)
        TouchAction(self.driver).press(None, 200, 100).wait(2000).move_to(None, 0, 300).release().perform()
        time.sleep(3)

    def refresh_heatingpage(self):
        # self.driver.swipe(200, 200, 200, 500, 500)
        TouchAction(self.driver).press(None, 300, 150).wait(2000).move_to(None, 0, 300).release().perform()
        time.sleep(3)

    # Add/Delete Events to match the expected count
    def add_or_remove_events(self, intExpectedEventCount):
        self.report_done('iOS APP: ScreenShot of existing schedule')
        intActualCount = 0
        # Get Event Count
        if self.is_element_present(*SchedulePageLocators.SLOT_SIX):
            intActualCount = 6
        elif self.is_element_present(*SchedulePageLocators.SLOT_FIVE):
            intActualCount = 5
        elif self.is_element_present(*SchedulePageLocators.SLOT_FOUR):
            intActualCount = 4
        elif self.is_element_present(*SchedulePageLocators.SLOT_THREE):
            intActualCount = 3
        elif self.is_element_present(*SchedulePageLocators.SLOT_TWO):
            intActualCount = 2
        elif self.is_element_present(*SchedulePageLocators.SLOT_ONE):
            intActualCount = 1
        print(intActualCount, intExpectedEventCount)
        if intActualCount == intExpectedEventCount:
            self.report_done('IOS App : Expected number of slots available')
        elif intActualCount > intExpectedEventCount:
            # Delete Event
            self.report_step('Deleting additional events')
            for intCntr in range(intActualCount, intExpectedEventCount, -1):
                if self.is_element_present(*SchedulePageLocators.SLOT_SIX):
                    self.driver.find_element(*SchedulePageLocators.SLOT_SIX).click()
                elif self.is_element_present(*SchedulePageLocators.SLOT_FIVE):
                    self.driver.find_element(*SchedulePageLocators.SLOT_FIVE).click()
                elif self.is_element_present(*SchedulePageLocators.SLOT_FOUR):
                    self.driver.find_element(*SchedulePageLocators.SLOT_FOUR).click()
                elif self.is_element_present(*SchedulePageLocators.SLOT_THREE):
                    self.driver.find_element(*SchedulePageLocators.SLOT_THREE).click()
                elif self.is_element_present(*SchedulePageLocators.SLOT_TWO):
                    self.driver.find_element(*SchedulePageLocators.SLOT_TWO).click()
                if self.is_element_present(*SchedulePageLocators.DELETE_TIME_SLOT):
                    self.driver.find_element(*SchedulePageLocators.DELETE_TIME_SLOT).click()
                    if self.is_element_present(*SchedulePageLocators.DELETE_TIME_SLOT_POPUP):
                        self.driver.find_element(*SchedulePageLocators.DELETE_TIME_SLOT_POPUP).click()
                    else:
                        self.report_fail('IOS App : Delete pop up was not displayed')
                else:
                    self.report_fail('IOS App : Delete time slot option was not displayed')
            self.report_done('IOS App : Additional slots deleted')
        elif intActualCount < intExpectedEventCount:
            # Add Event
            # self.report_step('Adding additional events')
            for intCntr in range((intExpectedEventCount - 1), intActualCount - 1, -1):
                self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                if self.wait_for_element_exist(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU):
                    self.driver.find_element(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU).click()
                    # self.report_done('iOS APP: Adding additional event number : ' + str(intCntr + 1))
                    self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                    # self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)
                    self.wait_for_element_exist(*SchedulePageLocators.EVENT_ARROW)
                elif self.wait_for_element_exist(*SchedulePageLocators.ALL_SLOTS_FILLED):
                    self.report_done('IOS App : All slots are filled')
                    self.driver.find_element(*SchedulePageLocators.CANCEL_SUBMENU).click()
                    break

        self.refresh_page()
        self.report_pass('ScreenShot after all additional events are added/removed')

    def navigate_to_device(self, nameOfDevice):
        Device_off = str(HomePageLocators.strLOCAL_OFF)
        Device_On = str(HomePageLocators.strLOCAL_ON)
        Device_Offline = str(HomePageLocators.strLOCAL_OFFLINE)

        M_OFF1 = Device_off.replace("name", nameOfDevice)
        M_ON1 = Device_On.replace("name", nameOfDevice)
        M_OFFLINE1 = Device_Offline.replace("name", nameOfDevice)

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()

                if self.is_element_present(By.XPATH, M_ON1):
                    self.driver.find_element(By.XPATH, M_ON1).click()
                    self.report_pass('IOS App : Navigated to device ' + nameOfDevice + ' screen')
                    time.sleep(3)
                elif ('offline' in M_OFFLINE1) & self.is_element_present(By.XPATH, M_OFFLINE1):
                    self.driver.find_element(By.XPATH, M_OFFLINE1).click()
                    self.report_pass(
                        'IOS App : Navigated to ' + nameOfDevice + ' screen where the device is offline')
                    time.sleep(3)

                elif self.is_element_present(By.XPATH, M_OFF1):
                    self.driver.find_element(By.XPATH, M_OFF1).click()
                    self.report_pass('IOS App : Navigated to device screen ' + nameOfDevice + ' screen')
                    time.sleep(3)
                else:
                    self.report_fail('IOS App : The given device does not exist in the kit')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_motionsensor Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

                # Navigate to the Day of the Week

    def _navigate_to_day(self, strDay):
        if self.reporter.ActionStatus:
            try:
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

                self.refresh_page()
            except:
                self.report_fail('Exception in _navigate_to_day Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set the Even Target temperature
    def set_schedule_event_hour(self, intSetHour):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.TITLE_LABEL) or self.wait_for_element_exist(
                        *EditTimeSlotPageLocators.ADD_SLOT_TITLE_LABEL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                    intSetHour = int(intSetHour)
                    intCurrentHour = int(oScrolElement.get_attribute('value').split(' ')[0])
                    intCntrIter = 1
                    while (intCurrentHour != intSetHour) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, intCurrentHour, intSetHour, 1, 1)
                        intCurrentHour = int(oScrolElement.get_attribute('value').split(' ')[0])
                        intCntrIter = +1
                    if intCurrentHour == intSetHour:
                        print('')
                        # self.report_pass('The start time Hour is successfully set to : ' + str(intSetHour))
                    else:
                        self.report_fail('Unable to set the start time Hour to : ' + str(intSetHour))

                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Edit Time Slot for Heating schedule Page to set the Event start time Hour")

            except:
                self.report_fail('iOS APP: Exception in set_schedule_event_hour Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set the Even Target temperature
    def set_schedule_event_minute(self, intSetMinute):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.TITLE_LABEL) or self.wait_for_element_exist(
                        *EditTimeSlotPageLocators.ADD_SLOT_TITLE_LABEL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                    intSetMinute = int(intSetMinute)
                    intCurrentMinute = int(oScrolElement.get_attribute('value').split(' ')[0])
                    intCntrIter = 1
                    while (intCurrentMinute != intSetMinute) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, intCurrentMinute, intSetMinute, 15, 1)
                        intCurrentMinute = int(oScrolElement.get_attribute('value').split(' ')[0])
                        intCntrIter = +1
                    if intCurrentMinute == intSetMinute:
                        print('')
                        # self.report_pass('iOS APP: The start time minute is successfully set to : ' + str(intSetMinute))
                    else:
                        self.report_fail('iOS APP: Unable to set the start time minute to : ' + str(intSetMinute))
                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Edit Time Slot for Heating schedule Page to set the Event start time Minute")

            except:
                self.report_fail('iOS APP: Exception in set_schedule_event_minute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Click Element via TouchAction
    def click_element(self, by, value=None):
        if value is None:
            oElement = by
        else:
            oElement = self.driver.find_element(by, value)
        action = TouchAction(oElement.parent)
        action.press(oElement).perform()

        # Set the Boost Time

    def set_boost_time_duration(self, intSetHour):
        if self.reporter.ActionStatus:
            try:

                self.driver.find_element(*HeatingControlPageLocators.BOOST_CURRENT_TIME_BUTTON).click()
                time.sleep(2)
                if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_TIME_SCROLL):
                    oScrolElement = self.driver.find_element(*HeatingControlPageLocators.BOOST_TIME_SCROLL)
                    intSetHour = int(intSetHour)
                    if intSetHour == 0.5:
                        intSetHour = 0
                    intCurrentHour = oScrolElement.get_attribute('value')
                    if '30' in intCurrentHour:
                        intCurrentHour = 0
                    else:
                        intCurrentHour = int(intCurrentHour.split(' ')[0])
                    self.scroll_element_to_value(oScrolElement, intCurrentHour, intSetHour, 1, 1.8)
                    self.driver.find_element(*HeatingControlPageLocators.BOOST_SAVE).click()

                else:
                    self.report_fail(
                        "Ios-App : Control not active on the Edit Boost Time for schedule Page to set the Boost duration Hour")

            except:
                self.report_fail('Android App : Exception: in set_boost_time_duration Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Page Class for Login page. Has all the methods for the Login page
class LoginPage(BasePage):
    # Select execution environment
    def select_environment(self, env):
        try:
            if self.is_element_present(*LoginPageLocators.TITLE_LABEL):
                if self.is_element_present(*LoginPageLocators.HIVE_LOGO):

                    oElement = self.driver.find_element(*LoginPageLocators.HIVE_LOGO)
                    action = TouchAction(self.driver)
                    action.press(oElement).wait(3000).release().perform()
                    time.sleep(5)
                else:
                    self.report_fail('Hive Logo not present')
            else:
                self.report_fail('User is not on Login Screen.')
            if self.is_element_present(*LoginPageLocators.LOGIN_OPTIONS):
                if env == 'isopBeta':
                    self.driver.find_element(*LoginPageLocators.BETA).click()
                elif env == 'isopInternProd':
                    self.driver.find_element(*LoginPageLocators.INT_PROD).click()
                elif env == 'isopStaging':
                    self.driver.find_element(*LoginPageLocators.STAGING).click()
                elif env == 'isopProd':
                    self.driver.find_element(*LoginPageLocators.LIVE).click()
                elif env == 'isopBetaUS':
                    self.driver.find_element(*LoginPageLocators.NA_BETA).click()
                TouchAction(self.driver).press(None, 329, 683).wait(2000).move_to(None, 0, -317).release().perform()
                if self.is_element_present(*LoginPageLocators.DONT_LOGIN):
                    self.driver.find_element(*LoginPageLocators.DONT_LOGIN).click()
                else:
                    self.report_fail('Dont login option not available')
                self.driver.find_element(*LoginPageLocators.LOGIN_OPTIONS_DONE).click()
            else:
                self.report_fail('User is not on Login Options screen')

        except:
            self.report_fail('iOS-App: Exception in select_hive_environment Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Log in to the Hive Mobile App
    def login_hive_app(self, strUserName, strPassword):
        # self.driver.reset()
        try:
            if self.is_element_present(*LoginPageLocators.TITLE_LABEL):
                self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys(strUserName)
                self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys(strPassword)
                time.sleep(2)
                self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                time.sleep(10)

                if self.is_element_present(*DashboardTutorialPageLocators.ALLOW_BUTTON):
                    self.skip_Dashboard_tutorial()

                elif self.driver.find_element(*HomePageLocators.MENU_BUTTON):
                    self.report_pass('iOS-App: The Hive iOS App is successfully Logged in')

                else:
                    self.report_fail(
                        'iOS-App: The Hive iOS App is not logged in. Please check the Login credentials and re-execute test.')
            else:
                self.report_fail(
                    'iOS-App: The Hive iOS App is not logged in. Please check the Login credentials and re-execute test.')

        except:
            self.report_fail('iOS-App: Exception in login_hive_app Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))


# Page Class for Home page. Has all the methods for the Home page
class HomePage(BasePage):
    # Navigates to the Heating control Page
    def navigate_to_heating_control_page(self, boolStopBoost=True):
        if self.reporter.ActionStatus:
            try:
                LeakSensor.navigate_to_device_updated(self, "Heating")
                # if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HEATING CONTROL') >= 0:
                #     print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                #
                #     if self.wait_for_element_exist(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                #         self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                #         time.sleep(2)
                #         self.driver.find_element(*DashboardPageLocators.HEAT_CONTROL_DASHBOARD).click()
                #
                #     elif self.wait_for_element_exist(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                #         self.driver.find_element(*DashboardPageLocators.HEAT_CONTROL_DASHBOARD).click()
                #         time.sleep(2)
                #
                #     print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                #     if self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HEATING BOOST') >= 0:
                #         if not boolStopBoost:
                #             self.report_pass('iOS-App: Successfully navigated to the Heat BOOST Control Page -' )
                #             return True
                #         if self.is_element_present(*HeatingControlPageLocators.BOOST_STOP):
                #             self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP).click()
                #             time.sleep(2)
                #             if self.is_element_present(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL):
                #                 self.report_pass('iOS-App: Successfully navigated to the Heating Control Page')
                #             else:
                #                 self.report_fail('iOS-App: Unable to navigate to Heating Control Page')
                #
                #     elif self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HEATING') >= 0:
                #         self.report_pass('iOS-App: Successfully navigated to the Heating Control Page')
                #     else:
                #         self.report_fail("iOS-App: Control not active on the Main Home Page to Navigate to Heating Control Page")
                #
            except:
                self.report_fail('iOS-App: Exception in navigate_to_heating_conrtol_page Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Navigates to the Heating Schedule Page
    def navigate_to_heating_schedule_page(self):
        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        'HEATING SCHEDULE') >= 0:
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                    if self.wait_for_element_exist(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                        time.sleep(2)

                    elif self.wait_for_element_exist(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HEAT_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                        time.sleep(2)
                        if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                            self.report_pass('iOS-App: Successfully navigated to the Heating Schedule Page')
                        else:
                            self.report_fail('iOS-App: Unable to navigate to Heating Schedule Page')
                    else:
                        self.report_fail(
                            "iOS-App: Control not active on the Main Home Page to Navigate to Heating Schedule Page")

            except:
                self.report_fail('iOS-App: Exception in navigate_to_heating_schedule_page Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Navigates to the Hot water Home Page
    def navigate_to_hot_water_control_page(self, boolStopBoost=True):
        if self.reporter.ActionStatus:
            try:
                self.refresh_page()
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        'HOT WATER CONTROL') >= 0:

                    if self.is_element_present(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.HOT_WATER_CONTROL_DASHBOARD).click()

                    elif self.is_element_present(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HOT_WATER_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                    if self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                            'HOT WATER BOOST') >= 0:
                        if not boolStopBoost:
                            self.report_pass('iOS-App: Successfully navigated to the Hot Water Control Page -')
                            return True
                        if self.is_element_present(*HotWaterControlPageLocators.BOOST_STOP):
                            self.driver.find_element(*HotWaterControlPageLocators.BOOST_STOP).click()
                            time.sleep(2)
                        if self.wait_for_element_exist(*HotWaterControlPageLocators.BOOST_MODE_LINK):
                            self.report_pass('iOS-App: Successfully navigated to the Hot Water Control Page')
                        else:
                            self.report_fail('iOS-App: Unable to navigate to Hot Water Control Page')
                    elif self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                            'HOT WATER CONTROL') >= 0:
                        self.report_pass('iOS-App: Successfully navigated to the Hot Water Control Page -')
                    else:
                        self.report_fail(
                            "iOS-App: Control not active on the Main Home Page to Navigate to Hot Water Control Page")
            except:
                self.report_fail('iOS-App: Exception in navigate_to_hot_water_control_page Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Navigates to the Hot water schedule Home Page
    def navigate_to_hot_water_schedule_page(self):

        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        'HOT WATER SCHEDULE') >= 0:

                    if self.is_element_present(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.HOT_WATER_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()

                    elif self.is_element_present(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HOT_WATER_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                        time.sleep(2)
                    strTitile = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    if self.is_element_present(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON) and strTitile.upper().find(
                            'HOT WATER SCHEDULE') >= 0:
                        self.report_pass('iOS-App: Successfully navigated to the Hot Water Schedule Page')
                    else:
                        self.report_fail('iOS-App: Unable to navigate to Hot Water Schedule Page')

                elif self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find(
                        'HOT WATER SCHEDULE') >= 0:
                    self.report_pass("iOS-App: Successfully navigated to the Hot Water Schedule Page")
                else:
                    self.report_fail(
                        "iOS-App: Control not active on the Main Home Page to Navigate to Hot Water Schedule Page")
            except:
                self.report_fail('iOS-App: Exception in navigate_to_hot_water_control_page Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Navigates to the plug schedule Home Page
    def navigate_to_plug_schedule_page(self):

        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute(
                        'name').upper().find('PLUG SCHEDULE') >= 0:

                    if self.is_element_present(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.PLUG_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()

                    elif self.is_element_present(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.PLUG_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                        time.sleep(2)
                    else:
                        self.report_fail('iOS-App: Unable to navigate to Plug Schedule Page')

                elif self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute(
                        'name').upper().find(
                    'PLUG SCHEDULE') >= 0:
                    self.report_pass("iOS-App: Successfully navigated to the Plug Schedule Page")
                else:
                    self.report_fail(
                        "iOS-App: Control not active on the Main Home Page to Navigate to Plug Schedule Page")
            except:
                self.report_fail('iOS-App: Exception in navigate_to_plug_control_page Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Log out of the Hive Mobile App

    def logout_hive_app(self):
        # self.driver.reset()
        try:
            if self.is_element_present(*HomePageLocators.SKIP_BUTTON):
                self.driver.find_element(*HomePageLocators.SKIP_BUTTON).click()

            if self.is_element_present(*LoginPageLocators.LOGIN_BUTTON):
                self.report_pass('iOS-App: The Hive iOS App is already Logged out')

            else:
                if self.is_element_present(*DashboardTutorialPageLocators.ALLOW_BUTTON):
                    self.skip_Dashboard_tutorial()
                if self.is_element_present(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.driver.swipe(200, 500, 200, 200, 500)
                    self.wait_for_element_exist(*LoginPageLocators.LOG_OUT_BUTTON)
                    self.driver.find_element(*LoginPageLocators.LOG_OUT_BUTTON).click()

                elif self.wait_for_element_exist(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                    self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.driver.swipe(200, 500, 200, 200, 500)
                    self.wait_for_element_exist(*LoginPageLocators.LOG_OUT_BUTTON)
                    self.driver.find_element(*LoginPageLocators.LOG_OUT_BUTTON).click()
                if self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON):
                    self.report_pass('iOS-App: The Hive iOS App is successfully Logged out')
                else:
                    self.report_fail('iOS-App: Not able to Logout the Hive iOS App ')

        except:
            self.report_fail('iOS-App: Exception in logout_hive_app Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Navigate To ChangePassword Screen
    def navigate_to_screen(self, strPageName):

        if self.reporter.ActionStatus:
            try:

                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    time.sleep(2)
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    if 'PASSWORD' in strPageName.upper():
                        if self.wait_for_element_exist(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU):
                            self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU).click()
                            time.sleep(2)
                            self.report_pass('iOS-App: Successfully navigated to the Change Password Page')
                        else:
                            self.report_fail("IOS-App : Control not active on the Change Password Page")
                    else:
                        self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                else:
                    self.report_fail("IOS-App : Control not active on the Menu Button")
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_change_password_screen\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Page Class for Heating Control page. Has all the methods for the Heating Control page
class HeatingControlPage(BasePage):
    # Set Heat mode
    def set_heat_mode(self, strMode, intTemperature=None, intDuration=1):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL):
                    self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP).click()
                    time.sleep(2)
                    self.driver.execute_script("mobile: scroll", {"direction": "up"})
                    time.sleep(2)
                    if strMode.upper() == 'AUTO':
                        self.driver.find_element(*HeatingControlPageLocators.SCHEDULE_MODE_LINK).click()
                    elif strMode.upper() == 'MANUAL':
                        self.driver.find_element(*HeatingControlPageLocators.MANUAL_MODE_LINK).click()
                    elif strMode.upper() == 'OFF':
                        self.driver.find_element(*HeatingControlPageLocators.OFF_MODE_LINK).click()
                    elif strMode.upper() == 'BOOST':
                        self.driver.find_element(*HeatingControlPageLocators.BOOST_MODE_LINK).click()
                        time.sleep(5)
                        print('intDuration', intDuration)
                        if self.currentAppVersion == 'V6':
                            # Set Boost Duration
                            if intDuration != 1:
                                intCurrentDuration = int(self.driver.find_element(
                                    *HeatingControlPageLocators.BOOST_TIME_SCROLL).get_attribute('value').split(' ')[0])
                                print('intCurrentDuration', intCurrentDuration)
                                print('intDuration', intDuration)
                                intCntrIter = 1
                                while (intCurrentDuration != intDuration) and (intCntrIter < 3):
                                    time.sleep(2)
                                    self.set_boost_time_duration(intDuration)
                                    intCurrentDuration = int(self.driver.find_element(
                                        *HeatingControlPageLocators.BOOST_TIME_SCROLL).get_attribute('value').split(
                                        ' ')[0])
                                    intCntrIter += 1

                            # Set Boost Target temperature
                            if intTemperature is not None:
                                oScrolElement = self.driver.find_element(
                                    *HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                                oScrolElementVAlue = oScrolElement.get_attribute('value')
                                if 'point' in oScrolElementVAlue:
                                    fltCurrentTargTemp = float(
                                        oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                                else:
                                    fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                                intCntrIter = 1
                                while (fltCurrentTargTemp != intTemperature) and (intCntrIter < 3):
                                    self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, intTemperature, 0.5,
                                                                 1)
                                    oScrolElementVAlue = oScrolElement.get_attribute('value')
                                    if 'point' in oScrolElementVAlue:
                                        fltCurrentTargTemp = float(
                                            oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                                    else:
                                        fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                                    intCntrIter += 1
                    time.sleep(5)
                    self.refresh_heatingpage()
                    time.sleep(5)
                    if self.wait_for_element_exist(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL):
                        self.report_pass('iOS-App: Successfully Heat mode is set to <B>' + strMode)
                    else:
                        self.report_fail('iOS-App: Unable to set Heat mode to <B>' + strMode)
                else:
                    self.report_fail("iOS-App: Control not active on the Heating Control Page to set the Heat Mode")

            except:
                self.report_fail('iOS-App: Exception in set_heat_mode Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set Target Temperature
    def set_target_temperature(self, fltTargetTemperature):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):
                    self.refresh_heatingpage()
                    time.sleep(3)
                    oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                    oScrolElementVAlue = oScrolElement.get_attribute('value')
                    if 'point' in oScrolElementVAlue:
                        fltCurrentTargTemp = float(
                            oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                    else:
                        fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltTargetTemperature) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltTargetTemperature, 0.5, 1)
                        oScrolElementVAlue = oScrolElement.get_attribute('value')
                        if 'point' in oScrolElementVAlue:
                            fltCurrentTargTemp = float(
                                oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                        else:
                            fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                        intCntrIter = +1
                    time.sleep(5)
                    self.refresh_heatingpage()

                    if fltCurrentTargTemp == fltTargetTemperature:
                        self.report_pass(
                            'iOS-App: The Target Temperature is successfully set to : ' + str(fltTargetTemperature))
                    else:
                        self.report_fail(
                            'iOS-App: Unable to set the Target Temperature to : ' + str(fltTargetTemperature))
                else:
                    self.report_fail(
                        "iOS-App: Control not active on the Heating Control Page to set the Target Temperature")

            except:
                self.report_fail('iOS-App: Exception in set_target_temperature Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Get Attributes for Heating Controls
    def get_heating_attribute(self):
        if self.reporter.ActionStatus:
            strMode = strRunningState = fltCurrentTargTemp = None
            try:
                self.refresh_heatingpage()
                if self.wait_for_element_exist(*HeatingControlPageLocators.SLIDER_DOTS):
                    strSelectedModeLabel = self.driver.find_element(
                        *HeatingControlPageLocators.SELECTED_MODE_LINK).text.upper()
                    print(strSelectedModeLabel)
                    if 'HEATING MODE SCHEDULE' in strSelectedModeLabel:
                        strMode = 'AUTO'
                    elif 'HEATING MODE MANUAL' in strSelectedModeLabel:
                        strMode = 'MANUAL'
                    elif 'HEATING MODE OFF' in strSelectedModeLabel:
                        strMode = 'OFF'
                elif self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_STOP):
                    strMode = 'BOOST'

                else:
                    self.report_fail(
                        "iOS-App : Control not active on the Heating Control Page to get Heating Attributes")

                oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                oScrolElementVAlue = oScrolElement.get_attribute('value')
                if 'point' in oScrolElementVAlue:
                    fltCurrentTargTemp = float(
                        oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                else:
                    fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                strFlameLabel = self.driver.find_element(*HeatingControlPageLocators.FLAME_ICON).get_attribute(
                    'label').upper()
                print(strFlameLabel)
                if 'ON' in strFlameLabel:
                    strRunningState = 'ON'
                elif 'OFF' in strFlameLabel:
                    strRunningState = 'OFF'

                self.report_done('iOS App : Screenshot while getting attributes')
                if strRunningState == 'OFF':
                    strRunningState = '0000'
                else:
                    strRunningState = '0001'
                if fltCurrentTargTemp == 7.0: fltCurrentTargTemp = 1.0
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('iOS App : NoSuchElementException: in get_heating_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Page Class for Heating Schedule page. Has all the methods for the Heating Schedule page
class HeatingSchedulePage(BasePage):
    # Reset Heating Schedule
    def resetHeatingSchedule(self, context):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON):
                    self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                    self._navigate_to_day(context.strDay)
                    time.sleep(3)
                    if self.is_element_present(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        if self.is_element_present(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU).click()
                            if self.is_element_present(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON):
                                self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON).click()
                                time.sleep(3)
                                self.report_pass('IOS App : Heating schedule was reset successfully')
                            else:
                                self.report_fail('IOS App : Heating schedule reset failed')

                        else:
                            self.report_fail('IOS App : Reset menu was not displayed')
                    else:
                        self.report_fail('IOS App : Schedule option button is not displayed')
                else:
                    self.report_fail('IOS App : Failed to find schedule button')
            except:
                self.report_fail('iOS App : NoSuchElementException: in resetHeatingSchedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set Heating Schedule
    def set_heating_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                    print('m here')
                    for oKey in oScheduleDict.keys():
                        self._navigate_to_day(oKey)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        self.add_or_remove_events(len(oScheduleList))
                        # Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.EVENT_ARROW)
                        for intCntr in range((len(lstStartTime) - 1), -1, -1):
                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetTargTemp = oScheduleList[intCntr][1]
                            if fltSetTargTemp == 1.0: fltSetTargTemp = 7.0
                            lstStartTime[intCntr].click()
                            self.report_done('iOS APP: Event number : ' + str(intCntr + 1) + ' before the event change')
                            print(fltSetTargTemp)
                            self.set_schedule_target_temperature(fltSetTargTemp)
                            self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                            self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                            self.report_done('iOS APP: Event number : ' + str(intCntr + 1) + ' after the event change')
                            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                            self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)
                            self.report_pass(
                                'iOS APP: Main Screen after Event number : ' + str(intCntr + 1) + ' is changed')
                        self.report_pass('iOS APP: Main Screen after all Events are changed')
                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Heating Schedule Page to set the Heating Schedule")
            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

                # Set the Even Target temperature

    def set_schedule_target_temperature(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.TITLE_LABEL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.EVENT_TARGET_TEMPERATURE_SCROLL)
                    oScrolElementVAlue = oScrolElement.get_attribute('value')

                    if 'point' in oScrolElementVAlue:
                        fltCurrentTargTemp = float(
                            oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                    else:
                        fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):
                        # self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 1)
                        self.scroll_to_set_temp(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 60)
                        oScrolElementVAlue = oScrolElement.get_attribute('value')
                        if 'point' in oScrolElementVAlue:
                            fltCurrentTargTemp = float(
                                oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                        else:
                            fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                        intCntrIter = +1
                        print(fltCurrentTargTemp, fltSetTargTemp)
                    if fltCurrentTargTemp == fltSetTargTemp:
                        self.report_pass(
                            'iOS APP: The Target Temperature is successfully set to : ' + str(fltSetTargTemp))
                    else:
                        self.report_fail('iOS APP: Unable to set the Target Temperature to : ' + str(fltSetTargTemp))
                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Edit Time Slot for Heating schedule Page to set the Event Target Temperature")
            except:
                self.report_fail('iOS APP: Exception in set_schedule_target_temperature Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Page Class for Heating Control page. Has all the methods for the Heating Control page
class HotWaterControlPage(BasePage):
    # Set Heat mode
    def set_hot_water_mode(self, strMode, intDuration=1):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HotWaterControlPageLocators.BOOST_MODE_LINK):
                    self.refresh_page()
                    time.sleep(5)
                    print('im here 1')
                    if strMode.upper() == 'AUTO':
                        self.driver.find_element(*HotWaterControlPageLocators.SCHEDULE_MODE_LINK).click()
                    elif strMode.upper() == 'MANUAL':
                        self.driver.find_element(*HotWaterControlPageLocators.MANUAL_MODE_LINK).click()
                    elif strMode.upper() == 'OFF':
                        self.driver.find_element(*HotWaterControlPageLocators.OFF_MODE_LINK).click()
                    elif strMode.upper() == 'BOOST':
                        self.driver.find_element(*HotWaterControlPageLocators.BOOST_MODE_LINK).click()
                        print('intDuration', intDuration)
                        if self.currentAppVersion == 'V6':
                            # Set Boost Duration
                            if intDuration != 1:

                                intCurrentDuration = int(self.driver.find_element(
                                    *HotWaterControlPageLocators.BOOST_TIME_SCROLL).get_attribute('value').split(' ')[
                                                             0])
                                print('intCurrentDuration', intCurrentDuration)
                                print('intDuration', intDuration)
                                intCntrIter = 0
                                while (intCurrentDuration != intDuration) and (intCntrIter < 3):
                                    time.sleep(2)
                                    self.set_boost_time_duration(intDuration)
                                    intCurrentDuration = int(self.driver.find_element(
                                        *HotWaterControlPageLocators.BOOST_TIME_SCROLL).get_attribute('value').split(
                                        ' ')[0])
                                    intCntrIter += 1
                    time.sleep(5)
                    self.refresh_page()
                    time.sleep(5)
                    intCurrentDuration = 1
                    if intCurrentDuration == intDuration:
                        self.report_pass('Android-App : Successfully Hot Water mode is set to <B>' + strMode)
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
            strMode = strRunningState = fltCurrentTargTemp = None
            try:
                self.refresh_page()
                if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_MODE_LINK):
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    print(strScreenName)
                    if 'HOT WATER BOOST' in strScreenName.upper():
                        strMode = 'BOOST'
                        if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON):
                            strRunningState = 'ON'
                        else:
                            strRunningState = 'OFF'
                    else:
                        strSelectedModeLabel = self.driver.find_element(
                            *HotWaterControlPageLocators.SELECTED_MODE_LINK).text.upper()
                        print(strSelectedModeLabel)
                        if 'HOT WATER MODE SCHEDULE' in strSelectedModeLabel:
                            strMode = 'AUTO'
                            if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON):
                                strRunningState = 'ON'
                            else:
                                strRunningState = 'OFF'
                        elif 'HOT WATER MODE ON' in strSelectedModeLabel:
                            strMode = 'Always ON'
                            if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON):
                                strRunningState = 'ON'
                            else:
                                strRunningState = 'OFF'
                        elif 'HOT WATER MODE OFF' in strSelectedModeLabel:
                            strMode = 'Always OFF'
                            if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_OFF):
                                strRunningState = 'OFF'
                            else:
                                strRunningState = 'ON'
                else:
                    self.report_fail(
                        "iOS-App : Control not active on the Hot Water Control Page to get Heating Attributes")

                self.report_done('iOS App : Screenshot while getting attributes')
                if strRunningState == 'OFF':
                    strRunningState = '0000'
                else:
                    strRunningState = '0001'
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('iOS App : NoSuchElementException: in get_hotwater_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Page Class for Hot Water Schedule page. Has all the methods for the Hot Water Schedule page
class HotWaterSchedulePage(BasePage):
    def resetHotWaterSchedule(self, context):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON):
                    self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                    self._navigate_to_day(context.strDay)
                    time.sleep(3)
                    if self.is_element_present(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        if self.is_element_present(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU).click()
                            if self.is_element_present(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON):
                                self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON).click()
                                time.sleep(3)
                                self.report_pass('IOS App : Hot water schedule was reset successfully')
                            else:
                                self.report_fail('IOS App : Hot water schedule reset failed')

                        else:
                            self.report_fail('IOS App : Reset menu was not displayed')
                    else:
                        self.report_fail('IOS App : Schedule option button is not displayed')
                else:
                    self.report_fail('IOS App : Failed to find schedule button')
            except:
                self.report_fail('iOS App : NoSuchElementException: in resetHotWaterSchedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set Hot Water Schedule
    def set_hot_water_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                    print('m here')
                    for oKey in oScheduleDict.keys():
                        self._navigate_to_day(oKey)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        self.add_or_remove_events(len(oScheduleList))
                        # Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.EVENT_ARROW)
                        for intCntr in range((len(lstStartTime) - 1), -1, -1):
                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetTargTemp = oScheduleList[intCntr][1]
                            if fltSetTargTemp == 1.0: fltSetTargTemp = 7.0
                            lstStartTime[intCntr].click()
                            self.report_done('iOS APP: Event number : ' + str(intCntr + 1) + ' before the event change')
                            print(self.driver.find_element(
                                *EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).get_attribute('name').upper())
                            # input(prompt)
                            if self.driver.find_element(
                                    *EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).get_attribute(
                                'name').upper().find('ON') >= 0:
                                strCurrentState = 'ON'
                            else:
                                strCurrentState = 'OFF'

                            if (fltSetTargTemp == 99.0 and strCurrentState == 'OFF') or (
                                            fltSetTargTemp == 0.0 and strCurrentState == 'ON'):
                                print('Clicking Toggle')
                                self.driver.find_element(*EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).click()

                            self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                            self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                            self.report_done('iOS APP: Event number : ' + str(intCntr + 1) + ' after the event change')
                            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                            self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)
                            self.report_pass(
                                'iOS APP: Main Screen after Event number : ' + str(intCntr + 1) + ' is changed')
                        self.report_pass('iOS APP: Main Screen after all Events are changed')
                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Heating Schedule Page to set the Heating Schedule")

            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


# Page Class for Plug Schedule page. Has all the methods for the Plug Schedule page
class PlugSchedulePage(BasePage):
    def edit_plug_schedule(self, strSlotDetails, intSlotPosition):
        if self.reporter.ActionStatus:
            try:
                if intSlotPosition == 0:
                    self.driver.find_element(*SchedulePageLocators.SLOT_ONE).click()
                elif intSlotPosition == 1:
                    self.driver.find_element(*SchedulePageLocators.SLOT_TWO).click()
                elif intSlotPosition == 2:
                    self.driver.find_element(*SchedulePageLocators.SLOT_THREE).click()
                elif intSlotPosition == 3:
                    self.driver.find_element(*SchedulePageLocators.SLOT_FOUR).click()
                elif intSlotPosition == 4:
                    self.driver.find_element(*SchedulePageLocators.SLOT_FIVE).click()
                elif intSlotPosition == 5:
                    self.driver.find_element(*SchedulePageLocators.SLOT_SIX).click()

                if 'OFF' in strSlotDetails:
                    if self.is_element_present(*EditTimeSlotPageLocators.PLUG_STATE_ON):
                        self.driver.find_element(*EditTimeSlotPageLocators.PLUG_TOGGLE_BUTTON).click()
                elif 'ON' in strSlotDetails:
                    if self.is_element_present(*EditTimeSlotPageLocators.PLUG_STATE_OFF):
                        self.driver.find_element(*EditTimeSlotPageLocators.PLUG_TOGGLE_BUTTON).click()

                strSlotTime = strSlotDetails[0]

                hourToSet = strSlotTime[:2]
                minToSet = strSlotTime[3:]
                self.set_schedule_event_hour(hourToSet)
                self.set_schedule_event_minute(minToSet)
                if self.is_element_present(*EditTimeSlotPageLocators.SAVE_BUTTON):
                    self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                    time.sleep(3)
                else:
                    self.report_fail('Slot update failed')
            except:
                self.report_fail('iOS APP: Exception in edit_plug_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set Hot Water Schedule
    def set_plug_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                    print('m here')
                    for oKey in oScheduleDict.keys():
                        self._navigate_to_day(oKey)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        self.add_or_remove_events(len(oScheduleList))
                        for intCntr in range((len(oScheduleList) - 1), -1, -1):
                            self.edit_plug_schedule(oScheduleList[intCntr], intCntr)
                        self.report_pass('iOS APP: Main Screen after all Events are changed')
                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Plug Schedule Page to set the Plug Schedule")

            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_plug_mode(self, strMode):
        blnFlag = False
        if self.reporter.ActionStatus:
            try:
                oDeviceMode = ""
                if self.is_element_present(*DashboardPageLocators.TAB_BAR_CONTROL_BUTTON):
                    self.driver.find_element(*DashboardPageLocators.TAB_BAR_CONTROL_BUTTON).click()
                    if strMode == "AUTO":
                        if self.is_element_present(*PlugLocators.PLUG_MODE_MANUAL):
                            oDeviceMode = self.driver.find_element(*PlugLocators.PLUG_MODE_MANUAL)
                    else:
                        if self.is_element_present(*PlugLocators.PLUG_MODE_SCHEDULE):
                            oDeviceMode = self.driver.find_element(*PlugLocators.PLUG_MODE_SCHEDULE)

                    if oDeviceMode != "":

                        intLeftX = oDeviceMode.location['x']
                        intUpperY = oDeviceMode.location['y']
                        intWidth = oDeviceMode.size['height']
                        intMid = intWidth / 2
                        intCenterX = intLeftX + 25
                        intCenterY = intUpperY + intMid
                        print("Arrow co-ordinates are : ", intCenterX, intCenterY)
                        positions = [(intCenterX, intCenterY)]
                        self.driver.tap(positions)
                        time.sleep(5)
                        blnFlag = True

                        if blnFlag:
                            self.report_pass('iOS-App : Successfully Plug Mode is set to <B>' + strMode)
                        else:
                            self.report_fail('iOS App : Unable to set Plug Mode to <B>' + strMode)
                    else:
                        self.report_done('IOS App : Plug is already in the expected mode')
            except:
                self.report_fail('iOS App : NoSuchElementException: in set_plug_mode Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def resetPlugSchedule(self, context):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON):
                    self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                    self._navigate_to_day(context.strDay)
                    time.sleep(3)
                    if self.is_element_present(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        if self.is_element_present(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU).click()
                            if self.is_element_present(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON):
                                self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON).click()
                                time.sleep(3)
                                self.report_pass('IOS App : Plug schedule was reset successfully')
                            else:
                                self.report_fail('IOS App : Plug schedule reset failed')

                        else:
                            self.report_fail('IOS App : Reset menu was not displayed')
                    else:
                        self.report_fail('IOS App : Schedule option button is not displayed')
                else:
                    self.report_fail('IOS App : Failed to find schedule button')
            except:
                self.report_fail('iOS App : NoSuchElementException: in resetPlugSchedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def delete_schedule(self, context):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON):
                    self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                    slotTime = context.addSlotTime
                    slot_Time = str(SchedulePageLocators.SELECT_SLOT)
                    self._navigate_to_day(context.strDay)
                    time.sleep(3)
                    if ':00' in slotTime:
                        slotHour = slotTime[:2]
                        slotMin = ', hundred,  , until'
                        slotTimeCombined = slotHour + slotMin
                        slotObject = slot_Time.replace("strSlotTime", slotTimeCombined)
                    else:
                        slotTimeCombined = slotTime + ' , until'
                        slotObject = slot_Time.replace("strSlotTime", slotTimeCombined)

                    if self.is_element_present(By.XPATH, slotObject):
                        self.driver.find_element(By.XPATH, slotObject).click()
                        if self.is_element_present(*SchedulePageLocators.DELETE_TIME_SLOT):
                            self.driver.find_element(*SchedulePageLocators.DELETE_TIME_SLOT).click()
                            if self.is_element_present(*SchedulePageLocators.DELETE_TIME_SLOT_POPUP):
                                self.driver.find_element(*SchedulePageLocators.DELETE_TIME_SLOT_POPUP).click()
                                time.sleep(3)
                                self.report_pass('IOS App : Slot deleted successfully')
                            else:
                                self.report_fail('IOS App : Delete confirmation pop up was not displayed')
                        else:
                            self.report_fail('IOS App : Delete option was not displayed')
                    else:
                        self.report_fail('IOS App : Time slot was not displayed')
                else:
                    self.report_fail('IOS App : Failed to find schedule button')
            except:
                self.report_fail('iOS App : NoSuchElementException: in resetPlugSchedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def addschedule(self, context):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON):
                    self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                    self._navigate_to_day(context.strDay)
                    time.sleep(3)
                    if self.is_element_present(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        if self.is_element_present(*SchedulePageLocators.ALL_SLOTS_FILLED):
                            self.report_fail('IOS App : All slots are filled no additional slots can be added')
                        elif self.is_element_present(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU).click()
                            strSlotTime = context.addSlotTime
                            strSlotState = context.addSlotState
                            if strSlotState.upper() == 'OFF':
                                if self.is_element_present(*EditTimeSlotPageLocators.PLUG_TOGGLE_BUTTON):
                                    self.driver.find_element(*EditTimeSlotPageLocators.PLUG_TOGGLE_BUTTON).click()
                                    hourToSet = strSlotTime[:2]
                                    minToSet = strSlotTime[3:]
                                    self.set_schedule_event_hour(hourToSet)
                                    self.set_schedule_event_minute(minToSet)
                                    if self.is_element_present(*EditTimeSlotPageLocators.SAVE_BUTTON):
                                        self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                                        time.sleep(3)
                                        self.report_pass('IOS App : Slot added successfully.')
                                    else:
                                        self.report_fail('IOS App : New slot addition failed.')
                        else:
                            self.report_fail('IOS App : Add slot menu was not displayed')
                    else:
                        self.report_fail('IOS App : Schedule option button is not displayed')

                else:
                    self.report_fail('IOS App : Failed to find schedule button')
            except:
                self.report_fail('iOS App : NoSuchElementException: in resetPlugSchedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class SetChangePassword(BasePage):
    def change_password_screen(self):
        if self.reporter.ActionStatus:
            try:
                strPassword = utils.getAttribute('common', 'password')
                if self.wait_for_element_exist(*ChangePasswordLocators.OLDPASSWORD_EDTBOX):
                    self.driver.find_element(*ChangePasswordLocators.OLDPASSWORD_EDTBOX).send_keys(strPassword)
                    self.report_pass('iOS APP: Change Password Screen: Old password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password Screen: Old password is entered successfully')

                if self.wait_for_element_exist(*ChangePasswordLocators.NEWPASSWORD_EDTBOX):
                    self.driver.find_element(*ChangePasswordLocators.NEWPASSWORD_EDTBOX).send_keys('Password1' + "a")
                    self.report_pass('iOS APP: Change Password Screen: New password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password Screen: New password is entered successfully')

                if self.wait_for_element_exist(*ChangePasswordLocators.RETYPEPASSWORD_EDTBOX):
                    self.driver.find_element(*ChangePasswordLocators.RETYPEPASSWORD_EDTBOX).send_keys('Password1' + "a")
                    self.report_pass('iOS APP: Change Password Screen: Retype password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password Screen: Retype password is entered successfully')

                if self.wait_for_element_exist(*ChangePasswordLocators.SAVE_BUTTON):
                    self.driver.find_element(*ChangePasswordLocators.SAVE_BUTTON).click()
                    self.report_pass('iOS APP: Change Password Screen:  Password is set successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password Screen: Password is not set ,Save button is not clicked')


            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_change_password(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.report_pass('iOS APP: Change Password : Navigated to Menu Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password : Menu is not selected Successfully')

                self.driver.swipe(287, 477, 285, 140, 500)

                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass('iOS APP: Navigated to Settings Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password : Settings is selected Successfully')

                print('settings clicked')

                if self.wait_for_element_exist(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU):
                    self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU).click()
                    self.report_pass('iOS APP: Navigated to Change Password screen Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password : is not selected Successfully')


            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def login_change_password(self):
        if self.reporter.ActionStatus:
            try:
                strUserName = utils.getAttribute('common', 'userName')
                strPassword = utils.getAttribute('common', 'password')

                if self.wait_for_element_exist(*LoginPageLocators.TITLE_LABEL):
                    self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).set_value(strUserName)
                    self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys('Password1' + "a")
                    self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                if self.driver.find_element(*HomePageLocators.MENU_BUTTON):
                    self.report_pass('iOS-App: The Hive iOS App is successfully Logged in with the Changed Password')
                else:
                    self.report_fail(
                        'iOS-App: The Hive iOS App is not logged in. Please check the Login credentials and re-execute test.')

                    # else:
                # self.report_fail('The Hive App is either not Launched or the Login screen is not displayed. Please check and re-execute test.')

                self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                self.driver.swipe(287, 477, 285, 140, 500)
                self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU).click()
                self.driver.find_element(*ChangePasswordLocators.OLDPASSWORD_EDTBOX).send_keys('Password1' + "a")
                self.driver.find_element(*ChangePasswordLocators.NEWPASSWORD_EDTBOX).send_keys(strPassword)
                self.driver.find_element(*ChangePasswordLocators.RETYPEPASSWORD_EDTBOX).send_keys(strPassword)
                self.driver.find_element(*ChangePasswordLocators.SAVE_BUTTON).click()

            except:
                self.report_fail('iOS-App: Exception in login_hive_app Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class SaveHeatingNotification(BasePage):
    def naivgate_to_ZoneNotificaiton(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.report_pass('iOS APP :  Hive user is able access Menu successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: What went wrong -> Opps! Hive user is not able to access Menu')

                self.driver.swipe(287, 477, 285, 140, 500)

                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass('iOS APP: Hive user is able to access sub menu item Settings successfully')
                    time.sleep(2)
                else:
                    self.report_fail(
                        'iOS APP: What went wrong -> Opps! Hive user is not able to access sub menu Setting')

                if self.wait_for_element_exist(*HeatingNotification.SUB_MENU_HEATING_NOTIFICATION):
                    self.driver.find_element(*HeatingNotification.SUB_MENU_HEATING_NOTIFICATION).click()
                    self.report_pass(
                        'iOS APP: Hive user is able to navigate to Heating Notification screen successfully')
                    time.sleep(2)
                else:
                    self.report_fail(
                        'iOS APP: What went wrong -> Hive user is not able to navigate to Heating Notifications screen')

            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def setHighTemperature(self, oTargetHighTemp):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotification.MAX_TEMPRATURE_NOTSET):
                    self.driver.find_element(*HeatingNotification.MAX_TEMPRATURE).click()
                    self.report_pass(
                        'iOS APP: Hive user is able to navigate to Maximum temperature screen successfully')
                    time.sleep(2)
                    if self.driver.find_element(*HeatingNotification.EMAIL_ME_OFF):
                        self.driver.find_element(*HeatingNotification.EMAIL_ME).click()
                        time.sleep(3)
                        self.set_target_Heating_notification_temperature(oTargetHighTemp)
                        time.sleep(3)
                        self.driver.find_element(*HeatingNotification.SAVE_CHANGES).click()
                    else:
                        self.driver.find_element(*HeatingNotification.BTN_BACK)
                else:
                    self.report_pass('iOS APP: Hive user had already set the Maximum Temperature')

            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def setLowTemperature(self, oTargetLowTemp):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotification.MIN_TEMPRATURE_NOTSET):
                    self.driver.find_element(*HeatingNotification.MIN_TEMPRATURE).click()
                    self.report_pass(
                        'iOS APP: Hive user is able to navigate to Minimum temperature screen successfully')
                    time.sleep(2)
                    if self.driver.find_element(*HeatingNotification.EMAIL_ME_OFF):
                        self.driver.find_element(*HeatingNotification.EMAIL_ME).click()
                        time.sleep(3)
                        self.set_target_Heating_notification_temperature(oTargetLowTemp)
                        self.driver.find_element(*HeatingNotification.SAVE_CHANGES).click()
                    else:
                        self.driver.find_element(*HeatingNotification.BTN_BACK)
                else:
                    self.report_pass('iOS APP: Hive user had already set the Minimum Temperature')

            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def receiveWarnings(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotification.RECEIVE_WARNINGS_OFF):
                    self.driver.find_element(*HeatingNotification.RECEIVE_WARNINGS).click()
                    self.report_pass('iOS APP: Hive user enabled the Receive Warnings')
                else:
                    self.report_pass('iOS APP: Hive user had already enabled Receive Warnings')

            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_target_Heating_notification_temperature(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try:
                oScrolElement = self.driver.find_element(*HeatingNotification.TARGET_TEMPERATURE_SCROLL_HN)
                oScrolElementVAlue = oScrolElement.get_attribute('value')
                if 'point' in oScrolElementVAlue:
                    fltCurrentTargTemp = float(
                        oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                else:
                    fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                intCntrIter = 1
                while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):
                    self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 1)
                    oScrolElementVAlue = oScrolElement.get_attribute('value')
                    if 'point' in oScrolElementVAlue:
                        fltCurrentTargTemp = float(
                            oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                    else:
                        fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                    intCntrIter = +1
                    print(fltCurrentTargTemp, fltSetTargTemp)
                if fltCurrentTargTemp == fltSetTargTemp:
                    self.report_pass('iOS APP: The Target Temperature is successfully set to : ' + str(fltSetTargTemp))
                else:
                    self.report_fail('iOS APP: Unable to set the Target Temperature to : ' + str(fltSetTargTemp))
            except:
                self.report_fail('iOS APP: Exception in set_schedule_target_temperature Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def setNotificationONtoOFF(self, strNotiState):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingNotification.MAX_TEMPRATURE):
                    self.driver.find_element(*HeatingNotification.MAX_TEMPRATURE).click()
                    self.report_pass(
                        'iOS APP: Hive user is able to navigate to Maximum temperature screen successfully')
                    time.sleep(2)
                    if strNotiState == 'OFF':
                        self.driver.find_element(*HeatingNotification.EMAIL_ME).click()
                        time.sleep(2)
                        self.driver.find_element(*HeatingNotification.SAVE_CHANGES).click()
                        self.report_pass('iOS APP: Hive user turn off the Maximum Temperature')
                    else:
                        self.driver.find_element(*HeatingNotification.BTN_BACK)
                if self.wait_for_element_exist(*HeatingNotification.MIN_TEMPRATURE):
                    self.driver.find_element(*HeatingNotification.MIN_TEMPRATURE).click()
                    self.report_pass(
                        'iOS APP: Hive user is able to navigate to Maximum temperature screen successfully')
                    time.sleep(2)
                    if strNotiState == 'OFF':
                        self.driver.find_element(*HeatingNotification.EMAIL_ME).click()
                        time.sleep(2)
                        self.driver.find_element(*HeatingNotification.SAVE_CHANGES).click()
                        self.report_pass('iOS APP: Hive user turn off the Minimum Temperature')
                        time.sleep(2)
                        self.driver.find_element(*HeatingNotification.RECEIVE_WARNINGS).click()
                        self.report_pass('iOS APP: Hive user turn off the Heating Notification')
                else:
                    self.report_pass('iOS APP: Hive user had already set the Maximum Temperature')

            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class SetPinLock(BasePage):
    def navigate_to_pin_lock(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.report_pass('iOS APP: Pin Lock : Navigated to Menu Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin Lock : Menu is not selected Successfully')

                self.driver.swipe(287, 477, 285, 140, 500)

                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass('iOS APP: Navigated to Settings Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin Lock : Settings is selected Successfully')

                print('settings clicked')

                if self.wait_for_element_exist(*HomePageLocators.PINLOCK_SUB_MENU):
                    self.driver.find_element(*HomePageLocators.PINLOCK_SUB_MENU).click()
                    self.report_pass('iOS APP: Navigated to Pin Lock screen Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin Lock: is not selected Successfully')


            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_pinlock(self):

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.CURRENT_TITLE):
                    strScreenName = self.wait_for_element_exist(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    print(strScreenName)
                    if 'PIN LOCK' in strScreenName.upper():
                        self.report_pass('iOS APP: Navigated to Set Pin Lock screen Successfully')
                    else:
                        self.report_pass('iOS APP: Navigated to Set Pin Lock screen is not Successfull')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin Lock Screen is not selected Successfully')

                if self.wait_for_element_exist(*PinLockPageLocators.PINLOCK_SETPIN):
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_SETPIN).click()
                    self.report_pass('iOS APP: Pin lock set pin is selected screen Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin lock set pin is not selected screen Successfully')

                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_TWO).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_THREE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_FOUR).click()
                    time.sleep(3)
                    self.report_pass('iOS APP: Enter new pin is selected success')
                else:
                    self.report_fail('iOS APP: Enter new pin is not successfully entered')

                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_TWO).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_THREE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_FOUR).click()
                    time.sleep(2)
                    self.report_pass('iOS APP: Re Enter  pin is selected success')
                else:
                    self.report_fail('iOS APP: Re Enter new pin is not successfully entered')

            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def validate_pin(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLockPageLocators.PINSET_ON):
                    strPinLock = self.wait_for_element_exist(*PinLockPageLocators.PINSET_ON).get_attribute('name')
                    if 'PIN LOCK' in strPinLock.upper():
                        self.report_pass('iOS APP: Pin lock is set successfully')
                    else:
                        self.report_fail('iOS APP: Pin lock is not set successfully')
                else:
                    self.report_fail('iOS APP:Pin lock is not set successfully')
            except:
                self.report_fail('iOS-App: Exception in login_hive_app Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def change_pin(self):

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLockPageLocators.PINLOCK_CHANGEPIN):
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_CHANGEPIN).click()
                    self.report_pass('iOS APP: Change Pin Screen is entered successfully')
                else:
                    self.report_fail('iOS APP: Change Pin Screen is not entered successfully')

                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_TWO).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_THREE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_FOUR).click()
                    time.sleep(3)
                    self.report_pass('iOS APP: Old Pin is entered success')
                else:
                    self.report_fail('iOS APP: Enter new pin is not entered entered')

                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.report_pass('iOS APP: Entered new  pin is success')
                else:
                    self.report_fail('iOS APP: Entered new  pin is not success')

                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.report_pass('iOS APP: Re Enter new pin is success')
                else:
                    self.report_fail('iOS APP: Re Enter new pin is not success')

            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def forgot_pin_lock(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLockPageLocators.PINLOCK_FORGOTPIN):
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_FORGOTPIN).click()
                    self.report_pass('iOS APP: Forgot Pin is selected Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Forgot Pin is not selected Successfully')

            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def forgot_validate_pin(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLockPageLocators.PINLOCK_LOGOUT):
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_LOGOUT).click()
                    self.report_pass('iOS APP: Logout is selected Successfully')
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_LOGOUT_OK).click()
                else:
                    self.report_fail('iOS APP: Forgot Pin is not done Successfully')

            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class TextControl(BasePage):
    def navigate_to_TextControl_page(self):

        if self.reporter.ActionStatus:
            try:
                strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                print(strScreenName)
                self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                time.sleep(2)

                if self.driver.find_element(*HomePageLocators.HELP_SUPPORT_LINK).is_displayed():
                    self.driver.find_element(*HomePageLocators.HELP_SUPPORT_LINK).click()
                    time.sleep(2)
                    self.driver.find_element(*HomePageLocators.TEXT_CONTROL_LINK).click()
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    print(strScreenName)
                    strUserCount = self.driver.find_element(*TextControlLocators.USER_TABLE).text
                    intRowCount = int(strUserCount[(len(strUserCount) - 1)]) - 1
                    print(intRowCount)
                else:
                    self.driver.swipe(340, 571, 344, 100, 2000)
                    self.driver.find_element(*HomePageLocators.HELP_SUPPORT_LINK).click()
                    self.driver.find_element(*HomePageLocators.TEXT_CONTROL_LINK).click()
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    print(strScreenName)
                if strScreenName == "Text control, screen":
                    self.report_pass("iOS APP :Successfully navigated to Text Control Page")
                else:
                    self.report.fail("iOS APP :Not able to navigate to Text Control Page")

            except:
                self.report_fail('iOS App : NoSuchElementException: in navigate_to_TextControl_page\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def textControlOptions(self, context):
        print("Adding user")
        if self.reporter.ActionStatus:

            strUserCount = self.driver.find_element(*TextControlLocators.USER_TABLE).text
            intRowCount = int(strUserCount[(len(strUserCount) - 1)])
            print(intRowCount)
            if intRowCount <= 6:
                print(intRowCount)
                for oRow in context.table:
                    strusername = oRow['UserName']
                    strMobileNo = oRow['MobileNo']
                    print(strusername, strMobileNo)
                    try:
                        if self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed():
                            self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).click()
                            self.report_done(
                                "iOS App: Adding new user :   " + str(intRowCount) + "  " + "for Text Control Options")
                            self.driver.find_element(*TextControlLocators.NAME_EDTBOX).send_keys(strusername)
                            self.driver.find_element(*TextControlLocators.MOBILE_EDTBOX).send_keys(strMobileNo)
                            self.driver.find_element(*TextControlLocators.SAVE_BUTTON).click()
                            time.sleep(5)
                            try:
                                if self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed():
                                    self.report.done("iOS App:More users can be added for Text Control options")
                                    print(intRowCount)
                                else:
                                    self.driver.find_element(*TextControlLocators.SAVE_BUTTON).is_displayed()
                                    self.report_fail("iOS App:This number is already registered to a Hive Account")
                            except:
                                self.report_pass("iOS App:User added to Text Control successfully")
                            intRowCount = intRowCount + 1

                    except:
                        self.report_fail("iOS App:Maximum user limit reached in TextControl Options")
            else:
                self.report_fail("iOS App:Maximum user limit reached in TextControl Options")

    def textControlValidation(self, context):
        if self.reporter.ActionStatus:
            try:
                strUserCount = self.driver.find_element(*TextControlLocators.USER_TABLE).text
                intRowCount = int(strUserCount[(len(strUserCount) - 1)])
                try:
                    if intRowCount == 6 and self.driver.find_element(
                            *TextControlLocators.ADD_NEW_USER_LINK).is_displayed() == False:
                        self.report_done("iOS App:More users can be added in TextControl Page")
                except:
                    intRowCount = intRowCount + 1
                    self.report_done("iOS App: Adding New user" + str(intRowCount) + "for Text Control Options")
                    self.report_pass("iOS App:Text Control Options reached Maximum user limits")
                else:
                    self.report_done("iOS App:More users can be added in TextControl Page")
            except:
                self.report_fail('iOS App : NoSuchElementException: in textControlValidation\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class HolidayMode(BasePage):
    def navigateToHeatingRecipes(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HolidayModePageLocators.HEATING_CELL):
                    self.driver.find_element(*HolidayModePageLocators.HEATING_CELL).click()
                    if self.wait_for_element_exist(*HolidayModePageLocators.HEATING_RECIPE_CONTROL):
                        self.driver.find_element(*HolidayModePageLocators.HEATING_RECIPE_CONTROL).click()
                    else:
                        self.report_fail('iOS App : Couldn\'t navigate to Heating recipes')
                else:
                    self.report_fail('iOS App : Couldn\'t find Heating on dashboard')
            except:
                self.report_fail('iOS App : Exception: in navigateToHeatingRecipes\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def disableHeatingRecipes(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HolidayModePageLocators.HEATING_RECIPE_SWITCHES):
                    lstRecipes = self.driver.find_elements(*HolidayModePageLocators.HEATING_RECIPE_SWITCHES)
                    intCount = len(lstRecipes)
                    intCntr = 0
                    while intCntr < intCount:
                        currentState = lstRecipes[intCntr].get_attribute('value')
                        if currentState == 1:
                            lstRecipes[intCntr].click()
                        intCntr = intCntr + 1
                    time.sleep(2)
                    if intCntr == intCount:
                        self.report_pass('iOS App : Disabled the Heating recipes')
                else:
                    self.report_done('iOS App : There are no recipes to disable')
            except:
                self.report_fail('iOS App : Exception: in disableHeatingRecipes\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def enableEditHolidayMode(self):
        try:
            if self.wait_for_element_exist(*HolidayModePageLocators.EDIT_HOLIDAYMODE_BUTTON):
                self.driver.find_element(*HolidayModePageLocators.EDIT_HOLIDAYMODE_BUTTON).click()
                time.sleep(2)
                if self.wait_for_element_exist(*HolidayModePageLocators.EDIT_HOLIDAYMODE_TEXT):
                    self.report_done('iOS App : Navigate to Edit Holiday Mode')
                else:
                    self.report_fail('iOS App : Couldn\'t navigate to Edit Holiday Mode')
            else:
                self.report_fail('iOS App : Couldn\'t Edit Holiday Mode')

        except:
            self.report_fail('iOS App : Exception: in editHolidayStartEndDates\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def navigate_To_HolidayScreen(self, context, actionType, holidayModeType):
        if self.reporter.ActionStatus:
            try:
                if "ACTIVATE" in actionType.upper():
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Disable Heating Recipes')
                    self.navigateToHeatingRecipes()
                    self.disableHeatingRecipes()
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Navigate to Holiday Mode screen')
                    if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                        strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute(
                            'name')
                        self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                        if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MENU_LINK):
                            self.driver.find_element(*HomePageLocators.SETTINGS_MENU_LINK).click()
                            time.sleep(2)
                            if self.wait_for_element_exist(*HomePageLocators.HOLIDAY_MODE_MENU_LINK):
                                self.driver.find_element(*HomePageLocators.HOLIDAY_MODE_MENU_LINK).click()
                                strScreenName = self.driver.find_element(
                                    *HomePageLocators.CURRENT_TITLE).get_attribute(
                                    'name')

                            if strScreenName == "Holiday mode, screen":
                                self.report_done("iOS App : User successfully navigated to Holiday Mode screen")
                            else:
                                self.report_fail("iOS App : Navigation to Holiday Mode Screen failed")

                if "EDIT" in actionType.upper():
                    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Edit Holiday Mode')
                    self.enableEditHolidayMode()

                time.sleep(4)
            except:
                self.report_fail('iOS App : Exception: in navigate_To_HolidayScreen\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def activateHolidayMode(self, context):
        try:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Activate Holiday Mode')
            if self.wait_for_element_exist(*HolidayModePageLocators.ACTIVATE_HOLIDAYMODE_BUTTON):
                self.driver.find_element(*HolidayModePageLocators.ACTIVATE_HOLIDAYMODE_BUTTON).click()
                time.sleep(3)
                if self.wait_for_element_exist(*HolidayModePageLocators.CANCEL_HOLIDAYMODE_BUTTON):
                    self.report_pass('iOS App : Activated Holiday Mode')
                else:
                    self.report_fail('iOS App : Couldn\'t activate Holiday Mode')
            else:
                self.report_fail('iOS App : Activate Holiday Mode control couldn\'t be found')
        except:
            self.report_fail('iOS App : Exception: in activateHolidayMode method \n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Set the Holiday Target temperature
    def set_holiday_target_temperature(self, context, targetTemp):
        if self.reporter.ActionStatus:
            try:
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set target temperature')
                if self.wait_for_element_exist(*HolidayModePageLocators.TEMP_PICKER):
                    oScrolElement = self.driver.find_element(*HolidayModePageLocators.TEMP_PICKER)
                    oScrolElementValue = oScrolElement.get_attribute('value')
                    fltSetTargTemp = float(targetTemp)
                    if 'point' in oScrolElementValue:
                        fltCurrentTargTemp = float(
                            oScrolElementValue.split(' ')[0] + '.' + oScrolElementValue.split(' ')[2])
                    else:
                        fltCurrentTargTemp = float(oScrolElementValue.split(' ')[0])
                        if not fltCurrentTargTemp == fltSetTargTemp:
                            status = self.scroll_to_set_temp(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 60)
                            if not status:
                                self.report_fail(
                                    'iOS APP: Unable to set the Target Temperature to : ' + str(fltSetTargTemp))
                else:
                    self.report_fail(
                        "iOS APP: Control not active to set the Holiday Target Temperature")
            except:
                self.report_fail('iOS APP: Exception in set_holiday_target_temperature Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def setHolidayStartEndDate(self, daysFromNow, duration):
        try:
            daysFromNow = int(daysFromNow)
            duration = int(duration)
            modTime = (datetime.now() + timedelta(days=daysFromNow, hours=0, minutes=30))

            'Setting Departure date-time for Holiday Mode'
            strStartHoliday = (modTime.strftime("%c"))
            if "  " in strStartHoliday:  # To replace the additional space due to single digit date
                strStartHoliday = strStartHoliday.replace("  ", " ")
            intDDate = (strStartHoliday.split(' ')[0]) + ' ' + (strStartHoliday.split(' ')[2]) + ' ' + (
                strStartHoliday.split(' ')[1])
            strDTime = (strStartHoliday.split(' ')[3])
            intDSetHour = (strDTime.split(':')[0])
            intDSetMin = (strDTime.split(':')[1])
            if self.wait_for_element_exist(*HolidayModePageLocators.SET_DEPARTURE):
                self.driver.find_element(*HolidayModePageLocators.SET_DEPARTURE).click()

                # Setting Day in Holiday mode
                if self.wait_for_element_exist(*HolidayModePageLocators.DDAY_PICKER):
                    dDayPicker = self.driver.find_element(*HolidayModePageLocators.DDAY_PICKER)
                    currentDDay = dDayPicker.get_attribute('value')
                    self.scroll_Date_Hour_Minute(dDayPicker, currentDDay, intDDate, 30, "Date")
                # Setting Hour in Holiday mode
                if self.wait_for_element_exist(*HolidayModePageLocators.DHOUR_PICKER):
                    dHourPicker = self.driver.find_element(*HolidayModePageLocators.DHOUR_PICKER)
                    currentDHour = dHourPicker.get_attribute('value')
                    self.scroll_Date_Hour_Minute(dHourPicker, currentDHour, intDSetHour, 24, "Hour")

                # Setting Minutes in Holiday Mode
                if self.wait_for_element_exist(*HolidayModePageLocators.DMIN_PICKER):
                    dMinPicker = self.driver.find_element(*HolidayModePageLocators.DMIN_PICKER)
                    currentDMin = dMinPicker.get_attribute('value')
                    self.scroll_Date_Hour_Minute(dMinPicker, currentDMin, intDSetMin, 60, "Minute")

            else:
                self.report_fail("iOS App : The Departure Date-Time couldn't be set")

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

            if self.wait_for_element_exist(*HolidayModePageLocators.SET_RETURN):
                self.driver.find_element(*HolidayModePageLocators.SET_RETURN).click()
                # Setting Day in Holiday mode
                if self.wait_for_element_exist(*HolidayModePageLocators.RDAY_PICKER):
                    rDayPicker = self.driver.find_element(*HolidayModePageLocators.RDAY_PICKER)
                    currentRDay = rDayPicker.get_attribute('value')
                    counter = (
                        duration + daysFromNow - 7)  # #this is used since this PICKER's 'value' property doesn't update
                    self.scroll_Date_Hour_Minute(rDayPicker, currentRDay, intRDate, counter, "Date")

                # Setting Hour in Holiday mode
                if self.wait_for_element_exist(*HolidayModePageLocators.RHOUR_PICKER):
                    rHourPicker = self.driver.find_element(*HolidayModePageLocators.RHOUR_PICKER)
                    currentRHour = rHourPicker.get_attribute('value')
                    self.scroll_Date_Hour_Minute(rHourPicker, currentRHour, intRSetHour, 24, "Hour")

                # Setting Minutes in Holiday Mode
                if self.wait_for_element_exist(*HolidayModePageLocators.RMIN_PICKER):
                    rMinPicker = self.driver.find_element(*HolidayModePageLocators.RMIN_PICKER)
                    currentRMin = rMinPicker.get_attribute('value')
                    self.scroll_Date_Hour_Minute(rMinPicker, currentRMin, intRSetMin, 60, "Minute")

                # Collapse the return picker
                self.driver.find_element(*HolidayModePageLocators.SET_RETURN).click()
                time.sleep(2)
            else:
                self.report_fail("iOS App : The Return Date-Time couldn't be set")
        except:
            self.report_fail('iOS APP: Exception in setHolidayStartEndDate method {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def cancelHolidayMode(self, context):
        try:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Cancel Holiday Mode')
            if self.wait_for_element_exist(*HolidayModePageLocators.CANCEL_HOLIDAYMODE_BUTTON):
                self.driver.find_element(*HolidayModePageLocators.CANCEL_HOLIDAYMODE_BUTTON).click()
                time.sleep(1)
                self.driver.find_element(*HolidayModePageLocators.YES_ALERT_BUTTON).click()
                time.sleep(2)
                if self.wait_for_element_exist(*HolidayModePageLocators.ACTIVATE_HOLIDAYMODE_BUTTON):
                    self.report_pass('iOS App : Canceled the Holiday Mode')
                else:
                    self.report_fail('iOS App : Couldn\'t cancel Holiday Mode')
            else:
                self.report_pass('iOS App : Holiday Mode is not active')
        except:
            self.report_fail('iOS APP: Exception in cancelHolidayMode method {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def stopHolidayMode(self, context):
        try:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Stop Holiday Mode')
            if self.wait_for_element_exist(*HolidayModePageLocators.STOP_HOLIDAYMODE_BUTTON):
                self.driver.find_element(*HolidayModePageLocators.STOP_HOLIDAYMODE_BUTTON).click()
                time.sleep(1)
                self.driver.find_element(*HolidayModePageLocators.YES_ALERT_BUTTON).click()
                time.sleep(2)
                if self.wait_for_element_exist(*HolidayModePageLocators.ACTIVATE_HOLIDAYMODE_BUTTON):
                    self.report_pass('iOS App : Stopped the Holiday Mode')
                else:
                    self.report_fail('iOS App : Couldn\'t stop Holiday Mode')
            else:
                self.report_fail('iOS App : Couldn\'t stop Holiday Mode, Holiday Mode is not active')
        except:
            self.report_fail('iOS APP: Exception in stopHolidayMode method {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def set_Holiday_Mode(self, context, actionType, strHolidayModeType, targetTemperature, daysFromNow, duration):
        if self.reporter.ActionStatus:
            try:
                if not "NEW" in strHolidayModeType.upper() and not "CANCEL" in actionType.upper() and not "STOP" in actionType.upper():
                    if self.wait_for_element_exist(*HolidayModePageLocators.STOP_HOLIDAYMODE_BUTTON):
                        self.driver.find_element(*HolidayModePageLocators.STOP_HOLIDAYMODE_BUTTON).click()
                        time.sleep(1)
                        self.driver.find_element(*HolidayModePageLocators.YES_ALERT_BUTTON).click()
                        time.sleep(2)

                    elif self.wait_for_element_exist(*HolidayModePageLocators.CANCEL_HOLIDAYMODE_BUTTON):
                        self.driver.find_element(*HolidayModePageLocators.CANCEL_HOLIDAYMODE_BUTTON).click()
                        time.sleep(1)
                        self.driver.find_element(*HolidayModePageLocators.YES_ALERT_BUTTON).click()
                        time.sleep(2)

                if "CANCEL" in actionType.upper():
                    self.cancelHolidayMode(context)

                if "STOP" in actionType.upper():
                    time.sleep(300)
                    self.refresh_page()
                    time.sleep(5)
                    self.report_done('iOS APP: ScreenShot of active Holiday Mode')
                    self.stopHolidayMode(context)

                if "DEFAULT" in strHolidayModeType.upper() and not "CANCEL" in actionType.upper() and not "STOP" in actionType.upper():
                    self.set_holiday_target_temperature(context, targetTemperature)
                    self.activateHolidayMode(context)

                if "FUTURE" in strHolidayModeType.upper() or "NEW" in strHolidayModeType.upper():
                    self.setHolidayStartEndDate(daysFromNow, duration)
                    self.set_holiday_target_temperature(context, targetTemperature)

                    if 'NEW' in strHolidayModeType.upper():
                        if self.wait_for_element_exist(*HolidayModePageLocators.SAVE_HOLIDAYMODE_BUTTON):
                            self.driver.find_element(*HolidayModePageLocators.SAVE_HOLIDAYMODE_BUTTON).click()
                            time.sleep(2)
                    else:
                        self.activateHolidayMode(context)

            except:
                self.report_fail('iOS APP: Exception in setting Holiday Mode Time {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

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
            self.report_fail('iOS APP: Exception in validateHolidayModeDetails method {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def get_Holiday_DetailsApp(self, actionType, strHolidayModeType):
        if self.wait_for_element_exist(*HolidayModePageLocators.CANCEL_HOLIDAYMODE_BUTTON):
            enabled = 'true'
            # Getting values for Holiday mode start Date & Time
            strDDay = self.driver.find_element(*HolidayModePageLocators.DDAY).get_attribute('value')
            strDMonth_Year = self.driver.find_element(*HolidayModePageLocators.DMONTH_YEAR).get_attribute('value')
            strDTime = self.driver.find_element(*HolidayModePageLocators.DTIME).get_attribute('value')

            # Getting values for Holiday mode return Date & Time
            strRDay = self.driver.find_element(*HolidayModePageLocators.RDAY).get_attribute('value')
            strRMonth_Year = self.driver.find_element(*HolidayModePageLocators.RMONTH_YEAR).get_attribute('value')
            strRTime = self.driver.find_element(*HolidayModePageLocators.RTIME).get_attribute('value')

            strTemp = self.driver.find_element(*HolidayModePageLocators.TEMP).get_attribute('value')

            if strTemp == '#':
                strHolidayTemp = '1'
            elif strTemp == 'N':
                strHolidayTemp = "FROST"
            else:
                strHolidayTemp = strTemp

            strHolidayStartDate = str(strDDay) + str(strDMonth_Year)
            strHolidayStartTime = str(strDTime)
            strHolidayEndDate = str(strRDay) + str(strRMonth_Year)
            strHolidayEndTime = str(strRTime)

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


class MotionSensor(BasePage):
    def navigate_to_motionsensor(self, nameMotionSensor):
        Motion_off = str(HomePageLocators.strLOCAL_OFF)
        Motion_On = str(HomePageLocators.strLOCAL_ON)
        Motion_Offline = str(HomePageLocators.strLOCAL_OFFLINE)

        M_OFF1 = Motion_off.replace("name", nameMotionSensor)
        M_ON1 = Motion_On.replace("name", nameMotionSensor)
        M_OFFLINE1 = Motion_Offline.replace("name", nameMotionSensor)

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()

                if self.is_element_present(By.XPATH, M_ON1):
                    self.driver.find_element(By.XPATH, M_ON1).click()
                    self.report_pass('IOS App : Navigated to device ' + nameMotionSensor + ' screen')
                    time.sleep(3)
                elif self.is_element_present(By.XPATH, M_OFF1):
                    print("Motion is not enabled")
                    self.driver.find_element(By.XPATH, M_OFF1).click()
                    self.report_pass('IOS App : Navigated to device screen ' + nameMotionSensor + ' screen')
                    time.sleep(3)
                elif ('offline' in M_OFFLINE1) & self.is_element_present(By.XPATH, M_OFFLINE1):
                    print("Motion sensor is offline")
                    self.driver.find_element(By.XPATH, M_OFFLINE1).click()
                    self.report_pass(
                        'IOS App : Navigated to ' + nameMotionSensor + ' screen where the sensor is offline')
                    time.sleep(3)
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : Navigated to ' + nameMotionSensor + ' screen')
                else:
                    self.report_fail('IOS App : The given device does not exist in the kit')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_motionsensor Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_eventlogs(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                elif self.wait_for_element_exist(*MotionSensorPageLocators.EVENTLOG_BUTTON):
                    self.driver.find_element(*MotionSensorPageLocators.EVENTLOG_BUTTON).click()
                    print("Navigated to event logs screen successfully")
                    self.report_pass('IOS App : Navigated to event logs of Motion Sensor screen')
                    time.sleep(5)
                else:
                    self.report_fail('IOS App : Navigation to event log failed')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_eventlogs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verify_event_logs(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*MotionSensorPageLocators.NO_MOTION_LOG):
                        print("There is no motion. Call API Validation")
                        self.report_pass('IOS App : Verified there are no logs present in Motion Sensor screen')
                    elif self.wait_for_element_exist(*MotionSensorPageLocators.CURRENT_MOTION_LOG):
                        print("There is current motion. Call API Validation")
                        self.report_pass(
                            'IOS App : Verified there is current motion log present in Motion Sensor screen')
                    elif self.wait_for_element_exist(*MotionSensorPageLocators.INTERRUPTED_MOTION_LOG):
                        print("Multiple motions were detected for today. Call API Validation")
                        self.report_pass('IOS App : Verified there are multiple logs present in Motion Sensor screen')
                    else:
                        self.report_fail('IOS App : Unexpected logs found')
                print("The event logs are verified successfully")
                # self.report_pass('IOS App : Verified the event logs for current day in Motion Sensor screen')
                if self.wait_for_element_exist(*MotionSensorPageLocators.CLOSE_LOG_BUTTON):
                    self.driver.find_element(*MotionSensorPageLocators.CLOSE_LOG_BUTTON).click()
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verify_current_status(self, nameMotionSensor):
        if self.reporter.ActionStatus:
            try:
                currentMotionStatus = ""
                self.driver.execute_script("mobile: scroll", {"direction": "up"})
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*MotionSensorPageLocators.MOTION_LABEL):
                        currentMotionStatus = "True"
                        self.report_pass('IOS App : Current motion status verified as in motion')
                        time.sleep(5)
                    elif self.wait_for_element_exist(*MotionSensorPageLocators.NOMOTION_LABEL):
                        currentMotionStatus = "False"
                        self.report_pass('IOS App : Current motion status verified as no motion')
                        time.sleep(5)
                    else:
                        self.report_fail('IOS App : The given Motion Sensor does not exist in the kit')
                return currentMotionStatus
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_selected_day_log(self, intNumberOf):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    counter = int(intNumberOf)
                    if (counter == 6) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY1_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY1_LOG).click()
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif (counter == 5) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY2_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY2_LOG).click()
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif (counter == 4) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY3_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY3_LOG).click()
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif (counter == 3) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY4_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY4_LOG).click()
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif (counter == 2) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY5_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY5_LOG).click()
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif (counter == 1) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY6_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY6_LOG).click()
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    else:
                        self.report_fail('IOS App : Invalid number of days')
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_recipes(self, strLocation):
        if self.reporter.ActionStatus:
            try:
                time.sleep(3)
                if strLocation == "sensor":
                    if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                        self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                    else:
                        if self.wait_for_element_exist(*MotionSensorPageLocators.TABBAR_RECIPES):
                            self.driver.find_element(*MotionSensorPageLocators.TABBAR_RECIPES).click()
                        if self.wait_for_element_exist(*MotionSensorPageLocators.RECIPE_SCREEN_HEADER):
                            self.report_pass('IOS App : Navigated to Recipes screen for the Sensor')
                        else:
                            self.report_fail('IOS App : Navigation to Recipes screen failed')
                if strLocation == "All":
                    if self.is_element_present(*HomePageLocators.FLIP_TO_HONEYCOMB):
                        self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        if self.is_element_present(*HomePageLocators.MENU_BUTTON):
                            self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                            if self.is_element_present(*HomePageLocators.ALL_RECIPES):
                                self.driver.find_element(*HomePageLocators.ALL_RECIPES).click()
                                if self.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                                    self.report_pass('IOS App : Navigated to All Recipes screen successfully')
                                else:
                                    self.report_fail('IOS App : All Recipes header is not as expected')
                            else:
                                self.report_fail('IOS App : All Recipes option is not displayed')
                        else:
                            self.report_fail('IOS App : Menu button is not displayed')
                    else:
                        self.report_fail('IOS App : Honeycomb dashboard button is not displayed')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_recipes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verify_recipes(self, nameMotionSensor):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    if self.is_element_present(*MotionSensorPageLocators.ADD_RECIPE):
                        self.driver.find_element(*MotionSensorPageLocators.ADD_RECIPE).click()
                        if (self.is_element_present(*MotionSensorPageLocators.RECIPE_SCREEN_HEADER_NEW)) & (
                                self.is_element_present(*MotionSensorPageLocators.CANCEL_RECIPE)):
                            self.driver.find_element(*MotionSensorPageLocators.CANCEL_RECIPE).click()
                            self.report_done("Additional Recipes can be added to the sensor")
                        else:
                            self.report_done("All possible recipes has been added for the sensor")
                        LIST_OF_RECIPES = self.driver.find_elements_by_xpath("//*[contains(@label,'detects motion')]")
                        TOTAL_NUMBER_OF_RECIPES = len(LIST_OF_RECIPES) / 2
                        RECIPE_DETAILS = ""
                        for counter in range(0, int(TOTAL_NUMBER_OF_RECIPES)):
                            IntY = 250 + counter * 72
                            self.driver.tap([(150, IntY)])
                            if self.is_element_present(*MotionSensorPageLocators.SENSOR_RECIPE):
                                RECIPE_TEMP = self.driver.find_element(
                                    *MotionSensorPageLocators.SENSOR_RECIPE).get_attribute('label')
                                RECIPE_DETAILS += RECIPE_TEMP
                                RECIPE_DETAILS += "\n"
                            if self.is_element_present(*MotionSensorPageLocators.CANCEL_RECIPE):
                                self.driver.find_element(*MotionSensorPageLocators.CANCEL_RECIPE).click()
                        self.report_pass(
                            'IOS App : The following recipes has been set for the sensor: \n' + RECIPE_DETAILS + '')
                    else:
                        self.report_fail("Recipes screens validation not completed")

            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_recipes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
                self.report_fail('IOS App : NoSuchElementException: in verify_recipes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class DeviceRecipes(BasePage):
    MS_AVAILABLE = 1
    CS_AVAILABLE = 1
    PLUG_AVAILABLE = 1
    BULB_AVAILABLE = 1
    SET_RECIPE_TRIGERRED = 0
    TEXT_RECIPE_SET = 0

    def chooseDevice(self, SensorName):
        if self.reporter.ActionStatus:
            try:
                print("Select Sensor")
                CurrentSensor = self.driver.find_element(*RecipeScreenLocators.SELECTED_SENSOR).get_attribute('value')
                print(SensorName)
                print(CurrentSensor)
                if SensorName == CurrentSensor:
                    self.driver.find_element(*RecipeScreenLocators.THEN_DONE).click()
                else:
                    for counter in range(0, 10):
                        self.driver.tap([(180, 360)])
                        CurrentSensor = self.driver.find_element(*RecipeScreenLocators.SELECTED_SENSOR).get_attribute(
                            'value')
                        if SensorName == CurrentSensor:
                            print(SensorName)
                            print(CurrentSensor)
                            self.driver.find_element(*RecipeScreenLocators.THEN_DONE).click()
                            break
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_device Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def swipe_control(self, TypeOf):
        if self.reporter.ActionStatus:
            try:
                'Old code for swiping'
                # oScrolElement = self.driver.find_element(*RecipeScreenLocators.NOTIFICATION_PICKER)
                # intLeftX = oScrolElement.location['x']
                # intUpperY = oScrolElement.location['y']
                # intWidth = oScrolElement.size['width']
                # intHieght = oScrolElement.size['height']
                # intStX = intLeftX + intWidth/2
                # intStY = intUpperY +(intHieght/4)
                # intEndX = intStX
                # intEndY = intUpperY + (intHieght/8)
                # intEndRY = intEndY+15
                # intStRY = intStY+15

                # self.driver.swipe(intStX, intEndRY, intEndX, intStRY)
                # self.driver.swipe(intStX, intEndRY, intEndX, intStRY)
                PUSH_STATUS = self.driver.find_element(*RecipeScreenLocators.PUSH_SWITCH).get_attribute('value')
                MAIL_STATUS = self.driver.find_element(*RecipeScreenLocators.MAIL_SWITCH).get_attribute('value')
                TEXT_STATUS = self.driver.find_element(*RecipeScreenLocators.TEXT_SWITCH).get_attribute('value')

                'Handle Text notification'
                if "Text" in TypeOf:
                    if TEXT_STATUS == 0:
                        self.driver.find_element(*RecipeScreenLocators.TEXT_SWITCH).click()
                        DeviceRecipes.TEXT_RECIPE_SET = 1
                        if self.is_element_present(*RecipeScreenLocators.NOT_NOW):
                            self.driver.find_element(*RecipeScreenLocators.NOT_NOW).click()
                            self.report_done(
                                'IOS App : The user is not a Hive Live subscriber so Text notification cannot be set')
                            if PUSH_STATUS == 0:
                                self.driver.find_element(*RecipeScreenLocators.PUSH_SWITCH).click()
                            if MAIL_STATUS == 1:
                                self.driver.find_element(*RecipeScreenLocators.MAIL_SWITCH).click()
                            DeviceRecipes.TEXT_RECIPE_SET = 0
                elif TEXT_STATUS == 1:
                    self.driver.find_element(*RecipeScreenLocators.TEXT_SWITCH).click()

                'Handle other notifications'
                if ("Push" in TypeOf) & ("Email" not in TypeOf):
                    if PUSH_STATUS == 0:
                        self.driver.find_element(*RecipeScreenLocators.PUSH_SWITCH).click()
                    if MAIL_STATUS == 1:
                        self.driver.find_element(*RecipeScreenLocators.MAIL_SWITCH).click()
                elif ("Push" in TypeOf) & ("Email" in TypeOf):
                    # self.driver.swipe(intStX, intStY, intEndX, intEndY)
                    if PUSH_STATUS == 0:
                        self.driver.find_element(*RecipeScreenLocators.PUSH_SWITCH).click()
                    if MAIL_STATUS == 0:
                        self.driver.find_element(*RecipeScreenLocators.MAIL_SWITCH).click()
                elif ("Push" not in TypeOf) & ("Email" in TypeOf):
                    # self.driver.swipe(intStX, intStY, intEndX, intEndY)
                    # self.driver.swipe(intStX, intStY, intEndX, intEndY)
                    if PUSH_STATUS == 1:
                        self.driver.find_element(*RecipeScreenLocators.PUSH_SWITCH).click()
                    if MAIL_STATUS == 0:
                        self.driver.find_element(*RecipeScreenLocators.MAIL_SWITCH).click()
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_device Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_device(self, nameDevice, typeDevice):
        print('Device to navigate :', nameDevice)
        Device_off = str(HomePageLocators.strLOCAL_OFF)
        Device_On = str(HomePageLocators.strLOCAL_ON)
        Device_Offline = str(HomePageLocators.strLOCAL_OFFLINE)

        D_OFF1 = Device_off.replace("name", nameDevice)
        D_ON1 = Device_On.replace("name", nameDevice)
        D_OFFLINE1 = Device_Offline.replace("name", nameDevice)

        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                if self.is_element_present(By.XPATH, D_ON1):
                    self.driver.find_element(By.XPATH, D_ON1).click()
                    time.sleep(3)
                elif ('offline' in D_OFFLINE1) & self.is_element_present(By.XPATH, D_OFFLINE1):
                    self.driver.find_element(By.XPATH, D_OFFLINE1).click()
                    self.report_pass('IOS App : ' + nameDevice + ' is paired with the hub and is offline')
                    time.sleep(3)
                elif self.is_element_present(By.XPATH, D_OFF1):
                    self.driver.find_element(By.XPATH, D_OFF1).click()
                    time.sleep(3)
                else:
                    self.report_fail('IOS App : The given device is not paired with the hub')
                    if 'MS' in typeDevice:
                        DeviceRecipes.MS_AVAILABLE = 0
                    elif 'CS' in typeDevice:
                        DeviceRecipes.CS_AVAILABLE = 0
                    elif 'Plug' in typeDevice:
                        DeviceRecipes.PLUG_AVAILABLE = 0
                    elif 'Bulb' in typeDevice:
                        DeviceRecipes.BULB_AVAILABLE = 0

            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_device Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_allrecipes(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    if self.is_element_present(*HomePageLocators.ALL_RECIPES):
                        self.driver.find_element(*HomePageLocators.ALL_RECIPES).click()
                        if self.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                            self.report_pass('IOS App : Navigated to All Recipes screen successfully')
                        else:
                            self.report_fail('IOS App : All Recipes header is not as expected')
                    else:
                        self.report_fail('IOS App : All Recipes option is not displayed')
                else:
                    self.report_fail('IOS App : Menu button is not displayed')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_device Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def remove_existing_recipes(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*RecipeScreenLocators.ADD_RECIPE):
                    COUNT_OF_RECIPES = 100
                    while COUNT_OF_RECIPES != 0:
                        MS_DISPLAYED = self.driver.find_elements(*RecipeScreenLocators.MS_RECIPE)
                        CSO_DISPLAYED = self.driver.find_elements(*RecipeScreenLocators.CSO_RECIPE)
                        CSC_DISPLAYED = self.driver.find_elements(*RecipeScreenLocators.CSC_RECIPE)
                        COUNT_OF_RECIPES = len(MS_DISPLAYED) + len(CSO_DISPLAYED) + len(CSC_DISPLAYED)
                        print(COUNT_OF_RECIPES)
                        self.driver.tap([(150, 225)])
                        if self.is_element_present(*RecipeScreenLocators.REMOVE_RECIPE):
                            if self.is_element_present(*RecipeScreenLocators.MS_RECIPE):
                                CURRENT_RECIPE = self.driver.find_element(
                                    *RecipeScreenLocators.MS_RECIPE).get_attribute('label')
                            if self.is_element_present(*RecipeScreenLocators.CSO_RECIPE):
                                CURRENT_RECIPE = self.driver.find_element(
                                    *RecipeScreenLocators.CSO_RECIPE).get_attribute('label')
                            if self.is_element_present(*RecipeScreenLocators.CSC_RECIPE):
                                CURRENT_RECIPE = self.driver.find_element(
                                    *RecipeScreenLocators.CSC_RECIPE).get_attribute('label')
                            self.driver.find_element(*RecipeScreenLocators.REMOVE_RECIPE).click()
                            self.report_done('Remove Recipe clicked')
                            if self.is_element_present(*RecipeScreenLocators.REMOVE_POPUP):
                                self.driver.find_element(*RecipeScreenLocators.REMOVE_POPUP).click()
                                self.report_done('Remove in pop up clicked')
                                if self.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                                    self.report_done('Recipe : ' + CURRENT_RECIPE + ' has been removed successfully')
                                else:
                                    self.report_done('Issue in removing recipe')
                            else:
                                self.report_done('Issue in remove recipe pop up')
                        else:
                            continue

                    if self.is_element_present(*RecipeScreenLocators.ADD_RECIPE):
                        self.driver.find_element(*RecipeScreenLocators.ADD_RECIPE).click()
                        if (self.is_element_present(*RecipeScreenLocators.ADD_A_NEW_RECIPE)) & (
                                self.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON)):
                            self.driver.find_element(*MotionSensorPageLocators.CANCEL_RECIPE).click()
                            self.report_pass('IOS App : All recipes set for the user has been removed')
                else:
                    self.report_fail('IOS App : All recipes set for the user was not removed')
            except:
                self.report_fail('IOS App : NoSuchElementException: in remove_existing_recipes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verify_recipe_template(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                if self.is_element_present(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    if self.is_element_present(*HomePageLocators.ALL_RECIPES):
                        self.driver.find_element(*HomePageLocators.ALL_RECIPES).click()
                        if self.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                            if self.is_element_present(*RecipeScreenLocators.ADD_RECIPE):
                                self.driver.find_element(*RecipeScreenLocators.ADD_RECIPE).click()
                                if (self.is_element_present(*RecipeScreenLocators.ADD_A_NEW_RECIPE)) & (
                                        self.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON)):
                                    self.report_pass('IOS App : Navigated to recipe template screen successfully')
                                    if DeviceRecipes.MS_AVAILABLE != 0:
                                        MS_RECIPES = self.driver.find_elements_by_xpath(
                                            "//*[contains(@label,'detects motion')]")
                                        if len(
                                                MS_RECIPES) == 1 & DeviceRecipes.PLUG_AVAILABLE == 0 & DeviceRecipes.BULB_AVAILABLE == 0:
                                            self.report_pass(
                                                'IOS App : As Plug and Bulb are not paired to the Hub, we have only notification recipe for the motion sensor')
                                        elif len(MS_RECIPES) == 2:
                                            if DeviceRecipes.PLUG_AVAILABLE == 0:
                                                self.report_pass(
                                                    'IOS App : As Plug is not paired to the Hub, we have multiple recipes for the motion sensor.')
                                            else:
                                                self.report_pass(
                                                    'IOS App : As Bulb is not paired to the Hub, we have multiple recipes for the motion sensor.')
                                        elif len(MS_RECIPES) == 3:
                                            self.report_pass(
                                                'IOS App : All applicable recipes for the motion sensor are displayed as expected.')
                                        else:
                                            self.report_fail(
                                                'IOS App : The recipe template for motion sensor is incorrect.')
                                    if DeviceRecipes.CS_AVAILABLE != 0:
                                        CSO_RECIPES = self.driver.find_elements_by_xpath(
                                            "//*[contains(@label,'is opened')]")
                                        CSC_RECIPES = self.driver.find_elements_by_xpath(
                                            "//*[contains(@label,'is closed')]")
                                        if len(CSO_RECIPES) == len(CSC_RECIPES):
                                            if len(
                                                    CSO_RECIPES) == 1 & DeviceRecipes.PLUG_AVAILABLE == 0 & DeviceRecipes.BULB_AVAILABLE == 0:
                                                self.report_pass(
                                                    'IOS App : As Plug and Bulb are not paired to the Hub, we have only notification recipe for the contact sensor.')
                                            elif len(CSO_RECIPES) == 2:
                                                if DeviceRecipes.PLUG_AVAILABLE == 0:
                                                    self.report_pass(
                                                        'IOS App : As Plug is not paired to the Hub, we have multiple recipes for the contact sensor.')
                                                else:
                                                    self.report_pass(
                                                        'IOS App : As Bulb is not paired to the Hub, we have multiple recipes for the contact sensor.')
                                            elif len(CSO_RECIPES) == 3:
                                                self.report_pass(
                                                    'IOS App : All applicable recipes for the contact sensor are displayed as expected.')
                                            else:
                                                self.report_fail(
                                                    'IOS App : The recipe template for contact sensor is incorrect.')
                                        else:
                                            self.report_fail(
                                                'IOS App : The recipe template for contact sensor is incorrect.')
                            if (self.is_element_present(*RecipeScreenLocators.ADD_A_NEW_RECIPE)) & (
                                    self.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON)):
                                self.driver.find_element(*MotionSensorPageLocators.CANCEL_RECIPE).click()
                                time.sleep(5)


            except:
                self.report_fail('IOS App : NoSuchElementException: in remove_existing_recipes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_sensor_recipe(self, recipe_exists, TypeOf, Sensor, SensorState):
        if self.reporter.ActionStatus:
            try:
                if recipe_exists == 1:
                    self.report_pass(
                        "" + TypeOf + " notification recipe already exists when " + Sensor + " " + SensorState + "")
                else:
                    if recipe_exists == 2:
                        self.report_pass(
                            "Edit existing recipe as " + TypeOf + " notification recipe when " + Sensor + " " + SensorState + "")
                    else:
                        self.report_pass(
                            "Create recipe as " + TypeOf + " notification recipe when " + Sensor + " " + SensorState + "")
                    DeviceRecipes.create_new_recipe(self, recipe_exists, TypeOf, Sensor, SensorState)
                    DeviceRecipes.SET_RECIPE_TRIGERRED = 1
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_sensor_recipe Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def report_recipe_exists(self, recipe_exists, TypeOf, Sensor, SensorState, Location):
        if self.reporter.ActionStatus:
            try:
                if recipe_exists == 1:
                    if "Text" in TypeOf:
                        if DeviceRecipes.TEXT_RECIPE_SET == 0:
                            self.report_pass(
                                "" + TypeOf + " notification recipe was set without Text notification for " + Sensor + " when " + SensorState + " as the user is not a Hive Live subscriber")
                        else:
                            self.report_pass(
                                "" + TypeOf + " notification recipe displayed in " + Location + " screen for " + Sensor + " when " + SensorState + "")
                    else:
                        self.report_pass(
                            "" + TypeOf + " notification recipe displayed in " + Location + " screen for " + Sensor + " when " + SensorState + "")
                else:
                    self.report_fail(
                        "" + TypeOf + " notification recipe was not displayed in " + Location + " screen for " + Sensor + " when " + SensorState + "")
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_sensor_recipe Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def create_new_recipe(self, recipe_exists, TypeOf, Sensor, SensorState):
        if self.reporter.ActionStatus:
            try:
                time.sleep(3)
                if self.is_element_present(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                if self.is_element_present(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    if self.is_element_present(*HomePageLocators.ALL_RECIPES):
                        self.driver.find_element(*HomePageLocators.ALL_RECIPES).click()
                        if self.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                            if recipe_exists == 2:
                                print('Navigate to existing Recipe')
                                MS_RECIPES = self.driver.find_elements_by_xpath(
                                    "//*[contains(@label,'detects motion')]")
                                CSO_RECIPES = self.driver.find_elements_by_xpath("//*[contains(@label,'is opened')]")
                                CSC_RECIPES = self.driver.find_elements_by_xpath("//*[contains(@label,'is closed')]")

                                TOTAL_NUMBER_OF_RECIPES = (len(MS_RECIPES) + len(CSO_RECIPES) + len(CSC_RECIPES)) / 2
                                for counter in range(0, int(TOTAL_NUMBER_OF_RECIPES)):
                                    IntY = 250 + counter * 72
                                    self.driver.tap([(150, IntY)])
                                    if self.is_element_present(*RecipeScreenLocators.THEN_EXIST):
                                        if self.is_element_present(*RecipeScreenLocators.MS_RECIPE):
                                            EXISTING_RECIPE = self.driver.find_element(
                                                *RecipeScreenLocators.MS_RECIPE).get_attribute('label')
                                        elif self.is_element_present(*RecipeScreenLocators.CSO_RECIPE):
                                            EXISTING_RECIPE = self.driver.find_element(
                                                *RecipeScreenLocators.CSO_RECIPE).get_attribute('label')
                                        elif self.is_element_present(*RecipeScreenLocators.CSC_RECIPE):
                                            EXISTING_RECIPE = self.driver.find_element(
                                                *RecipeScreenLocators.CSC_RECIPE).get_attribute('label')
                                        if (Sensor in EXISTING_RECIPE) & (SensorState in EXISTING_RECIPE):
                                            break
                                        else:
                                            if self.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON):
                                                self.driver.find_element(*RecipeScreenLocators.CANCEL_BUTTON).click()
                                                time.sleep(5)
                            else:
                                if self.is_element_present(*RecipeScreenLocators.ADD_RECIPE):
                                    self.driver.find_element(*RecipeScreenLocators.ADD_RECIPE).click()
                                    if self.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON):
                                        if 'detects motion' in SensorState:
                                            self.driver.find_element(*RecipeScreenLocators.MS_NOT_RECIPE).click()
                                        elif 'opened' in SensorState:
                                            self.driver.find_element(*RecipeScreenLocators.CSO_NOT_RECIPE).click()
                                        elif 'closed' in SensorState:
                                            self.driver.find_element(*RecipeScreenLocators.CSC_NOT_RECIPE).click()
                                        else:
                                            self.report_fail('IOS App : Navigation to Sensor recipe screen failed')
                                    else:
                                        self.report_fail('IOS App : Navigation to Recipe template failed')
                                else:
                                    self.report_fail('IOS App : Add a new recipe failed')
                            if self.is_element_present(*RecipeScreenLocators.TAP_TO_CHOOSE):
                                self.driver.find_element(*RecipeScreenLocators.TAP_TO_CHOOSE).click()
                                DeviceRecipes.chooseDevice(Sensor)
                            if self.is_element_present(*RecipeScreenLocators.THEN_EXIST):
                                self.driver.find_element(*RecipeScreenLocators.THEN_EXIST).click()
                            else:
                                self.report_fail('IOS App : Navigation to Then screen failed')
                            DeviceRecipes.swipe_control(self, TypeOf)
                            if self.is_element_present(*RecipeScreenLocators.THEN_DONE):
                                self.driver.find_element(*RecipeScreenLocators.THEN_DONE).click()
                                if self.is_element_present(*RecipeScreenLocators.SAVE_BUTTON):
                                    self.driver.find_element(*RecipeScreenLocators.SAVE_BUTTON).click()
                                    time.sleep(10)
                                elif self.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON):
                                    self.driver.find_element(*RecipeScreenLocators.CANCEL_BUTTON).click()
                                    time.sleep(10)
                                else:
                                    self.report_fail('IOS App : Recipe save failed')
                            else:
                                self.report_fail('IOS App : Setting Then failed')

                        else:
                            self.report_fail('IOS App : Recipe screen failed')



            except:
                self.report_fail('IOS App : NoSuchElementException: in create_new_recipe Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verify_notification_recipe_exists(self, Sensor, TypeOf, SensorState):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*MotionSensorPageLocators.ADD_RECIPE):
                    LIST_OF_RECIPES = self.driver.find_elements_by_xpath("//*[contains(@label,'Notify me')]")
                    TOTAL_NUMBER_OF_RECIPES = len(LIST_OF_RECIPES) / 2
                    if TOTAL_NUMBER_OF_RECIPES == 0:
                        return 100
                    else:
                        RECIPE_EXISTS = 0
                        for counter in range(0, int(TOTAL_NUMBER_OF_RECIPES)):
                            IntY = 250 + counter * 72
                            self.driver.tap([(150, IntY)])
                            if self.is_element_present(*RecipeScreenLocators.THEN_EXIST):
                                if self.is_element_present(*RecipeScreenLocators.MS_RECIPE):
                                    EXISTING_RECIPE = self.driver.find_element(
                                        *RecipeScreenLocators.MS_RECIPE).get_attribute('label')
                                elif self.is_element_present(*RecipeScreenLocators.CSO_RECIPE):
                                    EXISTING_RECIPE = self.driver.find_element(
                                        *RecipeScreenLocators.CSO_RECIPE).get_attribute('label')
                                elif self.is_element_present(*RecipeScreenLocators.CSC_RECIPE):
                                    EXISTING_RECIPE = self.driver.find_element(
                                        *RecipeScreenLocators.CSC_RECIPE).get_attribute('label')
                                EXISTING_NOTIFICATION = self.driver.find_element(
                                    *RecipeScreenLocators.THEN_EXIST).get_attribute('label')
                                if self.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON):
                                    self.driver.find_element(*RecipeScreenLocators.CANCEL_BUTTON).click()
                                    time.sleep(5)
                                if (Sensor in EXISTING_RECIPE) & (SensorState in EXISTING_RECIPE):
                                    RECIPE_EXISTS = 2
                                    if ("Push" in TypeOf) & ("Email" not in TypeOf) & (
                                                "push" in EXISTING_NOTIFICATION) & (
                                                "email" not in EXISTING_NOTIFICATION):
                                        RECIPE_EXISTS = 1
                                    elif ("Push" in TypeOf) & ("Email" in TypeOf) & (
                                                "push" in EXISTING_NOTIFICATION) & ("email" in EXISTING_NOTIFICATION):
                                        RECIPE_EXISTS = 1
                                    elif ("Push" not in TypeOf) & ("Email" in TypeOf) & (
                                                "email" in EXISTING_NOTIFICATION) & (
                                                "push" not in EXISTING_NOTIFICATION):
                                        RECIPE_EXISTS = 1
                                    elif ("Text" in TypeOf) & ("text" in EXISTING_NOTIFICATION):
                                        RECIPE_EXISTS = 1
                                    elif ("Text" in TypeOf) & ("text" not in EXISTING_NOTIFICATION) & (
                                                "push" in EXISTING_NOTIFICATION) & (
                                                "email" not in EXISTING_NOTIFICATION):
                                        RECIPE_EXISTS = 1
                                    break
                                    # elif (("Text" not in TypeOf) & ("text" not in EXISTING_NOTIFICATION)):
                                    #    RECIPE_EXISTS = 1
                                    # elif (("Text" in TypeOf) & ("text" not in EXISTING_NOTIFICATION)):
                                    #    RECIPE_EXISTS = 2
                                    # elif (("Text" not in TypeOf) & ("text" in EXISTING_NOTIFICATION)):
                                    #    RECIPE_EXISTS = 2
                                    # else:
                                    #    RECIPE_EXISTS = 0
                        return RECIPE_EXISTS
                elif self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_fail(
                        'IOS App : The device is offline so no recipe actions can be performed from device control screen')
                else:
                    self.report_fail("Recipes screens validation not completed")

            except:
                self.report_fail(
                    'IOS App : NoSuchElementException: in verify_notification_recipe_exists Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


class ContactSensors(BasePage):
    def navigate_to_contact_sensor(self, nameContactSensor):
        print('Contact sensor :', nameContactSensor)

        Motion_off = str(HomePageLocators.strLOCAL_OFF)
        Motion_On = str(HomePageLocators.strLOCAL_ON)
        Motion_Offline = str(HomePageLocators.strLOCAL_OFFLINE)

        M_OFF1 = Motion_off.replace("name", nameContactSensor)
        M_ON1 = Motion_On.replace("name", nameContactSensor)
        M_OFFLINE1 = Motion_Offline.replace("name", nameContactSensor)

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                    time.sleep(1)
                    if self.driver.find_element(By.XPATH, M_ON1):
                        self.driver.find_element(By.XPATH, M_ON1).click()
                        self.report_pass('Hive user navigated to ' + nameContactSensor + ' screen successfully')
                        time.sleep(2)
                    elif self.driver.find_element(By.XPATH, M_OFF1):
                        self.driver.find_element(By.XPATH, M_OFF1).click()
                        self.report_pass('Hive user navigated to ' + nameContactSensor + ' screen successfully')
                        time.sleep(2)

                elif self.wait_for_element_exist(*HomePageLocators.FLIP_TO_DEVICE_LIST):
                    if self.is_element_present(By.XPATH, M_ON1):
                        self.driver.find_element(By.XPATH, M_ON1).click()
                        self.report_pass('Hive user navigated to ' + nameContactSensor + ' screen successfully')
                        time.sleep(2)
                    elif self.driver.find_element(By.XPATH, M_OFF1):
                        self.driver.find_element(By.XPATH, M_OFF1).click()
                        time.sleep(2)
                        self.report_pass('Hive user navigated to ' + nameContactSensor + ' screen successfully')

                else:
                    self.report_fail('IOS App : The given Contact Sensor does not exist in the kit')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_contact_sensor Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    '''
    def navigate_to_contact_sensor(self, nameContactSensor):

        Motion_off=str(HomePageLocators.strLOCAL_OFF)
        Motion_On=str(HomePageLocators.strLOCAL_ON)
        Motion_Offline = str(HomePageLocators.strLOCAL_OFFLINE)

        M_OFF1=Motion_off.replace("name", nameContactSensor)
        M_ON1=Motion_On.replace("name", nameContactSensor)
        M_OFFLINE1=Motion_Offline.replace("name", nameContactSensor)

        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.PAGE_NAVIGATOR):
                    if self.is_element_present(By.XPATH,M_ON1):
                        self.driver.find_element(By.XPATH,M_ON1).click()
                        self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                    elif  self.is_element_present(By.XPATH,M_OFF1):
                        self.driver.find_element(By.XPATH,M_OFF1).click()
                        self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                    elif self.is_element_present(By.XPATH,M_OFFLINE1):
                        self.report_fail('IOS App : Given device ' +nameContactSensor+ ' is offline')

                    elif self.wait_for_element_exist(*HomePageLocators.PAGE_NAVIGATOR):
                        self.driver.find_element(*HomePageLocators.PAGE_NAVIGATOR).click()
                        if self.is_element_present(By.XPATH,M_ON1):
                            self.driver.find_element(By.XPATH,M_ON1).click()
                            self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                        elif self.is_element_present(By.XPATH,M_OFF1):
                            self.driver.find_element(By.XPATH,M_OFF1).click()
                            self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                        elif self.is_element_present(By.XPATH,M_OFFLINE1):
                            self.report_fail('IOS App : Given device ' +nameContactSensor+ ' is offline')

                    elif not self.wait_for_element_exist(*HomePageLocators.PAGE_NAVIGATOR):
                        self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB)
                        self.report_pass('IOS App : Hive user is at Dash board List view screen')
                        self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        self.report_pass('IOS App : Hive user is at Dash board screen')

                        if self.is_element_present(By.XPATH,M_ON1):
                         self.driver.find_element(By.XPATH,M_ON1).click()
                        self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                    elif  self.is_element_present(By.XPATH,M_OFF1):
                        self.driver.find_element(By.XPATH,M_OFF1).click()
                        self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                    elif self.is_element_present(By.XPATH,M_OFFLINE1):
                        self.report_fail('IOS App : Given device ' +nameContactSensor+ ' is offline')

                    elif self.wait_for_element_exist(*HomePageLocators.PAGE_NAVIGATOR):
                        self.driver.find_element(*HomePageLocators.PAGE_NAVIGATOR).click()
                        if self.is_element_present(By.XPATH,M_ON1):
                            self.driver.find_element(By.XPATH,M_ON1).click()
                            self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                        elif self.is_element_present(By.XPATH,M_OFF1):
                            self.driver.find_element(By.XPATH,M_OFF1).click()
                            self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                        elif self.is_element_present(By.XPATH,M_OFFLINE1):
                            self.report_fail('IOS App : Given device ' +nameContactSensor+ ' is offline')

                else:
                    self.report_fail('IOS App : The given Contact Sensor does not exist in the kit')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_contact_sensor Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    '''

    def contactSensorCurrentStatus(self, nameContactSensor):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*ContactSensorLocators.CS_STATUS_OPEN):
                    currentStatus = self.driver.find_element(*ContactSensorLocators.CS_STATUS_OPEN).get_attribute(
                        'value')
                    print(currentStatus)
                    self.report_pass('iOS APP: Captured the current status of device successfully')
                else:
                    currentStatus = self.driver.find_element(*ContactSensorLocators.CS_STATUS_CLOSED).get_attribute(
                        'value')
                    print(currentStatus)
                    self.report_pass('iOS APP: Captured the current status of device successfully')

                return currentStatus
            except:
                self.report_fail('IOS App : NoSuchElementException: in contactSensorCurrentStatus Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def todaysLog(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The Contact sensor is offline. No validations possible.')
                elif self.wait_for_element_exist(*ContactSensorLocators.LOGS):
                    self.driver.find_element(*ContactSensorLocators.LOGS).click()
                    self.report_pass('iOS APP: Hive user is able to see the Todays log screen')
                    time.sleep(3)
                else:
                    self.report_fail('iOS APP: Hive user is not able to see the Todays log screen')
            except:
                self.report_fail('IOS App : NoSuchElementException: in todaysLog Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def navigate_to_selected_weekday_log(self, selectWeekDay):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The Contact sensor is offline. No validations possible.')
                else:
                    counter = int(selectWeekDay)
                    if (counter == 6) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY1_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY1_LOG).click()
                        time.sleep(1)
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif (counter == 5) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY2_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY2_LOG).click()
                        time.sleep(1)
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif (counter == 4) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY3_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY3_LOG).click()
                        time.sleep(1)
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif (counter == 3) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY4_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY4_LOG).click()
                        time.sleep(1)
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif (counter == 2) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY5_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY5_LOG).click()
                        time.sleep(1)
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif (counter == 1) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY6_LOG)):
                        self.driver.find_element(*MotionSensorPageLocators.DAY6_LOG).click()
                        time.sleep(1)
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    else:
                        self.report_fail('IOS App : Invalid number of days')
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verify_todayevent_logs(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The contact sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*ContactSensorLocators.NO_EVENTS):
                        self.report_pass('IOS App : Verified that contact sensor did not have any events on the day')
                    elif self.wait_for_element_exist(*ContactSensorLocators.OPEN_ALL_DAY):
                        self.report_pass('IOS App : Verified that contact sensor opened all day')
                    elif self.wait_for_element_exist(*ContactSensorLocators.OPEN_CURRENT_LOG):

                        self.report_pass('IOS App : Verified that contact sensor is opened now')
                    elif self.wait_for_element_exist(*ContactSensorLocators.OPEN_MUTLIPE_LOG):

                        self.report_pass('IOS App : Verified that contact sensor is open multiple times')
                    else:
                        self.report_fail('IOS App : Unexpected logs found')

                if self.wait_for_element_exist(*MotionSensorPageLocators.CLOSE_LOG_BUTTON):
                    self.driver.find_element(*MotionSensorPageLocators.CLOSE_LOG_BUTTON).click()
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class ColourLights(BasePage):
    SETTINGS_LOCAL = ""
    VALUE_LOCAL = ""
    SWITCH_ON = 0
    Bulb_Object = ""
    Bulb_Tone_Ring = ""
    Bulb_Brightness_Ring = ""
    Bulb_Colour_Ring = ""
    BULB_MODEL = ""
    BULB_MODE = ""
    BULB_STATUS_DEVICE_LIST = ""

    def updateBulbObjects(self, strDeviceName):
        BulbName_Local = str(BulbScreenLocators.BULB_NAME)
        ColourLights.Bulb_Object = BulbName_Local.replace("name", strDeviceName)
        BulbTone_Local = str(BulbScreenLocators.BULB_TONE)
        ColourLights.Bulb_Tone_Ring = BulbTone_Local.replace("name", strDeviceName)
        BulbBrightness_Local = str(BulbScreenLocators.BULB_BRIGHTNESS)
        ColourLights.Bulb_Brightness_Ring = BulbBrightness_Local.replace("name", strDeviceName)
        BulbColour_Local = str(BulbScreenLocators.BULB_COLOUR)
        ColourLights.Bulb_Colour_Ring = BulbColour_Local.replace("name", strDeviceName)
        ColourLights.BULB_MODEL = oAPIValidations.getDeviceModel(strDeviceName)
        BulbMode_local = str(BulbScreenLocators.BULB_MODE)
        ColourLights.BULB_MODE = BulbMode_local.replace("name", strDeviceName)
        BulbStatusDeviceList_Local = str(BulbScreenLocators.BULB_STATUS_DEVICE_LIST)
        ColourLights.BULB_STATUS_DEVICE_LIST = BulbStatusDeviceList_Local.replace("name", strDeviceName)

    def setValues(self, Settings, Value):
        ColourLights.SETTINGS_LOCAL = Settings
        ColourLights.VALUE_LOCAL = Value

    def navigateToSettings(self, Settings):
        if self.reporter.ActionStatus:
            try:
                # BULB_STATUS = self.driver.find_element(*BulbScreenLocators.BULB).get_attribute('value')
                BULB_STATUS = self.driver.find_element(By.NAME, ColourLights.Bulb_Object).get_attribute('value')
                if "off" in BULB_STATUS:
                    self.driver.tap([(158, 236)])
                    ColourLights.SWITCH_ON = 1
                if "tone" in Settings:
                    if self.is_element_present(*BulbScreenLocators.COLOUR_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.COLOUR_BUTTON).click()
                    if self.is_element_present(*BulbScreenLocators.TONE_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.TONE_BUTTON).click()
                    else:
                        print("")
                elif "brightness" in Settings:
                    if self.is_element_present(*BulbScreenLocators.DIMMER_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.DIMMER_BUTTON).click()
                    else:
                        print("")
                elif "colour" in Settings:
                    if self.is_element_present(*BulbScreenLocators.TONE_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.TONE_BUTTON).click()
                    if self.is_element_present(*BulbScreenLocators.COLOUR_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.COLOUR_BUTTON).click()
                    else:
                        print("")
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigateToSettings Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def setValueForBulb(self, Settings, verifyValue):
        if self.reporter.ActionStatus:
            try:
                angleStep = 0
                if "tone" in Settings:
                    if self.is_element_present(By.XPATH, ColourLights.Bulb_Tone_Ring):
                        oBulb = self.driver.find_element(By.XPATH, ColourLights.Bulb_Tone_Ring)
                        angleStep = 20
                    else:
                        self.report_step('IOS App : Tone settings was not displayed')
                elif "brightness" in Settings:
                    if self.is_element_present(By.XPATH, ColourLights.Bulb_Brightness_Ring):
                        oBulb = self.driver.find_element(By.XPATH, ColourLights.Bulb_Brightness_Ring)
                        angleStep = 10
                    else:
                        self.report_step('IOS App : Brightness settings was not displayed')
                elif "colour" in Settings:
                    if self.is_element_present(By.XPATH, ColourLights.Bulb_Colour_Ring):
                        oBulb = self.driver.find_element(By.XPATH, ColourLights.Bulb_Colour_Ring)
                        angleStep = 10
                    else:
                        self.report_step('IOS App : Colour settings was not displayed')

                intLeftX = oBulb.location['x']
                intUpperY = oBulb.location['y']
                intSide = oBulb.size['width']
                intSideT = (intSide / 2)
                intCenterX = intLeftX + intSideT
                intCenterY = intUpperY + intSideT
                intRadius = intCenterX - 32
                intTempStartX = intCenterX + intRadius * math.cos(180)
                intTempStartY = intCenterY + intRadius * math.sin(180)

                for angle in range(165, 375, angleStep):
                    intTempNewStartX = intCenterX + intRadius * math.cos(angle * math.pi / 180)
                    intTempNewStartY = intCenterY + intRadius * math.sin(angle * math.pi / 180)
                    intTempNewStartX = int(intTempNewStartX)
                    intTempNewStartY = int(intTempNewStartY)
                    if intTempNewStartY <= 288:
                        self.driver.tap([(intTempNewStartX, intTempNewStartY)])
                        self.driver.swipe(intTempStartX, intTempStartY, intTempNewStartX, intTempNewStartY)
                    time.sleep(5)
                    if "tone" in Settings:
                        currentValue = self.driver.find_element(By.XPATH, ColourLights.Bulb_Tone_Ring).get_attribute(
                            'value')
                        if verifyValue in currentValue:  # cool white vs coolest white/warmest white
                            self.report_pass('IOS App : Value set for bulb ' + Settings + ' as ' + currentValue)
                            break
                    elif "brightness" in Settings:
                        currentValue = self.driver.find_element(By.XPATH,
                                                                ColourLights.Bulb_Brightness_Ring).get_attribute(
                            'value')
                        if verifyValue in currentValue:
                            self.report_pass('IOS App : Value set for bulb ' + Settings + ' as ' + currentValue)
                            break
                    elif "colour" in Settings:
                        currentValue = self.driver.find_element(By.XPATH, ColourLights.Bulb_Colour_Ring).get_attribute(
                            'value')
                        if verifyValue == currentValue:
                            self.report_pass('IOS App : Value set for bulb ' + Settings + ' as ' + currentValue)
                            break
            except:
                self.report_fail('IOS App : NoSuchElementException: in setValueForBulb Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verifyAPI(self):
        if self.reporter.ActionStatus:
            try:
                attributeVerify = ""
                attributeName = ""
                if "tone" in ColourLights.SETTINGS_LOCAL:
                    attributeVerify = "colourTemperature"
                    attributeName = "reportedValue"
                elif "colour" in ColourLights.SETTINGS_LOCAL:
                    attributeVerify = "hsvHue"
                    attributeName = "targetValue"
                elif "brightness" in ColourLights.SETTINGS_LOCAL:
                    attributeVerify = "brightness"
                    attributeName = "reportedValue"
                nodeID = oAPIValidations.getDeviceNodeID(ColourLights.BULB_MODEL)
                time.sleep(3)
                attributeValue = oAPIValidations.getColourBulbValues(nodeID, attributeVerify, attributeName)
                attributeValue = int(attributeValue)
                if attributeValue != "":
                    if "tone" in ColourLights.SETTINGS_LOCAL:
                        if "coolest white" in ColourLights.VALUE_LOCAL:
                            if attributeValue >= 5471 & attributeValue <= 6535:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for tone is updated in the API as ' + attributeValue + ' for given tone ' + ColourLights.VALUE_LOCAL)
                        elif "cool white" in ColourLights.VALUE_LOCAL:
                            if attributeValue >= 4981 & attributeValue <= 5740:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for tone is updated in the API as ' + attributeValue + ' for given tone ' + ColourLights.VALUE_LOCAL)
                        elif "mid white" in ColourLights.VALUE_LOCAL:
                            if attributeValue >= 4221 & attributeValue <= 4980:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for tone is updated in the API as ' + attributeValue + ' for given tone ' + ColourLights.VALUE_LOCAL)
                        elif "warm white" in ColourLights.VALUE_LOCAL:
                            if attributeValue >= 3461 & attributeValue <= 4220:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for tone is updated in the API as ' + attributeValue + ' for given tone ' + ColourLights.VALUE_LOCAL)
                        elif "warmest white" in ColourLights.VALUE_LOCAL:
                            if attributeValue >= 2700 & attributeValue <= 3460:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for tone is updated in the API as ' + attributeValue + ' for given tone ' + ColourLights.VALUE_LOCAL)
                        else:
                            attributeValue = str(attributeValue)
                            self.report_fail(
                                'IOS App : The value for tone is updated in the API as ' + attributeValue + ' for given tone ' + ColourLights.VALUE_LOCAL)
                    elif "colour" in ColourLights.SETTINGS_LOCAL:
                        if ColourLights.VALUE_LOCAL == "Red":
                            if attributeValue <= 6:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Red Orange":
                            if attributeValue >= 11 & attributeValue <= 20:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Orange":
                            if attributeValue >= 21 & attributeValue <= 40:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Orange Yellow":
                            if attributeValue >= 41 & attributeValue <= 50:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Yellow":
                            if attributeValue >= 51 & attributeValue <= 60:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Yellow Green":
                            if attributeValue >= 61 & attributeValue <= 80:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Green":
                            if attributeValue >= 81 & attributeValue <= 140:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Green Cyan":
                            if attributeValue >= 141 & attributeValue <= 169:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Cyan":
                            if attributeValue >= 170 & attributeValue <= 200:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Cyan Blue":
                            if attributeValue >= 201 & attributeValue <= 220:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Blue":
                            if attributeValue >= 221 & attributeValue <= 240:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Blue Magenta":
                            if attributeValue >= 241 & attributeValue <= 280:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Magenta":
                            if attributeValue >= 281 & attributeValue <= 320:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Magenta Pink":
                            if attributeValue >= 321 & attributeValue <= 330:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Pink":
                            if attributeValue >= 331 & attributeValue <= 345:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                        elif ColourLights.VALUE_LOCAL == "Pink Red":
                            if attributeValue >= 346 & attributeValue <= 355:
                                attributeValue = str(attributeValue)
                                self.report_pass(
                                    'IOS App : The value for colour is updated in the API as ' + attributeValue + ' for given colour ' + ColourLights.VALUE_LOCAL)
                    elif "brightness" in ColourLights.SETTINGS_LOCAL:
                        if int(ColourLights.VALUE_LOCAL) == attributeValue:
                            attributeValue = str(attributeValue)
                            self.report_pass(
                                'IOS App : The value for brightness is updated in the API as ' + attributeValue + ' for given brightness ' + ColourLights.VALUE_LOCAL)
                        else:
                            attributeValue = str(attributeValue)
                            self.report_fail(
                                'IOS App : The value for brightness is updated in the API as ' + attributeValue + ' for given brightness ' + ColourLights.VALUE_LOCAL)
                else:
                    self.report_fail('IOS App : API validation failed for ' + ColourLights.SETTINGS_LOCAL)

                if ColourLights.SWITCH_ON == 1:
                    self.driver.tap([(158, 236)])
                    ColourLights.SWITCH_ON = 0

            except:
                self.report_fail('IOS App : NoSuchElementException: in verifyAPI Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verifyDeviceModes(self, strdeviceName):
        if self.reporter.ActionStatus:
            try:
                oDeviceMode = self.driver.find_element(By.XPATH, ColourLights.BULB_MODE)
                intX = oDeviceMode.location['x']
                intY = oDeviceMode.location['y']
                intHeight = oDeviceMode.size['height']
                intMid = intHeight / 2
                # Co-ordinates to click on the "<" symbol to change the device mode from Manual to Schedule and vice versa
                intCenterX = intX + 25
                intCenterY = intY + intMid
                bulb_status_device_list = ""
                changeMode = [(intCenterX, intCenterY)]

                if self.is_element_present(*BulbScreenLocators.MANUAL_MODE_LABEL):
                    expectedMode1 = "Schedule active"
                    self.driver.tap(changeMode)
                    time.sleep(2)
                    if self.is_element_present(*BulbScreenLocators.SCHEDULE_MODE_LABEL):
                        self.report_step("Colour bulb was set on Manual Mode, successfully changed to Schedule mode.")
                        if self.is_element_present(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK):
                            self.driver.find_element(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK).click()
                            time.sleep(2)
                            if self.is_element_present(*BulbScreenLocators.SCHEDULE_ON):
                                self.report_pass(
                                    "Successfully navigated from manual mode to schedule mode and validated that the Schedule is active.")
                                self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                                time.sleep(2)
                                self.driver.find_element(*HomePageLocators.FLIP_TO_DEVICE_LIST).click()
                                time.sleep(2)
                                if self.is_element_present(By.XPATH, ColourLights.BULB_STATUS_DEVICE_LIST):
                                    bulb_status_device_list = self.driver.find_element(
                                        By.XPATH, ColourLights.BULB_STATUS_DEVICE_LIST).get_attribute('value')
                                    actualMode1 = bulb_status_device_list
                                if "Schedule active" in bulb_status_device_list:
                                    self.report_pass("Validated that the Schedule is active in the Device List.")

                                    Header = " Expected $$ Actual @@@"

                                    tableRow1 = expectedMode1 + "$$" + actualMode1

                                    StrLog = Header + tableRow1
                                    self.reporter.ReportEvent("Test Validation", StrLog, "PASS")

                                else:
                                    self.report_fail("Validation failed for active schedule in the Device List.")
                                    self.report_pass("Validated that the Schedule is active in the Device List.")

                                    Header = " Expected $$ Actual @@@"

                                    tableRow1 = expectedMode1 + "$$||" + actualMode1

                                    StrLog = Header + tableRow1
                                    self.reporter.ReportEvent("Test Validation", StrLog, "FAIL")
                                self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                                time.sleep(2)
                                # Navigate back to the light control page for further validation
                                strDeviceMode = self.verifyDeviceModeAPI()
                                if strDeviceMode != "":
                                    if "AUTO" in strDeviceMode.upper():
                                        self.report_pass("Schedule is active, verified through API")
                                    elif "MANUAL" in strDeviceMode.upper():
                                        self.report_fail("Schedule is NOT active, verified through API")
                self.navigate_to_device(strdeviceName)
                if self.is_element_present(*BulbScreenLocators.SCHEDULE_MODE_LABEL):
                    expectedMode2 = "Manual"
                    self.driver.tap(changeMode)
                    time.sleep(2)
                    if self.is_element_present(*BulbScreenLocators.MANUAL_MODE_LABEL):
                        self.report_step("Colour bulb was set on Schedule Mode, successfully changed to Manual mode.")
                        if self.is_element_present(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK):
                            self.driver.find_element(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK).click()
                            time.sleep(2)
                            if self.is_element_present(*BulbScreenLocators.SCHEDULE_OFF):
                                self.report_pass(
                                    "Successfully navigated from schedule mode to manual mode and validated that the schedule is not being used.")
                                if self.is_element_present(*BulbScreenLocators.CONTROL_LINK):
                                    self.driver.find_element(*BulbScreenLocators.CONTROL_LINK).click()
                                    time.sleep(2)
                                BULB_STATUS = self.driver.find_element(By.NAME, ColourLights.Bulb_Object).get_attribute(
                                    'value')
                                if "off" in BULB_STATUS:
                                    self.driver.tap([(158, 236)])
                                time.sleep(2)
                                self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                                time.sleep(2)
                                self.driver.find_element(*HomePageLocators.FLIP_TO_DEVICE_LIST).click()
                                time.sleep(2)
                                if self.is_element_present(By.XPATH, ColourLights.BULB_STATUS_DEVICE_LIST):
                                    bulb_status_device_list = self.driver.find_element(
                                        By.XPATH, ColourLights.BULB_STATUS_DEVICE_LIST).get_attribute('value')
                                    actualMode2 = bulb_status_device_list
                                if "Manual" in bulb_status_device_list:
                                    self.report_pass("Validated that the device is in Manual mode in the Device List.")
                                    Header = " Expected $$ Actual @@@"

                                    tableRow1 = expectedMode2 + "$$" + actualMode2

                                    StrLog = Header + tableRow1
                                    self.reporter.ReportEvent("Test Validation", StrLog, "PASS")
                                else:
                                    self.report_fail(
                                        "Validation failed for the manual mode of the device in the Device List.")
                                    Header = " Expected $$ Actual @@@"

                                    tableRow1 = expectedMode2 + "$$||" + actualMode2

                                    StrLog = Header + tableRow1
                                    self.reporter.ReportEvent("Test Validation", StrLog, "FAIL")
                                self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                                time.sleep(2)
                                strDeviceMode = self.verifyDeviceModeAPI()
                                if strDeviceMode != "":
                                    if "MANUAL" in strDeviceMode.upper():
                                        self.report_pass("Device is on Manual mode, verified through API")
                                    elif "AUTO" in strDeviceMode.upper():
                                        self.report_fail("Device is not on Manual mode, verified through API")

            except:
                self.report_fail('IOS App : NoSuchElementException: in verifyDeviceModes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
                print('IOS App : NoSuchElementException: in verifyDeviceModes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verifyDeviceModeAPI(self):
        if self.reporter.ActionStatus:
            try:
                nodeID = oAPIValidations.getDeviceNodeID(ColourLights.BULB_MODEL)
                time.sleep(3)
                strDeviceMode = oAPIValidations.getDeviceModeStatus(nodeID)
                if strDeviceMode != "":
                    return strDeviceMode
            except:
                self.report_fail('IOS App : Exception: in verifyDeviceModeAPI Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
                print('IOS App : Exception: in verifyDeviceModeAPI Method\n {0}'.format(
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
        nodes = oAPIValidations.getNodes()
        count = 0
        Plug = False
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
        Plug_Dashboard_on = HomePageLocators.Plug_runtime_Dashboard_on
        Plug_Dashboard_on = Plug_Dashboard_on.replace("devicename", PlugName)
        Plug_Dashboard_off = HomePageLocators.Plug_runtime_Dashboard_off
        Plug_Dashboard_off = Plug_Dashboard_off.replace("devicename", PlugName)
        try:
            if self.wait_for_element_exist(*PlugLocators.DEVICELIST_ICON):
                if 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute(
                        'name').upper():
                    self.report_done('User is in Dashboard Screen')
                else:
                    self.driver.find_element(*PlugLocators.DEVICELIST_ICON).click()
                    time.sleep(2)
                    if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                        self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                        time.sleep(2)
                        if 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute(
                                'name').upper():
                            self.report_done('User is in Dashboard Screen')
                        else:
                            self.report_fail('Dashboard Screen Label is not found')
                    else:
                        self.report_fail('Dashboard Icon not found')
                if self.is_element_present(By.XPATH, Plug_Dashboard_on):
                    self.driver.find_element(By.XPATH, Plug_Dashboard_on).click()
                    self.report_pass('Plug is found in Dashboard and clicked')
                elif self.is_element_present(By.XPATH, Plug_Dashboard_off):
                    self.driver.find_element(By.XPATH, Plug_Dashboard_off).click()
                    self.report_pass('Plug is found in Dashboard and clicked')
                else:
                    self.driver.swipe(1008.7, 1534.9, 108.3, 1598.7, 2000)
                    if self.is_element_present(By.XPATH, Plug_Dashboard_on):
                        self.driver.find_element(By.XPATH, Plug_Dashboard_on).click()
                        self.report_pass('Plug is found in Dashboard and clicked')
                    elif self.is_element_present(By.XPATH, Plug_Dashboard_off):
                        self.driver.find_element(By.XPATH, Plug_Dashboard_off).click()
                        self.report_pass('Plug is found in Dashboard and clicked')
                    else:
                        self.report_fail('Plug is not found in Dashboard')
            elif self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                time.sleep(2)
                if self.is_element_present(By.XPATH, Plug_Dashboard_on):
                    self.driver.find_element(By.XPATH, Plug_Dashboard_on).click()
                    self.report_pass('Plug is found in Dashboard and clicked')
                elif self.is_element_present(By.XPATH, Plug_Dashboard_off):
                    self.driver.find_element(By.XPATH, Plug_Dashboard_off).click()
                    self.report_pass('Plug is found in Dashboard and clicked')
                else:
                    self.driver.swipe(1008.7, 1534.9, 108.3, 1598.7, 2000)
                    if self.is_element_present(By.XPATH, Plug_Dashboard_on):
                        self.driver.find_element(By.XPATH, Plug_Dashboard_on).click()
                        self.report_pass('Plug is found in Dashboard and clicked')
                    elif self.is_element_present(By.XPATH, Plug_Dashboard_off):
                        self.driver.find_element(By.XPATH, Plug_Dashboard_off).click()
                        self.report_pass('Plug is found in Dashboard and clicked')
                    else:
                        self.report_fail('Plug is not found in Dashboard')

            else:
                self.report_fail('User is not inside the app')
        except:
            self.report_fail('IOS App : NoSuchElementException: in navigate_to_plug Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # function to verify the plugs screen title

    def verify_plugstitle(self, PlugName):
        Plug_Title = PlugLocators.PLUG_TITLE
        Plug_Title = Plug_Title.replace("devicename", PlugName)
        if self.is_element_present(By.XPATH, Plug_Title):
            if PlugName.upper() in self.driver.find_element(By.XPATH, Plug_Title).get_attribute('name').upper():
                self.report_pass('PlugTitle is same as name which user have given -' + PlugName)
        else:
            if not 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute(
                    'name').upper():
                if self.is_element_present(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                    PlugsPage.navigation_to_plugpage(self, PlugName)
                    if PlugName.upper() in self.driver.find_element(By.XPATH, Plug_Title).get_attribute(
                            'name').upper():
                        self.report_pass('PlugTitle is same as name which user have given -' + PlugName)
                    else:
                        self.report_fail('PlugTitle and Plugname are not same.')
                else:
                    self.report_fail('User is not inside the app')
            else:
                PlugsPage.navigation_to_plugpage(self, PlugName)
                if PlugName.upper() in self.driver.find_element(By.XPATH, Plug_Title).get_attribute(
                        'name').upper():
                    self.report_pass('PlugTitle is same as name which user have given -' + PlugName)
                else:
                    self.report_fail('PlugTitle and Plugname are not same.')

    # to check whether plug is in off state or on state

    def verify_plugstate_api(self, PlugName):
        nodes = oAPIValidations.getNodes()
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
        nodes = oAPIValidations.getNodes()
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

    # function to change the plug state
    def click_plugs_toggle(self, PlugName):
        apimode = self.verify_plugstate_api(PlugName)
        if self.is_element_present(*PlugLocators.PLUG_STATE):
            if self.is_element_present(*PlugLocators.PLUG_OFF):
                self.report_pass('Toggle Button is found')
                if apimode == "OFF":
                    self.report_pass('Plug is currently in OFF state in both api and app.')
                elif apimode == "ON":
                    self.report_fail('Plug is currently in ON state in api but off in app.')
                else:
                    self.report_fail('Not able to get the Plug state from api.')

                self.driver.find_element(*PlugLocators.PLUG_STATE).click()
                self.report_done('Toggle Button for changing Plugs state is clicked')
                PlugsPage.beforeoffmode = "off"
                if self.is_element_present(*PlugLocators.PLUG_ON):
                    PlugsPage.afteroffmode = "on"
            elif self.is_element_present(*PlugLocators.PLUG_ON):
                self.report_pass('Toggle Button is found')
                if apimode == "OFF":
                    self.report_fail('Plug is currently in OFF state in api but ON in app.')
                elif apimode == "ON":
                    self.report_pass('Plug is currently in ON state in both api and app.')
                else:
                    self.report_fail('Not able to get the Plug state from api.')
                self.driver.find_element(*PlugLocators.PLUG_STATE).click()
                self.report_done('Toggle Button for changing Plugs state is clicked')
                PlugsPage.beforeonmode = "on"
                if self.is_element_present(*PlugLocators.PLUG_OFF):
                    PlugsPage.afteronmode = "off"
            else:
                self.report_fail('Not able to get the Plug state from app.')
        else:
            self.report_fail('Toggle button not found.')

    # function to verify the state of the plugs
    def verify_plugs_on_off(self, PlugName):
        time.sleep(10)
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
        PLUG_ON_DASH = HomePageLocators.Plug_runtime_Dashboard_on
        PLUG_ON_DASH = PLUG_ON_DASH.replace("devicename", PlugName)
        PLUG_OFF_DASH = HomePageLocators.Plug_runtime_Dashboard_off
        PLUG_OFF_DASH = PLUG_OFF_DASH.replace("devicename", PlugName)
        if self.is_element_present(*PlugLocators.DASHBOARD_ICON):
            self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            if self.is_element_present(*PlugLocators.DASHBOARD_ICON):
                self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            self.report_done('Dashboard Icon is clicked.')
            time.sleep(5)
            if self.is_element_present(By.XPATH, PLUG_ON_DASH):
                if PlugsPage.finalstate == "ON":
                    self.report_pass('Plug is on in Dashboard Screen and Api.')
                elif PlugsPage.finalstate == "OFF":
                    self.report_fail('Plug is on in Dashboard Screen but off in Api.')
            elif self.is_element_present(By.XPATH, PLUG_OFF_DASH):
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
        PLUG = PlugLocators.PLUG_DEVICELIST
        PLUG = PLUG.replace("devicename", PlugName)

        if self.driver.find_element(*PlugLocators.DEVICELIST_ICON):
            self.driver.find_element(*PlugLocators.DEVICELIST_ICON).click()
            self.report_done('Device Screen Icon is clicked.')
            time.sleep(5)
            if 'ON' in self.driver.find_element(By.XPATH, PLUG).get_attribute('name').upper():
                if PlugsPage.finalstate == "ON":
                    self.report_pass('Plug is on in DeviceList Screen and Api.')
                    self.driver.find_element(By.XPATH, PLUG).click()
                elif PlugsPage.finalstate == "OFF":
                    self.report_fail('Plug is on in DeviceList Screen but off in Api.')
            elif 'OFF' in self.driver.find_element(By.XPATH, PLUG).get_attribute('name').upper():
                if PlugsPage.finalstate == "OFF":
                    self.report_pass('Plug is off in DeviceList Screen and Api.')
                    self.driver.find_element(By.XPATH, PLUG).click()
                elif PlugsPage.finalstate == "ON":
                    self.report_fail('Plug is off in DeviceList Screen but on in Api.')
            else:
                TouchAction(self.driver).press(None, 329, 683).wait(2000).move_to(None, 0, -317).release().perform()
                if 'ON' in self.driver.find_element(By.XPATH, PLUG).get_attribute('name').upper():
                    if PlugsPage.finalstate == "ON":
                        self.report_pass('Plug is on in DeviceList Screen and Api.')
                        self.driver.find_element(By.XPATH, PLUG).click()
                    elif PlugsPage.finalstate == "OFF":
                        self.report_fail('Plug is on in DeviceList Screen but off in Api.')
                elif 'OFF' in self.driver.find_element(By.XPATH, PLUG).get_attribute('name').upper():
                    if PlugsPage.finalstate == "OFF":
                        self.report_pass('Plug is off in DeviceList Screen and Api.')
                        self.driver.find_element(By.XPATH, PLUG).click()
                    elif PlugsPage.finalstate == "ON":
                        self.report_fail('Plug is off in DeviceList Screen but on in Api.')
                else:
                    self.report_fail('Error in getting the exact state in Device screen.')
            time.sleep(5)
        else:
            self.report_fail('Error in finding the PlugLocators for DeviceList Screen button.')

            # function to change the mode of the plugs.

    def click_plugs_arrow(self, PlugName):
        apimode = self.verify_plugmode_api(PlugName)
        if self.is_element_present(*PlugLocators.PLUG_MANUAL_MODE):
            oDeviceMode = self.driver.find_element(*PlugLocators.PLUG_MANUAL_MODE)
        elif self.is_element_present(*PlugLocators.PLUG_SCHEDULE_MODE):
            oDeviceMode = self.driver.find_element(*PlugLocators.PLUG_SCHEDULE_MODE)
        intLeftX = oDeviceMode.location['x']
        intUpperY = oDeviceMode.location['y']
        intWidth = oDeviceMode.size['height']
        intMid = intWidth / 2

        intCenterX = intLeftX + 25
        intCenterY = intUpperY + intMid

        print("Arrow co-ordinates are : ", intCenterX, intCenterY)
        positions = [(intCenterX, intCenterY)]

        if self.is_element_present(*PlugLocators.PLUG_MANUAL_MODE):
            PlugsPage.currentstate = "Manual"
            if apimode == "Manual":
                self.report_pass('Plug is currently in manual mode in both api and app.')
            elif apimode == "Schedule":
                self.report_fail('Plug is currently in Schedule mode in api but Manual in app.')
            else:
                self.report_fail('Not able to get the Plug mode from api.')
        elif self.is_element_present(*PlugLocators.PLUG_SCHEDULE_MODE):
            PlugsPage.currentstate = "Schedule"
            if apimode == "Manual":
                self.report_fail('Plug is currently in Manual mode in api but Schedule in app.')
            elif apimode == "Schedule":
                self.report_pass('Plug is currently in Schedule mode in both api and app.')
            else:
                self.report_fail('Not able to get the Plug mode from api.')
        else:
            self.report_fail('error in getting the current mode of Plugs from the app.')
        self.driver.tap(positions)
        self.report_done('Button for changing mode is clicked')
        time.sleep(5)
        if self.is_element_present(*PlugLocators.PLUG_MANUAL_MODE):
            PlugsPage.afterstate = "Manual"
        elif self.is_element_present(*PlugLocators.PLUG_SCHEDULE_MODE):
            PlugsPage.afterstate = "Schedule"
        else:
            self.report_fail('error in getting the current mode of Plugs from the app.')

    # function to verify the mode of the plugs
    def verify_modechange(self, PlugName):
        time.sleep(10)
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
        if self.is_element_present(*PlugLocators.SCHEDULE_ICON):
            self.report_pass('Schedule icon found')
            self.driver.find_element(*PlugLocators.SCHEDULE_ICON).click()
            self.report_done('Schedule Icon is clicked')
            time.sleep(5)
        else:
            self.report_fail('Schedule icon is not present')

    # function to verify to Plug Schedule Screen
    def verify_schedulescreen(self):
        if self.is_element_present(*PlugLocators.PLUG_SCHEDULE_SCREEN):
            self.report_pass('User is navigated to Schedule Screen.')
        else:
            self.report_fail('User is not navigated to Schedule screen as add image is not found.')

    # function to navigate to Plug Recipe Screen
    def click_recipesicon(self):
        if self.is_element_present(*PlugLocators.RECIPES_ICON):
            self.report_pass('recipes icon found')
            self.driver.find_element(*PlugLocators.RECIPES_ICON).click()
            self.report_done('Recipes Icon is clicked')
            time.sleep(5)

        else:
            self.report_fail('Recipes icon is not present')
            # function to verify to Plug recipe Screen

    def verify_recipesscreen(self):
        if self.is_element_present(*PlugLocators.PLUG_RECIPES_SCREEN):
            self.report_pass('User is navigated to Recipes Screen.')
        else:
            self.report_fail('User is not navigated to recipes screen as text is not found.')

    # function to navigate to the Control page
    def click_controlicon(self):
        if self.is_element_present(*PlugLocators.SCHEDULE_ICON):
            self.driver.find_element(*PlugLocators.SCHEDULE_ICON).click()
            time.sleep(5)
        else:
            self.report_fail('Schedule icon is not present')
        if self.is_element_present(*PlugLocators.CONTROL_ICON):
            self.report_pass('Control icon found')
            self.driver.find_element(*PlugLocators.CONTROL_ICON).click()
            self.report_done('Control Icon is clicked')
            time.sleep(5)

        else:
            self.report_fail('Control icon is not present')

    # function to verify the control screen.
    def verify_controlscreen(self):
        if self.is_element_present(*PlugLocators.PLUG_STATE):
            self.report_pass('User is navigated to control Screen.')
        else:
            self.report_fail('User is not navigated to control screen as arrow button is not found.')


# class for checking menu options..
class MainMenuPage(BasePage):
    # clicks the menu option
    def click_menuicon(self):
        if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_SHOW):
            self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
            self.report_done('Menu Button Icon is clicked')
            time.sleep(5)
        else:
            self.report_fail('Menu Button Icon is not present.')

            # to verify all the menu options in the app.

    def verify_main_menu(self):

        try:
            if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
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
                if self.wait_for_element_exist(*MainMenuLocators.ALLRECIPES_MAIN_MENU):
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
                self.report_fail('IOS-App: The Hive IOS App  is not in Home page.')
        except:

            self.report_fail('IOS-App: Exception in verify_main_menu Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

            # to click the managedevice option

    def click_managedeviceicon(self):
        if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.MANAGEDEVICES_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.MANAGEDEVICES_MAIN_MENU).click()
                self.report_done('Manage Devices Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('Managedevice option is not found')
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on Menu Page.')

            # to verify the managedevice screen

    def click_verify_managedevicescreen(self):
        if 'MANAGE DEVICES' in self.driver.find_element(*MainMenuLocators.MANAGEDEVICE_TITLE).get_attribute(
                'name').upper():
            self.report_pass('App is navigated to Managedevice Screen')
            if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                time.sleep(5)
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on manage device screen')

    # to click the install devices screen
    def click_installdevice(self):
        if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.INSTALLDEVICES_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.INSTALLDEVICES_MAIN_MENU).click()
                self.report_done('Install devices Icon is clicked')
                time.sleep(5)

            else:
                self.report_fail('Install option is not found')
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on Menu Page.')

            # to verify the install device navigation

    def click_verify_installdevicescreen(self):
        if 'INSTALL DEVICES' in self.driver.find_element(*MainMenuLocators.INSTALLDEVICE_TITLE).get_attribute(
                'name').upper():
            self.report_pass('App is navigated to Installdevice Screen')
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on install device screen')

            # to verify the install options..

    def click_verifyoptions_installdevicescreen(self):
        if 'INSTALL DEVICES' in self.driver.find_element(*MainMenuLocators.INSTALLDEVICE_TITLE).get_attribute(
                'name').upper():
            nodes = oAPIValidations.getNodes()
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
            if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                time.sleep(5)
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on install device screen')

            # to click all recepies

    def click_allrecipes(self):
        if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.ALLRECIPES_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.ALLRECIPES_MAIN_MENU).click()
                self.report_done('All Recipes Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('All Recipes Icon is not found')

        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on Menu Page.')

    def verify_allrecepiescreen(self):
        if 'ALL RECIPES' in self.driver.find_element(*MainMenuLocators.ALLRECIPES_TITLE).get_attribute('name').upper():
            self.report_pass('App is navigated to All Recipes Screen')
            if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                time.sleep(5)
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on all recipes screen')

    def click_settings(self):
        if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.SETTINGS_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.SETTINGS_MAIN_MENU).click()
                self.report_done('Setting Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('Setting Icon is not found')
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on Menu Page.')

    def verify_settingsoptions(self):
        if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
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
            if self.wait_for_element_exist(*MainMenuLocators.SETTINGS_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.SETTINGS_MAIN_MENU).click()
                time.sleep(10)
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on Menu Page.')

    def click_help(self):
        if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.is_element_present(*MainMenuLocators.HELP_S__MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.HELP_S__MAIN_MENU).click()
                self.report_done('Help Icon is clicked')
                time.sleep(5)
            else:
                self.report_fail('Help Icon is not found')
        else:
            self.report_fail('IOS-App: The Hive IOS App  is not on Menu Page.')

    def verify_helpoptions(self):
        if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            time.sleep(2)
            if self.wait_for_element_exist(*MainMenuLocators.PRODUCTIDEAS_HELP):
                self.report_pass('Product ideas icon is present')
            else:
                self.report_fail('Product ideas icon is not present.')
            if self.wait_for_element_exist(*MainMenuLocators.HELPIMPROVEHIVE_HELP):
                self.report_pass('Help icon is present')
            else:
                self.report_fail('Help icon is not present.')

            if self.wait_for_element_exist(*MainMenuLocators.SERVICESTATUS_HELP):
                self.report_pass('Service Status icon is present')
            else:
                self.report_fail('Service status icon is not present.')

            nodes = oAPIValidations.getNodes()
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
            if self.wait_for_element_exist(*MainMenuLocators.HELP_S__MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.HELP_S__MAIN_MENU).click()
                time.sleep(5)
        else:
            self.report_fail('IOS-App: The Hive IOS App is not on Menu Page.')

    def click_logout(self):
        if 'MENU' in self.driver.find_element(*MainMenuLocators.MENUPAGE_TITLE).get_attribute('name').upper():
            if self.wait_for_element_exist(*MainMenuLocators.LOGOUT_MAIN_MENU):
                self.driver.find_element(*MainMenuLocators.LOGOUT_MAIN_MENU).click()
                self.report_done('Logout Icon is clicked')
            time.sleep(5)
        else:
            self.report_fail('IOS-App: The Hive IOS App is not on Menu Page.')

    def verify_logout(self):
        if 'LOG IN' in self.driver.find_element(*MainMenuLocators.LOGINPAGE_TITLE).get_attribute('name').upper():
            self.report_pass('IOS-App: The Hive IOS App is successfully Logged out')
        else:
            self.report_fail('IOS-App: The Hive IOS App is not logged out.')


class ActiveLights(BasePage):
    SETTINGS_LOCAL = ""
    VALUE_LOCAL = ""
    SWITCH_ON = 0
    Bulb_Object = ""
    Bulb_Tone_Ring = ""
    Bulb_Brightness_Ring = ""
    Bulb_Colour_Ring = ""
    BULB_MODEL = ""
    BULB_MODE = ""
    BULB_STATUS_DEVICE_LIST = ""
    light_Locator = ""
    light_Offline = ""
    light_Name = ""
    light_Mode = ""

    def updateBulbObjects(self, strDeviceName):
        deviceName = strDeviceName
        BulbName_Local = str(BulbScreenLocators.BULB_NAME)
        ActiveLights.Bulb_Object = BulbName_Local.replace("name", deviceName)
        BulbTone_Local = str(BulbScreenLocators.BULB_TONE)
        ActiveLights.Bulb_Tone_Ring = BulbTone_Local.replace("name", deviceName)
        BulbBrightness_Local = str(BulbScreenLocators.BULB_BRIGHTNESS)
        ActiveLights.Bulb_Brightness_Ring = BulbBrightness_Local.replace("name", deviceName)
        BulbColour_Local = str(BulbScreenLocators.BULB_COLOUR)
        ActiveLights.Bulb_Colour_Ring = BulbColour_Local.replace("name", deviceName)
        ActiveLights.BULB_MODEL = oAPIValidations.getDeviceModel(deviceName)
        BulbMode_local = str(BulbScreenLocators.BULB_MODE)
        ActiveLights.BULB_MODE = BulbMode_local.replace("name", deviceName)
        ActiveLights.light_Name = deviceName
        light_Locator_Local = str(BulbScreenLocators.BULB_LOCATOR)
        ActiveLights.light_Locator = light_Locator_Local.replace("deviceName", deviceName)
        Light_Offline_Local = str(BulbScreenLocators.BULB_OFFLINE)
        ActiveLights.light_Offline = Light_Offline_Local.replace("deviceName", deviceName)
        light_Mode_local = str(BulbScreenLocators.BULB_MODE)
        ActiveLights.light_Mode = light_Mode_local.replace("deviceName", deviceName)

    def navigateToActiveLightControl(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(By.XPATH, ActiveLights.light_Locator):
                    self.driver.find_element(By.XPATH, ActiveLights.light_Locator).click()
                    time.sleep(2)
                    self.report_pass('iOS App : Successfully navigated to the ' + ActiveLights.light_Name + ' screen')
                else:
                    if self.wait_for_element_exist(By.XPATH, BulbScreenLocators.DASHBOARD_HONEYCOMB):
                        self.driver.find_element(By.XPATH, BulbScreenLocators.DASHBOARD_HONEYCOMB).click()
                        time.sleep(2)

                        if self.wait_for_element_exist(By.XPATH, ActiveLights.light_Locator):
                            self.driver.find_element(By.XPATH, ActiveLights.light_Locator).click()
                            time.sleep(2)
                            self.report_pass(
                                'iOS App : Successfully navigated to the ' + ActiveLights.light_Name + ' screen')
                        else:
                            self.report_fail(
                                'iOS App : Couldn\'t navigate to the ' + ActiveLights.light_Name + ' screen')
            except:
                self.report_fail(
                    'iOS App : Exception: in navigateToActiveLightControl Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    # Method to change the ActiveLight mode to Manual/Schedule
    def setActiveLightMode(self, strMode, myStatus=None):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(By.XPATH, ActiveLights.light_Mode):
                    if "MANUAL" in strMode.upper():
                        if self.wait_for_element_exist(*BulbScreenLocators.MANUAL_MODE_LABEL):
                            self.report_pass('iOS App : Active light mode is set to <B>' + strMode)
                        else:
                            self.changeDeviceMode()
                            time.sleep(3)
                            if self.wait_for_element_exist(*BulbScreenLocators.MANUAL_MODE_LABEL):
                                self.report_pass('iOS App : Successfully Active light mode is set to <B>' + strMode)
                    else:
                        if self.wait_for_element_exist(*BulbScreenLocators.SCHEDULE_MODE_LABEL):
                            self.report_pass('iOS App : Active light mode is set to <B>' + strMode)
                        else:
                            self.changeDeviceMode()
                            time.sleep(3)
                            if self.wait_for_element_exist(*BulbScreenLocators.SCHEDULE_MODE_LABEL):
                                self.report_pass('iOS App : Successfully Active light mode is set to <B>' + strMode)
                    if myStatus:
                        self.switchActiveLightMode(myStatus)
                    # Wait time to let the API data refresh
                    time.sleep(25)
                else:
                    self.report_fail("iOS App : Control not active on the Active light Page to set the light Mode")
            except:
                self.report_fail('iOS App : Exception: {0} in setActiveLightMode'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Method to switch ON/OFF the ActiveLight
    def switchActiveLightMode(self, myStatus):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(By.NAME, ActiveLights.Bulb_Object):
                    BULB_STATUS = self.driver.find_element(By.NAME, ActiveLights.Bulb_Object).get_attribute('value')
                    if "ON" in myStatus.upper():
                        if "off" in BULB_STATUS:
                            self.driver.tap([(158, 236)])
                            time.sleep(3)
                            BULB_STATUS = self.driver.find_element(By.NAME, ActiveLights.Bulb_Object).get_attribute(
                                'value')
                            if "ON" in BULB_STATUS.upper():
                                self.report_pass('iOS App : Active light status is successfully set to <B>' + myStatus)
                            else:
                                self.report_fail('iOS App : Active light status couldn\'t be set to <B>' + myStatus)
                        elif "on" in BULB_STATUS:
                            self.report_pass('iOS App : Active light status is set to <B>' + myStatus)
                    elif "OFF" in myStatus.upper():
                        if "on" in BULB_STATUS:
                            self.driver.tap([(158, 236)])
                            time.sleep(3)
                            BULB_STATUS = self.driver.find_element(By.NAME, ActiveLights.Bulb_Object).get_attribute(
                                'value')
                            if "OFF" in BULB_STATUS.upper():
                                self.report_pass('iOS App : Active light mode is successfully set to <B>' + myStatus)
                            else:
                                self.report_fail('iOS App : Active light status couldn\'t be set to <B>' + myStatus)
                        elif "off" in BULB_STATUS:
                            self.report_pass('iOS App : Active light status is set to <B>' + myStatus)
                else:
                    self.report_fail("iOS App : Control not active on the Active light Page to set the light Mode")
            except:
                self.report_fail('iOS App : Exception: {0} in setActiveLightMode'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def changeDeviceMode(self):
        oDeviceMode = self.driver.find_element(By.XPATH, ActiveLights.light_Mode)
        intX = oDeviceMode.location['x']
        intY = oDeviceMode.location['y']
        intHeight = oDeviceMode.size['height']
        intMid = intHeight / 2
        # Co-ordinates to click on the "<" symbol to change the device mode from Manual to Schedule and vice versa
        intCenterX = intX + 25
        intCenterY = intY + intMid
        changeMode = [(intCenterX, intCenterY)]
        self.driver.tap(changeMode)

    def setValues(self, settings, value):
        ActiveLights.SETTINGS_LOCAL = settings
        ActiveLights.VALUE_LOCAL = value

    def navigateToSettings(self, Settings):
        if self.reporter.ActionStatus:
            try:
                BULB_STATUS = self.driver.find_element(By.NAME, ActiveLights.Bulb_Object).get_attribute('value')
                if "off" in BULB_STATUS:
                    self.driver.tap([(158, 236)])
                    ActiveLights.SWITCH_ON = 1
                if "tone" in Settings:
                    if self.wait_for_element_exist(*BulbScreenLocators.COLOUR_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.COLOUR_BUTTON).click()
                    if self.wait_for_element_exist(*BulbScreenLocators.TONE_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.TONE_BUTTON).click()
                    else:
                        print("")
                elif "brightness" in Settings:
                    if self.wait_for_element_exist(*BulbScreenLocators.DIMMER_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.DIMMER_BUTTON).click()
                    else:
                        print("")
                elif "colour" in Settings:
                    if self.wait_for_element_exist(*BulbScreenLocators.TONE_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.TONE_BUTTON).click()
                    if self.wait_for_element_exist(*BulbScreenLocators.COLOUR_BUTTON):
                        self.driver.find_element(*BulbScreenLocators.COLOUR_BUTTON).click()
                    else:
                        print("")
            except:
                self.report_fail('IOS App : Exception in navigateToSettings Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def setValueForBulb(self, settings, verifyValue):
        if self.reporter.ActionStatus:
            try:
                if "BRIGHTNESS" in settings.upper():
                    verifyValue = str(verifyValue) + '%'
                angleStep = 0
                if "tone" in settings:
                    if self.wait_for_element_exist(By.XPATH, ActiveLights.Bulb_Tone_Ring):
                        oBulb = self.driver.find_element(By.XPATH, ActiveLights.Bulb_Tone_Ring)
                        angleStep = 20
                    else:
                        self.report_step('IOS App : Tone settings was not displayed')
                elif "brightness" in settings:
                    if self.wait_for_element_exist(By.XPATH, ActiveLights.Bulb_Brightness_Ring):
                        oBulb = self.driver.find_element(By.XPATH, ActiveLights.Bulb_Brightness_Ring)
                        angleStep = 10
                    else:
                        self.report_step('IOS App : Brightness settings was not displayed')
                elif "colour" in settings:
                    if self.wait_for_element_exist(By.XPATH, ActiveLights.Bulb_Colour_Ring):
                        oBulb = self.driver.find_element(By.XPATH, ActiveLights.Bulb_Colour_Ring)
                        angleStep = 10
                    else:
                        self.report_step('IOS App : Colour settings was not displayed')

                intLeftX = oBulb.location['x']
                intUpperY = oBulb.location['y']
                intSide = oBulb.size['width']
                intSideT = (intSide / 2)
                intCenterX = intLeftX + intSideT
                intCenterY = intUpperY + intSideT
                intRadius = intCenterX - 32
                intTempStartX = intCenterX + intRadius * math.cos(180)
                intTempStartY = intCenterY + intRadius * math.sin(180)

                for angle in range(165, 375, angleStep):
                    intTempNewStartX = intCenterX + intRadius * math.cos(angle * math.pi / 180)
                    intTempNewStartY = intCenterY + intRadius * math.sin(angle * math.pi / 180)
                    intTempNewStartX = int(intTempNewStartX)
                    intTempNewStartY = int(intTempNewStartY)
                    if intTempNewStartY <= 288:
                        self.driver.tap([(intTempNewStartX, intTempNewStartY)])
                        # self.driver.swipe(intTempStartX, intTempStartY, intTempNewStartX, intTempNewStartY)
                        # Wait time to let the API data refresh
                        time.sleep(25)
                    if "tone" in settings:
                        currentValue = self.driver.find_element(By.XPATH, ActiveLights.Bulb_Tone_Ring).get_attribute(
                            'value')
                        if verifyValue in currentValue.upper():
                            time.sleep(2)
                            self.report_pass("iOS App : Active light tone is set to " + currentValue)
                            break
                    elif "brightness" in settings:
                        currentValue = self.driver.find_element(By.XPATH,
                                                                ActiveLights.Bulb_Brightness_Ring).get_attribute(
                            'value')
                        if verifyValue in currentValue:
                            time.sleep(2)
                            self.report_pass("iOS App : Active light brightness is set to " + currentValue)
                            break
                    elif "colour" in settings:
                        currentValue = self.driver.find_element(By.XPATH, ActiveLights.Bulb_Colour_Ring).get_attribute(
                            'value')
                        if verifyValue == currentValue.upper():
                            time.sleep(2)
                            self.report_pass("iOS App : Active light colour is set to " + currentValue)
                            break
            except:
                self.report_fail('IOS App : Exception in setValueForBulb Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # Set Light Schedule
    def set_light_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK):
                    self.driver.find_element(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK).click()
                    time.sleep(1)
                    if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                        print('m here')
                        for oKey in oScheduleDict.keys():
                            self._navigate_to_day(oKey)
                            oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                            self.add_or_remove_events(len(oScheduleList))
                            # Get List of Options & Start Time
                            lstStartTime = self.driver.find_elements(*SchedulePageLocators.EVENT_ARROW)
                            for intCntr in range((len(lstStartTime) - 1), -1, -1):
                                strSetStartTime = oScheduleList[intCntr][0]
                                lightState = oScheduleList[intCntr][1]
                                lightBrightness = oScheduleList[intCntr][2]
                                lstStartTime[intCntr].click()
                                # self.report_done('iOS APP: Event number : ' + str(intCntr + 1) + ' before the event change')
                                print(lightState)
                                if lightState == "OFF":
                                    lightBrightness = 5
                                    light_status = self.driver.find_element(By.XPATH,
                                                                            ActiveLights.light_Locator).get_attribute(
                                        'value')
                                    if light_status == 1:
                                        self.driver.find_element(By.XPATH, ActiveLights.light_Locator).click()
                                elif lightState == "ON":
                                    light_status = self.driver.find_element(By.XPATH,
                                                                            ActiveLights.light_Locator).get_attribute(
                                        'value')
                                    if light_status == 0:
                                        self.driver.find_element(By.XPATH, ActiveLights.light_Locator).click()
                                        # self.set_light_brightness(lightBrightness) #Have issues at the moment with Brightness slider

                                if self.wait_for_element_exist(
                                        *EditTimeSlotPageLocators.HOUR_SCROLL) and self.wait_for_element_exist(
                                    *EditTimeSlotPageLocators.MINUTE_SCROLL):
                                    oHour = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                                    oMinute = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                                    intSetHour = strSetStartTime.split(':')[0]
                                    intSetMin = strSetStartTime.split(':')[1]
                                    intCurrentHour = oHour.get_attribute('value').split(' ')[0]
                                    intCurrentMin = oMinute.get_attribute('value').split(' ')[0]

                                    self.scroll_Date_Hour_Minute(oHour, intCurrentHour, intSetHour, 24, "HOUR")
                                    self.scroll_Date_Hour_Minute(oMinute, intCurrentMin, intSetMin, 60, "MINUTE")
                                # self.report_done('iOS APP: Event number : ' + str(intCntr + 1) + ' after the event change')
                                self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                                # self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)  #Not working while running the tests
                                self.wait_for_element_exist(*SchedulePageLocators.EVENT_ARROW)

                            # self.report_pass('iOS APP: Main Screen after Event number : ' + str(intCntr + 1) + ' is changed')
                            self.report_pass('iOS APP: Main Screen after all Events are changed')
                    if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                        self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        time.sleep(2)
                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Light Schedule Page to set the Light Schedule")
            except:
                self.report_fail('iOS APP: Exception in set_light_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def reset_light_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK):
                    self.driver.find_element(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK).click()
                    time.sleep(1)
                    if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                        print('m here')
                        for oKey in oScheduleDict.keys():
                            self._navigate_to_day(oKey)
                    time.sleep(5)
                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        time.sleep(2)
                        self.report_done("Clicked on + icon successfully")
                        if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESET_SUBMENU).click()
                            time.sleep(2)
                            self.report_done("Clicked on Reset Schedule successfully")
                            if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON):
                                self.driver.find_element(*SchedulePageLocators.SCHEDULE_RESETOK_BUTTON).click()
                                time.sleep(2)
                                self.report_done("Clicked on Reset confirmation pop-up successfully")
                            else:
                                self.report_fail("Couldn\'t find Reset Schedule confirmation pop-up")
                        else:
                            self.report_fail("Couldn\'t find Reset Schedule option")
                    else:
                        self.report_fail("Couldn\'t find + icon on Schedule screen")

                    self.refresh_page()
                    time.sleep(5)
                    if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                        self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        time.sleep(2)
                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Light Schedule Page to reset the Light Schedule")
            except:
                self.report_fail('iOS App : Exception: in reset_light_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def add_light_schedule(self, context, myDeviceName=None):
        if self.reporter.ActionStatus:
            strSetStartTime = str((list(context.oAddSchedule[context.strDay]))[0][0])
            lightState = str((list(context.oAddSchedule[context.strDay]))[0][1])

            try:
                if self.wait_for_element_exist(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK):
                    self.driver.find_element(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK).click()
                    time.sleep(1)

                    self._navigate_to_day(context.strDay)
                    time.sleep(1)
                    # self.reporter.HTML_TC_BusFlowKeyword_Initialize('Add a time slot')
                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        time.sleep(2)
                        self.report_done("Clicked on '+' icon successfully")

                        if self.wait_for_element_exist(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU).click()
                            time.sleep(2)
                            self.report_done("Clicked on 'Add a time slot' option successfully")
                        else:
                            self.report_fail("Couldn\'t find 'Add a time slot' option")
                            exit()

                        if lightState == "OFF":
                            lightBrightness = 5
                            light_status = self.driver.find_element(By.XPATH, ActiveLights.light_Locator).get_attribute(
                                'value')
                            if light_status == 1:
                                self.driver.find_element(By.XPATH, ActiveLights.light_Locator).click()
                        elif lightState == "ON":
                            light_status = self.driver.find_element(By.XPATH, ActiveLights.light_Locator).get_attribute(
                                'value')
                            if light_status == 0:
                                self.driver.find_element(By.XPATH, ActiveLights.light_Locator).click()
                        # self.set_light_brightness(lightBrightness) #Have issues at the moment with Brightness slider
                        if self.wait_for_element_exist(
                                *EditTimeSlotPageLocators.HOUR_SCROLL) and self.wait_for_element_exist(
                            *EditTimeSlotPageLocators.MINUTE_SCROLL):
                            oHour = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                            oMinute = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                            intSetHour = strSetStartTime.split(':')[0]
                            intSetMin = strSetStartTime.split(':')[1]
                            intCurrentHour = oHour.get_attribute('value').split(' ')[0]
                            intCurrentMin = oMinute.get_attribute('value').split(' ')[0]

                            self.scroll_Date_Hour_Minute(oHour, intCurrentHour, intSetHour, 24, "HOUR")
                            self.scroll_Date_Hour_Minute(oMinute, intCurrentMin, intSetMin, 60, "MINUTE")
                        self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                        # self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)  #Not working while running the tests
                        self.wait_for_element_exist(*SchedulePageLocators.EVENT_ARROW)
                    else:
                        self.report_fail("Couldn\'t find '+' icon")

                    if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                        self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        time.sleep(2)
                else:
                    self.report_fail(
                        "iOS APP: Control not active on the Light Schedule Page to reset the Light Schedule")
            except:
                self.report_fail('Android-App : NoSuchElementException: in reset_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def delete_light_schedule(self, context):
        if self.reporter.ActionStatus:
            try:
                strSetStartTime = context.addSlotTime

                if self.wait_for_element_exist(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK):
                    self.driver.find_element(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK).click()
                    time.sleep(1)

                    if context.intEvent > 0:
                        self._navigate_to_day(context.strDay)
                        # self.reporter.HTML_TC_BusFlowKeyword_Initialize('Deleting existing time slot')

                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.EVENT_ARROW)
                        for intCntr in range((len(lstStartTime) - 1), -1, -1):
                            lstStartTime[intCntr].click()
                            time.sleep(2)

                            if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_START_TIME):
                                startTime = self.driver.find_element(
                                    *SchedulePageLocators.SCHEDULE_START_TIME).get_attribute('value')
                                if strSetStartTime in startTime:
                                    if self.wait_for_element_exist(*EditTimeSlotPageLocators.DELETE_EVENT_BUTTON):
                                        self.driver.find_element(*EditTimeSlotPageLocators.DELETE_EVENT_BUTTON).click()
                                        time.sleep(1)
                                        if self.wait_for_element_exist(*EditTimeSlotPageLocators.DELETE_CONFIRM_BUTTON):
                                            self.driver.find_element(
                                                *EditTimeSlotPageLocators.DELETE_CONFIRM_BUTTON).click()
                                            time.sleep(2)

                                        self.report_pass("Below Time slot has been deleted")
                                        strLog = "Event Number $$Event Time @@@" + str(
                                            context.intEvent) + "$$" + context.addSlotTime
                                        self.reporter.ReportEvent('Test Validation', strLog, "DONE", "Center")
                                        time.sleep(2)
                                        break
                                    else:
                                        self.report_fail("Delete option is not found at time slot option menu")
                                else:
                                    if self.wait_for_element_exist(*EditTimeSlotPageLocators.CANCEL_BUTTON):
                                        self.driver.find_element(*EditTimeSlotPageLocators.CANCEL_BUTTON).click()
                                        time.sleep(2)
                    if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                        self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        time.sleep(2)
            except:
                self.report_fail(
                    'iOS App : Exception: in delete_light_schedule Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def copy_light_schedule(self, strToDay, strFromDay):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK):
                    self.driver.find_element(*BulbScreenLocators.EDIT_SCHEDULE_MODE_LINK).click()
                    time.sleep(1)

                    self._navigate_to_day(strFromDay)
                    time.sleep(5)

                    if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                        self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                        time.sleep(2)
                        self.report_done("'+' Icon is found and clicked successfully")

                        if self.wait_for_element_exist(*SchedulePageLocators.COPY_SCHEDULE_SUBMENU):
                            self.driver.find_element(*SchedulePageLocators.COPY_SCHEDULE_SUBMENU).click()
                            time.sleep(2)
                            self.report_done("Copy schedule Icon is found and clicked successfully")

                            day = (calendar.day_name[oSchedUtils.oWeekDayList.index(strToDay)])

                            strToDayElement = SchedulePageLocators.DAY_COPY_SCHEDULE.replace("day", day)

                            if self.wait_for_element_exist(By.XPATH, strToDayElement):
                                self.driver.find_element(By.XPATH, strToDayElement).click()
                                time.sleep(2)
                                self.report_done("The given day is found and clicked successfully")
                                if self.wait_for_element_exist(*EditTimeSlotPageLocators.SAVE_BUTTON):
                                    self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()
                                    time.sleep(2)
                                    self.report_done("Save OK Button is found and clicked successfully")
                                else:
                                    self.report_fail("Save OK Button couldn\'t be found on schedule screen")
                            else:
                                self.report_fail(
                                    "The given day, " + day + " couldn\'t be found on Schedule screen")
                        else:
                            self.report_fail("Couldn\'t find copy schedule on Schedule screen")
                    else:
                        self.report_fail("Couldn\'t find '+' icon on schedule screen")

                    if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                        self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        time.sleep(2)

            except:
                self.report_fail('iOS App : Exception: in copy_light_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_light_brightness(self, myBrightness):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*BulbScreenLocators.LIGHT_SCHEDULE_BRIGHTNESS):
                    oBrightness = self.driver.find_element(*BulbScreenLocators.LIGHT_SCHEDULE_BRIGHTNESS)
                    currentBrightness = self.driver.find_element(
                        *BulbScreenLocators.LIGHT_SCHEDULE_BRIGHTNESS).get_attribute('value')
                    intCurrentBrightness = currentBrightness.replace("%", "")
                    intWidth = oBrightness.size['width']
                    intHeight = oBrightness.size['height']
                    intStartX = ""
                    intStartY = (int(oBrightness.location['y']) + (intHeight / 2))
                    intEndX = ""
                    intEndY = intStartY
                    intGapBrightness = (intWidth / 10)
                    intSwipeCount = (myBrightness / 10)

                    if intCurrentBrightness == str(myBrightness):
                        print("Current Brightness is same as desired.")
                    else:
                        if ("5%" in currentBrightness) | (int(myBrightness) > int(intCurrentBrightness)):
                            intCnt = 0
                            intStartX = oBrightness.location['x']
                            while intCnt < 10:
                                intNewStartX = round((intStartX + (intGapBrightness * intCnt)), 1)
                                intEndX = round((intStartX + (intGapBrightness * (intCnt + 1))), 1)
                                print("StartX : " + str(intNewStartX) + "   StartY : " + str(
                                    intStartY) + "  EndX :" + str(intEndX) + "   EndY :" + str(intEndY))
                                self.driver.swipe(intNewStartX, intStartY, intEndX, intEndY)
                                time.sleep(1)
                                brightness = self.driver.find_element(
                                    *BulbScreenLocators.LIGHT_SCHEDULE_BRIGHTNESS).get_attribute('value')
                                intBrightness = brightness.replace("%", "")
                                if str(intBrightness) == str(myBrightness):
                                    break
                                intCnt = intCnt + 1
                        elif ("100%" in currentBrightness) | (int(myBrightness) < int(intCurrentBrightness)):
                            intCnt = 0
                            intX = oBrightness.location['x']
                            intStartX = (intX + intWidth)
                            while intCnt < 10:
                                intNewStartX = round((intStartX - (intGapBrightness * intCnt)), 1)
                                intEndX = round((intStartX - (intGapBrightness * (intCnt + 1))), 1)
                                print("StartX : " + str(intNewStartX) + "   StartY : " + str(
                                    intStartY) + "  EndX :" + str(intEndX) + "   EndY :" + str(intEndY))
                                self.driver.swipe(intNewStartX, intStartY, intEndX, intEndY)
                                time.sleep(1)
                                brightness = self.driver.find_element(
                                    *BulbScreenLocators.LIGHT_SCHEDULE_BRIGHTNESS).get_attribute('value')
                                intBrightness = brightness.replace("%", "")
                                if str(intBrightness) == str(myBrightness):
                                    break
                                intCnt = intCnt + 1

                else:
                    self.report_fail("iOS APP: Control not active on the Light Schedule Page to set the Light Schedule")
            except:
                self.report_fail('iOS APP: Exception in set_light_brightness Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class LeakSensor(BasePage):
    CURRENT_LEAK_STATUS = ""
    LEAK_MODEL = ""

    def navigate_to_device_updated(self, strDeviceName):
        try:
            device_found = 0
            if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
            if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_DEVICE_LIST):
                self.driver.find_element(*HomePageLocators.FLIP_TO_DEVICE_LIST).click()
            Device_Name = str(HomePageLocators.DEVICE_NAME)
            deviceObject = Device_Name.replace("name", strDeviceName)

            if self.is_element_present(By.XPATH, deviceObject):
                self.driver.find_element(By.XPATH, deviceObject).click()
                device_found = 1
                time.sleep(5)
                if self.is_element_present(*DashboardPageLocators.TAB_BAR_CONTROL_BUTTON):
                    self.report_pass('IOS App : Navigated to device ' + strDeviceName + ' screen')
                    device_found = 0
                elif device_found == 1:
                    # try scrolling and checking again before failing
                    self.driver.execute_script("mobile: scroll", {"direction": "down"})
                    if self.is_element_present(By.XPATH, deviceObject):
                        self.driver.find_element(By.XPATH, deviceObject).click()
                        device_found = 1
                        time.sleep(5)
                        if self.is_element_present(*DashboardPageLocators.TAB_BAR_CONTROL_BUTTON):
                            self.report_pass('IOS App : Navigated to device ' + strDeviceName + ' screen')
                            device_found = 0
                        else:
                            self.report_fail('IOS App : Navigation to device ' + strDeviceName + ' screen failed')
                    else:
                        self.report_fail('IOS App : Navigation to device ' + strDeviceName + ' screen failed')
        except:
            self.report_fail(
                'iOS App : NoSuchElementException: in function navigate_to_device_updated \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def getDeviceModel(self, strDeviceName):
        LeakSensor.LEAK_MODEL = oAPIValidations.getDeviceModel(strDeviceName)

    def setAlertSettings(self, oTargetDict):
        if self.reporter.ActionStatus:
            try:

                if self.wait_for_element_exist(*LeakSensorPageLocators.SETTINGS_BUTTON):
                    self.driver.find_element(*LeakSensorPageLocators.SETTINGS_BUTTON).click()
                    if self.wait_for_element_exist(*LeakSensorPageLocators.ALERT_NOTIFICATION):
                        self.driver.find_element(*LeakSensorPageLocators.ALERT_NOTIFICATION).click()
                        time.sleep(3)
                        self.report_pass('IOS App : Navigation to notifications settings screen was successful')
                        Push_Value = self.driver.find_element(
                            *LeakSensorPageLocators.PUSH_NOTIFICATION_STATUS).get_attribute('name')
                        Mail_Value = self.driver.find_element(*LeakSensorPageLocators.EMAIL_STATUS).get_attribute(
                            'name')
                        Text_Value = self.driver.find_element(*LeakSensorPageLocators.TEXT_STATUS).get_attribute('name')

                        # check if the settings is contradicting and click the button else ignore
                        if (oTargetDict['PushNotification'] == 'Active') & ('off' in Push_Value):
                            self.driver.find_element(*LeakSensorPageLocators.PUSH_NOTIFICATION_BUTTON).click()
                            self.report_done('IOS App : Push notification is set for the sensor')
                        if (oTargetDict['PushNotification'] == 'Inactive') & ('on' in Push_Value):
                            self.driver.find_element(*LeakSensorPageLocators.PUSH_NOTIFICATION_BUTTON).click()
                            self.report_done('IOS App : Push notification is turned off for the sensor')

                        if (oTargetDict['SendSubscriptionSMS'] == 'Active') & ('off' in Text_Value):
                            self.driver.find_element(*LeakSensorPageLocators.TEXT_BUTTON).click()
                            self.report_done('IOS App : Text notification is set for the sensor')
                        if (oTargetDict['SendSubscriptionSMS'] == 'Inactive') & ('on' in Text_Value):
                            self.driver.find_element(*LeakSensorPageLocators.TEXT_BUTTON).click()
                            self.report_done('IOS App : Text notification is turned off for the sensor')

                        if (oTargetDict['SendEmail'] == 'Active') & ('off' in Mail_Value):
                            self.driver.find_element(*LeakSensorPageLocators.EMAIL_BUTTON).click()
                            self.report_done('IOS App : Mail notification is set for the sensor')
                        if (oTargetDict['SendEmail'] == 'Inactive') & ('on' in Mail_Value):
                            self.driver.find_element(*LeakSensorPageLocators.EMAIL_BUTTON).click()
                            self.report_done('IOS App : Mail notification is turned off for the sensor')

                        if self.wait_for_element_exist(*LeakSensorPageLocators.SAVE_BUTTON):
                            self.driver.find_element(*LeakSensorPageLocators.SAVE_BUTTON).click()
                        time.sleep(5)
                        if self.wait_for_element_exist(*LeakSensorPageLocators.BACK_BUTTON):
                            self.driver.find_element(*LeakSensorPageLocators.BACK_BUTTON).click()
                        if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                            self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        self.driver.execute_script("mobile: scroll", {"direction": "up"})
                        time.sleep(3)
                    else:
                        self.report_fail('IOS App : Navigation to notifications settings screen failed')
            except:
                self.report_fail(
                    'iOS App : NoSuchElementException: in function fetchCurrentAlertSettings \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def fetchCurrentAlertSettings(self):
        if self.reporter.ActionStatus:
            try:
                strPushStatus, strEmailStatus, strTextStatus = 'INACTIVE', 'INACTIVE', 'INACTIVE'
                if self.wait_for_element_exist(*LeakSensorPageLocators.SETTINGS_BUTTON):
                    self.driver.find_element(*LeakSensorPageLocators.SETTINGS_BUTTON).click()
                    if self.wait_for_element_exist(*LeakSensorPageLocators.ALERT_NOTIFICATION):
                        self.driver.find_element(*LeakSensorPageLocators.ALERT_NOTIFICATION).click()
                        time.sleep(3)
                        self.report_pass('IOS App : Navigation to notifications settings screen was successful')
                        Push_Value = self.driver.find_element(
                            *LeakSensorPageLocators.PUSH_NOTIFICATION_STATUS).get_attribute('name')
                        Mail_Value = self.driver.find_element(*LeakSensorPageLocators.EMAIL_STATUS).get_attribute(
                            'name')
                        Text_Value = self.driver.find_element(*LeakSensorPageLocators.TEXT_STATUS).get_attribute('name')
                        if 'on' in Push_Value:
                            strPushStatus = 'ACTIVE'
                            self.report_done('IOS App : Push notification is set for the sensor')
                        if 'on' in Mail_Value:
                            strEmailStatus = 'ACTIVE'
                            self.report_done('IOS App : Mail notification is set for the sensor')
                        if 'on' in Text_Value:
                            strTextStatus = 'ACTIVE'
                            self.report_done('IOS App : Text notification is set for the sensor')
                        if self.wait_for_element_exist(*LeakSensorPageLocators.BACK_BUTTON):
                            self.driver.find_element(*LeakSensorPageLocators.BACK_BUTTON).click()
                        if self.wait_for_element_exist(*LeakSensorPageLocators.BACK_BUTTON):
                            self.driver.find_element(*LeakSensorPageLocators.BACK_BUTTON).click()
                    else:
                        self.report_fail('IOS App : Navigation to notifications settings screen failed')
                return {'SendSubscriptionSMS': strTextStatus, 'SendEmail': strEmailStatus,
                        'PushNotification': strPushStatus}
            except:
                self.report_fail(
                    'iOS App : NoSuchElementException: in function fetchCurrentAlertSettings \n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def setMinLeakDuration(self, strTarget):
        try:
            if self.wait_for_element_exist(*LeakSensorPageLocators.SETTINGS_BUTTON):
                self.driver.find_element(*LeakSensorPageLocators.SETTINGS_BUTTON).click()
                if self.wait_for_element_exist(*LeakSensorPageLocators.LARGE_FLOW_ALERT):
                    self.driver.find_element(*LeakSensorPageLocators.LARGE_FLOW_ALERT).click()
                    if self.wait_for_element_exist(*LeakSensorPageLocators.THRESHOLD_TIME):
                        self.driver.find_element(*LeakSensorPageLocators.THRESHOLD_TIME).click()
                        self.driver.tap([(190, 300)])
                        self.driver.tap([(190, 300)])
                        if "20" in strTarget:
                            self.driver.tap([(190, 370)])
                        elif "25" in strTarget:
                            self.driver.tap([(190, 370)])
                            self.driver.tap([(190, 370)])
                        self.driver.find_element(*LeakSensorPageLocators.DONE_BUTTON).click()
                        if self.wait_for_element_exist(*LeakSensorPageLocators.CONFIRM_BUTTON):
                            self.driver.find_element(*LeakSensorPageLocators.CONFIRM_BUTTON).click()
                        if self.wait_for_element_exist(*LeakSensorPageLocators.SAVE_BUTTON):
                            self.driver.find_element(*LeakSensorPageLocators.SAVE_BUTTON).click()
                            time.sleep(5)
                        self.report_pass(
                            'IOS App : The threshold time limit has been updated to ' + strTarget + ' mins')
        except:
            self.report_fail(
                'iOS App : NoSuchElementException: in function setMinLeakDuration \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def fetchMinLeakDuration(self):
        try:
            if self.wait_for_element_exist(*LeakSensorPageLocators.SETTINGS_BUTTON):
                self.driver.find_element(*LeakSensorPageLocators.SETTINGS_BUTTON).click()
                if self.wait_for_element_exist(*LeakSensorPageLocators.LARGE_FLOW_ALERT):
                    self.driver.find_element(*LeakSensorPageLocators.LARGE_FLOW_ALERT).click()
                    strMin = self.driver.find_element(*LeakSensorPageLocators.THRESHOLD_TIME).get_attribute('name')
                    self.report_pass('IOS App : Current threshold limit is set as ' + strMin)
                    if self.wait_for_element_exist(*LeakSensorPageLocators.BACK_BUTTON):
                        self.driver.find_element(*LeakSensorPageLocators.BACK_BUTTON).click()
                    if self.wait_for_element_exist(*LeakSensorPageLocators.BACK_BUTTON):
                        self.driver.find_element(*LeakSensorPageLocators.BACK_BUTTON).click()
                    strMin = strMin[:2]
                    return strMin
                else:
                    self.report_fail('IOS App : Navigation to large flow alert screen failed')
            else:
                self.report_fail('IOS App : Navigation to Settings screen failed')


        except:
            self.report_fail(
                'iOS App : NoSuchElementException: in function fetchMinLeakDuration \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def getLeakStatus(self):
        if self.reporter.ActionStatus:
            try:
                strStatus = ''
                strResult = ""
                LeakSensor.CURRENT_LEAK_STATUS = "NONE"
                blnCalibrationAt = False
                self.driver.execute_script("mobile: scroll", {"direction": "up"})
                if self.is_element_present(*LeakSensorPageLocators.CALIBRATING_SCREEN):
                    blnCalibrationAt = True
                    strResult = strResult + "The leak sensor is in calibration mode."
                if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                    if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_DEVICE_LIST):
                        self.driver.find_element(*HomePageLocators.FLIP_TO_DEVICE_LIST).click()
                    if self.is_element_present(*LeakSensorPageLocators.LARGE_FLOW_ALERT):
                        LeakSensor.CURRENT_LEAK_STATUS = "Large water flow alert"
                        strResult = strResult + "The current leak status is High"
                    elif self.is_element_present(*LeakSensorPageLocators.SMALL_FLOW_ALERT):
                        LeakSensor.CURRENT_LEAK_STATUS = "Small water flow alert"
                        strResult = strResult + "The current leak status is Low"
                    elif self.is_element_present(*LeakSensorPageLocators.NORMAL_FLOW):
                        LeakSensor.CURRENT_LEAK_STATUS = "All OK"
                        strResult = strResult + "The current leak status is Normal"
                    self.report_pass('IOS App : ' + strResult)
                else:
                    self.report_fail('IOS App : Retreiveing of leak status failed')
                strStatus = LeakSensor.CURRENT_LEAK_STATUS
                return strStatus, blnCalibrationAt
            except:
                self.report_fail('IOS App : NoSuchElementException: in getLeakStatus Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verifyLeakStatus(self, leakStatus):
        if self.reporter.ActionStatus:
            try:
                if (LeakSensor.CURRENT_LEAK_STATUS == "NONE") & (leakStatus == "NONE"):
                    self.report_pass('IOS App : There is normal flow recorded in the API')
                elif (LeakSensor.CURRENT_LEAK_STATUS == "LOW") & (leakStatus == "LOW"):
                    self.report_pass('IOS App : There is small flow alert recorded in the API')
                elif (LeakSensor.CURRENT_LEAK_STATUS == "HIGH") & (leakStatus == "HIGH"):
                    self.report_pass('IOS App : There is large flow alert recorded in the API')
            except:
                self.report_fail('IOS App : NoSuchElementException: in verifyLeakStatus Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def getBatteryStatus(self):
        if self.reporter.ActionStatus:
            try:
                if self.is_element_present(*LeakSensorPageLocators.NORMAL_BATTERY):
                    self.report_pass('IOS App : The battery status of the leak sensor is normal')
                    LeakSensor.CURRENT_LEAK_STATUS = "NORMAL"
                elif self.is_element_present(*LeakSensorPageLocators.LOW_BATTERY):
                    self.report_pass('IOS App : The battery status of the leak sensor is low or empty')
                    LeakSensor.CURRENT_LEAK_STATUS = "LOW"
                elif self.is_element_present(*LeakSensorPageLocators.FULL_BATTERY):
                    self.report_pass('IOS App : The battery status of the leak sensor is full')
                    LeakSensor.CURRENT_LEAK_STATUS = "FULL"
            except:
                self.report_fail('IOS App : NoSuchElementException: in getBatteryStatus Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
                self.report_fail('IOS App : NoSuchElementException: in getBatteryStatus Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verifyBatteryStatus(self):
        if self.reporter.ActionStatus:
            try:
                nodeID = oAPIValidations.getDeviceID(LeakSensor.LEAK_MODEL)
                verifyValue = oAPIValidations.getLeakSensorValues(nodeID, "Battery")
                if (LeakSensor.CURRENT_LEAK_STATUS == "NORMAL") & (verifyValue == "NORMAL"):
                    self.report_pass('IOS App : Battery state of the sensor is set as normal in the API')
                elif (LeakSensor.CURRENT_LEAK_STATUS == "LOW") & (verifyValue == "LOW"):
                    self.report_pass('IOS App : Battery state of the sensor is set as low in the API')
                elif (LeakSensor.CURRENT_LEAK_STATUS == "LOW") & (verifyValue == "EMPTY"):
                    self.report_pass('IOS App : Battery state of the sensor is set as empty in the API')
                elif (LeakSensor.CURRENT_LEAK_STATUS == "FULL") & (verifyValue == "FULL"):
                    self.report_pass('IOS App : Battery state of the sensor is set as full in the API')
            except:
                self.report_fail('IOS App : NoSuchElementException: in verifyBatteryStatus Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def largeFlowTroubleShooting(self):
        if self.reporter.ActionStatus:
            try:

                if self.is_element_present(*LeakSensorPageLocators.FLOW_YES):
                    self.driver.find_element(*LeakSensorPageLocators.
                                             FLOW_YES).click()
                    if self.is_element_present(*LeakSensorPageLocators.LARGE_FLOW_CONTINUOUS_ALERT):
                        self.report_pass(
                            'IOS App : The user was able to resolve the leak and additional notification will be sent if there is continuous leak')
                        self.driver.swipe(200, 500, 200, 200, 500)
                        time.sleep(2)
                        if self.is_element_present(*LeakSensorPageLocators.FLOW_NO):
                            self.driver.find_element(*LeakSensorPageLocators.FLOW_NO).click()
                            if self.is_element_present(*LeakSensorPageLocators.CALL_HIVE):
                                self.report_pass('IOS App : The Call Hive button was displayed as expected')
                                # Call Hive disabled for trial - below code to be uncommented once launched
                                # self.driver.find_element(*LeakSensorPageLocators.CALL_HIVE).click()
                                # if (self.is_element_present(*LeakSensorPageLocators.CANCEL_BUTTON)):
                                #    self.report_pass('IOS App : The user was not able to resolve the leak so they can book a job to resolve the issue')
                                #    time.sleep(2)
                                #    self.driver.find_element(*LeakSensorPageLocators.CANCEL_BUTTON).click()
                                #    self.report_pass('IOS App : Large flow troubleshooting screens were as expected in the App.')
                                # else:
                                #    self.report_fail('IOS App : The support number was not displayed as expected')
                            else:
                                self.report_fail('IOS App : The Call Hive button was not displayed as expected')
                        else:
                            self.report_fail('IOS App : The No option was not displayed as expected')
                    else:
                        self.report_fail('IOS App : The continuous alert was not displayed as expected')
                else:
                    self.report_fail('IOS App : The Yes option was not displayed as expected')
            except:
                self.report_fail('IOS App : NoSuchElementException: in largeFlowTroubleShooting Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def smallFlowTroubleShooting(self):
        if self.reporter.ActionStatus:
            try:
                # Job booking when not able to find the problem
                if self.is_element_present(*LeakSensorPageLocators.SMALL_FLOW_OK):
                    self.driver.find_element(*LeakSensorPageLocators.SMALL_FLOW_OK).click()
                    if self.is_element_present(*LeakSensorPageLocators.FLOW_NO):
                        # TouchAction(self.driver).press(None, 200, 100).wait(1000).move_to(None, 200,600).release().perform()
                        self.driver.execute_script("mobile: scroll", {"direction": "down"})
                        self.driver.find_element(*LeakSensorPageLocators.FLOW_NO).click()
                        time.sleep(2)
                        if self.is_element_present(*LeakSensorPageLocators.CALL_HIVE):
                            self.report_pass(
                                'IOS App : The Call Hive button was displayed as disabled - call validations commented until launch')
                        # Call Hive disabled for trial - below code to be uncommented once launched
                        #    self.driver.find_element(*LeakSensorPageLocators.CALL_HIVE).click()
                        #    if (self.is_element_present(*LeakSensorPageLocators.CANCEL_BUTTON)):
                        #        self.report_pass('IOS App : The user was not able to find the problem so they can book a job to resolve the issue')
                        #        time.sleep(2)
                        #        self.driver.find_element(*LeakSensorPageLocators.CANCEL_BUTTON).click()
                        #    else:
                        #        self.report_fail('IOS App : The support number was not displayed as expected')
                        else:
                            self.report_fail('IOS App : The Call Hive button was not displayed as expected')
                    else:
                        self.report_fail('IOS App : The No option was not displayed as expected')

                    # Job booking when the user is not able to resolve the leak
                    self.driver.swipe(200, 500, 200, 200, 500)
                    if self.is_element_present(*LeakSensorPageLocators.SMALL_FLOW_OK):
                        self.driver.find_element(*LeakSensorPageLocators.SMALL_FLOW_OK).click()
                        if self.is_element_present(*LeakSensorPageLocators.FLOW_YES):
                            self.driver.execute_script("mobile: scroll", {"direction": "down"})
                            self.driver.find_element(*LeakSensorPageLocators.FLOW_YES).click()
                            time.sleep(2)
                            if self.is_element_present(*LeakSensorPageLocators.POPUP_NO):
                                self.driver.find_element(*LeakSensorPageLocators.POPUP_NO).click()
                                time.sleep(2)
                                if self.is_element_present(*LeakSensorPageLocators.CALL_HIVE):
                                    self.report_pass(
                                        'IOS App : The Call Hive button was displayed as disabled - call validations commented until launch')
                                    # Call Hive disabled for trial - below code to be uncommented once launched
                                    # self.driver.find_element(*LeakSensorPageLocators.CALL_HIVE).click()
                                    # if (self.is_element_present(*LeakSensorPageLocators.CANCEL_BUTTON)):
                                    #    self.report_pass('IOS App : The user was not able to resolve the leak so they can book a job to resolve the issue')
                                    #    time.sleep(2)
                                    #    self.driver.find_element(*LeakSensorPageLocators.CANCEL_BUTTON).click()
                                    # else:
                                    #    self.report_fail('IOS App : The support number was not displayed as expected')
                                else:
                                    self.report_fail('IOS App : The Call Hive button was not displayed as expected')
                            else:
                                self.report_fail('IOS App : The No button was not displayed as expected')
                        else:
                            self.report_fail('IOS App : The No option was not displayed as expected')

                    # User resolves leak successfully
                    self.driver.swipe(200, 500, 200, 200, 500)
                    if self.is_element_present(*LeakSensorPageLocators.SMALL_FLOW_OK):
                        self.driver.find_element(*LeakSensorPageLocators.SMALL_FLOW_OK).click()
                        if self.is_element_present(*LeakSensorPageLocators.FLOW_YES):
                            self.driver.execute_script("mobile: scroll", {"direction": "down"})
                            self.driver.find_element(*LeakSensorPageLocators.FLOW_YES).click()
                            time.sleep(2)
                            if self.is_element_present(*LeakSensorPageLocators.POPUP_YES):
                                self.driver.find_element(*LeakSensorPageLocators.POPUP_YES).click()
                                time.sleep(2)
                                if self.is_element_present(*LeakSensorPageLocators.SMALL_FLOW_REFRESH):
                                    self.driver.find_element(*LeakSensorPageLocators.SMALL_FLOW_REFRESH).click()
                                    self.report_pass(
                                        'IOS App : The user was able to resolve the leak and the sensor is calibrating for the state to be updated')
                                else:
                                    self.report_fail('IOS App : The Call Hive button was not displayed as expected')
                            else:
                                self.report_fail('IOS App : The No button was not displayed as expected')
                        else:
                            self.report_fail('IOS App : The No option was not displayed as expected')
                    else:
                        self.report_fail('IOS App : The small flow alert was not displayed as expected')
            except:
                self.report_fail('IOS App : NoSuchElementException: in smallFlowTroubleShooting Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def verifyTroubleShootingScreens(self):
        if self.reporter.ActionStatus:
            try:
                if LeakSensor.CURRENT_LEAK_STATUS == "LOW":
                    LeakSensor.smallFlowTroubleShooting(self)
                elif LeakSensor.CURRENT_LEAK_STATUS == "HIGH":
                    LeakSensor.largeFlowTroubleShooting(self)
            except:
                self.report_fail(
                    'IOS App : NoSuchElementException: in verifyTroubleShootingScreens Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


class HoneyComb(BasePage):
    def honeycomb_verifyscreen(self):
        if self.is_element_present(*PlugLocators.DEVICELIST_ICON):
            if not self.is_element_present(*HomePageLocators.DASHBOARD_TITLE):
                self.driver.find_element(*PlugLocators.DEVICELIST_ICON).click()
                time.sleep(2)
                if self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                    self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                    time.sleep(2)
                    if not self.is_element_present(*HomePageLocators.DASHBOARD_TITLE):
                        self.report_fail('Dashboard Screen Label is not found')
                else:
                    self.report_fail('Dashboard Icon not found')
        elif self.is_element_present(*PlugLocators.DASHBOARD_ICON):
            self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            time.sleep(2)
            if not self.is_element_present(*HomePageLocators.DASHBOARD_TITLE):
                self.report_fail('Dashboard Screen Label is not found')

        else:
            self.report_fail('Error in getting the device and dashboard locators.')

    def devicelist_verifyscreen(self):
        if self.is_element_present(*PlugLocators.DASHBOARD_ICON):
            if not self.is_element_present(*HomePageLocators.DASHBOARD_TITLE):
                self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                time.sleep(2)
                if self.wait_for_element_exist(*PlugLocators.DEVICELIST_ICON):
                    self.driver.find_element(*PlugLocators.DEVICELIST_ICON).click()
                    time.sleep(2)
                    if not self.is_element_present(*HomePageLocators.DASHBOARD_TITLE):
                        self.report_fail('Device Screen Label is not found')
                else:
                    self.report_fail('Device Icon not found')
        elif self.is_element_present(*PlugLocators.DEVICELIST_ICON):
            self.driver.find_element(*PlugLocators.DEVICELIST_ICON).click()
            time.sleep(2)
            if not self.is_element_present(*HomePageLocators.DASHBOARD_TITLE):
                self.report_fail('Device Screen Label is not found')

        else:
            self.report_fail('Error in getting the device and dashboard locators.')

    def honeycomb_verify_Title(self):
        if 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute(
                'name').upper():
            self.report_pass('Title is displayed as expected')

        else:
            self.report_fail('Title is not displayed as expected or not found')
        self.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating the refresh functionality')
        self.refresh_page()
        time.sleep(2)
        title = self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute('name').upper()
        if 'LAST UPDATED: JUST NOW' in title:
            self.report_pass('Last Updated Time is updating after refresh')
        elif 'LAST UPDATED: ' and 'SECONDS AGO' in title:
            self.report_pass('Last Updated Time is updating after refresh')
        else:
            self.report_fail('Last updated Time is not updating after refresh')

        time.sleep(85)
        title = self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute('name').upper()
        if 'MINUTE AGO' in title:
            self.report_pass('Last Updated Time is updating without refresh')
        else:
            self.report_fail('Last updated Time is not updating without refresh')

    def navigation_to_screen(self, strScreenName):
        self.honeycomb_verifyscreen()
        if strScreenName == "Heating":
            if self.is_element_present(*HomePageLocators.HEATING_LOC):
                self.driver.find_element(*HomePageLocators.HEATING_LOC).click()
                time.sleep(2)
            else:
                self.report_fail('Heating Location is not found.')
        else:
            MainMenuPage.click_menuicon(self)
            if strScreenName == "Manage devices":
                MainMenuPage.click_managedeviceicon(self)
            elif strScreenName == "Install devices":
                MainMenuPage.click_installdevice(self)
            elif strScreenName == "All Recipes":
                MainMenuPage.click_allrecipes(self)
            elif strScreenName == "Geolocation":
                MainMenuPage.click_settings(self)
                if self.wait_for_element_exist(*MainMenuLocators.GEOLOCATION_SETTINGS):
                    self.driver.find_element(*MainMenuLocators.GEOLOCATION_SETTINGS).click()
                else:
                    self.report_fail('Geolocation is not present')
            elif strScreenName == "Holiday mode":
                if self.wait_for_element_exist(*MainMenuLocators.HOLIDAYMODE_SETTINGS):
                    self.driver.find_element(*MainMenuLocators.HOLIDAYMODE_SETTINGS).click()
                else:
                    MainMenuPage.click_settings(self)
                    if self.wait_for_element_exist(*MainMenuLocators.HOLIDAYMODE_SETTINGS):
                        self.driver.find_element(*MainMenuLocators.HOLIDAYMODE_SETTINGS).click()
                    else:
                        self.report_fail('Holiday mode is not present')

        if self.is_element_present(*PlugLocators.DASHBOARD_ICON):
            self.report_pass('Dashboard icon is present in ' + strScreenName + ' Screen')
            self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
            time.sleep(2)
            if 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute(
                    'name').upper():
                self.report_pass('User is able to reach the Dashboard after clicking the icon.')
            else:
                self.report_fail('User is not in Dashboard screen after clicking the icon.')

        else:
            self.report_fail('Dashboard Icon is not found in ' + strScreenName + ' Screen')

    def getdevicecount(self):
        nodes = oAPIValidations.getNodes()
        thermostatcount = 0
        blnFlag = False
        strDeviceName = ""
        strDeviceState = ""
        strDeviceText = ""
        listDevice = []
        hub = ""
        for oNode in nodes['nodes']:
            if 'nodeType' in oNode.keys() and not 'synthetic.rule' in oNode['name']:
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.thermostatui.json#':
                    thermostatcount += 1
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.hub.json#':
                    hub = oNode["attributes"]["hardwareVersion"]["reportedValue"]

        for oNode in nodes['nodes']:
            if 'nodeType' in oNode.keys() and not 'synthetic.rule' in oNode['name']:
                strDeviceName = oNode['name']
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.smartplug.json#':
                    strDeviceText = "NONE"
                    blnFlag = True
                    strDeviceState = oNode["attributes"]["presence"]["reportedValue"]
                    if strDeviceState.upper() == 'ABSENT':
                        strDeviceState = "offline"
                    else:
                        strDeviceState = oNode["attributes"]["state"]["reportedValue"]
                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.motion.sensor.json#':
                    blnFlag = True
                    strDeviceState = oNode["attributes"]["presence"]["reportedValue"]
                    if strDeviceState.upper() == 'ABSENT':
                        strDeviceState = "offline"
                    else:
                        blnDeviceState = oNode["attributes"]["inMotion"]["reportedValue"]
                        strDeviceText = "Last detected"
                        if blnDeviceState:
                            strDeviceState = "on"
                        else:
                            strDeviceState = "off"
                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.contact.sensor.json#':
                    blnFlag = True
                    strDeviceState = oNode["attributes"]["presence"]["reportedValue"]
                    if strDeviceState == 'ABSENT':
                        strDeviceState = "offline"
                    else:
                        if oNode["attributes"]["state"]["reportedValue"] == 'CLOSED':
                            strDeviceState = "off"
                            strDeviceText = "Last closed"

                        else:
                            strDeviceState = "on"
                            strDeviceText = "Last Opened"
                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.light.json#':
                    blnFlag = True
                    strDeviceText = "NONE"
                    strDeviceState = oNode["attributes"]["presence"]["reportedValue"]
                    if strDeviceState.upper() == 'ABSENT':
                        strDeviceState = "offline"
                    else:
                        strDeviceState = oNode["attributes"]["state"]["reportedValue"]
                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.tunable.light.json#':
                    blnFlag = True
                    strDeviceText = "NONE"
                    strDeviceState = oNode["attributes"]["presence"]["reportedValue"]
                    if strDeviceState.upper() == 'ABSENT':
                        strDeviceState = "offline"
                    else:
                        strDeviceState = oNode["attributes"]["state"]["reportedValue"]
                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.colour.tunable.light.json#':
                    blnFlag = True
                    strDeviceText = "NONE"
                    strDeviceState = oNode["attributes"]["presence"]["reportedValue"]
                    if strDeviceState.upper() == 'ABSENT':
                        strDeviceState = "offline"
                    else:
                        strDeviceState = oNode["attributes"]["state"]["reportedValue"]
                elif 'thermostat.json' in oNode["nodeType"] and 'thermostat' in oNode["name"].lower():
                    strDeviceText = "NONE"
                    if hub == "NANO1":
                        if oNode["attributes"]["zone"]["reportedValue"] == 'HOT_WATER':
                            strDeviceName = "Hot water"
                            strDeviceState = oNode["attributes"]["stateHotWaterRelay"]["reportedValue"]
                        else:
                            strDeviceState = oNode["attributes"]["stateHeatingRelay"]["reportedValue"]
                            strDeviceName = "Heating"

                        if oNode["attributes"]["presence"]["reportedValue"] == 'ABSENT':
                            strDeviceState = "offline"
                        blnFlag = True
                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.thermostatui.json#':
                    flag = False
                    strDeviceText = "NONE"
                    if hub == "NANO2":
                        receiverid = oNode["relationships"]["boundNodes"][0]["id"]
                        receiver = oAPIValidations.getNodeByID(receiverid)
                        if thermostatcount == 1:
                            strDeviceName = "Heating"
                        else:
                            strDeviceName = receiver["nodes"][0]["attributes"]["zoneName"]["reportedValue"]
                        for subNode in nodes['nodes']:
                            if 'nodeType' in subNode.keys() and not 'synthetic.rule' in subNode['name']:
                                if 'thermostat.json' in subNode['nodeType']:
                                    if 'stateHotWaterRelay' in subNode["attributes"] and subNode[
                                        "parentNodeId"] == receiverid:
                                        strDeviceState = subNode["attributes"]["stateHotWaterRelay"]["reportedValue"]
                                        strDeviceName = "Hot water"
                                        flag = True

                                    elif 'stateHeatingRelay' in subNode["attributes"] and subNode[
                                        "parentNodeId"] == receiverid:
                                        strDeviceState = subNode["attributes"]["stateHeatingRelay"]["reportedValue"]
                                        strDeviceName = receiver["nodes"][0]["attributes"]["zoneName"]["reportedValue"]
                                        if thermostatcount == 1:
                                            strDeviceName = "Heating"
                                        flag = True

                            if receiver["nodes"][0]["attributes"]["presence"]["reportedValue"] == 'ABSENT':
                                strDeviceState = 'offline'
                            if flag:
                                strDeviceState = strDeviceState.lower()
                                strText = strDeviceName + ", " + strDeviceState + ";" + strDeviceText
                                listDevice.append(strText)
                            flag = False

            if blnFlag:
                strDeviceState = strDeviceState.lower()

                strText = strDeviceName + ", " + strDeviceState + ";" + strDeviceText
                listDevice.append(strText)
            blnFlag = False
        listofdevices = listDevice

        return listofdevices

    def dashboard_device_status(self):
        devicelist = self.getdevicecount()
        totaldevices = len(devicelist)
        self.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Validating the multiple screens and empty slots accordingly to number of devices in KIT')
        if totaldevices <= 7:
            if not self.is_element_present(*HomePageLocators.PAGE_INDICATOR):
                self.report_pass('Only one screen is present as devices are less than 7')
                self.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the status of the devices in the dashboard')
                for devices in devicelist:
                    devices = devicelist.split(';')[0]
                    Devices = HomePageLocators.DEVICE_STATE_LOC
                    Devices = Devices.replace("deviceString", devices)
                    if self.is_element_present(By.XPATH, devices):
                        self.report_pass('Device is present with proper state in app and api: ' + devices)
                    else:
                        self.report_fail('device is not present.')


            else:
                self.report_fail('Multiple screens are available for less than or equal to 7 devices.')
        else:
            if self.is_element_present(*HomePageLocators.PAGE_INDICATOR):
                indicator = self.driver.find_element(*HomePageLocators.PAGE_INDICATOR).get_attribute('value')
                indicator = indicator[-1:]
                screens = totaldevices / 7
                if not isinstance(screens, int):
                    screens = screens + 1
                screens = int(screens)
                if screens == int(indicator):
                    self.report_pass('Multiple screens are present for more than 7 devices')
                    self.reporter.HTML_TC_BusFlowKeyword_Initialize(
                        'Verifying the status of the devices in the dashboard')
                    for devices in devicelist:
                        devices = devices.split(';')[0]
                        Devices = HomePageLocators.DEVICE_STATE_LOC
                        Devices = Devices.replace("deviceString", devices)
                        if self.is_element_present(By.XPATH, Devices):
                            self.report_pass('Device is present with proper state in app and api: ' + devices)
                        else:
                            TouchAction(self.driver).press(None, 360, 610).wait(2000).move_to(None, -300,
                                                                                              0).release().perform()
                            time.sleep(3)
                            if self.is_element_present(By.XPATH, Devices):
                                self.report_pass('Device is present with proper state in app and api: ' + devices)
                                TouchAction(self.driver).press(None, 50, 550).wait(2000).move_to(None, 300,
                                                                                                 0).release().perform()
                                time.sleep(3)
                            else:
                                TouchAction(self.driver).press(None, 360, 610).wait(2000).move_to(None, -300,
                                                                                                  0).release().perform()
                                time.sleep(3)
                                if self.is_element_present(By.XPATH, Devices):
                                    self.report_pass('Device is present with proper state in app and api: ' + devices)

                                else:
                                    self.report_fail('device is not present: ' + devices)
                                TouchAction(self.driver).press(None, 50, 550).wait(2000).move_to(None, 300,
                                                                                                 0).release().perform()
                                time.sleep(3)
                                TouchAction(self.driver).press(None, 50, 550).wait(2000).move_to(None, 300,
                                                                                                 0).release().perform()
                                time.sleep(3)
                else:
                    self.report_fail('Multiple screens are present but more/less than as expected')
            else:
                self.report_fail('Multiple screens are not available for more than 7 devices.')

    def devicelist_device_status(self):
        devicelist = self.getdevicecount()
        self.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the status of the devices in the devicelist screen')
        for devices in devicelist:
            devices.strip()
            devicetext = devices.split(';')[1]
            deviceString = devices.split(';')[0]
            devicename = deviceString.split(',')[0]
            devicestate = deviceString.split(',')[1]
            Devices = HomePageLocators.DEVICELIST
            Devices = Devices.replace("devicename", devicename)
            if not devicetext == "NONE":
                devicestate = devicetext
            if self.is_element_present(By.XPATH, Devices):
                if devicestate.upper() in self.driver.find_element(By.XPATH, Devices).get_attribute('name').upper():
                    self.report_pass('Device is present with proper state in app and api: ' + devicename)
                else:
                    self.report_fail('Device is not present with proper state in app and api: ' + devicename)
            else:
                TouchAction(self.driver).press(None, 329, 683).wait(2000).move_to(None, 0, -317).release().perform()
                time.sleep(3)
                if self.is_element_present(By.XPATH, Devices):
                    if devicestate.upper() in self.driver.find_element(By.XPATH, Devices).get_attribute('name').upper():
                        self.report_pass('Device is present with proper state in app and api: ' + devicename)
                    else:
                        self.report_fail('Device is not present with proper state in app and api: ')
                    self.refresh_page()
                    time.sleep(3)
                else:
                    TouchAction(self.driver).press(None, 329, 683).wait(2000).move_to(None, 0, -317).release().perform()
                    time.sleep(3)
                    if self.is_element_present(By.XPATH, Devices):
                        if devicestate.upper() in self.driver.find_element(By.XPATH, Devices).get_attribute(
                                'name').upper():
                            self.report_pass('Device is present with proper state in app and api: ' + devicename)

                        else:
                            self.report_fail('Device is not present: ' + devicename)
                    else:
                        self.report_fail('Device is not present: ' + devicename)
                    self.refresh_page()
                    time.sleep(3)
                    self.refresh_page()
                    time.sleep(3)

    def check_devicelist(self, counter, nextcounter, devicelist, devicename):
        flag = True
        endcounter = counter + nextcounter
        while counter < endcounter:
            if devicelist[counter].upper() == devicename.upper():
                flag = True
                break
            else:
                flag = False
            counter += 1
        if flag:
            self.report_pass('Device: ' + devicename + ' is present in DeviceList screen in proper position')
        else:
            self.report_fail('Device: ' + devicename + ' is not present in DeviceList screen in proper position')

    def devicelist_verifyIconHierarchy(self):
        self.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Verifying the hierarchy of the devices in the devicelist screen')
        nodes = oAPIValidations.getNodes()
        thermostatcount = 0
        plugcount = 0
        whitelightcount = 0
        tuneablelightcount = 0
        colourlightcount = 0
        motioncount = 0
        wincount = 0
        hub = ''
        devlistflag = True
        devlist = []
        hotwaterflag = False
        i = 1

        for oNode in nodes['nodes']:
            if 'nodeType' in oNode.keys() and not 'synthetic.rule' in oNode['name']:
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.thermostatui.json#':
                    thermostatcount += 1
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.smartplug.json#':
                    plugcount += 1
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.light.json#':
                    whitelightcount += 1
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.tunable.light.json#':
                    tuneablelightcount += 1
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.colour.tunable.light.json#':
                    colourlightcount += 1
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.motion.sensor.json#':
                    motioncount += 1
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.contact.sensor.json#':
                    wincount += 1
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.hub.json#':
                    hub = oNode["attributes"]["hardwareVersion"]["reportedValue"]

        while devlistflag == True:
            DevLocator = HomePageLocators.DEVICELIST_HIERARCHY
            DevLocator = DevLocator.replace('DeviceCounter', str(i))
            try:
                if self.wait_for_element_exist(By.XPATH, DevLocator):
                    devlist.append(self.driver.find_element(By.XPATH, DevLocator).get_attribute('name'))
                    if i == thermostatcount + 1:
                        if "HOT WATER" in self.driver.find_element(By.XPATH, DevLocator).get_attribute('name').upper():
                            hotwaterflag = True
                    i += 1
                    if i == 8 or i == 15 or i == 22:
                        TouchAction(self.driver).press(None, 329, 683).wait(2000).move_to(None, 0,
                                                                                          -317).release().perform()
                        time.sleep(3)
                else:
                    devlistflag = False
            except NoSuchElementException as e:
                self.report_fail('iOS-App: Exception in getting devicelist\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
                devlistflag = False

        for oNode in nodes['nodes']:
            if 'nodeType' in oNode.keys() and not 'synthetic.rule' in oNode['name']:
                strDeviceName = oNode['name']
                if oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.smartplug.json#':
                    if hotwaterflag:
                        counter = thermostatcount + 1
                    else:
                        counter = thermostatcount
                    HoneyComb.check_devicelist(self, counter, plugcount, devlist, strDeviceName)

                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.light.json#':
                    if hotwaterflag:
                        counter = thermostatcount + plugcount + 1
                    else:
                        counter = thermostatcount + plugcount
                    HoneyComb.check_devicelist(self, counter, whitelightcount, devlist, strDeviceName)

                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.tunable.light.json#':
                    if hotwaterflag:
                        counter = thermostatcount + plugcount + whitelightcount + 1
                    else:
                        counter = thermostatcount + plugcount + whitelightcount
                    HoneyComb.check_devicelist(self, counter, tuneablelightcount, devlist, strDeviceName)

                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.colour.tunable.light.json#':
                    if hotwaterflag:
                        counter = thermostatcount + plugcount + whitelightcount + tuneablelightcount + 1
                    else:
                        counter = thermostatcount + plugcount + whitelightcount + tuneablelightcount
                    HoneyComb.check_devicelist(self, counter, colourlightcount, devlist, strDeviceName)

                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.motion.sensor.json#':
                    if hotwaterflag:
                        counter = thermostatcount + plugcount + whitelightcount + tuneablelightcount + colourlightcount + 1
                    else:
                        counter = thermostatcount + plugcount + whitelightcount + tuneablelightcount + colourlightcount
                    HoneyComb.check_devicelist(self, counter, motioncount, devlist, strDeviceName)

                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.contact.sensor.json#':
                    if hotwaterflag:
                        counter = thermostatcount + plugcount + whitelightcount + tuneablelightcount + colourlightcount + motioncount + 1
                    else:
                        counter = thermostatcount + plugcount + whitelightcount + tuneablelightcount + colourlightcount + motioncount
                    HoneyComb.check_devicelist(self, counter, wincount, devlist, strDeviceName)

                elif 'thermostat.json' in oNode["nodeType"] and 'thermostat' in oNode["name"].lower():
                    if hub == "NANO1":
                        if oNode["attributes"]["zone"]["reportedValue"] == 'HOT_WATER':
                            strDeviceName = "HOT WATER"
                            if hotwaterflag:
                                counter = thermostatcount
                            else:
                                self.report_fail('Hot Water is present in Kit but not in Device list screen')
                            HoneyComb.check_devicelist(self, counter, 1, devlist, strDeviceName)
                        else:
                            strDeviceName = "HEATING"
                            counter = thermostatcount
                            HoneyComb.check_devicelist(self, 0, counter, devlist, strDeviceName)
                elif oNode['nodeType'] == 'http://alertme.com/schema/json/node.class.thermostatui.json#':
                    if hub == "NANO2":
                        receiverid = oNode["relationships"]["boundNodes"][0]["id"]
                        receiver = oAPIValidations.getNodeByID(receiverid)
                        strDeviceName = receiver["nodes"][0]["attributes"]["zoneName"]["reportedValue"]
                        for subNode in nodes['nodes']:
                            if 'nodeType' in subNode.keys() and not 'synthetic.rule' in subNode['name']:
                                if 'thermostat.json' in subNode['nodeType']:
                                    if 'stateHotWaterRelay' in subNode["attributes"] and subNode[
                                        "parentNodeId"] == receiverid:
                                        strDeviceName = "HOT WATER"
                                        if hotwaterflag:
                                            counter = thermostatcount
                                        else:
                                            self.report_fail(
                                                'Hot Water is present in Kit but not in Device list screen')
                                        HoneyComb.check_devicelist(self, counter, 1, devlist, strDeviceName)

                                    elif 'stateHeatingRelay' in subNode["attributes"] and subNode[
                                        "parentNodeId"] == receiverid:
                                        strDeviceName = receiver["nodes"][0]["attributes"]["zoneName"]["reportedValue"]
                                        if thermostatcount == 1:
                                            strDeviceName = "HEATING"
                                        counter = thermostatcount
                                        HoneyComb.check_devicelist(self, 0, counter, devlist, strDeviceName)


class DashboardCustomisation(BasePage):
    DELETE_DEVICE_BUTTON = ""
    DEVICE_NAME = ""
    DEVICE_NAME_IN_LIST = ""
    CELL = ""
    DEVICE_NODE_ID = ""
    SWAPPING_NODE_ID = ""
    DEVICES_POSITION_BEFORESWAPPING = {}
    DEVICES_POSITION_AFTERSWAPPING = {}

    def updateObjects(self, strDeviceName):
        DashboardCustomisation.DEVICE_NAME = strDeviceName
        DELETE_DEVICE_BUTTON_TEMP = str(DashboardCustomisationLocators.DELETE_DEVICE_BUTTON)
        DashboardCustomisation.DELETE_DEVICE_BUTTON = DELETE_DEVICE_BUTTON_TEMP.replace("deviceName", strDeviceName)
        CELL_TEMP = str(DashboardCustomisationLocators.CELL)
        DashboardCustomisation.CELL = CELL_TEMP.replace("deviceName", strDeviceName)
        DEVICE_NAME_IN_LIST_TEMP = str(DashboardCustomisationLocators.DEVICE_IN_LIST)
        DashboardCustomisation.DEVICE_NAME_IN_LIST = DEVICE_NAME_IN_LIST_TEMP.replace("deviceName", strDeviceName)

    def initiateEditMode(self):
        try:
            if self.is_element_present(By.XPATH, DashboardCustomisation.CELL):
                oElement = self.driver.find_element(By.XPATH, DashboardCustomisation.CELL)
                action = TouchAction(self.driver)
                action.press(oElement).wait(2000).release().perform()
                self.report_done('IOS App : Navigated to the dashboard screen and long pressed on the device cell.')
            else:
                self.report_fail('IOS App : Issue in enabling the edit mode.')
        except:
            self.report_fail('IOS App : Exception: in initiateEditMode Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def verifyDashboardEditMode(self):
        try:
            if self.is_element_present(By.XPATH, DashboardCustomisation.DELETE_DEVICE_BUTTON):
                self.report_pass('IOS-App : The Dashboard Edit mode initiated with cell displaying X on it.')
            else:
                self.report_fail('IOS App : The app is not in edit mode as expected.')
        except:
            self.report_fail('IOS App : Exception: in verifyDashboardEditMode Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def addDeviceFromListOnDashboard(self):
        try:
            if self.is_element_present(By.XPATH, DashboardCustomisation.DEVICE_NAME_IN_LIST):
                self.driver.find_element(By.XPATH, DashboardCustomisation.DEVICE_NAME_IN_LIST).click()
                time.sleep(2)
                if self.is_element_present(By.XPATH, DashboardCustomisation.DELETE_DEVICE_BUTTON):
                    if self.is_element_present(*DashboardCustomisationLocators.SAVE_CHANGES_BUTTON):
                        self.driver.find_element(*DashboardCustomisationLocators.SAVE_CHANGES_BUTTON).click()
                        time.sleep(2)
                        if self.is_element_present(By.XPATH, DashboardCustomisation.CELL):
                            time.sleep(2)
                            self.report_pass('IOS-App : Successfully added device on dashboard from Device List.')
                        else:
                            self.report_fail('IOS App : The device was not added to the device list.')
                    else:
                        self.report_fail('IOS App : Clicking on Save button failed')
                else:
                    self.report_fail('IOS App : Edit mode is not enabled in the dashboard.')
        except:
            self.report_fail('IOS App : Exception: in addDeviceFromListOnDashboard Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def validateDeletedDeviceInList(self):
        try:
            self.driver.find_element(*DashboardCustomisationLocators.ADD_DEVICE_BUTTON).click()
            time.sleep(2)
            if self.is_element_present(By.XPATH, DashboardCustomisation.DEVICE_NAME_IN_LIST):
                self.report_pass('IOS-App : Device is available in Device List, NOT on dashboard.')
                self.driver.find_element(*DashboardCustomisationLocators.CANCEL_ADD_DEVICE).click()
                time.sleep(2)
            else:
                self.report_fail('IOS App : Device is not available in the Device list')
        except:
            self.report_fail('IOS App : Exception: in validateDeletedDeviceInList Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def tapButton(self, buttonType):
        try:
            if "ADD" in buttonType.upper():
                if self.is_element_present(*DashboardCustomisationLocators.ADD_DEVICE_BUTTON):
                    self.driver.find_element(By.XPATH, DashboardCustomisation.DELETE_DEVICE_BUTTON).click()
                    time.sleep(3)
                    self.driver.find_element(*DashboardCustomisationLocators.ADD_DEVICE_BUTTON).click()
                    time.sleep(1)
                    if self.is_element_present(*DashboardCustomisationLocators.ADD_DEVICE_TITLE):
                        time.sleep(2)
                        self.report_done('IOS-App : Clicked on Add + button.')
                else:
                    self.report_fail('IOS App : Clicking of Add button failed')
            elif "SAVE" in buttonType.upper():
                if self.is_element_present(*DashboardCustomisationLocators.SAVE_CHANGES_BUTTON):
                    self.driver.find_element(*DashboardCustomisationLocators.SAVE_CHANGES_BUTTON).click()
                    time.sleep(2)
                    self.report_pass('IOS-App : Clicked on Save button to save the Dashboard Customisation changes')
                else:
                    self.report_fail('IOS App : Clicking on Save button failed')
            elif "CANCEL" in buttonType.upper():
                if self.is_element_present(*DashboardCustomisationLocators.CANCEL_CHANGES_BUTTON):
                    self.driver.find_element(*DashboardCustomisationLocators.CANCEL_CHANGES_BUTTON).click()
                    time.sleep(2)
                    self.report_pass(
                        'IOS-App : Clicked on Cancel button to discard the Dashboard Customisation changes')
                else:
                    self.report_fail('IOS App : Clicking on Cancel button failed')
            elif "REMOVE" in buttonType.upper():
                if self.is_element_present(By.XPATH, DashboardCustomisation.DELETE_DEVICE_BUTTON):
                    self.driver.find_element(By.XPATH, DashboardCustomisation.DELETE_DEVICE_BUTTON).click()
                    time.sleep(2)
                    self.report_done('IOS-App : Clicked on device\'s X button.')
                else:
                    self.report_fail('IOS App : Clicking on Remove button failed')
        except:
            self.report_fail('IOS App : Exception: in tapButton Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def validateChangesPostExit(self, type):
        try:
            if "REVERTED" in type.upper():
                if self.is_element_present(By.XPATH, DashboardCustomisation.CELL):
                    modeStatus = self.is_element_present(*DashboardCustomisationLocators.CANCEL_CHANGES_BUTTON)
                    if modeStatus:
                        self.report_fail('IOS-App : Dashboard is still in Edit mode')
                    else:
                        time.sleep(2)
                        self.report_pass('IOS-App : Discarded Dashboard Customisation changes and exited Edit mode')
            elif "SAVED" in type.upper():
                if self.is_element_present(By.XPATH, DashboardCustomisation.CELL):
                    self.report_fail(
                        'IOS-App : Couldn\'t save Dashboard Customisation changes, device is still present on dashboard after removal')
                else:
                    modeStatus = self.is_element_present(*DashboardCustomisationLocators.SAVE_CHANGES_BUTTON)
                    if modeStatus:
                        self.report_fail('IOS-App : Dashboard is still in Edit mode')
                    else:
                        time.sleep(2)
                        self.report_pass('IOS-App : Saved Dashboard Customisation changes and exited Edit mode')
                        time.sleep(2)
                        self.driver.find_element(*DashboardCustomisationLocators.ADD_DEVICE_BUTTON).click()
                        time.sleep(1)
                        if self.is_element_present(By.XPATH, DashboardCustomisation.DEVICE_NAME_IN_LIST):
                            self.driver.find_element(By.XPATH, DashboardCustomisation.DEVICE_NAME_IN_LIST).click()
            elif "SWAPPED" in type.upper():
                self.validateDeviceIndex()
        except:
            self.report_fail('IOS App : Exception: in validateChangesPostExit Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def swapDevicesOnDashboard(self, swapDeviceName):
        try:
            if self.reporter.ActionStatus:
                if self.is_element_present(By.XPATH, DashboardCustomisation.CELL):
                    oDevice = self.driver.find_element(By.XPATH, DashboardCustomisation.CELL)

                    intX = oDevice.location['x']
                    intY = oDevice.location['y']

                    intWidth = oDevice.size['width']
                    intHeight = oDevice.size['height']

                    intCenterX = (intX + (intWidth / 2))
                    intCenterY = (intY + (intHeight / 2))

                    CELL_TEMP = str(DashboardCustomisationLocators.CELL)
                    swapDevice = CELL_TEMP.replace("deviceName", swapDeviceName)

                    if self.is_element_present(By.XPATH, swapDevice):
                        oSwapDevice = self.driver.find_element(By.XPATH, swapDevice)

                        intSwapX = oSwapDevice.location['x']
                        intSwapY = oSwapDevice.location['y']

                        intWidthSwap = oSwapDevice.size['width']
                        intHeightSwap = oSwapDevice.size['height']

                        intSwapCenterX = (intSwapX + (intWidthSwap / 2))
                        intSwapCenterY = (intSwapY + (intHeightSwap / 2))

                        DashboardCustomisation.deviceNodeID = oAPIValidations.getDeviceNodeByName(
                            DashboardCustomisation.DEVICE_NAME)
                        DashboardCustomisation.swappingDeviceNodeID = oAPIValidations.getDeviceNodeByName(
                            swapDeviceName)
                        DashboardCustomisation.DEVICES_POSITION_BEFORESWAPPING = oAPIValidations.getDeviceIDsAndPositionsByBeekeeper()

                        self.driver.execute_script("mobile: dragFromToForDuration",
                                                   {"fromX": int(intCenterX), "fromY": int(intCenterY),
                                                    "toX": int(intSwapCenterX), "toY": int(intSwapCenterY),
                                                    "duration": 1})
                        # self.driver.swipe(int(intCenterX), int(intCenterY), int(intSwapCenterX), int(intSwapCenterY))
                        time.sleep(4)
                        self.report_pass(
                            'IOS App : Moving ' + DashboardCustomisation.DEVICE_NAME + ' to the new position')
                    else:
                        self.report_fail('IOS App : Swapping device is not found.')
                else:
                    self.report_fail('IOS App : Device is not found.')
        except:
            self.report_fail('IOS App : Exception: in swapDevicesOnDashboard Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def validateDeviceIndex(self):
        try:
            if self.reporter.ActionStatus:
                DashboardCustomisation.DEVICES_POSITION_AFTERSWAPPING = oAPIValidations.getDeviceIDsAndPositionsByBeekeeper()
                if DashboardCustomisation.DEVICES_POSITION_BEFORESWAPPING.get(
                        DashboardCustomisation.DEVICE_NODE_ID) == DashboardCustomisation.DEVICES_POSITION_AFTERSWAPPING.get(
                    DashboardCustomisation.SWAPPING_NODE_ID):
                    self.report_pass(
                        'IOS App : ' + DashboardCustomisation.DEVICE_NAME + ' moved to the new position : ' + str(
                            DashboardCustomisation.DEVICES_POSITION_AFTERSWAPPING.get(
                                DashboardCustomisation.SWAPPING_NODE_ID)) + ', validated the same through Beekeeper')
                else:
                    self.report_fail(
                        'IOS App : ' + DashboardCustomisation.DEVICE_NAME + ' couldn\'t be moved to the new position')
        except:
            self.report_fail('IOS App : Exception: in validateDeviceIndex Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))


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
                self.report_fail('iOS-App : NoSuchElementException: in reset_schedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    # for copying a schedule
    def copy_schedule(self, strToDay, strFromDay):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON):
                    self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                self._navigate_to_day(strFromDay)

                if self.wait_for_element_exist(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click()
                    time.sleep(2)
                    self.report_done("Add Icon is found and clicked sucessfully")
                else:
                    self.report_fail("Add Icon is not found on schedule screen, Exit condition")
                    exit()
                if self.wait_for_element_exist(*SchedulePageLocators.COPY_SCHEDULE_SUBMENU):
                    self.driver.find_element(*SchedulePageLocators.COPY_SCHEDULE_SUBMENU).click()
                    time.sleep(2)
                    self.report_done("Copy schedule Icon is found and clicked sucessfully")
                else:
                    self.report_fail("Copy schedule is not found on schedule screen, Exit condition")
                    exit()

                if strToDay.upper() == 'MON':
                    self.driver.find_element(*SchedulePageLocators.MON_SCHEDULE_BUTTON).click()
                elif strToDay.upper() == 'TUE':
                    self.driver.find_element(*SchedulePageLocators.TUE_SCHEDULE_BUTTON).click()
                elif strToDay.upper() == 'WED':
                    self.driver.find_element(*SchedulePageLocators.WED_SCHEDULE_BUTTON).click()
                elif strToDay.upper() == 'THU':
                    self.driver.find_element(*SchedulePageLocators.THU_SCHEDULE_BUTTON).click()
                elif strToDay.upper() == 'FRI':
                    self.driver.find_element(*SchedulePageLocators.FRI_SCHEDULE_BUTTON).click()
                elif strToDay.upper() == 'SAT':
                    self.driver.find_element(*SchedulePageLocators.SAT_SCHEDULE_BUTTON).click()
                elif strToDay.upper() == 'SUN':
                    self.driver.find_element(*SchedulePageLocators.SUN_SCHEDULE_BUTTON).click()

                if self.wait_for_element_exist(*SchedulePageLocators.SAVE_SCHEDULE):
                    self.driver.find_element(*SchedulePageLocators.SAVE_SCHEDULE).click()
                    time.sleep(2)
                    self.report_done("Save OK Button is found and clicked sucessfully")
                else:
                    self.report_fail("Save OK Button is not found on schedule screen, Exit condition")
                    exit()
            except:
                self.report_fail('iOS-App : NoSuchElementException: in copySchedule Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


class NAT(BasePage):
    def navigate(self, NATname, NATmode, NATstate):

        if 'OFF' == (NATstate.upper()):
            NATmode = 'OFF'
        else:
            if 'HEATING' == NATmode.upper():
                NATmode = 'HEAT'
            elif 'COOLING' == NATmode.upper():
                NATmode = 'COOL'
        NAT_Dashboard_on = HomePageLocators.Plug_runtime_Dashboard_on
        NAT_Dashboard_on = NAT_Dashboard_on.replace("devicename", NATname)
        NAT_Dashboard_on_SZ = NAT_Dashboard_on.replace("devicename", NATmode)
        NAT_Dashboard_off = HomePageLocators.Plug_runtime_Dashboard_off
        NAT_Dashboard_off = NAT_Dashboard_off.replace("devicename", NATname)
        NAT_Dashboard_off_SZ = NAT_Dashboard_off.replace("devicename", NATmode)
        if self.is_element_present(By.XPATH, NAT_Dashboard_on):
            self.driver.find_element(By.XPATH, NAT_Dashboard_on).click()
            self.report_pass('SLT4 is found in Dashboard and clicked')
        elif self.is_element_present(By.XPATH, NAT_Dashboard_off):
            self.driver.find_element(By.XPATH, NAT_Dashboard_off).click()
            self.report_pass('SLT4 is found in Dashboard and clicked')
        elif self.is_element_present(By.XPATH, NAT_Dashboard_on_SZ):
            self.driver.find_element(By.XPATH, NAT_Dashboard_on_SZ).click()
            self.report_pass('SLT4 is found in Dashboard and clicked')
        elif self.is_element_present(By.XPATH, NAT_Dashboard_off_SZ):
            self.driver.find_element(By.XPATH, NAT_Dashboard_off_SZ).click()
            self.report_pass('SLT4 is found in Dashboard and clicked')
        else:
            self.driver.swipe(1008.7, 1534.9, 108.3, 1598.7, 2000)
            if self.is_element_present(By.XPATH, NAT_Dashboard_on):
                self.driver.find_element(By.XPATH, NAT_Dashboard_on).click()
                self.report_pass('SLT4 is found in Dashboard and clicked')
            elif self.is_element_present(By.XPATH, NAT_Dashboard_off):
                self.driver.find_element(By.XPATH, NAT_Dashboard_off).click()
                self.report_pass('SLT4 is found in Dashboard and clicked')
            elif self.is_element_present(By.XPATH, NAT_Dashboard_on_SZ):
                self.driver.find_element(By.XPATH, NAT_Dashboard_on_SZ).click()
                self.report_pass('SLT4 is found in Dashboard and clicked')
            elif self.is_element_present(By.XPATH, NAT_Dashboard_off_SZ):
                self.driver.find_element(By.XPATH, NAT_Dashboard_off_SZ).click()
                self.report_pass('SLT4 is found in Dashboard and clicked')
            else:
                self.report_fail('SLT4 is not found in Dashboard')

    def navigation_to_NATpage(self, NATname, NATmode, NATstate):

        try:
            if self.wait_for_element_exist(*NATLocators.DEVICELIST_ICON):
                if 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute(
                        'name').upper():
                    self.report_done('User is in Dashboard Screen')
                else:
                    self.driver.find_element(*NATLocators.DEVICELIST_ICON).click()
                    time.sleep(2)
                    if self.wait_for_element_exist(*NATLocators.DASHBOARD_ICON):
                        self.driver.find_element(*NATLocators.DASHBOARD_ICON).click()
                        time.sleep(2)
                        if 'MY HIVE HOME' in self.driver.find_element(*HomePageLocators.DASHBOARD_TITLE).get_attribute(
                                'name').upper():
                            self.report_done('User is in Dashboard Screen')
                        else:
                            self.report_fail('Dashboard Screen Label is not found')
                    else:
                        self.report_fail('Dashboard Icon not found')
                self.navigate(NATname, NATmode, NATstate)
            elif self.wait_for_element_exist(*PlugLocators.DASHBOARD_ICON):
                self.driver.find_element(*PlugLocators.DASHBOARD_ICON).click()
                time.sleep(2)
                self.navigate(NATname, NATmode, NATstate)

            else:
                self.report_fail('User is not inside the app')
        except:
            self.report_fail('IOS App : NoSuchElementException: in navigate_to_plug Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    def NAT_ChangeModeAndOperatingMode(self, strMode, strOperatingMode, strThermostatName):
        if self.reporter.ActionStatus:
            try:
                blnModeFound = False
                blnOperatingMode = False
                if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_ICON):
                    self.driver.find_element(*NATLocators.THERMOSTAT_SETTINGS_ICON).click()
                    time.sleep(3)
                if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_TITLE):
                    self.report_pass('Settings Page Displayed')

                strModeUpdated = self.UpdateModeScreenEquivalent(strMode.upper())
                if strOperatingMode == "OFF":
                    if self.wait_for_element_exist(*NATLocators.THERMOSTAT_MODE_OFF_ICON):
                        self.driver.find_element(*NATLocators.THERMOSTAT_MODE_OFF_ICON).click()
                        time.sleep(3)
                        blnOperatingMode = True
                    else:
                        self.report_fail('Icon not found')
                else:
                    if strModeUpdated == "heat":
                        if self.wait_for_element_exist(*NATLocators.THERMOSTAT_MODE_HEAT_ICON):
                            self.driver.find_element(*NATLocators.THERMOSTAT_MODE_HEAT_ICON).click()
                            time.sleep(3)
                            blnModeFound = True
                        else:
                            self.report_fail('Icon not found')

                    elif strModeUpdated == "cool":
                        if self.wait_for_element_exist(*NATLocators.THERMOSTAT_MODE_COOL_ICON):
                            self.driver.find_element(*NATLocators.THERMOSTAT_MODE_COOL_ICON).click()
                            time.sleep(3)
                            blnModeFound = True
                        else:
                            self.report_fail('Icon not found')
                    elif strModeUpdated == "dual":
                        if self.wait_for_element_exist(*NATLocators.THERMOSTAT_MODE_DUAL_ICON):
                            self.driver.find_element(*NATLocators.THERMOSTAT_MODE_DUAL_ICON).click()
                            time.sleep(3)
                            blnModeFound = True
                        else:
                            self.report_fail('Icon not found')
                    if blnModeFound:
                        self.report_pass('Mode ' + strMode + ' is clicked')
                        time.sleep(3)
                    else:
                        self.report_fail('ICON for the mode ' + strMode + ' is not found')

                    if self.reporter.ActionStatus:
                        if strOperatingMode == "HOLD":
                            if self.wait_for_element_exist(*NATLocators.THERMOSTAT_MODE_HOLD_ICON):
                                self.driver.find_element(*NATLocators.THERMOSTAT_MODE_HOLD_ICON).click()
                                time.sleep(3)
                                blnOperatingMode = True
                            else:
                                self.driver.find_element(*NATLocators.THERMOSTAT_SETTINGS_SAVE).click()
                                time.sleep(3)
                                self.driver.find_element(*NATLocators.THERMOSTAT_SETTINGS_ICON).click()
                                time.sleep(3)
                                if self.wait_for_element_exist(*NATLocators.THERMOSTAT_MODE_HOLD_ICON):
                                    self.driver.find_element(*NATLocators.THERMOSTAT_MODE_HOLD_ICON).click()
                                    time.sleep(3)
                                    blnOperatingMode = True
                                else:
                                    self.report_fail('Icon not found')
                        elif strOperatingMode == "SCHEDULE":
                            if self.wait_for_element_exist(*NATLocators.THERMOSTAT_MODE_SCHEDULE_ICON):
                                self.driver.find_element(*NATLocators.THERMOSTAT_MODE_SCHEDULE_ICON).click()
                                time.sleep(3)
                                blnOperatingMode = True
                            else:
                                self.driver.find_element(*NATLocators.THERMOSTAT_SETTINGS_SAVE).click()
                                time.sleep(3)
                                self.driver.find_element(*NATLocators.THERMOSTAT_SETTINGS_ICON).click()
                                time.sleep(3)
                                if self.wait_for_element_exist(*NATLocators.THERMOSTAT_MODE_SCHEDULE_ICON):
                                    self.driver.find_element(*NATLocators.THERMOSTAT_MODE_SCHEDULE_ICON).click()
                                    time.sleep(3)
                                    blnOperatingMode = True
                                else:
                                    self.report_fail('Icon not found')

                if blnOperatingMode:
                    self.report_pass('Operating Mode ' + strOperatingMode + ' is clicked')
                    time.sleep(3)
                else:
                    self.report_fail('Operating mode ' + strOperatingMode + ' is not set')

                if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_TITLE):
                    if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_SAVE):
                        self.driver.find_element(*NATLocators.THERMOSTAT_SETTINGS_SAVE).click()
                        time.sleep(3)
                        if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_ICON):
                            self.report_pass('Thermostat Settings are saved')
                        else:
                            if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_TITLE):
                                self.driver.find_element(*NATLocators.THERMOSTAT_SETTINGS_CANCEL).click()
                                time.sleep(3)
                                if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_ICON):
                                    self.report_pass('Thermostat Settings are saved')
                                else:
                                    self.report_fail('Settings are not saved')
                        time.sleep(3)
                    else:
                        self.report_fail('Save button not found')
                    time.sleep(6)
                self.refresh_page()

            except:
                self.report_fail('IOS-App : NoSuchElementException: in NAThermostat Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def NAT_setTemp(self, strExpectedTemp, str_thermostat_name, objTempPicker=None):

        try:
            if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_ICON):
                if '--' in strExpectedTemp:

                    strTempSplitted = strExpectedTemp.split('--')
                    strMinTemp = strTempSplitted[1]
                    strMaxTemp = strTempSplitted[0]
                    self.NAT_setTemp(strMinTemp, str_thermostat_name, NATLocators.THERMOSTAT_CONTROL_HEAT)
                    self.NAT_setTemp(strMaxTemp, str_thermostat_name, NATLocators.THERMOSTAT_CONTROL_COOL)

                else:
                    if objTempPicker is None:
                        objTempPicker = NATLocators.THERMOSTAT_CONTROL
                    if self.wait_for_element_exist(*objTempPicker):
                        objTempPicker = self.driver.find_element(*NATLocators.THERMOSTAT_CONTROL)
                        oScrolElementVAlue = objTempPicker.get_attribute('value')
                        if 'point' in oScrolElementVAlue:
                            fltCurrentTargTemp = float(
                                oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                        else:
                            fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                        intCntrIter = 1
                        while (fltCurrentTargTemp != int(strExpectedTemp)) and (intCntrIter < 3):
                            self.scroll_element_to_value(objTempPicker, fltCurrentTargTemp, int(strExpectedTemp), 0.5,
                                                         1)
                            oScrolElementVAlue = objTempPicker.get_attribute('value')
                            if 'point' in oScrolElementVAlue:
                                fltCurrentTargTemp = float(
                                    oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                            else:
                                fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[4])
                            intCntrIter += 1

                        if fltCurrentTargTemp == int(strExpectedTemp):
                            self.report_pass('The Target Temperature is successfully set to : ' +
                                             strExpectedTemp)
                        else:
                            self.report_fail(
                                'Unable to set the Target Temperature to : ' + strExpectedTemp)
                    else:
                        self.report_fail('The temp scroll icon is not found')
            else:
                self.report_fail('User is not in Control screen.')
        except:
            self.report_fail(
                'IOS App : NoSuchElementException: in function NAT_setTemp \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def updateStatOperatingAttributes(self, str_thermostat_name):
        clientCurrentTargetTemp = ''
        clientFlameIconApperance = False
        clientThermostatOperatingMODE = ''
        clientNextScheduleSlot = ''
        try:
            if self.wait_for_element_exist(*NATLocators.THERMOSTAT_SETTINGS_ICON):
                if self.is_element_present(*NATLocators.THERMOSTAT_MODE_OFF_ICON):
                    clientThermostatOperatingMODE = 'OFF'
                else:

                    if self.is_element_present(*NATLocators.THERMOSTAT_CONTROL):
                        oScrolElement = self.driver.find_element(*NATLocators.THERMOSTAT_CONTROL)
                        oScrolElementVAlue = (oScrolElement.get_attribute('value').upper().split())
                        if 'point' in oScrolElementVAlue:
                            clientCurrentTargetTemp = float(
                                oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                        else:
                            clientCurrentTargetTemp = float(oScrolElementVAlue.split(' ')[4])

                    if self.is_element_present(*NATLocators.THERMOSTAT_CONTROL_HEAT):
                        oScrolElement = self.driver.find_element(*NATLocators.THERMOSTAT_CONTROL_HEAT)
                        oScrolElementVAlue = oScrolElement.get_attribute('value')
                        if 'point' in oScrolElementVAlue:
                            strTargetTemp = float(
                                oScrolElementVAlue.split(' ')[4] + '.' + oScrolElementVAlue.split(' ')[6])
                        else:
                            strTargetTemp = float(oScrolElementVAlue.split(' ')[4])
                        if clientCurrentTargetTemp == '':
                            clientCurrentTargetTemp = strTargetTemp
                        else:
                            clientCurrentTargetTemp = str(clientCurrentTargetTemp) + '--' + strTargetTemp

                    if '--' in str(clientCurrentTargetTemp):
                        if self.is_element_present(*NATLocators.THERMOSTAT_FLAKEICON_DUAL):
                            clientFlameIconApperance = 'COOL'
                        elif self.is_element_present(*NATLocators.THERMOSTAT_FLAMEICON_DUAL):
                            clientFlameIconApperance = 'HEAT'
                        else:
                            clientFlameIconApperance = False
                    else:
                        if self.is_element_present(*NATLocators.THERMOSTAT_FLAKEICON):
                            clientFlameIconApperance = True
                        elif self.is_element_present(*NATLocators.THERMOSTAT_FLAMEICON):
                            clientFlameIconApperance = True
                        else:
                            clientFlameIconApperance = False
                    if self.is_element_present(*NATLocators.THERMOSTAT_SCHEDULE_MODE_ICON):
                        clientThermostatOperatingMODE = 'SCHEDULE'
                    elif self.is_element_present(*NATLocators.THERMOSTAT_MANUAL_MODE_ICON):
                        clientThermostatOperatingMODE = 'HOLD'
                    else:
                        clientThermostatOperatingMODE = 'OFF'
            else:
                self.report_fail('User is not in Control Screen')


        except:
            self.report_fail(
                'IOS App : NoSuchElementException: in function NAT_setTemp \n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
        self.report_done('Screen shot after Temp and mode updates')
        return clientCurrentTargetTemp, clientFlameIconApperance, clientThermostatOperatingMODE

    # For fetching the screen equivalent of mode
    def UpdateModeScreenEquivalent(self, strMode):
        ModeDictionary = {"HEATING": "heat", "COOLING": "cool", "DUAL": "dual", "OFF": "off", "COOL": "cool",
                          "HEAT": "heat"}
        return ModeDictionary[strMode]
