"""
Created on 16 Jun 2015

@author: ranganathan.veluswamy
"""

import os
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from decimal import Decimal

from EE_Locators_WebApp import LoginPageLocators, LoginPageLocatorsV3, DashboardLocatorsV3, HeatingPageLocators, HotWaterPageLocators, ActivePlugPageLocators, \
    ForgottenPasswordPageLocators, HeatingDashboardLocators, HeatingNotificationLocators, DashboardLocators, \
    HolidayModePageLocators , WarmWhiteLightPageLocators, WarmWhiteLightPageLocatorsV3, TuneableLightPageLocators, ColourLightPageLocators, PageHeaderLocators, \
    ActivePlugPageLocators_V3, MotionSensorPageLocators_V3


import FF_ScheduleUtils as oSchedUtils
import FF_convertTimeTemperature as tt
from _decimal import Context
from lib2to3.pgen2.driver import Driver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class BasePage(object):

    #Contructor for BasePage
    def __init__(self, driver, reporter):
        self.driver = driver
        self.reporter = reporter

        self.webDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.EXPLICIT_WAIT_TIME = 10

    #Waits for the given element exists for EXPLICIT_WAIT_TIME
    def wait_for_element_exist(self, by, value, intWaitTime = 0):
        if intWaitTime == 0: intWaitTime = self.EXPLICIT_WAIT_TIME
        try:
            wait = WebDriverWait(self.driver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False
            print(by, value, 'element not found')

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    #Initializes the  Selenium Web Driver
    def setup_Selenium_driver(self, strBrowserName, strURL):
        if strBrowserName.upper() == 'FIREFOX':
            '''desired_cap = {
            "platform": "Windows 10",
            "browserName": "internet explorer",
            "version": "11"
            }
            driver = webdriver.Remote(
               command_executor='http://rangawillb4u:2f69f940-28e9-4cae-ac75-b5f0c430f339@ondemand.saucelabs.com:80/wd/hub',
               desired_capabilities=desired_cap)'''
            caps = DesiredCapabilities.FIREFOX
            caps["marionette"] = True
            caps["binary"] = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"
            geckodriver = "/Users/skuppusamy/Documents/workspace/HiveTestAutomation/Geckodriver/geckodriver"

            driver = webdriver.Firefox(capabilities=caps, executable_path=geckodriver)
            #driver = webdriver.Firefox()
            driver.get(strURL)
            #driver.maximize_window()
            #driver.implicitly_wait(60)
        if strBrowserName.upper() == 'CHROME':
            chromedriver = "/Users/sri.gunasekaran/Documents/workspace/HiveTestAutomation/chromedriver"

            driver =  webdriver.Chrome(executable_path=chromedriver)
            driver.get(strURL)
            driver.maximize_window()

        return driver

    #Report the Failure step the HTML report
    def report_fail(self, strFailDescription):
        self.reporter.ActionStatus = False
        self.reporter.ReportEvent('Test Validation', strFailDescription, "FAIL", 'Center', True, self.driver)

    #Report the Pass step the HTML report
    def report_pass(self, strPassDescription):
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strPassDescription, "PASS", 'Center', True, self.driver)

    #Report the Done step the HTML report
    def report_done(self, strStepDescription):
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strStepDescription, "DONE", 'Center', True, self.driver)

    #Report the Done step the HTML report
    def report_step(self, strStepDescription):
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strStepDescription, "DONE", 'Center', True)

    def refresh_page(self):
        self.driver.refresh()
        time.sleep(3)

    def click_element_on_position(self, oClickElement, strPosition = 'Center'):
        intWidth = oClickElement.size['width']
        intHieght = oClickElement.size['height']
        intX = intWidth/2

        if strPosition.upper() == 'TOP':
            intY = intHieght/4
        elif strPosition.upper() == 'BOTTOM':
            intY = (intHieght/4) * 3
        else: intY = intHieght/2

        action = ActionChains(oClickElement.parent)
        action.move_to_element_with_offset(oClickElement, intX, intY)
        action.click()
        action.perform()
        time.sleep(0.2)

    #Clicks on the Scrollable element to set the specific value passed
    def _set_target_temperature(self, oTargTempElement, fltSetTargTemp):
        if fltSetTargTemp == 1.0: fltSetTargTemp = 7.0
        fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')

        if fltCurrentTargTemp is None:
            self.click_element_on_position(oTargTempElement, 'Top')
            self.click_element_on_position(oTargTempElement, 'Bottom')
            fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
        fltCurrentTargTemp = float(fltCurrentTargTemp)

        print(fltCurrentTargTemp)
        print(fltSetTargTemp)
        if not fltSetTargTemp==fltCurrentTargTemp:
            intCntrIter = 1
            while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):
                strPositionToClick = 'Top'
                if fltSetTargTemp < fltCurrentTargTemp: strPositionToClick = 'Bottom'
                intIterCount = int(abs(fltSetTargTemp-fltCurrentTargTemp)/0.5)
                for intCnt in range(intIterCount):
                    self.click_element_on_position(oTargTempElement, strPositionToClick)
                fltCurrentTargTemp = float(oTargTempElement.get_attribute('aria-valuenow'))
                intCntrIter += 1
        time.sleep(5)
        if  fltSetTargTemp==fltCurrentTargTemp: return True
        else: return False

    def _set_brightness(self, oTargBrightnessElement, intSetTargBrightness):
        if intSetTargBrightness == 0:
            intSetTargBrightness = 'OFF'
        targBrightnessElContent = oTargBrightnessElement.text
        if 'off' in targBrightnessElContent:
            intCurrentBrightness = 'OFF'
        else :
            intCurrentBrightness = targBrightnessElContent.split('%')[0]
        print(intCurrentBrightness)
        if 'OFF' in intCurrentBrightness.upper() and not str(intSetTargBrightness) == 'OFF':
            print('Check')
            oTargBrightnessElement.click()
        if str(intCurrentBrightness.upper()) == str(intSetTargBrightness):
            print('Test')
            return True
        else:
        #if 'OFF' in str(intCurrentBrightness).upper():
            #oTargBrightnessElement.click()

            if intSetTargBrightness == 5:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_5_PERCENT).click()
            elif intSetTargBrightness == 10:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_10_PERCENT).click()
            elif intSetTargBrightness == 20:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_20_PERCENT).click()
            elif intSetTargBrightness == 30:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_30_PERCENT).click()
            elif intSetTargBrightness == 40:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_40_PERCENT).click()
            elif intSetTargBrightness == 50:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_50_PERCENT).click()
            elif intSetTargBrightness == 60:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_60_PERCENT).click()
            elif intSetTargBrightness == 70:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_70_PERCENT).click()
            elif intSetTargBrightness == 80:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_80_PERCENT).click()
            elif intSetTargBrightness == 90:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_90_PERCENT).click()
            elif intSetTargBrightness == 100:
                self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_DIMMER_100_PERCENT).click()
            else:
                oTargBrightnessElement.click()
        time.sleep(5)

        intCurrentBrightness = oTargBrightnessElement.text
        if not str(intCurrentBrightness).upper() == 'OFF':
            intCurrentBrightness = intCurrentBrightness.rstrip('%')


        if str(intSetTargBrightness) == str(intCurrentBrightness):
            return True
        else:
            return False

    def _set_tone(self, oTargToneElement, strTargetTone, strLightType = None):
        if not '-' in strTargetTone:
            if not strLightType:
                self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_TONE_DIMMER_SWITCH).click()
            else:
                oTargetElPickerText = oTargToneElement.text
                if 'TONE' in oTargetElPickerText.upper():
                    self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_TONE_DIMMER_SWITCH).click()
                else:
                    self.driver.find_element(*ColourLightPageLocators.SCHEDULE_TONE_COLOUR_SWITCH).click()
                    self.driver.find_element(*ColourLightPageLocators.SCHEDULE_TONE_SWITCH).click()
        else :
            return True
        if strTargetTone == 'WARMEST WHITE':
            if strLightType: self.driver.find_element(*ColourLightPageLocators.SCHEDULE_WARMEST_WHITE).click()
            else: self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_WARMEST_WHITE).click()
        elif strTargetTone == 'WARM WHITE':
            if strLightType: self.driver.find_element(*ColourLightPageLocators.SCHEDULE_WARM_WHITE).click()
            else: self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_WARM_WHITE).click()
        elif strTargetTone == 'MID WHITE':
            if strLightType: self.driver.find_element(*ColourLightPageLocators.SCHEDULE_MID_WHITE).click()
            else: self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_MID_WHITE).click()
        elif strTargetTone == 'COOL WHITE':
            if strLightType: self.driver.find_element(*ColourLightPageLocators.SCHEDULE_COOL_WHITE).click()
            else: self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_COOL_WHITE).click()
        elif strTargetTone == 'COOLEST WHITE':
            if strLightType: self.driver.find_element(*ColourLightPageLocators.SCHEDULE_COOLEST_WHITE).click()
            else: self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_COOLEST_WHITE).click()
        time.sleep(5)
        if not strLightType:
            strCurrentTone = oTargToneElement.text

            if strCurrentTone == strTargetTone:
                return True
            else:
                return False

    def _set_colour(self, oTargColourElement, strTargetColour ,strLightType = None):
        if not '-' in strTargetColour:
            if not strLightType:
                self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_TONE_DIMMER_SWITCH).click()
            else :
                oTargetElPickerText = self.driver.find_element(*ColourLightPageLocators.SCHEDULE_TONE_COLOUR_SWITCH).text
                if 'COLOUR' in oTargetElPickerText.upper():
                    self.driver.find_element(*ColourLightPageLocators.SCHEDULE_TONE_COLOUR_SWITCH).click()
                else:
                    self.driver.find_element(*ColourLightPageLocators.SCHEDULE_TONE_COLOUR_SWITCH).click()
                    self.driver.find_element(*ColourLightPageLocators.SCHEDULE_COLOUR_SWITCH).click()
        else:
            return True
        if str(strTargetColour) == 'RED':
            self.driver.find_element(*ColourLightPageLocators.RED_LEFT).click()
        elif str(strTargetColour) == 'RED ORANGE':
            self.driver.find_element(*ColourLightPageLocators.RED_ORANGE).click()
        elif str(strTargetColour) == 'ORANGE':
            self.driver.find_element(*ColourLightPageLocators.ORANGE).click()
        elif str(strTargetColour) == 'ORANGE YELLOW':
            self.driver.find_element(*ColourLightPageLocators.ORANGE_YELLOW).click()
        elif str(strTargetColour) == 'YELLOW':
            self.driver.find_element(*ColourLightPageLocators.YELLOW).click()
        elif str(strTargetColour) == 'YELLOW GREEN':
            self.driver.find_element(*ColourLightPageLocators.YELLOW_GREEN).click()
        elif str(strTargetColour) == 'GREEN':
            self.driver.find_element(*ColourLightPageLocators.GREEN).click()
        elif str(strTargetColour) == 'GREEN CYAN':
            self.driver.find_element(*ColourLightPageLocators.GREEN_CYAN).click()
        elif str(strTargetColour) == 'CYAN':
            self.driver.find_element(*ColourLightPageLocators.CYAN).click()
        elif str(strTargetColour) == 'CYAN BLUE':
            self.driver.find_element(*ColourLightPageLocators.CYAN_BLUE).click()
        elif str(strTargetColour) == 'BLUE':
            self.driver.find_element(*ColourLightPageLocators.BLUE).click()
        elif str(strTargetColour) == 'BLUE MAGENTA':
            self.driver.find_element(*ColourLightPageLocators.BLUE_MAGENTA).click()
        elif str(strTargetColour) == 'MAGENTA':
            self.driver.find_element(*ColourLightPageLocators.MAGENTA).click()
        elif str(strTargetColour) == 'MAGENTA PINK':
            self.driver.find_element(*ColourLightPageLocators.MAGENTA_PINK).click()
        elif str(strTargetColour) == 'PINK':
            self.driver.find_element(*ColourLightPageLocators.PINK).click()
        elif str(strTargetColour) == 'PINK RED':
            self.driver.find_element(*ColourLightPageLocators.PINK_RED).click()
        time.sleep(5)

        #strCurrentTone = oTargColourElement.text

        #if strCurrentTone == strTargetTone:
            #return True
        #else:
            #return False

    #Highlight Element on the webpafe
    def highlight(self, element):
        """Highlights (blinks) a Selenium Webdriver element"""
        driver = element._parent
        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                  element, s)
        original_style = element.get_attribute('style')
        apply_style("background: yellow; border: 2px solid red;")
        time.sleep(.3)
        apply_style(original_style)

    #The Schedule Row on the Table on Web Application for the  given Day
    def get_SchedRow(self, oSchedRowElLst, strDay):
        intDayIndexCntr = 0
        for oSchedRow in oSchedRowElLst:
            if len(oSchedRow.get_attribute('data-reactid')) == 9:
                strActDay = self.webDayList[intDayIndexCntr]
                if strDay == strActDay:
                    return oSchedRow
                intDayIndexCntr +=1

    #Get StartX int15MinLen
    def get_15min_Xlen(self):
        oTimeScaleStartEl = self.driver.find_element(*HeatingPageLocators.TIME_SCALE_FIRST)
        oTimeScaleEndEl = self.driver.find_element(*HeatingPageLocators.TIME_SCALE_LAST)
        fltStartX = oTimeScaleStartEl.location['x']
        flt15MinLen = (oTimeScaleEndEl.location['x'] - fltStartX) / (24 * 4)
        return flt15MinLen, fltStartX

    #First Set all event to Last one
    def set_all_events_to_last(self, oEventList, intLstEvntXPos):
        for intC in range(len(oEventList)-1, 0, -1):
            evnt = oEventList[intC]
            if not evnt.get_attribute('class') == 'desktop-event-container event-overlap':
                evntDotEl = evnt.find_elements_by_tag_name('div')[1]
            else: evntDotEl = evnt
            self.highlight(evntDotEl)
            #time.sleep(3)
            offsetX = intLstEvntXPos - evntDotEl.location['x']
            #if not float(offsetX) == 0.0:
            action = ActionChains(self.driver)
            action.drag_and_drop_by_offset(evntDotEl, offsetX, 5).perform()
            evnt.click()

    #Remove events
    def remove_events(self, intDelEventCount):
        intButtonCenterY = 27
        intEventMinusButtonX = 190
        intSchedBtnBtnX = 60
        #Click Schedule Options button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intSchedBtnBtnX, intButtonCenterY).click().perform()
        time.sleep(1)
        #Click Minus button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intEventMinusButtonX, intButtonCenterY).click().perform()
        time.sleep(1)

        # Deleting Event
        for intCntr in range(0, intDelEventCount):
            print(intCntr)
            oCurEvent = self.oSourceSchedList[intCntr]
            print(oCurEvent)
            intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                oCurEvent[0]) / 15) * self.intWidthOf15Min
            if intCntr == len(self.oSourceSchedList) - 1:
                intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
            else:
                intNextEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                    self.oSourceSchedList[intCntr + 1][0]) / 15) * self.intWidthOf15Min
            intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition) / 2
            intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid
            # Click on events that needs to be deleted
            action = ActionChains(self.oSchedTableEL.parent)
            action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos, self.intYDay).click().perform()
            time.sleep(1)
            self.oSourceSchedList.remove(oCurEvent)

        # Click Schedule Options Cancel button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intSchedBtnBtnX, intButtonCenterY).click().perform()
        time.sleep(2)

    # Remove events
    def remove_events_V3(self, intDelEventCount):
        # Click Minus button
        oDeleteButton = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_DELETE_BUTTON)
        oDeleteButton.click()
        time.sleep(2)
        #self.oSvgSlotsOnThatDay = self.oSvgDayList[self.intYDay].find_elements_by_xpath('.//*[@class="sc-gldTML cItZkp"]')

        # Deleting Event
        for intCntr in range(0, intDelEventCount):
            print(intCntr)
            oCurEvent = self.oSourceSchedList[intCntr]
            print(oCurEvent)
            #NEed a logic here
            self.oSvgDayList[self.intYDay].click()
            time.sleep(2)
            self.oSvgSlotsOnThatDay[(intCntr + (intCntr + 2))].click()
            time.sleep(2)

            self.oSourceSchedList.remove(oCurEvent)

        # Click Schedule Options Cancel button
        oDeleteButton.click()
        time.sleep(2)

    def add_events_V3(self, intEventsToAdd):
        # Get schedule option button details
        #intButtonCenterY = 27
        #intSchedBtnBtnX = 60
        #intEventAddButtonX = 110

        #To get current event starting time
        self.oSvgSlotsOnThatDay = self.oSvgDayList[self.intYDay].find_elements(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_EVENTS)
        self.oSvgDayList[self.intYDay].click()
        time.sleep(2)
        self.oSvgSlotsOnThatDay[2].click()
        time.sleep(2)
        oTextFromTime = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER).text

        # Click Add button
        oAddButton = self.driver.find_elements(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_ADD_BUTTON)
        oAddButton.click()
        time.sleep(2)

        #+ button inside the events
        #self.oSvgDayList[self.intYDay].click()
        #time.sleep(2)
        oSvgAddSlot = self.driver.find_elements_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_PLUS_BUTTONS)
        #self.oSvgSlotsOnThatDay = self.oSvgDayList[self.intYDay].find_elements_by_xpath('.//*[@class="sc-gldTML cItZkp"]')
        #self.oSvgSlotsOnThatDay[3].click()
        #time.sleep(2)

        # Adding Event
        for intCntr in range(0, intEventsToAdd):
            print(intCntr)
            oSvgAddSlot[0].click()
            time.sleep(2)
            self.oSourceSchedList.insert(intCntr, (oTextFromTime, 'OFF'))

            oHours = oTextFromTime[:2]
            oHours = int(oHours)
            oMinutes = oTextFromTime[3:]
            oMinutes = int(oMinutes)
            oHoursIntoMinutes = oHours * 60
            oTotalMinutes = oHoursIntoMinutes + oMinutes
            oTextFromTime = str(oTotalMinutes + 15)

            #oCurEvent = self.oSourceSchedList[intCntr]
            #print(oCurEvent)
            #self.oSvgSlotsOnThatDay[(intCntr + (intCntr + 3))].click()
            #self.oSourceSchedList.remove(oCurEvent)


        # Add events

    def add_events(self, intEventsToAdd):
        # Get schedule option button details
        intButtonCenterY = 27
        intSchedBtnBtnX = 60
        intEventAddButtonX = 110

        # Click Schedule Options button

        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intSchedBtnBtnX, intButtonCenterY).click().perform()

        # Click Add button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intEventAddButtonX, intButtonCenterY).click().perform()

        # Load Event Positions to List
        oSourceEventPosList = [self.intWidthLeftPad]
        for oEvent in self.oSourceSchedList:
            intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                oEvent[0]) / 15) * self.intWidthOf15Min
            oSourceEventPosList.append(intCurrentEventStartPosition)
        print(oSourceEventPosList)

        # Get Event Positions to add
        oEventToAddPosList = []
        intStartPosToClick = oSourceEventPosList[1]
        intEventIndexCntr = 0
        while True:
            intStartPosToClick = intStartPosToClick + self.intWidthOf15Min
            if not intStartPosToClick in oSourceEventPosList:
                oEventToAddPosList.append(intStartPosToClick)
                if self.oSourceSchedList[intEventIndexCntr][1] == 'ON' or self.oSourceSchedList[intEventIndexCntr][
                    1] == 'OFF':
                    if self.oSourceSchedList[intEventIndexCntr][1] == 'ON':
                        fltNewTargTemp = 'OFF'
                    else:
                        fltNewTargTemp = 'ON'
                    print(intEventIndexCntr, intStartPosToClick, self.oSourceSchedList[intEventIndexCntr][1],
                          fltNewTargTemp)
                else:
                    if self.oSourceSchedList[intEventIndexCntr][1] == 99.0:
                        fltNewTargTemp = 0.0
                    else:
                        fltNewTargTemp = 99.0
                    print(intEventIndexCntr, intStartPosToClick, float(self.oSourceSchedList[intEventIndexCntr][1]),
                          fltNewTargTemp)
                self.oSourceSchedList.insert(intEventIndexCntr + 1, (intStartPosToClick, fltNewTargTemp))
                intEventIndexCntr = intEventIndexCntr + 1
            else:
                intEventIndexCntr = intEventIndexCntr + 1
            if len(oEventToAddPosList) >= intEventsToAdd:
                break
        print(self.oSourceSchedList)

        # Click on new event Position to add
        for oPos in oEventToAddPosList:
            action = ActionChains(self.oSchedTableEL.parent)
            print(oPos)
            action.move_to_element_with_offset(self.oSchedTableEL, oPos,
                                               self.intYDay).click_and_hold().release().perform()
            time.sleep(2)

        # Click Schedule Options Cancel button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intSchedBtnBtnX, intButtonCenterY).click().perform()
        time.sleep(2)

    # Set Schedule Start times for the given schedule for the day
    def set_event_start_times(self, oEventListEL, oSchedList, intLstEvntXPos):
        for intC in range(0, len(oSchedList)):
            evnt = oEventListEL[intC + 1]
            int15MinLen = self.get_15min_Xlen()
            fltStartX = int15MinLen[1]
            int15MinLen = int15MinLen[0]
            intCurEvntXPos = fltStartX + (tt.timeStringToMinutes(oSchedList[intC][0]) / 15) * int15MinLen
            offSetVal = intLstEvntXPos - intCurEvntXPos
            if not offSetVal == 0.0:
                action = ActionChains(self.driver)
                action.drag_and_drop_by_offset(evnt, -offSetVal, 5).perform()
                evnt.click()
                time.sleep(1)
        time.sleep(2)


    def navigate_to_settingScreen(self, strPageName):
        if self.reporter.ActionStatus:
            try:
                if strPageName == 'NOTIFICATION':
                    landingPage = self.driver.find_element(*HeatingDashboardLocators.NOTIFICATION_LINK)
                if strPageName == 'Manage Device':
                    landingPage = self.driver.find_element(*HeatingDashboardLocators.MANAGE_DEVICE_LINK)
                    # if (strPageName == 'Install Device') :
                    # landingPage = self.driver.find_element(*HeatingDashboardLocators.INSTALL_DEVICE_LINK)
                    # if (strPageName == 'Change Password') :
                    # landingPage = self.driver.find_element(*HeatingDashboardLocators.CHANGE_PASSWORD_LINK)
                    # if (strPageName == 'Text Control') :
                    # landingPage = self.driver.find_element(*HeatingDashboardLocators.TEXT_CONTROL_LINK)
                    # if (strPageName == 'Holiday Mode') :
                    # landingPage = self.driver.find_element(*HeatingDashboardLocators.HOLIDAY_MODE_LINK)


                if self.wait_for_element_exist(*HeatingDashboardLocators.SETTINGS_MENU):
                    oMoveToSettings = self.driver.find_element(*HeatingDashboardLocators.SETTINGS_MENU)
                    action = ActionChains(self.driver).move_to_element(oMoveToSettings)
                    action.perform()
                time.sleep(2)

                try :
                    landingPage.click()
                    if self.wait_for_element_exist(*HeatingNotificationLocators.TITLE_LABEL):
                        time.sleep(1)
                        self.report_done('Web App : Navigation to Notification screen is successful')

                except NoSuchElementException as z :
                    self.report_fail('Web App : No Such link exists in Settings menu')
            except:
                self.report_fail('Web App : NoSuchElementException: in get_heating_attribute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))


#Page Class for Login page. Has all the methods for the Login page
class LoginPage(BasePage):
    # Log in to the Hive Mobile App

    def login_hive_app(self, strUserName, strPassword):
        try:

            if self.wait_for_element_exist(*LoginPageLocatorsV3.TITLE_LABEL):
                self.driver.find_element(*LoginPageLocatorsV3.COOKIES_CLOSE_LINK).click()
                self.driver.find_element(*LoginPageLocatorsV3.USERNAME_EDTBOX).send_keys(strUserName)
                self.driver.find_element(*LoginPageLocatorsV3.PASSWORD_EDTBOX).send_keys(strPassword)
                self.driver.find_element(*LoginPageLocatorsV3.LOGIN_BUTTON).click()
                if self.wait_for_element_exist(*DashboardLocatorsV3.DATE_AND_TIME):

                    self.report_pass('Web App : The Hive Desktop Application is successfully Logged in')
                    # if self.wait_for_element_exist(*HeatingPageLocators.MY_HIVE_LINK):
                    # self.report_pass('Web App : The Hive Desktop Application is successfully Logged in')

                    # elif self.wait_for_element_exist(*HeatingPageLocators.MY_HIVE_MENU):
                    # self.report_pass('Web App : The Hive Desktop Application is successfully Logged in')

                else:
                    self.report_fail(
                        'Web App : The Hive Desktop Application is not logged in. Please check the Login credentials and re-execute test.')
            else:
                self.report_fail(
                    'Web App : The Hive Desktop Application is either not Launched or the Login screen is not displayed. Please check and re-execute test.')

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in login_hive_app Method'.format(e))

class HoneycombDashboardPage(BasePage):

    def navigate_to_heating_product_page(self):
        if self.reporter.ActionStatus:
            try :
                if self.wait_for_element_exist(*DashboardLocators.HEATING_THUMBNAIL):
                    if self.wait_for_element_exist(*DashboardLocators.HEATING_THUMBNAIL_OFFLINE):
                        self.report_fail('Web App : Device is Offline ')
                    else:
                        self.driver.find_element(*DashboardLocators.HEATING_THUMBNAIL).click()
                        self.report_pass('Web App : Successfully navigated to the Heating product page')
            except:
                self.report_fail('Web App : NoSuchElementException: in navigate_to_heating_product_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    def navigate_to_hot_water_product_page(self):
        if self.reporter.ActionStatus:
            try :
                if self.wait_for_element_exist(*DashboardLocators.HOTWATER_THUMBNAIL):
                    if self.wait_for_element_exist(*DashboardLocators.HOTWATER_THUMBNAIL_OFFLINE):
                        self.report_fail('Web App : Device is Offline ')
                    else:
                        self.driver.find_element(*DashboardLocators.HOTWATER_THUMBNAIL).click()
                        self.report_pass('Web App : Successfully navigated to the Hotwater product page')
            except:
                self.report_fail(
                    'Web App : NoSuchElementException: in navigate_to_hot_water_product_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def navigate_to_active_plug_product_page(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*DashboardLocators.ACTIVEPLUG_THUMBNAIL):
                    if self.wait_for_element_exist(*DashboardLocators.ACTIVEPLUG_THUMBNAIL_OFFLINE):
                        self.report_fail('Web App : Device is Offline ')
                    else:
                        self.driver.find_element(*DashboardLocators.ACTIVEPLUG_THUMBNAIL).click()
                        self.report_pass('Web App : Successfully navigated to the Active Plug product page')
            except:
                self.report_fail(
                    'Web App : NoSuchElementException: in navigate_to_active_plug_product_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))


    def navigate_to_active_plug_product_page_V3(self):
        if self.reporter.ActionStatus:

            self.driver.get("https://staging-my.hivehome.com/products/activeplug/4058687b-b73e-4315-a695-2b31377391ea")
            time.sleep(10)

    def navigate_to_holiday_mode_page(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingDashboardLocators.SETTINGS_MENU):
                    if self.wait_for_element_exist(*DashboardLocators.HEATING_THUMBNAIL_OFFLINE):
                        self.report_fail('Web App : Heating Device is Offline ')
                    else:
                        oSettings = self.driver.find_element(*HeatingDashboardLocators.SETTINGS_MENU)
                        oHover = ActionChains(self.driver).move_to_element(oSettings)
                        oHover.perform()
                        time.sleep(3)
                        self.driver.find_element(*HolidayModePageLocators.HOLIDAY_MENU_OPTION).click()
                        self.report_pass('Web App : Successfully navigated to the Holiday Mode page')
            except:
                self.report_fail(
                    'Web App : NoSuchElementException: in navigate_to_holiday_mode_page Method\n {0}'.format(
                        traceback.format_exc().replace('File', '$~File')))

    def navigate_to_warm_white_light_product_page(self):
        if self.reporter.ActionStatus:
            try:
                self.driver.find_element(*DashboardLocators.DASHBOARD_CONTENT).get_attribute(
                'childElementCount')
                try:
                    if self.wait_for_element_exist(*DashboardLocators.WARMWHITE_THUMBNAIL):
                        self.driver.find_element(*DashboardLocators.WARMWHITE_THUMBNAIL).click()
                    else:
                        self.wait_for_element_exist(*DashboardLocators.WARMWHITE_THUMBNAIL_OFFLINE)
                        self.report_fail('Web App : Device is Offline ')
                    self.report_pass('Web App : Successfully navigated to the Warm White light product page')
                except:
                    self.report_fail(
                                 'Web App : NoSuchElementException: in navigate_to_warm_white_light_product_page Method\n {0}'.format(
                                        traceback.format_exc().replace('File', '$~File')))
            except:
                print('Already in Warm white product page')

    def navigate_to_device_product_pageV3(self,deviceNodeID):
        if self.reporter.ActionStatus:
            exitLoop = 0
            try:
                if self.wait_for_element_exist(*DashboardLocatorsV3.DASHBOARD_VIEW_SELECTOR):
                    print(deviceNodeID)
                    for a in range(0,10):
                        if exitLoop == 1:
                            break
                        if a!=0 and a!=1:
                            self.driver.find_element(*DashboardLocatorsV3.RIGHT_ARROW).click()
                            time.sleep(1)
                        for b in range(0,7):
                            oDashboardCell = self.driver.find_element(*DashboardLocatorsV3.dashboard_traverse(str(a),str(b)))
                            DashboardID = oDashboardCell.get_attribute("id")
                            if str(DashboardID)==str(deviceNodeID):
                                action = ActionChains(self.driver).click_and_hold(oDashboardCell)
                                action.perform()
                                time.sleep(0.15)
                                action1 = ActionChains(self.driver).release(oDashboardCell)
                                action1.perform()
                                exitLoop = 1
                                break
            except:
                print('Already in the product page')

    def navigate_to_tuneable_light_product_page(self):
        if self.reporter.ActionStatus:
            try:
                if self.driver.find_element(*DashboardLocators.DASHBOARD_CONTENT).get_attribute('childElementCount'):
                    try:
                        if self.wait_for_element_exist(*DashboardLocators.TUNEABLE_THUMBNAIL):
                          self.driver.find_element(*DashboardLocators.TUNEABLE_THUMBNAIL).click()
                        else:
                            self.wait_for_element_exist(*DashboardLocators.TUNEABLE_THUMBNAIL_OFFLINE)
                            self.report_fail('Web App : Device is Offline ')
                        self.report_pass('Web App : Successfully navigated to the Tuneable light product page')
                    except:
                        self.report_fail(
                                   'Web App : NoSuchElementException: in navigate_to_tuneable_light_product_page Method\n {0}'.format(
                                          traceback.format_exc().replace('File', '$~File')))
            except:
                print('Already in Tuneable product page')

    def navigate_to_colour_light_product_page(self):
        if self.reporter.ActionStatus:
            try:
               if self.driver.find_element(*DashboardLocators.DASHBOARD_CONTENT).get_attribute('childElementCount'):
                try:
                    if self.wait_for_element_exist(*DashboardLocators.COLOUR_THUMBNAIL):
                        self.driver.find_element(*DashboardLocators.COLOUR_THUMBNAIL).click()
                    else:
                        self.wait_for_element_exist(*DashboardLocators.COLOUR_THUMBNAIL_OFFLINE)
                        self.report_fail('Web App : Device is Offline ')
                    self.report_pass('Web App : Successfully navigated to the Colour light product page')
                except:
                    self.report_fail(
                            'Web App : NoSuchElementException: in navigate_to_colour_light_product_page Method\n {0}'.format(
                                traceback.format_exc().replace('File', '$~File')))
            except:
                print('Already in Colour product page')

    def navigate_to_motion_sensor_product_page(self):
        try:
            self.driver.get("https://staging-my.hivehome.com/products/motionsensor/d859103d-c868-4db1-8c55-5dcf9083e50e")
            time.sleep(10)
        except:
            self.report_fail('Web App : NoSuchElementException: in navigate_to_motion_sensor_product_page Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))


class HeatingDashboardPage(BasePage):

    def logout(self):
        #if self.reporter.ActionStatus:
            try:
                oMoveToSettings = self.driver.find_element(*HeatingDashboardLocators.SETTINGS_MENU)
                action = ActionChains(self.driver).move_to_element(oMoveToSettings)
                action.perform()
                self.driver.find_element(*HeatingDashboardLocators.LOGOUT_LINK).click()

            except NoSuchElementException as z :
                self.report_fail('Web App : NoSuchElementException: {0} in logout method'.format(z.strerror))

#Page Class for Heating page. Has all the methods for the Heating page
class HeatingPage(BasePage):
    #Set Heat mode
    def set_heat_mode(self, strMode):
        try:

            if self.wait_for_element_exist(*HeatingPageLocators.HEAT_MODE_GROUP):
                self.driver.refresh()
                time.sleep(5)
                if self.wait_for_element_exist(*HeatingPageLocators.STOP_BOOST_BUTTON):
                    if self.driver.find_element(*HeatingPageLocators.STOP_BOOST_BUTTON).is_displayed():
                        self.driver.find_element(*HeatingPageLocators.STOP_BOOST_BUTTON).click()
                        time.sleep(5)
                        self.driver.refresh()
                        time.sleep(5)
                self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                if strMode.upper() == 'AUTO': self.driver.find_element(*HeatingPageLocators.SCHEDULE_MODE_LINK).click()
                elif strMode.upper() == 'MANUAL': self.driver.find_element(*HeatingPageLocators.MANUAL_MODE_LINK).click()
                elif strMode.upper() == 'OFF': self.driver.find_element(*HeatingPageLocators.OFF_MODE_LINK).click()
                elif strMode.upper() == 'BOOST': self.driver.find_element(*HeatingPageLocators.BOOST_MODE_LINK).click()
                time.sleep(5)
                self.driver.refresh()
                if self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL):
                    self.report_pass('Web App : Successfully Heat mode is set to <B>' + strMode)
                    '''
                    oTargTempElement = self.driver.find_element(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                    fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
                    if fltCurrentTargTemp is None and strMode == 'MANUAL':
                        self.click_element_on_position(oTargTempElement, 'Top')
                        self.click_element_on_position(oTargTempElement, 'Bottom')
                        fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
                    if not fltCurrentTargTemp is None: fltCurrentTargTemp = float(fltCurrentTargTemp)
                    '''
                    return None
                else:
                    self.report_fail('Web App : Unable to set Heat mode to <B>' + strMode)
            else:
                self.report_fail("Web App : Control not active on the Heating Page to set the Heat Mode")

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_heat_mode Method'.format(e.strerror))

    # Set Target Temperature
    def set_target_temperature(self, fltTargetTemperature):
        try:
            if self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL):
                self.driver.refresh()
                self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                oTargTempEL = self.driver.find_element(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                boolSetTargTemp = self._set_target_temperature(oTargTempEL, fltTargetTemperature)

                self.driver.refresh()
                self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)

                if boolSetTargTemp:
                    self.report_pass('Web App : The Target Temperature is successfully set to : ' + str(fltTargetTemperature))
                else:
                    self.report_fail('Web App : Unable to set the Target Temperature to : ' + str(fltTargetTemperature))
            else:
                self.report_fail("Web App : Control not active on the Heating Page to set the Target Temperature")

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_target_temperature Method'.format(e.strerror))

    #Set Heating Schedule
    def set_heating_schedule(self, oSourceSchedDict, oDestSchedDict):
        try:
            if self.wait_for_element_exist(*HeatingPageLocators.HEATING_SCHEDULE_MAIN):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                # Get StartX int15MinLen
                self.oSchedTableEL = self.driver.find_element(*HeatingPageLocators.HEATING_SCHEDULE_MAIN)

                # Setup Initial Configs
                self.intWidthLeftPad = 60
                intWidthRightPad = 30
                intWidthOfCavas = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfCavas - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule / 24) / 4
                print(self.intWidthOf15Min)

                for strDay in oDestSchedDict.keys():
                    # Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    self.intYDay = 100 + 40 * (oWeekDayList.index(strDay))

                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount:
                        self.remove_events(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount:
                        self.add_events(intDestListCount - intSourceListCount)
                    print(intSourceListCount, intDestListCount)

                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    # Get Last events position
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intLstEvntXPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                        strLstEvntStTime) / 15) * self.intWidthOf15Min
                    intLastEventMoveToPosition = len(self.oSourceSchedList) * self.intWidthOf15Min
                    intLastEventInitialOffset = - (intLstEvntXPos - intLastEventMoveToPosition)
                    # And move all the events to the beginning
                    action = ActionChains(self.oSchedTableEL.parent)
                    action.move_to_element_with_offset(self.oSchedTableEL, intLstEvntXPos, self.intYDay).click_and_hold().move_by_offset(intLastEventInitialOffset, 0).release().perform()
                    time.sleep(2)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    #Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList)-1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]
                        intCurEvntDestPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                        intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntSourcePos,
                                                           self.intYDay).click_and_hold().move_by_offset(
                            intCurOffsetPos, 0).release().perform()
                        # time.sleep(2)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set Target temperature to for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)
                        intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        if intCntr == len(self.oDestSchedList) - 1:
                            intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
                        else:
                            intNextEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                                self.oDestSchedList[intCntr + 1][0]) / 15) * self.intWidthOf15Min
                        intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition) / 2
                        intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos,
                                                           self.intYDay).click().perform()
                        time.sleep(2)
                        self.report_pass(
                            'Web App : For Day  : ' + strDay + ' Before Target Temperatures for Event number ' + str(
                                intCntr + 1) + ' is set')
                        fltSetTargTemp = float(oCurEvent[1])
                        if self.wait_for_element_exist(*HeatingPageLocators.SCHEDULE_TARGET_TEMPERATURE_SCROLLV6):
                            oSchedTargTemScrollEL = self.driver.find_element(
                                *HeatingPageLocators.SCHEDULE_TARGET_TEMPERATURE_SCROLLV6)
                            self._set_target_temperature(oSchedTargTemScrollEL, fltSetTargTemp)
                            self.report_pass(
                                'Web App : For Day  : ' + strDay + ' After Target Temperatures for Event number ' + str(
                                    intCntr + 1) + ' is set')
                        else:
                            self.report_fail(
                                'Web App : For Day  : ' + strDay + ' Target Temperatures Object for Event number ' + str(
                                    intCntr + 1) + ' is not displayed')

                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Temperatures are set')

                self.driver.find_element(*HeatingPageLocators.SAVE_BUTTONV6).click()
                self.report_pass('Web App : Heating Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Heating Page to set the Heating Schedule")

        except:
            self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Set Heating Schedule
    def set_heating_scheduleV5(self, oScheduleDict):
        try:
            if self.wait_for_element_exist(*HeatingPageLocators.HEATING_SCHEDULE_TABLE):
                # Get StartX int15MinLen
                int15MinLen = self.get_15min_Xlen()
                fltStartX = int15MinLen[1]
                int15MinLen = int15MinLen[0]

                # Heating Schedule Table
                oSchedTableEl = self.driver.find_element(*HeatingPageLocators.HEATING_SCHEDULE_TABLE)
                oSchedRowElLst = oSchedTableEl.find_elements_by_tag_name('li')

                for strDay in oScheduleDict.keys():
                    # strDay = 'fri'
                    oSchedList = oScheduleDict[strDay]
                    oSchedList = oSchedUtils.remove_duplicates(oSchedList)
                    oSchedRow = self.get_SchedRow(oSchedRowElLst, strDay)
                    self.highlight(oSchedRow)
                    oEventList = oSchedRow.find_elements_by_tag_name('li')
                    strLstEvntStTime = oSchedList[len(oSchedList) - 1][0]
                    intLstEvntXPos = fltStartX + (tt.timeStringToMinutes(strLstEvntStTime) / 15) * int15MinLen
                    print(fltStartX, int15MinLen)
                    print(intLstEvntXPos, strLstEvntStTime)
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')

                    # First Set all event to Last one
                    self.set_all_events_to_last(oEventList, intLstEvntXPos)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    # Set all events start time
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events Start Times are set')
                    oEventListEL = oSchedRow.find_elements_by_tag_name('li')
                    self.set_event_start_times(oEventListEL, oSchedList, intLstEvntXPos)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set all events Target Temperature
                    self.report_done(
                        'Web App : For Day  : ' + strDay + ' Before all events Target Temperatures are set')
                    oEventListEL = oSchedRow.find_elements_by_tag_name('li')
                    for intC in range(0, len(oSchedList)):
                        intEvntCntr = intC + 1
                        if intC == len(oSchedList) - 1:
                            intEvntCntr = 6
                        fltSetTargTemp = float(oSchedList[intC][1])
                        oEvent = oEventListEL[intEvntCntr]
                        if not oEvent.get_attribute('class') == 'desktop-event-container event-overlap':
                            evntTempEl = oEvent.find_elements_by_tag_name('div')[0]
                            fltTargTemp = float(evntTempEl.get_attribute('class').split('temp')[1].replace('-', '.'))
                            if not fltSetTargTemp == fltTargTemp:
                                evntTempEl.click()
                                time.sleep(1)
                                oTargTempElement = self.driver.find_elements(
                                    *HeatingPageLocators.SCHEDULE_TARGET_TEMPERATURE_SCROLL)
                                self.set_target_temperature(oTargTempElement[1], fltSetTargTemp)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Temperatures are set')

                self.driver.find_element(*HeatingPageLocators.SAVE_BUTTON).click()
                self.report_pass('Web App : Heating Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Heating Page to set the Heating Schedule")

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_heating_schedule Method'.format(e.strerror))

    # Get Attributes for Heating Controls
    def get_heating_attribute(self):
        if self.reporter.ActionStatus:
            strMode = 'OFF'
            strRunningState = '0000'
            fltCurrentTargTemp = 0.0
            try:
                self.refresh_page()
                if self.wait_for_element_exist(*HeatingPageLocators.HEAT_MODE_GROUP):
                    oHMGEL = self.driver.find_element(*HeatingPageLocators.HEAT_MODE_GROUP)
                    print(oHMGEL.find_element(*HeatingPageLocators.STOP_BOOST_BUTTON).is_displayed())
                    if oHMGEL.find_element(*HeatingPageLocators.STOP_BOOST_BUTTON).is_displayed():
                        strMode = 'BOOST'
                    else:
                        strMode = oHMGEL.find_element(*HeatingPageLocators.CURRENT_MODE_ITEM).text.upper()
                        if 'SCHEDULE' in strMode: strMode = 'AUTO'

                    oTargTempElement = self.driver.find_element(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                    fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
                    if fltCurrentTargTemp is None:
                        self.click_element_on_position(oTargTempElement, 'Top')
                        self.click_element_on_position(oTargTempElement, 'Bottom')
                        fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
                    fltCurrentTargTemp = float(fltCurrentTargTemp)

                    if oHMGEL.find_element(
                            *HeatingPageLocators.RUNNING_STATE_FLAME_ICON).is_displayed(): strRunningState = '0001'
                    print(strMode, fltCurrentTargTemp, strRunningState)

                else:
                    self.report_fail("Web-App : Control not active on the Heating Page to get Heating Attributes")

                self.report_done('Web App : Screenshot while getting attributes')
                if fltCurrentTargTemp == 7.0: fltCurrentTargTemp = 1.0
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('Web App : NoSuchElementException: in get_heating_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

# Page Class for Hot Water page. Has all the methods for the Hot Water page
class HotWaterPage(BasePage):
    # Set Hot Water mode
    def set_hot_water_mode(self, strMode):
        try:
            if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP):
                if self.driver.find_element(*HotWaterPageLocators.STOP_BOOST_BUTTON).is_displayed():
                    self.driver.find_element(*HotWaterPageLocators.STOP_BOOST_BUTTON).click()
                    time.sleep(5)
                    self.driver.refresh()
                oHotWaterMenuEl = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP)
                self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP)
                if strMode.upper() == 'AUTO':
                    oHotWaterMenuEl.find_element(*HotWaterPageLocators.SCHEDULE_MODE_LINK).click()
                elif strMode.upper() == 'MANUAL':
                    oHotWaterMenuEl.find_element(*HotWaterPageLocators.MANUAL_MODE_LINK).click()
                elif strMode.upper() == 'OFF':
                    oHotWaterMenuEl.find_element(*HotWaterPageLocators.OFF_MODE_LINK).click()
                elif strMode.upper() == 'BOOST':
                    oHotWaterMenuEl.find_element(*HotWaterPageLocators.BOOST_MODE_LINK).click()
                time.sleep(5)
                self.driver.refresh()
                if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP):
                    self.report_pass('Web APP : Successfully Hot Water Mode mode is set to <B>' + strMode)
                else:
                    self.report_fail('Web APP : Unable to set Hot Water mode to <B>' + strMode)
            else:
                self.report_fail("Web App : Control not active on the Hot Water Page to set the Hot Water Mode")

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_Hot Water_mode Method'.format(e.strerror))

    # Set Hot water Schedule
    def set_hot_water_schedule(self, oSourceSchedDict, oDestSchedDict):
        try:
            if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_SCHEDULE_MAIN):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                # Get StartX int15MinLen
                self.oSchedTableEL = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_SCHEDULE_MAIN)

                # Setup Initial Configs
                self.intWidthLeftPad = 60
                intWidthRightPad = 30
                intWidthOfCavas = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfCavas - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule / 24) / 4
                print(self.intWidthOf15Min)

                for strDay in oDestSchedDict.keys():
                    # Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    self.intYDay = 100 + 40 * (oWeekDayList.index(strDay))

                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount:
                        self.remove_events(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount:
                        self.add_events(intDestListCount - intSourceListCount)
                    print(intSourceListCount, intDestListCount)
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    # Get Last events position
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intLstEvntXPos = self.intWidthLeftPad + (tt.timeStringToMinutes(strLstEvntStTime)/15) * self.intWidthOf15Min
                    intLastEventMoveToPosition = len(self.oSourceSchedList) * self.intWidthOf15Min
                    intLastEventInitialOffset = - (intLstEvntXPos - intLastEventMoveToPosition)
                    # And move all the events to the beginning
                    action = ActionChains(self.oSchedTableEL.parent)
                    action.move_to_element_with_offset(self.oSchedTableEL, intLstEvntXPos,
                                                       self.intYDay).click_and_hold().move_by_offset(
                        intLastEventInitialOffset, 0).release().perform()
                    time.sleep(2)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    # Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList) - 1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]
                        intCurEvntDestPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                        intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntSourcePos,
                                                           self.intYDay).click_and_hold().move_by_offset(
                            intCurOffsetPos, 0).release().perform()
                        # time.sleep(2)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set Running State for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)
                        intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        if intCntr == len(self.oDestSchedList) - 1:
                            intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
                        else:
                            intNextEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                                self.oDestSchedList[intCntr + 1][0]) / 15) * self.intWidthOf15Min
                        intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition) / 2
                        intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid

                        self.report_pass(
                            'Web App : For Day  : ' + strDay + ' Before Running State for Event number ' + str(
                                intCntr + 1) + ' is set')
                        if oCurEvent[1] != self.oSourceSchedList[intCntr][1]:
                            action = ActionChains(self.oSchedTableEL.parent)
                            action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos,
                                                               self.intYDay).click().perform()
                            time.sleep(2)
                            self.report_pass(
                                'Web App : For Day  : ' + strDay + ' After Running State for Event number ' + str(
                                    intCntr + 1) + ' is set')

                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Running State are set')

                self.driver.find_element(*HotWaterPageLocators.SAVE_BUTTONV6).click()
                self.report_pass('Web App : Hot Water Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Hot Water Page to set the Heating Schedule")

        except:
            self.report_fail('iOS APP: Exception in set_hot_water_schedule Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

    # Set Hot Water Schedule
    def set_hot_water_scheduleV5(self, oScheduleDict):
        try:
            if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_SCHEDULE_TABLE):
                # Get StartX int15MinLen
                int15MinLen = self.get_15min_Xlen()
                fltStartX = int15MinLen[1]
                int15MinLen = int15MinLen[0]

                # Heating Schedule Table
                oSchedTableEl = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_SCHEDULE_TABLE)
                oSchedRowElLst = oSchedTableEl.find_elements_by_tag_name('li')

                for strDay in oScheduleDict.keys():
                    # strDay = 'fri'
                    oSchedList = oScheduleDict[strDay]
                    oSchedList = oSchedUtils.remove_duplicates(oSchedList)
                    oSchedRow = self.get_SchedRow(oSchedRowElLst, strDay)
                    self.highlight(oSchedRow)
                    oEventList = oSchedRow.find_elements_by_tag_name('li')
                    strLstEvntStTime = oSchedList[len(oSchedList) - 1][0]
                    intLstEvntXPos = fltStartX + (tt.timeStringToMinutes(strLstEvntStTime) / 15) * int15MinLen
                    print(fltStartX, int15MinLen)
                    print(intLstEvntXPos, strLstEvntStTime)
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')

                    # First Set all event to Last one
                    self.set_all_events_to_last(oEventList, intLstEvntXPos)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    # Set all events start time
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events Start Times are set')
                    oEventListEL = oSchedRow.find_elements_by_tag_name('li')
                    self.set_event_start_times(oEventListEL, oSchedList, intLstEvntXPos)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set all events Target Temperature
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events Modes are set')
                    oEventListEL = oSchedRow.find_elements_by_tag_name('li')
                    for intC in range(0, len(oSchedList)):
                        intEvntCntr = intC + 1
                        if intC == len(oSchedList) - 1:
                            intEvntCntr = 6
                        fltSetTargTemp = float(oSchedList[intC][1])
                        if fltSetTargTemp == 99.0:
                            strExpectMode = 'ON'
                        else:
                            strExpectMode = 'OFF'
                        oEvent = oEventListEL[intEvntCntr]
                        if not oEvent.get_attribute('class') == 'desktop-event-container event-overlap':
                            evntModeEl = oEvent.find_elements_by_tag_name('div')[0]
                            strActualMode = evntModeEl.text
                            if not strExpectMode == strActualMode.upper():
                                evntModeEl.click()
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Modes are set')
                oSchedGroupEL = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_SCHEDULE_GROUP)
                oSchedGroupEL.find_element(*HotWaterPageLocators.SAVE_BUTTON).click()
                self.report_pass('Web App : Hot Water Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Hot Water Page to set the Hot Water Schedule")

        except NoSuchElementException as e:
            self.report_fail(
                'Web App : NoSuchElementException: {0} in set_hot_water_schedule Method'.format(e.strerror))

    # Get Attributes for Heating Controls
    def get_hotwater_attribute(self):
        if self.reporter.ActionStatus:
            strMode = 'OFF'
            strRunningState = '0000'
            fltCurrentTargTemp = 0.0
            try:
                self.refresh_page()
                if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP):
                    oHWMGEL = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP)
                    print(oHWMGEL.find_element(*HotWaterPageLocators.STOP_BOOST_BUTTON).is_displayed())
                    if oHWMGEL.find_element(*HotWaterPageLocators.STOP_BOOST_BUTTON).is_displayed():
                        strMode = 'BOOST'
                    else:
                        strMode = oHWMGEL.find_element(*HotWaterPageLocators.CURRENT_MODE_ITEM).text.upper()
                        if 'SCHEDULE' in strMode:
                            strMode = 'AUTO'
                        elif 'ON' in strMode:
                            strMode = 'Always ON'
                        elif 'OFF' in strMode:
                            strMode = 'Always OFF'
                    if oHWMGEL.find_element(*HotWaterPageLocators.HOT_WATER_RUNNING_STATE).get_attribute(
                            'aria-hidden').upper() == 'TRUE': strRunningState = '0001'
                else:
                    self.report_fail("Web-App : Control not active on the Hot Water Page to get Heating Attributes")

                self.report_done('Web App : Screenshot while getting attributes')
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('Web App : NoSuchElementException: in get_hot_water_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

# Page Class for Active plug page. Yet to have all the methods for the Active plug page
class ActivePlugPage(BasePage):
    # Set active plug mode
    def set_active_plug_mode(self, strMode):

        try:
            time.sleep(3)
            if self.wait_for_element_exist(*ActivePlugPageLocators_V3.ACTIVE_PLUG_CONTROLER_GROUP_V3):
                if strMode.upper() == 'MANUAL':
                    oSetPlugMode = self.check_exists_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCHEDULE_V3)
                    if oSetPlugMode:
                        self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_MANUAL_MODE_V3).click()
                        print("Plug mode changed from Schedule to Manual")
                    else:
                        self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCHEDULE_MODE_V3).click()
                        time.sleep(5)
                        self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_MANUAL_MODE_V3).click()
                        print('Plug set to manual mode though it was already in Manual')

                elif strMode.upper() == 'AUTO':
                    oSetPlugMode = self.check_exists_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCHEDULE_V3)
                    if oSetPlugMode:
                        self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_MANUAL_MODE_V3).click()
                        time.sleep(5)
                        self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCHEDULE_MODE_V3).click()
                        print('Plug set to Schedule mode though it was already in Schedule')
                    else:
                        self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCHEDULE_MODE_V3).click()
                        print("Plug mode changed from Schedule to Manual")

                self.report_pass('Web APP : Successfully Plug Mode mode is set to <B>' + strMode)
            else: self.report_fail("Web App : Control not active on the Active plug Page to set the Active Plug Mode")

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in  set_active_plug_mode Method'.format(e.strerror))



    #Get Attributes for Active plug Controls
    def get_activeplug_attribute(self):

        if self.reporter.ActionStatus:
            strMode = 'OFF'
            strRunningState = '0000'
            fltCurrentTargTemp = 0.0
            try:
                self.refresh_page()
                if self.wait_for_element_exist(*ActivePlugPageLocators_V3.ACTIVE_PLUG_CONTROLER_GROUP_V3):
                    oAPMGEL = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_CONTROLER_GROUP_V3)
                    time.sleep(3)
                    oPlugModeMode = self.check_exists_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCHEDULE_V3)
                    if oPlugModeMode: strMode = 'AUTO'
                    else: strMode = 'Always ON'

                    oPlugModeState = self.check_exists_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR)
                    if oPlugModeState:
                        oPlugModeState = self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR).text
                        if oPlugModeState == 'on': strRunningState = '0001'

                else:
                    self.report_fail("Web-App : Control not active on the Active Plug Page to get plug Attributes")
                self.report_done('Web App : Screen shot while getting attributes')
                return strMode, strRunningState, fltCurrentTargTemp

            except:
                self.report_fail('Web App : NoSuchElementException: in get_activeplug_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


    #Sets the active plug state
    def set_activeplug_state(self, strExpectedState):
        try:
            if self.wait_for_element_exist(*ActivePlugPageLocators_V3.ACTIVE_PLUG_CONTROLER_GROUP_V3):
                oAPMGEL = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_CONTROLER_GROUP_V3)
                oSetPlugState = self.check_exists_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR)
                oSetPlugStateText = self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR).text
                if oSetPlugState:
                    if strExpectedState.upper() == 'OFF':
                        oPlugState = oSetPlugStateText
                        if oPlugState.upper() == 'OFF':
                            print("Plug state is already OFF")
                            self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR).click()
                            time.sleep(10)
                            self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR).click()
                            print('Plug state changed from OFF to ON to OFF')
                            time.sleep(10)
                        else:
                            self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR).click()
                            print("Plug state changed from ON to OFF")

                    elif strExpectedState.upper() == 'ON':
                        oPlugState = oSetPlugStateText
                        if oPlugState.upper() == 'ON':
                            print("Plug state already in ON state")
                            self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR).click()
                            time.sleep(10)
                            self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR).click()
                            time.sleep(10)
                            print('Plug state changed from ON to OFF to ON')
                        else:
                            self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_STATE_INDICATOR).click()
                            print("Plug state changed from OFF to ON")
                            time.sleep(5)

                else:
                    print ("Switch not available")
                    self.report_fail("Web App : Switch not available in the active plug page to set the plug state")

                self.report_pass('Web APP : Successfully Plug state is set to <B>' + strExpectedState)
            else:
                self.report_fail("Web App : Control not active on the Active Plug Page to set the plug state")

        except NoSuchElementException as e:
            self.report_fail(  'Web App : NoSuchElementException: {0} in set_activeplug_state Method'.format(e.strerror))


    #Set Active Plug Schedule
    def set_active_plug_schedule(self, oSourceSchedDict, oDestSchedDict):
        try:
            if self.wait_for_element_exist(*ActivePlugPageLocators.ACTIVE_PLUG_SCHEDULE_MAIN):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                # Get StartX int15MinLen
                self.oSchedTableEL = self.driver.find_element(*ActivePlugPageLocators.ACTIVE_PLUG_SCHEDULE_MAIN)

                # Setup Initial Configs
                self.intWidthLeftPad = 60
                intWidthRightPad = 30
                intWidthOfCavas = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfCavas - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule / 24) / 4
                print(self.intWidthOf15Min)

                for strDay in oDestSchedDict.keys():
                    # Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    self.intYDay = 100 + 40 * (oWeekDayList.index(strDay))

                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount:
                        self.remove_events(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount:
                        self.add_events(abs(intDestListCount - intSourceListCount))
                    print(intSourceListCount, intDestListCount)
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    # Get Last events position
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intLstEvntXPos = self.intWidthLeftPad + (tt.timeStringToMinutes(strLstEvntStTime) / 15) * self.intWidthOf15Min
                    intLastEventMoveToPosition = len(self.oSourceSchedList) * self.intWidthOf15Min
                    intLastEventInitialOffset = - (intLstEvntXPos - intLastEventMoveToPosition)
                    # And move all the events to the beginning
                    action = ActionChains(self.oSchedTableEL.parent)
                    action.move_to_element_with_offset(self.oSchedTableEL, intLstEvntXPos,
                                                       self.intYDay).click_and_hold().move_by_offset(
                        intLastEventInitialOffset, 0).release().perform()
                    time.sleep(2)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    # Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList) - 1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]
                        intCurEvntDestPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                        intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntSourcePos,
                                                           self.intYDay).click_and_hold().move_by_offset(
                            intCurOffsetPos, 0).release().perform()
                        # time.sleep(2)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set Running State for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)
                        intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        if intCntr == len(self.oDestSchedList) - 1:
                            intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
                        else:
                            intNextEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                                self.oDestSchedList[intCntr + 1][0]) / 15) * self.intWidthOf15Min
                        intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition) / 2
                        intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid

                        self.report_pass(
                            'Web App : For Day  : ' + strDay + ' Before Running State for Event number ' + str(
                                intCntr + 1) + ' is set')
                        if oCurEvent[1] != self.oSourceSchedList[intCntr][1]:
                            action = ActionChains(self.oSchedTableEL.parent)
                            action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos,
                                                               self.intYDay).click().perform()
                            time.sleep(2)
                            self.report_pass(
                                'Web App : For Day  : ' + strDay + ' After Running State for Event number ' + str(
                                    intCntr + 1) + ' is set')

                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Running State are set')

                self.driver.find_element(*ActivePlugPageLocators.SAVE_BUTTONV6).click()
                print ('Save button clicked')
                self.report_pass('Web App : Active Plug Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Active Plug Page to set the Plug Schedule")

        except:
            self.report_fail('Web APP: Exception in set_active_Plug Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))



    #Set Active Plug Schedule
    def set_active_plug_schedule_V3_new(self, oSourceSchedDict, oDestSchedDict):
        try:
            if self.wait_for_element_exist(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCHEDULE_MAIN_V3):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                # Get StartX int15MinLen
                self.oSchedTableEL = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_CONTROLER_GROUP_V3)
                self.oSvgDayList = []
                for num in range(0, 7):
                    oWeekdayPath = ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_WEEKDAYS + str(num) + '"]'
                    self.oSvgDayListentry = self.driver.find_element_by_xpath(oWeekdayPath)
                    self.oSvgDayList.append(self.oSvgDayListentry)
                print(self.oSvgDayList)

                # Setup Initial Configs
                self.intWidthLeftPad = 40
                intWidthRightPad = 40
                intWidthOfSVG = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfSVG - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule / 24) / 4
                print(self.intWidthOf15Min)

                for strDay in oDestSchedDict.keys():
                    # Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    self.intYDay = oWeekDayList.index(strDay)
                    self.oSvgSlotsOnThatDay = self.oSvgDayList[self.intYDay].find_elements(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_EVENTS)
                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount: self.remove_events_V3(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount: self.add_events_V3(abs(intDestListCount - intSourceListCount))
                    print(intSourceListCount, intDestListCount)
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intNoOf15Mins = tt.timeStringToMinutes(strLstEvntStTime) / 15
                    intNoOf15Mins = int(intNoOf15Mins)
                    intNumberOfEventsOnThatDay = len(self.oSourceSchedList)-1
                    intNumberOfEventsOnThatDay = int(intNumberOfEventsOnThatDay)
                    oXoffset = ((intNumberOfEventsOnThatDay - intNoOf15Mins) * self.intWidthOf15Min)
                    time.sleep(1)
                    self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_COOKIES_CLOSE).click()
                    time.sleep(1)
                    oCloseButton = self.check_exists_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_DAY_CLOSE)
                    if oCloseButton:
                        self.driver.find_element_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_DAY_CLOSE).click()
                    time.sleep(2)
                    oResetSch = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_RESET_SCHEDULE)
                    oResetSch.send_keys(Keys.END)
                    time.sleep(3)
                    self.oSvgSlotsOnThatDay = self.oSvgDayList[self.intYDay].find_elements(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_EVENTS)

                    #self.oSvgSlotsOnThatDay[len(self.oSourceSchedList)*2].click()
                    self.oSvgSlotsOnThatDay[len(self.oSourceSchedList)].click()
                    time.sleep(2)
                    #self.oSvgSlotsOnThatDay[len(self.oSourceSchedList)].click()
                    #time.sleep(2)
                    #self.oSvgSlotsOnThatDay[len(self.oSourceSchedList)*2].click()
                    #time.sleep(2)

                    oEventSlider = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUS_SCH_EVENT_SLIDER)
                    time.sleep(2)
                    ActionChains(self.driver).click_and_hold(oEventSlider).move_by_offset(oXoffset, 0).release().perform()
                    time.sleep(5)

                    oTimeToBeSet = (len(self.oSourceSchedList)-1) * 15
                    if oTimeToBeSet == 60 :  oTimeToBeSet = '0100'
                    elif oTimeToBeSet == 75:  oTimeToBeSet = '0115'
                    else:
                        oTimeToBeSet = str(oTimeToBeSet)
                        while len(oTimeToBeSet) < 4: oTimeToBeSet = '0' + oTimeToBeSet
                        oTimeToBeSet = oTimeToBeSet[:2] + ":" + oTimeToBeSet[2:]

                    oTextFromTime = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER).text
                    if not oTextFromTime == oTimeToBeSet:
                        oFlag = 1
                        while oFlag > 0:
                            oTextFromTime = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER).text
                            intNoOf15Mins = tt.timeStringToMinutes(oTextFromTime) / 15
                            oXoffset = ((len(self.oSourceSchedList)-1) - intNoOf15Mins) * self.intWidthOf15Min
                            ActionChains(self.driver).click_and_hold(oEventSlider).move_by_offset(oXoffset, 0).release().perform()
                            time.sleep(5)
                            oTextFromTime = self.driver.find_element(
                                *ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER).text
                            if oTextFromTime == oTimeToBeSet:  oFlag = 0
                            else: oFlag = oFlag + 1
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    # Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList)-1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]

                        #oCurEventinApp = self.oSvgSlotsOnThatDay[intCntr * 2]
                        oCurEventinApp = self.oSvgSlotsOnThatDay[intCntr]
                        oCurEventinApp.click()
                        time.sleep(3)
                        oTimer = self.check_exists_by_xpath(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER_PATH)
                        if oTimer:
                            oTextFromTime = self.driver.find_element(
                                *ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER).text
                            oCurEventInMinutes = tt.timeStringToMinutes(oTextFromTime)
                            oCurEventSourceTime = oCurEventInMinutes/15
                            intCurEvntDestTime = (tt.timeStringToMinutes(oCurEvent[0])/15)
                            intCurrentEventOffset = (intCurEvntDestTime - oCurEventSourceTime) * self.intWidthOf15Min

                            #intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                            #intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                            # And move the event to the Dest Position
                            oEventSlider = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUS_SCH_EVENT_SLIDER)
                            action = ActionChains(self.driver)
                            action.click_and_hold(oEventSlider).move_by_offset(intCurrentEventOffset, 0).release().perform()
                            time.sleep(4)

                            oTextFromTime = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER).text

                            oDestTimeMinMinus15 = tt.timeStringToMinutes(oCurEvent[0]) - 15
                            oDestHour = oDestTimeMinMinus15 // 60
                            if len(str(oDestHour)) < 2 : oDestHour = '0' + str(oDestHour)
                            oDestMinutes = oDestTimeMinMinus15 % 60
                            if len(str(oDestMinutes)) < 2 : oDestMinutes = '0' + str(oDestMinutes)
                            oDestTimeLessThan15Min = str(oDestHour) + ':' + str(oDestMinutes)

                            if not oTextFromTime == oDestTimeLessThan15Min:
                                oFlag = 1
                                while oFlag > 0:
                                    oTextFromTime = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER).text
                                    intNoOf15Mins = tt.timeStringToMinutes(oTextFromTime) / 15
                                    oXoffset = (intCurEvntDestTime - intNoOf15Mins) * self.intWidthOf15Min
                                    time.sleep(1)
                                    ActionChains(self.driver).click_and_hold(oEventSlider).move_by_offset(oXoffset, 0).release().perform()
                                    time.sleep(4)
                                    oTextFromTime = self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_TIME_FROM_SLIDER).text
                                    if oTextFromTime == oDestTimeLessThan15Min:
                                        oFlag = 0
                                    else:
                                        oFlag = oFlag + 1

                            # time.sleep(2)
                                print("print done")
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set Running State for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        #Need to change the above condition when remove duplicates gets completed
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)
                        oCurrentEventinApp = self.oSvgSlotsOnThatDay[intCntr+1]
                        oCurrentEventinApp.click()
                        oCurrentEventSourceState = oCurrentEventinApp.text.upper()
                        oCurrentEventDestState = self.oDestSchedList[intCntr][1]
                        self.report_pass( 'Web App : For Day  : ' + strDay + ' Before Running State for Event number ' + str(intCntr + 1) + ' is set')
                        if not oCurrentEventSourceState == oCurrentEventDestState:
                            oCurrentEventinApp.click()
                            time.sleep(2)
                            oCurrentEventSourceState = oCurrentEventinApp.text.upper()
                            if oCurrentEventSourceState == oCurrentEventSourceState :
                                print ("All good")
                            else:
                                print ("Something wrong with text in schedule")
                        self.report_pass('Web App : For Day  : ' + strDay + ' After Running State for Event number ' + str(intCntr + 1) + ' is set')

                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Running State are set')

                self.driver.find_element(*ActivePlugPageLocators_V3.ACTIVE_PLUG_SCH_SAVE_BUTTON).click()

                self.report_pass('Web App : Active Plug Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Active Plug Page to set the Plug Schedule")

        except:
            self.report_fail('Web APP: Exception in set_active_Plug Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))


'''
#Holiday mode page class
class HolidayModePage(BasePage):
    #def set_holiday_mode(self, holidayStart, holidayEnd, holidayTemp):



    # Get Attributes for Holiday Mode page
    def get_holiday_mode_attribute(self):
        if self.reporter.ActionStatus:
            strMode = 'OFF'
            #strRunningState = '0000'

            fltCurrentTargTemp = 0.0
            strHolidayStartTime = ''
            strHolidayEndTime = ''

            try:
                self.refresh_page()
                oHolidayScreenEdit = self.check_exists_by_xpath(*HolidayModePageLocators.HOLIDAY_MODE_PAGE_EDIT)

                if not oHolidayScreenEdit:
                    oHolidayEditButton = self.check_exists_by_xpath(*HolidayModePageLocators.HOLIDAY_MODE_PAGE_EDIT_BUTTON)
                    if __name__ == '__main__':
                        if oHolidayEditButton:
                            strMode = 'HOLIDAY'
                            #oDepartureTime =
                            #strHolidayStartTime =
                            print ('Holiday Mode is going to start in Future - Edit button displayed')

                            date = self.driver.find_element_by_xpath(
                                './/div[@class="date-cell columns small-6 left-cell"]/span[@class="date-day ng-binding"]').text
                            Month = self.driver.find_element_by_xpath(
                                './/div[@class="date-cell columns small-6 left-cell"]/span[@class="date-detail ng-binding"]').text

                            strHolidayStartTime = date + Month
                            #Need to convert string into time - if needed




                elif oHolidayScreenEdit:

                    #strMode = ''
                    self.report_fail("Web-App : Holiday mode was not already set for this user")


                    if oHWMGEL.find_element(*HotWaterPageLocators.HOT_WATER_RUNNING_STATE).get_attribute(
                            'aria-hidden').upper() == 'TRUE': strRunningState = '0001'
                else:
                    self.report_fail("Web-App : Control not active on the Hot Water Page to get Heating Attributes")

                self.report_done('Web App : Screenshot while getting attributes')
                return strMode, strRunningState, fltCurrentTargTemp, strHolidayStartTime, strHolidayEndTime
            except:
                self.report_fail('Web App : NoSuchElementException: in get_hot_water_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))
'''

class ForgottenPassword(BasePage):
    def set_screen(self, strScreenName):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*LoginPageLocators.FORGOTTEN_PASSWORD_LINK):
                    self.driver.find_element(*LoginPageLocators.FORGOTTEN_PASSWORD_LINK).click()
                    self.report_pass('Web App : Forgotten Password link clicked successfully')
                    if self.wait_for_element_exist(*ForgottenPasswordPageLocators.TITLE_LABEL):
                        self.report_pass('Web App : Forgotten Password screen loaded successfully')
                    else:
                        self.report_fail('Web App : Forgotten Password screen does not exist')

                else:
                    self.report_fail('Web App : Forgotten Password link is not working')
            except NoSuchElementException as z:
                self.report_fail('Web App : NoSuchElementException: {0} in set_screen method'.format(z.strerror))

    def submit_username(self, strEmailAddr):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*ForgottenPasswordPageLocators.TITLE_LABEL):
                    self.driver.find_element(*ForgottenPasswordPageLocators.EMAIL_ADDR_FIELD).send_keys(strEmailAddr)
                    self.driver.find_element(*ForgottenPasswordPageLocators.SUBMIT_BUTTON).click()
                    time.sleep(4)
                    if self.wait_for_element_exist(*ForgottenPasswordPageLocators.REMINDER_MESSAGE):
                        self.report_pass('Web App : Password reset email is sent successfully')
                        time.sleep(5)
            except NoSuchElementException as z:
                self.report_fail('Web App : NoSuchElementException: {0} in submit_username method'.format(z.strerror))

    def set_new_password(self, strUsername, strNewPassword):
        yopmailURL = 'http://www.yopmail.com/en/'
        if self.reporter.ActionStatus:
            try:
                self.driver.get(yopmailURL)
                self.driver.find_element(*ForgottenPasswordPageLocators.YOPMAIL_EMAIL_ADDR_FIELD).clear()
                self.driver.find_element(*ForgottenPasswordPageLocators.YOPMAIL_EMAIL_ADDR_FIELD).send_keys(strUsername)
                self.driver.find_element(*ForgottenPasswordPageLocators.YOPMAIL_CHECK_INBOX).click()
                time.sleep(5)

                self.driver.switch_to_frame(self.driver.find_element(*ForgottenPasswordPageLocators.FRAME_REF))

                time.sleep(4)
                # if self.wait_for_element_exist(*ForgottenPasswordPageLocators.YOPMAIL_HREF_LINK):
                reset_link = self.driver.find_element(*ForgottenPasswordPageLocators.YOPMAIL_HREF_LINK).get_attribute(
                    'href')
                self.driver.switch_to_default_content()
                self.report_pass('Web App : Password reset email received')
                self.driver.get(reset_link)

                if self.wait_for_element_exist(*ForgottenPasswordPageLocators.PASSWORD_RESET_LABEL):
                    self.driver.find_element(*ForgottenPasswordPageLocators.NEW_PASSWORD).send_keys(strNewPassword)
                    self.driver.find_element(*ForgottenPasswordPageLocators.CONFIRM_PASSWORD).send_keys(strNewPassword)
                    self.driver.find_element(*ForgottenPasswordPageLocators.SUBMIT_BUTTON).click()

                if self.wait_for_element_exist(*ForgottenPasswordPageLocators.SUCCESS_MESSAGE):
                    self.report_pass('Web App : Password reset successful')
                else:
                    self.report_fail('Web App : Password reset failed')

                self.driver.find_element(*ForgottenPasswordPageLocators.LOGIN_BUTTON).click()

            except NoSuchElementException as z:
                self.report_fail(
                    'Web App : NoSuchElementException: {0} in forgotten_password method'.format(z.strerror))

class SetNotification(BasePage):
    def click_element(self, oCheckboxElem, xCoordinator, yCoordinator):
        self.oLoc = oCheckboxElem
        oAction = ActionChains(self.oLoc.parent)
        oAction.move_to_element_with_offset(self.oLoc, xCoordinator, yCoordinator).click().perform()
        return True

    def iteration_count(self, oTargetTemp, oCurrentTemp):
        if oTargetTemp != oCurrentTemp:
            itrCount = int(abs(oTargetTemp - oCurrentTemp) / 0.5)
            return itrCount
        else:
            return 0

    def upDown_decider(self, oTargetTemp, oCurrentTemp, num_iteration, tempUpDown):
        if oTargetTemp > oCurrentTemp:
            for itrCount in range(num_iteration):
                self.click_element(tempUpDown, 51, 15)
        elif oTargetTemp < oCurrentTemp:
            for itrCount in range(num_iteration):
                self.click_element(tempUpDown, 51, 25)
        else:
            print()

    def set_high_temperature(self, oTargetHighTemp, oTargetLowTemp='', oBothAlert='No'):
        if oBothAlert == 'Yes':
            self.driver.refresh()

        if self.reporter.ActionStatus:
            if self.wait_for_element_exist(*HeatingNotificationLocators.TITLE_LABEL):
                try:
                    if not self.driver.find_element(
                            *HeatingNotificationLocators.HIGH_TEMP_CHKBOX).is_selected() == True:
                        self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_CHKBOX).click()
                    tempUpDown = self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_TT)
                    oCurrentTemp = tempUpDown.get_attribute('value')
                    oCurrentTemp = float(oCurrentTemp)
                    time.sleep(1)
                    num_iteration = self.iteration_count(oTargetHighTemp, oCurrentTemp)
                    self.upDown_decider(oTargetHighTemp, oCurrentTemp, num_iteration, tempUpDown)
                    # self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_TT).clear()
                    # self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_TT).send_keys(temp)
                    time.sleep(2)

                    self.report_done('Web App : Target Temperature for High temperature Alert has been set to ' + str(
                        oTargetHighTemp))
                    if oBothAlert == 'Yes':
                        self.set_low_temperature(oTargetLowTemp, oBothAlert)
                    else:
                        self.driver.find_element(*HeatingNotificationLocators.SAVE_BUTTON).click()
                        time.sleep(3)
                        self.report_pass('Web App : High Notification Alert has been successfully set')
                        self.driver.refresh()

                except NoSuchElementException as z:
                    self.report_fail(
                        'Web App : NoSuchElementException: {0} in set_high_temperature method'.format(z.strerror))
        else:
            self.report_fail("Web App : Control not active on the Notification Page to set the notification")

    def set_low_temperature(self, oTargetLowTemp, oBothAlert='No'):
        if self.reporter.ActionStatus:
            if self.wait_for_element_exist(*HeatingNotificationLocators.TITLE_LABEL):
                try:
                    if not self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_CHKBOX).is_selected() == True:
                        self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_CHKBOX).click()
                    tempUpDown = self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_TT)
                    oCurrentTemp = tempUpDown.get_attribute('value')
                    oCurrentTemp = float(oCurrentTemp)
                    time.sleep(1)
                    num_iteration = self.iteration_count(oTargetLowTemp, oCurrentTemp)
                    self.upDown_decider(oTargetLowTemp, oCurrentTemp, num_iteration, tempUpDown)
                    time.sleep(2)
                    self.report_done(
                        'Web App : Target Temperature for Low temperature Alert has been set to ' + str(oTargetLowTemp))
                    time.sleep(1)
                    self.driver.find_element(*HeatingNotificationLocators.SAVE_BUTTON).click()
                    time.sleep(3)
                    if oBothAlert == 'Yes':
                        self.report_pass(
                            'Web App : High Notification & Low Notification Alert has been successfully set')
                    else:
                        self.report_pass('Web App : Low Notification Alert has been successfully set')
                    self.driver.refresh()

                except NoSuchElementException as z:
                    self.report_fail(
                        'Web App : NoSuchElementException: {0} in set_low_temperature method'.format(z.strerror))

            else:
                self.report_fail("Web App : Control not active on the Notification Page to set the notification")

    def setNotificationOnOff(self, strNotiState, strNotiType='Both'):
        if self.reporter.ActionStatus:
            if self.wait_for_element_exist(*HeatingNotificationLocators.TITLE_LABEL):
                try:
                    if strNotiType == 'Both' or strNotiType == 'High':
                        if strNotiState == 'OFF':
                            self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_CHKBOX).click()
                            time.sleep(1)

                    if strNotiType == 'Both' or strNotiType == 'Low':
                        if strNotiState == 'OFF':
                            self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_CHKBOX).click()
                            time.sleep(1)
                    self.driver.find_element(*HeatingNotificationLocators.SAVE_BUTTON).click()
                    time.sleep(1)
                    self.report_pass('Web App : Notification Alerts has been turned ' + strNotiState + ' successfully')

                except NoSuchElementException as z:
                    self.report_fail(
                        'Web App : NoSuchElementException: {0} in set_low_temperature method'.format(z.strerror))

            else:
                self.report_fail("Web App : Control not active on the Notification Page to set the notification")

    def getNotificationTempFromUI(self, strNotiType='Both'):
        if strNotiType == 'Both' or strNotiType == 'High':
            tempHighUpDown = self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_TT)
            oCurrentHighTemp = tempHighUpDown.get_attribute('value')
            oCurrentHighTemp = float(oCurrentHighTemp)

        if strNotiType == 'Both' or strNotiType == 'Low':
            tempLowUpDown = self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_TT)
            oCurrentLowTemp = tempLowUpDown.get_attribute('value')
            oCurrentLowTemp = float(oCurrentLowTemp)

        return oCurrentHighTemp, oCurrentLowTemp


class motionSensorPage(BasePage):

    def get_motion_sensor_attributes(self):
        if self.reporter.ActionStatus:

            strStatus = 'OFF'
            oNoOfTimesSensorTriggeredToday = 0
            oBusiestPeriod = ()
            oEventsLogFromAppForWeek = {}

            try:
                if self.wait_for_element_exist(*MotionSensorPageLocators_V3.MOTION_SENSOR_STATUS_INDICATOR):
                    time.sleep(1)
                    #Getting the state of the sensor
                    oStateText = self.driver.find_element(*MotionSensorPageLocators_V3.MOTION_SENSOR_STATE).text
                    if oStateText.upper().find('MOTION') == 0: strStatus = 'ON'
                    elif oStateText.upper().find('MOTION') > 0: strStatus = 'OFF'

                    #LastDetected
                    oLastDetectedToday = self.driver.find_element_by_xpath(*MotionSensorPageLocators_V3.MOTION_SENSOR_LAST_DETECTED).text
                    if oLastDetectedToday.upper().find('DETECTED') > 0:
                        oLastDetected = self.driver.find_element_by_xpath(*MotionSensorPageLocators_V3.MOTION_SENSOR_LAST_DETECTED_TIME).text
                    else: oLastDetected = 'No activity today'
                    print(oLastDetected)

                    #Busiest Period
                    oNoOfTimesSensorTriggeredToday, BusiestPeriod = self.busiest_Period(oNoOfTimesSensorTriggeredToday, oBusiestPeriod)

                    # EventLogs
                    self.zoom_plus_button_click()
                    oCalenderDaysUL = self.driver.find_element(*MotionSensorPageLocators_V3.MOTION_SENSOR_DAY_CALENDAR)
                    oCalenderDays = oCalenderDaysUL.find_elements(*MotionSensorPageLocators_V3.MOTION_SENSOR_CALENDAR_LIST)
                    for oDay in range(7, 0, -1):
                        count = 8 - oDay
                        oDayNumber = 'Day' + str(count)
                        oCalenderDays[oDay-1].click()
                        time.sleep(2)
                        oEventsLogFromApp = self.event_Logs()
                        oEventsLogFromAppForWeek.update({oDayNumber: oEventsLogFromApp})
                    print(oEventsLogFromAppForWeek)

                else:
                    self.report_fail("Web-App : Control not active on the Warm white light Page to get light Attributes")
                self.report_done('Web App : Screenshot while getting attributes')
                print(strStatus)
                return strStatus, BusiestPeriod, oLastDetected, oNoOfTimesSensorTriggeredToday, oEventsLogFromAppForWeek
                time.sleep(1)
            except:
                self.report_fail('Web App : NoSuchElementException: in get_motion_sensor_attributes Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))


    def busiest_Period(self, oNoOfTimesSensorTriggeredToday, oBusiestPeriod):

        oNoOfTimesSensorTriggeredTodayID = self.driver.find_element(*MotionSensorPageLocators_V3.MOTION_SENSOR_TRIGGERED).text
        oNoOfTimesSensorTriggeredToday = oNoOfTimesSensorTriggeredTodayID[8:]
        if not 'NOT TRIGGERED' in oNoOfTimesSensorTriggeredToday.upper() >=0 :
            oBusiestPeriodID = self.driver.find_element(*MotionSensorPageLocators_V3.MOTION_SENSOR_BUSIEST_PERIOD).text
            oLength = len(oBusiestPeriodID)
            Time = oLength - 15
            oBusiestPeriod = oBusiestPeriodID[Time:]
            print(oNoOfTimesSensorTriggeredToday)
            print(oBusiestPeriod)
        return oNoOfTimesSensorTriggeredToday, oBusiestPeriod

    def event_Logs(self):

        oEventsDictForTheDay = {}
        oMotionEventsForTodayID = self.driver.find_elements(*MotionSensorPageLocators_V3.MOTION_SENSOR_TODAY_EVENTS)
        oNumberOfEventsToday = len(oMotionEventsForTodayID)
        print(oNumberOfEventsToday)
        #Creating a dict with a tupule or list inside with start time and duration

        for i in range(0, oNumberOfEventsToday):
            oText = oMotionEventsForTodayID[i].text
            oTextLength = len(oText)
            oMotionStartTime = oText[(oTextLength-5):]
            oMotionDuration = oText[7:]
            oMotionDuration = oMotionDuration[:(len(oMotionDuration)-7)]

            if oMotionDuration.find('Detected') >= 0:
                oMotionDuration = oMotionDuration[10:]
            else: oMotionDuration = oMotionDuration[1:]
            oMotionEventsForToday = [(oMotionStartTime, oMotionDuration)]
            print (oMotionEventsForToday)
            oEventNumber = "Event %d" % (i+1)
            oEventsDictForTheDay.update({oEventNumber: oMotionEventsForToday})
        #print (oEventsDictForTheDay)
        return oEventsDictForTheDay

    #def eventLogDict(self, oEventsLogFromAppForWeek, oEventsLogFromApp):

    def zoom_plus_button_click(self):

        EventlogsElm = self.driver.find_element(*MotionSensorPageLocators_V3.MOTION_SENSOR_EVENT_LOGS_BASE)
        EventlogsElm.send_keys(Keys.END)
        time.sleep(5)

        oButtonDisabled = self.check_exists_by_xpath(*MotionSensorPageLocators_V3.MOTION_SENSOR_PLUS_ZOOM_BUTTON_DISABLED)
        if not oButtonDisabled:
            oZoomPlusClick = self.driver.find_element(*MotionSensorPageLocators_V3.MOTION_SENSOR_PLUS_ZOOM_BUTTON)
            oZoomPlusClick1 = oZoomPlusClick
            for num in range(0, 6):
                oZoomPlusClick1.click()
                time.sleep(2)
                oButtonDisabled = self.check_exists_by_xpath(*MotionSensorPageLocators_V3.MOTION_SENSOR_PLUS_ZOOM_BUTTON_DISABLED)
                if oButtonDisabled:
                    break


class WarmWhiteLightPage(BasePage):

    def set_light_mode(self, strMode, strStatus = None):
        try:
            if self.wait_for_element_exist(*WarmWhiteLightPageLocatorsV3.MODE_SELECTOR_TEXT):
                if strMode.upper().find('MANUAL') >= 0:
                    self.driver.find_element(*WarmWhiteLightPageLocatorsV3.MANUAL_MODE_SELECTOR).click()
                else:
                    self.driver.find_element(*WarmWhiteLightPageLocatorsV3.SCHEDULE_MODE_SELECTOR).click()
                time.sleep(7)
                if self.wait_for_element_exist(*WarmWhiteLightPageLocatorsV3.CENTRAL_STATUS_INDICATOR):
                    self.report_pass('Web App : Successfully Active light mode is set to <B>' + strMode)
                else:
                    self.report_fail('Web App : Unable to set active light mode to <B>' + strMode)

                strCurrentState = self.driver.find_element(*WarmWhiteLightPageLocatorsV3.CENTRAL_STATUS_INDICATOR).text
                if strStatus == 'ON':
                    if 'OFF' in strCurrentState.upper():
                        self.driver.find_element(*WarmWhiteLightPageLocatorsV3.CENTRAL_STATUS_INDICATOR).click()
                    self.report_pass('Web App : Successfully Active light status is set to <B>' + strStatus)
                elif strStatus == 'OFF':
                    if not 'OFF' in strCurrentState.upper():
                        self.driver.find_element(*WarmWhiteLightPageLocatorsV3.CENTRAL_STATUS_INDICATOR).click()
                    self.report_pass('Web App : Successfully Active light status is set to <B>' + strStatus)

            else:
                self.report_fail("Web App : Control not active on the Active light Page to set the light Mode")


        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_light_mode'.format(e.strerror))

    def set_brightness(self,targetBrightnessValue):
        try :
            strState = 'off'
            if self.driver.find_element(*WarmWhiteLightPageLocatorsV3.CENTRAL_STATUS_INDICATOR).text == strState:
                self.driver.find_element(*WarmWhiteLightPageLocatorsV3.CENTRAL_STATUS_INDICATOR).click()
            if targetBrightnessValue >= str(0):
            #if self.wait_for_element_exist(*WarmWhiteLightPageLocators.BRIGHTNESS_PICKER):
                #if self.wait_for_element_exist(*WarmWhiteLightPageLocators.INDICATOR_OFF):
                    #self.driver.find_element(*WarmWhiteLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
                    #time.sleep(1)
                #if targetBrightnessValue == 5:
                self.driver.find_element(*WarmWhiteLightPageLocatorsV3.dimmer_percentage(str(targetBrightnessValue))).click()
                #elif targetBrightnessValue == 10:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_10_PERCENT).click()
                #elif targetBrightnessValue == 20:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_20_PERCENT).click()
                #elif targetBrightnessValue == 30:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_30_PERCENT).click()
                #elif targetBrightnessValue == 40:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_40_PERCENT).click()
                #elif targetBrightnessValue == 50:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_50_PERCENT).click()
                #elif targetBrightnessValue == 60:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_60_PERCENT).click()
                #elif targetBrightnessValue == 70:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_70_PERCENT).click()
                #elif targetBrightnessValue == 80:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_80_PERCENT).click()
                #elif targetBrightnessValue == 90:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_90_PERCENT).click()
                #elif targetBrightnessValue == 100:
                    #self.driver.find_element(*WarmWhiteLightPageLocators.DIMMER_100_PERCENT).click()
            else :
                self.report_fail('Web App : Control not active on Active light page to set the brighness')

            time.sleep(5)
            self.driver.refresh()
            if self.wait_for_element_exist(*WarmWhiteLightPageLocatorsV3.CURRENT_BRIGHTNESS):
                oDisplayValue = self.driver.find_element(*WarmWhiteLightPageLocatorsV3.CURRENT_BRIGHTNESS).get_attribute('textContent')
            if len(oDisplayValue.split())>1:
                displayValuePercent = oDisplayValue.split()[1]
                currentBrightness = displayValuePercent.rstrip('%')
            if str(currentBrightness) == str(targetBrightnessValue) :
                self.report_pass('Web App : The brightness is successfully set to : ' + str(targetBrightnessValue) + '%')
            else :
                self.report_fail('Web App : Unable to set the brightness to : ' + str(targetBrightnessValue) + '%')

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_brightness Method'.format(e.strerror))

    def get_light_attribute(self):
        if self.reporter.ActionStatus:
            strLightBrightness = 0
            strMode = 'MANUAL'
            strStatus = 'OFF'
            try:
                self.refresh_page()
                if self.wait_for_element_exist(*WarmWhiteLightPageLocators.CENTRAL_STATUS_INDICATOR):
                    time.sleep(1)
                    oModetext = self.driver.find_element(*WarmWhiteLightPageLocators.MODE_SELECTOR_TEXT).text
                    if oModetext.upper().find('SCHEDULE') >= 0:
                        strMode = 'SCHEDULE'
                    else :
                        strMode = 'MANUAL'
                    print (strMode)
                    oDisplayValue = self.driver.find_element(*WarmWhiteLightPageLocators.CENTRAL_STATUS_INDICATOR).text
                    if not 'OFF' in oCSIValue.upper():
                        displayValuePercent = oDisplayValue.split()[1]
                        strLightBrightness = displayValuePercent.rstrip('%')
                        strStatus = 'ON'
                    else :
                        strStatus = oDisplayValue.upper()

                else:
                    self.report_fail("Web-App : Control not active on the Warm white light Page to get light Attributes")

                self.report_done('Web App : Screenshot while getting attributes')
                print(strMode, strStatus, strLightBrightness)
                return strMode, strStatus, strLightBrightness
                time.sleep(1)
            except:
                self.report_fail('Web App : NoSuchElementException: in get_light_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_light_schedule(self, oSourceSchedDict, oDestSchedDict):
        try:
            if self.wait_for_element_exist(*WarmWhiteLightPageLocators.SCHEDULE_LIGHT_TABLE):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                # Get StartX int15MinLen
                self.oSchedTableEL = self.driver.find_element(*WarmWhiteLightPageLocators.SCHEDULE_LIGHT_TABLE)

                # Setup Initial Configs
                self.intWidthLeftPad = 60
                intWidthRightPad = 30
                intWidthOfCavas = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfCavas - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule / 24) / 4
                print(self.intWidthOf15Min)

                for strDay in oDestSchedDict.keys():
                    # Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    print('Destination Schedule')
                    print(self.oDestSchedList)
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    print('Source Schedule')
                    print(self.oSourceSchedList)
                    self.intYDay = 100 + 40 * (oWeekDayList.index(strDay))

                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount:
                        self.remove_events(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount:
                        self.add_events(intDestListCount - intSourceListCount)
                    print(intSourceListCount, intDestListCount)

                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    # Get Last events position
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intLstEvntXPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                        strLstEvntStTime) / 15) * self.intWidthOf15Min
                    intLastEventMoveToPosition = len(self.oSourceSchedList) * self.intWidthOf15Min
                    intLastEventInitialOffset = - (intLstEvntXPos - intLastEventMoveToPosition)
                    # And move all the events to the beginning
                    action = ActionChains(self.oSchedTableEL.parent)
                    action.move_to_element_with_offset(self.oSchedTableEL, intLstEvntXPos,
                                                       self.intYDay).click_and_hold().move_by_offset(
                        intLastEventInitialOffset, 0).release().perform()
                    time.sleep(2)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    # Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList) - 1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]
                        intCurEvntDestPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                        intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntSourcePos,
                                                           self.intYDay).click_and_hold().move_by_offset(
                            intCurOffsetPos, 0).release().perform()
                        time.sleep(2)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set Brightness to for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        self.driver.find_element(*PageHeaderLocators.USERNAME_DISPLAY).click()
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)
                        intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        if intCntr == len(self.oDestSchedList) - 1:
                            intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
                        else:
                            intNextEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                                self.oDestSchedList[intCntr + 1][0]) / 15) * self.intWidthOf15Min
                        intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition) / 2
                        intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos,
                                                           self.intYDay).click().perform()
                        time.sleep(2)
                        self.report_pass(
                            'Web App : For Day  : ' + strDay + ' Before Brightness for Event number ' + str(
                                intCntr + 1) + ' is set')
                        intSetBrightness = int(oCurEvent[2])
                        if self.wait_for_element_exist(*WarmWhiteLightPageLocators.SCHEDULE_BRIGHTNESS_PICKER):
                            oSchedBrightnessPickerEL = self.driver.find_element(
                                *WarmWhiteLightPageLocators.SCHEDULE_BRIGHTNESS_PICKER)
                            self._set_brightness(oSchedBrightnessPickerEL, intSetBrightness)
                            self.report_pass(
                                'Web App : For Day  : ' + strDay + ' After Target Brightness for Event number ' + str(
                                    intCntr + 1) + ' is set')
                        else:
                            self.report_fail(
                                'Web App : For Day  : ' + strDay + ' Target Brightness Object for Event number ' + str(
                                    intCntr + 1) + ' is not displayed')

                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Brightness are set')

                self.driver.find_element(*WarmWhiteLightPageLocators.SAVE_BUTTON).click()
                self.report_pass('Web App : Light Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Light Page to set the Light Schedule")

        except:
            self.report_fail('WEB APP: Exception in set_light_schedule Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

class TuneableLightPage(BasePage):

    def set_light_mode(self, strMode, strStatus = None):
        try:
            if self.wait_for_element_exist(*TuneableLightPageLocators.MODE_SELECTOR_TEXT):
                if strMode.upper().find('MANUAL') >= 0:
                    self.driver.find_element(*TuneableLightPageLocators.MANUAL_MODE_SELECTOR).click()
                else:
                    self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_MODE_SELECTOR).click()
                time.sleep(5)
                if self.wait_for_element_exist(*TuneableLightPageLocators.CENTRAL_STATUS_INDICATOR):
                    self.report_pass('Web App : Successfully Active light mode is set to <B>' + strMode)
                else:
                    self.report_fail('Web App : Unable to set active light mode to <B>' + strMode)

                strCurrentState = self.driver.find_element(*TuneableLightPageLocators.CENTRAL_STATUS_INDICATOR).text
                if strStatus == 'ON':
                    if 'off' in strCurrentState:
                        self.driver.find_element(*TuneableLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
                    self.report_pass('Web App : Successfully Active light status is set to <B>' + strStatus)
                elif strStatus == 'OFF':
                    if not 'off' in strCurrentState:
                        self.driver.find_element(*TuneableLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
                    self.report_pass('Web App : Successfully Active light status is set to <B>' + strStatus)

            else:
                self.report_fail("Web App : Control not active on the Active light Page to set the light Mode")


        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_light_mode'.format(e.strerror))

    def set_brightness(self,targetBrightnessValue):
        try :
            strState = 'off'
            if self.driver.find_element(*TuneableLightPageLocators.CENTRAL_STATUS_INDICATOR).text == strState:
                self.driver.find_element(*TuneableLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
            if targetBrightnessValue >= 0:
            #if self.wait_for_element_exist(*WarmWhiteLightPageLocators.BRIGHTNESS_PICKER):
                #if self.wait_for_element_exist(*WarmWhiteLightPageLocators.INDICATOR_OFF):
                    #self.driver.find_element(*WarmWhiteLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
                    #time.sleep(1)
                if targetBrightnessValue == 5:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_5_PERCENT).click()
                elif targetBrightnessValue == 10:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_10_PERCENT).click()
                elif targetBrightnessValue == 20:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_20_PERCENT).click()
                elif targetBrightnessValue == 30:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_30_PERCENT).click()
                elif targetBrightnessValue == 40:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_40_PERCENT).click()
                elif targetBrightnessValue == 50:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_50_PERCENT).click()
                elif targetBrightnessValue == 60:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_60_PERCENT).click()
                elif targetBrightnessValue == 70:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_70_PERCENT).click()
                elif targetBrightnessValue == 80:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_80_PERCENT).click()
                elif targetBrightnessValue == 90:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_90_PERCENT).click()
                elif targetBrightnessValue == 100:
                    self.driver.find_element(*TuneableLightPageLocators.DIMMER_100_PERCENT).click()
            else :
                self.report_fail('Web App : Control not active on Active light page to set the brighness')

            time.sleep(3)
            currentBrightness = self.driver.find_element(*TuneableLightPageLocators.CURRENT_BRIGHTNESS).get_attribute('textContent')
            if str(currentBrightness) == str(targetBrightnessValue) :
                self.report_pass('Web App : The brightness is successfully set to : ' + str(targetBrightnessValue) + '%')
            else :
                self.report_fail('Web App : Unable to set the brightness to : ' + str(targetBrightnessValue) + '%')

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_brightness Method'.format(e.strerror))

    def set_tone(self,targetTone):
        try :
            viewSwitch = self.driver.find_element(*TuneableLightPageLocators.TONE_DIMMER_TEXT).text
            if viewSwitch == 'tone':
                self.driver.find_element(*TuneableLightPageLocators.TONE_DIMMER_SWITCH).click()
                self.report_pass('Web App: Successfully set to Tone view')
            if str(targetTone) == 'WARMEST WHITE':
                self.driver.find_element(*TuneableLightPageLocators.WARMEST_WHITE).click()
            elif str(targetTone) == 'WARM WHITE':
                self.driver.find_element(*TuneableLightPageLocators.WARM_WHITE).click()
            elif str(targetTone) == 'MID WHITE':
                self.driver.find_element(*TuneableLightPageLocators.MID_WHITE).click()
            elif str(targetTone) == 'COOL WHITE':
                self.driver.find_element(*TuneableLightPageLocators.COOL_WHITE).click()
            elif str(targetTone) == 'COOLEST WHITE':
                self.driver.find_element(*TuneableLightPageLocators.COOLEST_WHITE).click()
            time.sleep(3)
            currentTone = self.driver.find_element(*TuneableLightPageLocators.CURRENT_TONE).text
            if currentTone.upper() == targetTone:
                self.report_pass('Web App : Tone is successfully set to : ' + targetTone)
            else :
                self.report_fail('Web App : Unable to set the tone to : ' + targetTone)

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_brightness Method'.format(e.strerror))

    def get_light_attribute(self):
        if self.reporter.ActionStatus:
            strLightBrightness = 0
            try:
                self.refresh_page()
                if self.wait_for_element_exist(*TuneableLightPageLocators.CENTRAL_STATUS_INDICATOR):
                    oModetext = self.driver.find_element(*TuneableLightPageLocators.MODE_SELECTOR_TEXT).text
                    if oModetext.upper().find('SCHEDULE') >= 0:
                        strMode = 'SCHEDULE'
                    else :
                        strMode = oModetext.upper()
                    oCSIValue = self.driver.find_element(*TuneableLightPageLocators.CENTRAL_STATUS_INDICATOR).text
                    if not 'OFF' in oCSIValue:
                        strLightBrightness = oCSIValue.rstrip('%')
                        strStatus = 'ON'
                    else :
                        strStatus = oCSIValue

                else:
                    self.report_fail("Web-App : Control not active on the Tuneable light Page to get light Attributes")

                self.report_done('Web App : Screenshot while getting attributes')
                print(strMode, strStatus, strLightBrightness)

                return strMode, strStatus, strLightBrightness
            except:
                self.report_fail('Web App : NoSuchElementException: in get_light_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_light_schedule(self, oSourceSchedDict, oDestSchedDict):
        try:
            if self.wait_for_element_exist(*TuneableLightPageLocators.SCHEDULE_LIGHT_TABLE):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                # Get StartX int15MinLen
                self.oSchedTableEL = self.driver.find_element(*TuneableLightPageLocators.SCHEDULE_LIGHT_TABLE)

                # Setup Initial Configs
                self.intWidthLeftPad = 60
                intWidthRightPad = 30
                intWidthOfCavas = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfCavas - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule / 24) / 4
                print(self.intWidthOf15Min)

                for strDay in oDestSchedDict.keys():
                    # Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    print('Destination Schedule')
                    print(self.oDestSchedList)
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    print('Source Schedule')
                    print(self.oSourceSchedList)
                    self.intYDay = 100 + 40 * (oWeekDayList.index(strDay))

                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount:
                        self.remove_events(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount:
                        self.add_events(intDestListCount - intSourceListCount)
                    print(intSourceListCount, intDestListCount)

                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    # Get Last events position
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intLstEvntXPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                        strLstEvntStTime) / 15) * self.intWidthOf15Min
                    intLastEventMoveToPosition = len(self.oSourceSchedList) * self.intWidthOf15Min
                    intLastEventInitialOffset = - (intLstEvntXPos - intLastEventMoveToPosition)
                    # And move all the events to the beginning
                    action = ActionChains(self.oSchedTableEL.parent)
                    action.move_to_element_with_offset(self.oSchedTableEL, intLstEvntXPos,
                                                       self.intYDay).click_and_hold().move_by_offset(
                        intLastEventInitialOffset, 0).release().perform()
                    time.sleep(2)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    # Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList) - 1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]
                        intCurEvntDestPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                        intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntSourcePos,
                                                           self.intYDay).click_and_hold().move_by_offset(
                            intCurOffsetPos, 0).release().perform()
                        time.sleep(2)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set Brightness to for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        self.driver.find_element(*PageHeaderLocators.USERNAME_DISPLAY).click()
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)
                        intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        if intCntr == len(self.oDestSchedList) - 1:
                            intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
                        else:
                            intNextEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                                self.oDestSchedList[intCntr + 1][0]) / 15) * self.intWidthOf15Min
                        intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition) / 2
                        intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos,
                                                           self.intYDay).click().perform()
                        time.sleep(2)
                        #if not oCurEvent[3]:
                             #self.report_pass(
                                #'Web App : For Day  : ' + strDay + ' Before Brightness for Event number ' + str(
                                #intCntr + 1) + ' is set')
                        #else:
                        self.report_pass(
                                'Web App : For Day  : ' + strDay + ' Before Brightness & Tone for Event number ' + str(
                                    intCntr + 1) + ' is set')
                        intSetBrightness = int(oCurEvent[2])
                        if self.wait_for_element_exist(*TuneableLightPageLocators.SCHEDULE_BRIGHTNESS_PICKER):
                            oSchedBrightnessPickerEL = self.driver.find_element(
                                *TuneableLightPageLocators.SCHEDULE_BRIGHTNESS_PICKER)
                            self._set_brightness(oSchedBrightnessPickerEL, intSetBrightness)
                            if oCurEvent[3]:
                                strSetTone = str(oCurEvent[3])
                                oSchedTonePickerEL = self.driver.find_element(
                                    *TuneableLightPageLocators.SCHEDULE_TONE_PICKER)
                                self._set_tone(oSchedTonePickerEL, strSetTone)
                                self.report_pass(
                                    'Web App : For Day  : ' + strDay + ' After Target Brightness & Tone for Event number ' + str(
                                        intCntr + 1) + ' is set')
                            else :
                                self.report_pass(
                                    'Web App : For Day  : ' + strDay + ' After Target Brightness for Event number ' + str(
                                        intCntr + 1) + ' is set')
                        else:
                            self.report_fail(
                                'Web App : For Day  : ' + strDay + ' Target Brightness & Tone Object for Event number ' + str(
                                    intCntr + 1) + ' is not displayed')

                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Schedule are set')

                self.driver.find_element(*TuneableLightPageLocators.SAVE_BUTTON).click()
                self.report_pass('Web App : Light Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Light Page to set the Light Schedule")

        except:
            self.report_fail('WEB APP: Exception in set_light_schedule Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))

class ColourLightPage(BasePage):

    def set_light_mode(self, strMode, strStatus = None):
        try:
            if self.wait_for_element_exist(*ColourLightPageLocators.MODE_SELECTOR_TEXT):
                if strMode.upper().find('MANUAL') >= 0:
                    self.driver.find_element(*ColourLightPageLocators.MANUAL_MODE_SELECTOR).click()
                else:
                    self.driver.find_element(*ColourLightPageLocators.SCHEDULE_MODE_SELECTOR).click()
                time.sleep(5)
                if self.wait_for_element_exist(*ColourLightPageLocators.CENTRAL_STATUS_INDICATOR):
                    self.report_pass('Web App : Successfully Active light mode is set to <B>' + strMode)
                else:
                    self.report_fail('Web App : Unable to set active light mode to <B>' + strMode)

                strCurrentState = self.driver.find_element(*ColourLightPageLocators.CENTRAL_STATUS_INDICATOR).text
                if strStatus == 'ON':
                    if 'off' in strCurrentState:
                        self.driver.find_element(*ColourLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
                    self.report_pass('Web App : Successfully Active light status is set to <B>' + strStatus)
                elif strStatus == 'OFF':
                    if not 'off' in strCurrentState:
                        self.driver.find_element(*ColourLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
                    self.report_pass('Web App : Successfully Active light status is set to <B>' + strStatus)

            else:
                self.report_fail("Web App : Control not active on the Active light Page to set the light Mode")


        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_light_mode'.format(e.strerror))

    def set_brightness(self,targetBrightnessValue):
        try :
            strState = 'off'
            if self.driver.find_element(*ColourLightPageLocators.CENTRAL_STATUS_INDICATOR).text == strState:
                self.driver.find_element(*ColourLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
            if targetBrightnessValue >= 0:
            #if self.wait_for_element_exist(*WarmWhiteLightPageLocators.BRIGHTNESS_PICKER):
                #if self.wait_for_element_exist(*WarmWhiteLightPageLocators.INDICATOR_OFF):
                    #self.driver.find_element(*WarmWhiteLightPageLocators.CENTRAL_STATUS_INDICATOR).click()
                    #time.sleep(1)
                if targetBrightnessValue == 5:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_5_PERCENT).click()
                elif targetBrightnessValue == 10:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_10_PERCENT).click()
                elif targetBrightnessValue == 20:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_20_PERCENT).click()
                elif targetBrightnessValue == 30:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_30_PERCENT).click()
                elif targetBrightnessValue == 40:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_40_PERCENT).click()
                elif targetBrightnessValue == 50:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_50_PERCENT).click()
                elif targetBrightnessValue == 60:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_60_PERCENT).click()
                elif targetBrightnessValue == 70:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_70_PERCENT).click()
                elif targetBrightnessValue == 80:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_80_PERCENT).click()
                elif targetBrightnessValue == 90:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_90_PERCENT).click()
                elif targetBrightnessValue == 100:
                    self.driver.find_element(*ColourLightPageLocators.DIMMER_100_PERCENT).click()
            else :
                self.report_fail('Web App : Control not active on Active light page to set the brighness')

            time.sleep(3)
            currentBrightness = self.driver.find_element(*ColourLightPageLocators.CURRENT_BRIGHTNESS).get_attribute('textContent')
            if str(currentBrightness) == str(targetBrightnessValue) :
                self.report_pass('Web App : The brightness is successfully set to : ' + str(targetBrightnessValue) + '%')
            else :
                self.report_fail('Web App : Unable to set the brightness to : ' + str(targetBrightnessValue) + '%')

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_brightness Method'.format(e.strerror))

    def set_tone(self, targetTone):
        try:
            viewSwitch = self.driver.find_element(*ColourLightPageLocators.TONE_COLOUR_SWITCH).text
            if viewSwitch == 'tone':
                self.driver.find_element(*ColourLightPageLocators.TONE_COLOUR_SWITCH).click()
            else:
                self.driver.find_element(*ColourLightPageLocators.TONE_COLOUR_SWITCH).click()
                self.driver.find_element(*ColourLightPageLocators.TONE__SWITCH).click()
                self.report_pass('Web App: Successfully set to Tone view')
            if str(targetTone) == 'WARMEST WHITE':
                self.driver.find_element(*ColourLightPageLocators.WARMEST_WHITE).click()
            elif str(targetTone) == 'WARM WHITE':
                self.driver.find_element(*ColourLightPageLocators.WARM_WHITE).click()
            elif str(targetTone) == 'MID WHITE':
                self.driver.find_element(*ColourLightPageLocators.MID_WHITE).click()
            elif str(targetTone) == 'COOL WHITE':
                self.driver.find_element(*ColourLightPageLocators.COOL_WHITE).click()
            elif str(targetTone) == 'COOLEST WHITE':
                self.driver.find_element(*ColourLightPageLocators.COOLEST_WHITE).click()
            time.sleep(3)
            currentTone = self.driver.find_element(*TuneableLightPageLocators.CURRENT_TONE).text
            if currentTone.upper() == targetTone:
                self.report_pass('Web App : Tone is successfully set to : ' + targetTone)
            else:
                self.report_fail('Web App : Unable to set the tone to : ' + targetTone)

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_tone Method'.format(e.strerror))

    def set_colour(self,targetColour):
        print(targetColour)
        try :
            viewSwitch = self.driver.find_element(*ColourLightPageLocators.TONE_COLOUR_SWITCH).text
            print (viewSwitch+'Test')
            if viewSwitch == 'colour':
                print('check1')
                self.driver.find_element(*ColourLightPageLocators.TONE_COLOUR_SWITCH).click()
                self.report_pass('Web App: Successfully set to Colour view')
            elif viewSwitch == 'tone':
                print('check2')
                self.driver.find_element(*ColourLightPageLocators.TONE_COLOUR_SWITCH).click()
                self.driver.find_element(*ColourLightPageLocators.COLOUR_SWITCH).click()
                self.report_pass('Web App: Successfully set to Colour view')
            time.sleep(3)
            if str(targetColour) == 'RED':
                self.driver.find_element(*ColourLightPageLocators.RED_LEFT).click()
            elif str(targetColour) == 'RED ORANGE':
                self.driver.find_element(*ColourLightPageLocators.RED_ORANGE).click()
            elif str(targetColour) == 'ORANGE':
                self.driver.find_element(*ColourLightPageLocators.ORANGE).click()
            elif str(targetColour) == 'ORANGE YELLOW':
                self.driver.find_element(*ColourLightPageLocators.ORANGE_YELLOW).click()
            elif str(targetColour) == 'YELLOW':
                self.driver.find_element(*ColourLightPageLocators.YELLOW).click()
            elif str(targetColour) == 'YELLOW GREEN':
                self.driver.find_element(*ColourLightPageLocators.YELLOW_GREEN).click()
            elif str(targetColour) == 'GREEN':
                self.driver.find_element(*ColourLightPageLocators.GREEN).click()
            elif str(targetColour) == 'GREEN CYAN':
                self.driver.find_element(*ColourLightPageLocators.GREEN_CYAN).click()
            elif str(targetColour) == 'CYAN':
                self.driver.find_element(*ColourLightPageLocators.CYAN).click()
            elif str(targetColour) == 'CYAN BLUE':
                self.driver.find_element(*ColourLightPageLocators.CYAN_BLUE).click()
            elif str(targetColour) == 'BLUE':
                self.driver.find_element(*ColourLightPageLocators.BLUE).click()
            elif str(targetColour) == 'BLUE MAGENTA':
                self.driver.find_element(*ColourLightPageLocators.BLUE_MAGENTA).click()
            elif str(targetColour) == 'MAGENTA':
                self.driver.find_element(*ColourLightPageLocators.MAGENTA).click()
            elif str(targetColour) == 'MAGENTA PINK':
                self.driver.find_element(*ColourLightPageLocators.MAGENTA_PINK).click()
            elif str(targetColour) == 'PINK':
                self.driver.find_element(*ColourLightPageLocators.PINK).click()
            elif str(targetColour) == 'PINK RED':
                self.driver.find_element(*ColourLightPageLocators.PINK_RED).click()
            time.sleep(3)
            #currentTone = self.driver.find_element(*ColourLightPageLocators.CURRENT_TONE).text
            #if currentTone.upper() == targetColour:
            self.report_pass('Web App : Colour is successfully set to : ' + targetColour)
            #else :
                #self.report_fail('Web App : Unable to set the tone to : ' + targetTone)

        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_colour Method'.format(e.strerror))


    def get_light_attribute(self):
        if self.reporter.ActionStatus:
            strLightBrightness = 0
            try:
                self.refresh_page()
                if self.wait_for_element_exist(*ColourLightPageLocators.CENTRAL_STATUS_INDICATOR):
                    oModetext = self.driver.find_element(*ColourLightPageLocators.MODE_SELECTOR_TEXT).text
                    if oModetext.upper().find('SCHEDULE') >= 0:
                        strMode = 'SCHEDULE'
                    else :
                        strMode = oModetext.upper()
                    oCSIValue = self.driver.find_element(*ColourLightPageLocators.CENTRAL_STATUS_INDICATOR).text
                    if not 'OFF' in oCSIValue:
                        strLightBrightness = oCSIValue.rstrip('%')
                        strStatus = 'ON'
                    else :
                        strStatus = oCSIValue

                else:
                    self.report_fail("Web-App : Control not active on the Colour light Page to get light Attributes")

                self.report_done('Web App : Screenshot while getting attributes')
                print(strMode, strStatus, strLightBrightness)

                return strMode, strStatus, strLightBrightness
            except:
                self.report_fail('Web App : NoSuchElementException: in get_light_attribute Method\n {0}'.format(
                    traceback.format_exc().replace('File', '$~File')))

    def set_light_schedule(self, oSourceSchedDict, oDestSchedDict):
        try:
            if self.wait_for_element_exist(*ColourLightPageLocators.SCHEDULE_LIGHT_TABLE):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                # Get StartX int15MinLen
                self.oSchedTableEL = self.driver.find_element(*ColourLightPageLocators.SCHEDULE_LIGHT_TABLE)

                # Setup Initial Configs
                self.intWidthLeftPad = 60
                intWidthRightPad = 30
                intWidthOfCavas = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfCavas - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule / 24) / 4
                print(self.intWidthOf15Min)

                for strDay in oDestSchedDict.keys():
                    # Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    print('Destination Schedule')
                    print(self.oDestSchedList)
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    print('Source Schedule')
                    print(self.oSourceSchedList)
                    self.intYDay = 100 + 40 * (oWeekDayList.index(strDay))

                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount:
                        self.remove_events(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount:
                        self.add_events(intDestListCount - intSourceListCount)
                    print(intSourceListCount, intDestListCount)

                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    # Get Last events position
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intLstEvntXPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                        strLstEvntStTime) / 15) * self.intWidthOf15Min
                    intLastEventMoveToPosition = len(self.oSourceSchedList) * self.intWidthOf15Min
                    intLastEventInitialOffset = - (intLstEvntXPos - intLastEventMoveToPosition)
                    # And move all the events to the beginning
                    action = ActionChains(self.oSchedTableEL.parent)
                    action.move_to_element_with_offset(self.oSchedTableEL, intLstEvntXPos,
                                                       self.intYDay).click_and_hold().move_by_offset(
                        intLastEventInitialOffset, 0).release().perform()
                    time.sleep(2)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')

                    # Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList) - 1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]
                        intCurEvntDestPos = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                        intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntSourcePos,
                                                           self.intYDay).click_and_hold().move_by_offset(
                            intCurOffsetPos, 0).release().perform()
                        time.sleep(2)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')

                    # Set Brightness to for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        self.driver.find_element(*PageHeaderLocators.USERNAME_DISPLAY).click()
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)
                        intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                            oCurEvent[0]) / 15) * self.intWidthOf15Min
                        if intCntr == len(self.oDestSchedList) - 1:
                            intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
                        else:
                            intNextEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(
                                self.oDestSchedList[intCntr + 1][0]) / 15) * self.intWidthOf15Min
                        intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition) / 2
                        intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid
                        # And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos,
                                                           self.intYDay).click().perform()
                        time.sleep(2)
                        #if not oCurEvent[3]:
                             #self.report_pass(
                                #'Web App : For Day  : ' + strDay + ' Before Brightness for Event number ' + str(
                                #intCntr + 1) + ' is set')
                        #else:
                        self.report_pass(
                                'Web App : For Day  : ' + strDay + ' Before Brightness & Tone/Colour for Event number ' + str(
                                    intCntr + 1) + ' is set')
                        intSetBrightness = int(oCurEvent[2])
                        if self.wait_for_element_exist(*ColourLightPageLocators.SCHEDULE_BRIGHTNESS_PICKER):
                            oSchedBrightnessPickerEL = self.driver.find_element(
                                *ColourLightPageLocators.SCHEDULE_BRIGHTNESS_PICKER)
                            self._set_brightness(oSchedBrightnessPickerEL, intSetBrightness)
                            if oCurEvent[3]:
                                strSetTone = str(oCurEvent[3])
                                oSchedTonePickerEL = self.driver.find_element(
                                    *ColourLightPageLocators.SCHEDULE_TONE_COLOUR_SWITCH)
                                if 'WHITE' in strSetTone :
                                    self._set_tone(oSchedTonePickerEL, strSetTone, 'COLOUR')
                                else :
                                    self._set_colour(oSchedTonePickerEL, strSetTone,'COLOUR')
                                self.report_pass(
                                    'Web App : For Day  : ' + strDay + ' After Target Brightness & Tone/Colour for Event number ' + str(
                                        intCntr + 1) + ' is set')
                            else :
                                self.report_pass(
                                    'Web App : For Day  : ' + strDay + ' After Target Brightness for Event number ' + str(
                                        intCntr + 1) + ' is set')
                        else:
                            self.report_fail(
                                'Web App : For Day  : ' + strDay + ' Target Brightness & Tone/Colour Object for Event number ' + str(
                                    intCntr + 1) + ' is not displayed')

                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Schedule are set')

                self.driver.find_element(*TuneableLightPageLocators.SAVE_BUTTON).click()
                self.report_pass('Web App : Light Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Light Page to set the Light Schedule")

        except:
            self.report_fail('WEB APP: Exception in set_light_schedule Method\n {0}'.format(
                traceback.format_exc().replace('File', '$~File')))
