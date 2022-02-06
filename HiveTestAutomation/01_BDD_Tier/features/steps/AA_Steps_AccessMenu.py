"""
@author: Shubanker
"""

from behave import *

import CC_platformAPI as platAPI
import FF_Platform_Utils as pUtils
import FF_utils as utils

strMainClient = utils.getAttribute('common', 'mainClient')


@given(u'Hive products should be paired to the Hub.')
def setup_menu(context):
    oDeviceVersionList = pUtils.getNodeAndDeviceVersionID()
    print(oDeviceVersionList, "\n")


@when(u'User is in Dashboard screen.')
def verify_dashboardscreen(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the Dashboard screen')
    platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
    platMenu.verifydashboardscreen()


@then(u'calculate the number of devices and check the empty slots if number of devices is less than 7.')
def verify_emptyslots(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the empty slots')
    platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
    platMenu.verifyemptyslots()


@when(u'User clicks the Main Menu icon.')
def click_main_menu_icon(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the main menu Icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.clickmainmenu()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.clickmainmenu()


@then(u'User is able to see the below options.')
def verify_icons(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the main menu options')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.verifymainmenuicons()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.verifymainmenuicons()


@when(u'User clicks the Manage Device icon from the menu list.')
def click_managedevices(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the Manage Devices icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.clickmanagedevices()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.clickmanagedevices()


@then(u'User should be navigated to the Manage Devices Screen.')
def verify_managedevicescreen(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verfying the manage device screen navigation.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.verifymanagedevicescreen()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.verifymanagedevicescreen()


@when(u'User clicks on the install devices icon.')
def click_installdevices(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the install devices icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.clickinstalldevices()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.clickinstalldevices()


@then(u'User should be navigated to the Install Devices screen')
def verify_installdevicescreen(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the install devices navigation.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.verifyinstalldevicescreen()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.verifyinstalldevicescreen()


@then(u'User is able to see the below install options.')
def verify_options_installdevices(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the install devices options.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.verifyoptions_installdevices()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.verifyoptions_installdevices()


@when(u'User clicks on the All Recipes icon.')
def click_allrecipes(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the All Recipes icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.clickallrecipes()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.clickallrecipes()


@then(u'User should be navigated to All Recipes screen.')
def verify_allrecipescreen(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the All Recipes icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.verifyallrecipescreen()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.verifyallrecipescreen()


@when(u'User clicks the Settings icon from main menu page.')
def click_settings(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the Settings icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.clicksettings()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.clicksettings()


@then(u'User is able to see the below sub settings icons.')
def verify_settingsoptions(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the Settings option.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.verifysettingsoptions()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.verifysettingsoptions()


@when(u'User clicks the Help & Support icon from main menu options.')
def click_help(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the Help icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.clickhelp()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.clickhelp()


@then(u'User is able to see the below sub help options.')
def verify_helpoptions(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the Help icons.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.verifyhelpoptions()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.verifyhelpoptions()


@when(u'User clicks on the logout icon.')
def click_logout(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clicking the logout icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.clicklogout()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.clicklogout()


@then(u'User should be logged out and navigated to Login Screen.')
def verify_logout(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying the logout icon.')
    if 'ANDROID' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.AndroidDriver, context.reporter)
        platMenu.verifylogout()
    elif 'IOS' in strMainClient.upper():
        platMenu = platAPI.MainMenu(context.iOSDriver, context.reporter)
        platMenu.verifylogout()
