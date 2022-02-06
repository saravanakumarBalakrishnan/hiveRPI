import remi.gui as gui
import sys
sys.path.append("01_BDD_Tier/features/steps")
sys.path.append("01_BDD_Tier/features/steps/PageObjects")
sys.path.append("01_BDD_Tier/features/steps/Locators")
sys.path.append("01_BDD_Tier/features/steps/Function_Libraries")
from remi import start, App
import FF_device_utils as dUtils
import os
import platform
import subprocess
import FF_threadedSerial as AT
import re
import operator
import time
import threading
from threading import Thread as start_new_thread
import FF_utils as utils
import json
import ctypes
import FF_zigbeeToolsConfig as config
import sys
import queue
import serial
import time
import datetime
import json
import FF_zigbeeClusters as zcl
import FF_alertmeApi as apiUtils
import requests
import urllib.request
from collections import OrderedDict

class MyApp(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(__file__), 'res')
        super(MyApp, self).__init__(*args, static_file_path=res_path)
        self.flag = False

    envDict = {"Internal Prod":"isopInternProd","Beta":"isopBeta","Staging":"isopStaging","Production":"isopProd","USBeta":"isopBetaUS"}
    def main(self):

        self.OS = ""
        if 'DARWIN' in platform.system().upper():
            self.OS = "MAC"
        elif 'LINUX' in platform.system().upper():
            self.OS = "LINUX"
        elif sys.platform.startswith('win'):
            self.OS = "WINDOWS"
        verticalContainer = gui.Widget(width='90%', margin='0px auto')  # the margin 0px auto centers the main container
        verticalContainer.style['display'] = 'block'
        verticalContainer.style['overflow'] = 'hidden'
        horizontalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        horizontalContainer.style['display'] = 'block'
        horizontalContainer.style['overflow'] = 'auto'
        self.listDetails = gui.ListView(True)
        self.p = None
        self.upgradeVersion = gui.TextInput(width='100px')
        self.DowngradeVersion = gui.TextInput(width='100px')
        subContainerLeft = gui.Widget(width=320)
        subContainerLeft.style['display'] = 'block'
        subContainerLeft.style['overflow'] = 'auto'
        subContainerLeft.style['text-align'] = 'center'
        self.img = gui.Image('/res/hive.png', width=100, height=100, margin='10px')
        # self.img.style['background-image'] = "url('/res/FWLogo.png')"
        subContainerLeft.append(self.img)
        self.consoleContainer = gui.Widget(width='100%')
        self.consoleContainer.style['background-color'] = 'rgb(211, 211, 211)'
        self.subContainerRight = gui.Widget(width='70%')
        self.subContainerRightRPI = gui.Widget(width='70%')
        self.ReadFeatureFile(subContainerLeft)
        self.subContainerDevices = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                              margin='0px')
        self.subContainerDevicesOTA = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                 margin='0px')
        self.subContainerDevicesZDump = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                 margin='0px')
        self.subContainerDevicesRPI = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                   margin='0px')
        self.subContainerDevicesLive = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                 margin='0px')
        self.subContainerVerticalLive = gui.Widget(width='15%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                 margin='0px')
        self.subContainerfirmwareOTA = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                  margin='0px')
        self.subContainerfirmwareZDump = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                  margin='0px')
        self.subContainerfirmwareLive = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                  margin='0px')
        self.subContainerDevicesAPI = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                 margin='0px')
        self.subContainerDevicesAPITest = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                 margin='0px')
        self.lblFirmwareOTA = gui.Label("Firmware Path", width='10%')
        self.txtFirmwarePath = gui.TextInput(True, width='70%')
        self.lblValidationOTA = gui.Label("Current Device Firmware", width='50%')
        self.txtValidationOTA = gui.Label("firmware version", width='50%')
        self.btnChangeFirmwareOTA = gui.Button("Browse", width='20%')
        self.btnChangeFirmwareOTA.set_on_click_listener(self.changeFirmwarePathOTA)
        self.btnFirmwareOTA = gui.Button("Start", width='20%')
        self.btnFirmwareOTA.set_on_click_listener(self.FirmwareOTA)

        self.btnFirmwareZDump = gui.Button("Start", width='20%')
        self.btnFirmwareZDump.set_on_click_listener(self.deviceZigbeeDump)
        self.btnFirmwareLive = gui.Button("Start", width='20%')
        self.btnFirmwareLive.set_on_click_listener(self.live)
        
        self.subContainerDevicesOTA.append(self.lblValidationOTA)
        self.subContainerDevicesOTA.append(self.txtValidationOTA)
        self.subContainerDevicesOTA.append(self.lblFirmwareOTA)
        self.subContainerDevicesOTA.append(self.txtFirmwarePath)
        self.subContainerDevicesOTA.append(self.btnChangeFirmwareOTA)
        self.subContainerDevicesOTA.append(self.btnFirmwareOTA)
        self.subContainerDumpZDump = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                margin='0px')
        self.subContainerDumpRPI = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                margin='0px')
        self.subContainerDumpLive = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                margin='0px')
        self.distributedExecution = gui.CheckBoxLabel("  Distributed Execution", False, user_data="Distributed", width="100%",
                                                      height="30px")
        self.subContainerDevicesZDump.append(self.btnFirmwareZDump)
        self.subContainerDevicesLive.append(self.btnFirmwareLive)
        self.subContainerDevicesInner = gui.Widget(width='100%')
        self.subContainerDevicesInnerOTA = gui.Widget(width='100%')
        self.subContainerDevicesInnerZDump = gui.Widget(width='100%')
        self.subContainerDevicesInnerRPI = gui.Widget(width='100%',layout_orientation=gui.Widget.LAYOUT_HORIZONTAL)
        self.subContainerDevicesInnerLive = gui.Widget(width='100%')
        self.subContainerDevicesInnerConsoleLive = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL)
        self.subContainerDevicesInnerConsole = gui.Widget(width='80%')
        self.subContainerDevicesInnerConsole.style['background-color'] = 'rgb(211, 211, 211)'
        self.subContainerDevicesInnerConsoleRPI = gui.Widget(width='100%',layout_orientation=gui.Widget.LAYOUT_HORIZONTAL)
        self.firmwareContainer = gui.Widget(width='20%')
        self.firmwareContainerOTA = gui.Widget(width='20%')
        self.firmwareContainerZDump = gui.Widget(width='20%')
        self.firmwareContainerLive = gui.Widget(width='20%')
        # self.subContainerDevicesInner.style['border'] = '1px solid #9C9B9B'
        self.horizontalContainerDialog = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.horizontalContainerDialogOTA = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                       margin='0px')
        self.horizontalContainerDialogZDump = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                       margin='0px')
        self.horizontalContainerDialogRPI = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                         margin='0px')
        self.horizontalContainerDialogLive = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                       margin='0px')
        self.listDetailsContainer = gui.Widget(width='30%')
        self.TopDetailsContainer = gui.Widget(width='30%')
        self.DevDetailsContainer = gui.Widget(width='20%')
        self.listDetailsContainerOTA = gui.Widget(width='30%')
        self.TopDetailsContainerOTA = gui.Widget(width='30%')
        self.DevDetailsContainerOTA = gui.Widget(width='20%')
        self.listDetailsContainerZDump = gui.Widget(width='30%')
        self.TopDetailsContainerZDump = gui.Widget(width='30%')
        self.DevDetailsContainerZDump = gui.Widget(width='20%')
        self.listDetailsContainerRPI = gui.Widget(width='30%')
        self.TopDetailsContainerRPI = gui.Widget(width='30%')
        self.DevDetailsContainerRPI = gui.Widget(width='20%')
        self.listDetailsContainerLive = gui.Widget(width='30%')
        self.listClusterContainerLive = gui.Widget(width='30%')
        self.listAttrContainerLive = gui.Widget(width='30%')
        self.listAttrContainerRepoLive = gui.Widget(width='100%')
        self.TopDetailsContainerLive = gui.Widget(width='30%')
        self.DevDetailsContainerLive = gui.Widget(width='20%')
        self.horizontalContainerDialog.style['display'] = 'block'
        self.horizontalContainerDialog.style['overflow'] = 'auto'
        horizontalContainer.append(subContainerLeft)
        self.dialog = gui.GenericDialog(title='Dialog Box',
                                        width='90%')
        self.oThread = None
        horizontalContainer.append(self.subContainerRight)
        self.dtextinput = gui.TextInput(width=200, height=30)
        self.dtextUserName = gui.TextInput(width=400, height=30)
        self.dtextHubId = gui.TextInput(width=400, height=30)
        self.dtextPassword = gui.TextInput(width=400, height=30)
        self.firmwareFolderPath = gui.TextInput(width=200, height=30)
        self.dialog = gui.GenericDialog(title='Zigbee Test', width='90%')
        self.OTAdialog = gui.GenericDialog(title='OTA Test', width='90%')
        self.zDumpdialog = gui.GenericDialog(title='Zigbee Dump', width='90%')
        self.rpiDialog = gui.GenericDialog(title='RPI Test Execution', width='90%')
        self.liveDialog = gui.GenericDialog(title='Live', width='90%')
        self.configDialog = gui.GenericDialog(title='Configuration', width='90%')
        self.apiDialog = gui.GenericDialog(title='API', width='90%')
        self.apiTestDialog = gui.GenericDialog(title='API Test', width='90%')
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
        m1.set_on_click_listener(self.homePage)
        m2.set_on_click_listener(self.menu_dialog_clicked)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m5.set_on_click_listener(self.open_Config)
        m6.set_on_click_listener(self.open_OTA)
        m7.set_on_click_listener(self.open_ZigbeeDump)
        m8.set_on_click_listener(self.open_Terminal)
        m9.set_on_click_listener(self.killBatch)
        m10.set_on_click_listener(self.open_API)
        m11.set_on_click_listener(self.open_API_Test)
        m12.set_on_click_listener(self.open_rpiTest)
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
        menubar.append(menu)

        verticalContainer.append(menubar)

        verticalContainer.append(horizontalContainer)
        self.menubarConfig = gui.MenuBar(width='100%', height='30px')
        self.menubarAPI = gui.MenuBar(width='100%', height='30px')
        self.menubarAPITest = gui.MenuBar(width='100%', height='30px')
        self.subConfig = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='10px')
        self.configDialog.append(self.menubarConfig)
        #self.apiDialog.append(self.menubarAPI)
        self.lblFirmware = gui.Label("Firmware Path", width='10%')
        self.txtFirmware = gui.TextInput(True, width='70%')
        self.lblValidation = gui.Label("Validation Type", width='10%')
        self.drpValidation = gui.DropDown(width='70%')
        self.drpValidation.append("Zigbee API")
        self.drpValidation.append("Platform API")
        self.drpValidation.append("Factory API")
        self.envValidation = gui.DropDown(width='70%')
        self.envValidation.append("Select")
        self.envValidation.append("Internal Prod")
        self.envValidation.append("Beta")
        self.envValidation.append("Staging")
        self.envValidation.append("Production")
        self.envValidation.append("USBeta")
        self.envTestValidation = gui.DropDown(width='70%')
        self.envTestValidation.append("Select")
        self.envTestValidation.append("Internal Prod")
        self.envTestValidation.append("USBeta")
        self.envTestValidation.append("Staging")
        self.envTestValidation.append("Production")
        self.btnChangeFirmware = gui.Button("Change Path", width='20%')
        self.btnChangeFirmware.set_on_click_listener(self.changeFirmwarePath)
        self.subConfig.append(self.lblFirmware)
        self.subConfig.append(self.txtFirmware)
        self.subConfig.append(self.btnChangeFirmware)
        self.subConfig.append(self.lblValidation)
        self.subConfig.append(self.drpValidation)
        self.subConfigTop = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='10px')
        self.btnSave = gui.Button("Save", width='100px')
        self.btnSave.set_on_click_listener(self.saveConfig)
        self.subConfigTop.append(self.btnSave)
        # self.configDialog.append(self.subConfigTop)
        self.configDialog.append(self.subConfig)
        # self.configDialog.add_field_with_label('firmwareFolderPath', 'Firmware Path', self.txtFirmware)
        self.subContainerConfig = gui.Widget(width='100%')
        self.subContainerConfigLibraries = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                      margin='10px')
        self.subContainerConfigLibraries.style['display'] = 'block'
        self.subContainerConfigLibraries.style['overflow'] = 'auto'
        self.subContainerConfigLibrariesList = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                          margin='10px')
        self.txtInstalled = gui.Label("Installed Libraries", width='20%')
        self.txtUnInstalled = gui.Label("Missing Libraries", width='20%')
        self.txtInstallConsole = gui.Label("Console", width='60%')
        self.subContainerConfigLibrariesList.append(self.txtInstalled)
        self.subContainerConfigLibrariesList.append(self.txtUnInstalled)
        self.subContainerConfigLibrariesList.append(self.txtInstallConsole)
        self.btnInstall = gui.Button("Check / Fix Libraries")
        self.btnInstall.set_on_click_listener(self.installLibraries)
        self.listInstalled = gui.ListView(True, width='20%')
        self.listInstalled.append("List of Libraries")
        self.listInstalled.style['background-color'] = 'rgb(107, 201, 78)'
        self.subContainerConfigLibrariesList.append(self.listInstalled)
        self.listNotInstalled = gui.ListView(True, width='20%')
        self.listNotInstalled.append("List of Libraries")
        self.listNotInstalled.style['background-color'] = 'rgb(209, 50, 50)'
        self.subContainerConfigLibrariesList.append(self.listNotInstalled)
        self.subContainerConfigLibrariesConsole = gui.Widget(width='60%')
        self.subContainerConfigLibrariesConsole.style['background-color'] = 'rgb(211, 211, 211)'
        self.subContainerConfigLibrariesList.append(self.subContainerConfigLibrariesConsole)
        self.subContainerConfigLibraries.append(self.subConfigTop)
        self.subContainerConfigLibraries.append(self.btnInstall)
        self.subContainerConfigLibraries.append(self.subContainerConfigLibrariesList)
        self.subContainerConfig.append(self.subContainerConfigLibraries)
        self.configDialog.append(self.subContainerConfig, "container")
        wid = gui.VBox()
        '''self.oThread = start_new_thread(target=self.getRPIStatusThread)
        self.oThread.setDaemon(True)
        self.oThread.start()'''

        # the 'id' param allows to have an alias in the url to refer to the widget that will manage the call
        self.lbl = RemoteLabel(
            'type in other page url "http://127.0.0.1:8082/label/api_set_text?value1=text1&value2=text2" !',
            width='80%', height='50%', id='api')
        self.lbl.style['margin'] = 'auto'

        # appending a widget to another, the first argument is a string key
        wid.append(self.lbl)


        # returning the root widget
        return verticalContainer

    def FirmwareOTA(self, widget):
        MacAddress = ""
        for i in range(0, 4):
            temp = self.listDetailsOTA.children[list(self.listDetailsOTA.children)[i]].children['text'].replace("\'",
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
                os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
            for file in files:
                if file.endswith('firmwareUpgrade.py'):
                    with open(root + "/" + file,'r') as f:
                        self.lines = f.readlines()
                    with open(root + "/" + file, 'w') as f:
                        f.seek(0)
                        f.truncate()
                        intCounter = 0
                        for bline in self.lines:
                            line = bline
                            if "imageFile = " in line:
                                line = "imageFile = '" + self.txtFirmwarePath.get_text() + "'\n"
                                self.lines[intCounter] = line
                            if "nodeId = " in line:
                                line = "nodeId = '" + nodeid + "'\n"
                                self.lines[intCounter] = line
                            if "ep = " in line:
                                line = "ep = '" + ep + "'\n"
                                self.lines[intCounter] = line
                            if "zbType = " in line:
                                line = "zbType = '" + zbtype + "'\n"
                                self.lines[intCounter] = line
                            intCounter = intCounter + 1
                        f.writelines(self.lines)
                        f.close()
        try:
            try:
                self.p.terminate()
                self.p.kill()
            except:
                pass
            self.killBatch()
            self.oThread = start_new_thread(target=self.OTAupgrade)
            self.oThread.setDaemon(True)
            self.flag = False
            self.oThread.start()
        except:
            pass

    def OTAupgrade(self):
        self.subContainerDevicesInnerConsole.empty()
        self.subContainerDevicesInnerConsole.redraw()
        lbl2 = gui.Label("0%", width='100%', height='45px')
        lbl2.style['color'] = 'rgb(48, 141, 255)'
        lbl2.style['background-color'] = 'rgb(255, 255, 255)'
        lbl2.style['font-size'] = '36px'
        lbl2.style['font-weight'] = 'bold'
        self.subContainerDevicesInnerConsole.append(lbl2)
        # self.consoleText = gui.TextInput(single_line=False, width='100%', height='1000px')
        # self.subContainerDevicesInnerConsole.append(self.consoleText)
        # self.consoleText.set_text("")
        act = 0
        oFileName = "firmwareUpgrade.command"
        if "WINDOWS" in self.OS:
            oFileName = "firmwareUpgrade.bat"
        if "LINUX" in self.OS:
            oFileName = "firmwareUpgrade.sh"
        intCtr = 0
        for root, dirs, files in os.walk(
                os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
            for file in files:

                if file.endswith(oFileName):
                    try:
                        if "WINDOWS" in self.OS:
                            self.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        else:
                            self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        temp = ''
                        tempInner = ''
                        tempInnerGroup = ''
                        while True:
                            if self.flag:
                                print("\nstopped by API\n")
                                break
                            out = self.p.stdout.read(1)
                            if str(out) == 'b\'\'' and self.p.poll() != None:
                                break
                            if out != '':
                                sys.stdout.write(out.decode('utf-8'))

                                if '\n' in tempInner:
                                    if intCtr % 200 == 0:
                                        lbl = gui.TextInput(single_line=False, width='100%', height='100%')
                                        lbl.set_text(tempInnerGroup + "\n")
                                        lbl.style['font-size'] = '10px'
                                        self.subContainerDevicesInnerConsole.append(lbl)
                                        tempInnerGroup = ''
                                    else:
                                        if " ---- " not in tempInner:
                                            tempInnerGroup = tempInnerGroup + "\n" + tempInner
                                        if "DONE" in tempInner.upper():
                                            lbl = gui.TextInput(single_line=False, width='100%')
                                            lbl.set_text(tempInnerGroup + "\n")
                                            lbl.style['font-size'] = '10px'
                                            self.subContainerDevicesInnerConsole.append(lbl)

                                    if (" ---- " in tempInner):
                                        # self.consoleText.set_text(temp)
                                        Max = int(tempInner.split(" ---- ")[0])
                                        act = act + int(tempInner.split(" ---- ")[1])
                                        val = (act / Max) * 100
                                        lbl2.set_text(str(round(val, 2)) + "% ||||||||||| " + str(act) + " / " + str(
                                            Max) + " |||||||||||  *" + (tempInner.split(" ---- ")[1]) + " block size")

                                        # lbl2.redraw()
                                    # if ("ERROR" in tempInner.upper() or "NACK" in tempInner.upper() or "**** PROBLEM" in tempInner.upper()):
                                    #    lbl2.style['color'] = 'rgb(99, 7, 7)'
                                    #    lbl2.style['font-size'] = '12px'
                                    tempInner = ''
                                    intCtr = intCtr + 1
                                temp = temp + out.decode('utf-8')
                                tempInner = tempInner + out.decode('utf-8')
                                if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                                    self.p.kill()
                                    break
                                sys.stdout.flush()

                        print("\ncompleted\n")
                        MyApp.execute_javascript(self, code="alert('Completed');")
                        break
                    except:
                        self.killBatch()

    def deviceZigbeeDump(self, widget):
        MacAddress = ""
        for i in range(0, 4):
            temp = self.listDetailsZDump.children[list(self.listDetailsZDump.children)[i]].children['text'].replace("\'",
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
                        self.lines = f.readlines()
                    with open(root + "/" + file, 'w') as f:
                        f.seek(0)
                        f.truncate()
                        intCounter = 0
                        for bline in self.lines:
                            line = bline
                            if "NODE_ID = " in line:
                                line = "NODE_ID = '" + nodeid + "'\n"
                                self.lines[intCounter] = line
                            if "EP_ID = " in line:
                                line = "EP_ID = '" + ep + "'\n"
                                self.lines[intCounter] = line
                            intCounter = intCounter + 1
                        f.writelines(self.lines)
                        f.close()
        os.walk(
            os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0])

        try:
            try:
                self.p.terminate()
                self.p.kill()
            except:
                pass
            self.killBatch()
            self.oThread = start_new_thread(target=self.ZDump)
            self.flag = False
            self.oThread.setDaemon(True)
            self.oThread.start()
        except:
            pass

    def ZDump(self):
        self.subContainerDevicesInnerConsole.empty()
        self.subContainerDevicesInnerConsole.redraw()
        self.subContainerDumpZDump.empty()
        self.subContainerDumpZDump.redraw()
        act = 0
        oFileName = "zDump.command"
        if "WINDOWS" in self.OS:
            oFileName = "zDump.bat"
        if "LINUX" in self.OS:
            oFileName = "zDump.sh"

        intCtr = 0
        lst = []
        for root, dirs, files in os.walk(
                os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
            for file in files:

                if file.endswith(oFileName):
                    try:
                        if "WINDOWS" in self.OS:
                            self.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        else:
                            self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        temp = ''
                        tempInner = ''
                        tempInnerGroup = ''
                        flag = False
                        while True:
                            if self.flag:
                                print("\nstopped by API\n")
                                break
                            out = self.p.stdout.read(1)
                            if str(out) == 'b\'\'' and self.p.poll() != None:
                                self.table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                self.subContainerDumpZDump.append(self.table)
                                break
                            if out != '':
                                sys.stdout.write(out.decode('utf-8'))
                                # self.consoleText.set_text(temp)
                                if '\n' in tempInner:
                                    if 'Cluster' in tempInner and 'InCluster' not in tempInner:
                                        flag = True
                                    if flag:
                                        if 'Endpoint=' in tempInner and ', Endpoint=' not in tempInner:
                                            if len(lst) > 0:
                                                if len(lst) == 1:
                                                    if any("Attribute Id" not in s for s in lst):
                                                        self.table = gui.Table.new_from_list(lst, width='100%',
                                                                                             margin='10px')
                                                        self.subContainerDumpZDump.append(self.table)
                                                else:

                                                    self.table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                                    self.table.style['background-color'] = 'rgb(91,91,91)'
                                                    self.subContainerDumpZDump.append(self.table)
                                            lst = []
                                            lst.append([tempInner.split(',')[0], tempInner.split(',')[1],
                                                        tempInner.split(',')[2], tempInner.split(',')[3]])

                                            self.table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                            self.subContainerDumpZDump.append(self.table)
                                            lst = []

                                        else:

                                            if len(lst) == 0:
                                                if ',' in tempInner:
                                                    lst.append(['Attribute Id', 'Attribute Type', 'Attribute Name',
                                                                'Attribute Value', 'Reporting configuration'])
                                            if len(tempInner.split(',')) == 4:
                                                lst.append([tempInner.split(',')[0],tempInner.split(',')[1],tempInner.split(',')[2],tempInner.split(',')[3]])
                                            if len(tempInner.split(',')) > 4:
                                                strRem = ""
                                                for i in range(4,len(tempInner.split(','))):
                                                    strRem = strRem + tempInner.split(',')[i]
                                                lst.append([tempInner.split(',')[0], tempInner.split(',')[1],
                                                            tempInner.split(',')[2], tempInner.split(',')[3],strRem])
                                    lbl = gui.Label(tempInner, width='100%')
                                    lbl.style['font-size'] = '10px'
                                    self.subContainerDevicesInnerConsole.append(lbl)
                                    tempInner = ''
                                temp = temp + out.decode('utf-8')
                                tempInner = tempInner + out.decode('utf-8')
                                if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                                    self.p.kill()
                                    self.table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                    self.subContainerDumpZDump.append(self.table)
                                    break
                                sys.stdout.flush()

                        print("\ncompleted\n")
                        MyApp.execute_javascript(self, code="alert('Completed');")
                        break
                    except:
                        self.killBatch()

    def live(self, widget):
        if len(self.DevDetailsContainerLive.children) == 0:
            MyApp.execute_javascript(self, code="alert('Click on Get Devices Connected to continue');")
            return
        if self.DevDetailsContainerLive.children[
                list(self.DevDetailsContainerLive.children.keys())[0]]._selected_item is None:
            MyApp.execute_javascript(self, code="alert('Click on any device to continue');")
            return
        if 'Stop' in self.btnFirmwareLive.get_text():
            AT.stopThreads()
            self.btnFirmwareLive.set_text("Start")
            return
        MacAddress = ""
        for i in range(0, 4):
            temp = self.listDetailsLive.children[list(self.listDetailsLive.children)[i]].children['text'].replace("\'",
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
        if len(list(nodes['endPoints'])) > 0:
            ep = str(list(nodes['endPoints'])[0])
        zbtype = nodes['type']

        try:
            try:
                self.p.terminate()
                self.p.kill()
            except:
                pass
            #self.killBatch()
            #time.sleep(5)
        except:
            pass
        try:
            self.consoleContainer.empty()
            AT.startSerialThreads(config.PORT,config.BAUD,True,True,False)
            self.btnFirmwareLive.set_text("Stop")
            lbl = gui.Label("Start")
            self.consoleContainer.append(lbl)
            #AT.txQueue = self.txQueue
            #AT.rxQueue = self.rxQueue
            AT.UIObj = self
            AT.UIgui = gui;
        except:
            AT.stopThreads()

    def zlive(self):
        self.subContainerDevicesInnerConsole.empty()
        self.subContainerDevicesInnerConsole.redraw()
        self.subContainerDumpLive.empty()
        self.subContainerDumpLive.redraw()
        act = 0
        oFileName = "Live.command"
        if "WINDOWS" in self.OS:
            oFileName = "Live.bat"
        if "LINUX" in self.OS:
            oFileName = "Live.sh"

        intCtr = 0
        lst = []
        for root, dirs, files in os.walk(
                os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
            for file in files:

                if file.endswith(oFileName):
                    try:
                        if "WINDOWS" in self.OS:
                            self.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        else:
                            self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        temp = ''
                        tempInner = ''
                        tempInnerGroup = ''
                        flag = False
                        while True:
                            if self.flag:
                                print("\nstopped by API\n")
                                break
                            out = self.p.stdout.read(1)
                            if str(out) == 'b\'\'' and self.p.poll() != None:
                                self.table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                self.subContainerDumpLive.append(self.table)
                                break
                            if out != '':
                                sys.stdout.write(out.decode('utf-8'))
                                # self.consoleText.set_text(temp)
                                if '\n' in tempInner:
                                    if 'Cluster' in tempInner:
                                        flag = True
                                    if flag:
                                        if 'Endpoint=' in tempInner:
                                            if len(lst) > 0:
                                                if len(lst) == 1:
                                                    if 'Attribute Id' not in lst[0]:
                                                        self.table = gui.Table.new_from_list(lst, width='100%',
                                                                                             margin='10px')
                                                        self.subContainerDumpLive.append(self.table)
                                                else:
                                                    self.table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                                    self.subContainerDumpLive.append(self.table)
                                            lst = []
                                            lst.append([tempInner.split(',')[0], tempInner.split(',')[1],
                                                        tempInner.split(',')[2], tempInner.split(',')[3]])
                                            self.table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                            self.subContainerDumpLive.append(self.table)
                                            lst = []

                                        else:

                                            if len(lst) == 0:
                                                if ',' in tempInner:
                                                    lst.append(['Attribute Id', 'Attribute Type', 'Attribute Name',
                                                                'Attribute Value', 'Reporting configuration'])
                                            if len(tempInner.split(',')) == 4:
                                                lst.append([tempInner.split(',')[0],tempInner.split(',')[1],tempInner.split(',')[2],tempInner.split(',')[3]])
                                            if len(tempInner.split(',')) > 4:
                                                strRem = ""
                                                for i in range(4,len(tempInner.split(','))):
                                                    strRem = strRem + tempInner.split(',')[i]
                                                lst.append([tempInner.split(',')[0], tempInner.split(',')[1],
                                                            tempInner.split(',')[2], tempInner.split(',')[3],strRem])
                                    lbl = gui.Label(tempInner, width='100%')
                                    lbl.style['font-size'] = '10px'
                                    self.subContainerDevicesInnerConsole.append(lbl)
                                    tempInner = ''
                                temp = temp + out.decode('utf-8')
                                tempInner = tempInner + out.decode('utf-8')
                                if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                                    self.p.kill()
                                    self.table = gui.Table.new_from_list(lst, width='100%', margin='10px')
                                    self.subContainerDumpLive.append(self.table)
                                    break
                                sys.stdout.flush()

                        print("\ncompleted\n")
                        break
                    except:
                        self.killBatch()

    def on_fileselection_dialog_confirm(self, widget, filelist):
        # a list() of filenames and folders is returned
        self.txtFirmware.set_text(dict(widget.fileFolderNavigator.pathEditor.children)["text"])

    def on_fileselection_dialog_confirmOTA(self, widget, filelist):
        # a list() of filenames and folders is returned
        self.txtFirmwarePath.set_text(str(filelist[0]))

    def changeFirmwarePath(self, widget):
        if os.path.exists(self.getFirmwarePath(self.OS)):
            self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', True,
                                                               self.getFirmwarePath(self.OS), False,
                                                               allow_folder_selection=True)
        else:
            self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', True,
                                                               os.path.abspath(os.path.curdir), False,
                                                               allow_folder_selection=True)
        self.fileselectionDialog.set_on_confirm_value_listener(
            self.on_fileselection_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialog.show(self)

    def changeFirmwarePathOTA(self, widget):
        if os.path.exists(self.getFirmwarePath(self.OS)):
            self.fileselectionDialogOTA = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders',
                                                                  False,
                                                                  self.getFirmwarePath(self.OS), allow_file_selection=True,
                                                                  allow_folder_selection=False)
        else:
            self.fileselectionDialogOTA = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders',
                                                                  False,
                                                               os.path.abspath(os.path.curdir), allow_file_selection=True,
                                                                  allow_folder_selection=False)
        self.fileselectionDialogOTA.set_on_confirm_value_listener(
            self.on_fileselection_dialog_confirmOTA)

        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialogOTA.show(self)

    def saveConfig(self, widget):
        for root, dirs, files in os.walk(
                os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
            for file in files:
                if file.endswith('FF_zigbeeToolsConfig.py'):
                    with open(root + "/" + file) as f:
                        self.lines = f.readlines()
                    with open(root + "/" + file, 'w') as f:
                        f.seek(0)
                        f.truncate()
                        intCounter = 0
                        for line in self.lines:
                            if "FIRMWARE_ROOT_FILE_PATH = " in line:
                                if self.txtFirmware.get_text().endswith("/\n"):
                                    line = "FIRMWARE_ROOT_FILE_PATH = '" + self.txtFirmware.get_text().replace("/\n",
                                                                                                               "") + "/'\n"
                                else:
                                    line = "FIRMWARE_ROOT_FILE_PATH = '" + self.txtFirmware.get_text().replace("\n",
                                                                                                               "") + "/'\n"
                                self.lines[intCounter] = line
                            intCounter = intCounter + 1
                        f.writelines(self.lines)
                        f.close()
        utils.setAttribute('common', 'apiValidationType', self.drpValidation.get_value())

    def open_Config(self, widget):
        self.homePageNavaigation()
        strJson = open(utils.strGlobVarFilePath, mode='r')
        utils.oJsonDict = json.loads(strJson.read())
        strJson.close()
        strAPIValidationType = utils.getAttribute('common', 'apiValidationType')
        self.drpValidation.set_value(strAPIValidationType)
        # self.firmwareFolderPath.set_value('')
        #   self.configDialog.add_field_with_label('firmwareFolderPath', 'Firmware Path', self.txtFirmware)
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m2 = gui.MenuItem('Zigbee Test', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m6 = gui.MenuItem('OTA Test', width=100, height=30)
        m7 = gui.MenuItem('Zigbee Dump', width=100, height=30)
        m8 = gui.MenuItem('LIVE', width=100, height=30)
        m9 = gui.MenuItem('STOP', width=100, height=30)
        m10 = gui.MenuItem('API', width=100, height=30)
        m11 = gui.MenuItem('API Test', width=100, height=30)
        m1.set_on_click_listener(self.homePage)
        m2.set_on_click_listener(self.menu_dialog_clicked)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m6.set_on_click_listener(self.open_OTA)
        m7.set_on_click_listener(self.open_ZigbeeDump)
        m9.set_on_click_listener(self.killBatch)
        m8.set_on_click_listener(self.open_Terminal)
        m10.set_on_click_listener(self.open_API)
        m11.set_on_click_listener(self.open_API_Test)
        menu.append(m1)
        menu.append(m2)
        menu.append(m3)
        menu.append(m4)
        menu.append(m6)
        menu.append(m7)
        menu.append(m8)
        menu.append(m9)
        menu.append(m10)
        menu.append(m11)
        self.menubarConfig.empty()
        self.menubarConfig.append(menu)
        self.menubarConfig.redraw()
        self.txtFirmware.set_text(self.getFirmwarePath(self.OS))
        self.configDialog.show(self)

    def open_API_Test(self,widget):
        self.homePageNavaigation()
        self.subContainerDevicesAPITest.empty()
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m2 = gui.MenuItem('Zigbee Test', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m6 = gui.MenuItem('OTA Test', width=100, height=30)
        m7 = gui.MenuItem('Zigbee Dump', width=100, height=30)
        m8 = gui.MenuItem('LIVE', width=100, height=30)
        m9 = gui.MenuItem('STOP', width=100, height=30)
        m10 = gui.MenuItem('API', width=100, height=30)
        m11 = gui.MenuItem('Config', width=100, height=30)
        m1.set_on_click_listener(self.homePage)
        m2.set_on_click_listener(self.menu_dialog_clicked)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m6.set_on_click_listener(self.open_OTA)
        m7.set_on_click_listener(self.open_ZigbeeDump)
        m9.set_on_click_listener(self.killBatch)
        m8.set_on_click_listener(self.open_Terminal)
        m10.set_on_click_listener(self.open_API)
        m11.set_on_click_listener(self.open_Config)
        menu.append(m1)
        menu.append(m2)
        menu.append(m3)
        menu.append(m4)
        menu.append(m6)
        menu.append(m7)
        menu.append(m8)
        menu.append(m9)
        menu.append(m10)
        menu.append(m11)
        self.menubarAPITest.empty()
        self.menubarAPITest.append(menu)
        self.menubarAPITest.redraw()
        self.apiTestDialog.add_field("menu",self.menubarAPITest)
        self.apiTestDialog.add_field("cred",self.subContainerDevicesAPITest)

        self.subContainerDevicesAPITestenv = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                 margin='0px')
        self.subContainerDevicesAPITestuser = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPITestpwd = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPITestjson = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPITesthub = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPITestNodes = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPITestenv.append(gui.Label("Select the environment"))
        self.subContainerDevicesAPITestenv.append(self.envTestValidation)
        self.subContainerDevicesAPITestuser.append(gui.Label("User Name"))
        self.subContainerDevicesAPITestuser.append(self.dtextUserName)
        self.subContainerDevicesAPITestpwd.append(gui.Label("Password"))
        self.subContainerDevicesAPITestpwd.append(self.dtextPassword)
        self.subContainerDevicesAPITest.append(self.subContainerDevicesAPITestenv)
        self.subContainerDevicesAPITest.append(self.subContainerDevicesAPITestuser)
        self.subContainerDevicesAPITest.append(self.subContainerDevicesAPITestpwd)
        self.apiTestLogin = gui.Button("Login", width=200, height=30, margin='10px')
        self.apiTestLogin.set_on_click_listener(self.on_apiLogin_Test)
        self.subContainerDevicesAPITest.append(self.apiTestLogin)
        #self.request = gui.TextInput(single_line=False,width="50%",height="200px")
        self.response = gui.TextInput(single_line=False,width="100%",height="100px")
        self.subContainerDevicesAPITest.redraw()
        #self.subContainerDevicesAPIjson.append(self.request)
        self.subContainerDevicesAPITestjson.append(self.response)
        self.subContainerDevicesAPITest.append(self.subContainerDevicesAPITestjson)
        #self.subContainerDevicesAPITesthub.append(gui.Label("Hub Long Id"))
        #self.subContainerDevicesAPITesthub.append(self.dtextHubId)
        #self.apiTestGetHubDetails = gui.Button("Get Nodes", width=200, height=30, margin='10px')
        #self.apiTestGetHubDetails.set_on_click_listener(self.on_apiHubDetails)
        #self.subContainerDevicesAPITesthub.append(self.apiTestGetHubDetails)
        self.lstDevicesTest = gui.ListView(selectable=True,width="25%",height="100%")
        self.lstDevicesNodeTest1 = gui.ListView(selectable=True,width="25%",height="100%")
        self.lstDevicesNodeTest2 = gui.ListView(selectable=True,width="25%",height="100%")
        self.lstDevicesNodeTest3 = gui.ListView(selectable=True,width="25%",height="100%")
        #self.subContainerDevicesAPITest.append(self.subContainerDevicesAPIhub)
        self.subContainerDevicesAPITestNodes.append(self.lstDevicesTest)
        self.subContainerDevicesAPITestNodes.append(self.lstDevicesNodeTest1)
        self.subContainerDevicesAPITestNodes.append(self.lstDevicesNodeTest2)
        self.subContainerDevicesAPITestNodes.append(self.lstDevicesNodeTest3)
        self.subContainerDevicesAPITest.append(self.subContainerDevicesAPITestNodes)
        self.apiTestDialog.show(self)

    def open_API(self,widget):
        self.homePageNavaigation()
        self.subContainerDevicesAPI.empty()
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m2 = gui.MenuItem('Zigbee Test', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m6 = gui.MenuItem('OTA Test', width=100, height=30)
        m7 = gui.MenuItem('Zigbee Dump', width=100, height=30)
        m8 = gui.MenuItem('LIVE', width=100, height=30)
        m9 = gui.MenuItem('STOP', width=100, height=30)
        m10 = gui.MenuItem('API Test', width=100, height=30)
        m11 = gui.MenuItem('Config', width=100, height=30)
        m1.set_on_click_listener(self.homePage)
        m2.set_on_click_listener(self.menu_dialog_clicked)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m6.set_on_click_listener(self.open_OTA)
        m7.set_on_click_listener(self.open_ZigbeeDump)
        m9.set_on_click_listener(self.killBatch)
        m8.set_on_click_listener(self.open_Terminal)
        m10.set_on_click_listener(self.open_API_Test)
        m11.set_on_click_listener(self.open_Config)
        menu.append(m1)
        menu.append(m2)
        menu.append(m3)
        menu.append(m4)
        menu.append(m6)
        menu.append(m7)
        menu.append(m8)
        menu.append(m9)
        menu.append(m10)
        menu.append(m11)
        self.menubarAPI.empty()
        self.menubarAPI.append(menu)
        self.menubarAPI.redraw()
        self.apiDialog.add_field("menu",self.menubarAPI)
        self.apiDialog.add_field("cred",self.subContainerDevicesAPI)

        self.subContainerDevicesAPIenv = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                 margin='0px')
        self.subContainerDevicesAPIuser = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPIpwd = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPIjson = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPIhub = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPINodes = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL,
                                                    margin='0px')
        self.subContainerDevicesAPIenv.append(gui.Label("Select the environment"))
        self.subContainerDevicesAPIenv.append(self.envValidation)
        self.subContainerDevicesAPIuser.append(gui.Label("User Name"))
        self.subContainerDevicesAPIuser.append(self.dtextUserName)
        self.subContainerDevicesAPIpwd.append(gui.Label("Password"))
        self.subContainerDevicesAPIpwd.append(self.dtextPassword)
        self.subContainerDevicesAPI.append(self.subContainerDevicesAPIenv)
        self.subContainerDevicesAPI.append(self.subContainerDevicesAPIuser)
        self.subContainerDevicesAPI.append(self.subContainerDevicesAPIpwd)
        self.apiLogin = gui.Button("Login", width=200, height=30, margin='10px')
        self.apiLogin.set_on_click_listener(self.on_apiLogin)
        self.subContainerDevicesAPI.append(self.apiLogin)
        #self.request = gui.TextInput(single_line=False,width="50%",height="200px")
        self.response = gui.TextInput(single_line=False,width="100%",height="200px")
        self.subContainerDevicesAPI.redraw()
        #self.subContainerDevicesAPIjson.append(self.request)
        self.subContainerDevicesAPIjson.append(self.response)
        self.subContainerDevicesAPI.append(self.subContainerDevicesAPIjson)
        self.subContainerDevicesAPIhub.append(gui.Label("Hub Long Id"))
        self.subContainerDevicesAPIhub.append(self.dtextHubId)
        self.apiGetHubDetails = gui.Button("Get Hub Details", width=200, height=30, margin='10px')
        self.apiGetHubDetails.set_on_click_listener(self.on_apiHubDetails)
        self.subContainerDevicesAPIhub.append(self.apiGetHubDetails)
        self.lstDevices = gui.ListView(selectable=True,width="25%",height="100%")
        self.lstDevicesNode1 = gui.ListView(selectable=True,width="25%",height="100%")
        self.lstDevicesNode2 = gui.ListView(selectable=True,width="25%",height="100%")
        self.lstDevicesNode3 = gui.ListView(selectable=True,width="25%",height="100%")
        self.subContainerDevicesAPI.append(self.subContainerDevicesAPIhub)
        self.subContainerDevicesAPINodes.append(self.lstDevices)
        self.subContainerDevicesAPINodes.append(self.lstDevicesNode1)
        self.subContainerDevicesAPINodes.append(self.lstDevicesNode2)
        self.subContainerDevicesAPINodes.append(self.lstDevicesNode3)
        self.subContainerDevicesAPI.append(self.subContainerDevicesAPINodes)
        self.apiDialog.show(self)

    def on_apiHubDetails(self,widget):
        hubLogs = apiUtils.getHubLogsV6(self.session ,self.dtextHubId.get_value())
        hudModel = hubLogs["internalHubState"]["featureStates"][list(hubLogs["internalHubState"]["featureStates"].keys())[0]]['properties']["hardwareVersion"]['receivedValue']
        self.oDictDevice = {hudModel:{}}
        for hubKey in hubLogs["internalHubState"].keys():
            if "featureStates" not in hubKey:
                self.oDictDevice[hudModel][hubKey] = hubLogs["internalHubState"][hubKey]
            else:
                for propkey in hubLogs["internalHubState"]["featureStates"][list(hubLogs["internalHubState"]["featureStates"].keys())[0]]['properties'].keys():
                    self.oDictDevice[hudModel][propkey] = hubLogs["internalHubState"][hubKey][list(hubLogs["internalHubState"]["featureStates"].keys())[0]]['properties'][propkey]
        devlog = 0

        for devlogs in hubLogs['internalNodeStates']:
            modelid = ""
            for okey in hubLogs['internalNodeStates'][devlog]['defaultEndpoint']['featureStates'].keys():
                try:
                    if hubLogs['internalNodeStates'][devlog]['defaultEndpoint']['featureStates'][okey]['properties']['model']['receivedValue'] is not None:
                        modelid = hubLogs['internalNodeStates'][devlog]['defaultEndpoint']['featureStates'][okey]['properties']['model']['receivedValue']
                        macId = \
                        hubLogs['internalNodeStates'][devlog]['defaultEndpoint']['featureStates'][okey]['properties'][
                            'macAddress']['receivedValue']
                        modelid = modelid + " - " + macId
                except:
                    pass
            try:

                if "NANO" not in modelid:
                    self.oDictDevice[modelid]={}
                    for nodeKey in hubLogs['internalNodeStates'][devlog]:
                        if "defaultEndpoint" not in nodeKey:
                            self.oDictDevice[modelid][nodeKey] = hubLogs['internalNodeStates'][devlog][nodeKey]
                        else:
                            for oInKey in hubLogs['internalNodeStates'][devlog]['defaultEndpoint']['featureStates'].keys():
                                for iFkey in hubLogs['internalNodeStates'][devlog]['defaultEndpoint']['featureStates'][oInKey]['properties'].keys():
                                    self.oDictDevice[modelid][iFkey] = hubLogs['internalNodeStates'][devlog]['defaultEndpoint']['featureStates'][oInKey]['properties'][iFkey]
                                    #self.oDictDevice[hudModel] = hubLogs['internalNodeStates'][devlog]
                    devlog += 1
            except:
                pass
        self.lstDevices.empty()
        self.lstDevices = self.lstDevices.new_from_list(list(self.oDictDevice.keys()))
        self.lstDevices.set_on_selection_listener(self.list_view_on_lstDevices)
        self.subContainerDevicesAPINodes.append(self.lstDevices)
        self.response.set_text(str(hubLogs).replace("',","',\n").replace("\",","\",\n").replace("},","},\n").replace("{","{\n"))

    def list_view_on_lstDevices(self,widget,selected_item_key):
        self.lstDevicesNode1.empty()
        self.lstDevicesNode2.empty()
        self.lstDevicesNode3.empty()
        self.subContainerDevicesAPINodes.remove_child(self.lstDevicesNode3)
        self.subContainerDevicesAPINodes.remove_child(self.lstDevicesNode2)
        self.lstDevicesNode1 = gui.ListView(selectable=True,width="25%",height="100%").new_from_list(list(self.oDictDevice[str(widget.children[selected_item_key].get_text())].keys()))
        self.subContainerDevicesAPINodes.append(self.lstDevicesNode1)
        self.lstDevicesNode1.set_on_selection_listener(self.list_view_on_lstDevicesNode1)

    def list_view_on_lstDevicesNode1(self, widget, selected_item_key):
        self.lstDevicesNode2.empty()
        self.lstDevicesNode3.empty()
        self.subContainerDevicesAPINodes.remove_child(self.lstDevicesNode3)
        self.subContainerDevicesAPINodes.remove_child(self.lstDevicesNode2)
        if type(self.oDictDevice[self.lstDevices.children[self.lstDevices._selected_key].get_text()][str(widget.children[selected_item_key].get_text())]) is dict:
            self.lstDevicesNode2 = gui.ListView(selectable=True, width="25%", height="100%").new_from_list(
                list(self.oDictDevice[self.lstDevices.children[self.lstDevices._selected_key].get_text()][str(widget.children[selected_item_key].get_text())].keys()))
        else:
            self.lstDevicesNode2.append(str(self.oDictDevice[self.lstDevices.children[self.lstDevices._selected_key].get_text()][str(widget.children[selected_item_key].get_text())]))
        self.subContainerDevicesAPINodes.append(self.lstDevicesNode2)
        self.lstDevicesNode2.set_on_selection_listener(self.list_view_on_lstDevicesNode2)

    def list_view_on_lstDevicesNode2(self, widget, selected_item_key):
        self.lstDevicesNode3.empty()
        self.subContainerDevicesAPINodes.remove_child(self.lstDevicesNode3)
        try:
            self.lstDevicesNode3.append(str(
                self.oDictDevice[self.lstDevices.children[self.lstDevices._selected_key].get_text()][self.lstDevicesNode1.children[self.lstDevicesNode1._selected_key].get_text()][
                    str(widget.children[selected_item_key].get_text())]))
            self.subContainerDevicesAPINodes.append(self.lstDevicesNode3)
        except:
            pass

    def on_apiLogin(self,widget):
        if self.envValidation.get_value() is None:
            MyApp.execute_javascript(self, code="alert('Please select environment');")
            return
        utils.setAttribute('common', 'currentEnvironment',self.envDict[self.envValidation.get_value()])
        utils.setAttribute('common', 'userName', self.dtextUserName.get_value())
        utils.setAttribute('common', 'password', self.dtextPassword.get_value())
        strPlatformVersion = apiUtils.createCredentials(self.envDict[self.envValidation.get_value()])
        self.session = apiUtils.sessionObject()
        self.response.set_text(str(self.session.response).replace("',","',\n").replace("\",","\",\n").replace("},","},\n").replace("{","{\n"))
        strSessionId = json.loads(self.session.response)['sessions'][0]['sessionId']

    def on_apiLogin_Test(self,widget):
        if self.envTestValidation.get_value() is None:
            MyApp.execute_javascript(self, code="alert('Please select environment');")
            return
        utils.setAttribute('common', 'currentEnvironment',self.envDict[self.envTestValidation.get_value()])
        utils.setAttribute('common', 'userName', self.dtextUserName.get_value())
        utils.setAttribute('common', 'password', self.dtextPassword.get_value())
        strPlatformVersion = apiUtils.createCredentials(self.envDict[self.envTestValidation.get_value()])
        self.session = apiUtils.sessionObject()
        self.response.set_text(str(self.session.response).replace("',","',\n").replace("\",","\",\n").replace("},","},\n").replace("{","{\n"))
        strSessionId = json.loads(self.session.response)['sessions'][0]['sessionId']
        response = apiUtils.getNodesV6(self.session)
        lstNodes = []
        for odict in response["nodes"]:
            try:
                if odict["attributes"]["model"] is not None:
                    lstNodes.append(odict["attributes"]["model"]["reportedValue"] + "_"+odict["id"]+"_"+odict["name"])
            except:
                pass
        self.lstDevicesTest.empty()
        self.lstDevicesTest = self.lstDevicesTest.new_from_list(lstNodes)
        self.subContainerDevicesAPITest.append(self.lstDevicesTest)
        self.subContainerDevicesAPITest.redraw()
        #print(response)

    def getFirmwarePath(self, os):
        global FIRMWARE_ROOT_FILE_PATH
        if 'DARWIN' in platform.system().upper():
            FIRMWARE_ROOT_FILE_PATH = config.FIRMWARE_ROOT_FILE_PATH
        elif 'LINUX' in platform.system().upper():
            FIRMWARE_ROOT_FILE_PATH = '/home/pi/hardware/firmware-release-notes/'
        elif sys.platform.startswith('win'):
            FIRMWARE_ROOT_FILE_PATH = config.FIRMWARE_ROOT_FILE_PATH
        return FIRMWARE_ROOT_FILE_PATH

    def installLibraries(self, widget):
        try:
            self.p.terminate()
            self.p.kill()
        except:
            pass
        self.killBatch()
        self.oThread = start_new_thread(target=self.installLib)
        self.flag = False
        self.oThread.setDaemon(True)
        self.oThread.start()

    def installLib(self):
        self.subContainerConfigLibrariesConsole.empty()
        self.subContainerConfigLibrariesConsole.redraw()
        self.listInstalled.empty()
        self.listNotInstalled.empty()
        self.listNotInstalled.append("List of Libraries", "Header")
        listLib = []
        listLibraries = ['Behave', 'Redis', 'pyserial', 'tqdm', 'ipdb', 'appium-python-client', 'selenium', 'tqdm',
                         'selenium', 'requests', 'pytesseract', 'pillow', 'numpy', 'speechrecognition', 'pysmbus']
        oFileName = "Installation_MAC.command"
        if "WINDOWS" in self.OS:
            oFileName = "Installation_WIN.bat"
        if "LINUX" in self.OS:
            oFileName = "Installation_MAC.sh"
        for root, dirs, files in os.walk(
                os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
            for file in files:

                if file.endswith(oFileName):
                    if "WINDOWS" in self.OS:
                        self.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    elif "LINUX" in self.OS:
                        self.p = subprocess.Popen(root + '/./' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    else:
                        self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                  stdout=subprocess.PIPE)
                    temp = ''
                    tempInner = ''
                    while True:
                        if self.flag:
                            print("\nstopped by API\n")
                            break
                        out = self.p.stdout.read(1)
                        if str(out) == 'b\'\'' and self.p.poll() != None:
                            break
                        if out != '':
                            sys.stdout.write(out.decode('utf-8'))
                            # self.consoleText.set_text(temp)
                            if '\n' in tempInner:
                                lbl = gui.Label(tempInner, width='100%')
                                if (
                                        "Requirement already satisfied: behave" in tempInner or "Successfully installed behave" in tempInner):
                                    listLib.append("Behave")
                                    self.listInstalled.append("Behave")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: redis" in tempInner or "Successfully installed redis" in tempInner):
                                    listLib.append("Redis")
                                    self.listInstalled.append("Redis")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: pyserial" in tempInner or "Successfully installed pyserial" in tempInner):
                                    listLib.append("pyserial")
                                    self.listInstalled.append("pyserial")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: tqdm" in tempInner or "Successfully installed tqdm" in tempInner):
                                    listLib.append("tqdm")
                                    self.listInstalled.append("tqdm")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: ipdb" in tempInner or "Successfully installed ipdb" in tempInner):
                                    listLib.append("ipdb")
                                    self.listInstalled.append("ipdb")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: appium-python-client" in tempInner or "Successfully installed appium-python-client" in tempInner):
                                    listLib.append("appium-python-client")
                                    self.listInstalled.append("appium-python-client")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: selenium" in tempInner or "Successfully installed selenium" in tempInner):
                                    listLib.append("selenium")
                                    self.listInstalled.append("selenium")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: requests" in tempInner or "Successfully installed requests" in tempInner):
                                    listLib.append("tqdm")
                                    self.listInstalled.append("tqdm")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: nmap" in tempInner or "Successfully installed nmap" in tempInner):
                                    listLib.append("requests")
                                    self.listInstalled.append("requests")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: pytesseract" in tempInner or "Successfully installed pytesseract" in tempInner):
                                    listLib.append("pytesseract")
                                    self.listInstalled.append("pytesseract")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: pillow" in tempInner or "Successfully installed pillow" in tempInner):
                                    listLib.append("pillow")
                                    self.listInstalled.append("pillow")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: numpy" in tempInner or "Successfully installed numpy" in tempInner):
                                    listLib.append("numpy")
                                    self.listInstalled.append("numpy")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: speechrecognition" in tempInner or "Successfully installed speechrecognition" in tempInner):
                                    listLib.append("speechrecognition")
                                    self.listInstalled.append("speechrecognition")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                        "Requirement already satisfied: pysmbus" in tempInner or "Successfully installed pysmbus" in tempInner):
                                    listLib.append("pysmbus")
                                    self.listInstalled.append("pysmbus")
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                                    "ERROR" in tempInner.upper() or "NACK" in tempInner.upper() or "**** PROBLEM" in tempInner.upper()):
                                    lbl.style['color'] = 'rgb(99, 7, 7)'
                                    lbl.style['font-size'] = '12px'
                                self.subContainerConfigLibrariesConsole.append(lbl)
                                self.subContainerConfigLibrariesConsole.redraw()
                                tempInner = ''
                            temp = temp + out.decode('utf-8')
                            tempInner = tempInner + out.decode('utf-8')
                            if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                                self.p.kill()
                                break
                            sys.stdout.flush()
                    listNotInstalled = []
                    listNotInstalled = [elem for elem in listLibraries if elem not in listLib]
                    for e in listNotInstalled:
                        self.listNotInstalled.append(e)
                    if len(listNotInstalled) < 1:
                        self.listNotInstalled.append("No missing Libraries", "Header")
                    self.listNotInstalled.redraw()
                    self.listInstalled.redraw()
                    self.subContainerConfigLibrariesList.redraw()
                    self.subContainerConfigLibrariesConsole.redraw()
                    print("\ncompleted\n")
                    break
                    # self.listInstalled.new_from_list(listLib)

    def open_resultsFolder(self, widget):
        oroot = None
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
            # print("path" + str(root))
            oroot = root
            break
        if platform.system() == "Windows":
            os.startfile(oroot + "/03_Results_Tier")
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", oroot + "/03_Results_Tier"])
        else:
            subprocess.Popen(["xdg-open", oroot + "/03_Results_Tier"])

    def open_LatestResult(self, widget):
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
                    if platform.system() == "Windows":
                        os.startfile(file)
                    elif platform.system() == "Darwin":
                        subprocess.Popen(["open", file])
                    else:
                        subprocess.Popen(["xdg-open", file])

    def ReadFeatureFile(self, horizontalContainer, RPI=None):
        # print("path = " +str(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]))
        if RPI is None:
            self.HeadLable = gui.Label("<BR>HIVE TEST AUTOMATION <BR>")
            self.HeadLable.style['font-size'] = '36px'
            self.subContainerRight.append(self.HeadLable)
        else:
            self.HeadLable = gui.Label("<BR>HIVE TEST AUTOMATION <BR>")
            self.HeadLable.style['font-size'] = '36px'
            self.subContainerRightRPI.append(self.HeadLable)
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                             0] + "/01_BDD_Tier/features/"):
            # print("path" + str(root))


            for file in files:
                if file.endswith(".feature"):
                    btn = gui.Button(file, width=200, height=30, margin='10px')
                    if RPI is None:
                        btn.set_on_click_listener(self.on_button_pressed)
                        horizontalContainer.append(btn)
                    else:
                        btn.set_on_click_listener(self.on_button_pressed_RPI)
                        horizontalContainer.append(btn)

    def on_runTest_API(self,widget):
        self.lstRPIurl = config.RPIURL
        flag = False
        try:
            if self.distributedExecution.children['checkbox'].attributes['checked'] is not None:
                flag = True
        except:
            pass
        if flag:
            if str(self.distributedExecution.children['checkbox'].attributes['checked']).upper() == "CHECKED":
                intCtr = 0
                intTCCtr = 0
                lstUrL = []
                lstTag = []
                strTag = widget.get_text()
                r = RemoteLabel.readTotalTestCase(self)
                jsonTC = json.loads(r)
                for node in jsonTC:
                    for oInnerNode in jsonTC[node]:
                        if "@" + str(strTag).strip() in str(oInnerNode):
                            strSplit = str(oInnerNode).split("@")
                            for strScenario in strSplit:
                                if strScenario.upper().strip().startswith("SC-"):
                                    if str(strScenario).strip().endswith("_"):
                                        lstTag.append(str(strScenario).strip()[:-1])
                                    else:
                                        lstTag.append(str(strScenario).strip())
                                    intTCCtr += 1
                for oContainer in self.subContainerDevicesInnerRPI.children:
                    for oInnerContainer in self.subContainerDevicesInnerRPI.children[oContainer].children:
                        if self.subContainerDevicesInnerRPI.children[oContainer].children[oInnerContainer].children is not None:
                            for oCheckContainer in self.subContainerDevicesInnerRPI.children[oContainer].children[
                                oInnerContainer].children:
                                try:
                                    if str(self.subContainerDevicesInnerRPI.children[oContainer].children[
                                               oInnerContainer].children[oCheckContainer].attributes[
                                               'class']).upper() == 'CHECKBOX':
                                        try:
                                            if str(self.subContainerDevicesInnerRPI.children[oContainer].children[
                                                       oInnerContainer].children[oCheckContainer].attributes[
                                                       'checked']).upper() == "CHECKED":
                                                url = self.lstRPIurl[str(
                                                    self.subContainerDevicesInnerRPI.children[oContainer].children[
                                                        oInnerContainer].children[oCheckContainer].attributes['value'])]
                                                lstUrL.append(url)
                                                intCtr += 1

                                        except:
                                            pass
                                except:
                                    pass

                intMod = intTCCtr % intCtr
                intNumber = (intTCCtr-intMod) / intCtr
                intIndex = 0
                lstTCSplit = []
                intRpiCtr = 0
                strTCTag = ""
                for oTc in lstTag:
                    intIndex += 1
                    if intIndex % intNumber > 0:
                        if intIndex % intNumber == 1 and intIndex <= len(lstTag) :
                            strTCTag = oTc
                        else:
                            strTCTag = strTCTag+","+oTc

                    else:
                        strTCTag = strTCTag + "," + oTc
                        url = lstUrL[intRpiCtr]
                        r = requests.get(url + "/api/testrun?tagName=" + strTCTag)
                        print(r)
                        if r.status_code == 200:
                            status = r.content
                            print(status)
                        intRpiCtr += 1
                print("hi")

        else:
            for oContainer in self.subContainerDevicesInnerRPI.children:
                for oInnerContainer in self.subContainerDevicesInnerRPI.children[oContainer].children:
                    if self.subContainerDevicesInnerRPI.children[oContainer].children[oInnerContainer].children is not None:
                        for oCheckContainer in self.subContainerDevicesInnerRPI.children[oContainer].children[oInnerContainer].children:
                            try:
                                if str(self.subContainerDevicesInnerRPI.children[oContainer].children[oInnerContainer].children[oCheckContainer].attributes['class']).upper() == 'CHECKBOX':
                                    try:
                                        if str(self.subContainerDevicesInnerRPI.children[oContainer].children[oInnerContainer].children[oCheckContainer].attributes['checked']).upper() == "CHECKED":
                                            url = self.lstRPIurl[str(self.subContainerDevicesInnerRPI.children[oContainer].children[oInnerContainer].children[oCheckContainer].attributes['value'])]
                                            r = requests.get(url + "/api/testrun?tagName="+widget.get_text())
                                            print(r)
                                            if r.status_code == 200:
                                                status = r.content
                                                print(status)
                                                '''if r.content == b"":
                                                    status = "Ready"
                                                    self.rpi1.attributes["src"] = 'res/Ready.png'
                                                elif r.content == b"started" or r.content == b"completed" or r.content == b"running":
                                                    self.rpi1.attributes["src"] = 'res/Inprogress.gif'''

                                    except:
                                        pass
                            except:
                                pass

    def on_runTest(self, widget):
        try:
            self.p.terminate()
            self.p.kill()
        except:
            pass
        self.oThread = start_new_thread(target=self.runTest, args=(widget,))
        self.flag = False
        self.oThread.setDaemon(True)
        self.oThread.start()

    def runTest(self, widget):
        MyApp.execute_javascript(self, code="document.getElementsByTagName('textarea')[3].focus();")
        MyApp.execute_javascript(self, code="alert('Test Execution Started');")
        self.consoleText.set_text("")
        self.consoleContainer.empty()
        #self.killBatch()
        oFileName = "Execute.command"
        if "WINDOWS" in self.OS:
            oFileName = "Execute_WIN.bat"
        if "LINUX" in self.OS:
            oFileName = "Execute.sh"
        for root, dirs, files in os.walk(os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
            for file in files:
                if file.endswith(oFileName):
                    if "WINDOWS" not in self.OS and "LINUX" not in self.OS:
                        with open(root + "/" + file, 'w') as f:
                            f.write("#!/bin/sh \n")
                            f.write('cd "$(dirname ${BASH_SOURCE[0]})/../../01_BDD_Tier/features"\n')
                            f.write("behave --tags=" + widget.get_text())
                    elif "WINDOWS" in self.OS:
                        with open(root + "/" + file, 'w') as f:
                            f.write('cd "%~dp0/../../01_BDD_Tier/features"\n')
                            f.write("behave --tags=" + widget.get_text())
                    elif "LINUX" in self.OS:
                        with open(root + "/" + file, 'w') as f:
                            f.write("#!/bin/sh \n")
                            f.write('cd $(dirname "$0")/../../01_BDD_Tier/features\n')
                            f.write("behave --tags=" + widget.get_text())
                    if "WINDOWS" in self.OS:
                        self.p = subprocess.Popen(root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                    else:
                        self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                    temp = ''
                    tempInner = ''
                    while True:
                        if self.flag:
                            print("\nstopped by API\n")
                            break
                        self.consoleText.onfocus()
                        self.consoleText.onclick()
                        out = self.p.stdout.read(1)
                        if out == '' and self.p.poll() != None:
                            # MyApp.execute_javascript(self, code="document.getElementsByTagName('textarea')[0].focus();")
                            # MyApp.execute_javascript(self, code="alert('Done');")
                            break
                        if out != '':
                            sys.stdout.write(out.decode('utf-8'))
                            # self.consoleText.set_text(temp)
                            if '\n' in tempInner:
                                lbl = gui.Label(tempInner, width='100%')
                                if ("DEBUG Tx:" in tempInner):
                                    lbl.style['color'] = 'rgb(30, 104, 46)'
                                    lbl.style['font-size'] = '12px'
                                if ("DEBUG RX:" in tempInner):
                                    lbl.style['color'] = 'rgb(44, 55, 130)'
                                    lbl.style['font-size'] = '12px'
                                if (
                                            "ERROR" in tempInner.upper() or "NACK" in tempInner.upper() or "**** PROBLEM" in tempInner.upper()):
                                    lbl.style['color'] = 'rgb(99, 7, 7)'
                                    lbl.style['font-size'] = '12px'
                                self.consoleText.set_text(temp)
                                self.consoleContainer.append(lbl)
                                # self.consoleContainer.redraw()
                                tempInner = ''
                            temp = temp + out.decode('utf-8')
                            tempInner = tempInner + out.decode('utf-8')
                            if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp:
                                self.p.kill()
                                MyApp.execute_javascript(self,
                                                         code="document.getElementsByTagName('textarea')[0].focus();")
                                MyApp.execute_javascript(self, code="alert('Error');")
                                break
                            sys.stdout.flush()
                    print("\ncompleted\n")
                    MyApp.execute_javascript(self, code="document.getElementsByTagName('textarea')[0].focus();")
                    MyApp.execute_javascript(self, code="alert('Test Completed Successfully');")
                    break
                    '''output = pipe.read()
                    print(output)'''
                    '''s = pxssh.pxssh()
                    if not s.login('devices-rpi1.local','pi','Rathb0n3'):
                        print("SSH session failed on login.")
                        print(str(s))
                    else:
                        print("SSH session login successful")
                        s.sendline('pwd')
                        s.prompt()  # match the prompt
                        print(s.before)  # print everything before the prompt.
                        s.logout()'''

    def on_EditTest(self, widget):
        '''s = pxssh.pxssh()
        if not s.login('devices-rpi2.local', 'pi', 'Rathb0n3'):
            print("SSH session failed on login.")
            print(str(s))
        else:
            print("SSH session login successful")
            s.sendline('pwd')
            s.prompt()  # match the prompt
            print(s.before)
            s.sendline('cd /home/pi/workspace/HiveTestAutomation/')
            s.prompt()  # match the prompt
            print(s.before)  # print everything before the prompt.
            s.sendline('rm ~/.execute.sh')
            s.prompt()  # m
            print(s.before)  # print everything before the prompt.
            s.sendline('touch ~/.execute.sh')
            s.prompt()  # m
            print(s.before)  # print everything before the prompt.
            s.sendline('echo "#!/bin/sh " >> ~/.execute.sh')
            s.prompt()  # match the prompt
            print(s.before)  # print everything before the prompt.
            s.sendline('echo "killall screen" >> ~/.execute.sh')
            s.prompt()  # m
            print(s.before)  # print everything before the prompt.
            s.sendline('echo "screen -dmS test " >> ~/.execute.sh')
            s.prompt()  # m
            print(s.before)  # print everything before the prompt.
            s.sendline('echo "sleep 5" >> ~/.execute.sh')
            s.prompt()  # m
            print(s.before)  # print everything before the prompt.
            s.sendline('echo "screen -S test -X stuff $\'behave\'">> ~/.execute.sh')
            s.prompt()  # match the prompt
            print(s.before)  # print everything before the prompt.
            s.sendline('echo "screen -S test -X stuff $\'behave auto^M\'" >> ~/.execute.sh')
            s.prompt()  # match the prompt
            print(s.before)  # print everything before the prompt.
            s.sendline('echo "screen -S test -X stuff $\'behave behave --tags=SC-AL-SP-01^M\'" >> ~/.execute.sh')
            s.prompt()  # match the prompt
            print(s.before)  # print everything before the prompt.
            s.sendline('sh ~/.execute.sh')
            s.prompt()  # match the prompt
            print(s.before)  # print everything before the prompt.
            s.logout()


        shell = spur.SshShell(hostname="devices-rpi9.local", username="pi", password="Rathb0n3")

        result = shell.run(["ssh","pi@devices-rpi9.local","screen","-m","-d"])
        print
        result.output  # prints hello'''
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

    def on_RefreshTest(self, widget):
        self.subContainerRight.empty()
        self.subContainerRight.redraw()
        btn = gui.Button("Edit " + str(widget.get_text()).replace("Refresh ", ""), width=200, height=30, margin='10px')
        btn.set_on_click_listener(self.on_EditTest)
        self.HeadLable = gui.Label("<BR>HIVE TEST AUTOMATION <BR>")
        self.HeadLable.style['font-size'] = '36px'
        self.subContainerRight.append(self.HeadLable)
        self.subContainerRight.append(btn)
        btn = gui.Button(widget.get_text(), width=200, height=30, margin='10px')
        btn.set_on_click_listener(self.on_RefreshTest)
        self.subContainerRight.append(btn)
        self.subContainerRight.append(gui.Label(str(widget.get_text()).replace("Refresh ", "")))
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
                                    btn = gui.Button(tag, width=200, height=30, margin='10px')
                                    btn.set_on_click_listener(self.on_runTest)
                                    self.subContainerRight.append(btn)
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
                                self.subContainerRight.append(tbl)
                                Tableflag = False
                                continueFlag = False
                                counter = 0
                                TableList.clear()
                            txt = gui.Label(line, width='100%')
                            subTxt = gui.Widget(width='100%')
                            if ("#" in line):
                                subTxt.style['color'] = 'rgb(32, 94, 15)'
                                subTxt.style['font-size'] = '10px'
                            if ("Feature" in line):
                                subTxt.style['color'] = 'rgb(130, 9, 9)'
                                subTxt.style['font-weight'] = 'bold'
                            if ("Scenario" in line):
                                subTxt.style['color'] = 'rgb(193, 81, 1)'
                                subTxt.style['font-weight'] = 'bold'
                            if ("Given" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("When" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("Then" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("And" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            subTxt.append(txt)
                            self.subContainerRight.append(subTxt)
        self.consoleText = gui.TextInput(width='100%', height=1000)

        self.subContainerRight.append(self.consoleText)

    def on_button_pressed(self, widget):

        self.subContainerRight.empty()
        self.subContainerRight.redraw()
        self.HeadLable = gui.Label("<BR>HIVE TEST AUTOMATION <BR>")
        self.HeadLable.style['font-size'] = '36px'
        self.subContainerRight.append(self.HeadLable)
        btn = gui.Button("Edit " + widget.get_text(), width=200, height=30, margin='10px')
        btn.set_on_click_listener(self.on_EditTest)
        self.subContainerRight.append(btn)
        btn = gui.Button("Refresh " + widget.get_text(), width=200, height=30, margin='10px')
        btn.set_on_click_listener(self.on_RefreshTest)
        self.subContainerRight.append(btn)
        self.subContainerRight.append(gui.Label(widget.get_text()))
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                             0] + "/01_BDD_Tier/features/"):
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
                            for tag in line.split("@"):
                                tag = str(tag).replace('  ', '')
                                if str(tag).strip() != "" and str(tag).strip() != "#":
                                    btn = gui.Button(tag, width=200, height=30, margin='10px')
                                    btn.set_on_click_listener(self.on_runTest)
                                    self.subContainerRight.append(btn)
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
                                # for row in line.split("|"):
                                #    if str(row).strip() != "":
                                #        print("hi")
                                TableList.append(line.split("|"))

                                counter = counter + 1
                        else:
                            if len(TableList) > 0:
                                tbl = gui.Table.new_from_list(TableList, width='100%')
                                self.subContainerRight.append(tbl)
                                Tableflag = False
                                continueFlag = False
                                counter = 0
                                TableList.clear()
                            txt = gui.Label(line, width='100%')
                            subTxt = gui.Widget(width='100%')
                            if ("#" in line):
                                subTxt.style['color'] = 'rgb(32, 94, 15)'
                                subTxt.style['font-size'] = '10px'
                            if ("Feature" in line):
                                subTxt.style['color'] = 'rgb(130, 9, 9)'
                                subTxt.style['font-weight'] = 'bold'
                            if ("Scenario" in line):
                                subTxt.style['color'] = 'rgb(193, 81, 1)'
                                subTxt.style['font-weight'] = 'bold'
                            if ("Given" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("When" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("Then" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("And" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            subTxt.append(txt)
                            self.subContainerRight.append(subTxt)
        self.consoleText = gui.TextInput(width='100%', height=1000)

        self.subContainerRight.append(self.consoleContainer)
        self.subContainerRight.append(self.consoleText)
        
    def on_button_pressed_RPI(self, widget):

        self.subContainerRightRPI.empty()
        self.subContainerRightRPI.redraw()
        self.HeadLable = gui.Label("<BR>HIVE TEST AUTOMATION <BR>")
        self.HeadLable.style['font-size'] = '36px'
        self.subContainerRightRPI.append(self.HeadLable)
        btn = gui.Button("Edit " + widget.get_text(), width=200, height=30, margin='10px')
        btn.set_on_click_listener(self.on_EditTest)
        self.subContainerRightRPI.append(btn)
        btn = gui.Button("Refresh " + widget.get_text(), width=200, height=30, margin='10px')
        btn.set_on_click_listener(self.on_RefreshTest)
        self.subContainerRightRPI.append(btn)
        self.subContainerRightRPI.append(gui.Label(widget.get_text()))
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[
                                             0] + "/01_BDD_Tier/features/"):
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
                            for tag in line.split("@"):
                                tag = str(tag).replace('  ', '')
                                if str(tag).strip() != "" and str(tag).strip() != "#":
                                    btn = gui.Button(tag, width=200, height=30, margin='10px')
                                    btn.set_on_click_listener(self.on_runTest_API)
                                    self.subContainerRightRPI.append(btn)
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
                                # for row in line.split("|"):
                                #    if str(row).strip() != "":
                                #        print("hi")
                                TableList.append(line.split("|"))

                                counter = counter + 1
                        else:
                            if len(TableList) > 0:
                                tbl = gui.Table.new_from_list(TableList, width='100%')
                                self.subContainerRightRPI.append(tbl)
                                Tableflag = False
                                continueFlag = False
                                counter = 0
                                TableList.clear()
                            txt = gui.Label(line, width='100%')
                            subTxt = gui.Widget(width='100%')
                            if ("#" in line):
                                subTxt.style['color'] = 'rgb(32, 94, 15)'
                                subTxt.style['font-size'] = '10px'
                            if ("Feature" in line):
                                subTxt.style['color'] = 'rgb(130, 9, 9)'
                                subTxt.style['font-weight'] = 'bold'
                            if ("Scenario" in line):
                                subTxt.style['color'] = 'rgb(193, 81, 1)'
                                subTxt.style['font-weight'] = 'bold'
                            if ("Given" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("When" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("Then" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            if ("And" in line):
                                subTxt.style['color'] = 'rgb(28, 61, 178)'
                            subTxt.append(txt)
                            self.subContainerRightRPI.append(subTxt)
        self.consoleText = gui.TextInput(width='100%', height=1000)
        self.subContainerRightRPI.append(self.consoleContainer)
        self.subContainerRightRPI.append(self.consoleText)

    def menu_dialog_clicked(self, widget):
        self.homePageNavaigation()
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m5 = gui.MenuItem('Config', width=100, height=30)
        m6 = gui.MenuItem('OTA Test', width=100, height=30)
        m7 = gui.MenuItem('Zigbee Dump', width=100, height=30)
        m8 = gui.MenuItem('LIVE', width=100, height=30)
        m9 = gui.MenuItem('STOP', width=100, height=30)
        m1.set_on_click_listener(self.homePage)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m5.set_on_click_listener(self.open_Config)
        m6.set_on_click_listener(self.open_OTA)
        m7.set_on_click_listener(self.open_ZigbeeDump)
        m8.set_on_click_listener(self.open_Terminal)
        m9.set_on_click_listener(self.killBatch)
        menu.append(m1)
        menu.append(m3)
        menu.append(m4)
        menu.append(m5)
        menu.append(m6)
        menu.append(m7)
        menu.append(m8)
        menu.append(m9)
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)
        self.dialog.add_field("menu", menubar)
        self.dtextinput.set_value('Click on Verify Devices Connected')
        self.dialog.add_field_with_label('dtextinput', 'Status', self.dtextinput)
        self.verifyTGStick = gui.Button("Verify Devices Connected", width=200, height=30, margin='10px')
        self.verifyTGStick.set_on_click_listener(self.on_VerfifyTGSTick)
        self.dialog.add_field("Devices Verification", self.verifyTGStick)
        self.subContainerDevices.append(self.DevDetailsContainer)
        self.subContainerDevices.append(self.TopDetailsContainer)
        self.subContainerDevices.append(self.listDetailsContainer)
        self.subContainerDevices.append(self.listDetailsContainer)
        self.subContainerDevices.append(self.firmwareContainer)
        self.consoleText = gui.TextInput(width='100%', height='100%')
        # self.subContainerDevicesInnerConsole.append(self.consoleText)
        # self.subContainerDevices.append(self.subContainerDevicesInnerConsole)
        self.dialog.add_field("container", self.horizontalContainerDialog)
        self.horizontalContainerDialog.append(self.subContainerDevices)
        self.subContainerDevicesInnerConsole.append(self.consoleContainer)
        self.dialog.add_field("Scenario", self.subContainerDevicesInner)
        self.dialog.add_field("console", self.subContainerDevicesInnerConsole)

        self.dialog.show(self)

    def open_OTA(self, widget):
        self.homePageNavaigation()
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m2 = gui.MenuItem('Zigbee Test', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m5 = gui.MenuItem('Config', width=100, height=30)
        m6 = gui.MenuItem('Zigbee Dump', width=100, height=30)
        m7 = gui.MenuItem('LIVE', width=100, height=30)
        m8 = gui.MenuItem('STOP', width=100, height=30)
        m9 = gui.MenuItem('API', width=100, height=30)
        m10 = gui.MenuItem('API Test', width=100, height=30)
        m1.set_on_click_listener(self.homePage)
        m2.set_on_click_listener(self.menu_dialog_clicked)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m5.set_on_click_listener(self.open_Config)
        m6.set_on_click_listener(self.open_ZigbeeDump)
        m7.set_on_click_listener(self.open_Terminal)
        m8.set_on_click_listener(self.killBatch)
        m9.set_on_click_listener(self.open_API)
        m10.set_on_click_listener(self.open_API_Test)
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
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)
        self.OTAdialog.add_field("menu", menubar)
        self.dtextinput.set_value('Click on Verify Devices Connected')
        self.OTAdialog.add_field_with_label('dtextinput', 'Status', self.dtextinput)
        self.verifyTGStickOTA = gui.Button("Get Devices Connected", width=200, height=30, margin='10px')
        self.verifyTGStickOTA.set_on_click_listener(self.on_VerfifyTGSTickOTA)
        self.OTAdialog.add_field("Devices Verification", self.verifyTGStickOTA)
        self.subContainerDevicesOTA.append(self.DevDetailsContainerOTA)
        self.subContainerDevicesOTA.append(self.TopDetailsContainerOTA)
        self.subContainerDevicesOTA.append(self.listDetailsContainerOTA)
        self.subContainerDevicesOTA.append(self.listDetailsContainerOTA)
        self.subContainerDevicesOTA.append(self.firmwareContainerOTA)
        self.consoleText = gui.TextInput(width='100%', height='100%')
        self.OTAdialog.add_field("container", self.horizontalContainerDialogOTA)
        self.horizontalContainerDialogOTA.append(self.subContainerDevicesOTA)
        self.horizontalContainerDialogOTA.append(self.subContainerfirmwareOTA)
        self.subContainerDevicesInnerConsole.append(self.consoleContainer)
        self.OTAdialog.add_field("Scenario", self.subContainerDevicesInnerOTA)
        self.OTAdialog.add_field("console", self.subContainerDevicesInnerConsole)
        self.OTAdialog.add_field("consoleText", self.consoleText)
        self.OTAdialog.show(self)

    def open_ZigbeeDump(self, widget):
        self.homePageNavaigation()
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m2 = gui.MenuItem('Zigbee Test', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m5 = gui.MenuItem('Config', width=100, height=30)
        m6 = gui.MenuItem('OTA Test', width=100, height=30)
        m7 = gui.MenuItem('LIVE', width=100, height=30)
        m8 = gui.MenuItem('STOP', width=100, height=30)
        m9 = gui.MenuItem('API', width=100, height=30)
        m10 = gui.MenuItem('API Test', width=100, height=30)
        m1.set_on_click_listener(self.homePage)
        m2.set_on_click_listener(self.menu_dialog_clicked)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m5.set_on_click_listener(self.open_Config)
        m6.set_on_click_listener(self.open_OTA)
        m7.set_on_click_listener(self.open_Terminal)
        m8.set_on_click_listener(self.killBatch)
        m9.set_on_click_listener(self.open_API)
        m10.set_on_click_listener(self.open_API_Test)
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
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)
        self.zDumpdialog.add_field("menu", menubar)
        self.dtextinput.set_value('Click on Verify Devices Connected')
        self.zDumpdialog.add_field_with_label('dtextinput', 'Status', self.dtextinput)
        self.verifyTGStickZDump = gui.Button("Get Devices Connected", width=200, height=30, margin='10px')
        self.verifyTGStickZDump.set_on_click_listener(self.on_VerfifyTGSTickZDump)
        self.zDumpdialog.add_field("Devices Verification", self.verifyTGStickZDump)
        self.subContainerDevicesZDump.append(self.DevDetailsContainerZDump)
        self.subContainerDevicesZDump.append(self.TopDetailsContainerZDump)
        self.subContainerDevicesZDump.append(self.listDetailsContainerZDump)
        self.subContainerDevicesZDump.append(self.listDetailsContainerZDump)
        self.subContainerDevicesZDump.append(self.firmwareContainerZDump)
        self.consoleText = gui.TextInput(width='100%', height='100%')
        self.zDumpdialog.add_field("container", self.horizontalContainerDialogZDump)
        self.horizontalContainerDialogZDump.append(self.subContainerDevicesZDump)
        self.horizontalContainerDialogZDump.append(self.subContainerfirmwareZDump)
        self.subContainerDevicesInnerConsole.append(self.consoleContainer)

        self.zDumpdialog.add_field("Dump", self.subContainerDumpZDump)
        self.zDumpdialog.add_field("Scenario", self.subContainerDevicesInnerZDump)
        self.zDumpdialog.add_field("console", self.subContainerDevicesInnerConsole)
        self.zDumpdialog.add_field("consoleText", self.consoleText)
        self.zDumpdialog.show(self)

    def open_rpiTest(self, widget):

        self.homePageNavaigation()
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m2 = gui.MenuItem('Zigbee Test', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m5 = gui.MenuItem('Config', width=100, height=30)
        m6 = gui.MenuItem('OTA Test', width=100, height=30)
        m7 = gui.MenuItem('LIVE', width=100, height=30)
        m8 = gui.MenuItem('STOP', width=100, height=30)
        m9 = gui.MenuItem('API', width=100, height=30)
        m10 = gui.MenuItem('API Test', width=100, height=30)
        m11 = gui.MenuItem('Zigbee Dump', width=100, height=30)
        m1.set_on_click_listener(self.homePage)
        m2.set_on_click_listener(self.menu_dialog_clicked)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m5.set_on_click_listener(self.open_Config)
        m6.set_on_click_listener(self.open_OTA)
        m7.set_on_click_listener(self.open_Terminal)
        m8.set_on_click_listener(self.killBatch)
        m9.set_on_click_listener(self.open_API)
        m10.set_on_click_listener(self.open_API_Test)
        m11.set_on_click_listener(self.open_ZigbeeDump)
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
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)
        self.rpiDialog.add_field("menu", menubar)
        self.dtextinput.set_value('Click on Verify Devices Connected')
        self.rpiDialog.add_field_with_label('dtextinput', 'Status', self.dtextinput)
        self.verifyTGStickRPI = gui.Button("Get RPI stats", width=200, height=30, margin='10px')
        self.verifyTGStickRPI.set_on_click_listener(self.on_getRPIStatus)

        self.rpiDialog.add_field("RPI Status", self.verifyTGStickRPI)
        self.rpiDialog.add_field_with_label(key="Execution Type",label_description="Execution Type",field=self.distributedExecution)
        self.consoleText = gui.TextInput(width='100%', height='100%')
        self.rpiDialog.add_field("container", self.horizontalContainerDialogRPI)
        self.horizontalContainerDialogRPI.append(self.subContainerDevicesRPI)
        self.subContainerDevicesInnerConsole.append(self.consoleContainer)

        #self.rpiDialog.add_field("Dump", self.subContainerDumpRPI)
        self.rpiDialog.add_field("Scenario", self.subContainerDevicesInnerRPI)
        self.subContainerLeft = gui.Widget(width=320)
        self.subContainerLeft.empty()
        self.subContainerRightRPI.empty()
        self.subContainerDevicesInnerConsoleRPI.empty()
        self.subContainerDevicesInnerConsoleRPI.append(self.subContainerLeft)
        self.subContainerDevicesInnerConsoleRPI.append(self.subContainerRightRPI)
        self.rpiDialog.add_field("console", self.subContainerDevicesInnerConsoleRPI)
        self.rpiDialog.add_field("consoleText", self.consoleText)
        #self.zDumpdialog.add_field("RPI1",self.rpi1)
        self.ReadFeatureFile(self.subContainerLeft,True)
        self.rpiDialog.show(self)

    def on_getRPIStatus(self, widget):
        self.dtextinput.set_value("Please Wait ...")
        self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
        self.dtextinput.redraw()
        self.getRPIStatus()

    def getRPIStatusThread(self):
        while True:
            self.getRPIStatus()
            time.sleep(10)

    def getRPIStatus(self):
        self.lstRPIurl = config.RPIURL
        #url = self.lstRPIurl["RPI1"]
        self.subContainerDevicesInnerRPI.empty()
        self.subContainerDumpRPI.empty()
        for oPi in self.lstRPIurl.keys():
            self.subContainerDumpRPI = gui.Widget(width='10%', layout_orientation=gui.Widget.LAYOUT_VERTICAL,
                                                    margin='0px')
            self.rpi1 = gui.Image('res/Inprogress.gif')
            url = self.lstRPIurl[oPi]
            status = ""
            try:
                r = requests.get(url + "/api/getStatus", timeout=5)
                print(r)
                if r.status_code == 200:
                    status = r.content
                    if r.content == b"" or r.content == b"completed" or r.content== b"Ready":
                        status = "Ready"
                        self.rpi1.attributes["src"] = 'res/Ready.png'
                    elif r.content == b"started" or r.content == b"running":

                        self.rpi1.attributes["src"] = 'res/Inprogress.gif'

            except:
                print(oPi)
                status = "offline"
                self.rpi1.attributes["src"] = 'res/Networkoffline.png'
            self.dtextinput.set_value("Completed")
            self.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
            self.subContainerDumpRPI.append(self.rpi1)
            self.subContainerDumpRPI.append(gui.Label(oPi))
            self.subContainerDumpRPI.append(gui.Label(status))
            self.subContainerDumpRPI.append(gui.CheckBoxLabel("select", False, user_data=oPi, width="100%", height="30px"))
            self.subContainerDevicesInnerRPI.append(self.subContainerDumpRPI)
            self.subContainerDumpRPI.redraw()
            self.subContainerDevicesInnerRPI.redraw()
        print("completed")

    listOption = ['ATI','AT+DASSL','AT+EN','REMOVE','AT+PJOIN','AT+JN','AT+READ','AT+BIND','AT+UNBIND','AT+BTABLE','AT+NTABLE'
                  ,'SET REPORTING','ON','OFF','AT+LCMTOLEV','AT+CCMVTOCT','AT+CCMVTOHUS']
    def open_Terminal(self, widget):
        self.homePageNavaigation()
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Home', width=100, height=30)
        m2 = gui.MenuItem('Zigbee Test', width=100, height=30)
        m3 = gui.MenuItem('Results Folder', width=100, height=30)
        m4 = gui.MenuItem('Latest Result', width=100, height=30)
        m5 = gui.MenuItem('Config', width=100, height=30)
        m6 = gui.MenuItem('OTA Test', width=100, height=30)
        m7 = gui.MenuItem('Zigbee Dump', width=100, height=30)
        m8 = gui.MenuItem('STOP', width=100, height=30)
        m9 = gui.MenuItem('API', width=100, height=30)
        m10 = gui.MenuItem('API Test', width=100, height=30)
        m1.set_on_click_listener(self.homePage)
        m2.set_on_click_listener(self.menu_dialog_clicked)
        m3.set_on_click_listener(self.open_resultsFolder)
        m4.set_on_click_listener(self.open_LatestResult)
        m5.set_on_click_listener(self.open_Config)
        m6.set_on_click_listener(self.open_OTA)
        m7.set_on_click_listener(self.open_ZigbeeDump)
        m8.set_on_click_listener(self.killBatch)
        m9.set_on_click_listener(self.open_API)
        m10.set_on_click_listener(self.open_API_Test)
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
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)
        self.liveDialog.add_field("menu", menubar)
        self.dtextinput.set_value('Click on Verify Devices Connected')
        self.liveDialog.add_field_with_label('dtextinput', 'Status', self.dtextinput)
        self.verifyTGStickLive = gui.Button("Get Devices Connected", width=200, height=30, margin='10px')
        self.verifyTGStickLive.set_on_click_listener(self.on_VerfifyTGSTickLive)
        self.liveDialog.add_field("Devices Verification", self.verifyTGStickLive)
        self.subContainerDevicesLive.append(self.DevDetailsContainerLive)
        self.subContainerDevicesLive.append(self.TopDetailsContainerLive)
        self.subContainerDevicesLive.append(self.listDetailsContainerLive)
        self.subContainerDevicesLive.append(self.listClusterContainerLive)
        self.subContainerDevicesLive.append(self.listAttrContainerLive)
        self.subContainerDevicesLive.append(self.firmwareContainerLive)
        self.consoleText = gui.TextInput(width='100%', height='100%')
        self.liveDialog.add_field("container", self.horizontalContainerDialogLive)
        self.subContainerDevicesInnerConsoleLive.append(self.subContainerDevicesInnerConsole)
        self.subContainerDevicesInnerConsoleLive.append(self.subContainerVerticalLive)
        self.horizontalContainerDialogLive.append(self.subContainerDevicesLive)
        self.subContainerDevicesInnerConsole.append(self.consoleContainer)
        self.liveDialog.add_field("Dump", self.subContainerDumpLive)
        self.liveDialog.add_field("Scenario", self.subContainerDevicesInnerLive)
        self.liveDialog.add_field("console", self.subContainerDevicesInnerConsoleLive)
        #self.liveDialog.add_field("co", self.subContainerVerticalLive)
        self.subContainerVerticalLive.empty()
        self.liveDialog.add_field("consoleText", self.consoleText)
        self.tabless = gui.ListView(True).new_from_list(self.listOption, width='100%')
        self.tabless.set_on_selection_listener(self.on_table_row_click)
        self.subContainerVerticalLive.append(self.tabless)
        self.liveDialog.show(self)

    def on_table_row_click(self, widget, selected_item_key):
        if len(self.DevDetailsContainerLive.children) == 0:
            MyApp.execute_javascript(self, code="alert('Click on get connected devices');")
            return
        if self.btnFirmwareLive.get_text() == "Start":
            MyApp.execute_javascript(self, code="alert('Select any device and Click on start button');")
            return
        MacAddress = ""
        for i in range(0, 4):
            temp = self.listDetailsLive.children[list(self.listDetailsLive.children)[i]].children['text'].replace("\'",
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
        try:
            strCluster = self.listClusterContainerLive.children[
                list(self.listClusterContainerLive.children.keys())[0]]._selected_item.children['text']
            strType = str(strCluster).split(" - ")[2].replace("(", "").replace(")", "")
            try:
                strAttr = self.listAttrContainerLive.children[
                    list(self.listAttrContainerLive.children.keys())[0]]._selected_item.children['text']
            except:
                strAttr = self.listAttrContainerLive.children[
                    list(self.listAttrContainerLive.children.keys())[1]]._selected_item.children['text']
            strCluster = str(strCluster).split(" - ")[0]
        except:
            pass
        try:
            strAttr = str(strAttr).split(" - ")[0]
        except:pass
        if 'ATI' in str(widget.children[selected_item_key].get_text()):
            AT.sendCommand("ATI","OK",2,1)
        if 'AT+DASSL' in str(widget.children[selected_item_key].get_text()):
            AT.sendCommand("AT+DASSL","OK",2,1)
        if 'REMOVE' in str(widget.children[selected_item_key].get_text()):
            AT.sendCommand("AT+DASSR:"+nodeid,"OK",2,5)
        if 'AT+PJOIN' in str(widget.children[selected_item_key].get_text()):
            AT.sendCommand("AT+PJOIN","OK",1,1)
        if 'AT+EN' in str(widget.children[selected_item_key].get_text()):
            AT.sendCommand("AT+EN", 'JPAN:(..)', 2, 1)
        if 'AT+READ' in str(widget.children[selected_item_key].get_text()):
            msg, exp = AT.buildGetAttributeCommands(nodeid, ep,strCluster
            ,strAttr,strType)
            AT.sendCommand(msg, exp, 2, 1)
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
            self.consoleContainer.append(btab)
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
            self.consoleContainer.append(ntab)
        if 'SET REPORTING' in str(widget.children[selected_item_key].get_text()):
            AT.setAttributeReporting(nodeid,ep,strCluster,strAttr,self.txtMinRepo.get_text(),self.txtMaxRepo.get_text(),1)
        if str(widget.children[selected_item_key].get_text()) == 'ON':
            utils.setOnOff(nodeid,ep,'ON',True)
        if str(widget.children[selected_item_key].get_text()) == 'OFF':
            utils.setOnOff(nodeid,ep,'OFF',True)

    def homePage(self, widget):
        self.homePageNavaigation()

    def homePageNavaigation(self):
        try:
            self.dialog.cancel_dialog()
        except:
            pass
        try:
            self.configDialog.cancel_dialog()
        except:
            pass
        try:
            self.OTAdialog.cancel_dialog()
        except:
            pass
        try:
            self.zDumpdialog.cancel_dialog()
        except:
            pass
        try:
            self.liveDialog.cancel_dialog()
        except:
            pass
        try:
            self.apiDialog.cancel_dialog()
        except:
            pass
        try:
            self.apiTestDialog.cancel_dialog()
        except:
            pass
        try:
            self.rpiDialog.cancel_dialog()
        except:
            pass
        try:
            AT.stopThreads()
        except:
            pass
        try:
            self.consoleContainer.empty()
            self.subContainerDevicesInnerConsole.empty()
            self.subContainerDevicesInnerConsole.append(self.consoleContainer)
            self.consoleText.set_text("")
            lbl = gui.Label("Start")
            self.consoleContainer.append(lbl)
        except:
            pass

    def refreshzigbeeTest(self, widget=None, selected_item_key=None):
        strDeviceName = ""
        if widget is not None and selected_item_key is not None:
            self.dtextinput.set_value(str(widget.children[selected_item_key].get_text()).split("-")[0])
            self.dtextinput.style['background-color'] = 'rgb(232, 242, 255)'
            strDeviceName = str(widget.children[selected_item_key].get_text()).split("-")[0]
        else:
            strDeviceName = self.dtextinput.get_text().replace(" ", "")
        self.subContainerDevicesInner.empty()
        self.subContainerDevicesInner.redraw()
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
                                    btn = gui.Button(tag, width=200, height=30, margin='10px')
                                    btn.set_on_click_listener(self.on_runTest)
                                    self.subContainerDevicesInner.append(btn)
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
                                self.subContainerDevicesInner.append(tbl)
                                Tableflag = False
                                continueFlag = False
                                counter = 0
                                TableList.clear()
                            txt = gui.Label(line, width='100%')
                            subTxt = gui.Widget(width='100%')
                            if ("#" in line):
                                subTxt.style['color'] = 'rgb(32, 94, 15)'
                                subTxt.style['font-size'] = '10px'
                            if ("Feature" in line):
                                subTxt.style['color'] = 'rgb(130, 9, 9)'
                                subTxt.style['font-weight'] = 'bold'
                            if ("Scenario" in line):
                                subTxt.style['color'] = 'rgb(193, 81, 1)'
                                subTxt.style['font-weight'] = 'bold'
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
                            self.subContainerDevicesInner.append(subTxt)
        self.subContainerDevicesInnerConsole.redraw()
        self.firmwareContainer.empty()
        self.firmwareContainer.redraw()
        self.upgradeVersion.set_text(upgradeVersion)
        self.DowngradeVersion.set_text(downgradeVersion)
        self.upgradeVersionTxt = gui.Label("Upgrade Version")
        self.downgradeVersionTxt = gui.Label("Downgrade Version")
        self.upContainer = gui.Widget(width='100%')
        self.upContainer.append(self.upgradeVersionTxt)
        self.upContainer.append(self.upgradeVersion)
        self.downContainer = gui.Widget(width='100%')
        self.downContainer.append(self.downgradeVersionTxt)
        self.downContainer.append(self.DowngradeVersion)
        self.changeFirmware = gui.Button("Replace " + strDeviceName + " firmware", width='100%')
        self.changeFirmware.set_on_click_listener(self.changeFirmawares)
        self.firmwareContainer.append(self.upContainer)
        self.firmwareContainer.append(self.downContainer)
        self.firmwareContainer.append(self.changeFirmware)
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
            self.listDetailsContainer.empty()
            self.listDetailsContainer.redraw()
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
            self.listDetails.new_from_list(listItems)
            self.listDetailsContainer.append(self.listDetails)

            btn = gui.Button("Replace " + oJson[
                str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(", "").replace(")", "")][
                'macID'] + " for " + oJson[
                                 str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(",
                                                                                                          "").replace(
                                     ")", "")]['name'] + " Mac ID")
            btn.set_on_click_listener(self.on_ReplaceMac)
            self.listDetailsContainer.append(btn)

    def refreshzigbeeTestOTA(self, widget=None, selected_item_key=None):
        strDeviceName = ""
        if widget is not None and selected_item_key is not None:
            self.dtextinput.set_value(str(widget.children[selected_item_key].get_text()).split("-")[0])
            self.dtextinput.style['background-color'] = 'rgb(232, 242, 255)'
            strDeviceName = str(widget.children[selected_item_key].get_text()).split("-")[0]
        else:
            strDeviceName = self.dtextinput.get_text().replace(" ", "")
        self.subContainerDevicesInnerOTA.empty()
        self.subContainerDevicesInnerOTA.redraw()
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
            self.listDetailsContainerOTA.empty()
            self.listDetailsContainerOTA.redraw()
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
            self.listDetailsOTA = gui.ListView(True).new_from_list(listItems)
            self.listDetailsContainerOTA.append(self.listDetailsOTA)

    def refreshzigbeeTestZDump(self, widget=None, selected_item_key=None):
        strDeviceName = ""
        if widget is not None and selected_item_key is not None:
            self.dtextinput.set_value(str(widget.children[selected_item_key].get_text()).split("-")[0])
            self.dtextinput.style['background-color'] = 'rgb(232, 242, 255)'
            strDeviceName = str(widget.children[selected_item_key].get_text()).split("-")[0]
        else:
            strDeviceName = self.dtextinput.get_text().replace(" ", "")
        self.subContainerDevicesInnerZDump.empty()
        self.subContainerDevicesInnerZDump.redraw()
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
            self.listDetailsContainerZDump.empty()
            self.listDetailsContainerZDump.redraw()
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
            self.listDetailsZDump = gui.ListView(True).new_from_list(listItems)
            self.listDetailsContainerZDump.append(self.listDetailsZDump)

    def refreshzigbeeTestLive(self, widget=None, selected_item_key=None):
        strDeviceName = ""
        if widget is not None and selected_item_key is not None:
            self.dtextinput.set_value(str(widget.children[selected_item_key].get_text()).split("-")[0])
            self.dtextinput.style['background-color'] = 'rgb(232, 242, 255)'
            strDeviceName = str(widget.children[selected_item_key].get_text()).split("-")[0]
        else:
            strDeviceName = self.dtextinput.get_text().replace(" ", "")
        self.subContainerDevicesInnerLive.empty()
        self.subContainerDevicesInnerLive.redraw()
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
            self.listDetailsContainerLive.empty()
            self.listDetailsContainerLive.redraw()
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
            self.listDetailsLive = gui.ListView(True).new_from_list(listItems)
            self.listDetailsContainerLive.append(self.listDetailsLive)
            baselineDumpFile = os.path.abspath(
                __file__ +"/../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/" + oJson[
                    str(widget.children[selected_item_key].get_text()).split("-")[1].replace("(", "").replace(")", "")][
                    'name'] + "_Baseline_Dump.json"
            oJsonCluster = open(baselineDumpFile, mode='r')
            oBSDumpJson = json.loads(oJsonCluster.read())
            lstClister = []
            oJsonCluster.close()
            self.listClusterContainerLive.empty()
            for ep in sorted(oBSDumpJson["ListOfEndPoints"].keys()):
                oEP = oBSDumpJson["ListOfEndPoints"][ep]
                strExpEndPoint = oEP["EndPoint"]
                for oClust in sorted(oEP["ListOfClusters"].keys()):
                    oClust = oEP["ListOfClusters"][oClust]
                    strExpClusterID = oClust["ClusterID"]
                    strExpClusterName = oClust["ClusterName"]
                    strExpClusterTYpe = oClust["ClusterType"]
                    lstClister.append(strExpClusterID +" - "+strExpClusterName+" - ("+strExpClusterTYpe+")")
            self.listDetailsClusterLive = gui.ListView(True).new_from_list(lstClister)
            self.listDetailsClusterLive.set_on_selection_listener(self.list_view_attr_on_selected)
            self.listClusterContainerLive.append(self.listDetailsClusterLive)

    def list_view_attr_on_selected(self, widget, selected_item_key):
        self.listAttrContainerLive.empty()
        oJson = dUtils.getZigbeeDevicesJson()
        baselineDumpFile = os.path.abspath(
            __file__ + "/../") + "/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/" + self.dtextinput.get_text() + "_Baseline_Dump.json"
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
        self.listDetailsAttrLive = gui.ListView(True).new_from_list(lstAttr)
        self.listAttrContainerLive.append(self.listDetailsAttrLive)
        self.listAttrContainerRepoLive.empty()
        lbl1 = gui.Label("Min Report(hex)")
        self.txtMinRepo =  gui.TextInput(True)
        lbl2 = gui.Label("Min Report(hex)")
        self.txtMaxRepo =  gui.TextInput(True)
        self.listAttrContainerRepoLive.append(lbl1 )
        self.listAttrContainerRepoLive.append(self.txtMinRepo )
        self.listAttrContainerRepoLive.append(lbl2)
        self.listAttrContainerRepoLive.append(self.txtMaxRepo)
        self.listAttrContainerLive.append(self.listAttrContainerRepoLive)

    def list_view_on_selected(self, widget, selected_item_key):
        self.refreshzigbeeTest(widget, selected_item_key)

    def list_view_on_selectedOTA(self, widget, selected_item_key):
        self.refreshzigbeeTestOTA(widget, selected_item_key)

    def list_view_on_selectedZDump(self, widget, selected_item_key):
        self.refreshzigbeeTestZDump(widget, selected_item_key)

    def list_view_on_selectedLive(self, widget, selected_item_key):
        self.refreshzigbeeTestLive(widget, selected_item_key)

    def changeFirmawares(self, widget):
        if self.upgradeVersion.get_text().replace(" ", "") == "":
            return
        if self.DowngradeVersion.get_text().replace(" ", "") == "":
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
                                                    self.upgradeVersion.get_text().replace(" ", ""))
                        filedata = filedata.replace(downgradeVersion.replace(" ", ""),
                                                    self.DowngradeVersion.get_text().replace(" ", ""))
                    with open(root + "/" + file, 'w') as f:
                        f.write(filedata)
        self.refreshzigbeeTest(widget=None, selected_item_key=None)

    def on_ReplaceMac(self, widget):
        btnText = str(widget.get_text()).split(" ")
        fileName = btnText[(len(btnText) - 3)]
        btnMac = btnText[1]
        self.subContainerDevicesInner.empty()
        self.subContainerDevicesInner.redraw()
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
        strDeviceName = self.dtextinput.get_text().replace(" ", "")
        self.subContainerDevicesInner.empty()
        self.subContainerDevicesInner.redraw()
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
                                    btn = gui.Button(tag, width=200, height=30, margin='10px')
                                    btn.set_on_click_listener(self.on_runTest)
                                    self.subContainerDevicesInner.append(btn)
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
                                self.subContainerDevicesInner.append(tbl)
                                Tableflag = False
                                continueFlag = False
                                counter = 0
                                TableList.clear()
                            txt = gui.Label(line, width='100%')
                            subTxt = gui.Widget(width='100%')
                            if ("#" in line):
                                subTxt.style['color'] = 'rgb(32, 94, 15)'
                                subTxt.style['font-size'] = '10px'
                            if ("Feature" in line):
                                subTxt.style['color'] = 'rgb(130, 9, 9)'
                                subTxt.style['font-weight'] = 'bold'
                            if ("Scenario" in line):
                                subTxt.style['color'] = 'rgb(193, 81, 1)'
                                subTxt.style['font-weight'] = 'bold'
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
                            self.subContainerDevicesInner.append(subTxt)

    def getNodes(self, widget):
        try:
            self.dtextinput.set_value("Please Wait ...")
            self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
            oFileName = "getNodes.command"
            if "WINDOWS" in self.OS:
                oFileName = "getNodes_WIN.bat"
            if "LINUX" in self.OS:
                oFileName = "getNodes.sh"
            for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
                for file in files:
                    if file.endswith(oFileName):
                        if "WINDOWS" in self.OS:
                            self.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        else:
                            self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        # print("pid = " + str(self.p.pid) + "\n")
                        temp = ''
                        tempInner = ''
                        self.consoleContainer.empty()
                        while True:
                            if self.flag:
                                print("\nstopped by API\n")
                                break
                            out = self.p.stdout.read(1)
                            if out == '' and self.p.poll() != None:
                                # self.p.kill()
                                break
                            if out != '':
                                sys.stdout.write(out.decode('utf-8'))
                                # self.consoleText.set_text(temp)
                                if '\n' in tempInner:
                                    lbl = gui.Label(tempInner, width='100%')
                                    if ("DEBUG Tx:" in tempInner):
                                        lbl.style['color'] = 'rgb(30, 104, 46)'
                                        lbl.style['font-size'] = '12px'
                                    if ("DEBUG RX:" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                    if ("ERROR" in tempInner.upper() or "NACK" in tempInner.upper()):
                                        lbl.style['color'] = 'rgb(99, 7, 7)'
                                        lbl.style['font-size'] = '12px'
                                    self.consoleText.set_text(temp)
                                    self.consoleContainer.append(lbl)
                                    self.consoleContainer.redraw()
                                    # self.horizontalContainerDialog.redraw()
                                    tempInner = ''
                                temp = temp + out.decode('utf-8')
                                tempInner = tempInner + out.decode('utf-8')
                                if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp or 'Done' in temp:
                                    self.p.kill()
                                    # AT.stopThreads()
                                    break
                                sys.stdout.flush()
                        # try:
                        #     AT.stopThreads()
                        #     strStatus = AT.startSerialThreadsReturn(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                        # except:
                        #     strStatus = AT.startSerialThreadsReturn(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                        strStatus = "Please Wait ..."
                        if 'Error opening port' in temp:
                            self.dtextinput.set_value("Error : Please connect TG STick")
                            self.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
                            try:
                                AT.stopThreads()
                            except:
                                pass
                        else:
                            self.dtextinput.set_value("Please Wait ...")
                            self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
                            self.consoleText = gui.TextInput(width='100%', height='100%')
                            self.consoleContainer.append(self.consoleText)

                            self.consoleText.set_text("")
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
                            self.DevDetailsContainer.empty()
                            self.DevDetailsContainer.redraw()
                            self.dtextinput.set_value("Completed")
                            self.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                            # self.horizontalContainerDialog.empty()
                            # self.horizontalContainerDialog.redraw()

                            txt = gui.ListView(True).new_from_list(listItems, width='100%')
                            txt.set_on_selection_listener(self.list_view_on_selected)
                            self.DevDetailsContainer.append(txt)
                            self.DevDetailsContainer.redraw()
                            self.TopDetailsContainer.empty()
                            self.TopDetailsContainer.redraw()
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
                            lstTop = gui.ListView(True).new_from_list(oDictTopology, width='100%')

                            self.TopDetailsContainer.append(lstTop)
                            self.TopDetailsContainer.redraw()
                        break
        except:
            self.dtextinput.set_value("Error")
            self.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'

    def getNodesOTA(self, widget):
        try:
            self.dtextinput.set_value("Please Wait ...")
            self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
            oFileName = "getNodes.command"
            # self.subContainerDevicesInnerConsole.children.clear()
            self.consoleContainer.empty()
            if "WINDOWS" in self.OS:
                oFileName = "getNodes_WIN.bat"
            if "LINUX" in self.OS:
                oFileName = "getNodes.sh"
            for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
                for file in files:
                    if file.endswith(oFileName):
                        if "WINDOWS" in self.OS:
                            self.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        else:
                            self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        # print("pid = " + str(self.p.pid) +"\n")
                        temp = ''
                        tempInner = ''
                        self.consoleContainer.empty()
                        while True:
                            if self.flag:
                                print("\nstopped by API\n")
                                break
                            out = self.p.stdout.read(1)
                            if out == '' and self.p.poll() != None:
                                # self.p.kill()
                                break
                            if out != '':
                                sys.stdout.write(out.decode('utf-8'))
                                # self.consoleText.set_text(temp)
                                if '\n' in tempInner:
                                    lbl = gui.Label(tempInner, width='100%')
                                    if ("DEBUG Tx:" in tempInner):
                                        lbl.style['color'] = 'rgb(30, 104, 46)'
                                        lbl.style['font-size'] = '12px'
                                    if ("DEBUG RX:" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                    if ("ERROR" in tempInner.upper() or "NACK" in tempInner.upper()):
                                        lbl.style['color'] = 'rgb(99, 7, 7)'
                                        lbl.style['font-size'] = '12px'
                                    self.consoleText.set_text(temp)
                                    self.consoleContainer.append(lbl)
                                    self.consoleContainer.redraw()
                                    # self.horizontalContainerDialog.redraw()
                                    tempInner = ''
                                temp = temp + out.decode('utf-8')
                                tempInner = tempInner + out.decode('utf-8')
                                if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp or 'Done' in temp:
                                    self.p.kill()
                                    # AT.stopThreads()
                                    break
                                sys.stdout.flush()
                        # try:
                        #     AT.stopThreads()
                        #     strStatus = AT.startSerialThreadsReturn(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                        # except:
                        #     strStatus = AT.startSerialThreadsReturn(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                        strStatus = "Please Wait ..."
                        if 'Error opening port' in temp:
                            self.dtextinput.set_value("Error : Please connect TG STick")
                            self.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
                            try:
                                AT.stopThreads()
                            except:
                                pass
                        else:
                            self.dtextinput.set_value("Please Wait ...")
                            self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
                            self.consoleText = gui.TextInput(width='100%', height='100%')
                            self.consoleContainer.append(self.consoleText)

                            self.consoleText.set_text("")
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
                            self.DevDetailsContainerOTA.empty()
                            self.DevDetailsContainerOTA.redraw()
                            self.dtextinput.set_value("Completed")
                            self.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                            # self.horizontalContainerDialog.empty()
                            # self.horizontalContainerDialog.redraw()

                            txt = gui.ListView(True).new_from_list(listItems, width='100%')
                            txt.set_on_selection_listener(self.list_view_on_selectedOTA)
                            self.DevDetailsContainerOTA.append(txt)
                            self.DevDetailsContainerOTA.redraw()
                            self.TopDetailsContainerOTA.empty()
                            self.TopDetailsContainerOTA.redraw()
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
                            lstTop = gui.ListView(True).new_from_list(oDictTopology, width='100%')

                            self.TopDetailsContainerOTA.append(lstTop)
                            self.TopDetailsContainerOTA.redraw()
                        break
        except:
            self.dtextinput.set_value("Error")
            self.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'

    def getNodesZDump(self, widget):
        try:
            self.dtextinput.set_value("Please Wait ...")
            self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
            oFileName = "getNodes.command"
            # self.subContainerDevicesInnerConsole.children.clear()
            self.consoleContainer.empty()
            if "WINDOWS" in self.OS:
                oFileName = "getNodes_WIN.bat"
            if "LINUX" in self.OS:
                oFileName = "getNodes.sh"
            for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
                for file in files:
                    if file.endswith(oFileName):
                        if "WINDOWS" in self.OS:
                            self.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        else:
                            self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        # print("pid = " + str(self.p.pid) +"\n")
                        temp = ''
                        tempInner = ''
                        self.consoleContainer.empty()
                        while True:
                            if self.flag:
                                print("\nstopped by API\n")
                                break
                            out = self.p.stdout.read(1)
                            if out == '' and self.p.poll() != None:
                                # self.p.kill()
                                break
                            if out != '':
                                sys.stdout.write(out.decode('utf-8'))
                                # self.consoleText.set_text(temp)
                                if '\n' in tempInner:
                                    lbl = gui.Label(tempInner, width='100%')
                                    if ("DEBUG Tx:" in tempInner):
                                        lbl.style['color'] = 'rgb(30, 104, 46)'
                                        lbl.style['font-size'] = '12px'
                                    if ("DEBUG RX:" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                    if ("ERROR" in tempInner.upper() or "NACK" in tempInner.upper()):
                                        lbl.style['color'] = 'rgb(99, 7, 7)'
                                        lbl.style['font-size'] = '12px'
                                    self.consoleText.set_text(temp)
                                    self.consoleContainer.append(lbl)
                                    self.consoleContainer.redraw()
                                    #self.horizontalContainerDialogZDump.redraw()
                                    tempInner = ''
                                temp = temp + out.decode('utf-8')
                                tempInner = tempInner + out.decode('utf-8')
                                if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp or 'Done' in temp:
                                    self.p.kill()
                                    # AT.stopThreads()
                                    break
                                sys.stdout.flush()
                        # try:
                        #     AT.stopThreads()
                        #     strStatus = AT.startSerialThreadsReturn(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                        # except:
                        #     strStatus = AT.startSerialThreadsReturn(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                        strStatus = "Please Wait ..."
                        if 'Error opening port' in temp:
                            self.dtextinput.set_value("Error : Please connect TG STick")
                            self.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
                            try:
                                AT.stopThreads()
                            except:
                                pass
                        else:
                            self.dtextinput.set_value("Please Wait ...")
                            self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
                            self.consoleText = gui.TextInput(width='100%', height='100%')
                            self.consoleContainer.append(self.consoleText)

                            #self.consoleText.set_text("")
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
                            self.DevDetailsContainerZDump.empty()
                            self.DevDetailsContainerZDump.redraw()
                            self.dtextinput.set_value("Completed")
                            self.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                            # self.horizontalContainerDialog.empty()
                            # self.horizontalContainerDialog.redraw()

                            txt = gui.ListView(True).new_from_list(listItems, width='100%')
                            txt.set_on_selection_listener(self.list_view_on_selectedZDump)
                            self.DevDetailsContainerZDump.append(txt)
                            self.DevDetailsContainerZDump.redraw()
                            self.TopDetailsContainerZDump.empty()
                            self.TopDetailsContainerZDump.redraw()
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
                            lstTop = gui.ListView(True).new_from_list(oDictTopology, width='100%')

                            self.TopDetailsContainerZDump.append(lstTop)
                            self.TopDetailsContainerZDump.redraw()
                        break
        except:
            self.dtextinput.set_value("Error")
            self.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'

    def getNodesLive(self, widget):
        try:
            if self.btnFirmwareLive.get_text() == "Stop":
                MyApp.execute_javascript(self, code="alert('Click on Stop to get connected devices');")
                return
            time.sleep(2)
            self.dtextinput.set_value("Please Wait ...")
            self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
            oFileName = "getNodes.command"
            # self.subContainerDevicesInnerConsole.children.clear()
            self.consoleContainer.empty()
            if "WINDOWS" in self.OS:
                oFileName = "getNodes_WIN.bat"
            if "LINUX" in self.OS:
                oFileName = "getNodes.sh"
            for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)).split("/03_Results_Tier")[0]):
                for file in files:
                    if file.endswith(oFileName):
                        if "WINDOWS" in self.OS:
                            self.p = subprocess.Popen(root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        else:
                            self.p = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True,
                                                      stdout=subprocess.PIPE)
                        # print("pid = " + str(self.p.pid) +"\n")
                        temp = ''
                        tempInner = ''
                        self.consoleContainer.empty()
                        while True:
                            if self.flag:
                                print("\nstopped by API\n")
                                break
                            out = self.p.stdout.read(1)
                            if out == '' and self.p.poll() != None:
                                # self.p.kill()
                                break
                            if out != '':
                                sys.stdout.write(out.decode('utf-8'))
                                # self.consoleText.set_text(temp)
                                if '\n' in tempInner:
                                    lbl = gui.Label(tempInner, width='100%')
                                    if ("DEBUG Tx:" in tempInner):
                                        lbl.style['color'] = 'rgb(30, 104, 46)'
                                        lbl.style['font-size'] = '12px'
                                    if ("DEBUG RX:" in tempInner):
                                        lbl.style['color'] = 'rgb(44, 55, 130)'
                                        lbl.style['font-size'] = '12px'
                                    if ("ERROR" in tempInner.upper() or "NACK" in tempInner.upper()):
                                        lbl.style['color'] = 'rgb(99, 7, 7)'
                                        lbl.style['font-size'] = '12px'
                                    self.consoleText.set_text(temp)
                                    self.consoleContainer.append(lbl)
                                    self.consoleContainer.redraw()
                                    #self.horizontalContainerDialogLive.redraw()
                                    tempInner = ''
                                temp = temp + out.decode('utf-8')
                                tempInner = tempInner + out.decode('utf-8')
                                if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp or 'Done' in temp:
                                    self.p.kill()
                                    # AT.stopThreads()
                                    break
                                sys.stdout.flush()
                        # try:
                        #     AT.stopThreads()
                        #     strStatus = AT.startSerialThreadsReturn(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                        # except:
                        #     strStatus = AT.startSerialThreadsReturn(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
                        strStatus = "Please Wait ..."
                        if 'Error opening port' in temp:
                            self.dtextinput.set_value("Error : Please connect TG STick")
                            self.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'
                            try:
                                AT.stopThreads()
                            except:
                                pass
                        else:
                            self.dtextinput.set_value("Please Wait ...")
                            self.dtextinput.style['background-color'] = 'rgb(255, 211, 102)'
                            self.consoleText = gui.TextInput(width='100%', height='100%')
                            self.consoleContainer.append(self.consoleText)

                            #self.consoleText.set_text("")
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
                            self.DevDetailsContainerLive.empty()
                            self.DevDetailsContainerLive.redraw()
                            self.dtextinput.set_value("Completed")
                            self.dtextinput.style['background-color'] = 'rgb(77, 209, 90)'
                            # self.horizontalContainerDialog.empty()
                            # self.horizontalContainerDialog.redraw()

                            txt = gui.ListView(True).new_from_list(listItems, width='100%')
                            txt.set_on_selection_listener(self.list_view_on_selectedLive)
                            self.DevDetailsContainerLive.append(txt)
                            self.DevDetailsContainerLive.redraw()
                            self.TopDetailsContainerLive.empty()
                            self.TopDetailsContainerLive.redraw()
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
                            lstTop = gui.ListView(True).new_from_list(oDictTopology, width='100%')

                            self.TopDetailsContainerLive.append(lstTop)
                            self.TopDetailsContainerLive.redraw()
                        break
        except:
            self.dtextinput.set_value("Error")
            self.dtextinput.style['background-color'] = 'rgb(255, 0, 89)'

    def killProcess(self):
        try:
            pid = self.p.pid
            oFileName = "killProcess.command"
            if "WINDOWS" in self.OS:
                oFileName = "killProcess_WIN.bat"
            if "LINUX" in self.OS:
                oFileName = "killProcess.sh"
            for root, dirs, files in os.walk(
                    os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
                for file in files:
                    if file.endswith(oFileName):
                        with open(root + "/" + file, 'w') as f:
                            f.write("#!/bin/sh \n")
                            f.write('ps -T -p ' + str(pid) + '\n')
                        if "WINDOWS" in self.OS:
                            t = subprocess.Popen(root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                        else:
                            t = subprocess.Popen('sh ' + root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                        temp = ''
                        tempInner = ''
                        self.consoleContainer.empty()
                        while True:
                            if self.flag:
                                print("\nstopped by API\n")
                                break
                            out = t.stdout.read(1)
                            if out == '' and t.poll() != None:
                                # self.p.kill()
                                break
                            if out != '':
                                sys.stdout.write(out.decode('utf-8'))
                                self.consoleText.set_text(temp)
                                if '\n' in tempInner and "PID" not in tempInner:
                                    self.kill = subprocess.Popen('pkill ' + tempInner.split(" ")[0], shell=True,
                                                                 stdout=subprocess.PIPE)
                                    tempInner = ''
                                temp = temp + out.decode('utf-8')
                                tempInner = tempInner + out.decode('utf-8')
                                if "ipdb>" in temp or 'Error opening port' in temp or 'Took ' in temp or 'Done' in temp:
                                    t.kill()
                                    # AT.stopThreads()
                                    break
                                sys.stdout.flush()
            self.kill = subprocess.Popen('pkill ' + str(pid), shell=True, stdout=subprocess.PIPE)
            self.oThread.join(1)
            time.sleep(1)
        except:
            pass

    def on_VerfifyTGSTick(self, widget):
        try:
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e bash | awk '{ print $2 }')", shell=True, stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e sh | awk '{ print $2 }')", shell=True,
            #                      stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e Python | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e python3.5 | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e sh | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e /dev/tty.SLAB_USBtoUART | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e getNodes.py | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e getNodes.command | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e mdworker | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e bash | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("ps -ef | grep getNode.py | grep -v \"grep\" | awk '{print $2}' | xargs kill;", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("ps -ef | grep getNode.command | grep -v \"grep\" | awk '{print $2}' | xargs kill;", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill "+self.p.pid, shell=True,
            #                       stdout=subprocess.PIPE)
            # self.oThread.join(timeout=1)
            # time.sleep(1)
            # if self.oThread.is_alive():
            #     self.oThread.join(timeout=1)
            #     os.kill(self.p.pid, signal.SIGKILL)
            #     os.kill(self.p.pid, signal.SIGTERM)
            #
            #
            # while not self.p.poll():
            #     self.p.terminate()
            #     self.p.kill()
            # print('hi')
            # self.oThreadKill = threading.Thread(target=self.killProcess)
            # self.oThreadKill.start()

            try:
                self.p.terminate()
                self.p.kill()
            except:
                pass
            self.killBatch()
            self.oThread = start_new_thread(target=self.getNodes, args=(widget,))
            self.flag = False
            self.oThread.setDaemon(True)
            self.oThread.start()
        except:
            pass

    def on_VerfifyTGSTickOTA(self, widget):
        try:
            self.killBatch()
            try:
                self.p.terminate()
                self.p.kill()
            except:
                pass

            self.oThread = start_new_thread(target=self.getNodesOTA, args=(widget,))
            self.flag = False
            self.oThread.setDaemon(True)
            self.oThread.start()
        except:
            pass

    def on_VerfifyTGSTickZDump(self, widget):
        try:
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e bash | awk '{ print $2 }')", shell=True, stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e sh | awk '{ print $2 }')", shell=True,
            #                      stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e Python | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e python3.5 | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e sh | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e /dev/tty.SLAB_USBtoUART | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e getNodes.py | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e getNodes.command | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e mdworker | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill -9 $(ps aux | grep -e bash | awk '{ print $2 }')", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("ps -ef | grep getNode.py | grep -v \"grep\" | awk '{print $2}' | xargs kill;", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("ps -ef | grep getNode.command | grep -v \"grep\" | awk '{print $2}' | xargs kill;", shell=True,
            #                       stdout=subprocess.PIPE)
            # pK = subprocess.Popen("kill "+self.p.pid, shell=True,
            #                       stdout=subprocess.PIPE)
            # self.oThread.join(timeout=1)
            # time.sleep(1)
            # if self.oThread.is_alive():
            #     self.oThread.join(timeout=1)
            #     os.kill(self.p.pid, signal.SIGKILL)
            #     os.kill(self.p.pid, signal.SIGTERM)
            #
            #
            # while not self.p.poll():
            #     self.p.terminate()
            #     self.p.kill()
            # print('hi')
            # self.oThreadKill = threading.Thread(target=self.killProcess)
            # self.oThreadKill.start()

            try:
                self.p.terminate()
                self.p.kill()
            except:
                pass
            self.killBatch()
            self.oThread = start_new_thread(target=self.getNodesZDump, args=(widget,))
            self.flag = False
            self.oThread.setDaemon(True)
            self.oThread.start()
        except:
            pass

    def on_VerfifyTGSTickLive(self, widget):
        try:
            try:
                self.p.terminate()
                self.p.kill()
            except:
                pass
            self.killBatch()
            self.oThread = start_new_thread(target=self.getNodesLive, args=(widget,))
            self.flag = False
            self.oThread.setDaemon(True)
            self.oThread.start()
        except:
            pass

    def killBatch(self, widget=None):
        '''try:
            self.p.terminate()
            self.p.kill()
            threading._shutdown()

            try:
                if self.oThread.isAlive():
                    self.oThread._stop()
                if self.oThread2.isAlive():
                    self.oThread2._stop()
            except:
                pass
        except:
            pass
        try:
            if self.oThread.isAlive():
                exc = ctypes.py_object(SystemExit)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(self.oThread.ident), exc)
                if res == 0:
                    raise ValueError("nonexistent thread id")
                elif res > 1:
                    # """if it returns a number greater than one, you're in trouble,
                    # and you should call it again with exc=NULL to revert the effect"""
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(self.oThread.ident, None)
                    raise SystemError("PyThreadState_SetAsyncExc failed")
        except:
            pass
        oFileName = "killProcesses.command"
        if "WINDOWS" in self.OS:
            oFileName = "killProcesses_WIN.bat"
        if "LINUX" in self.OS:
            oFileName = "killProcesses.sh"
        for root, dirs, files in os.walk(
                os.path.dirname((os.path.abspath(__file__)).split("/03_Results_Tier")[0]) + "/res/pythonScript"):
            for file in files:
                if file.endswith(oFileName):
                    if "WINDOWS" in self.OS:
                        subprocess.Popen(root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                    elif "LINUX" in self.OS:
                        subprocess.Popen('sh ' + root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                    else:
                        subprocess.Popen('sh ' + root + '/' + oFileName, shell=True, stdout=subprocess.PIPE)
                    break
        time.sleep(2)'''
        self.flag = True

class RemoteLabel(gui.Label):
    import platform
    import sys
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
        utils.setSPOnOff(nodeId,state,False)
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
                            sys.stdout.write(out.decode('utf-8'))
                            if '\n' in tempInner:
                                tempInner = ''
                            temp = temp + out.decode('utf-8')
                            self.temp = temp
                            tempInner = tempInner + out.decode('utf-8')
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
                            sys.stdout.write(out.decode('utf-8'))
                            if '\n' in tempInner:
                                tempInner = ''
                            temp = temp + out.decode('utf-8')
                            tempInner = tempInner + out.decode('utf-8')
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
                            if strText is not "":
                                jsonScenario[file][strTag] = {}
                                jsonScenario[file][strTag] = strText
                                strText = ""
                                strTag = ''
                            for tag in line.split("@"):
                                if strTag is not "":
                                    strTag = strTag + "_"
                                tag = str(tag).replace('  ', '')
                                if str(tag).strip() != "" and str(tag).strip() != "#":
                                    strTag = strTag + "@" + str(tag).strip()
                        elif strTag is not "" and not line.startswith("#"):
                            strText = strText + str(line)
                    if strText is not "":
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
    if "LINUX" in sys.platform.upper():
        start(MyApp, debug=False, address='0.0.0.0', port=8000, websocket_port=8082, update_interval=0.5)
    else:
        start(MyApp, debug=False, address='0.0.0.0', port=8000, websocket_port=8082, update_interval=0.5)


