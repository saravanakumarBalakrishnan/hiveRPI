"""
Created on 06 July 2017

@author: Rajeshwar.Srinivasan
"""

from behave import *

import FF_utils as utils
import FF_alertmeApi as ALAPI


@given(u'Alexa user is setup with Hive devices and {strDeviceType} for {strSkillName} skill validation')
def initSetUp(context, strDeviceType, strSkillName):
    context.oLightClass = context.oThermostatClass

    if strDeviceType == '<Active Heating>':
        context.oThermostatEP = context.oThermostatClass.heatEP
        context.oThermostatEP.update()

    if strDeviceType == '<Active HotWater>':
        context.oThermostatEP = context.oThermostatClass.waterEP
        context.oThermostatEP.update()

    if strDeviceType == '<Active Plug>':
        context.plugEP = context.oThermostatClass.plugEP
        context.plugEP.update()

    if strDeviceType.upper().find('WARM') >= 0:
        context.oLightEP = context.oLightClass.warmWhiteLightEP
        context.oLightEP.update()
    elif strDeviceType.upper().find('TUNEABLE') >= 0:
        context.oLightEP = context.oLightClass.tuneableLightEP
        context.oLightEP.update()
    elif strDeviceType.upper().find('COLOR') >= 0:
        context.oLightEP = context.oLightClass.colourLightEP
        context.oLightEP.update()


@given(u'Rename {strDefaultName} to DeviceName')
def setDeviceName(context, strDefaultName):
    if strDefaultName == '<Active Plug>':
        listPlug = []
        serverName = utils.getAttribute('common', 'currentEnvironment')
        ALAPI.createCredentials(serverName)
        session = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(session)
        for oNode in resp['nodes']:
            if oNode["attributes"] is not None:
                if 'smartplug.json' in oNode["nodeType"]:
                    PlugName = oNode['name']
                    listPlug.append(PlugName)
        if strDefaultName is not None:
            if strDefaultName == '<Active Plug OFF>':
                context.reporter.deviceName = listPlug[1]
            else:
                context.reporter.deviceName = listPlug[0]

    if strDefaultName == '<Active Tuneable Light>':
        context.oLightEP = context.oLightClass.tuneableLightEP
        context.oLightEP.update()
        strDefaultName = context.oLightEP.deviceName
    if strDefaultName == '<Active Colour Light>':
        context.oLightEP = context.oLightClass.colourLightEP
        context.oLightEP.update()
        strDefaultName = context.oLightEP.deviceName
    if strDefaultName == '<Active Warm White Light>':
        # listlight = []
        # serverName = utils.getAttribute('common', 'currentEnvironment')
        # ALAPI.createCredentials(serverName)
        # session = ALAPI.sessionObject()
        # resp = ALAPI.getNodesV6(session)
        # for oNode in resp['nodes']:
        #     if oNode["attributes"] != None:
        #         if oNode["nodeType"] is None:
        #             break
        #         elif 'class.light.json' in oNode["nodeType"]:
        #             lightName = oNode['name']
        #             listlight.append(lightName)
        #             context.reporter.deviceName = listlight[0]
        #             context.oLightEP.deviceName = context.reporter.deviceName
        #             break
        # context.reporter.deviceName = strDefaultName
        strDefaultName = context.oLightEP.deviceName

    if strDefaultName == '<Active Heating>':
        listheat = []
        serverName = utils.getAttribute('common', 'currentEnvironment')
        ALAPI.createCredentials(serverName)
        session = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(session)
        for oNode in resp['nodes']:
            if oNode["attributes"] is not None:
                if 'thermostatui.json' in oNode["nodeType"]:
                    heatName = oNode['name']
                    listheat.append(heatName)
                    context.reporter.deviceName = listheat[0]
                    context.oLightEP.deviceName = context.reporter.deviceName
                    break


@given(u'Rename {strDefaultName} to invalid DeviceName')
def setDeviceName(context, strDefaultName):
    listPlug = []
    serverName = utils.getAttribute('common', 'currentEnvironment')
    ALAPI.createCredentials(serverName)
    session = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        if oNode["attributes"] is not None:
            if 'smartplug.json' in oNode["nodeType"]:
                PlugName = oNode['name']
                listPlug.append(PlugName)

    if strDefaultName is not None:
        if strDefaultName == '<Active Plug OFF>':
            context.reporter.deviceName = 'PlugName'
        else:
            context.reporter.deviceName = 'PlugName'
