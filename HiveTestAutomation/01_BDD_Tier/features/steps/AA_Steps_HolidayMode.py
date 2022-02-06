from behave import *


@when(
    'User navigates to {actionType} the Holiday mode with {holidayModeType} duration with target Temperature as {targetTemperature}')
def setHolidayMode(context, actionType, holidayModeType, targetTemperature):
    context.oThermostatEP.navigateToHolidayScreen(context, actionType, holidayModeType)
    context.oThermostatEP.setHolidayMode(context, actionType, holidayModeType, targetTemperature)


@then(
    'The Holiday Mode should be {actionType} for {holidayModeType} duration with target Temperature as {targetTemperature}')
def validateHolidayMode(context, actionType, holidayModeType, targetTemperature):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate Holiday Mode')
    context.oThermostatEP.verifyHolidayMode(context, actionType, holidayModeType, targetTemperature)


@when(
    'User navigates to {actionType} the Holiday mode with {holidayModeType} duration as {daysFromNow} days from now for {duration} days with target Temperature as {targetTemperature}')
def setHolidayMode(context, actionType, holidayModeType, daysFromNow, duration, targetTemperature):
    context.oThermostatEP.navigateToHolidayScreen(context, actionType, holidayModeType)
    context.oThermostatEP.setHolidayMode(context, actionType, holidayModeType, targetTemperature, daysFromNow, duration)
