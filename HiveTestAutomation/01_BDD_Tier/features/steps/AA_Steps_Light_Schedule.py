"""
Created on 20 Dec 2016

@author: sri.gunasekaran
modified by Anuj for reset and copy schedule
"""

from datetime import datetime
from datetime import timedelta
from behave import *
import FF_ScheduleUtils as oSchdUtil
import FF_utils as utils


@when(u'The below schedule of {strDeviceType} is set for {strDay}')
def setlightDaySchedule(context, strDeviceType, strDay):
    utils.setClient(context, strDay, True)

    strDay = strDay.split()[0]

    # To identify strDay in terms of actual weekday (eg : sun , mon etc.)
    if strDay.upper() == "TOMMOROW":
        strDay = (datetime.today() + timedelta(days=1)).strftime("%a").lower()
    elif strDay.upper() in oSchdUtil.oWeekDayDict:
        strDay = oSchdUtil.oWeekDayDict[strDay.upper()]
    else:
        strDay = datetime.today().strftime("%a").lower()
    print(strDay)
    oSchedDict = {}
    oSchedDict.clear()
    if 'Start Time' in context.table.headings:
        oSheduleList = oSchdUtil.createLightSceduleFormatFromTable(context)
        if not oSheduleList: return False
        oSchedDict = {strDay: oSheduleList}
    else:
        oSheduleList = oSchdUtil.createLightSceduleFormatFromTableWithoutStartTime(context)
        if not oSheduleList: return False
        oSchedDict = {strDay: oSheduleList}
    context.oSchedDict = oSchedDict

    strDeviceName = context.oLightEP.deviceName

    # Set and report schedule
    context.rFM.setLightSchedule(context, strDeviceName, oSchedDict)


@when(u'The below schedule is reset for active lights on {strDay}')
def resetlightDaySchedule(context, strDay):
    utils.setClient(context, strDay, True)

    strDay = strDay.split()[0]

    # To identify strDay in terms of actual weekday (eg : sun , mon etc.)
    if strDay.upper() == "TOMMOROW":
        strDay = (datetime.today() + timedelta(days=1)).strftime("%a").lower()
    elif strDay.upper() in oSchdUtil.oWeekDayDict:
        strDay = oSchdUtil.oWeekDayDict[strDay.upper()]
    else:
        strDay = datetime.today().strftime("%a").lower()

    print(strDay)
    oSchedDict = {}
    oSchedDict.clear()
    if 'Start Time' in context.table.headings:
        oSheduleList = oSchdUtil.createLightSceduleFormatFromTable(context)
        if not oSheduleList: return False
        oSchedDict = {strDay: oSheduleList}
    else:
        oSheduleList = oSchdUtil.createLightSceduleFormatFromTableWithoutStartTime(context)
        if not oSheduleList: return False
        oSchedDict = {strDay: oSheduleList}
    context.oSchedDict = oSchedDict

    strDeviceName = context.oLightEP.deviceName

    # Set and report schedule
    context.rFM.resetLightSchedule(context, strDeviceName, oSchedDict)


@when(u'Add the below time slot for active light on {strDay} on the Client')
def addlightDaySchedule(context, strDay):
    utils.setClient(context, strDay, True)

    strDay = strDay.split()[0]

    # To identify strDay in terms of actual weekday (eg : sun , mon etc.)
    if strDay.upper() == "TOMMOROW":
        strDay = (datetime.today() + timedelta(days=1)).strftime("%a").lower()
    elif strDay.upper() in oSchdUtil.oWeekDayDict:
        strDay = oSchdUtil.oWeekDayDict[strDay.upper()]
    else:
        strDay = datetime.today().strftime("%a").lower()

    context.strDay = strDay

    print(strDay)
    oSchedDict = {}
    oSchedDict.clear()
    if 'Start Time' in context.table.headings:
        oSheduleList = oSchdUtil.createLightSceduleFormatFromTable(context)
        if not oSheduleList: return False
    else:
        oSheduleList = oSchdUtil.createLightSceduleFormatFromTableWithoutStartTime(context)
        if not oSheduleList: return False
    oSheduleList = oSchdUtil.remove_duplicates(oSheduleList)
    context.oAddSchedule = {strDay: oSheduleList}
    context.addSchedule = oSheduleList
    oSheduleList = oSchdUtil.add_light_time_slot(context)
    oSchedDict = {strDay: oSheduleList}
    context.oSchedDict = oSchedDict

    strDeviceName = context.oLightEP.deviceName

    # Set and report schedule
    context.rFM.addLightSchedule(context, strDeviceName, oSchedDict)


@when('Delete a time slot for active light of {strStartTime} for {strDay}')
def delLightTimeSlotScedule(context, strStartTime, strDay):
    utils.setClient(context, strDay, True)

    strDay = strDay.split()[0]
    if strDay.upper() == "TOMMOROW":
        strDay = (datetime.today() + timedelta(days=1)).strftime("%a").lower()
    elif strDay.upper() in oSchdUtil.oWeekDayDict:
        strDay = oSchdUtil.oWeekDayDict[strDay.upper()]
    else:
        strDay = datetime.today().strftime("%a").lower()

    context.addSlotTime = strStartTime
    context.strDay = strDay
    oSchedDict = {}
    oSchedDict.clear()
    oUpdatedSchedList = oSchdUtil.del_timeslot(context)
    oSchedDict = {strDay: oUpdatedSchedList}
    context.oSchedDict = oSchedDict

    strDeviceName = context.oLightEP.deviceName

    print(context.oSchedDict)
    # Set and report schedule
    context.rFM.delLightSchedule(context, strDeviceName, oSchedDict)


@when('The schedule is copied to {strDay2} from {strDay1} for Active light')
def copyDayScedule(context, strDay2, strDay1):
    utils.setClient(context, strDay1, True)

    strDay1 = strDay1.split()[0]
    # To identify strDay in terms of actual weekday (eg : sun , mon etc.)
    if strDay1.upper() == "TOMMOROW":
        strDay1 = (datetime.today() + timedelta(days=1)).strftime("%a").lower()
    elif strDay1.upper() in oSchdUtil.oWeekDayDict:
        strDay1 = oSchdUtil.oWeekDayDict[strDay1.upper()]
    else:
        strDay1 = datetime.today().strftime("%a").lower()

    # To identify strDay in terms of actual weekday (eg : sun , mon etc.)
    if strDay2.upper() == "TOMMOROW":
        strDay2 = (datetime.now() + timedelta(days=1)).strftime("%a").lower()
    elif strDay2.upper() in oSchdUtil.oWeekDayDict:
        strDay2 = oSchdUtil.oWeekDayDict[strDay2.upper()]
    else:
        strDay2 = datetime.today().strftime("%a").lower()
    oSheduleList = context.oSchedDict.pop(strDay1)

    context.oSchedDict = {strDay2: oSheduleList}
    context.strDay1 = strDay1
    context.strDay2 = strDay2

    strDeviceName = context.oLightEP.deviceName
    # Set and report schedule
    context.rFM.copyLightSchedule(context, strDeviceName, context.oSchedDict)


'''
@when(u'The below schedule of {strNodeType} is set for {strDay1} and copied to {strDay2} on the Client')
def verifyDayCopyandSchedule(context,strNodeType,strDay1,strDay2):
    utils.setClient(context, strDay1, True)

    if strDay.upper() in oSchdUtil.oWeekDayDict:
        strDay = oSchdUtil.oWeekDayDict[strDay.upper()]
    else:
        strDay = datetime.today().strftime("%a").lower()
    print(strDay)
    oSchedDict = {}
    oSchedDict.clear()
    if 'Start Time' in context.table.headings:
        oSheduleList = oSchdUtil.createLightSceduleFormatFromTable(context)
        if oSheduleList == False: return False
        oSchedDict = {strDay: oSheduleList}
    else:
        oSheduleList = oSchdUtil.createLightSceduleFormatFromTableWithoutStartTime(context)
        if oSheduleList == False: return False
        oSchedDict = {strDay: oSheduleList}
    context.oSchedDict = oSchedDict

    context.rFM.setLightSchedule(context, oSchedDict)
    context.rFM.copyLightSchedule(context, strDay1, strDay1)

'''


@then(u'Verify if the {strNodeType} Schedule is set')
def verifyDaySchedule(context, strNodeType):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying if the Schedule is set')
    for oKey in context.oSchedDict.keys():
        if oKey in context.WeeklyScheduleAfter.keys():
            strReportSchedule, boolCompStatus = oSchdUtil.getLightScheduleForReportWithComparison(
                oSchdUtil.remove_duplicates(context.oSchedDict[oKey]),
                oSchdUtil.remove_duplicates(context.WeeklyScheduleAfter[oKey]), oKey)
            context.reporter.ReportEvent('TestValidation', strReportSchedule, boolCompStatus, 'Center')
