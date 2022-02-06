from http.cookiejar import offset_from_tz_string

import remi.gui as gui
from remi import start, App
import threading
from remi.gui import *
import sys
sys.path.append("01_BDD_Tier/features/steps")
sys.path.append("01_BDD_Tier/features/steps/Constants")
sys.path.append("01_BDD_Tier/features/steps/Thermostat_Screen_Text")
sys.path.append("01_BDD_Tier/features/steps/Function_Libraries")
sys.path.append("01_BDD_Tier/features/steps/Handlers")
from remi import start, App
import FF_device_utils as dUtils
import os
import platform
import subprocess
import FF_threadedSerial as AT
import re
import operator
from threading import Thread as start_new_thread
import FF_utils as utils
import FF_zigbeeToolsConfig as config
import sys
import time
import json
import FF_zigbeeClusters as zcl
import FF_alertmeApi as apiUtils
import requests
from collections import OrderedDict
import GG_ExceptionHandler as Exceptionclass
import socket


global oStore

class variables:
    def __init__(self):
        self.p = None
        self.oThread = None
        self.flag = None
        self.OS = self.osName()
        self.sessionName = ""
        self.classObject = None
        self.screenObject = None
        self.listOption = ['ATI', 'AT+DASSL', 'AT+EN', 'REMOVE', 'AT+PJOIN', 'AT+JN', 'AT+READ', 'AT+BIND', 'AT+UNBIND',
                      'AT+BTABLE', 'AT+WRITE', 'AT+NTABLE'
            , 'GET REPORTING', 'SET REPORTING', 'SET REPORTING ON CHANGE', 'ON', 'OFF', 'AT+LCMTOLEV', 'AT+CCMVTOCT',
                      'AT+CCMVTOHUS']

        self.consoleContainer = gui.Container(width='100%')
        self.consoleContainer.style['background-color'] = 'transparent'
        self.subContainerRight = gui.Container(width='70%')
        self.subContainerLeft = gui.Container(width=320)
        self.consoleText = gui.TextInput(width='100%', height=1000)
        self.consoleText.style['overflow'] = "auto"
        self.consoleText.set_on_change_listener(focusToBottom)
        self.dtextinput = gui.TextInput(width='100%')
        self.DevDetailsContainer = gui.Container(width='30%')
        self.TopDetailsContainer = gui.Container(width='30%')
        self.subContainerDevicesInner = gui.Container(width='100%')
        self.subContainerDevicesInner.style["border-style"] = 'ridge'
        self.subContainerDevicesInnerConsole = gui.Container(width='80%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        self.subContainerDevicesInnerConsole.style["overflow"]="scroll"
        self.subContainerDevicesInnerConsole.style["height"]="500px"
        self.subContainerDevicesInnerConsole.style["vertical-align"]="bottom"
        self.subContainerDevicesInnerConsole.style["border-style"] = 'ridge'
        self.firmwareContainer = gui.Container(width='40%')
        self.firmwareContainer.add_class("panel panel-default")
        self.upgradeVersion = gui.TextInput(width='100px')
        self.upgradeVersion.add_class("form-control input-lg")
        self.DowngradeVersion = gui.TextInput(width='100px')
        self.DowngradeVersion.add_class("form-control input-lg")
        self.listDetailsContainer = gui.Container(width='40%')
        self.listDetailsContainer.add_class("panel panel-default")
        self.listDetails = gui.ListView(True,width="70%")
        self.upContainer = gui.Container(width='100%')
        self.downContainer = gui.Container(width='100%')
        self.changeFirmware = gui.Button("Replace firmware", width='70%')
        self.changeFirmware.add_class("btn-primary")
        self.verifyTGStick = gui.Button("Verify Devices Connected", width=250, height=30, margin='10px')
        self.verifyTGStick.add_class("btn-success")
        self.subContainerDevices = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL,
                                         margin='0px')
        self.subContainerDevicesLive = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL,
                                              margin='0px')
        self.btnFirmwareZDump = gui.Button("Start", width='20%')
        self.btnFirmwareZDump.add_class("btn-success")
        self.btnFirmwareZDump.set_on_click_listener(deviceZigbeeDump)
        self.txtFirmwarePath = gui.TextInput(True, width='70%')
        self.txtFirmwarePath.add_class("form-control input-lg")
        self.btnChangeFirmwareOTA = gui.Button("Browse", width='20%')
        self.btnChangeFirmwareOTA.add_class("btn-primary")
        self.btnChangeFirmwareOTA.set_on_click_listener(changeFirmwarePathOTA)
        self.fileselectionDialogOTA = None
        self.lblFirmwareOTA = gui.Label("Firmware Path", width='10%')
        self.txtFirmwarePath = gui.TextInput(True, width='100%')
        self.txtFirmwarePath.add_class("form-control input-lg")
        self.btnFirmwareOTA = gui.Button("Start", width='30%')
        self.btnFirmwareOTA.add_class("btn-success")
        self.btnFirmwareOTA.set_on_click_listener(FirmwareOTA)
        self.drpValidation = gui.DropDown(width='70%')

        self.lblFirmware = gui.Label("Firmware Path", width='10%')
        self.txtFirmware = gui.TextInput(True, width='70%')
        self.txtFirmware.add_class("form-control input-lg")
        self.lblValidation = gui.Label("Validation Type", width='25%')
        self.drpValidation = gui.DropDown(width='75%')
        self.drpValidation.append("Zigbee API")
        self.drpValidation.add_class("form-control dropdown")
        self.drpValidation.append("Platform API")
        self.drpValidation.append("Factory API")


        self.btnChangeFirmware = gui.Button("Change Path", width='20%')
        self.btnChangeFirmware.add_class("btn-primary")
        self.btnChangeFirmware.set_on_click_listener(changeFirmwarePath)
        self.subConfig = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px')
        self.subConfig.append(self.lblFirmware)
        self.subConfig.append(self.txtFirmware)
        self.subConfig.append(self.btnChangeFirmware)
        self.subConfig.append(self.lblValidation)
        self.subConfig.append(self.drpValidation)
        self.subConfigTop = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px')
        self.btnSave = gui.Button("Save", width='100px')
        self.btnSave.add_class("btn-primary")
        self.btnSave.set_on_click_listener(saveConfig)
        self.subConfigTop.append(self.btnSave)
        # self.configDialog.append(self.subConfigTop)
        # self.configDialog.add_field_with_label('firmwareFolderPath', 'Firmware Path', self.txtFirmware)
        self.subContainerConfig = gui.Container(width='100%')
        self.subContainerConfigLibraries = gui.Container(width='80%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL,
                                                      margin='10px')
        self.subContainerConfigLibraries.style['display'] = 'block'
        self.subContainerConfigLibraries.style['overflow'] = 'auto'
        self.subContainerConfigLibrariesList = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL,
                                                          margin='10px')
        self.txtInstalled = gui.Label("Installed Libraries", width='20%')
        self.txtUnInstalled = gui.Label("Missing Libraries", width='20%')
        self.txtInstallConsole = gui.Label("Console", width='60%')
        self.subContainerConfigLibrariesList.append(self.txtInstalled)
        self.subContainerConfigLibrariesList.append(self.txtUnInstalled)
        self.subContainerConfigLibrariesList.append(self.txtInstallConsole)
        self.btnInstall = gui.Button("Check / Fix Libraries")
        self.btnInstall.add_class("btn-primary")
        self.btnInstall.set_on_click_listener(installLibraries)
        self.listInstalled = gui.ListView(True, width='20%')
        self.listInstalled.add_class("list-group")
        self.listInstalled.append("List of Libraries")
        self.listInstalled.style['background-color'] = 'rgb(107, 201, 78)'
        self.subContainerConfigLibrariesList.append(self.listInstalled)
        self.listNotInstalled = gui.ListView(True, width='20%')
        self.listNotInstalled.add_class("list-group")
        self.listNotInstalled.append("List of Libraries")
        self.listNotInstalled.style['background-color'] = 'rgb(209, 50, 50)'
        self.subContainerConfigLibrariesList.append(self.listNotInstalled)
        self.subContainerConfigLibrariesConsole = gui.Container(width='60%')
        self.subContainerConfigLibrariesConsole.style['background-color'] = 'rgb(211, 211, 211)'
        self.subContainerConfigLibrariesList.append(self.subContainerConfigLibrariesConsole)
        self.subContainerConfigLibraries.append(self.subConfigTop)
        self.subContainerConfigLibraries.append(self.btnInstall)
        self.subContainerConfigLibraries.append(self.subContainerConfigLibrariesList)
        self.subContainerConfig.append(self.subContainerConfigLibraries)
        self.listClusterContainer = gui.Container(width='30%')
        self.listAttrContainer = gui.Container(width='70%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        self.subContainerVerticalLive = gui.Container(width='15%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL,)
        #self.subContainerVerticalLive.style['bottom'] = "0"
        self.btnFirmwareLive = gui.Button("Start", width='20%')
        self.btnFirmwareLive.add_class("btn-success")
        self.btnFirmwareLive.set_on_click_listener(live)

        self.lbl1 = gui.Label("Min Report(hex)")
        self.txtMinRepo = gui.TextInput(True)
        self.txtMinRepo.add_class("form-control input-lg")
        self.lbl2 = gui.Label("Min Report(hex)")
        self.txtMaxRepo = gui.TextInput(True)
        self.txtMaxRepo.add_class("form-control input-lg")
        self.lbl3 = gui.Label("Write Value")
        self.txtWriteVal = gui.TextInput(True)
        self.txtWriteVal.add_class("form-control input-lg")
        self.listAttrContainerRepoLive = gui.Container(width='40%')
        self.listAttrContainerRepoLive.append(self.lbl1)
        self.listAttrContainerRepoLive.append(self.txtMinRepo)
        self.listAttrContainerRepoLive.append(self.lbl2)
        self.listAttrContainerRepoLive.append(self.txtMaxRepo)
        self.listAttrContainerRepoLive.append(self.lbl3)
        self.listAttrContainerRepoLive.append(self.txtWriteVal)
        self.txtFocus = gui.TextInput(True, width='65%',id="focus")
        self.txtFocus.add_class("form-control input-lg")
        self.btnSend = gui.Button("Send", width='15%')
        self.btnSend.add_class("btn-success")
        self.btnSend.set_on_click_listener(sendCommand)
        self.otaLog = gui.Container(width="100%",height="200px")
        self.results = gui.Container(width="100%",height="200px")
        self.otaLog.style["overflow"] = "scroll"
        self.ipAddr = self.getIp()

    def osName(self):
        if 'DARWIN' in platform.system().upper():
            OS = "MAC"
        elif 'LINUX' in platform.system().upper():
            OS = "LINUX"
        elif sys.platform.startswith('win'):
            OS = "WINDOWS"
        return OS

    def getIp(self):
        cmd = 'ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2'
        if "WINDOWS" in sys.platform.upper():
            cmd = 'ipconfig | find "IPv4" & hostname'
        if "LINUX" in sys.platform.upper():
            cmd = "ifconfig en0 | grep 'inet ' | awk '{ print $2 }'"

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        tempInner, temp = '', ''
        while True:
            out = p.stdout.read(1)
            if out == '' and p.poll() != None:
                print("hi=" + tempInner)
                break
            if out != '':
                sys.stdout.write(out.decode('latin1'))
                if '\n' in tempInner:
                    print(tempInner)
                    break
                temp = temp + out.decode('latin1')
                tempInner = tempInner + out.decode('latin1')
                sys.stdout.flush()
        value = "" + tempInner
        value = value.strip()
        if "WINDOWS" in sys.platform.upper():
            value = value.split("IPv4 Address. . . . . . . . . . . : ")[1].strip()
        print("value=" + value)
        return value

def sendCommand(widget):
    AT.sendCommand(oStore.txtFocus.get_text(),['OK'],1)

def live(widget):
    if len(oStore.DevDetailsContainer.children) == 0:
        oStore.dtextinput.set_value("Error : Click on Get Devices Connected to continue")
        oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
        return
    try:
        if oStore.DevDetailsContainer.children[
                list(oStore.DevDetailsContainer.children.keys())[0]]._selected_item is None:
            oStore.dtextinput.set_value("Error : Click on Get Devices Connected to continue")
            oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
            return
    except:
        if oStore.DevDetailsContainer.children[
            list(oStore.DevDetailsContainer.children.keys())[1]]._selected_item is None:
            oStore.dtextinput.set_value("Error : Click on Get Devices Connected to continue")
            oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
            return
    if 'Stop' in oStore.btnFirmwareLive.get_text():
        AT.stopThreads()
        oStore.btnFirmwareLive.set_text("Start")
        return
    MacAddress = ""
    for i in range(0, 4):
        temp = oStore.listDetails.children[list(oStore.listDetails.children)[i]].children['text'].replace("\'",
                                                                                                            "").replace(
            "[",
            "").replace(
            "]", "").split(",")[0]
        if len(temp) == 16 and "[" not in temp:
            MacAddress = temp
    node = dUtils.getDeviceIdWithMAC(MacAddress)
    nodes = dUtils.getDeviceNode(node)
    nodeid = nodes['nodeID']
    if len(list(nodes['endPoints'])) > 0:
        ep = str(list(nodes['endPoints'])[0])
    zbtype = nodes['type']

    try:
        try:
            if oStore.p:
                oStore.p.terminate()
                oStore.p.kill()
        except Exception as e:
            if "[Errno 3] No such process" in str(e):
                pass
            else:
                raise Exceptionclass.ExceptionHandling(str(e))
    except Exception as e:
        raise Exceptionclass.ExceptionHandling(str(e))
    try:
        oStore.consoleContainer.empty()
        #oStore.consoleContainer.append(gui.Label('<div id="div1" style="overflow:scroll; height:400px;">'))
        AT.startSerialThreads(config.PORT,config.BAUD,True,True,False)
        oStore.btnFirmwareLive.set_text("Stop")
        lbl = gui.Label("Start")
        oStore.consoleContainer.append(lbl)
        oStore.subContainerDevicesInnerConsole.append(oStore.txtFocus)
        oStore.subContainerDevicesInnerConsole.append(oStore.btnSend)
        AT.UIObj = oStore
        AT.UIgui = gui
        AT.MyApp = MyApp
        AT.debug = True
    except Exception as e:
        AT.stopThreads()
        raise Exceptionclass.ExceptionHandling(str(e))

def changeFirmwarePath( widget):
    if os.path.exists(getFirmwarePath(oStore.OS)):
        oStore.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', True,
                                                             getFirmwarePath(oStore.OS), False,
                                                           allow_folder_selection=True)
    else:
        oStore.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', True,
                                                           os.path.abspath(os.path.curdir), False,
                                                           allow_folder_selection=True)
    oStore.fileselectionDialog.set_on_confirm_value_listener(
        on_fileselection_dialog_confirm)

    # here is returned the Input Dialog widget, and it will be shown
    oStore.fileselectionDialog.show(oStore.classObject)

def on_fileselection_dialog_confirm( widget, filelist):
    # a list() of filenames and folders is returned
    oStore.txtFirmware.set_text(dict(widget.fileFolderNavigator.pathEditor.children)["text"])

def installLibraries(widget):
    try:
        if oStore.p:
            oStore.p.terminate()
            oStore.p.kill()
    except Exception as e:
        if "[Errno 3] No such process" in str(e):
            pass
        else:
            raise Exceptionclass.ExceptionHandling(str(e))
    #killBatch()
    oStore.oThread = start_new_thread(target=installLib)
    oStore.flag = False
    oStore.oThread.setDaemon(True)
    oStore.oThread.start()

def installLib():
    oStore.subContainerConfigLibrariesConsole.empty()
    oStore.subContainerConfigLibrariesConsole.redraw()
    oStore.listInstalled.empty()
    oStore.listNotInstalled.empty()
    oStore.listNotInstalled.append("List of Libraries", "Header")
    listLib = []
    listLibraries = ['Behave', 'Redis', 'pyserial', 'tqdm', 'ipdb', 'appium-python-client', 'selenium', 'tqdm',
                     'selenium', 'requests', 'pytesseract', 'pillow', 'numpy', 'speechrecognition', 'pysmbus']
    oFileName = "Installation_MAC.command"
    if "WINDOWS" in oStore.OS:
        oFileName = "Installation_WIN.bat"
    if "LINUX" in oStore.OS:
        oFileName = "Installation_MAC.sh"
    for root, dirs, files in os.walk(
            os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
        for file in files:

            if file.endswith(oFileName):
                if "WINDOWS" in oStore.OS:
                    oStore.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                              stdout=subprocess.PIPE)
                elif "LINUX" in oStore.OS:
                    oStore.p = subprocess.Popen(root + '/./' + oFileName, shell=True,
                                              stdout=subprocess.PIPE)
                else:
                    oStore.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                              stdout=subprocess.PIPE)
                temp = ''
                tempInner = ''
                while True:
                    if oStore.flag:
                        print("\nstopped by API\n")
                        oStore.flag = False
                        break
                    out = oStore.p.stdout.read(1)
                    if str(out) == 'b\'\'' and oStore.p.poll() != None:
                        break
                    if out != '':
                        sys.stdout.write(out.decode('latin1'))
                        # oStore.consoleText.set_text(temp)
                        if '\n' in tempInner:
                            lbl = gui.Label(tempInner, width='100%')
                            if (
                                    "Requirement already satisfied: behave" in tempInner or "Successfully installed behave" in tempInner):
                                listLib.append("Behave")
                                oStore.listInstalled.append("Behave")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: redis" in tempInner or "Successfully installed redis" in tempInner):
                                listLib.append("Redis")
                                oStore.listInstalled.append("Redis")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: pyserial" in tempInner or "Successfully installed pyserial" in tempInner):
                                listLib.append("pyserial")
                                oStore.listInstalled.append("pyserial")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: tqdm" in tempInner or "Successfully installed tqdm" in tempInner):
                                listLib.append("tqdm")
                                oStore.listInstalled.append("tqdm")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: ipdb" in tempInner or "Successfully installed ipdb" in tempInner):
                                listLib.append("ipdb")
                                oStore.listInstalled.append("ipdb")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: appium-python-client" in tempInner or "Successfully installed appium-python-client" in tempInner):
                                listLib.append("appium-python-client")
                                oStore.listInstalled.append("appium-python-client")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: selenium" in tempInner or "Successfully installed selenium" in tempInner):
                                listLib.append("selenium")
                                oStore.listInstalled.append("selenium")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: requests" in tempInner or "Successfully installed requests" in tempInner):
                                listLib.append("tqdm")
                                oStore.listInstalled.append("tqdm")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: nmap" in tempInner or "Successfully installed nmap" in tempInner):
                                listLib.append("requests")
                                oStore.listInstalled.append("requests")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: pytesseract" in tempInner or "Successfully installed pytesseract" in tempInner):
                                listLib.append("pytesseract")
                                oStore.listInstalled.append("pytesseract")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: pillow" in tempInner or "Successfully installed pillow" in tempInner):
                                listLib.append("pillow")
                                oStore.listInstalled.append("pillow")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: numpy" in tempInner or "Successfully installed numpy" in tempInner):
                                listLib.append("numpy")
                                oStore.listInstalled.append("numpy")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: speechrecognition" in tempInner or "Successfully installed speechrecognition" in tempInner):
                                listLib.append("speechrecognition")
                                oStore.listInstalled.append("speechrecognition")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                    "Requirement already satisfied: pysmbus" in tempInner or "Successfully installed pysmbus" in tempInner):
                                listLib.append("pysmbus")
                                oStore.listInstalled.append("pysmbus")
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            if (
                                                "ERROR" in tempInner.upper() or "NACK" in tempInner.upper() or "**** PROBLEM" in tempInner.upper()):
                                lbl.style['color'] = 'rgb(99, 7, 7)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            oStore.subContainerConfigLibrariesConsole.append(lbl)
                            oStore.subContainerConfigLibrariesConsole.redraw()
                            tempInner = ''
                        temp = temp + out.decode('latin1')
                        tempInner = tempInner + out.decode('latin1')
                        if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                            oStore.p.kill()
                            break
                        sys.stdout.flush()
                listNotInstalled = []
                listNotInstalled = [elem for elem in listLibraries if elem not in listLib]
                for e in listNotInstalled:
                    oStore.listNotInstalled.append(e)
                if len(listNotInstalled) < 1:
                    oStore.listNotInstalled.append("No missing Libraries", "Header")
                oStore.listNotInstalled.redraw()
                oStore.listInstalled.redraw()
                oStore.subContainerConfigLibrariesList.redraw()
                oStore.subContainerConfigLibrariesConsole.redraw()
                print("\ncompleted\n")
                break
                # self.listInstalled.new_from_list(listLib)

def saveConfig(widget):
    for root, dirs, files in os.walk(
            os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
        for file in files:
            if file.endswith('FF_zigbeeToolsConfig.py'):
                with open(root + "/" + file) as f:
                    lines = f.readlines()
                with open(root + "/" + file, 'w') as f:
                    f.seek(0)
                    f.truncate()
                    intCounter = 0
                    for line in lines:
                        if "FIRMWARE_ROOT_FILE_PATH = " in line:
                            if oStore.txtFirmware.get_text().endswith("/\n"):
                                line = "FIRMWARE_ROOT_FILE_PATH = '" + oStore.txtFirmware.get_text().replace("/\n",
                                                                                                           "") + "/'\n"
                            else:
                                line = "FIRMWARE_ROOT_FILE_PATH = '" + oStore.txtFirmware.get_text().replace("\n",
                                                                                                           "") + "/'\n"
                            lines[intCounter] = line
                        intCounter = intCounter + 1
                    f.writelines(lines)
                    f.close()
    utils.setAttribute('common', 'apiValidationType', oStore.drpValidation.get_value())

def deviceZigbeeDump(widget):
    try:
        MacAddress = ""
        for i in range(0, 4):
            temp = oStore.listDetails.children[list(oStore.listDetails.children)[i]].children['text'].replace("\'",
                                                                                                                "").replace(
                "[",
                "").replace(
                "]", "").split(",")[0]
            if len(temp) == 16 and "[" not in temp:
                MacAddress = temp
            # nodeid = dUtils.getModelIdWithMAC(MacAddress)
        node = dUtils.getDeviceIdWithMAC(MacAddress)
        nodes = dUtils.getDeviceNode(node)
        nodeid = nodes['nodeID']
        ep = str(list(nodes['endPoints'])[0])
        zbtype = nodes['type']
        for root, dirs, files in os.walk(
                os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
            for file in files:
                if file.endswith('FF_zigbeeToolsConfig.py'):
                    with open(root + "/" + file,'r') as f:
                        lines = f.readlines()
                    with open(root + "/" + file, 'w') as f:
                        f.seek(0)
                        f.truncate()
                        intCounter = 0
                        for bline in lines:
                            line = bline
                            if "NODE_ID = " in line:
                                line = "NODE_ID = '" + nodeid + "'\n"
                                lines[intCounter] = line
                            if "EP_ID = " in line:
                                line = "EP_ID = '" + ep + "'\n"
                                lines[intCounter] = line
                            intCounter = intCounter + 1
                        f.writelines(lines)
                        f.close()
        os.walk(
            os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0])
    except Exception as e:
        #raise Exceptionclass.ExceptionHandling(str(e))
        if "AttributeError: 'MyApp' object has no attribute 'listDetailsZDump'" in str(e):
            oStore.dtextinput.set_value("Please select the device")
            oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
        elif "list index out of range" in str(e):
            oStore.dtextinput.set_value("Please select the correct device")
            oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
            raise Exceptionclass.ExceptionHandling(str(e))
        else:
            raise Exceptionclass.ExceptionHandling(str(e))

    try:
        try:
            if oStore.p:
                oStore.p.terminate()
                oStore.p.kill()
        except Exception as e:
            if "[Errno 3] No such process" in str(e):
                pass
            else:
                raise Exceptionclass.ExceptionHandling(str(e))
        #killBatch()
        oStore.oThread = start_new_thread(target=ZDump)
        oStore.flag = False
        oStore.oThread.setDaemon(True)
        oStore.oThread.start()
    except Exception as e:
        raise Exceptionclass.ExceptionHandling(str(e))

def ZDump():
    try:
        for i in range(0, 4):
            temp = oStore.listDetails.children[list(oStore.listDetails.children)[i]].children['text'].replace("\'",
                                                                                                                "").replace(
                "[",
                "").replace(
                "]", "").split(",")[0]
            if len(temp) == 16 and "[" not in temp:
                MacAddress = temp
    except Exception as e:
        oStore.dtextinput.set_value("Please select the device")
        oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
        raise Exceptionclass.ExceptionHandling(str(e))
    oStore.dtextinput.set_value("Please Wait ...")
    oStore.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
    oStore.subContainerDevicesInnerConsole.empty()
    oStore.subContainerDevicesInnerConsole.redraw()
    oStore.subContainerDevicesInner.empty()
    oStore.subContainerDevicesInner.redraw()
    HeadLable = gui.Label("Console",width='100%')
    HeadLable.style['font-size'] = '20px'
    HeadLable.add_class("label label-primary")
    oStore.subContainerDevicesInnerConsole.append(HeadLable)
    oStore.subContainerDevicesInnerConsole.append(gui.Label("<br>"))
    oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
    act = 0
    oFileName = "zDump.command"
    if "WINDOWS" in oStore.OS:
        oFileName = "zDump.bat"
    if "LINUX" in oStore.OS:
        oFileName = "zDump.sh"

    intCtr = 0
    lst = []
    for root, dirs, files in os.walk(
            os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
        for file in files:

            if file.endswith(oFileName):
                try:
                    if "WINDOWS" in oStore.OS:
                        oStore.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    else:
                        oStore.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    temp = ''
                    tempInner = ''
                    tempInnerGroup = ''
                    flag = False
                    while True:
                        if oStore.flag:
                            print("\nstopped by API\n")
                            oStore.flag = False
                            break
                        out = oStore.p.stdout.read(1)
                        if str(out) == 'b\'\'' and oStore.p.poll() != None:
                            table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                            table.add_class("table table-hover")
                            oStore.subContainerDevicesInner.append(table)
                            break
                        if out != '':
                            sys.stdout.write(out.decode('latin1'))
                            # self.consoleText.set_text(temp)
                            if '\n' in tempInner:
                                if 'Cluster' in tempInner and 'InCluster' not in tempInner:
                                    flag = True
                                if flag:
                                    if 'Endpoint=' in tempInner and ', Endpoint=' not in tempInner:
                                        if len(lst) > 0:
                                            if len(lst) == 1:
                                                if any("Attribute Id" not in s for s in lst):
                                                    table = gui.Table.new_from_list(lst, width='100%',
                                                                                         margin='10px')
                                                    table.add_class("table table-hover")
                                                    oStore.subContainerDevicesInner.append(table)
                                            else:

                                                table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                                table.style['background-color'] = 'rgb(91,91,91)'
                                                table.add_class("table table-hover")
                                                oStore.subContainerDevicesInner.append(table)
                                        lst = []
                                        lst.append([tempInner.split(',')[0], tempInner.split(',')[1],
                                                    tempInner.split(',')[2], tempInner.split(',')[3]])

                                        table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                        table.add_class("table table-hover")
                                        oStore.subContainerDevicesInner.append(table)
                                        lst = []

                                    else:

                                        if len(lst) == 0:
                                            if ',' in tempInner:
                                                lst.append(['Attribute Id', 'Attribute Type', 'Attribute Name',
                                                            'Attribute Value','Data Type', 'Reporting configuration'])
                                        if len(tempInner.split(',')) == 5:
                                            lst.append([tempInner.split(',')[0],tempInner.split(',')[1],tempInner.split(',')[2],tempInner.split(',')[3],tempInner.split(',')[4]])
                                        if len(tempInner.split(',')) > 5:
                                            strRem = ""
                                            for i in range(5,len(tempInner.split(','))):
                                                strRem = strRem + tempInner.split(',')[i]
                                            lst.append([tempInner.split(',')[0], tempInner.split(',')[1],
                                                        tempInner.split(',')[2], tempInner.split(',')[3], tempInner.split(',')[4],strRem])
                                lbl = gui.Label(tempInner, width='100%')
                                lbl.style['font-size'] = '10px'
                                oStore.subContainerDevicesInnerConsole.append(lbl)
                                tempInner = ''
                            temp = temp + out.decode('latin1')
                            tempInner = tempInner + out.decode('latin1')
                            if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp or "TIMEOUT: sendCommand() timeout" in temp:
                                oStore.p.kill()
                                table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                table.add_class("table table-hover")
                                oStore.subContainerDevicesInner.append(table)
                                if "Took" not in temp:
                                    oStore.dtextinput.set_value(temp)
                                    oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
                                break
                            sys.stdout.flush()

                    print("\ncompleted\n")
                    oStore.dtextinput.set_value("Completed")
                    oStore.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                    break
                except Exception as e:
                    killBatch()
                    raise Exceptionclass.ExceptionHandling(str(e))

def ReadFeatureFile( horizontalContainer, RPI=None):
    # print("path = " +str(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]))
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                         0] + "/01_BDD_Tier/features/"):
        # print("path" + str(root))


        for file in files:
            if file.endswith(".feature"):
                btn = gui.Button(file, width=250, height=30, margin='10px')
                btn.add_class("btn-success")
                if RPI is None:
                    btn.set_on_click_listener(on_button_pressed)
                    horizontalContainer.append(btn)
                else:
                    btn.set_on_click_listener(on_button_pressed)
                    horizontalContainer.append(btn)

def on_button_pressed(widget):
    oStore.subContainerRight.empty()
    oStore.subContainerRight.redraw()
    btn = gui.Button("Edit " + widget.get_text(), width=350, height=30, margin='10px')
    btn.add_class("btn-warning")
    btn.set_on_click_listener(on_EditTest)
    oStore.subContainerRight.append(btn)
    btn = gui.Button("Refresh " + widget.get_text(), width=350, height=30, margin='10px')
    btn.add_class("btn-info")
    btn.set_on_click_listener(on_RefreshTest)
    oStore.subContainerRight.append(btn)
    BreakLable = gui.Label("<BR><BR><BR>")
    oStore.subContainerRight.append(BreakLable)
    oStore.subContainerRight.append(gui.Label(widget.get_text()))
    for root, dirs, files in os.walk(
                    os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                        0] + "/01_BDD_Tier/features/"):
        TableList = []
        for file in files:
            if file.endswith(widget.get_text()):
                with open(root + "/" + file) as f:
                    lines = f.readlines()
                Tableflag = False
                continueFlag = False
                counter = 0
                TableList = []
                for line in lines:
                    if "@" in line:
                        oStore.subContainerRight.append(gui.Label("<BR><BR>"))
                        oStore.subContainerRight.append(gui.Label("<hr>"))
                        oStore.subContainerRight.append(gui.Label("<BR>"))
                        for tag in line.split("@"):
                            tag = str(tag).replace('  ', '')
                            if str(tag).strip() != "" and str(tag).strip() != "#":
                                btn = gui.Button(tag, width=250, height=30, margin='10px')
                                btn.add_class("btn-danger   ")
                                btn.set_on_click_listener(on_runTest)
                                oStore.subContainerRight.append(btn)
                    elif "|" in line:

                        if not Tableflag:
                            if not continueFlag:
                                oStore.subContainerRight.append(gui.Label("<BR><BR>"))
                                # for col in line.split("|"):
                                #    if str(col).strip() != "":
                                #        print("hi")
                                TableList.append(line.split("|"))
                                continueFlag = True
                                Tableflag = True
                                counter = counter + 1
                        else:
                            # for row in line.split("|"):
                            #    if str(row).strip() != "":
                            #        print("hi")
                            TableList.append(line.split("|"))

                            counter = counter + 1
                    else:
                        if len(TableList) > 0:
                            tbl = gui.Table.new_from_list(TableList, width='100%')
                            tbl.add_class("table table-hover")
                            oStore.subContainerRight.append(tbl)
                            Tableflag = False
                            continueFlag = False
                            counter = 0
                            TableList.clear()
                        txt = gui.Label(line, width='100%')
                        subTxt = gui.Container(width='100%')
                        if ("#" in line):
                            subTxt.style['color'] = 'rgb(32, 94, 15)'
                            subTxt.style['font-size'] = '10px'
                        if ("Feature" in line):
                            subTxt.style['color'] = 'rgb(130, 9, 9)'
                            # subTxt.style['font-weight'] = '100'
                        if ("Scenario" in line):
                            subTxt.style['font-size'] = '16px'
                            subTxt.style['color'] = 'rgb(193, 81, 1)'
                            # subTxt.style['font-weight'] = '100'
                        if ("Given" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                        if ("When" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                        if ("Then" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                        if ("And" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                        if ("Examples:" in line):
                            oStore.subContainerRight.append(gui.Label("<BR>"))
                        subTxt.append(txt)
                        oStore.subContainerRight.append(subTxt)
        if len(TableList) > 0:
            tbl = gui.Table.new_from_list(TableList, width='100%')
            tbl.add_class("table table-hover")
            oStore.subContainerRight.append(tbl)
            TableList.clear()
    oStore.consoleText.add_class("form-control input-lg")
    oStore.consoleText.style['background-color'] = 'black'
    oStore.subContainerRight.append(oStore.consoleContainer)
    oStore.subContainerRight.append(oStore.consoleText)

def on_EditTest(widget):
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                         0] + "/01_BDD_Tier/features/"):
        for file in files:
            if file.endswith(str(widget.get_text()).replace("Edit ", "")):
                if platform.system() == "Windows":
                    os.startfile(root)
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", root])
                else:
                    subprocess.Popen(["xdg-open", root])

def on_RefreshTest( widget):
    oStore.subContainerRight.empty()
    oStore.subContainerRight.redraw()
    btn = gui.Button("Edit " + str(widget.get_text()).replace("Refresh ", ""), width=250, height=30, margin='10px')
    btn.add_class("btn-primary")
    btn.set_on_click_listener(on_EditTest)
    HeadLable = gui.Label("<BR>HIVE TEST AUTOMATION <BR>")
    HeadLable.style['font-size'] = '36px'
    oStore.subContainerRight.append(HeadLable)
    oStore.subContainerRight.append(btn)
    btn = gui.Button(widget.get_text(), width=250, height=30, margin='10px')
    btn.add_class("btn-primary")
    btn.set_on_click_listener(on_RefreshTest)
    oStore.subContainerRight.append(btn)
    oStore.subContainerRight.append(gui.Label(str(widget.get_text()).replace("Refresh ", "")))
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                         0] + "/01_BDD_Tier/features/"):
        for file in files:
            if file.endswith(str(widget.get_text()).replace("Refresh ", "")):
                with open(root + "/" + file) as f:
                    lines = f.readlines()
                Tableflag = False
                continueFlag = False
                counter = 0
                TableList = []
                for line in lines:
                    if "@" in line:
                        for tag in line.split("@"):
                            tag = str(tag).replace('  ', '')
                            if str(tag).strip() != "" and str(tag).strip() != "#":
                                btn = gui.Button(tag, width=250, height=30, margin='10px')
                                btn.add_class("btn-primary")
                                btn.set_on_click_listener(on_runTest)
                                oStore.subContainerRight.append(btn)
                    elif "|" in line:
                        if not Tableflag:
                            if not continueFlag:
                                # for col in line.split("|"):
                                # if str(col).strip() != "":
                                #    print("hi")
                                TableList.append(line.split("|"))
                                continueFlag = True
                                Tableflag = True
                                counter = counter + 1
                        else:
                            # for row in line.split("|"):
                            #    if str(row).strip() != "":
                            #        print("hi")
                            TableList.append(line.split("|"))

                            counter = counter + 1
                    else:
                        if len(TableList) > 0:
                            tbl = gui.Table.new_from_list(TableList, width='100%')
                            tbl.add_class("table table-hover")
                            oStore.subContainerRight.append(tbl)
                            Tableflag = False
                            continueFlag = False
                            counter = 0
                            TableList.clear()
                        txt = gui.Label(line, width='100%')
                        subTxt = gui.Container(width='100%')
                        if ("#" in line):
                            subTxt.style['color'] = 'rgb(32, 94, 15)'
                            subTxt.style['font-size'] = '10px'
                            subTxt.style['font-weight'] = '100'
                        if ("Feature" in line):
                            subTxt.style['color'] = 'rgb(130, 9, 9)'
                            subTxt.style['font-weight'] = '100'
                        if ("Scenario" in line):
                            subTxt.style['color'] = 'rgb(193, 81, 1)'
                            subTxt.style['font-weight'] = '100'
                        if ("Given" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                        if ("When" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                        if ("Then" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                        if ("And" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                        subTxt.append(txt)
                        oStore.subContainerRight.append(subTxt)
    oStore.consoleText.add_class("form-control input-lg")
    oStore.subContainerRight.append(oStore.consoleText)

def on_runTest(widget):
    try:
        if oStore.p:
            oStore.p.terminate()
            oStore.p.kill()
    except Exception as e:
        if "[Errno 3] No such process" in str(e):
            pass
        else:
            raise Exceptionclass.ExceptionHandling(str(e))
    oThread = start_new_thread(target=runTest, args=(widget,))
    flag = False
    oThread.setDaemon(True)
    oThread.start()

def runTest(widget):
    oStore.dtextinput.set_text('Test Execution Started, Please wait....')
    oStore.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
    oStore.consoleText.set_text("")
    oStore.consoleContainer.empty()
    #oStore.consoleContainer.append(gui.Label('<div id="div1" style="overflow:scroll; height:400px;">'))
    oFileName = "Execute.command"
    if "WINDOWS" in oStore.OS:
        oFileName = "Execute_WIN.bat"
    if "LINUX" in oStore.OS:
        oFileName = "Execute.sh"
    for root, dirs, files in os.walk(
                    os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
        for file in files:
            if file.endswith(oFileName):
                if "WINDOWS" not in oStore.OS and "LINUX" not in oStore.OS:
                    with open(root + "/" + file, 'w') as f:
                        f.write("#!/bin/sh \n")
                        f.write('cd "$(dirname ${BASH_SOURCE[0]})/../../01_BDD_Tier/features"\n')
                        f.write("behave --tags=" + widget.get_text())
                elif "WINDOWS" in oStore.OS:
                    with open(root + "/" + file, 'w') as f:
                        f.write('cd "%~dp0/../../01_BDD_Tier/features"\n')
                        f.write("behave --tags=" + widget.get_text())
                elif "LINUX" in oStore.OS:
                    with open(root + "/" + file, 'w') as f:
                        f.write("#!/bin/sh \n")
                        f.write('cd $(dirname "$0")/../../01_BDD_Tier/features\n')
                        f.write("behave --tags=" + widget.get_text())
                if "WINDOWS" in oStore.OS:
                    oStore.p = subprocess.Popen(root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                else:
                    oStore.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                temp = ''
                tempInner = ''
                while True:
                    if oStore.flag:
                        print("\nstopped by API\n")
                        oStore.flag = False
                        break
                    oStore.consoleText.onfocus()
                    oStore.consoleText.onclick()
                    out = oStore.p.stdout.read(1)
                    if out == '' and oStore.p.poll() != None:
                        oStore.dtextinput.set_value("Completed")
                        oStore.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                        break
                    if out != '':
                        sys.stdout.write(out.decode('latin1'))
                        if '\n' in tempInner:
                            lbl = gui.Label(tempInner, width='100%')
                            if ("DEBUG Tx:" in tempInner):
                                lbl.style['color'] = 'rgb(30, 104, 46)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                                lbl.style['text-align'] = 'right'
                            if ("DEBUG RX:" in tempInner):
                                if (",  OK" in tempInner):
                                    lbl.style['color'] = 'rgb(44, 55, 130)'
                                    lbl.style['font-size'] = '12px'
                                    lbl.style['background-color'] = '#edf3ff'
                                elif (",   ACK" in tempInner):
                                    lbl.style['color'] = 'rgb(44, 55, 130)'
                                    lbl.style['font-size'] = '12px'
                                    lbl.style['background-color'] = '#d4fbfc'
                                elif (",   NACK" in tempInner):
                                    lbl.style['color'] = 'rgb(44, 55, 130)'
                                    lbl.style['font-size'] = '12px'
                                    lbl.style['background-color'] = '#f99faa'
                                elif (",  RESPATTR" in tempInner):
                                    lbl.style['color'] = 'rgb(44, 55, 130)'
                                    lbl.style['font-size'] = '12px'
                                    lbl.style['background-color'] = '#f7e394'
                                elif (",  REPORTATTR" in tempInner):
                                    lbl.style['color'] = 'rgb(44, 55, 130)'
                                    lbl.style['font-size'] = '12px'
                                    lbl.style['background-color'] = '#fcc2f9'
                                elif (",  ZONESTATUS" in tempInner):
                                    lbl.style['color'] = 'rgb(44, 55, 130)'
                                    lbl.style['font-size'] = '12px'
                                    lbl.style['background-color'] = '#f3cdf7'
                                elif (
                                                    ",  IMGQUERY" in tempInner or ",  Bind" in tempInner or ",  Unbind" in tempInner or ",  CFGRPT" in tempInner
                                or ",  CHECKIN" in tempInner):
                                    lbl.style['color'] = 'rgb(44, 55, 130)'
                                    lbl.style['font-size'] = '12px'
                                    lbl.style['background-color'] = '#e4f9de'
                                else:
                                    lbl.style['background-color'] = '#fffbed'
                            if (
                                        "ERROR" in tempInner.upper() or "NACK" in tempInner.upper() or "**** PROBLEM" in tempInner.upper()):
                                lbl.style['color'] = 'rgb(99, 7, 7)'
                                lbl.style['font-size'] = '12px'
                                lbl.style['font-weight'] = 'bolder'
                            oStore.consoleText.set_text(temp)
                            oStore.consoleContainer.append(lbl)
                            #MyApp.execute_javascript(oStore.classObject, code=" $('#div1').scrollTop(1000000);")
                            # consoleContainer.redraw()
                            tempInner = ''
                        temp = temp + out.decode('latin1')
                        tempInner = tempInner + out.decode('latin1')
                        if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                            oStore.p.kill()
                            oStore.dtextinput.set_value("Error : Please check")
                            oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
                            break
                        sys.stdout.flush()
                print("\ncompleted\n")
                oStore.dtextinput.set_value("Test Execution Completed Sucessfully")
                oStore.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                break

def on_VerfifyTGSTick(widget):
    try:
        try:
            if oStore.p:
                oStore.p.terminate()
                oStore.p.kill()

        except Exception as e:
            if "[Errno 3] No such process" in str(e):
                pass
            else:
                raise Exceptionclass.ExceptionHandling(str(e))
        #killBatch()
        oThread = start_new_thread(target=getNodes, args=(widget,))
        flag = False
        oThread.setDaemon(True)
        oThread.start()
    except Exception as e:
        raise Exceptionclass.ExceptionHandling(str(e))

def killBatch(widget=None):
        oStore.flag = True

def getNodes(widget):
    try:
        oStore.dtextinput.set_value("Please Wait ...")
        oStore.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
        oFileName = "getNodes.command"
        if "WIND    OWS" in oStore.OS:
            oFileName = "getNodes_WIN.bat"
        if "LINUX" in oStore.OS:
            oFileName = "getNodes.sh"
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]+ str("/res")):
            for file in files:
                if file.endswith(oFileName):
                    if "WINDOWS" in oStore.OS:
                        p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    else:
                        p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    # print("pid = " + str(self.p.pid) + "\n")
                    temp = ''
                    tempInner = ''
                    oStore.consoleContainer.empty()

                    oStore.consoleContainer.append(gui.Label('<div id="div1" onLoad="scrll();" style="overflow:scroll; height:400px;">'))
                    while True:
                        if oStore.flag:
                            print("\nstopped by API\n")
                            oStore.flag = False
                            break
                        out = p.stdout.read(1)
                        if out == '' and p.poll() != None:
                            # self.p.kill()
                            break
                        if out != '':
                            sys.stdout.write(out.decode('latin1'))
                            # self.consoleText.set_text(temp)
                            if '\n' in tempInner:
                                lbl = gui.Label(tempInner, width='100%')
                                if ("DEBUG Tx:" in tempInner):
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                    lbl.style['text-align'] = 'right'
                                if ("DEBUG RX:" in tempInner):
                                    if (",  OK" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                        lbl.style['background-color'] = '#edf3ff'
                                    elif (",   ACK" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                        lbl.style['background-color'] = '#d4fbfc'
                                    elif (",   NACK" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                        lbl.style['background-color'] = '#f99faa'
                                    elif (",  RESPATTR" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                        lbl.style['background-color'] = '#f7e394'
                                    elif (",  REPORTATTR" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                        lbl.style['background-color'] = '#fcc2f9'
                                    elif (",  ZONESTATUS" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                        lbl.style['background-color'] = '#f3cdf7'
                                    elif (",  IMGQUERY" in tempInner or ",  Bind" in tempInner or ",  Unbind" in tempInner or ",  CFGRPT" in tempInner
                                          or ",  CHECKIN" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                        lbl.style['background-color'] = '#e4f9de'
                                    else:
                                        lbl.style['background-color'] = '#fffbed'
                                if ("ERROR" in tempInner.upper() or "NACK" in tempInner.upper()):
                                    lbl.style['color'] = 'rgb(99, 7, 7)'
                                    lbl.style['font-size'] = '12px'
                                oStore.consoleText.set_text(temp)
                                oStore.consoleContainer.append(lbl)
                                #MyApp.execute_javascript(oStore.classObject, code=" $('#div1').scrollTop(1000000);")
                                #oStore.consoleContainer.redraw()
                                # self.horizontalContainerDialog.redraw()
                                tempInner = ''
                            temp = temp + out.decode('latin1')
                            tempInner = tempInner + out.decode('latin1')
                            if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp or 'Done' in temp or "TIMEOUT: sendCommand() timeout" in temp:
                                p.kill()
                                # AT.stopThreads()
                                break
                            sys.stdout.flush()

                    strStatus = "Please Wait ..."
                    if 'Error opening port' in temp:
                        oStore.dtextinput.set_value("Error : Please connect TG STick")
                        oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
                        try:
                            AT.stopThreads()
                        except Exception as e:
                            raise Exceptionclass.ExceptionHandling(str(e))
                    elif "TIMEOUT: sendCommand() timeout" in temp:
                        oStore.dtextinput.set_value("TIMEOUT : Device did not respond")
                        oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
                        try:
                            AT.stopThreads()
                        except Exception as e:
                            raise Exceptionclass.ExceptionHandling(str(e))
                    else:
                        oStore.dtextinput.set_value("Please Wait ...")
                        oStore.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
                        consoleText = gui.TextInput(width='100%', height='100%')
                        consoleText.add_class("form-control input-lg")
                        oStore.consoleContainer.append(consoleText)
                        consoleText.set_text("")
                        # self.subContainerDevicesInnerConsole.empty()
                        # print(widget.get_text())
                        # os.system("cd /01_BDD_Tier/features")
                        # os.system("behave")



                        oNodes = dUtils.getZigbeeDevicesJson()

                        listItems = []
                        for oNode in oNodes:
                            listItems.append(oNodes[oNode]['name'] + "-(" + oNode + ")")
                            # txt = gui.Label(oNodes[oNode]['name'])
                            # self.subContainerDevices.append(txt)
                        oStore.DevDetailsContainer.empty()
                        oStore.DevDetailsContainer.redraw()
                        oStore.dtextinput.set_value("Completed")
                        oStore.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                        # self.horizontalContainerDialog.empty()
                        # self.horizontalContainerDialog.redraw()

                        txt = gui.ListView(True).new_from_list(listItems, width='70%')
                        txt.set_on_selection_listener(list_view_on_selected)
                        txt.add_class("list-group-item")
                        headingLabel = gui.Label("DEVICES")
                        headingLabel.style["font-size"] = "14px"
                        headingLabel.add_class("label label-info")
                        oStore.DevDetailsContainer.append(headingLabel)
                        oStore.DevDetailsContainer.append(txt)
                        oStore.DevDetailsContainer.redraw()
                        oStore.TopDetailsContainer.empty()
                        oStore.TopDetailsContainer.redraw()
                        try:
                            AT.stopThreads()
                        except:
                            print("stopped thread")
                        oJson = dUtils.getZigbeeDevicesJson()

                        oNodes = str(oJson.keys()).replace("dict_keys([", "").replace("'", "").replace("])",
                                                                                                       "").split(
                            ",")
                        oAllNodes = {}
                        for intCounter in range(0, len(oNodes)):
                            strDevice = str(oNodes[intCounter]).replace(" ", "")
                            strkey = str(oJson[strDevice]["name"]) + "-" + str(oJson[strDevice]["nodeID"])
                            oAllNodes[strkey] = {}
                            oAllNodes[strkey]["key"] = strkey
                            oAllNodes[strkey]["macID"] = oJson[strDevice]["macID"]
                            oAllNodes[strkey]["name"] = strDevice
                            oAllNodes[strkey]["ModeId"] = str(oJson[strDevice]["name"])
                            if str(oJson[strDevice]["type"]) != "RFD":
                                oAllNodes[strkey]["childNode"] = oJson[strDevice]["childNodes"]
                            else:
                                oAllNodes[strkey]["childNode"] = []
                        strChartData = "["
                        nodesList = []
                        intNodeCtr = 0
                        nodesList.append([])
                        nodesList[intNodeCtr].append("TGStick-0000")
                        nodesList[intNodeCtr].append("")
                        nodesList[intNodeCtr].append("")
                        flag = True
                        oDictTopology = []
                        while flag:
                            flag = False
                            for oNodeId in nodesList:
                                if oNodeId[1] == "False" or oNodeId[1] == "":
                                    strChartData = strChartData + "{"
                                    strChartData = strChartData + "\"key\":\"" + oAllNodes[oNodeId[0]][
                                        "key"] + "\","
                                    strChartData = strChartData + "\"name\":\"" + oAllNodes[oNodeId[0]][
                                        "name"] + "\","
                                    strChartData = strChartData + "\"model\":\"" + oAllNodes[oNodeId[0]][
                                        "ModeId"] + "\","
                                    strChartData = strChartData + "\"macID\":\"" + oAllNodes[oNodeId[0]][
                                        "macID"] + "\","
                                    if oNodeId[1] == "":
                                        oNodeId[1] = "True"
                                        strChartData = strChartData[:-1]
                                    if oNodeId[1] == "False":
                                        oNodeId[1] = "True"
                                        strChartData = strChartData + "\"parent\":\"" + str(oNodeId[2]) + "\""
                                        oDictTopology.append(
                                            str(oNodeId[2]) + " --> " + oAllNodes[oNodeId[0]]["key"])
                                    strChartData = strChartData + "},"
                                    for oNode in oAllNodes[oNodeId[0]]["childNode"]:
                                        flag = True
                                        intNodeCtr = intNodeCtr + 1
                                        nodesList.append([])
                                        for oRow in oAllNodes:
                                            if oNode in oRow:
                                                nodesList[intNodeCtr].append(oRow)
                                        nodesList[intNodeCtr].append("False")
                                        nodesList[intNodeCtr].append(oNodeId[0])

                        strChartData = strChartData[:-1]
                        strChartData = strChartData + "]"
                        lstTop = gui.ListView(True).new_from_list(oDictTopology, width='70%')
                        lstTop.add_class("list-group-item")
                        headingLabel = gui.Label("Topology")
                        headingLabel.style["font-size"] = "14px"
                        headingLabel.add_class("label label-info")
                        oStore.TopDetailsContainer.append(headingLabel)

                        oStore.TopDetailsContainer.append(lstTop)
                        oStore.TopDetailsContainer.redraw()
                        oStore.TopDetailsContainer.append(gui.Label("<BR>"))
                        oStore.consoleContainer.empty()
                    break
    except Exception as e:
        oStore.dtextinput.set_value("Error")
        oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
        raise Exceptionclass.ExceptionHandling(str(e))

def list_view_on_selected(widget, selected_item_key):
    refreshzigbeeTest(widget, selected_item_key)

def refreshzigbeeTest(widget=None, selected_item_key=None):
    strDeviceName = ""
    if widget is not None and selected_item_key is not None:
        oStore.dtextinput.set_value(str(widget.children[selected_item_key].get_text()).split("-")[0])
        oStore.dtextinput.style['background-color'] = 'rgb(232, 242, 255)'
        strDeviceName = str(widget.children[selected_item_key].get_text()).split("-")[0]
    else:
        strDeviceName = oStore.dtextinput.get_text().replace(" ", "")
    oStore.subContainerDevicesInner.empty()
    oStore.subContainerDevicesInner.redraw()
    if oStore.sessionName is "Zigbee":
        subContainerDevicesInnerScenarios = gui.Container(width='100%')
        subContainerDevicesInnerScenarios.style['overflow'] = "auto"
        subContainerDevicesInnerScenarios.style['left'] = "10px"
        subContainerDevicesInnerScenarios.style['top'] = "600px"
        subContainerDevicesInnerScenarios.style['margin'] = "0px"
        HeadLable = gui.Label("DEVICE REGRESSION TEST PACK FOR "+strDeviceName+" ",width='100%')
        HeadLable.style['font-size'] = '36px'
        HeadLable.add_class("label label-primary")
        subContainerDevicesInnerScenarios.append(gui.Label("<br>"))
        subContainerDevicesInnerScenarios.append(HeadLable)
        subContainerDevicesInnerScenarios.append(gui.Label("<br><br>"))
        oStore.subContainerDevicesInner.append(subContainerDevicesInnerScenarios)
        upgradeVersion = ""
        downgradeVersion = ""
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                             0] + "/01_BDD_Tier/features/"):
            TableList = []
            for file in files:
                if file.endswith(strDeviceName + ".feature"):
                    with open(root + "/" + file) as f:
                        lines = f.readlines()
                    Tableflag = False
                    continueFlag = False
                    counter = 0
                    TableList = []
                    upgradeFlag = False
                    for line in lines:
                        if "@" in line:
                            subContainerDevicesInnerScenarios.append(gui.Label("<BR><BR>"))
                            subContainerDevicesInnerScenarios.append(gui.Label("<hr>"))
                            subContainerDevicesInnerScenarios.append(gui.Label("<BR>"))
                            for tag in line.split("@"):
                                tag = str(tag).replace('  ', '')
                                if str(tag).strip() != "" and str(tag).strip() != "#":
                                    btn = gui.Button(tag, width=250, height=30, margin='10px')
                                    btn.add_class("btn-danger")
                                    btn.set_on_click_listener(on_runTest)
                                    subContainerDevicesInnerScenarios.append(btn)
                        elif "|" in line:
                            if not Tableflag:
                                if not continueFlag:
                                    subContainerDevicesInnerScenarios.append(gui.Label("<BR><BR>"))
                                    for col in line.split("|"):
                                        if str(col).strip() != "":
                                            if "DeviceVersion" in str(line):
                                                upgradeFlag = True
                                    TableList.append(line.split("|"))
                                    continueFlag = True
                                    Tableflag = True
                                    counter = counter + 1
                            else:
                                intCounter = 0
                                for row in line.split("|"):
                                    if str(row).strip() != "":

                                        if upgradeFlag and intCounter == 2 and "NA" not in str(row):
                                            if downgradeVersion == "":
                                                downgradeVersion = str(row)
                                        if upgradeFlag and intCounter == 3 and "NA" not in str(row):
                                            if upgradeVersion == "":
                                                upgradeVersion = str(row)
                                        intCounter = intCounter + 1
                                TableList.append(line.split("|"))

                                counter = counter + 1
                        else:
                            if len(TableList) > 0:
                                tbl = gui.Table.new_from_list(TableList, width='80%')
                                tbl.add_class("table table-hover")
                                subContainerDevicesInnerScenarios.append(tbl)
                                Tableflag = False
                                continueFlag = False
                                counter = 0
                                TableList.clear()
                            txt = gui.Label(line, width='100%')
                            subTxt = gui.Container(width='100%')
                            if ("#" in line):
                                subTxt.style['color'] = 'rgb(32, 94, 15)'
                                subTxt.style['font-size'] = '10px'
                            if ("Feature" in line):
                                subTxt.style['color'] = 'rgb(130, 9, 9)'
                                subTxt.style['font-weight'] = '100'
                            if ("Scenario" in line):
                                subTxt.style['color'] = 'rgb(193, 81, 1)'
                                subTxt.style['font-size'] = '16px'
                            if ("Given" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                                # subTxt.style['background-color'] = 'rgb(221, 221, 221)'
                            if ("When" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                                # subTxt.style['background-color'] = 'rgb(221, 221, 221)'
                            if ("Then" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                                # subTxt.style['background-color'] = 'rgb(221, 221, 221)'
                            if ("And" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                                # subTxt.style['background-color'] = 'rgb(221, 221, 221)'
                            if ("Examples:" in line):
                                subContainerDevicesInnerScenarios.append(gui.Label("<BR>"))
                            subTxt.append(txt)
                            subContainerDevicesInnerScenarios.append(subTxt)
            if len(TableList) > 0:
                tbl = gui.Table.new_from_list(TableList, width='100%')
                tbl.add_class("table table-hover")
                subContainerDevicesInnerScenarios.append(tbl)
                TableList.clear()
        oStore.subContainerDevicesInnerConsole.redraw()
        oStore.firmwareContainer.empty()
        oStore.firmwareContainer.redraw()
        oStore.upgradeVersion.set_text(upgradeVersion)
        oStore.DowngradeVersion.set_text(downgradeVersion)
        upgradeVersionTxt = gui.Label("Upgrade Version")
        downgradeVersionTxt = gui.Label("Downgrade Version")
        oStore.upContainer.empty()
        oStore.downContainer.empty()
        oStore.upContainer.append(upgradeVersionTxt)
        oStore.upContainer.append(oStore.upgradeVersion)
        oStore.changeFirmware.set_text("Replace " + strDeviceName + " firmware")
        oStore.changeFirmware.add_class("btn-warning")
        oStore.downContainer.append(downgradeVersionTxt)
        oStore.downContainer.append(oStore.DowngradeVersion)
        oStore.changeFirmware.set_on_click_listener(changeFirmawares)
        oStore.firmwareContainer.append(oStore.upContainer)
        oStore.firmwareContainer.append(oStore.downContainer)
        oStore.upContainer.append(gui.Label("<BR>"))
        oStore.firmwareContainer.append(oStore.changeFirmware)
        oStore.upContainer.append(gui.Label("<BR>"))
    if widget is not None and selected_item_key is not None:
        oJson = dUtils.getZigbeeDevicesJson()

        oNodes = str(oJson.keys()).replace("dict_keys([", "").replace("'", "").replace("])", "").split(",")
        oAllNodes = {}
        for intCounter in range(0, len(oNodes)):
            strDevice = str(oNodes[intCounter]).replace(" ", "")
            strkey = str(oJson[strDevice]["name"]) + "-" + str(oJson[strDevice]["nodeID"])
            oAllNodes[strkey] = {}
            oAllNodes[strkey]["key"] = strkey
            oAllNodes[strkey]["macID"] = oJson[strDevice]["macID"]
            oAllNodes[strkey]["name"] = strDevice
            oAllNodes[strkey]["ModeId"] = str(oJson[strDevice]["name"])
            if str(oJson[strDevice]["type"]) != "RFD":
                oAllNodes[strkey]["childNode"] = oJson[strDevice]["childNodes"]
            else:
                oAllNodes[strkey]["childNode"] = []
        listItems = []
        oStore.listDetailsContainer.empty()
        oStore.listDetailsContainer.redraw()
        if "Live" in oStore.sessionName:
            oStore.listDetailsContainer.append(oStore.btnFirmwareLive)
        listItems.append(
            oJson[
                str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(", "").replace(")", "")][
                'name'])
        listItems.append(
            oJson[
                str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(", "").replace(")", "")][
                'macID'])
        listItems.append(
            oJson[
                str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(", "").replace(")", "")][
                'nodeID'])
        listItems.append(
            oJson[
                str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(", "").replace(")", "")][
                'type'])
        listItems.append(str(
            oJson[
                str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(", "").replace(")", "")][
                'endPoints']))
        oStore.listDetails.new_from_list(listItems)
        oStore.listDetailsContainer.append(oStore.listDetails)
        if oStore.sessionName is "Zigbee":
            btn = gui.Button("Replace " + oJson[
                str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(", "").replace(")", "")][
                'macID'] + " for " + oJson[
                                 str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(",
                                                                                                          "").replace(
                                     ")", "")]['name'] + " Mac ID",width='70%')
            btn.add_class("btn-warning")
            btn.set_on_click_listener(on_ReplaceMac)
            oStore.listDetailsContainer.append(btn)
        if "Dump" in oStore.sessionName or "Live" in oStore.sessionName:
            oStore.listDetails.empty()
            oStore.listDetails = gui.ListView(True).new_from_list(listItems)
            oStore.listDetails.add_class("list-group")
            oStore.listDetailsContainer.append(oStore.listDetails)
            if "Dump" in oStore.sessionName: oStore.firmwareContainer.append(oStore.btnFirmwareZDump)
        if "OTA" in oStore.sessionName:
            oStore.listDetails.empty()
            oStore.listDetails = gui.ListView(True).new_from_list(listItems)
            oStore.listDetails.add_class("list-group")
            oStore.listDetailsContainer.append(oStore.listDetails)
            oStore.listDetailsContainer.append(oStore.lblFirmwareOTA)
            oStore.listDetailsContainer.append(oStore.txtFirmwarePath)
            oStore.listDetailsContainer.append(oStore.btnChangeFirmwareOTA)
            oStore.listDetailsContainer.append(oStore.btnFirmwareOTA)
        if "Live" in oStore.sessionName:
            baselineDumpFile = os.path.abspath(
                __file__ + "/../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/" + oJson[
                                   str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(",
                                                                                                            "").replace(
                                       ")", "")][
                                   'name'] + "_Baseline_Dump.json"
            oJsonCluster = open(baselineDumpFile, mode='r')
            oBSDumpJson = json.loads(oJsonCluster.read())
            lstClister = []
            oJsonCluster.close()
            oStore.listClusterContainer.empty()
            for ep in sorted(oBSDumpJson["ListOfEndPoints"].keys()):
                oEP = oBSDumpJson["ListOfEndPoints"][ep]
                strExpEndPoint = oEP["EndPoint"]
                for oClust in sorted(oEP["ListOfClusters"].keys()):
                    oClust = oEP["ListOfClusters"][oClust]
                    strExpClusterID = oClust["ClusterID"]
                    strExpClusterName = oClust["ClusterName"]
                    strExpClusterTYpe = oClust["ClusterType"]
                    lstClister.append(strExpClusterID + " - " + strExpClusterName + " - (" + strExpClusterTYpe + ")")
            oStore.listDetailsCluster = gui.ListView(True).new_from_list(lstClister)
            oStore.listDetailsCluster.add_class("list-group")
            oStore.listDetailsCluster.set_on_selection_listener(list_view_attr_on_selected)
            oStore.listClusterContainer.append(gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
            oStore.listClusterContainer.append(gui.Label('<div class="card-header">Available Clusters</div>'))
            oStore.listClusterContainer.append(oStore.listDetailsCluster)
            oStore.listClusterContainer.append(gui.Label('</div>'))

def FirmwareOTA(widget):
    MacAddress = ""
    for i in range(0, 4):
        temp = oStore.listDetails.children[list(oStore.listDetails.children)[i]].children['text'].replace("\'",
                                                                                                            "").replace(
            "[",
            "").replace(
            "]", "").split(",")[0]
        if len(temp) == 16 and "[" not in temp:
            MacAddress = temp
    # nodeid = dUtils.getModelIdWithMAC(MacAddress)
    node = dUtils.getDeviceIdWithMAC(MacAddress)
    nodes = dUtils.getDeviceNode(node)
    nodeid = nodes['nodeID']
    ep = str(list(nodes['endPoints'])[0])
    zbtype = nodes['type']
    oStore.otaLog.empty()
    for root, dirs, files in os.walk(
            os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
        for file in files:
            if file.endswith('firmwareUpgrade.py'):
                with open(root + "/" + file,'r') as f:
                    lines = f.readlines()
                with open(root + "/" + file, 'w') as f:
                    f.seek(0)
                    f.truncate()
                    intCounter = 0
                    for bline in lines:
                        line = bline
                        if "imageFile = " in line:
                            line = "imageFile = '" + oStore.txtFirmwarePath.get_text() + "'\n"
                            lines[intCounter] = line
                        if "nodeId = " in line:
                            line = "nodeId = '" + nodeid + "'\n"
                            lines[intCounter] = line
                        if "ep = " in line:
                            line = "ep = '" + ep + "'\n"
                            lines[intCounter] = line
                        if "zbType = " in line:
                            line = "zbType = '" + zbtype + "'\n"
                            lines[intCounter] = line
                        intCounter = intCounter + 1
                    f.writelines(lines)
                    f.close()
    try:
        try:
            if oStore.p:
                oStore.p.terminate()
                oStore.p.kill()
        except Exception as e:
            if "[Errno 3] No such process" in str(e):
                pass
            else:
                raise Exceptionclass.ExceptionHandling(str(e))
        #killBatch()
        oStore.oThread = start_new_thread(target=OTAupgrade)
        oStore.oThread.setDaemon(True)
        oStore.flag = False
        oStore.oThread.start()
    except Exception as e:
        raise Exceptionclass.ExceptionHandling(str(e))

def OTAupgrade():
    oStore.subContainerDevicesInnerConsole.empty()
    oStore.subContainerDevicesInnerConsole.redraw()
    oStore.subContainerDevicesInnerConsole.append(gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
    oStore.subContainerDevicesInnerConsole.append(gui.Label('<div class="card-header">OTA PROGRESS '))
    oStore.subContainerDevicesInnerConsole.append(gui.Label('<div class="progress"><div id="OTAProgress" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%"></div></div>'))
    lbl2 = gui.Label("0%")
    oStore.subContainerDevicesInnerConsole.append(lbl2)
    oStore.subContainerDevicesInnerConsole.append(gui.Label('</div >'))
    act = 0
    oFileName = "firmwareUpgrade.command"
    if "WINDOWS" in oStore.OS:
        oFileName = "firmwareUpgrade.bat"
    if "LINUX" in oStore.OS:
        oFileName = "firmwareUpgrade.sh"
    intCtr = 0
    for root, dirs, files in os.walk(
            os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
        for file in files:

            if file.endswith(oFileName):
                try:
                    if "WINDOWS" in oStore.OS:
                        oStore.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    else:
                        oStore.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    temp = ''
                    tempInner = ''
                    tempInnerGroup = ''
                    oStore.dtextinput.set_value("Please wait the OTA upgrade has Started ...")
                    oStore.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
                    while True:
                        if oStore.flag:
                            print("\nstopped by API\n")
                            oStore.flag = False
                            break
                        out = oStore.p.stdout.read(1)
                        if str(out) == 'b\'\'' and oStore.p.poll() != None:
                            break
                        lbl = gui.Label(tempInner, width='100%')
                        lbl.style['font-size'] = '10px'
                        if out != '':
                            sys.stdout.write(out.decode('latin1'))

                            if '\n' in tempInner:
                                if (" ---- " in tempInner):
                                    Max = int(tempInner.split(" ---- ")[0])
                                    act = act + int(tempInner.split(" ---- ")[1])
                                    val = (act / Max) * 100
                                    lbl2.set_text(str(round(val, 2)) + "% ||||||||||| " + str(act) + " / " + str(
                                        Max) + " |||||||||||  *" + (tempInner.split(" ---- ")[1]) + " block size")
                                    MyApp.execute_javascript(oStore.classObject, code="$('#OTAProgress').width('"+str(round(val, 2))+"%');")
                                else:
                                    lbl.set_text(tempInner)
                                    oStore.otaLog.append(lbl)
                                tempInner = ''
                                intCtr = intCtr + 1
                            temp = temp + out.decode('latin1')
                            tempInner = tempInner + out.decode('latin1')
                            if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                                oStore.p.kill()
                                break
                            sys.stdout.flush()

                    print("\ncompleted\n")
                    oStore.dtextinput.set_value("Completed")
                    oStore.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                    break
                except Exception as e:
                    killBatch()
                    raise Exceptionclass.ExceptionHandling(str(e))

def changeFirmwarePathOTA(widget):
    if os.path.exists(getFirmwarePath(oStore.OS)):
        oStore.fileselectionDialogOTA = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders',
                                                              False,
                                                              getFirmwarePath(oStore.OS), allow_file_selection=True,
                                                              allow_folder_selection=False)
    else:
        oStore.fileselectionDialogOTA = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders',
                                                              False,
                                                           os.path.abspath(os.path.curdir), allow_file_selection=True,
                                                              allow_folder_selection=False)
    oStore.fileselectionDialogOTA.set_on_confirm_value_listener(
        on_fileselection_dialog_confirmOTA)

    # here is returned the Input Dialog widget, and it will be shown
    oStore.fileselectionDialogOTA.show(oStore.classObject)

def getFirmwarePath( os):
    global FIRMWARE_ROOT_FILE_PATH
    if 'DARWIN' in platform.system().upper():
        FIRMWARE_ROOT_FILE_PATH = config.FIRMWARE_ROOT_FILE_PATH
    elif 'LINUX' in platform.system().upper():
        FIRMWARE_ROOT_FILE_PATH = '/home/pi/hardware/firmware-release-notes/'
    elif sys.platform.startswith('win'):
        FIRMWARE_ROOT_FILE_PATH = config.FIRMWARE_ROOT_FILE_PATH
    return FIRMWARE_ROOT_FILE_PATH

def on_fileselection_dialog_confirmOTA( widget, filelist):
    # a list() of filenames and folders is returned
    oStore.txtFirmwarePath.set_text(str(filelist[0]))

def changeFirmawares(widget):
    if oStore.upgradeVersion.get_text().replace(" ", "") == "":
        return
    if oStore.DowngradeVersion.get_text().replace(" ", "") == "":
        return
    btnText = str(widget.get_text()).split(" ")
    fileName = btnText[1]
    upgradeVersion = ""
    downgradeVersion = ""
    featureFilePath = ""
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                         0] + "/01_BDD_Tier/features/"):
        for file in files:
            if file.endswith(fileName + ".feature"):
                featureFilePath = root + "/" + fileName + ".feature"
                with open(root + "/" + file) as f:
                    lines = f.readlines()
                Tableflag = False
                continueFlag = False
                counter = 0
                TableList = []
                upgradeFlag = False
                for line in lines:
                    if "@" in line:
                        for tag in line.split("@"):
                            tag = str(tag).replace('  ', '')
                            # if str(tag).strip() != "" and str(tag).strip() != "#":
                            #    print("hi")
                    elif "|" in line:
                        if not Tableflag:
                            if not continueFlag:
                                # for col in line.split("|"):
                                #    if str(col).strip() != "":
                                #        print("hi")
                                if "DeviceVersion" in str(line):
                                    upgradeFlag = True
                                TableList.append(line.split("|"))
                                continueFlag = True
                                Tableflag = True
                                counter = counter + 1
                        else:
                            intCounter = 0
                            for row in line.split("|"):
                                if str(row).strip() != "":

                                    if upgradeFlag and intCounter == 2 and "NA" not in str(row):
                                        if downgradeVersion == "":
                                            downgradeVersion = str(row)
                                    if upgradeFlag and intCounter == 3 and "NA" not in str(row):
                                        if upgradeVersion == "":
                                            upgradeVersion = str(row)
                                    intCounter = intCounter + 1
                            TableList.append(line.split("|"))

                            counter = counter + 1
                    else:
                        if len(TableList) > 0:
                            Tableflag = False
                            continueFlag = False
                            counter = 0
                            TableList.clear()
    filedata = None
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                         0] + "/01_BDD_Tier/features/"):
        for file in files:
            if file.endswith(fileName + ".feature"):
                with open(root + "/" + file) as f:
                    filedata = f.read()
                    filedata = filedata.replace(upgradeVersion.replace(" ", ""),
                                                oStore.upgradeVersion.get_text().replace(" ", ""))
                    filedata = filedata.replace(downgradeVersion.replace(" ", ""),
                                                oStore.DowngradeVersion.get_text().replace(" ", ""))
                with open(root + "/" + file, 'w') as f:
                    f.write(filedata)
    refreshzigbeeTest(widget=None, selected_item_key=None)

def on_ReplaceMac(widget):
    btnText = str(widget.get_text()).split(" ")
    fileName = btnText[(len(btnText) - 3)]
    btnMac = btnText[1]
    oStore.subContainerDevicesInner.empty()
    oStore.subContainerDevicesInner.redraw()
    lstMac = []
    featureFilePath = ""
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                         0] + "/01_BDD_Tier/features/"):
        for file in files:
            if file.endswith(fileName + ".feature"):
                featureFilePath = root + "/" + fileName + ".feature"
                with open(root + "/" + file) as f:
                    lines = f.readlines()
                Tableflag = False
                continueFlag = False
                counter = 0
                TableList = []
                for line in lines:
                    if "@" in line:
                        for tag in line.split("@"):
                            tag = str(tag).replace('  ', '')
                            # if str(tag).strip() != "" and str(tag).strip() != "#":
                            #    print("hi")
                    elif "|" in line:
                        if not Tableflag:
                            if not continueFlag:
                                # for col in line.split("|"):
                                #    if str(col).strip() != "":
                                #        print("hi")
                                TableList.append(line.split("|"))
                                continueFlag = True
                                Tableflag = True
                                counter = counter + 1
                        else:
                            for row in line.split("|"):
                                if str(row).strip() != "":
                                    macReg = re.compile("([0-9a-f]{2}(:?[0-9a-f]{2}){5})")
                                    res = re.findall(r"([0-9A-F]{2}(:?[0-9A-F]{2}){5})", str(row).replace(" ", ""))
                                    if len(res) > 0:
                                        lstMac.append(str(row).replace(" ", ""))
                                        # print(str(row).replace(" ",""))

                            TableList.append(line.split("|"))

                            counter = counter + 1
                    else:
                        if len(TableList) > 0:
                            Tableflag = False
                            continueFlag = False
                            counter = 0
                            TableList.clear()
    filedata = None
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                         0] + "/01_BDD_Tier/features/"):
        for file in files:
            if file.endswith(fileName + ".feature"):
                with open(root + "/" + file) as f:
                    filedata = f.read()
                    for oMac in lstMac:
                        filedata = filedata.replace(oMac, btnMac)
                with open(root + "/" + file, 'w') as f:
                    f.write(filedata)

    strDeviceName = ""
    strDeviceName = oStore.dtextinput.get_text().replace(" ", "")
    oStore.subContainerDevicesInner.empty()
    oStore.subContainerDevicesInner.redraw()
    upgradeVersion = ""
    downgradeVersion = ""
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                         0] + "/01_BDD_Tier/features/"):
        for file in files:
            if file.endswith(strDeviceName + ".feature"):
                with open(root + "/" + file) as f:
                    lines = f.readlines()
                Tableflag = False
                continueFlag = False
                counter = 0
                TableList = []
                upgradeFlag = False
                for line in lines:
                    if "@" in line:
                        for tag in line.split("@"):
                            tag = str(tag).replace('  ', '')
                            if str(tag).strip() != "" and str(tag).strip() != "#":
                                btn = gui.Button(tag, width=250, height=30, margin='10px')
                                btn.add_class("btn-primary")
                                btn.set_on_click_listener(on_runTest)
                                oStore.subContainerDevicesInner.append(btn)
                    elif "|" in line:
                        if not Tableflag:
                            if not continueFlag:
                                for col in line.split("|"):
                                    if str(col).strip() != "":
                                        if "DeviceVersion" in str(line):
                                            upgradeFlag = True
                                TableList.append(line.split("|"))
                                continueFlag = True
                                Tableflag = True
                                counter = counter + 1
                        else:
                            intCounter = 0
                            for row in line.split("|"):
                                if str(row).strip() != "":

                                    if upgradeFlag and intCounter == 2 and "NA" not in str(row):
                                        if downgradeVersion == "":
                                            downgradeVersion = str(row)
                                    if upgradeFlag and intCounter == 3 and "NA" not in str(row):
                                        if upgradeVersion == "":
                                            upgradeVersion = str(row)
                                    intCounter = intCounter + 1
                            TableList.append(line.split("|"))

                            counter = counter + 1
                    else:
                        if len(TableList) > 0:
                            tbl = gui.Table.new_from_list(TableList, width='80%')
                            tbl.add_class("table table-hover")
                            oStore.subContainerDevicesInner.append(tbl)
                            Tableflag = False
                            continueFlag = False
                            counter = 0
                            TableList.clear()
                        txt = gui.Label(line, width='100%')
                        subTxt = gui.Container(width='100%')
                        if ("#" in line):
                            subTxt.style['color'] = 'rgb(32, 94, 15)'
                            subTxt.style['font-size'] = '10px'
                        if ("Feature" in line):
                            subTxt.style['color'] = 'rgb(130, 9, 9)'
                            subTxt.style['font-weight'] = '100'
                        if ("Scenario" in line):
                            subTxt.style['color'] = 'rgb(193, 81, 1)'
                            subTxt.style['font-weight'] = '100'
                        if ("Given" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                            # subTxt.style['background-color'] = 'rgb(221, 221, 221)'
                        if ("When" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                            # subTxt.style['background-color'] = 'rgb(221, 221, 221)'
                        if ("Then" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                            # subTxt.style['background-color'] = 'rgb(221, 221, 221)'
                        if ("And" in line):
                            subTxt.style['color'] = 'rgb(28, 61, 178)'
                            # subTxt.style['background-color'] = 'rgb(221, 221, 221)'
                        subTxt.append(txt)
                        oStore.subContainerDevicesInner.append(subTxt)

def list_view_attr_on_selected( widget, selected_item_key):
    oStore.listAttrContainer.empty()
    oJson = dUtils.getZigbeeDevicesJson()
    baselineDumpFile = os.path.abspath(
        __file__ + "/../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/" + oStore.dtextinput.get_text() + "_Baseline_Dump.json"
    oJsonCluster = open(baselineDumpFile, mode='r')
    oBSDumpJson = json.loads(oJsonCluster.read())
    lstAttr = []
    oJsonCluster.close()
    for ep in sorted(oBSDumpJson["ListOfEndPoints"].keys()):
        oEP = oBSDumpJson["ListOfEndPoints"][ep]
        strExpEndPoint = oEP["EndPoint"]
        for oClust in sorted(oEP["ListOfClusters"].keys()):
            oClust = oEP["ListOfClusters"][oClust]
            if oClust["ClusterID"] in str(widget.children[selected_item_key].get_text()).split(" - ")[0]:
                strExpClusterID = oClust["ClusterID"]
                strExpClusterName = oClust["ClusterName"]
                strExpClusterTYpe = oClust["ClusterType"]
                for oAttr in sorted(oClust["ListOfAttributes"].keys()):
                    oAttr = oClust["ListOfAttributes"][oAttr]
                    strExpAttrID = oAttr["AttributeID"]
                    strExpAttrName = oAttr["AttributeName"]
                    strExpAttrType = oAttr["AttributeType"]
                    strExpAttrValue = oAttr["DefaultValue"]
                    strExpAttrRCS = oAttr["ReportableConfigState"]
                    lstAttr.append(strExpAttrID+" - "+strExpAttrName+" - "+strExpAttrType)
    listDetailsAttrLive = gui.ListView(True).new_from_list(lstAttr)
    listDetailsAttrLive.style['width'] = "60%"
    oStore.listAttrContainer.append(gui.Label('<div class="card border-secondary mb-3" style="width: 70%;display: inline-block;">'))
    oStore.listAttrContainer.append(gui.Label('<div class="card-header">Available Attributes</div>'))
    oStore.listAttrContainer.append(listDetailsAttrLive)
    oStore.listAttrContainerRepoLive.empty()
    oStore.listAttrContainerRepoLive.append(gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
    oStore.listAttrContainerRepoLive.append(gui.Label('<div class="card-header">Attribute Config</div>'))
    oStore.listAttrContainerRepoLive.append(oStore.lbl1 )
    oStore.listAttrContainerRepoLive.append(oStore.txtMinRepo)
    oStore.listAttrContainerRepoLive.append(oStore.lbl2)
    oStore.listAttrContainerRepoLive.append(oStore.txtMaxRepo)
    oStore.listAttrContainerRepoLive.append(oStore.lbl3)
    oStore.listAttrContainerRepoLive.append(oStore.txtWriteVal)
    oStore.listAttrContainerRepoLive.append(gui.Label('</div></div>'))
    oStore.listAttrContainer.append(oStore.listAttrContainerRepoLive)

def on_table_row_click(widget, selected_item_key):
    if len(oStore.DevDetailsContainer.children) == 0:
        oStore.dtextinput.set_value("Error : Click on get connected devices to continue")
        oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
        return
    if oStore.btnFirmwareLive.get_text() == "Start":
        oStore.dtextinput.set_value("Error : Click on get connected devices to continue")
        oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
        return
    MacAddress = ""
    for i in range(0, 4):
        temp = oStore.listDetails.children[list(oStore.listDetails.children)[i]].children['text'].replace("\'",
                                                                                                              "").replace(
            "[",
            "").replace(
            "]", "").split(",")[0]
        if len(temp) == 16 and "[" not in temp:
            MacAddress = temp
    # nodeid = dUtils.getModelIdWithMAC(MacAddress)
    node = dUtils.getDeviceIdWithMAC(MacAddress)
    nodes = dUtils.getDeviceNode(node)
    nodeid = nodes['nodeID']
    ep = 0
    if len(list(nodes['endPoints'])) > 0:
        ep = str(list(nodes['endPoints'])[0])
    zbtype = nodes['type']
    strCluster = ""
    strAttr = ""
    strType = ""
    strAttrType = ""
    try:
        for oCl in oStore.listClusterContainer.children:
            if 'ListView' in str(oStore.listClusterContainer.children[oCl]):
                strCluster = oStore.listClusterContainer.children[oCl]._selected_item.children['text']
                strType = str(strCluster).split(" - ")[2].replace("(", "").replace(")", "")
                strCluster = oStore.listClusterContainer.children[oCl]._selected_item.children['text'].split(" - ")[0]
        for oAt in oStore.listAttrContainer.children:
            if 'ListView' in str(oStore.listAttrContainer.children[oAt]):
                strAttr = oStore.listAttrContainer.children[oAt]._selected_item.children['text']
    except Exception as e:
        print(str(e))
        pass
    try:
        strAttrType = str(strAttr).split(" - ")[2]
        strAttr = str(strAttr).split(" - ")[0]

    except Exception as e:
        print(str(e))
        pass
    CoordnodeEUI = ""
    nodeEUI = ""
    if 'ATI' in str(widget.children[selected_item_key].get_text()):
        AT.sendCommand("ATI","OK",2,3)
    if 'AT+DASSL' in str(widget.children[selected_item_key].get_text()):
        AT.sendCommand("AT+DASSL","OK",2,3)
    if 'REMOVE' in str(widget.children[selected_item_key].get_text()):
        AT.sendCommand("AT+DASSR:"+nodeid,"OK",2,5)
    if 'AT+PJOIN' in str(widget.children[selected_item_key].get_text()):
        AT.sendCommand("AT+PJOIN","OK",1,3)
    if 'AT+EN' in str(widget.children[selected_item_key].get_text()):
        AT.sendCommand("AT+EN", 'JPAN:(..)', 2, 3)
    if 'AT+JN' in str(widget.children[selected_item_key].get_text()):
        AT.sendCommand("AT+EN", 'JPAN', 2, 3)
    if 'AT+READ' in str(widget.children[selected_item_key].get_text()):
        msg, exp = AT.buildGetAttributeCommands(nodeid, ep,strCluster
        ,strAttr,strType)
        AT.sendCommand(msg, exp, 2, 3)
    if 'AT+BIND' in str(widget.children[selected_item_key].get_text()):
        respState, respCode, respValue = AT.getEUI(nodeid, nodeid)

        if respState and respCode == zcl.statusCodes['SUCCESS']:
            nodeEUI = respValue
        respState, respCode, respValue = AT.getEUI('0000', '0000')
        if respState and respCode == zcl.statusCodes['SUCCESS']:
            CoordnodeEUI = respValue
            AT.setBinding(nodeid,nodeEUI,ep,strCluster,CoordnodeEUI,'01')
    if 'AT+UNBIND' in str(widget.children[selected_item_key].get_text()):
        respState, respCode, respValue = AT.getEUI(nodeid, nodeid)
        if respState and respCode == zcl.statusCodes['SUCCESS']:
            nodeEUI = respValue
        respState, respCode, respValue = AT.getEUI('0000', '0000')
        if respState and respCode == zcl.statusCodes['SUCCESS']:
            CoordnodeEUI = respValue
        AT.setUnBind(nodeid,nodeEUI,ep,strCluster,CoordnodeEUI,'01')
    if 'AT+BTABLE' in str(widget.children[selected_item_key].get_text()):
        lstDel = []
        _,_,rows = AT.getBindings(nodeid)
        for ro in rows:
            if 'BTable' in ro or 'Length' in ro:
                lstDel.append(ro)
        for ro in lstDel:
            rows.remove(ro)
        lstFinal = []
        for ro in rows:
            lstFinal.append([str(ro).split("|")[0],str(ro).split("|")[1],str(ro).split("|")[2],str(ro).split("|")[3],str(ro).split("|")[4],str(ro).split("|")[5]])
        btab = gui.Table.new_from_list(lstFinal,True,width='100%')
        btab.add_class("table table-hover")
        oStore.consoleContainer.append(btab)
        #MyApp.execute_javascript(oStore.classObject, code=" $('#div1').scrollTop(1000000);")
    if 'AT+NTABLE' in str(widget.children[selected_item_key].get_text()):
        _, _, rows = utils.getNtable(nodeid)
        lstDel = []
        for ro in rows:
            if 'NTable' in ro or 'Length' in ro:
                lstDel.append(ro)
        for ro in lstDel:
            rows.remove(ro)
        lstFinal = []
        for ro in rows:
            lstFinal.append([str(ro).split("|")[0],str(ro).split("|")[1],str(ro).split("|")[2],str(ro).split("|")[3],str(ro).split("|")[4]])
        ntab = gui.Table.new_from_list(lstFinal, True, width='100%')
        ntab.add_class("table table-hover")
        oStore.consoleContainer.append(ntab)
        #MyApp.execute_javascript(oStore.classObject, code=" $('#div1').scrollTop(1000000);")
    if 'AT+WRITE' in str(widget.children[selected_item_key].get_text()):
        AT.setAttribute(nodeid, ep,strCluster,strType,strAttr,strAttrType,oStore.txtWriteVal.get_text())
    if 'GET REPORTING' in str(widget.children[selected_item_key].get_text()):
        AT.getAttributeReporting(nodeid,ep,strCluster,strAttr,False)
    if 'SET REPORTING ON CHANGE' in str(widget.children[selected_item_key].get_text()):
        if oStore.txtMinRepo.get_text() == "" or oStore.txtMaxRepo.get_text() == "":
            oStore.dtextinput.set_value("Error : Enter min and max values to set reporting")
            oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
            return
        AT.setAttributeReporting(nodeid,ep,strCluster,strAttr,oStore.txtMinRepo.get_text(),oStore.txtMaxRepo.get_text(),"1")
    if 'SET REPORTING' in str(widget.children[selected_item_key].get_text()) and 'ON CHANGE' not in str(widget.children[selected_item_key].get_text()):
        if oStore.txtMinRepo.get_text() == "" or oStore.txtMaxRepo.get_text() == "":
            oStore.dtextinput.set_value("Error : Enter min and max values to set reporting")
            oStore.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
            return
        AT.setAttributeReporting(nodeid,ep,strCluster,strAttr,oStore.txtMinRepo.get_text(),oStore.txtMaxRepo.get_text())
    if str(widget.children[selected_item_key].get_text()) == 'ON':
        utils.setSPOnOff(nodeid, ep,'ON')
    if str(widget.children[selected_item_key].get_text()) == 'OFF':
        utils.setSPOnOff(nodeid, ep,'OFF')
    oStore.txtFocus.onfocus()
    MyApp.execute_javascript(oStore.classObject, code="document.getElementById('focus').focus();")

def focusToBottom(widget):
    MyApp.execute_javascript(oStore.classObject, code="$('#div1').scrollTop($('#div1')[0].scrollHeight- $('#div1')[0].clientHeight);")

class screen1Widget(Container):
    def __init__(self,**kwargs):
        super(screen1Widget,self).__init__(**kwargs)
        self.style['position'] = "absolute"
        self.style['overflow'] = "auto"
        self.style['left'] = "10px"
        self.style['top'] = "10px"
        self.style['margin'] = "0px"
        self.style['width'] = "98%"
        self.style['display'] = "block"
        self.style['height'] = "98%"

        self.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
        self.append(gui.Label('<div class="card-header" style="display: inherit;">'
                              '<img class="Image" style="width:70px;margin:10px;height:70px" src="res/hive.png"></img>'
                              '<h1 style="text-align:center;width:70%">HIVE TEST AUTOMATION - UI </h1></div>'))
        #self.append(testlabel,'testlabel')
        #self.append(mytextbox,'mytextbox')
        oStore.subContainerLeft.style['display'] = 'block'
        oStore.subContainerLeft.style['overflow'] = 'auto'
        oStore.subContainerLeft.style['text-align'] = 'center'
        self.img = gui.Image('/res/hive.png', width=100, height=100, margin='10px')
        # self.img.style['background-image'] = "url('/res/FWLogo.png')"
        #oStore.subContainerLeft.append(self.img)
        ReadFeatureFile(oStore.subContainerLeft)
        horizontalContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px')
        horizontalContainer.style['display'] = 'block'
        horizontalContainer.style['overflow'] = 'auto'
        horizontalContainer.append(oStore.subContainerLeft)
        horizontalContainer.append(oStore.subContainerRight)
        self.append(horizontalContainer)
        self.append(gui.Label('</div>'))

#class definition for content "screen2" (inherits from remi.gui.Container)

class screen2Widget(Container):
    def __init__(self,**kwargs):
        super(screen2Widget,self).__init__(**kwargs)
        self.style['position'] = "absolute"
        self.style['overflow'] = "auto"
        self.style['background-color'] = "#ffffff"
        self.style['left'] = "10px"
        self.style['top'] = "10px"
        self.style['margin'] = "0px"
        self.style['width'] = "98%"
        self.style['display'] = "block"
        self.style['height'] = "98%"
        self.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
        self.append(gui.Label('<div class="card-header"><h1 style="text-align:center;">ZIGBEE REGRESSION TEST </h1></div>'))
        oStore.verifyTGStick.set_on_click_listener(on_VerfifyTGSTick)
        self.append(oStore.dtextinput)
        self.append(oStore.verifyTGStick)
        oStore.dtextinput.style['left'] = "10px"
        oStore.dtextinput.style['top'] = "100px"
        oStore.dtextinput.add_class("form-control input-lg")
        oStore.subContainerDevices.append(oStore.DevDetailsContainer)
        oStore.subContainerDevices.append(oStore.TopDetailsContainer)
        oStore.subContainerDevices.append(oStore.listDetailsContainer)
        oStore.subContainerDevices.append(oStore.listDetailsContainer)
        oStore.subContainerDevices.append(oStore.firmwareContainer)
        self.append(oStore.subContainerDevices)
        oStore.subContainerDevicesInnerConsole.append(gui.Label("<br>"))
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        oStore.subContainerDevicesInnerConsole.append(gui.Label("<br>"))
        self.append(oStore.subContainerDevicesInner)
        self.append(oStore.subContainerDevicesInnerConsole)
        self.append(gui.Label('</div>'))

class screen3Widget(Container):
    def __init__(self,**kwargs):
        super(screen3Widget,self).__init__(**kwargs)
        self.style['position'] = "absolute"
        self.style['overflow'] = "auto"
        self.style['background-color'] = "#ffffff"
        self.style['left'] = "10px"
        self.style['top'] = "10px"
        self.style['margin'] = "0px"
        self.style['width'] = "98%"
        self.style['display'] = "block"
        self.style['height'] = "98%"
        self.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
        self.append(gui.Label('<div class="card-header"><h1 style="text-align:center;"> ZIGBEE DUMPS </h1></div>'))
        oStore.verifyTGStick.set_on_click_listener(on_VerfifyTGSTick)
        self.append(oStore.dtextinput)
        self.append(oStore.verifyTGStick)
        oStore.dtextinput.style['left'] = "10px"
        oStore.dtextinput.style['top'] = "100px"
        oStore.dtextinput.add_class("form-control input-lg")
        oStore.subContainerDevices.append(oStore.DevDetailsContainer)
        oStore.subContainerDevices.append(oStore.TopDetailsContainer)
        oStore.subContainerDevices.append(oStore.listDetailsContainer)
        oStore.subContainerDevices.append(oStore.firmwareContainer)
        #oStore.subContainerDevices.append(oStore.btnFirmwareZDump)
        self.append(oStore.subContainerDevices)
        #oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        self.append(oStore.subContainerDevicesInner)
        self.append(oStore.subContainerDevicesInnerConsole)
        self.append(gui.Label('</div>'))

class screen4Widget(Container):
    def __init__(self,**kwargs):
        super(screen4Widget,self).__init__(**kwargs)
        classObject = self
        self.style['position'] = "absolute"
        self.style['overflow'] = "auto"
        self.style['background-color'] = "#ffffff"
        self.style['left'] = "10px"
        self.style['top'] = "10px"
        self.style['margin'] = "0px"
        self.style['width'] = "98%"
        self.style['display'] = "block"
        self.style['height'] = "98%"
        self.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
        self.append(gui.Label('<div class="card-header"><h1 style="text-align:center;"> OTA UPGRADE / DOWNGRADE </h1></div>'))
        oStore.verifyTGStick.set_on_click_listener(on_VerfifyTGSTick)
        self.append(oStore.dtextinput)
        self.append(oStore.verifyTGStick)
        oStore.dtextinput.style['left'] = "10px"
        oStore.dtextinput.style['top'] = "100px"
        oStore.dtextinput.add_class("form-control input-lg")
        oStore.subContainerDevices.append(oStore.DevDetailsContainer)
        oStore.subContainerDevices.append(oStore.TopDetailsContainer)
        oStore.subContainerDevices.append(oStore.listDetailsContainer)
        oStore.subContainerDevices.append(oStore.firmwareContainer)
        self.append(oStore.subContainerDevices)
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        self.append(oStore.subContainerDevicesInner)
        self.append(oStore.subContainerDevicesInnerConsole)
        self.append(oStore.otaLog)
        self.append(gui.Label('</div>'))

class screen5Widget(Container):
    def __init__(self,**kwargs):
        super(screen5Widget,self).__init__(**kwargs)
        classObject = self
        self.style['position'] = "absolute"
        self.style['overflow'] = "auto"
        self.style['background-color'] = "#ffffff"
        self.style['left'] = "10px"
        self.style['top'] = "10px"
        self.style['margin'] = "0px"
        self.style['width'] = "98%"
        self.style['display'] = "block"
        self.style['height'] = "98%"
        self.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
        self.append(gui.Label('<div class="card-header"><h1 style="text-align:center;"> FRAMEWORK CONFIG </h1></div>'))
        self.append(oStore.dtextinput)
        oStore.dtextinput.style['left'] = "10px"
        oStore.dtextinput.style['top'] = "100px"
        oStore.dtextinput.add_class("form-control input-lg")
        #self.append(oStore.subContainerDevices)
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        strJson = open(utils.strGlobVarFilePath, mode='r')
        utils.oJsonDict = json.loads(strJson.read())
        strJson.close()
        strAPIValidationType = utils.getAttribute('common', 'apiValidationType')
        oStore.drpValidation.set_value(strAPIValidationType)
        self.append(oStore.subConfig)
        self.append(oStore.subContainerConfig, "container")
        oStore.txtFirmware.set_text(getFirmwarePath(oStore.OS))
        self.append(oStore.subContainerDevicesInner)
        self.append(oStore.subContainerDevicesInnerConsole)
        self.append(gui.Label('</div>'))

class screen6Widget(Container):
    def __init__(self,**kwargs):
        super(screen6Widget,self).__init__(**kwargs)
        classObject = self
        self.style['position'] = "absolute"
        self.style['overflow'] = "auto"
        self.style['background-color'] = "#ffffff"
        self.style['left'] = "10px"
        self.style['top'] = "10px"
        self.style['margin'] = "0px"
        self.style['width'] = "98%"
        self.style['display'] = "block"
        self.style['height'] = "98%"
        self.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
        self.append(gui.Label('<div class="card-header"><h1 style="text-align:center;">LIVE TERMINAL</h1></div>'))
        self.append(oStore.dtextinput)
        oStore.verifyTGStick.set_on_click_listener(on_VerfifyTGSTick)
        self.append(oStore.dtextinput)
        self.append(oStore.verifyTGStick)
        oStore.dtextinput.style['left'] = "10px"
        oStore.dtextinput.style['top'] = "100px"
        oStore.dtextinput.add_class("form-control input-lg")
        oStore.subContainerDevices.append(oStore.listDetailsContainer)
        oStore.subContainerDevices.append(oStore.listClusterContainer)
        oStore.subContainerDevices.append(oStore.listAttrContainer)
        self.append(oStore.subContainerDevices)
        self.append(gui.Label('<div style="width: 85%;display: -webkit-inline-box">'))
        self.append(gui.Label('<div class="card-header" style="width: 80%;"><h5 style="text-align:center;"> CONSOLE </h5>'))
        self.append(gui.Label('</div>'))
        self.append(gui.Label('<div class="card-header" style="width: 20%;"><h5 style="text-align:center;"> COMMANDS </h5>'))
        self.append(gui.Label('</div></div>'))
        oStore.subContainerDevicesInnerConsole.append(gui.Label('<div style="width: 100%">'))
        oStore.subContainerDevicesInnerConsole.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 80%">'))
        oStore.subContainerDevicesInnerConsole.append(gui.Label('<div class="card-header"><h3 style="text-align:center;"> CONSOLE </h3></div>'))
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        oStore.subContainerDevicesInnerConsole.append(oStore.txtFocus)
        oStore.subContainerDevicesInnerConsole.append(oStore.btnSend)
        oStore.subContainerDevicesInnerConsole.append(gui.Label('</div>'))
        self.append(oStore.subContainerDevicesInnerConsole)
        oStore.subContainerDevicesInnerConsole.append(gui.Label('<div style="width:10%">'))
        oStore.subContainerDevicesInnerConsole.append(oStore.subContainerVerticalLive)
        oStore.subContainerDevicesInnerConsole.append(gui.Label('</div>'))
        oStore.screenObject = self
        self.append(gui.Label('</div>'))

class screen7Widget(Container):
    def __init__(self,**kwargs):
        super(screen7Widget,self).__init__(**kwargs)
        classObject = self
        self.style['position'] = "absolute"
        self.style['overflow'] = "auto"
        self.style['background-color'] = "#ffffff"
        self.style['left'] = "10px"
        self.style['top'] = "10px"
        self.style['margin'] = "0px"
        self.style['width'] = "98%"
        self.style['display'] = "block"
        self.style['height'] = "98%"
        self.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
        self.append(gui.Label('<div class="card-header"><h1 style="text-align:center;">Latest Result</h1></div>'))
        oStore.screenObject = self
        self.append(oStore.results)
        self.append(gui.Label('<div id="result"></div>'))
        self.append(gui.Label('</div>'))

class screen8Widget(Container):
    def __init__(self,**kwargs):
        super(screen8Widget,self).__init__(**kwargs)
        classObject = self
        self.style['position'] = "absolute"
        self.style['overflow'] = "auto"
        self.style['background-color'] = "#ffffff"
        self.style['left'] = "10px"
        self.style['top'] = "10px"
        self.style['margin'] = "0px"
        self.style['width'] = "98%"
        self.style['display'] = "block"
        self.style['height'] = "98%"
        self.append(
            gui.Label('<div class="card border-secondary mb-3" style="width: 100%">'))
        self.append(gui.Label('<div class="card-header"><h1 style="text-align:center;"> Result Directory</h1></div>'))
        oStore.screenObject = self
        self.append(oStore.results)
        self.append(gui.Label('<div id="result"></div>'))
        self.append(gui.Label('</div>'))

class MyApp(App):
    def __init__(self, *args):
        #custom additional html head tags
        my_html_head = """<title>Hive Test - Device Automation</title>"""
        my_css_head = """                    
                    <link rel="stylesheet" href="https://bootswatch.com/4/cerulean/bootstrap.min.css">
                    <link rel="stylesheet" href="https://bootswatch.com/4/cerulean/bootstrap.css">
                    """
        # custom js
        my_js_head = """
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
                    
                    """
        #res_path = [os.path.join(os.path.dirname(__file__), 'res') , os.path.join(os.path.dirname(__file__), '03_Results_Tier')]
        res_path = os.path.join(os.path.dirname(__file__), 'res')
        super(MyApp, self).__init__(*args, static_file_path=res_path, html_head=my_html_head, css_head=my_css_head, js_head=my_js_head)
        flag = False

    def idle(self):
        #this function is called automatically by remi library at specific interval
        # so here I can assign values to widget
        pass

    def main(self):
        subprocess.Popen('python3 -m http.server 8012',shell=True)
        oStore.classObject = self
        baseContainer = Container()
        baseContainer.attributes['class'] = "Widget"
        baseContainer.attributes['editor_baseclass'] = "Widget"
        baseContainer.attributes['editor_varname'] = "baseContainer"
        baseContainer.attributes['editor_tag_type'] = "widget"
        baseContainer.attributes['editor_newclass'] = "False"
        baseContainer.attributes['editor_constructor'] = "()"
        baseContainer.style['position'] = "absolute"
        baseContainer.style['overflow'] = "auto"
        baseContainer.style['left'] = "10px"
        baseContainer.style['top'] = "10px"
        baseContainer.style['margin'] = "0px"
        #baseContainer.style['border-style'] = "solid"
        baseContainer.style['width'] = "97%"
        baseContainer.style['height'] = "100%"
        baseContainer.style['display'] = "block"
        baseContainer.style['border-width'] = "1px"

        # The menuContainer on the left side
        menuContainer = Container()
        menuContainer.attributes['class'] = "Widget"
        menuContainer.attributes['editor_baseclass'] = "Widget"
        menuContainer.attributes['editor_varname'] = "menuContainer"
        menuContainer.attributes['editor_tag_type'] = "widget"
        menuContainer.attributes['editor_newclass'] = "False"
        menuContainer.attributes['editor_constructor'] = "()"
        menuContainer.style['position'] = "absolute"
        menuContainer.style['overflow'] = "auto"
        menuContainer.style['left'] = "10px"
        menuContainer.style['top'] = "10px"
        menuContainer.style['margin'] = "0px"
        #menuContainer.style['border-style'] = "solid"
        menuContainer.style['width'] = "98%"
        menuContainer.style['display'] = "block"
        menuContainer.style['border-width'] = "1px"
        menuContainer.style['height'] = "32px"
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m2 = gui.MenuItem('Zigbee Test', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m5 = gui.MenuItem('Config', width=100, height=30)
        m6 = gui.MenuItem('OTA Test', width=100, height=30)
        m7 = gui.MenuItem('Zigbee Dump', width=100, height=30)
        m8 = gui.MenuItem('LIVE', width=100, height=30)
        m9 = gui.MenuItem('STOP', width=100, height=30)
        m10 = gui.MenuItem('API', width=100, height=30)
        m11 = gui.MenuItem('API Test', width=100, height=30)
        m12 = gui.MenuItem('RPI Test', width=100, height=30)
        m1.set_on_click_listener(self.onclick_btnScreen1)
        m2.set_on_click_listener(self.onclick_btnScreen2)
        m3.set_on_click_listener(self.onclick_btnScreen8)
        m4.set_on_click_listener(self.onclick_btnScreen7)
        m5.set_on_click_listener(self.onclick_btnScreen5)
        m6.set_on_click_listener(self.onclick_btnScreen4)
        m7.set_on_click_listener(self.onclick_btnScreen3)
        m8.set_on_click_listener(self.onclick_btnScreen6)
        m9.set_on_click_listener(killBatch)
        menu.append(m1)
        menu.append(m2)
        menu.append(m3)
        menu.append(m4)
        menu.append(m5)
        menu.append(m6)
        menu.append(m7)
        menu.append(m8)
        menu.append(m9)
        menu.append(m10)
        menu.append(m11)
        menu.append(m12)
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.add_class('navbar navbar-expand-lg navbar-dark bg-dark')
        menubar.append(menu)
        menuContainer.append(menubar, 'btnScreen1')

        # Add the menuContainer to the baseContainer and define the listeners for the menu elements

        baseContainer.append(menuContainer, 'menuContainer')
        #baseContainer.children['menuContainer'].children['btnScreen2'].set_on_click_listener(self.onclick_btnScreen2)
        #baseContainer.children['menuContainer'].children['btnScreen1'].set_on_click_listener(self.onclick_btnScreen1)

        # The contentContainer
        contentContainer = Container()
        contentContainer.attributes['class'] = "Widget"
        contentContainer.attributes['editor_baseclass'] = "Widget"
        contentContainer.attributes['editor_varname'] = "contentContainer"
        contentContainer.attributes['editor_tag_type'] = "widget"
        contentContainer.attributes['editor_newclass'] = "False"
        contentContainer.attributes['editor_constructor'] = "()"
        contentContainer.style['position'] = "absolute"
        contentContainer.style['overflow'] = "auto"
        contentContainer.style['left'] = "10px"
        contentContainer.style['top'] = "70px"
        contentContainer.style['margin'] = "0px"
        contentContainer.style['border-style'] = "outset"
        contentContainer.style['width'] = "98%"
        contentContainer.style['display'] = "block"
        contentContainer.style['border-width'] = "2px"
        contentContainer.style['border-color'] = "#ededed"
        contentContainer.style['height'] = "98%"

        # Create top Level instances for the content Widgets.
        # By defining these as top Level the Widgets live even if they are not shown

        self.screen1 = screen1Widget()
        self.screen2 = screen2Widget()
        self.screen3 = screen3Widget()
        self.screen4 = screen4Widget()
        self.screen5 = screen5Widget()
        self.screen6 = screen6Widget()
        self.screen7 = screen7Widget()
        self.screen8 = screen8Widget()
        self.screens = {"screen1":self.screen1,"screen2":self.screen2,"screen3":self.screen3,"screen4":self.screen4,"screen5":self.screen5,"screen6":self.screen6,"screen7":self.screen7,"screen8":self.screen8}

        # Add the initial content to the contentContainer
        contentContainer.append(self.screen1, 'screen1')

        # Define the listeners for GUI elements which are contained in the content Widgets
        # We can't define it in the Widget classes because the listeners wouldn't have access to other GUI elements outside the Widget
        #self.screen2.children['btnsend'].set_on_click_listener(self.send_text_to_screen1)

        # Add the contentContainer to the baseContainer
        baseContainer.append(contentContainer, 'contentContainer')

        # Make the local "baseContainer" a class member of the App
        self.baseContainer = baseContainer

        # the 'id' param allows to have an alias in the url to refer to the widget that will manage the call
        self.lbl = RemoteLabel(
            'type in other page url "http://127.0.0.1:8082/label/api_set_text?value1=text1&value2=text2" !',
            width='80%', height='50%', id='api')
        # return the baseContainer as root Widget
        return self.baseContainer

        # Define the callbacks for the listeners

    def loadScreen(self,strScreen):
        if strScreen not in self.baseContainer.children['contentContainer'].children.keys():
            for oScreen in self.baseContainer.children['contentContainer'].children.keys():
                if 'screen' in oScreen:
                    self.baseContainer.children['contentContainer'].remove_child(
                        self.baseContainer.children['contentContainer'].children[oScreen])
                    break
        self.baseContainer.children['contentContainer'].append(self.screens[strScreen], strScreen)

    def onclick_btnScreen2(self, emitter):
        self.loadScreen('screen2')
        oStore.sessionName = "Zigbee"
        oStore.subContainerDevices.redraw()
        oStore.firmwareContainer.empty()
        oStore.firmwareContainer.redraw()
        oStore.listDetailsContainer.empty()
        oStore.listDetailsContainer.redraw()
        oStore.listDetails.empty()
        oStore.listDetails.redraw()
        oStore.subContainerDevicesInner.empty()
        oStore.subContainerDevicesInner.redraw()
        oStore.subContainerDevicesInnerConsole.empty()
        oStore.subContainerDevicesInnerConsole.redraw()
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        oStore.btnFirmwareLive.empty()
        oStore.listClusterContainer.empty()
        oStore.listAttrContainer.empty()
        oStore.subContainerVerticalLive.empty()
        oStore.consoleContainer.empty()
        oStore.consoleContainer.redraw()

    def onclick_btnScreen1(self, emitter):
        self.loadScreen('screen1')
        oStore.sessionName = "Home"
        oStore.consoleContainer.empty()
        oStore.consoleContainer.redraw()

    def onclick_btnScreen3(self, emitter):
        self.loadScreen('screen3')
        oStore.sessionName = "Dump"
        oStore.subContainerDevices.redraw()
        oStore.firmwareContainer.empty()
        oStore.firmwareContainer.redraw()
        oStore.listDetailsContainer.empty()
        oStore.listDetailsContainer.redraw()
        oStore.subContainerDevicesInner.empty()
        oStore.subContainerDevicesInner.redraw()
        oStore.subContainerDevicesInnerConsole.empty()
        oStore.subContainerDevicesInnerConsole.redraw()
        oStore.btnFirmwareZDump.empty()
        oStore.btnFirmwareZDump.redraw()
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        oStore.btnFirmwareLive.empty()
        oStore.listClusterContainer.empty()
        oStore.listAttrContainer.empty()
        oStore.subContainerVerticalLive.empty()
        oStore.consoleContainer.empty()
        oStore.consoleContainer.redraw()

    def onclick_btnScreen4(self, emitter):
        self.loadScreen('screen4')
        oStore.sessionName = "OTA"
        oStore.subContainerDevices.redraw()
        oStore.firmwareContainer.empty()
        oStore.firmwareContainer.redraw()
        oStore.listDetailsContainer.empty()
        oStore.listDetailsContainer.redraw()
        oStore.subContainerDevicesInner.empty()
        oStore.subContainerDevicesInner.redraw()
        oStore.subContainerDevicesInnerConsole.empty()
        oStore.subContainerDevicesInnerConsole.redraw()
        oStore.btnFirmwareZDump.empty()
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        oStore.btnFirmwareLive.empty()
        oStore.listClusterContainer.empty()
        oStore.listAttrContainer.empty()
        oStore.subContainerVerticalLive.empty()
        oStore.consoleContainer.empty()
        oStore.consoleContainer.redraw()

    def onclick_btnScreen5(self, emitter):
        self.loadScreen('screen5')
        oStore.sessionName = "Config"
        oStore.firmwareContainer.empty()
        oStore.firmwareContainer.redraw()
        oStore.listDetailsContainer.empty()
        oStore.listDetailsContainer.redraw()
        oStore.subContainerDevicesInner.empty()
        oStore.subContainerDevicesInner.redraw()
        oStore.subContainerDevicesInnerConsole.empty()
        oStore.subContainerDevicesInnerConsole.redraw()
        oStore.btnFirmwareZDump.empty()
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        oStore.btnFirmwareLive.empty()
        oStore.listClusterContainer.empty()
        oStore.listAttrContainer.empty()
        oStore.subContainerVerticalLive.empty()
        oStore.consoleContainer.empty()
        oStore.consoleContainer.redraw()
        #oStore.subContainerDevices.empty()

    def onclick_btnScreen6(self, emitter):
        self.loadScreen('screen6')
        oStore.sessionName = "Live"
        oStore.subContainerDevices.redraw()
        oStore.firmwareContainer.empty()
        oStore.firmwareContainer.redraw()
        oStore.listDetailsContainer.empty()
        oStore.listDetailsContainer.redraw()
        oStore.listDetailsContainer.append(oStore.btnFirmwareLive)
        oStore.subContainerDevicesInner.empty()
        oStore.subContainerDevicesInner.redraw()
        oStore.subContainerDevicesInnerConsole.empty()
        oStore.subContainerDevicesInnerConsole.redraw()
        oStore.btnFirmwareZDump.empty()
        oStore.consoleContainer.empty()
        oStore.consoleContainer.redraw()
        oStore.subContainerVerticalLive.empty()
        oStore.subContainerVerticalLive.redraw()
        oStore.subContainerDevicesInnerConsole.append(gui.Label('<div style="width: 100%;display: -webkit-inline-box">'))
        oStore.subContainerDevicesInnerConsole.append(
            gui.Label('<div class="card bg-info mb-3" style="width: 80%">'))
        oStore.subContainerDevicesInnerConsole.append(gui.Label('<div class="card-header"><h3 style="text-align:center;"> CONSOLE </h3></div>'))
        oStore.subContainerDevicesInnerConsole.append(oStore.consoleContainer)
        oStore.subContainerDevicesInnerConsole.append(oStore.txtFocus)
        oStore.subContainerDevicesInnerConsole.append(gui.Label('</div>'))
        oStore.subContainerDevicesInnerConsole.append(gui.Label('<div style="width: 15%">'))
        oStore.subContainerDevicesInnerConsole.append(oStore.subContainerVerticalLive)
        oStore.subContainerDevicesInnerConsole.append(gui.Label('</div></div>'))
        oStore.btnFirmwareLive.empty()
        oStore.listClusterContainer.empty()
        oStore.listAttrContainer.empty()
        self.tabless = gui.ListView(True).new_from_list(oStore.listOption, width='100%')
        self.tabless.add_class("list-group")
        self.tabless.set_on_selection_listener(on_table_row_click)
        self.tabless.style["position"] = "absolute"
        self.tabless.style["width"] = "15%"
        oStore.subContainerVerticalLive.append(gui.Label('<div>'))
        oStore.subContainerVerticalLive.append(self.tabless)
        oStore.subContainerVerticalLive.append(gui.Label('</div>'))

    def onclick_btnScreen7(self, emitter):
        self.loadScreen('screen7')
        oStore.sessionName = "latestresult"
        oStore.screenObject = self
        self.onclick_latestResults()

    def onclick_btnScreen8(self, emitter):
        self.loadScreen('screen8')
        oStore.sessionName = "latestresult"
        oStore.screenObject = self
        self.onclick_resultsfolder()

    def send_text_to_screen1(self, emitter):
        # Take the text of the TextBox in screen2 and put it into the TextBox in screen1
        self.screen1.children['mytextbox'].set_text(self.screen2.children['mytextbox'].get_text())

    def onclick_resultsfolder(self):
        oroot = None
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
            # print("path" + str(root))
            oroot = root
            break
        '''if platform.system() == "Windows":
            os.startfile(oroot + "/03_Results_Tier")
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", oroot + "/03_Results_Tier"])
        else:
            subprocess.Popen(["xdg-open", oroot + "/03_Results_Tier"])'''
        oStore.results.empty()
        host_name = socket.gethostname()
        oStore.results.append(gui.Label(
            "<iframe style='width:100%;height:1000px;' id='serviceFrameSend' src='http://" + oStore.ipAddr + ":8012/03_Results_Tier/'></iframe>"))

    def onclick_latestResults(self):
        oroot = None
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
            # print("path" + str(root))
            oroot = root
            break
        directory = oroot + "/03_Results_Tier"
        alist = {}
        now = time.time()
        directory = oroot + "/03_Results_Tier"
        os.chdir(directory)
        for file in os.listdir("."):
            if os.path.isdir(file):
                timestamp = os.path.getmtime(file)
                # get timestamp and directory name and store to dictionary
                alist[os.path.join(os.getcwd(), file)] = timestamp

        # sort the timestamp
        for i in sorted(alist.items(), key=operator.itemgetter(1), reverse=True):
            latest = "%s" % (i[0])
            break
        # latest=sorted(alist.iteritems(), key=operator.itemgetter(1))[-1]
        # print("newest directory is ", latest)
        os.chdir(latest)
        for root, dirs, files in os.walk(str(latest).replace(".DS_Store", "")):
            for file in files:
                if file.endswith('_Summary.HTML'):
                    #MyApp.execute_javascript(self, code="$('#result').load('/03_Results_Tier/"+latest.split("/")[len(latest.split("/"))-1]+"/"+file+"');")
                    oStore.results.empty()
                    host_name = socket.gethostname()
                    oStore.results.append(gui.Label("<iframe style='width:100%;height:1000px;' id='serviceFrameSend' src='http://"+oStore.ipAddr+":8012/03_Results_Tier/"+latest.split("/")[len(latest.split("/"))-1]+"/"+file+"'></iframe>"))
                    '''if platform.system() == "Windows":
                        os.startfile(file)
                    elif platform.system() == "Darwin":
                        subprocess.Popen(["open", file])
                    else:
                        subprocess.Popen(["xdg-open", file])'''

class RemoteLabel(gui.Label):
    def __init__(self, text, **kwargs):
        super(RemoteLabel, self).__init__(text, **kwargs)
        self.status = "Ready"
        self.temp = "None"
        self.oThread = None
        self.flag = False

    # api function
    def getNodes(self):
        #self.set_text('parameters: %s - %s' % (value1, value2))
        headers = {'Content-type': 'application/json'}

        return [json.dumps(dUtils.getZigbeeDevicesJson(), ensure_ascii=False), headers]

    def plugState(self,state,nodeId):
        utils.setSPOnOff(nodeId, state)
        headers = {'Content-type': 'text/plain'}
        return [str(nodeId) +" is set to "+ str(state), headers]

    def runTest(self,tagName):
        self.flag = False
        if 'DARWIN' in sys.platform.upper():
            self.OS = "MAC"
        elif 'LINUX' in sys.platform.upper():
            self.OS = "LINUX"
        elif sys.platform.startswith('win'):
            self.OS = "WINDOWS"
        oFileName = "Execute.command"
        if "WINDOWS" in sys.platform.upper():
            oFileName = "Execute_WIN.bat"
        if "LINUX" in sys.platform.upper():
            oFileName = "Execute.sh"
        temp = ''
        tempInner = ''
        self.status ="running"
        for root, dirs, files in os.walk(os.path.dirname(
                (os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
            for file in files:
                if file.endswith(oFileName):
                    if "WINDOWS" not in sys.platform.upper() and "LINUX" not in sys.platform.upper():
                        with open(root + "/" + file, 'w') as f:
                            f.write("#!/bin/sh \n")
                            f.write('cd "$(dirname ${BASH_SOURCE[0]})/../../01_BDD_Tier/features"\n')
                            f.write("behave --tags=" + tagName)
                    elif "WINDOWS" in sys.platform.upper():
                        with open(root + "/" + file, 'w') as f:
                            f.write('cd "%~dp0/../../01_BDD_Tier/features"\n')
                            f.write("behave --tags=" + tagName)
                    elif "LINUX" in sys.platform.upper():
                        with open(root + "/" + file, 'w') as f:
                            f.write("#!/bin/sh \n")
                            f.write('cd $(dirname "$0")/../../01_BDD_Tier/features\n')
                            f.write("behave --tags=" + tagName)
                    if "WINDOWS" in sys.platform.upper():
                        self.p = subprocess.Popen(root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                    else:
                        self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)

                    while True:
                        if self.flag:
                            print("\nstopped by API\n")
                            break
                        out = self.p.stdout.read(1)
                        if out == '' and self.p.poll() != None:
                            # MyApp.execute_javascript(self, code="document.getElementsByTagName('textarea')[0].focus();")
                            # MyApp.execute_javascript(self, code="alert('Done');")
                            self.status = "completed"
                            break
                        if out != '':
                            sys.stdout.write(out.decode('latin1'))
                            if '\n' in tempInner:
                                tempInner = ''
                            temp = temp + out.decode('latin1')
                            self.temp = temp
                            tempInner = tempInner + out.decode('latin1')
                            if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                                self.p.kill()
                                self.status = "completed"
                                break
                            sys.stdout.flush()
                    self.status = "completed"
                    print("\ncompleted\n")
                    break

    def stopRun(self):
        #self.oThread.join()
        self.flag = True
        headers = {'Content-type': 'text/plain'}
        return ["Stopped",headers]

    def testrun(self, tagName):
        self.status = "started"
        headers = {'Content-type': 'text/plain'}
        self.oThread = start_new_thread(target=self.runTest, args=(tagName,))
        self.flag = False
        self.oThread.setDaemon(True)
        self.oThread.start()
        self.OS = ""
        return [self.status,headers]

    def getTestCase(self, tagName):
        headers = {'Content-type': 'text/plain'}
        self.OS = ""
        if 'DARWIN' in platform.system().upper():
            self.OS = "MAC"
        elif 'LINUX' in platform.system().upper():
            self.OS = "LINUX"
        elif sys.platform.startswith('win'):
            self.OS = "WINDOWS"
        oFileName = "Execute.command"
        if "WINDOWS" in self.OS:
            oFileName = "Execute_WIN.bat"
        if "LINUX" in self.OS:
            oFileName = "Execute.sh"
        temp = ''
        tempInner = ''
        for root, dirs, files in os.walk(os.path.dirname(
                (os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
            for file in files:
                if file.endswith(oFileName):
                    if "WINDOWS" not in self.OS.upper() and "LINUX" not in self.OS.upper():
                        with open(root + "/" + file, 'w') as f:
                            f.write("#!/bin/sh \n")
                            f.write('cd "$(dirname ${BASH_SOURCE[0]})/../../01_BDD_Tier/features"\n')
                            f.write("behave --dry-run --tags=" + tagName)
                    elif "WINDOWS" in self.OS.upper():
                        with open(root + "/" + file, 'w') as f:
                            f.write('cd "%~dp0/../../01_BDD_Tier/features"\n')
                            f.write("behave --dry-run --tags=" + tagName)
                    elif "LINUX" in self.OS.upper():
                        with open(root + "/" + file, 'w') as f:
                            f.write("#!/bin/sh \n")
                            f.write('cd $(dirname "$0")/../../01_BDD_Tier/features\n')
                            f.write("behave --dry-run --tags=" + tagName)
                    if "WINDOWS" in self.OS.upper():
                        self.p = subprocess.Popen(root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                    else:
                        self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)

                    while True:
                        out = self.p.stdout.read(1)
                        if out == '' and self.p.poll() != None:
                            # MyApp.execute_javascript(self, code="document.getElementsByTagName('textarea')[0].focus();")
                            # MyApp.execute_javascript(self, code="alert('Done');")
                            break
                        if out != '':
                            sys.stdout.write(out.decode('latin1'))
                            if '\n' in tempInner:
                                tempInner = ''
                            temp = temp + out.decode('latin1')
                            tempInner = tempInner + out.decode('latin1')
                            if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                                self.p.kill()
                                break
                            sys.stdout.flush()
                    print("\ncompleted\n")
                    break
        return [temp,headers]

    def readTotalTestCase(self):
        jsonScenario = {}
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                             0] + "/01_BDD_Tier/features/"):
            for file in files:
                if file.endswith(".feature"):
                    jsonScenario[file] = {}
                    with open(root + "/" + file) as f:
                        lines = f.readlines()
                    strTag = ""
                    strText = ""
                    for line in lines:
                        if "@" in line:
                            if strText != "":
                                jsonScenario[file][strTag] = {}
                                jsonScenario[file][strTag] = strText
                                strText = ""
                                strTag = ''
                            for tag in line.split("@"):
                                if strTag != "":
                                    strTag = strTag + "_"
                                tag = str(tag).replace('  ', '')
                                if str(tag).strip() != "" and str(tag).strip() != "#":
                                    strTag = strTag + "@" + str(tag).strip()
                        elif strTag != "" and not line.startswith("#"):
                            strText = strText + str(line)
                    if strText != "":
                        jsonScenario[file][strTag] = {}
                        jsonScenario[file][strTag] = strText
                        strText = ""
                        strTag = ''
        return json.dumps(OrderedDict(sorted(jsonScenario.items(), key=lambda t: t[0])), ensure_ascii=False)

    def totalTestCase(self):
        headers = {'Content-type': 'application/json'}
        try:
            val = self.readTotalTestCase()
            return [val, headers]
            #return [json.dumps(jsonScenario, ensure_ascii=False),headers]
        except Exception as e:
            headers = {'Content-type': 'text/plain'}
            return [str(e),headers]

    def getStatus(self):
        headers = {'Content-type': 'text/plain'}
        return [self.status,headers]

    def getLog(self):
        headers = {'Content-type': 'text/plain'}
        return [self.temp, headers]

    def setFastPoll(self, nodeid, ep):
        headers = {'Content-type': 'text/plain'}
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
        longPollInt, checkInInt = AT.setCompletFastPoll(nodeid,ep,True)
        AT.stopThreads()
        if longPollInt is None and checkInInt is None:
            return ["fast poll setting failed",headers]
        else:
            return ["fast poll setting successful",headers]

if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    #start(MyApp, debug=False, standalone=True)
    oStore = variables()

    if "LINUX" in sys.platform.upper():
        start(MyApp, debug=False, address='0.0.0.0', port=8080, websocket_port=8082, update_interval=0.5, multiple_instance=True)
    else:
        # start(MyApp, debug=False, address='0.0.0.0', port=8080, websocket_port=8082, update_interval=0.5, multiple_instance=True)
        start(MyApp, debug=False, address='0.0.0.0', port=1000, update_interval=0.5, multiple_instance=True)