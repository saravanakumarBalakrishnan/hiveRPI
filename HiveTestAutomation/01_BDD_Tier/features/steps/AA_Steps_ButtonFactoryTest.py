from behave import *
import FF_uartHandler as UAT
import FF_zigbeeToolsConfig as config
import FF_device_utils as dutils
import time


@when(u"the reset command is sent to the device and validated")
def resetDevice(context):
    UAT.startSerialThreads(config.BUTTON_PORT, config.BAUD, True, True, False)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Reset the device')
    respState, respValue, Log = dutils.testMode("RESET")
    if respState:
        context.reporter.ReportEvent("Test Validation", Log, "PASS")
    else:
        context.reporter.ReportEvent("Test Validation", Log, "FAIL")


@Then(u"the test command is sent and validated")
def validateTestMode(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Testing Factory tests commands')
    for oRow in context.table:
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(str(oRow['TestName']).upper() + " Command")
        respState, respValue, Log = dutils.testMode(str(oRow['TestName']).upper())
        if respState:
            context.reporter.ReportEvent("Test Validation", Log, "PASS")
        else:
            context.reporter.ReportEvent("Test Validation", Log, "FAIL")
        if str(oRow['TestName']) == "SLEEP":
            time.sleep(5)
        if str(oRow['TestName']) == "ZIGBEE":
            time.sleep(10)
        if str(oRow['TestName']) == "SWITCH":
            time.sleep(5)
        if str(oRow['TestName']) == "REARBUTTON":
            time.sleep(5)


@Then(u"the test command is sent and validated for the sensor")
def validateTestMode(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Testing Factory tests commands')
    for oRow in context.table:
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(str(oRow['TestName']).upper() + " Command")
        respState, respValue, Log = dutils.testSensorFactoryMode(str(oRow['TestName']).upper())
        if respState:
            context.reporter.ReportEvent("Test Validation", Log, "PASS")
        else:
            context.reporter.ReportEvent("Test Validation", Log, "FAIL")
        if str(oRow['TestName']) == "SLEEP":
            time.sleep(5)
        if str(oRow['TestName']) == "ZIGBEE":
            time.sleep(10)
        if str(oRow['TestName']) == "SWITCH":
            time.sleep(5)
        if str(oRow['TestName']) == "REARBUTTON":
            time.sleep(5)


@When(u'the serial port is connected')
def connectSerialPort(context):
    UAT.startSerialThreads(config.BUTTON_PORT, config.BAUD, True, True, False)
