"""
Created on 18 Dec 2017

@author: Anuj Kumar
@note: Contact sensor Test case
"""

from behave import *
import DD_Page_AndroidApp as paygeAndroid
import FF_utils as utils

strMainClient = utils.getAttribute('common', 'mainClient')


@given('The Hive products are paired with hub')
def honneycomb_navigation(context):
    print("given is launched")
    oHoneyComb = context.oThermostatClass.heatEP
    oHoneyComb.reporter = context.reporter
    oHoneyComb.iOSDriver = context.iOSDriver
    oHoneyComb.AndroidDriver = context.AndroidDriver
    context.reporter.ActionStatus = True
    context.oThermostatEP = oHoneyComb


@when('Dashboard preview screen is displayed')
def validate_honeycomb(context):
    print("when is launched")
    if strMainClient == 'ANDROID' or strMainClient == 'Android App':
        print("Call method for Android")
        oHoneycomb = paygeAndroid.HoneyComb(context.AndroidDriver, context.reporter)
        oHoneycomb.honeycomb_preview_verify()
    else:
        print("Problem in getting Main client")


@then('Validate user is able to navigate to dashboard page')
def verify_honeycomb(context):
    print("then is launched")

    if strMainClient == 'ANDROID' or strMainClient == 'Android App':
        print("Call method for Android")

        oHoneycomb = paygeAndroid.HoneyComb(context.AndroidDriver, context.reporter)
        oHoneycomb.honeycomb_preview_click()
    else:
        print("Problem in getting Main client")


@Then('Validate status of devices in dashboard')
def validate_honeycomb(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.DashboardFetchVerification(context)


@When('User is on Dashboard screen')
def verify_honeycomb(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.honeycomb_verify(context)


@Then('User is on Dashboard screen')
def verify_honeycomb(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.honeycomb_verify(context)


@Then('Validate the title header of the HoneyComb dashboard screen')
def verify_honeycomb_title(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.honeycomb_verifyTitle(context)


@Then('Validate the hierarchy of the HoneyComb dashboard screen')
def verify_honeycomb_hierachy(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.honeycomb_verifyHierarchy(context)


@When('User is on Device list screen')
def navigate_DeviceListScreen(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.devicelist_verify()


@Then('Validate the Status of devices in Device List screen')
def validate_devicelistStatus(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.DeviceListFetchVerification(context)


@Then('Validate the title header of Device List screen')
def verify_deviceList_title(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.honeycomb_verifyTitle(context)


@Then('Validate the Hierarchy of Device List screen')
def verify_deviceList_hierachy(context):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.deviceList_verifyHierarchy(context)


@When(u'User navigates to {strScreenName} screen and Validates the presence and click on the honeycomb icon')
def navigateTo_Screen(context, strScreenName):
    utils.setClient(context, strMainClient)
    context.oThermostatEP.navigationTo_screen(context, strScreenName)
