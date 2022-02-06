"""
Created on 11 August 2016

@authors:
iOS        - rajeshwaran
Android    - Vinod Pasalkar
Web        - TBD
"""

from behave import *
import DD_Page_iOSApp as paygeiOS
import FF_utils as utils

strMainClient = utils.getAttribute('common', 'mainClient')


@given(
    u'The {nameMotionSensor} / {nameContactSensor} / {namePlug} / {nameLight} / {nameHeating} are paired with the hub')
def navToDevices(context, nameMotionSensor, nameContactSensor, namePlug, nameLight, nameHeating):
    oSensorEP = context.oThermostatClass.heatEP
    oSensorEP.reporter = context.reporter
    oSensorEP.iOSDriver = context.iOSDriver
    if strMainClient == 'iOS App':
        oSensorEP.iOSDriver = context.iOSDriver
    elif 'ANDROID' in strMainClient.upper():
        oSensorEP.AndroidDriver = context.AndroidDriver
    elif strMainClient == 'Web App':
        oSensorEP.WebDriver = context.WebDriver
    else:
        print("Problem in getting Main client")
    context.reporter.ActionStatus = True
    context.oThermostatEP = oSensorEP
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Given : The ' + nameMotionSensor + ',' + nameContactSensor + ',' + namePlug + ',' + nameLight + ',' + nameHeating + ' are paired with the hub')
    utils.setClient(context, strMainClient)
    context.oThermostatEP.checkDeviceWithHub(nameMotionSensor)
    context.oThermostatEP.checkDeviceWithHub(nameContactSensor)
    context.oThermostatEP.checkDeviceWithHub(namePlug)
    context.oThermostatEP.checkDeviceWithHub(nameLight)
    # context.oThermostatEP.checkDeviceWithHub(nameHeating)


@given(u'The {nameSensor} and {nameDevice} are paired with the hub')
def CheckDeviceWithHub(context, nameSensor, nameDevice):
    oSensorEP = context.oThermostatClass.heatEP
    oSensorEP.reporter = context.reporter
    oSensorEP.iOSDriver = context.iOSDriver
    if strMainClient == 'iOS App':
        oSensorEP.iOSDriver = context.iOSDriver
    elif 'ANDROID' in strMainClient.upper():
        oSensorEP.AndroidDriver = context.AndroidDriver
    elif strMainClient == 'Web App':
        oSensorEP.WebDriver = context.WebDriver
    else:
        print("Problem in getting Main client")
    context.reporter.ActionStatus = True
    context.oThermostatEP = oSensorEP
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Given : The ' + nameSensor + ',' + nameDevice + ' are paired with the hub')
    utils.setClient(context, strMainClient)
    context.oThermostatEP.checkDeviceWithHub(nameSensor)
    context.oThermostatEP.checkDeviceWithHub(nameDevice)


@when(u'User removes all of the existing Actions')
def removeExistingRecipes(context):
    if strMainClient == 'iOS App':
        oDeviceRecipes = paygeiOS.DeviceRecipes(context.iOSDriver, context.reporter)
        oDeviceRecipes.navigate_to_allrecipes()
        oDeviceRecipes.remove_existing_recipes()
    elif 'ANDROID' in strMainClient.upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('When : User removes all of the existing recipes')
        context.oThermostatEP.removeAllActions()
    elif strMainClient == 'Web App':
        print("Call method for Web")
    else:
        print("Problem in getting Main client")


@when(u'User taps on {strCategory} on Discover Actions')
def navigateToActionsCategory(context, strCategory):
    context.oActions = context.oThermostatClass.ActionsEP
    context.oActions.client = utils.getAttribute('common', 'mainClient')
    context.oActions.updateActions()
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('When : User taps on ' + strCategory + ' on Discover Actions')
    context.oActions.navigateToTemplatesCategory(strCategory)


@then(u'Verify if the Actions template has all available options')
def navToAddaNewRecip(context):
    if strMainClient == 'iOS App':
        oDeviceRecipes = paygeiOS.DeviceRecipes(context.iOSDriver, context.reporter)
        oDeviceRecipes.verify_recipe_template()
    elif 'ANDROID' in strMainClient.upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Then : Verify if the recipe template has all available options')
        context.oThermostatEP.verifyRecipeTemplate()
    elif strMainClient == 'Web App':
        print("Call method for Web")
    else:
        print("Problem in getting Main client")


@when(u'User sets {TypeOf} notification Action for {Sensor} when {SensorState} in app')
def setNewRecipes(context, TypeOf, Sensor, SensorState):
    if strMainClient == 'iOS App':
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'When :User sets ' + TypeOf + ' notification recipe for ' + Sensor + ' when ' + SensorState + ' in app')
        context.oThermostatEP.setNotifyMeRecipe(TypeOf, Sensor, SensorState)
    elif 'ANDROID' in strMainClient.upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'User sets ' + TypeOf + ' notification recipe for  ' + Sensor + ' when ' + SensorState + '  in the Client')
        context.oThermostatEP.setNotifyMeRecipe(TypeOf, Sensor, SensorState)
    elif strMainClient == 'Web App':
        print("Call method for Web")
    else:
        print("Problem in getting Main client")


@when(u'User sets {strDevice} to {strDeviceState} for {strDuration} Action for {strSensor} when {strSensorState}')
def setNewRecipes(context, strDevice, strDeviceState, strDuration, strSensor, strSensorState):
    if strMainClient == 'iOS App':
        print("TBD")
    elif 'ANDROID' in strMainClient.upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'User sets ' + strDevice + ' to ' + strDeviceState + ' for ' + strDuration + ' recipe for ' + strSensor + " " + strSensorState)
        context.oThermostatEP.setOnOffMeRecipe(strDevice, strDeviceState, strDuration, strSensor, strSensorState)
    elif strMainClient == 'Web App':
        print("Call method for Web")
    else:
        print("Problem in getting Main client")


@when(u'User edits {strDevice} to {strDeviceState} for {strDuration} Action for {strSensor} when {strSensorState}')
def setNewRecipes(context, strDevice, strDeviceState, strDuration, strSensor, strSensorState):
    if strMainClient == 'iOS App':
        print("TBD")
    elif 'ANDROID' in strMainClient.upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'User edits ' + strDevice + ' to ' + strDeviceState + ' for ' + strDuration + ' recipe for ' + strSensor + " " + strSensorState)
        context.oThermostatEP.setOnOffMeRecipe(strDevice, strDeviceState, strDuration, strSensor, strSensorState)
    elif strMainClient == 'Web App':
        print("Call method for Web")
    else:
        print("Problem in getting Main client")


@then(u'the {TypeOf} notification Action is displayed for {Sensor} when {SensorState} in the {Location} screen')
def verifySavedRecipe(context, TypeOf, Sensor, SensorState, Location):
    if strMainClient == 'iOS App':
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Then : The ' + TypeOf + ' notification recipe is displayed for ' + Sensor + ' when ' + SensorState + ' in device recipe screen')
        context.oThermostatEP.verifyNotifyMeRecipeDevicePage(TypeOf, Sensor, SensorState, Location)
    elif 'ANDROID' in strMainClient.upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'The ' + TypeOf + ' notification recipe is displayed for ' + Sensor + ' when ' + SensorState + ' in the device recipe screen')
        context.oThermostatEP.verifyNotifyMeRecipeDevicePage(TypeOf, Sensor, SensorState, Location)
    elif strMainClient == 'Web App':
        print("Call method for Web")
    else:
        print("Problem in getting Main client")


@then(u'the action is saved successfully in {strSensor} Actions screen')
def verifySavedRecipe(context, strSensor):
    if strMainClient == 'iOS App':
        print("TBD")
    elif 'ANDROID' in strMainClient.upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'the recipe is saved successfully in ' + strSensor + ' Recipe screen')
        context.oThermostatEP.verifyOnOffRecipeSensorPage(strSensor)
    elif strMainClient == 'Web App':
        print("Call method for Web")
    else:
        print("Problem in getting Main client")


@then(u'the action templates for {Category} are')
def countActionTemplates(context, Category):
    blnSuccess = True
    counter = 0
    context.oActions = context.oThermostatClass.ActionsEP
    blnSuccess, Counter = context.oActions.countActionTemplates(Category)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Then : The action templates for ' + Category + ' are ' + str(Counter))


@then(u'the {templateprice} action templates are')
def countActionTemplates(context, templateprice):
    blnSuccess = True
    counterFree = 0
    counterPaid = 0
    counterBuildYourOwn = 0
    counterWelcomeHome = 0
    context.oActions = context.oThermostatClass.ActionsEP
    blnSuccess, counterFree, counterPaid, counterBuildYourOwn, counterWelcomeHome = context.oActions.countFreeOrPaidActionTemplates(
        templateprice)
    if templateprice == 'free':
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Then : The free action templates are ' + str(counterFree))
    elif templateprice == 'paid':
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Then : The paid action templates are ' + str(counterPaid))
    elif templateprice == 'build your own':
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Then : The build your own action templates are ' + str(counterBuildYourOwn))
    elif templateprice == 'welcome home':
        context.reporter.HTML_TC_BusFlowKeyword_Initialize(
            'Then : The welcome home action templates are ' + str(counterWelcomeHome))
    else:
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('No category provided')


@then(u'The templates for {strCategory} are shown')
def checkCategoryActionTemplates(context, strCategory):
    context.oActions = context.oThermostatClass.ActionsEP
    context.oActions.client = utils.getAttribute('common', 'mainClient')
    context.oActions.updateActions()
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Then : The templates for ' + strCategory + ' are shown')
    context.oActions.verify_action_templates_category(strCategory)
