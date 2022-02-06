"""
Created on 5 Jun 2015

@author: ranganathan.veluswamy
"""

import collections
from datetime import datetime
from datetime import timedelta
import json
import random
import time

import FF_convertTimeTemperature as tt
import FF_timeZone as TZ

oWeekDayDict = {'SUNDAY': 'sun',
                'MONDAY': 'mon',
                'TUESDAY': 'tue',
                'WEDNESDAY': 'wed',
                'THURSDAY': 'thu',
                'FRIDAY': 'fri',
                'SATURDAY': 'sat'}

oEventPositionDict = {'FIRST': 1,
                      'SECOND': 2,
                      'THIRD': 3,
                      'FOURTH': 4,
                      'FIFTH': 5,
                      'SIXTH': 6}

oWaterStateDict = {'ON': 99.0,
                   'OFF': 0.0,
                   99.0: 'ON',
                   0.0: 'OFF'}

oPlugStateDict = {'ON': 'ON',
                  'OFF': 'OFF',
                  99.0: 'ON',
                  0.0: 'OFF'}

oWeekDayList = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def getRemainingDaySchedule(oSchedList):
    print()
    oNewSched = []
    intNewStartCntr = 0
    oSchedList = remove_duplicates(oSchedList)
    for intCntr in range(len(oSchedList)):
        intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
        intCurrentEventStartMin = tt.timeStringToMinutes(oSchedList[intCntr][0])
        if not intCntr == len(oSchedList) - 1:
            intNextEventStartTime = tt.timeStringToMinutes(oSchedList[intCntr + 1][0])
        else:
            intNextEventStartTime = tt.timeStringToMinutes('24:00')
        if intCurrentEventStartMin < intCurrentMin < intNextEventStartTime:
            intNewStartCntr = intCntr + 1
            if intCntr == len(oSchedList) - 1: intNewStartCntr = intCntr
            break

    for intCntr1 in range(intNewStartCntr, len(oSchedList)):
        oNewSched.append(oSchedList[intCntr1])

    return oNewSched


def makeSixEventSceduleFormat(oSchedList):
    oNewSchedList = []
    intRowCount = len(oSchedList)
    for intTmp in range(6 - intRowCount):
        oNewSchedList.append(oSchedList[0])
    for oEvent in oSchedList:
        oNewSchedList.append(oEvent)
    return oNewSchedList


def buildCompleteRandomSchedule(numberOfEvents):
    """ Build a schedule for today with given numberOfEvents and eventLength.  Schedule event 1 is rounded to next 15mins.
        
        Returns a list of N datetime events and temperatures. [(dt1,sp1), (dt2,sp2), (dt3,sp3)...]
        
        Events will alternate heat demand by setting setpoints of Current temperature +/- 5'C
        1st event heat demand is selected randomly true/false after which they alternate
        For each HDoff event we randomly select a setpoint of either:
            currentTemp-5'C
                or..
            Frost protection
         
        First event time will be next nearest whole minute + holdoff (say 5 minutes) to allow test to be setup.
          
    """
    # Build a list of setpoints.
    # First make a list of the correct length with random boolean values for heat demand
    hd = []
    for i in range(0, numberOfEvents):
        hd.append(random.choice([True, False]))

    # Now get current time rounded to nearest 15mins.
    currentTime = datetime.now()
    nextEventTime = tt.roundTimeUp(currentTime, 15 * 60)
    # if time has rolled into next day then subract a day to bring it back.
    if nextEventTime.day > currentTime.day:
        nextEventTime = nextEventTime.replace(day=currentTime.day)

    # Now make the real setpoint list.
    setpoints = []
    fpSetpoint = 1.0
    intStartMin = 0
    intMinLeftForTheDay = (24 * 60) - 1
    for i in range(0, numberOfEvents):
        if hd[i]:
            # Generate a random setpoint (in 0.5'C steps) where
            # (currentTemp+5) <= N <= 32
            heatSetpoint = random.randint(40, 64) / 2
            # Generate a random setpoint (in 0.5'C steps) where
            # 5 <= N <= (currentTemperature-5)
            setpoints.append((nextEventTime, heatSetpoint))
        else:
            frost = random.choice([True, False])
            offSetpoint = random.randint(14, 40) / 2
            if frost:
                setpoints.append((nextEventTime, fpSetpoint))
            else:
                setpoints.append((nextEventTime, offSetpoint))

        # Increment nextEventTime by 15mins.
        intMinLeftForTheDay = intMinLeftForTheDay - int(nextEventTime.strftime("%M"))
        intRandMin = random.randint(intStartMin, intMinLeftForTheDay)
        intRandMin = intRandMin - (intRandMin % 15)
        nextEventTime = (nextEventTime + timedelta(minutes=intRandMin)).replace(day=currentTime.day)

    setpoints = sorted(setpoints)
    setpointsStr = []
    for sp in setpoints:
        setpointsStr.append(("{:02}:{:02}".format(sp[0].hour, sp[0].minute), sp[1]))

    return setpointsStr


def buildCompleteRandomScheduleForWater(numberOfEvents):
    # Build a list of setpoints.
    # First make a list of the correct length with random boolean values for heat demand
    hd = []
    for i in range(0, numberOfEvents):
        hd.append(random.choice([True, False]))

    # Now get current time rounded to nearest 15mins.
    currentTime = datetime.now()
    nextEventTime = tt.roundTimeUp(currentTime, 15 * 60)
    # if time has rolled into next day then subract a day to bring it back.
    if nextEventTime.day > currentTime.day:
        nextEventTime = nextEventTime.replace(day=currentTime.day)

    # Now make the real setpoint list.
    setpoints = []
    intStartMin = 0
    intMinLeftForTheDay = (24 * 60) - 1
    for i in range(0, numberOfEvents):
        if hd[i]:
            strHotWaterState = 'ON'
            setpoints.append((nextEventTime, strHotWaterState))
        else:
            strHotWaterState = 'OFF'
            setpoints.append((nextEventTime, strHotWaterState))

        intMinLeftForTheDay = intMinLeftForTheDay - int(nextEventTime.strftime("%M"))
        intRandMin = random.randint(intStartMin, intMinLeftForTheDay)
        intRandMin = intRandMin - (intRandMin % 15)
        nextEventTime = (nextEventTime + timedelta(minutes=intRandMin)).replace(day=currentTime.day)

    setpoints = sorted(setpoints)
    setpointsStr = []
    for sp in setpoints:
        setpointsStr.append(("{:02}:{:02}".format(sp[0].hour, sp[0].minute), sp[1]))

    return setpointsStr


# Validating the remaining schedules of the week after the new schedule is set
def validateSchedulesOfOtherWeekdays(reporter, oCurrentlySetSchedDict, oFullWeekSchedDictBefore,
                                     oFullWeekSchedDictAfter):
    for oKey in oFullWeekSchedDictBefore.keys():
        if not oKey in oCurrentlySetSchedDict.keys():
            strReportSchedule, boolCompStatus = getScheduleForReportWithComparison(
                remove_duplicates(oFullWeekSchedDictBefore[oKey]), remove_duplicates(oFullWeekSchedDictAfter[oKey]),
                oKey)
            reporter.ReportEvent('TestValidation', strReportSchedule, boolCompStatus, 'Center')


# Validating the schedules of the week after the new schedule is set
def validateSchedulesOfWeekdays(reporter, oCurrentlySetSchedDict, oFullWeekSchedDictAfter):
    for oKey in oFullWeekSchedDictAfter.keys():
        strReportSchedule, boolCompStatus = getScheduleForReportWithComparison(
            remove_duplicates(oCurrentlySetSchedDict[oKey]), remove_duplicates(oFullWeekSchedDictAfter[oKey]), oKey)
        reporter.ReportEvent('TestValidation', strReportSchedule, boolCompStatus, 'Center')


def validateLightSchedulesOfOtherWeekdays(reporter, oCurrentlySetSchedDict, oFullWeekSchedDictBefore,
                                          oFullWeekSchedDictAfter):
    for oKey in oFullWeekSchedDictBefore.keys():
        if not oKey in oCurrentlySetSchedDict.keys():
            strReportSchedule, boolCompStatus = getLightScheduleForReportWithComparison(
                remove_duplicates(oFullWeekSchedDictBefore[oKey]), remove_duplicates(oFullWeekSchedDictAfter[oKey]),
                oKey)
            reporter.ReportEvent('TestValidation', strReportSchedule, boolCompStatus, 'Center')


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def add_light_time_slot(context):
    output = []
    seen = set()
    values = context.oSchedDict[context.strDay]

    for oTimeSlotList in context.addSchedule:

        oAddTimeSlot = oTimeSlotList[0]

        blnFlag = False
        for value in values:
            if value not in seen:
                if int(value[0].split(':')[0]) > int(oAddTimeSlot.split(':')[0]) and not blnFlag:
                    output.append(oTimeSlotList)
                    seen.add(oTimeSlotList)
                    output.append(value)
                    seen.add(value)
                    blnFlag = True
                elif int(value[0].split(':')[0]) == int(oAddTimeSlot.split(':')[0]) and int(
                        value[0].split(':')[1]) >= int(oAddTimeSlot.split(':')[1]) and not blnFlag:
                    output.append(oTimeSlotList)
                    seen.add(oTimeSlotList)
                    output.append(value)
                    seen.add(value)
                    blnFlag = True
                else:
                    output.append(value)
                    seen.add(value)
        if not blnFlag:
            output.append(oTimeSlotList)
            seen.add(oTimeSlotList)

    return output


def add_timeslot(context):
    output = []
    seen = set()
    values = context.oSchedDict[context.strDay]
    if not "O" in context.addSlotState.upper():
        oTimeSlotList = (context.addSlotTime, float(context.addSlotState))
    else:
        oTimeSlotList = (context.addSlotTime, context.addSlotState)

    blnFlag = False
    for value in values:
        if value not in seen:
            if int(value[0].split(':')[0]) > int(context.addSlotTime.split(':')[0]) and not blnFlag:
                output.append(oTimeSlotList)
                seen.add(oTimeSlotList)
                output.append(value)
                seen.add(value)
                blnFlag = True
            elif int(value[0].split(':')[0]) == int(context.addSlotTime.split(':')[0]) and int(
                    value[0].split(':')[1]) >= int(context.addSlotTime.split(':')[1]) and not blnFlag:
                output.append(oTimeSlotList)
                seen.add(oTimeSlotList)
                output.append(value)
                seen.add(value)
                blnFlag = True
            else:
                output.append(value)
                seen.add(value)
    if not blnFlag:
        output.append(oTimeSlotList)
        seen.add(oTimeSlotList)

    return output


def del_timeslot(context):
    output = []
    seen = set()
    values = context.oSchedDict[context.strDay]
    blnFlag = False
    intEventCount = 0
    context.intEvent = 0
    for value in values:
        if value not in seen:
            if int(value[0].split(':')[0]) == int(context.addSlotTime.split(':')[0]) and int(
                    value[0].split(':')[1]) == int(context.addSlotTime.split(':')[1]):
                if not blnFlag:
                    intEventCount += 1
                    context.intEvent = intEventCount
                blnFlag = True
            else:
                if not blnFlag:
                    intEventCount += 1
                output.append(value)
                seen.add(value)
    if not blnFlag:
        context.report_fail("The Time Slot " + context.addSlotTime + " is not found in schedule, Exit condition")
        exit()

    return output


def createRandomSceduleFormatFromTable(context, strFieldName, intNumberOfEvents):
    if intNumberOfEvents == 0:
        intNumberOfEvents = random.randrange(2, 8, 2)
        if context.oThermostatEP.type == 'WATER':
            oSchedList = \
                converWaterStateForSchedule({context.strDay: buildCompleteRandomScheduleForWater(intNumberOfEvents)})[
                    context.strDay]
        else:
            oSchedList = buildCompleteRandomSchedule(intNumberOfEvents)
        return makeSixEventSceduleFormat(oSchedList)
    else:
        if context.oThermostatEP.type == 'WATER':
            oSchedList = \
                converWaterStateForSchedule({context.strDay: buildCompleteRandomScheduleForWater(intNumberOfEvents)})[
                    context.strDay]
        else:
            oSchedList = buildCompleteRandomSchedule(intNumberOfEvents)
        if strFieldName == 'Start Time':
            intReplaceIndex = 0
        elif strFieldName == 'Target Temperature' or strFieldName == 'Hot Water State':
            intReplaceIndex = 1
        else:
            return makeSixEventSceduleFormat(oSchedList)

        for intCntr in range(len(context.table.rows)):
            oSchedList[intCntr] = list(oSchedList[intCntr])
            strCellVal = context.table.rows[intCntr][strFieldName]
            if strFieldName == 'Hot Water State': strCellVal = oWaterStateDict[strCellVal]
            if intReplaceIndex == 1: strCellVal = float(strCellVal)
            oSchedList[intCntr][intReplaceIndex] = strCellVal
            oSchedList[intCntr] = tuple(oSchedList[intCntr])
    return makeSixEventSceduleFormat(oSchedList)


# Creates a Dictionary Object for the schedule that is passed from the datatable where only list of Target temperature is passed
def createSceduleFormatFromTableWithoutStartTime(context):
    oSchedList = []
    oSchedList.clear()
    if not tableRowVaidate(context, 1, 6): return
    intScedStartMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
    intScedStartMin = intScedStartMin + (15 - (intScedStartMin % 15))
    intRowCount = len(context.table.rows)
    for intTmp in range(6 - intRowCount):
        strStartTime = timeStringToMinutes(intScedStartMin)
        if hasattr(context, 'oNaThermostatEP'):
            eventValue = context.table.rows[0]['Target Temperature']
        else:
            if context.oThermostatEP.type == 'WATER':
                eventValue = oWaterStateDict[context.table.rows[0]['Hot Water State'].upper()]
            elif context.oThermostatEP.type == 'PLUG':
                eventValue = oPlugStateDict[context.table.rows[0]['Active Plug State'].upper()]
            else:
                eventValue = float(context.table.rows[0]['Target Temperature'])
        oSchedList = oSchedList + [(strStartTime, eventValue)]
    for oRow in context.table:
        strStartTime = timeStringToMinutes(intScedStartMin)
        if hasattr(context, 'oNaThermostatEP'):
            eventValue = context.table.rows[0]['Target Temperature']
        else:
            if context.oThermostatEP.type == 'WATER':
                eventValue = oWaterStateDict[oRow['Hot Water State'].upper()]
            elif context.oThermostatEP.type == 'PLUG':
                eventValue = oPlugStateDict[oRow['Active Plug State'].upper()]
            else:
                eventValue = float(oRow['Target Temperature'])
                # if not tempValidate(context, float(oRow['Target Temperature'])): return

        oSchedList = oSchedList + [(strStartTime, eventValue)]
        intScedStartMin += 15
    return oSchedList


def createLightSceduleFormatFromTableWithoutStartTime(context):
    oSchedList = []
    oSchedList.clear()
    if not tableRowVaidate(context, 1, 6): return
    intScedStartMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
    intScedStartMin = intScedStartMin + (15 - (intScedStartMin % 15))
    intRowCount = len(context.table.rows)
    for intTmp in range(6 - intRowCount):
        strStartTime = timeStringToMinutes(intScedStartMin)
        eventStatus = int(context.table.rows[0]['Status'])
        eventValue = int(context.table.rows[0]['Brightness Value'])
        if len(context.table.headings) > 2:
            if context.oLightEP.type == 'COLOURLIGHT':
                eventTone = str(context.table.rows[0]['Tone / Colour'])
            else:
                eventTone = str(context.table.rows[0]['Tone'])
            oSchedList = oSchedList + [(strStartTime, eventStatus, eventValue, eventTone)]
        else:
            oSchedList = oSchedList + [(strStartTime, eventStatus, eventValue)]
    for oRow in context.table:
        strStartTime = timeStringToMinutes(intScedStartMin)
        eventStatus = oRow['Status']
        eventValue = int(oRow['Brightness Value'])
        if len(context.table.headings) > 2:
            if context.oLightEP.type == 'COLOURLIGHT':
                eventTone = str(oRow['Tone / Colour'])
            else:
                eventTone = str(oRow['Tone'])
            oSchedList = oSchedList + [(strStartTime, eventStatus, eventValue, eventTone)]
        # if not tempValidate(context, int(oRow['Brightness Value'])): return
        else:
            oSchedList = oSchedList + [(strStartTime, eventStatus, eventValue)]
        intScedStartMin += 15
    return oSchedList


# Creates a Dictionary Object for the schedule that is passed from the datatable where only list of Target temperature is passed
def createSceduleFormatFromTableWithEventPosition(context, strCurrentEvenPosition):
    if not eventPositionVaidate(context, strCurrentEvenPosition): return False
    intCurrentEvenPosition = oEventPositionDict[strCurrentEvenPosition.upper()]

    oSchedList = []
    oSchedList.clear()

    if not tableRowVaidate(context, 1, 6): return

    intScedStartMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
    intScedStartMin = intScedStartMin + (15 - (intScedStartMin % 15))
    intScedStartMin = intScedStartMin - 15 * intCurrentEvenPosition
    intRowCount = len(context.table.rows)
    for intTmp in range(6 - intRowCount):
        strStartTime = timeStringToMinutes(intScedStartMin)
        if context.oThermostatEP.type == 'WATER':
            eventValue = oWaterStateDict[context.table.rows[0]['Hot Water State'].upper()]
        elif context.oThermostatEP.type == 'PLUG':
            eventValue = oPlugStateDict[context.table.rows[0]['Active Plug State'].upper()]
        else:
            eventValue = float(context.table.rows[0]['Target Temperature'])
        oSchedList = oSchedList + [(strStartTime, eventValue)]
    for oRow in context.table:
        strStartTime = timeStringToMinutes(intScedStartMin)
        if context.oThermostatEP.type == 'WATER':
            eventValue = oWaterStateDict[oRow['Hot Water State'].upper()]
        elif context.oThermostatEP.type == 'PLUG':
            eventValue = oPlugStateDict[oRow['Active Plug State'].upper()]
        else:
            eventValue = float(oRow['Target Temperature'])
            if not tempValidate(context, float(oRow['Target Temperature'])): return
        oSchedList = oSchedList + [(strStartTime, eventValue)]
        intScedStartMin += 15
    return oSchedList


# Creates a Dictionary Object for the schedule that is passed from the datatable
def createSceduleFormatFromTable(context):
    oSchedList = []
    oSchedList.clear()

    if not tableRowVaidate(context, 1, 6): return False
    if not timeSequenceValidate(context, 'Start Time'): return False
    intRowCount = len(context.table.rows)
    for intTmp in range(6 - intRowCount):
        if hasattr(context, 'oNaThermostatEP'):
            eventValue = context.table.rows[0]['Target Temperature']
        else:
            if context.oThermostatEP.type == 'WATER':
                eventValue = oWaterStateDict[context.table.rows[0]['Hot Water State'].upper()]
            elif context.oThermostatEP.type == 'PLUG':
                eventValue = oPlugStateDict[context.table.rows[0]['Active Plug State'].upper()]
            else:
                eventValue = context.table.rows[0]['Target Temperature']
        oSchedList = oSchedList + [(context.table.rows[0]['Start Time'], eventValue)]
    for oRow in context.table:
        if not timeValidate(context, oRow['Start Time']): return False
        if hasattr(context, 'oNaThermostatEP'):
            eventValue = str(oRow['Target Temperature'])

        else:
            if context.oThermostatEP.type == 'WATER':
                eventValue = oWaterStateDict[oRow['Hot Water State'].upper()]
            elif context.oThermostatEP.type == 'PLUG':
                eventValue = oPlugStateDict[oRow['Active Plug State'].upper()]
            else:
                eventValue = float(oRow['Target Temperature'])
                if not tempValidate(context, float(oRow['Target Temperature'])): return False
        oSchedList = oSchedList + [(oRow['Start Time'], eventValue)]
    return oSchedList


def createLightSceduleFormatFromTable(context):
    oSchedList = []
    oSchedList.clear()

    if not tableRowVaidate(context, 1, 6): return False
    if not timeSequenceValidate(context, 'Start Time'): return False
    intRowCount = len(context.table.rows)
    for intTmp in range(6 - intRowCount):
        eventStatus = str(context.table.rows[0]['Status'])
        eventValue = int(context.table.rows[0]['Brightness Value'])
        if len(context.table.headings) > 3:
            if context.oLightEP.type == 'COLOURLIGHT':
                eventTone = str(context.table.rows[0]['Tone / Colour'])
            else:
                eventTone = str(context.table.rows[0]['Tone'])
            oSchedList = oSchedList + [(context.table.rows[0]['Start Time'], eventStatus, eventValue, eventTone)]
        else:
            oSchedList = oSchedList + [(context.table.rows[0]['Start Time'], eventStatus, eventValue)]

    for oRow in context.table:
        if not timeValidate(context, oRow['Start Time']): return False

        eventStatus = str(oRow['Status'])
        eventValue = int(oRow['Brightness Value'])
        if len(context.table.headings) > 3:
            if context.oLightEP.type == 'COLOURLIGHT':
                eventTone = str(oRow['Tone / Colour'])
            else:
                eventTone = str(oRow['Tone'])
            oSchedList = oSchedList + [(oRow['Start Time'], eventStatus, eventValue, eventTone)]
        else:
            oSchedList = oSchedList + [(oRow['Start Time'], eventStatus, eventValue)]
    return oSchedList


# Creates a Dictionary Object for the schedule via hub that is passed from the datatable
def createSceduleFormatFromTableForHUB(context):
    oSchedList = []
    oSchedList.clear()

    if not tableRowVaidate(context, 1, 6): return False
    oOrderedHeaders = orderTableHeaders(context.table.headings)
    if len(searchSubStringInList(oOrderedHeaders, "Time")) > 0:
        if not timeSequenceValidate(context, 'Start Time'): return False

    intRowCount = len(context.table.rows)
    for intTmp in range(6 - intRowCount):
        oRowValList = []
        for oRHead in oOrderedHeaders:
            if 'TEMP' in oRHead.upper():
                strCellVal = float(context.table.rows[0][oRHead])
            elif 'BRIGHT' in oRHead.upper():
                strCellVal = int(context.table.rows[0][oRHead])
            else:
                strCellVal = str(context.table.rows[0][oRHead].upper())

            oRowValList.append(strCellVal)

        oSchedList = oSchedList + [tuple(oRowValList)]

    for oRow in context.table:
        if len(searchSubStringInList(oOrderedHeaders, "Time")) > 0:
            if not timeValidate(context, oRow['Start Time']): return False
        oRowValList = []
        for oRHead in oOrderedHeaders:
            if 'TEMP' in oRHead.upper():
                strCellVal = float(oRow[oRHead])
            elif 'BRIGHT' in oRHead.upper():
                strCellVal = int(oRow[oRHead])
            else:
                strCellVal = str(oRow[oRHead].upper())

            oRowValList.append(strCellVal)
        oSchedList = oSchedList + [tuple(oRowValList)]

    return oSchedList


def orderTableHeaders(oHeaderList):
    newHeaderList = []
    strFilter = "Time"
    if len(searchSubStringInList(oHeaderList, strFilter)) > 0: newHeaderList.append(
        searchSubStringInList(oHeaderList, strFilter)[0])
    strFilter = "Temperature"
    if len(searchSubStringInList(oHeaderList, strFilter)) > 0: newHeaderList.append(
        searchSubStringInList(oHeaderList, strFilter)[0])
    strFilter = "State"
    if len(searchSubStringInList(oHeaderList, strFilter)) > 0: newHeaderList.append(
        searchSubStringInList(oHeaderList, strFilter)[0])
    strFilter = "Bright"
    if len(searchSubStringInList(oHeaderList, strFilter)) > 0: newHeaderList.append(
        searchSubStringInList(oHeaderList, strFilter)[0])

    return newHeaderList


def searchSubStringInList(oList, strSearchString):
    return [oHeader for oHeader in oList if isinstance(oHeader, collections.Iterable) and (strSearchString in oHeader)]


# Create schedule for the smart plugs
def createScheduleForSP(intNumberOfEvents=0, intInterval=0):
    if intNumberOfEvents == 0 and intInterval == 0: return False
    if not intNumberOfEvents == 0:
        intInterval = int(1440 / intNumberOfEvents)

    if not intInterval == 0:
        intNumberOfEvents = 1440 / intInterval

    oWeekDayList = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    oSPSchedule = {}
    oSchedule = []
    oState = ["ON", "OFF"]
    for intDayIndex in range(1, 8):
        oSchedList = []
        oTransitions = []
        intStateIndexCntr = intDayIndex
        for intDeltaminutes in range(0, 1440, intInterval):
            oDayStartTime = datetime.strptime('01Jan2016', '%d%b%Y')
            strTime = oDayStartTime + timedelta(minutes=intDeltaminutes)
            intStateIndex = intStateIndexCntr % 2
            oTransitions.append({"time": strTime.strftime("%H:%M"), "action": {"state": oState[intStateIndex]}})
            oSchedList.append((strTime.strftime("%H:%M"), oState[intStateIndex]))
            intStateIndexCntr = intStateIndexCntr + 1
        oSchedule.append({"dayIndex": intDayIndex, "transitions": oTransitions})
        oSPSchedule[oWeekDayList[intDayIndex - 1]] = oSchedList

    oScheduleDict = {
        "nodes": [
            {
                "attributes": {
                    "syntheticDeviceConfiguration": {
                        "targetValue": {
                            "enabled": "true",
                            "schedule": oSchedule
                        }
                    }
                }
            }
        ]
    }
    return json.dumps(oScheduleDict), oSPSchedule


def createScheduleForHubAPI(oScheduleDictRaw, oSchedule):
    # oSchedule = []

    for strDay in oScheduleDictRaw.keys():
        oTransitions = []
        intDayIndex = oWeekDayList.index(strDay) + 1
        oScheduleListRaw = remove_duplicates(oScheduleDictRaw[strDay])
        for oEvent in oScheduleListRaw:
            strTime = oEvent[0]
            strState = str(oEvent[1])
            if len(oEvent) > 2:
                intBrightness = int(oEvent[2])
                oTransitions.append({"time": strTime, "action": {"brightness": intBrightness, "state": strState}})
            else:
                oTransitions.append({"time": strTime, "action": {"state": strState}})
        oSchedule.append({"dayIndex": intDayIndex, "transitions": oTransitions})

    oScheduleDict = {
        "nodes": [
            {
                "attributes": {
                    "syntheticDeviceConfiguration": {
                        "targetValue": {
                            "enabled": "true",
                            "schedule": oSchedule
                        }
                    }
                }
            }
        ]
    }
    return json.dumps(oScheduleDict)


def createWeekSceduleFormatFromTable(context):
    oSchedDict = {}
    oSchedDict.clear()

    for oRow in context.table:
        strDay = oRow['Day'][:3].lower()
        tempSchdlList = []
        oSchedList = []
        for intColCntr in range(1, len(oRow.cells)):
            if not oRow.cells[intColCntr].strip() == "":
                strTime = oRow.cells[intColCntr].split(',')[0].strip()
                strHeatWaterState = oRow.cells[intColCntr].split(',')[1].strip().upper()
                if hasattr(context, 'oThermostatEP'):
                    # modified since context.oThermostatEP.type alone enough to distungish Heat and Water if it is app testing
                    if hasattr(context, 'deviceType'):
                        if "SLR" in context.deviceType.upper() and not context.oThermostatEP.type == 'WATER':
                            strHeatWaterState = float(
                                strHeatWaterState)
                        else:
                            if context.oThermostatEP.type == 'WATER': strHeatWaterState = float(oWaterStateDict[strHeatWaterState])
                if len(oRow.cells[intColCntr].split(',')) > 2:
                    intBrightness = int(oRow.cells[intColCntr].split(',')[2].strip().upper())
                    tempSchdlList = tempSchdlList + [(strTime, strHeatWaterState, intBrightness)]
                else:
                    if strHeatWaterState in oWaterStateDict:
                        tempSchdlList = tempSchdlList + [(strTime, oWaterStateDict[strHeatWaterState])]
                    else:
                        tempSchdlList = tempSchdlList + [(strTime, strHeatWaterState)]

        for intTmpCntr in range(6 - len(tempSchdlList)):
            oSchedList = oSchedList + [tempSchdlList[0]]

        for oEvent in tempSchdlList:
            oSchedList = oSchedList + [oEvent]

        oSchedDict[strDay] = oSchedList

    # print('oSchedDict', oSchedDict)
    return oSchedDict


def getActiveSchedule(oweeklySchedule, strThermostat):
    dictMode = {'DUAL': 0, 'AUTO': 0, 'HEAT': 2, 'HEATING': 2, 'COOL': 1, 'COOLING': 1, 'autoSchedule': 0,
                'heatSchedule': 2, 'coolSchedule': 1}
    if len(oweeklySchedule) > 1:
        return oweeklySchedule[dictMode[strThermostat]]
    else:
        return oweeklySchedule[0]


# Gets the current Target temperature from the given schedule dictionary object
def getCurrentTempFromSchedule(oSchedule):
    fltTemp = 'NO-TEMP'
    intLeftDurarionMin = 15
    oWeekDay = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    intToday = int(datetime.today().strftime("%w"))
    intYesterday = int(datetime.today().strftime("%w")) - 1
    if intYesterday == -1: intYesterday = 6
    strToday = oWeekDay[intToday]
    strYesterday = oWeekDay[intYesterday]

    intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))

    if strToday in oSchedule:
        oScheduleList = oSchedule[strToday]
        for intCntr in range(len(oScheduleList)):
            intEventStartMin = tt.timeStringToMinutes(oScheduleList[intCntr][0])
            if intCntr == 0 and intCurrentMin < intEventStartMin:
                if strYesterday in oSchedule:
                    oYestScheduleList = oSchedule[strYesterday]
                    fltTemp = oYestScheduleList[len(oYestScheduleList) - 1][1]
                    intLeftDurarionMin = intEventStartMin - intCurrentMin
                    return fltTemp, intLeftDurarionMin
                else:
                    return 0.0, 0
            if intCntr == len(oScheduleList) - 1:
                fltTemp = oScheduleList[intCntr][1]
                return fltTemp, intLeftDurarionMin
            elif (intCurrentMin >= intEventStartMin) and (
                        intCurrentMin < tt.timeStringToMinutes(oScheduleList[intCntr + 1][0])):
                fltTemp = oScheduleList[intCntr][1]
                intLeftDurarionMin = tt.timeStringToMinutes(oScheduleList[intCntr + 1][0]) - intCurrentMin
                return fltTemp, intLeftDurarionMin
    else:
        return 0.0, 0
    return fltTemp, intLeftDurarionMin


# Gets the current Target temperature from the given schedule dictionary object
def getCurrentTempFromTimeZoneSchedule(timeZone, oSchedule):
    fltTemp = 'NO-TEMP'
    intLeftDurarionMin = 15
    oWeekDay = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    tz = TZ.getTZ(timeZone)
    intToday = int(datetime.now(tz).strftime("%w"))
    intYesterday = int(datetime.now(tz).strftime("%w")) - 1
    if intYesterday == -1: intYesterday = 6
    strToday = oWeekDay[intToday]
    strYesterday = oWeekDay[intYesterday]

    intCurrentMin = tt.timeStringToMinutes(datetime.now(tz).strftime("%H:%M"))
    if strToday in oSchedule:
        oScheduleList = oSchedule[strToday]
        for intCntr in range(len(oScheduleList)):
            intEventStartMin = tt.timeStringToMinutes(oScheduleList[intCntr][0])
            if intCntr == 0 and intCurrentMin < intEventStartMin:
                if strYesterday in oSchedule:
                    oYestScheduleList = oSchedule[strYesterday]
                    fltTemp = oYestScheduleList[len(oYestScheduleList) - 1][1]
                    intLeftDurarionMin = intEventStartMin - intCurrentMin
                    return fltTemp, intLeftDurarionMin
                else:
                    return 0.0, 0
            if intCntr == len(oScheduleList) - 1:
                fltTemp = oScheduleList[intCntr][1]
                return fltTemp, intLeftDurarionMin
            elif (intCurrentMin >= intEventStartMin) and (
                        intCurrentMin < tt.timeStringToMinutes(oScheduleList[intCntr + 1][0])):
                fltTemp = oScheduleList[intCntr][1]
                intLeftDurarionMin = tt.timeStringToMinutes(oScheduleList[intCntr + 1][0]) - intCurrentMin
                return fltTemp, intLeftDurarionMin
    else:
        return 0.0, 0
    return fltTemp, intLeftDurarionMin


# Gets the current Target temperature from the given schedule dictionary object
def getCurrentTempAndNextEventTimeFromSchedule(oSchedule):
    fltTemp = 'NO-TEMP'
    intLeftDurarionMin = 15
    oWeekDay = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    intToday = int(datetime.today().strftime("%w"))
    intYesterday = int(datetime.today().strftime("%w")) - 1
    if intYesterday == -1: intYesterday = 6
    intTomorrow = int(datetime.today().strftime("%w")) + 1
    if intTomorrow == 7: intTomorrow = 0
    strToday = oWeekDay[intToday]
    strYesterday = oWeekDay[intYesterday]
    strTomorrow = oWeekDay[intTomorrow]

    intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
    if strToday in oSchedule:
        oScheduleList = remove_duplicates(oSchedule[strToday])
        for intCntr in range(len(oScheduleList)):
            intEventStartMin = tt.timeStringToMinutes(oScheduleList[intCntr][0])
            if intCntr == 0 and intCurrentMin < intEventStartMin:
                if strYesterday in oSchedule:
                    oYestScheduleList = oSchedule[strYesterday]
                    fltTemp = oYestScheduleList[len(oYestScheduleList) - 1][1]
                    intLeftDurarionMin = intEventStartMin - intCurrentMin
                    return fltTemp, intLeftDurarionMin, oScheduleList[intCntr][0], 'Today'
                else:
                    return 0.0, 0, '0:00', 'Today'
            if intCntr == len(oScheduleList) - 1:
                fltTemp = oScheduleList[intCntr][1]
                if strTomorrow in oSchedule:
                    oTomoScheduleList = oSchedule[strTomorrow]
                    intEventStartMin = tt.timeStringToMinutes(oTomoScheduleList[0][0])
                    intLeftDurarionMin = intEventStartMin - intCurrentMin + 1440
                    return fltTemp, intLeftDurarionMin, oTomoScheduleList[0][0], 'Tomorrow'
                return fltTemp, intLeftDurarionMin, oScheduleList[intCntr][0], 'Today'
            elif (intCurrentMin >= intEventStartMin) and (
                        intCurrentMin < tt.timeStringToMinutes(oScheduleList[intCntr + 1][0])):
                fltTemp = oScheduleList[intCntr][1]
                intLeftDurarionMin = tt.timeStringToMinutes(oScheduleList[intCntr + 1][0]) - intCurrentMin
                return fltTemp, intLeftDurarionMin, oScheduleList[intCntr + 1][0], 'Today'
    else:
        return 0.0, 0, '0:00', 'Today'
    return fltTemp, intLeftDurarionMin


def getSPCurrentStateAndNextEventTimeFromSchedule(oSchedule):
    strState = ''
    intLeftDurarionMin = 15
    oWeekDay = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    intToday = int(datetime.today().strftime("%w"))
    intYesterday = int(datetime.today().strftime("%w")) - 1
    if intYesterday == -1: intYesterday = 6
    intTomorrow = int(datetime.today().strftime("%w")) + 1
    if intTomorrow == 7: intTomorrow = 0
    strToday = oWeekDay[intToday]
    strYesterday = oWeekDay[intYesterday]
    strTomorrow = oWeekDay[intTomorrow]

    intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
    if strToday in oSchedule:
        oScheduleList = remove_duplicates(oSchedule[strToday])
        for intCntr in range(len(oScheduleList)):
            intEventStartMin = tt.timeStringToMinutes(oScheduleList[intCntr][0])
            if intCntr == 0 and intCurrentMin < intEventStartMin:
                if strYesterday in oSchedule:
                    oYestScheduleList = oSchedule[strYesterday]
                    strState = oYestScheduleList[len(oYestScheduleList) - 1][1]
                    intLeftDurarionMin = intEventStartMin - intCurrentMin
                    return strState, intLeftDurarionMin, oScheduleList[intCntr][0], 'Today'
                else:
                    return strState, 0, '0:00', 'Today'
            if intCntr == len(oScheduleList) - 1:
                strState = oScheduleList[intCntr][1]
                if strTomorrow in oSchedule:
                    oTomoScheduleList = oSchedule[strTomorrow]
                    intEventStartMin = tt.timeStringToMinutes(oTomoScheduleList[0][0])
                    intLeftDurarionMin = intEventStartMin - intCurrentMin + 1440
                    return strState, intLeftDurarionMin, oTomoScheduleList[0][0], 'Tomorrow'
                return strState, intLeftDurarionMin, oScheduleList[intCntr][0], 'Today'
            elif (intCurrentMin >= intEventStartMin) and (
                        intCurrentMin < tt.timeStringToMinutes(oScheduleList[intCntr + 1][0])):
                strState = oScheduleList[intCntr][1]
                intLeftDurarionMin = tt.timeStringToMinutes(oScheduleList[intCntr + 1][0]) - intCurrentMin
                return strState, intLeftDurarionMin, oScheduleList[intCntr + 1][0], 'Today'
    else:
        return strState, 0, '0:00', 'Today'
    return strState, intLeftDurarionMin


def getDeviceCurrentStateAndNextEventTimeFromSchedule(oSchedule):
    strState = ''
    intLeftDurarionMin = 15
    oWeekDay = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    intToday = int(datetime.today().strftime("%w"))
    intYesterday = int(datetime.today().strftime("%w")) - 1
    if intYesterday == -1: intYesterday = 6
    intTomorrow = int(datetime.today().strftime("%w")) + 1
    if intTomorrow == 7: intTomorrow = 0
    strToday = oWeekDay[intToday]
    strYesterday = oWeekDay[intYesterday]
    strTomorrow = oWeekDay[intTomorrow]

    intBrightness = 0
    intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
    if strToday in oSchedule:
        oScheduleList = remove_duplicates(oSchedule[strToday])
        for intCntr in range(len(oScheduleList)):
            intEventStartMin = tt.timeStringToMinutes(oScheduleList[intCntr][0])

            if intCntr == 0 and intCurrentMin < intEventStartMin:
                if strYesterday in oSchedule:
                    oYestScheduleList = oSchedule[strYesterday]
                    oEvent = oYestScheduleList[len(oYestScheduleList) - 1]
                    strState = oEvent[1]
                    if len(oEvent) > 2: intBrightness = oEvent[2]
                    intLeftDurarionMin = intEventStartMin - intCurrentMin
                    return strState, intBrightness, intLeftDurarionMin, oScheduleList[intCntr][0], 'Today'
                else:
                    return strState, intBrightness, 0, '0:00', 'Today'

            if intCntr == len(oScheduleList) - 1:
                strState = oScheduleList[intCntr][1]
                if len(oScheduleList[intCntr]) > 2: intBrightness = oScheduleList[intCntr][2]
                if strTomorrow in oSchedule:
                    oTomoScheduleList = oSchedule[strTomorrow]
                    intEventStartMin = tt.timeStringToMinutes(oTomoScheduleList[0][0])
                    intLeftDurarionMin = intEventStartMin - intCurrentMin + 1440
                    return strState, intBrightness, intLeftDurarionMin, oTomoScheduleList[0][0], 'Tomorrow'
                return strState, intBrightness, intLeftDurarionMin, oScheduleList[intCntr][0], 'Today'

            elif (intCurrentMin >= intEventStartMin) and (
                        intCurrentMin < tt.timeStringToMinutes(oScheduleList[intCntr + 1][0])):
                print(str(oScheduleList[intCntr][2]) + " \n")
                strState = oScheduleList[intCntr][1]
                if len(oScheduleList[intCntr]) > 2: intBrightness = oScheduleList[intCntr][2]
                intLeftDurarionMin = tt.timeStringToMinutes(oScheduleList[intCntr + 1][0]) - intCurrentMin
                return strState, intBrightness, intLeftDurarionMin, oScheduleList[intCntr + 1][0], 'Today'

    else:
        return strState, intBrightness, 0, '0:00', 'Today'
    return strState, intBrightness, intLeftDurarionMin


def checkGuardTime(nextEventStartTime, nextEventDay):
    strCurrentTime = datetime.today().strftime("%H:%M")
    intCurrentMin = tt.timeStringToMinutes(strCurrentTime)
    intNextEventStartTimeMinute = tt.timeStringToMinutes(nextEventStartTime)
    if 'TOMO' in nextEventDay.upper(): intNextEventStartTimeMinute = intNextEventStartTimeMinute + 1440
    if intCurrentMin > intNextEventStartTimeMinute:
        if intNextEventStartTimeMinute - intCurrentMin < 2:
            time.sleep(60)
        return False
    else:
        if abs(intNextEventStartTimeMinute - intCurrentMin) < 2:
            time.sleep(60)
            return False
        return True


# Converts the time string to Minutes Integer
def timeStringToMinutes(intMinutes):
    """ Convert an integer number of minutes since midnight to a 'hh:mm' string 
    
    """
    intHours = (intMinutes // 60) % 24
    intMinutes = intMinutes % 60
    strTime = '{:02d}:{:02d}'.format(intHours, intMinutes)
    return strTime


# Validate the Temperature is in the right Format
def tempValidate(context, strTemperature):
    fltTemperature = float(strTemperature)
    if (fltTemperature < 5 or fltTemperature > 32) and fltTemperature != 1.0:
        context.boolScenarioExecStatus = False
        context.strStepFailReason = 'Temperature ' + str(strTemperature) + ' passed is not within the range 5 to 32 C'
        return False
    else:
        return True


# Validates the format of the temperature and it falls between 5 to 32C
def timeValidate(context, strTime):
    intHour = int(strTime.split(':')[0])
    intMinute = int(strTime.split(':')[1])

    if (intHour < 0 or intHour > 23) or (intMinute < 0 or intMinute > 59):
        context.boolScenarioExecStatus = False
        context.strStepFailReason = 'Start Time ' + strTime + ' passed is not within the 24 hour range'
    else:
        return True


# Validates the number are records in the datatable. It should be between 1 to 6
def tableRowVaidate(context, intMinRow, intMaxRow):
    if (len(context.table.rows) < int(intMinRow)) or (len(context.table.rows) > int(intMaxRow)):
        context.boolScenarioExecStatus = False
        context.strStepFailReason = "There should at least be one and a maximum of six events for the schedule<br>" + str(
            context.table)
        return False
    if context.reporter.platformVersion == 'V5':
        if not ((len(context.table.rows) == 4) or (len(context.table.rows) == 6)):
            context.boolScenarioExecStatus = False
            context.strStepFailReason = "Only FOUR and SIX events schedule can be set for a V5 User<br>" + str(
                context.table)
            return False

    return True


def eventPositionVaidate(context, strCurrentEvenPosition):
    if not strCurrentEvenPosition.upper() in oEventPositionDict:
        context.boolScenarioExecStatus = False
        context.strStepFailReason = "The Event Position given should only be one of these [ FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH] <br> But the given Event psosition is " + strCurrentEvenPosition + str(
            context.table)
        return False
    if oEventPositionDict[strCurrentEvenPosition.upper()] > len(context.table.rows):
        context.boolScenarioExecStatus = False
        context.strStepFailReason = "The Event Position given is more than the number of events. Please check and re-execute<br>" + str(
            context.table)
        return False
    else:
        return True


# The List of start time passed in the datatable should be in ascending order. This function validates the same
def timeSequenceValidate(context, strColumnName):
    fltPreviousTime = 0.0
    for oRow in context.table:
        strTime = oRow[strColumnName]
        if not timeValidate(context, strTime): return
        fltCurrentTime = float(strTime.replace(':', '.'))
        if fltPreviousTime > fltCurrentTime:
            context.boolScenarioExecStatus = False
            context.strStepFailReason = "The Time in the table is not following a sequence. Please modify and re-execute the scenario<br>" + str(
                context.table)
            return False
        fltPreviousTime = fltCurrentTime
    else:
        return True


# Updates the HTML report with the Schedule that is passed to this function
def reportSchedule(oThermostatEP, reporter, oSchedule):
    for oKey in oSchedule.keys():
        oSheduleList = remove_duplicates(oSchedule[oKey])
        strLog = getScheduleForReport(oSheduleList, oKey)
        reporter.ReportEvent('Test Validation', strLog, 'DONE', 'CENTER')


def converWaterStateForSchedule(oSchedule):
    oNewSchedule = {}
    for oKey in oSchedule.keys():
        oSchedList = oSchedule[oKey]
        oNewSchedList = []
        for oEvent in oSchedList:
            strEventTime = oEvent[0]
            strEventValue = oWaterStateDict[oEvent[1]]
            oNewSchedList.append((strEventTime, strEventValue))
        oNewSchedule.update({oKey: oNewSchedList})
    return oNewSchedule


def converPlugStateForSchedule(oSchedule):
    oNewSchedule = {}
    for oKey in oSchedule.keys():
        oSchedList = oSchedule[oKey]
        oNewSchedList = []
        for oEvent in oSchedList:
            strEventTime = oEvent[0]
            strEventValue = oPlugStateDict[oEvent[1]]
            oNewSchedList.append((strEventTime, strEventValue))
        oNewSchedule.update({oKey: oNewSchedList})
    return oNewSchedule


# Compare the two schedule that is passed to this function
def compareSchedules(context, oDictExpect, oDictActual, oKey):
    oExpectSchedList = oDictExpect[oKey]
    oActualSchedList = oDictActual[oKey]

    if len(oExpectSchedList) != len(oActualSchedList):
        strLog = getScheduleForReportWithoutComparison(oExpectSchedList, oActualSchedList,
                                                       oKey)  # The Events in the Expected and Actual Schedule are not matching.<Br> Please find the schedules below:<Br>'  +
        context.reporter.ReportEvent('Test Validation', strLog, 'FAIL', 'CENTER')
        return
    strLog, strStatus = getScheduleForReportWithComparison(oExpectSchedList, oActualSchedList, oKey)
    context.reporter.ReportEvent('Test Validation', strLog, strStatus, 'CENTER')


# Compares the schedule and updates the report
def getScheduleForReportWithComparison(oExpectSchedList, oActualSchedList, oKey=None):
    boolCompStatus = 'PASS'
    strExpTimeRow = ""
    strExpTempRow = ""
    strExpBrightnessRow = ""
    strActTimeRow = ""
    strActTempRow = ""
    strActBrightnessRow = ""

    intMax = max(len(oExpectSchedList), len(oActualSchedList))
    for intCntr in range(intMax):
        strExpStartTime = ''
        strExpTemp = ''
        strExpBrightness = ''
        strActStartTime = ''
        strActTemp = ''
        strActBrightness = ''
        boolBrightness = False

        if len(oExpectSchedList) > intCntr: strExpStartTime = oExpectSchedList[intCntr][0]
        if len(oExpectSchedList) > intCntr:
            strExpTemp = oExpectSchedList[intCntr][1]
            if len(oExpectSchedList[intCntr]) > 2:
                if len(oExpectSchedList) > intCntr: strExpBrightness = oExpectSchedList[intCntr][2]
                boolBrightness = True
        if len(oActualSchedList) > intCntr: strActStartTime = oActualSchedList[intCntr][0]
        if len(oActualSchedList) > intCntr: strActTemp = oActualSchedList[intCntr][1]
        if len(oActualSchedList) > intCntr:
            if len(oActualSchedList[intCntr]) > 2:
                if len(oActualSchedList) > intCntr: strActBrightness = oActualSchedList[intCntr][2]
                boolBrightness = True
        try:
            if float(strExpTemp) != strActTemp:
                strActTemp = '||' + str(strActTemp)
                boolCompStatus = 'FAIL'
        except:
            if str(strExpTemp) != str(strActTemp):
                strActTemp = '||' + str(strActTemp)
                boolCompStatus = 'FAIL'

        if strExpStartTime != strActStartTime:
            strActStartTime = '||' + strActStartTime
            boolCompStatus = 'FAIL'

        if strExpBrightness != strActBrightness:
            strActBrightness = '||' + strActBrightness
            boolCompStatus = 'FAIL'

        strExpTimeRow = strExpTimeRow + strExpStartTime + "$$"
        strExpTempRow = strExpTempRow + str(strExpTemp) + "$$"
        if boolBrightness: strExpBrightnessRow = strExpBrightnessRow + str(strExpBrightness) + "$$"

        strActTimeRow = strActTimeRow + strActStartTime + "$$"
        strActTempRow = strActTempRow + str(strActTemp) + "$$"
        if boolBrightness: strActBrightnessRow = strActBrightnessRow + str(strActBrightness) + "$$"

    strTarg = 'Targ-Temp'
    if 'ON' in oExpectSchedList[0] or 'OFF' in oExpectSchedList[0]: strTarg = 'Device State'
    strReportSchedule = getSchedLog(oExpectSchedList, oActualSchedList, strExpTimeRow, strExpTempRow, strActTimeRow,
                                    strActTempRow, oKey, strTarg, strExpBrightnessRow, strActBrightnessRow)
    return strReportSchedule, boolCompStatus


# Updates the report withour comparing the two schedules
def getScheduleForReportWithoutComparison(oExpectSchedList, oActualSchedList, oKey=None):
    strExpTimeRow = ""
    strExpTempRow = ""
    strActTimeRow = ""
    strActTempRow = ""
    for intCntr in range(len(oExpectSchedList)):
        strExpStartTime = oExpectSchedList[intCntr][0]
        strExpTemp = oExpectSchedList[intCntr][1]
        strExpTimeRow = strExpTimeRow + strExpStartTime + "$$"
        strExpTempRow = strExpTempRow + str(strExpTemp) + "$$"
    for intCntr in range(len(oActualSchedList)):
        strActStartTime = oActualSchedList[intCntr][0]
        strActTemp = oActualSchedList[intCntr][1]
        strActTimeRow = strActTimeRow + strActStartTime + "$$"
        strActTempRow = strActTempRow + str(strActTemp) + "$$"

    strReportSchedule = getSchedLog(oExpectSchedList, oActualSchedList, strExpTimeRow, strExpTempRow, strActTimeRow,
                                    strActTempRow, oKey)
    return strReportSchedule


# Creates a log string that can be used to update the report
def getSchedLog(oExpectSchedList, oActualSchedList, strExpTimeRow, strExpTempRow, strActTimeRow, strActTempRow, oKey,
                strTarg, strExpBrightnessRow="", strActBrightnessRow="", strExpToneRow="", strActToneRow=""):
    strExpTimeRow = strExpTimeRow[:len(strExpTimeRow) - 2]
    strExpTempRow = strExpTempRow[:len(strExpTempRow) - 2]
    strActTimeRow = strActTimeRow[:len(strActTimeRow) - 2]
    strActTempRow = strActTempRow[:len(strActTempRow) - 2]
    if not strExpBrightnessRow == "":
        strExpBrightnessRow = strExpBrightnessRow[:len(strExpBrightnessRow) - 2]
        strActBrightnessRow = strActBrightnessRow[:len(strActBrightnessRow) - 2]
    if not strExpToneRow == "":
        strExpToneRow = strExpToneRow[:len(strExpToneRow) - 2]
        strActToneRow = strActToneRow[:len(strActToneRow) - 2]

    intMinEvent = min(len(oExpectSchedList), len(oActualSchedList))
    intMaxEvent = max(len(oExpectSchedList), len(oActualSchedList)) + 1
    strEvent = ""
    for intCntr in range(1, intMaxEvent):
        strTempEvent = 'Event ' + str(intCntr)
        if intCntr > intMinEvent: strTempEvent = '||Event ' + str(intCntr)
        strEvent = strEvent + strTempEvent + '$$'
    strEvent = strEvent[:len(strEvent) - 2]

    intExpRows = '2'
    if not strExpBrightnessRow == "": intExpRows = '3'
    if not strExpToneRow == "": intExpRows = '4'
    strHeader = 'Value Type    $$   Schedule Day   $$  Event Type  $$' + strEvent + '@@@'
    strExpTimeRow = 'Expected&R&' + intExpRows + '$$' + oKey + '&R&' + intExpRows + ' $$' + 'Start Time' + '$$' + strExpTimeRow + '$~'
    strExpTempRow = strTarg + '$$' + strExpTempRow + '$~'  # Expected' + '$$' +
    if not strExpBrightnessRow == "":
        strExpBrightnessRow = "Brightness" + '$$' + strExpBrightnessRow + '$~'
    if not strExpToneRow == "":
        strExpToneRow = "Tone" + '$$' + strExpToneRow + '$~'

    strActTimeRow = 'Actual&R&' + intExpRows + '$$' + oKey + '&R&' + intExpRows + ' $$' + ' Start Time' + '$$' + strActTimeRow + '$~'
    strActTempRow = strTarg + '$$' + strActTempRow
    if not strActBrightnessRow == "":
        strActBrightnessRow = '$~' + "Brightness" + '$$' + strActBrightnessRow
    if not strActToneRow == "":
        strActToneRow = '$~' + "Tone" + '$$' + strActToneRow

    strReportSchedule = strHeader + strExpTimeRow + strExpTempRow + strExpBrightnessRow + strExpToneRow + strActTimeRow + strActTempRow + strActBrightnessRow + strActToneRow
    return strReportSchedule


# Updates the report with the schedule that is passed
def getScheduleForReport(oSchedList, oKey):
    strExpTimeRow = ""
    strExpTempRow = ""
    intExpBrightnessRow = ""
    strExpToneRow = ""
    boolBrightnessExist = False
    boolToneExist = False
    strRowCount = '&R&2'
    for intCntr in range(len(oSchedList)):
        strExpStartTime = oSchedList[intCntr][0]
        strExpTemp = oSchedList[intCntr][1]
        if len(oSchedList[intCntr]) > 2:
            intExpBrightness = str(oSchedList[intCntr][2])
            intExpBrightnessRow = intExpBrightnessRow + str(intExpBrightness) + "$$"
            boolBrightnessExist = True
            strRowCount = '&R&3'
        if len(oSchedList[intCntr]) > 3:
            strExpTone = oSchedList[intCntr][3]
            strExpToneRow = strExpToneRow + strExpTone + "$$"
            boolToneExist = True
            strRowCount = '&R&4'
        strExpTimeRow = strExpTimeRow + strExpStartTime + "$$"
        strExpTempRow = strExpTempRow + str(strExpTemp) + "$$"

    strExpTimeRow = strExpTimeRow[:len(strExpTimeRow) - 2]
    strExpTempRow = strExpTempRow[:len(strExpTempRow) - 2]
    intExpBrightnessRow = intExpBrightnessRow[:len(intExpBrightnessRow) - 2]
    strExpToneRow = strExpToneRow[:len(strExpToneRow) - 2]

    intMaxEvent = len(oSchedList) + 1
    strEvent = ""
    for intCntr in range(1, intMaxEvent):
        strTempEvent = 'Event ' + str(intCntr)
        strEvent = strEvent + strTempEvent + '$$'
    strEvent = strEvent[:len(strEvent) - 2]

    strTarg = 'Targ-Temp'
    if 'ON' in oSchedList[0] or 'OFF' in oSchedList[0]: strTarg = 'Device State'
    strHeader = 'Schedule Day   $$  Event Type  $$' + strEvent + '@@@'
    strExpTimeRow = oKey + strRowCount + ' $$' + 'Start Time' + '$$' + strExpTimeRow + '$~'
    strExpTempRow = strTarg + '$$' + strExpTempRow
    if boolBrightnessExist:
        intExpBrightnessRow = '$~' + "Brightness" + '$$' + intExpBrightnessRow
    if boolToneExist:
        strExpToneRow = '$~' + "Tone / Colour" + '$$' + strExpToneRow

    strReportSchedule = strHeader + strExpTimeRow + strExpTempRow + intExpBrightnessRow + strExpToneRow
    return strReportSchedule


# Runs the validation for the given period
def runValidationForPeriod(context, fltTargetTemp, strCurrentEventStartTime, strNextEventStartTime, strMode='AUTO'):
    intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
    intCurrentEventStartMin = tt.timeStringToMinutes(strCurrentEventStartTime)

    '''
    while intCurrentMin < intCurrentEventStartMin:
        time.sleep(5)        
        print(datetime.today().strftime("%H:%M:%S" ))
        intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M" )) 
    '''
    if intCurrentMin < intCurrentEventStartMin:
        fltExistTargetTemp, intDuration = getCurrentTempFromSchedule(context.oThermostatEP.getSchedule())
        context.rFM.validateSysmode(context.reporter, True, context.oThermostatEP, strMode, fltExistTargetTemp,
                                    intDuration * 60, 20)

    if strNextEventStartTime == '':
        intNexEventMin = intCurrentMin + 15
    else:
        intNexEventMin = tt.timeStringToMinutes(strNextEventStartTime)
    strNextEventTimeDiffinSec = (intNexEventMin - intCurrentMin) * 60

    context.rFM.validateSysmode(context.reporter, True, context.oThermostatEP, strMode, fltTargetTemp, 60, 2)
    context.rFM.validateSysmode(context.reporter, True, context.oThermostatEP, strMode, fltTargetTemp,
                                strNextEventTimeDiffinSec - 60, 30)
    print('Done : ', datetime.today().strftime("%H:%M:%S"))


# Runs the validation for the given period
def runValidationForSchedule(context, oScheduleList):
    strMode = 'AUTO'
    intGaurdTime = 30
    intChekInterval = 20
    for intCntr in range(len(oScheduleList)):
        fltTargetTemp = oScheduleList[intCntr][1]
        strCurrentEventStartTime = oScheduleList[intCntr][0]
        if intCntr == len(oScheduleList) - 1:
            strNextEventStartTime = ""
        else:
            strNextEventStartTime = oScheduleList[intCntr + 1][0]

        intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
        intCurrentEventStartMin = tt.timeStringToMinutes(strCurrentEventStartTime)

        print('Next Event Start time' + strNextEventStartTime)
        # Checks for the first schedule and if current time is less than the first schedule then gets the previous days last
        if intCurrentMin < intCurrentEventStartMin and intCntr == 0:
            oCurrentSchedule = context.oThermostatEP.getSchedule()
            if context.oThermostatEP.type == 'WATER':
                oCurrentSchedule = converWaterStateForSchedule(oCurrentSchedule)
                fltExistTargetTemp, intDuration = getCurrentTempFromSchedule(oCurrentSchedule)
                print(fltExistTargetTemp, intDuration)
            elif context.oThermostatEP.type == 'PLUG':
                oCurrentSchedule = converWaterStateForSchedule(oCurrentSchedule)
                fltExistTargetTemp, intDuration = getCurrentTempFromSchedule(oCurrentSchedule)
                fltExistTargetTemp = oPlugStateDict[fltExistTargetTemp]

            intRemainSecinCurMin = 60 - int(datetime.today().strftime("%S"))
            if not intRemainSecinCurMin == 60:
                time.sleep(intRemainSecinCurMin)
                intDuration = intDuration - 1
            print('Time Before start of validation: ' + datetime.today().strftime("%H:%M:%S"))
            context.rFM.validateSysmode(context.reporter, True, context.oThermostatEP, strMode, fltExistTargetTemp,
                                        (intDuration * 60) - intGaurdTime, intChekInterval)
            context.reporter.ReportEvent('Test Validation',
                                         'Wait for ' + str(intGaurdTime) + ' seconds before the Scheduled Event Change',
                                         'DONE')
            time.sleep(intGaurdTime)

        intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M"))
        # context.reporter.ReportEvent('Testtttttt', 'Next Event Start time' + strNextEventStartTime, 'Done')
        print('Next Event Start time' + strNextEventStartTime)
        if strNextEventStartTime == '':
            intNexEventMin = intCurrentMin + 15
        else:
            intNexEventMin = tt.timeStringToMinutes(strNextEventStartTime)

        print('Current and next even min: ', intCurrentMin, intNexEventMin)
        strNextEventTimeDiffinSec = (intNexEventMin - intCurrentMin) * 60

        context.reporter.ReportEvent('Test Validation',
                                     'Wait for ' + str(intGaurdTime) + ' seconds after the Scheduled Event Change',
                                     'DONE')
        time.sleep(intGaurdTime)
        context.rFM.validateSysmode(context.reporter, False, context.oThermostatEP, strMode, fltTargetTemp,
                                    60 - intGaurdTime, 2)
        context.rFM.validateSysmode(context.reporter, True, context.oThermostatEP, strMode, fltTargetTemp,
                                    (strNextEventTimeDiffinSec - 60) - intGaurdTime, intChekInterval)
        if intCntr != len(oScheduleList) - 1:
            context.reporter.ReportEvent('Test Validation',
                                         'Wait for ' + str(intGaurdTime) + ' seconds before the Scheduled Event Change',
                                         'DONE')
            time.sleep(intGaurdTime)
        print('Done : ', datetime.today().strftime("%H:%M:%S"))


# Runs the SP Schedule validation for the whole week
def runSPValidationForWeekSchedule(context):
    strMode = 'AUTO'
    intGaurdTime = 30
    intChekInterval = 120
    oSPSchedule = context.oSPSchedDict
    while True:
        strSPState, intDuration, nextEventStartTime, nextEventDay = getSPCurrentStateAndNextEventTimeFromSchedule(
            oSPSchedule)
        print(strSPState, intDuration, nextEventStartTime)
        context.rFM.validateSPSysmode(context.reporter, True, context.SPNodeID, strMode, strSPState, intDuration * 60,
                                      intChekInterval, nextEventStartTime=nextEventStartTime, nextEventDay=nextEventDay)


# Runs the validation for the whole week
def runValidationForWeekSchedule(context):
    strMode = 'AUTO'
    intGaurdTime = 30
    intChekInterval = 120
    oSchedule = context.oSchedDict
    while True:
        fltCurrentTargTemp, intDuration, nextEventStartTime, nextEventDay = getCurrentTempAndNextEventTimeFromSchedule(
            oSchedule)
        print(fltCurrentTargTemp, intDuration, nextEventStartTime)
        context.rFM.validateSysmode(context.reporter, True, context.oThermostatEP, strMode, fltCurrentTargTemp,
                                    intDuration * 60, intChekInterval, nextEventStartTime=nextEventStartTime,
                                    nextEventDay=nextEventDay)


# Runs the validation for the whole week
def runValidationForWeekScheduleForDevice(context):
    strMode = 'AUTO'
    intGaurdTime = 30
    intChekInterval = 120
    oSchedule = context.oSchedDict
    while True:
        strState, intBrightness, intDuration, nextEventStartTime, nextEventDay = getDeviceCurrentStateAndNextEventTimeFromSchedule(
            oSchedule)
        print(strState, intDuration, nextEventStartTime)
        context.rFM.validateSPSysmode(context, True, context.NodeID, strMode, strState, intBrightness, intChekInterval,
                                      nextEventStartTime=nextEventStartTime, nextEventDay=nextEventDay)


def getLightScheduleForReportWithComparison(oExpectSchedList, oActualSchedList, oKey=None):
    boolCompStatus = 'PASS'
    strExpTimeRow = ""
    strExpStatusRow = ""
    strExpBrightnessRow = ""
    strExpToneRow = ""
    strActTimeRow = ""
    strActStatusRow = ""
    strActBrightnessRow = ""
    strActToneRow = ""

    intMax = max(len(oExpectSchedList), len(oActualSchedList))
    for intCntr in range(intMax):
        strExpStartTime = ''
        strExpStatus = ''
        strExpBrightness = ''
        strExpTone = ''
        strActStartTime = ''
        strActStatus = ''
        strActBrightness = ''
        strActTone = ''
        boolBrightness = False
        boolTone = False

        if len(oExpectSchedList) > intCntr:
            strExpStartTime = oExpectSchedList[intCntr][0]
            if len(oExpectSchedList) > intCntr: strExpStatus = oExpectSchedList[intCntr][1]
            if len(oExpectSchedList[intCntr]) > 2:
                if len(oExpectSchedList) > intCntr: strExpBrightness = oExpectSchedList[intCntr][2]
                boolBrightness = True
            else:
                strExpBrightness = ''
                boolBrightness = True
            if len(oExpectSchedList[intCntr]) > 3:
                if len(oExpectSchedList) > intCntr: strExpTone = oExpectSchedList[intCntr][3]
                boolTone = True
            else:
                strExpTone = ''
                boolTone = True

        if len(oActualSchedList) > intCntr:
            strActStartTime = oActualSchedList[intCntr][0]
            if len(oActualSchedList) > intCntr: strActStatus = oActualSchedList[intCntr][1]
            if len(oActualSchedList[intCntr]) > 2:
                if len(oActualSchedList) > intCntr: strActBrightness = oActualSchedList[intCntr][2]
                boolBrightness = True
            else:
                strActBrightness = ''
                boolBrightness = True
            if len(oActualSchedList[intCntr]) > 3:
                if len(oActualSchedList) > intCntr: strActTone = oActualSchedList[intCntr][3]
                boolTone = True

        if str(strExpStatus) != str(strActStatus):
            strActStatus = '||' + str(strActStatus)
            boolCompStatus = 'FAIL'

        if strExpStartTime != strActStartTime:
            strActStartTime = '||' + strActStartTime
            boolCompStatus = 'FAIL'

        if strExpBrightness == 0:
            strExpBrightness = ''

        if strExpBrightness != strActBrightness:
            strActBrightness = '||' + str(strActBrightness)
            boolCompStatus = 'FAIL'

        if strExpTone != strActTone:
            strActTone = '||' + strActTone
            boolCompStatus = 'FAIL'

        strExpTimeRow = strExpTimeRow + strExpStartTime + "$$"
        strExpStatusRow = strExpStatusRow + str(strExpStatus) + "$$"
        if boolBrightness:
            strExpBrightnessRow = strExpBrightnessRow + str(strExpBrightness) + "$$"
        if boolTone:
            strExpToneRow = strExpToneRow + str(strExpTone) + "$$"

        strActTimeRow = strActTimeRow + strActStartTime + "$$"
        strActStatusRow = strActStatusRow + str(strActStatus) + "$$"
        if boolBrightness:
            strActBrightnessRow = strActBrightnessRow + str(strActBrightness) + "$$"
        if boolTone:
            strActToneRow = strActToneRow + str(strActTone) + "$$"

    strStatus = 'Device Status'
    strReportSchedule = getSchedLog(oExpectSchedList, oActualSchedList, strExpTimeRow, strExpStatusRow, strActTimeRow,
                                    strActStatusRow, oKey, strStatus, strExpBrightnessRow, strActBrightnessRow,
                                    strExpToneRow, strActToneRow)
    return strReportSchedule, boolCompStatus


def getLightScheduleForReportWithoutComparison(oExpectSchedList, oActualSchedList, oKey=None):
    strExpTimeRow = ""
    strExpStatusRow = ""
    strExpBrightnessRow = ""
    strExpToneRow = ""
    strActTimeRow = ""
    strActStatusRow = ""
    strActBrightnessRow = ""
    strActToneRow = ""
    for intCntr in range(len(oExpectSchedList)):
        strExpStartTime = oExpectSchedList[intCntr][0]
        strExpStatus = oExpectSchedList[intCntr][1]
        strExpBrightness = oExpectSchedList[intCntr][2]
        strExpTone = oExpectSchedList[intCntr][3]
        strExpTimeRow = strExpTimeRow + strExpStartTime + "$$"
        strExpStatusRow = strExpStatusRow + str(strExpStatus) + "$$"
        strExpBrightnessRow = strExpBrightnessRow + str(strExpBrightness) + "$$"
        strExpToneRow = strExpToneRow + str(strExpTone) + "$$"
    for intCntr in range(len(oActualSchedList)):
        strActStartTime = oActualSchedList[intCntr][0]
        strActStatus = oActualSchedList[intCntr][1]
        strActBrightness = oActualSchedList[intCntr][2]
        strActTone = oActualSchedList[intCntr][3]
        strActTimeRow = strActTimeRow + strActStartTime + "$$"
        strActStatusRow = strActStatusRow + str(strActStatus) + "$$"
        strActBrightnessRow = strActBrightnessRow + str(strActBrightness) + "$$"
        strActToneRow = strActToneRow + str(strActTone) + "$$"

    strReportSchedule = getSchedLog(oExpectSchedList, oActualSchedList, strExpTimeRow, strExpStatusRow,
                                    strExpBrightnessRow, strExpToneRow, strActTimeRow,
                                    strActStatusRow, strActBrightnessRow, strActToneRow, oKey)
    return strReportSchedule

    '''for intCntr in range(len(oScheduleList)):
        fltTargetTemp = oScheduleList[intCntr][1]
        strCurrentEventStartTime = oScheduleList[intCntr][0]
        if intCntr == len(oScheduleList) -1 : 
            strNextEventStartTime = ""
        else: 
            strNextEventStartTime = oScheduleList[intCntr + 1][0]
    
        intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M" )) 
        intCurrentEventStartMin = tt.timeStringToMinutes(strCurrentEventStartTime) 
        
        print('Next Event Start time' + strNextEventStartTime)
        #Checks for the first schedule and if current time is less than the first schedule then gets the previous days last  
        if intCurrentMin < intCurrentEventStartMin and intCntr ==0:
            oCurrentSchedule = context.oThermostatEP.getSchedule()
            if context.oThermostatEP.type == 'WATER': oCurrentSchedule = converWaterStateForSchedule(oCurrentSchedule)
            fltExistTargetTemp, intDuration= getCurrentTempFromSchedule(oCurrentSchedule)
            print(fltExistTargetTemp, intDuration)
            intRemainSecinCurMin = 60 - int(datetime.today().strftime("%S" ))
            if not intRemainSecinCurMin == 60: 
                time.sleep(intRemainSecinCurMin)
                intDuration = intDuration-1
            print('Time Before start of validation: ' + datetime.today().strftime("%H:%M:%S" ))
            context.rFM.validateSysmode(context.reporter, True, context.oThermostatEP, strMode, fltExistTargetTemp, (intDuration * 60) - intGaurdTime, intChekInterval)
            context.reporter.ReportEvent('Test Validation','Wait for ' + str(intGaurdTime) + ' seconds before the Scheduled Event Change', 'DONE')
            time.sleep(intGaurdTime)
        
        
        intCurrentMin = tt.timeStringToMinutes(datetime.today().strftime("%H:%M" )) 
        #context.reporter.ReportEvent('Testtttttt', 'Next Event Start time' + strNextEventStartTime, 'Done')   
        print('Next Event Start time' + strNextEventStartTime)
        if strNextEventStartTime =='': intNexEventMin = intCurrentMin + 15
        else: intNexEventMin = tt.timeStringToMinutes(strNextEventStartTime)
        
        print('Currentt and next even min: ', intCurrentMin, intNexEventMin)
        strNextEventTimeDiffinSec = (intNexEventMin - intCurrentMin)* 60
        
        context.reporter.ReportEvent('Test Validation','Wait for ' + str(intGaurdTime) + ' seconds after the Scheduled Event Change', 'DONE')
        time.sleep(intGaurdTime)
        context.rFM.validateSysmode(context.reporter, False, context.oThermostatEP, strMode, fltTargetTemp, 60 - intGaurdTime, 2)
        context.rFM.validateSysmode(context.reporter, True, context.oThermostatEP, strMode, fltTargetTemp, (strNextEventTimeDiffinSec - 60) - intGaurdTime, intChekInterval, nextEventStartTime = "")
        if intCntr != len(oScheduleList) -1:
            context.reporter.ReportEvent('Test Validation','Wait for ' + str(intGaurdTime) + ' seconds before the Scheduled Event Change', 'DONE')
            time.sleep(intGaurdTime)
        print('Done : ' , datetime.today().strftime("%H:%M:%S" ))'''
