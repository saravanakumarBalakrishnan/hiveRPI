from behave import *

import FF_utils as utils

strMainClient = utils.getAttribute('common', 'mainClient')


@given(u'The {deviceName} is paired with the user account')
def validateDevicePaired(context, deviceName):
    context.oThermostatEP = context.oThermostatClass.heatEP
    context.oThermostatEP.update()
    context.reporter.ActionStatus = True
    utils.setClient(context, strMainClient)
    if deviceName != 'Hive Heating':
        context.oThermostatEP.checkDeviceOnDashboard(deviceName)


@when('User navigates to the dashboard screen and long presses on the device cell')
def navigateAndLongPress(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Enable Edit Mode')
    context.oThermostatEP.navigateAndLongPressCell()


@then('Edit mode should be initiated with cell displaying X on it')
def verifyEditMode(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Edit Mode validation')
    context.oThermostatEP.validateEditMode()


@when('user taps on {buttonType} button')
def tapOnButton(context, buttonType):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('User taps on ' + buttonType + ' button')
    context.oThermostatEP.clickButton(buttonType)


@then('User should be able to add the device from list view and save it')
def addDeviceFromListView(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Adding device from list view')
    context.oThermostatEP.addDeviceFromList()


@when('user taps on X of device cell on dashboard screen')
def deleteDevice(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Delete device from dashboard')
    context.oThermostatEP.deleteDeviceFromDashboard()


@then('Device should disappear from the dashboard')
def validateDeviceAvailability(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate device got removed from dashboard')
    context.oThermostatEP.validateDeviceOnDashboard()


@then('{Changes} should be {type} and edit mode should be exited')
def validateChangesAndExit(context, Changes, type):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Exit Edit mode')
    context.oThermostatEP.validateChangesAfterExit(type)


@when('User selects and drags a device to another device {SwapDeviceName} cell')
def dragDeviceToAnotherCell(context, SwapDeviceName):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Swap device positions')
    context.oThermostatEP.swapDevices(SwapDeviceName)
