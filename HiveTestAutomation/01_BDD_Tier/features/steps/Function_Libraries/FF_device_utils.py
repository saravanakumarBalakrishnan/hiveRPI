"""
Created on 14 Oct 2015

@author: ranganathan.veluswamy
"""

import json
import subprocess, time, os
import FF_utils as utils
import FF_threadedSerial as AT
import FF_zigbeeToolsConfig as config
import platform
import serial
import sys
import FF_uartHandler as UAT
import FF_convertTimeTemperature as timeTempConvert
import FF_OCRUtils as oUtils
import FF_alertmeApi as ALAPI
#import EE_Constants as constants

strAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node " + \
                            "/Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js  --log-level error"

strAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node " + \
                            "/Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js " + \
                            "--address 127.0.0.1 --command-timeout  \"7200\"  --debug-log-spacing " + \
                            "--no-reset " + \
                            "--native-instruments-lib --log-level error"

testModesCommandList = {"VERSIONS": "test Gver",
                        "RESET": "reset",
                        "DEVICETYPE": "test Gdev",
                        "STACKVERSION": "test Gstk",
                        "EUI": "test Geui",
                        "BATTERYVOLTAGE": "test Gvcc",
                        "LEDON": "test SledA",
                        "LEDOFF": "test Sleda",
                        "RADIO11": "test Srad11",
                        "RADIO12": "test Srad12",
                        "RADIO13": "test Srad13",
                        "RADIO14": "test Srad14",
                        "RADIO15": "test Srad15",
                        "RADIO16": "test Srad16",
                        "RADIO17": "test Srad17",
                        "RADIO18": "test Srad18",
                        "RADIO19": "test Srad19",
                        "RADIO20": "test Srad20",
                        "RADIO21": "test Srad21",
                        "RADIO22": "test Srad22",
                        "RADIO23": "test Srad23",
                        "RADIO24": "test Srad24",
                        "RADIO25": "test Srad25",
                        "RADIO26": "test Srad26",
                        "RADIOSTOP": "test Srad",
                        "SLEEP":"test Sslp",
                        "ZIGBEE":"test Tzig",
                        "SWITCH":"test Tswi",
                        "REARBUTTON":"test Tbtn"}
testModesResponseList = {"VERSIONS": "Iver",
                         "RESET": "HIVEHOME.COM",
                         "DEVICETYPE": "IdevButton01",
                         "STACKVERSION": "Istk",
                         "EUI": "Ieui",
                         "BATTERYVOLTAGE": "Ivcc",
                         "LEDON": "Cled",
                         "LEDOFF": "Cled",
                         "RADIO11": "Crad11",
                         "RADIO12": "Crad12",
                         "RADIO13": "Crad13",
                         "RADIO14": "Crad14",
                         "RADIO15": "Crad15",
                         "RADIO16": "Crad16",
                         "RADIO17": "Crad17",
                         "RADIO18": "Crad18",
                         "RADIO19": "Crad19",
                         "RADIO20": "Crad20",
                         "RADIO21": "Crad21",
                         "RADIO22": "Crad22",
                         "RADIO23": "Crad23",
                         "RADIO24": "Crad24",
                         "RADIO25": "Crad25",
                         "RADIO26": "Crad26",
                         "RADIOSTOP": "Crad",
                         "SLEEP":"Cslp",
                         "ZIGBEE":"Izig",
                         "SWITCH":"Cswi",
                         "REARBUTTON":"Cbtn"}

sensorTestModesCommandList = {"VERSIONS": "test Gver",
                        "MOTIONDEVICETYPE": "test Gdev",
                        "CONTACTDEVICETYPE": "test Gdev",
                        "STACKVERSION": "test Gstk",
                        "EUI": "test Geui",
                        "TEMP": "test Gtmp",
                        "BATTERYVOLTAGE": "test Gvcc",
                        "LUX": "test Glux",
                        "LEDRON": "test SledRg",
                        "LEDGON": "test SledrG",
                        "LEDOFF": "test Sledrg",
                        "NVM": "test Snvm",
                        "RADIO11": "test Trad11",
                        "RADIO12": "test Trad12",
                        "RADIO13": "test Trad13",
                        "RADIO14": "test Trad14",
                        "RADIO15": "test Trad15",
                        "RADIO16": "test Trad16",
                        "RADIO17": "test Trad17",
                        "RADIO18": "test Trad18",
                        "RADIO19": "test Trad19",
                        "RADIO20": "test Trad20",
                        "RADIO21": "test Trad21",
                        "RADIO22": "test Trad22",
                        "RADIO23": "test Trad23",
                        "RADIO24": "test Trad24",
                        "RADIO25": "test Trad25",
                        "RADIO26": "test Trad26",
                        "RADIOSTOP": "test Srad",
                        "ZIGBEE11":"test Tzig11",
                        "ZIGBEE12":"test Tzig12",
                        "ZIGBEE13":"test Tzig13",
                        "ZIGBEE14":"test Tzig14",
                        "ZIGBEE15":"test Tzig15",
                        "ZIGBEE16":"test Tzig16",
                        "ZIGBEE17":"test Tzig17",
                        "ZIGBEE18":"test Tzig18",
                        "ZIGBEE19":"test Tzig19",
                        "ZIGBEE20":"test Tzig20",
                        "ZIGBEE21":"test Tzig21",
                        "ZIGBEE22":"test Tzig22",
                        "ZIGBEE23":"test Tzig23",
                        "ZIGBEE24":"test Tzig24",
                        "ZIGBEE25":"test Tzig25",
                        "ZIGBEE26":"test Tzig26",
                        "MEMORY":"test Tmem",
                        "PIR":"test Tpir",
                        "MAGNET":"test Tmag",
                        "REARBUTTON":"test Tbtn"}
sensorTestModesResponseList = {"VERSIONS": "IverIceOS",
                         "MOTIONDEVICETYPE": "IdevMotion sensor",
                         "CONTACTDEVICETYPE": "IdevContact sensor",
                         "STACKVERSION": "IstkZStack",
                         "TEMP": "Itmp",
                         "EUI": "Ieui",
                         "BATTERYVOLTAGE": "Ivcc",
                         "LUX": "Ilux",
                         "LEDRON": "CledRg",
                         "LEDGON": "CledrG",
                         "LEDOFF": "CledrG",
                         "NVM": "RnvmP",
                         "RADIO11": "Crad11",
                         "RADIO12": "Crad12",
                         "RADIO13": "Crad13",
                         "RADIO14": "Crad14",
                         "RADIO15": "Crad15",
                         "RADIO16": "Crad16",
                         "RADIO17": "Crad17",
                         "RADIO18": "Crad18",
                         "RADIO19": "Crad19",
                         "RADIO20": "Crad20",
                         "RADIO21": "Crad21",
                         "RADIO22": "Crad22",
                         "RADIO23": "Crad23",
                         "RADIO24": "Crad24",
                         "RADIO25": "Crad25",
                         "RADIO26": "Crad26",
                         "RADIOSTOP": "RradF",
                         "ZIGBEE11":"Izig11",
                         "ZIGBEE12":"Izig12",
                         "ZIGBEE13":"Izig13",
                         "ZIGBEE14":"Izig14",
                         "ZIGBEE15":"Izig15",
                         "ZIGBEE16":"Izig16",
                         "ZIGBEE17":"Izig17",
                         "ZIGBEE18":"Izig18",
                         "ZIGBEE19":"Izig19",
                         "ZIGBEE20":"Izig20",
                         "ZIGBEE21":"Izig21",
                         "ZIGBEE22":"Izig22",
                         "ZIGBEE23":"Izig23",
                         "ZIGBEE24":"Izig24",
                         "ZIGBEE25":"Izig25",
                         "ZIGBEE26":"Izig26",
                         "SWITCH":"Cswi",
                         "MEMORY":"RmemP",
                         "PIR":"RpirP",
                         "MAGNET":"RmagP",
                         "REARBUTTON":"RbtnF"}

strAndroidAppFilePath = '/Users/ranganathan.veluswamy/Downloads/Hive-productV6Internalprod-release-1.2.0.47.apk'
strADBPath = '/Users/ranganathan.veluswamy/Desktop/Ranga/RnD/Appium/android-sdk-macosx/platform-tools/'

strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../../../02_Manager_Tier/EnviromentFile/")
#oColorTempList = constants.oColorTempList

def get_connected_android_devices():
    oProcess = subprocess.Popen(strADBPath + "adb devices", stdout=subprocess.PIPE, shell=True)
    # oProcess = subprocess.Popen("$ANDROID_HOME/platform-tools/adb devices", stdout=subprocess.PIPE, shell=True)
    deviceList = []
    while True:
        output = oProcess.stdout.readline()
        if oProcess.poll() is not None:
            break
        if output:
            # print(output)
            if not 'DEVICES' in str(output).upper():
                if 'DEVICE' in str(output).upper():
                    deviceList.append(str(output).split("\\t")[0].split("'")[1].strip())
        else:
            break
    print(deviceList)
    return deviceList


def install_app_android_device(strAndroidAppFilePath):
    strAppPakage = utils.getAttribute('android', 'appPackage')
    print(strAppPakage)
    oDeviceList = get_connected_android_devices()
    for strDeviceID in oDeviceList:
        # Uninstall the existing App
        subprocess.call(strADBPath + "adb -s " + strDeviceID + " uninstall " + strAppPakage, shell=True)
        # Install the App
        subprocess.call(strADBPath + "adb -s " + strDeviceID + " install -rg " + strAndroidAppFilePath, shell=True)


def create_android_device_json():
    killall_nodes()
    intPort = 4723
    intBootStrap = 4724
    oDeviceList = get_connected_android_devices()
    if len(oDeviceList) == 0:
        oDeviceList = get_connected_android_devices()

    oADLJsonDict = getAndroidDeviceListJson()
    oADLJsonDict['android_devicelist'] = {}
    intIndex = 1
    for oDevice in oDeviceList:
        strPort = str(intPort)
        strBootStrap = str(intBootStrap)
        strDeviceNode = 'device' + str(intIndex)
        oADLJsonDict['android_devicelist'][strDeviceNode] = {}
        oADLJsonDict['android_devicelist'][strDeviceNode]['device_id'] = oDevice
        oADLJsonDict['android_devicelist'][strDeviceNode]['port'] = strPort
        oADLJsonDict['android_devicelist'][strDeviceNode]['bootstrap'] = strBootStrap
        # + ' --address 127.0.0.' + strPort[3:] 
        strDeviceAppiumConnectionString = strAppiumConnectionString + ' -p ' + strPort + ' -bp ' + strBootStrap  # + ' -U ' + oDevice
        oADLJsonDict['android_devicelist'][strDeviceNode]['appium_connection_string'] = strDeviceAppiumConnectionString
        launch_appium_server(strDeviceAppiumConnectionString)
        oADLJsonDict['android_devicelist'][strDeviceNode]['status'] = 'Not Started'
        oADLJsonDict['android_devicelist'][strDeviceNode]['execution_start_time'] = ""
        intIndex = intIndex + 1
        intPort = intPort + 2
        intBootStrap = intBootStrap + 2

    putAndroidDeviceListJson(oADLJsonDict)


def killall_nodes():
    subprocess.Popen("killall node", shell=True)
    time.sleep(5)
    '''subprocess.call('adb kill-server', shell=True)
    time.sleep(10)'''
    subprocess.call('adb start-server', shell=True)
    time.sleep(10)


def getPort():
    # Set Network Path
    networkBasePath = ""
    PORT = ""
    if 'DARWIN' in platform.system().upper():
        networkBasePath = '/volumes/hardware/'
        PORT = '/dev/tty.SLAB_USBtoUART'
    elif 'LINUX' in platform.system().upper():
        networkBasePath = '/home/pi/hardware/'
        PORT = '/dev/ttyUSB0'
    elif sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
        result = []
        FinalPort = ""
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
                FinalPort = port
            except (OSError, serial.SerialException):
                pass
        print(result)
        networkBasePath = "\\\\nas1\Hardware\\"
        PORT = FinalPort
        print('Windows ' + FinalPort + '\n')
    else:
        networkBasePath = ""
        PORT = config.PORT
        print('I should not be hereeeee \n')
    return PORT


def launch_appium_server(strAppiumConString):
    print(strAppiumConString)
    subprocess.Popen(strAppiumConString, shell=True)


def getAndroidDeviceListJson():
    strAndroidDeviceListPath = strEnvironmentFolderPAth + '/android_device_list.json'
    strJson = open(strAndroidDeviceListPath, mode='r')
    oADLJsonDict = json.loads(strJson.read())
    strJson.close()
    return oADLJsonDict


def putAndroidDeviceListJson(oADLJsonDict):
    strNodeClustAttrPath = strEnvironmentFolderPAth + '/android_device_list.json'
    # Write back the JSON to the GlobalVar.JSON
    oJson = open(strNodeClustAttrPath, mode='w+')
    oJson.write(json.dumps(oADLJsonDict, indent=4, sort_keys=False))
    oJson.close()


def getNodes(boolATStarted=True):
    if not boolATStarted:
        #AT.stopThreads()
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
        #TGstick in pairing mode to pair the device for 10 sec
        AT.pjoin(10)
        time.sleep(15)
        print("sleepiinngggg")
        #AT.stopThreads()

        # status, statusMessage = AT.startSerialThreads(getPort(), config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
        # if not status:
        #    putZigbeeDevicesJson({})
        #    return {}
    try:
        AT.stopThreads()
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
    except:
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)

    putZigbeeDevicesJson({})
    intListCounter = 1
    NodeList, oAllNodes = initiateNodeList()
    intCounter = 0
    boolFlag = True
    #AT.stopThread.clear()
    while boolFlag:
        boolFlag = False
        for oNode in NodeList:
            myNodeId = oNode[1]
            myType = oNode[2]
            myModelName = oNode[4]
            mychildNodeList = []
            if myType != "RFD" and oNode[0] != "ID" :


                '''try:
                    AT.stopThreads()
                    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=True, rxQ=True, listenerQ=False)
                except:
                    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=True, rxQ=True, listenerQ=False)
                '''
                _, _, rows = utils.getNtable(myNodeId)
                intCounter = 0
                try:
                    for oRow in rows:
                        mytype = ""
                        intInnerCounter = 0
                        if intCounter > 0:
                            oItems = oRow.split("|")
                            if "No" not in oItems[0]:
                                for oItem in oItems:
                                    'Get Device Type'
                                    if intInnerCounter == 1:
                                        mytype = oItem.replace(" ", "")

                                    'Get Device Mac Address'
                                    if intInnerCounter == 2:
                                        macID = oItem.replace(" ", "")

                                    'Get Device Model, End Point, Name and append to the list'
                                    if intInnerCounter == 3:
                                        if not any(oItem.replace(" ", "") == e[1] for e in NodeList):
                                            strModel = utils.getDeviceModeId(oItem.replace(" ", ""))
                                            NodeList.append([])

                                            'Naming the devices'
                                            strModelTemp = strModel
                                            strModel = namingDevices(strModelTemp, oAllNodes)
                                            oAllNodes[strModel] = {}
                                            NodeList[intListCounter].append(macID)
                                            NodeList[intListCounter].append(oItem.replace(" ", ""))  # NodeID
                                            NodeList[intListCounter].append(mytype)
                                            _, _, endPoints = AT.discEndpoints(oItem.replace(" ", ""))
                                            NodeList[intListCounter].append(endPoints)  # EndPoints
                                            NodeList[intListCounter].append(strModel)  # name
                                            mychildNodeList.append(oItem.replace(" ", ""))
                                            NodeList[intListCounter].append([])
                                            intListCounter += 1
                                            boolFlag = True

                                            'Add to dictionary'
                                            oAllNodes[strModel]["nodeID"] = oItem.replace(" ", "")
                                            oAllNodes[strModel]["type"] = mytype
                                            oAllNodes[strModel]["macID"] = macID
                                            oAllNodes[strModel]["name"] = strModelTemp
                                            oAllNodes[strModel]["endPoints"] = endPoints
                                    intInnerCounter += 1
                        intCounter += 1

                        'Add child Nodes'
                        if len(mychildNodeList) > 0:
                            for oNode in NodeList:
                                oAllNodes[myModelName]["childNodes"] = mychildNodeList
                        elif 'childNodes' not in oAllNodes[myModelName]:
                            oAllNodes[myModelName]["childNodes"] = []
                except:
                    print("Error")
    if not boolATStarted:
        AT.stopThreads()
    putZigbeeDevicesJson(oAllNodes)
    return oAllNodes


def getNodesWithoutThread():
    putZigbeeDevicesJson({})
    intListCounter = 1
    NodeList, oAllNodes = initiateNodeList()
    intCounter = 0
    boolFlag = True
    #AT.stopThread.clear()
    while boolFlag:
        boolFlag = False
        for oNode in NodeList:
            myNodeId = oNode[1]
            myType = oNode[2]
            myModelName = oNode[4]
            mychildNodeList = []
            if myType != "RFD" and oNode[0] != "ID" :


                '''try:
                    AT.stopThreads()
                    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=True, rxQ=True, listenerQ=False)
                except:
                    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=True, rxQ=True, listenerQ=False)
                '''
                _, _, rows = utils.getNtable(myNodeId)
                intCounter = 0
                try:
                    for oRow in rows:
                        mytype = ""
                        intInnerCounter = 0
                        if intCounter > 0:
                            oItems = oRow.split("|")
                            if "No" not in oItems[0]:
                                for oItem in oItems:
                                    'Get Device Type'
                                    if intInnerCounter == 1:
                                        mytype = oItem.replace(" ", "")

                                    'Get Device Mac Address'
                                    if intInnerCounter == 2:
                                        macID = oItem.replace(" ", "")

                                    'Get Device Model, End Point, Name and append to the list'
                                    if intInnerCounter == 3:
                                        if not any(oItem.replace(" ", "") == e[1] for e in NodeList):
                                            strModel = utils.getDeviceModeId(oItem.replace(" ", ""))
                                            NodeList.append([])

                                            'Naming the devices'
                                            strModelTemp = strModel
                                            strModel = namingDevices(strModelTemp, oAllNodes)
                                            oAllNodes[strModel] = {}
                                            NodeList[intListCounter].append(macID)
                                            NodeList[intListCounter].append(oItem.replace(" ", ""))  # NodeID
                                            NodeList[intListCounter].append(mytype)
                                            _, _, endPoints = AT.discEndpoints(oItem.replace(" ", ""))
                                            NodeList[intListCounter].append(endPoints)  # EndPoints
                                            NodeList[intListCounter].append(strModel)  # name
                                            mychildNodeList.append(oItem.replace(" ", ""))
                                            NodeList[intListCounter].append([])
                                            intListCounter += 1
                                            boolFlag = True

                                            'Add to dictionary'
                                            oAllNodes[strModel]["nodeID"] = oItem.replace(" ", "")
                                            oAllNodes[strModel]["type"] = mytype
                                            oAllNodes[strModel]["macID"] = macID
                                            oAllNodes[strModel]["name"] = strModelTemp
                                            oAllNodes[strModel]["endPoints"] = endPoints
                                    intInnerCounter += 1
                        intCounter += 1

                        'Add child Nodes'
                        if len(mychildNodeList) > 0:
                            for oNode in NodeList:
                                oAllNodes[myModelName]["childNodes"] = mychildNodeList
                        elif 'childNodes' not in oAllNodes[myModelName]:
                            oAllNodes[myModelName]["childNodes"] = []
                    #AT.stopThreads()
                except:
                    print("Error")
    putZigbeeDevicesJson(oAllNodes)
    return oAllNodes


def namingDevices(strModelTemp, oAllNodes):
    intDeviceCntr = 0
    strModel = strModelTemp
    while True:
        intDeviceCntr = intDeviceCntr + 1
        strModel = strModelTemp + "_" + str(intDeviceCntr)
        if strModel in oAllNodes:
            continue
        else:
            break
    return strModel


def initiateNodeList():
    _, _, rows = utils.getNtable('0000')
    NodeList = [[]]
    _, _, myDstAddr = AT.getEUI('0000', '0000')
    NodeList[0].append(myDstAddr)
    NodeList[0].append("0000")
    NodeList[0].append("COO")
    NodeList[0].append("--")
    NodeList[0].append("TGStick")
    NodeList[0].append([])

    oAllNodes = {"TGStick": {}}
    oAllNodes["TGStick"]["nodeID"] = "0000"
    oAllNodes["TGStick"]["type"] = "COO"
    oAllNodes["TGStick"]["macID"] = myDstAddr
    oAllNodes["TGStick"]["name"] = "TGStick"
    oAllNodes["TGStick"]["endPoints"] = []
    return NodeList, oAllNodes


def getNodeIDbyDeciveID(deviceID, boolATStarted=True):
    oNodeList = getZigbeeDevicesJson()
    nodeID = ""
    if deviceID in oNodeList: nodeID = oNodeList[deviceID]['nodeID']
    return nodeID


def getDeviceNode(deviceID, boolATStarted=True):
    oNodeList = getZigbeeDevicesJson()
    Node = ""
    if deviceID in oNodeList: Node = oNodeList[deviceID]
    return Node


def getDeviceNodeWithMAC(deviceID, strMacId, boolATStarted=True):
    oNodeList = getZigbeeDevicesJson()
    Node = ""
    for oNode in oNodeList:
        if strMacId in oNodeList[oNode]["macID"]:
            Node = oNodeList[oNode]['nodeID']
    return Node

def getDeviceIdWithMAC(strMacId, boolATStarted=True):
    oNodeList = getZigbeeDevicesJson()
    Node = ""
    for oNode in oNodeList:
        if strMacId in oNodeList[oNode]["macID"]:
            Node = oNode
    return Node


def getModelIdWithMAC(strMacId, boolATStarted=True):
    oNodeList = getZigbeeDevicesJson()
    strName = ""
    for oNode in oNodeList:
        if strMacId in oNodeList[oNode]["macID"]:
            strName = oNodeList[oNode]['name']
    return strName


def getDeviceMACWithModel(deviceID, boolATStarted=True):
    oNodeList = getZigbeeDevicesJson()
    MacID = ""
    for oNode in oNodeList:
        if str(deviceID).upper() in str(oNodeList[oNode]["name"]).upper():
            MacID = oNodeList[oNode]['macID']
    return MacID


def getDeviceEPWithModel(deviceID, boolATStarted=True):
    oNodeList = getZigbeeDevicesJson()
    EP = []
    for oNode in oNodeList:
        if str(deviceID).upper() in str(oNodeList[oNode]["name"]).upper():
            EP = oNodeList[oNode]['endPoints']
    return EP
def getDeviceNodeAndEPWithDeviceType(strDeviceType, boolATStarted=True):
    macId = getDeviceMACWithModel(strDeviceType,True)
    myNodeId = getDeviceNodeWithMAC(strDeviceType, macId)
    return myNodeId


def putZigbeeDevicesJson(oADLJsonDict):
    strNodeClustAttrPath = strEnvironmentFolderPAth + '/zigbeeDevices.json'
    # Write back the JSON to the GlobalVar.JSON
    oJson = open(strNodeClustAttrPath, mode='w+')
    oJson.write(json.dumps(oADLJsonDict, indent=4, sort_keys=False))
    oJson.close()


def getZigbeeDevicesJson():
    strAndroidDeviceListPath = strEnvironmentFolderPAth + '/zigbeeDevices.json'
    strJson = open(strAndroidDeviceListPath, mode='r')
    oZDLJsonDict = json.loads(strJson.read())
    strJson.close()
    return oZDLJsonDict


def resetDevice():
    respState, respValue = UAT.sendCommand("reset", "HiveHome.com")
    Header = ""
    oRow = ""
    if respState:
        Header = Header + "Expected and Actual@@@"
        oRow = respValue + "~"
    else:
        Header = Header + "Expected$$Actual@@@"
        oRow = testModesResponseList["reset"] + "$$" + respValue + "~"

    Log = Header + oRow
    return respState, respValue, Log


def testMode(strTestName):
    respState, respValue = UAT.sendCommand(testModesCommandList[strTestName], testModesResponseList[strTestName])
    Header = ""
    oRow = ""
    if respState:
        Header = Header + "Expected and Actual@@@"
        oRow = respValue
    else:
        Header = Header + "Expected$$Actual@@@"
        oRow = testModesResponseList[strTestName] + "$$" + respValue

    Log = Header + oRow
    return respState, respValue, Log

def testSensorFactoryMode(strTestName):
    respState, respValue = UAT.sendCommand(sensorTestModesCommandList[strTestName], sensorTestModesResponseList[strTestName])
    Header = ""
    oRow = ""
    if respState:
        Header = Header + "Expected and Actual@@@"
        oRow = respValue
    else:
        Header = Header + "Expected$$Actual@@@"
        oRow = testModesResponseList[strTestName] + "$$" + respValue

    Log = Header + oRow
    return respState, respValue, Log


def rebootDevice(nodeId, ep):
    cmd = "at+rawzcl:" + nodeId + "," + ep + ",0000,0539100000"
    responseMsg = "OK"
    respState, respValue = AT.sendCommand(cmd, responseMsg, 1)
    return respState, respValue


def factoryRestoreDevice(nodeId, ep):
    cmd = "at+rawzcl:" + nodeId + "," + ep + ",0000,0539100001"
    responseMsg = "OK"
    respState,respCode, respValue = AT.sendCommand(cmd, responseMsg, 1)
    return respState, respValue


def rebootDevice(nodeId, ep):
    cmd = "at+rawzcl:" + nodeId + "," + ep + ",0000,0539100000"
    responseMsg = "OK"
    respState,respCode, respValue = AT.sendCommand(cmd, responseMsg, 1)
    return respState, respValue


def pressDeviceButton(nodeId, ep, strButtonName, strPressType, strHoldDuration="",doublehold=False):
    strButtonCode = ""
    if str(strButtonName).upper() == "BACK":
        strButtonCode = "01"
    elif str(strButtonName).upper() == "MENU":
        strButtonCode = "02"
    elif str(strButtonName).upper() == "TICK":
        strButtonCode = "04"
    elif str(strButtonName).upper() == "TOP LEFT":
        strButtonCode = "08"
    elif str(strButtonName).upper() == "TOP RIGHT":
        strButtonCode = "10"
    elif str(strButtonName).upper() == "DIAL":
        strButtonCode = "20"

    strPressCode = ""
    if str(strPressType).upper() == "PRESS":
        strPressCode = "00"
    if str(strPressType).upper() == "HOLD":
        strPressCode = "01"
    if str(strPressType).upper() == "RELEASE":
        strPressCode = "02"

    cmd = "at+rawzcl:" + nodeId + "," + ep + ",FD00,05391000" + strPressCode + strButtonCode
    responseMsg = "OK"
    respState, _, respValue = AT.sendCommand(cmd, responseMsg, maxAttempts=1,retryTimeout=1)

    if respState:
        if strPressCode == "01" and doublehold is False:
            time.sleep(strHoldDuration)
            strPressCode = "02"
            cmd = "at+rawzcl:" + nodeId + "," + ep + ",FD00,05391000" + strPressCode + strButtonCode
            responseMsg = "OK"
            respState, _,respValue = AT.sendCommand(cmd, responseMsg, 1)

    return respState, respValue


def rotateDial(nodeId, ep, strDirection, intUnits):
    global respState, respValue
    strPressCode = ""
    strButtonCode = "20"
    if str(strDirection).upper() == "CLOCKWISE":
        strPressCode = "03"
    elif str(strDirection).upper() == "ANTICLOCKWISE":
        strPressCode = "04"
    for intCounter in range(0, int(intUnits)):
        cmd = "at+rawzcl:" + nodeId + "," + ep + ",FD00,05391000" + strPressCode + strButtonCode
        responseMsg = "OK"
        respState, _,respValue = AT.sendCommand(cmd, responseMsg, 1,1)
        time.sleep(3)
        if not respState:
            return respState, respValue
    return respState, respValue

def heatBoost(context,myNodeId,ep):
    mySetpoint = 22
    pressDeviceButton(myNodeId, ep, "Tick", "Press")
    time.sleep(4)
    context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Tick Button", "Done")
    pressDeviceButton(myNodeId, ep, "Top Right", "Press")
    time.sleep(3)
    context.reporter.ReportEvent("Event Log", "Heat Boost Button is pressed", "Done")
    pressDeviceButton(myNodeId, ep, "Tick", "Press")
    context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done")
    context.oThermostatEP.model.occupiedHeatingSetpoint = timeTempConvert.temperatureFloatToHexString(mySetpoint)
    context.oThermostatEP.model.mode = "BOOST"


def waterBoost(context,myNodeId,ep):
    mySetpoint = 22
    pressDeviceButton(myNodeId, ep, "Tick", "Press")
    time.sleep(4)
    _, imgWakeName = oUtils.captureOriginal(context)
    context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Tick Button", "Done")
    pressDeviceButton(myNodeId, ep, "Top LEFT", "Press")
    time.sleep(3)
    _, imgBoostName = oUtils.captureOriginal(context)
    context.reporter.ReportEvent("Event Log", "Water Boost Button is pressed", "Done")
    pressDeviceButton(myNodeId, ep, "Tick", "Press")
    _, imgConfirmName = oUtils.captureOriginal(context)
    context.reporter.ReportEvent("Event Log", "Confirm Button is pressed", "Done")
    time.sleep(1)
    _, imgHomeName = oUtils.capture(context)
    context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Tick Button", "Done",
                                 ocrImagePath=imgWakeName)
    oImgWake = oUtils.loadImage(imgWakeName, context)
    Mode = oUtils.getText(oImgWake, context)
    oImgWake = None
    Mode = str(Mode).replace("0FF", "OFF").replace("0N","ON")
    context.oThermostatEP.model.occupiedHeatingSetpoint = timeTempConvert.temperatureFloatToHexString(mySetpoint)
    context.oThermostatEP.model.mode = "BOOST"
    context.oThermostatEP.model.thermostatRunningState = "0001"
    return Mode,imgBoostName,_,_,imgHomeName


# Power cycle the HUB
def power_cycle_plug(context, strDuration):
    AT.stopThreads()
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    respState, _, resp = utils.discoverNodeIDbyCluster('0006')
    if respState:
        utils.setSPOnOff(myNodeId=resp, strOnOff='OFF', boolZigbee=True)
        context.reporter.ReportEvent("Test Validation", "Plug is turned OFF", "DONE")
        time.sleep(int(strDuration))
        utils.setSPOnOff(myNodeId=resp, strOnOff='ON', boolZigbee=True)
        context.reporter.ReportEvent("Test Validation", "Plug is turned ON", "DONE")
        time.sleep(10)
    AT.stopThreads()
    return respState

#Get the Node ID for the given device type
def getNodeID(resp):
    oDeviceNodes = {}
    for oNode in resp['nodes']:
        if not ('supportsHotWater' or 'consumers' or 'producers') in oNode['attributes']:
            if 'nodeType' in oNode.keys():
                if 'thermostatui.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'thermostat.json' in oNode["nodeType"]:
                    if 'reportedValue' not in oNode["attributes"]["model"]: strModel = 'SLR2'
                    else: strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'hub.json' in oNode["nodeType"]:
                    try:
                        strModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    except:
                        strModel = "Exception"
                        oDeviceNodes[strModel] = oNode["id"]
                elif 'smartplug.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'extender.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif '.light.json' in oNode["nodeType"]:  #LDS_DimmerLight
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'contact.sensor.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'motion.sensor.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'connected.boiler.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]

    return oDeviceNodes

 #Get the FirmwareVersion for the given device type
def getFWversion():
    strCurrentEnvironment = utils.getAttribute('common', 'currentEnvironment')
    ALAPI.createCredentials(strCurrentEnvironment, None)
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    oDeviceVersion = {}
    for oNode in resp['nodes']:
        if not 'supportsHotWater'  in oNode['attributes']:
            if 'nodeType' in oNode.keys():
                if 'thermostatui.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'thermostat.json' in oNode["nodeType"]:
                    if 'reportedValue' not in oNode["attributes"]["model"]: strModel = 'SLR2'
                    else: strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'hub.json' in oNode["nodeType"]:
                    try:
                        strModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    except:
                        strModel = "Exception"
                        oDeviceVersion[strModel] = strModel
                elif 'smartplug.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'extender.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif '.light.json' in oNode["nodeType"]:  #LDS_DimmerLight
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'contact.sensor.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'motion.sensor.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'connected.boiler.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
    ALAPI.deleteSessionV6(session)
    return oDeviceVersion

#Upgrade Firmware for the give device type
def upgradeFirware( DeviceType, fwTargetVersion):
    strCurrentEnvironment = utils.getAttribute('common', 'currentEnvironment')
    ALAPI.createCredentials(strCurrentEnvironment, None)
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    nodeIdList = getNodeID(resp)
    if DeviceType in nodeIdList:
        nodeId = nodeIdList[DeviceType]
        ALAPI.firmwareUpgrade(session, nodeId, fwTargetVersion)
    else: print("Unable to Fetch Node ID for the Given Device Type: " + DeviceType)
    ALAPI.deleteSessionV6(session)


def wakeUpTheDevice(context, myNodeId, ep):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize(
        'Wake up the thermostat')
    pressDeviceButton(myNodeId, ep, "Tick", "Press")
    time.sleep(3)
    context.reporter.ReportEvent("Event Log", "Wake up stat by pressing Menu button", "Done")
    # time.sleep(4)


def handleButtonPress(nodeId, ep, strButtonName, clusterId,strPressType, strHoldDuration="",doublehold=False):
    strButtonCode = ""
    if str(strButtonName).upper() == "BACK":
        strButtonCode = "01"
    elif str(strButtonName).upper() == "MENU":
        strButtonCode = "02"
    elif str(strButtonName).upper() == "TICK":
        strButtonCode = "04"
    elif str(strButtonName).upper() == "TOP LEFT":
        strButtonCode = "08"
    elif str(strButtonName).upper() == "TOP RIGHT":
        strButtonCode = "10"
    elif str(strButtonName).upper() == "DIAL":
        strButtonCode = "20"

    strPressCode = ""
    if str(strPressType).upper() == "PRESS":
        strPressCode = "00"
    if str(strPressType).upper() == "HOLD":
        strPressCode = "01"
    if str(strPressType).upper() == "RELEASE":
        strPressCode = "02"

    cmd = "at+rawzcl:" + nodeId + "," + ep + "," + clusterId + "," + "05391000" + strPressCode + strButtonCode
    responseMsg = "OK"
    respState, _, respValue = AT.sendCommand(cmd, responseMsg)

    if respState:
        if strPressCode == "01" and doublehold is False:
            time.sleep(strHoldDuration)
            strPressCode = "02"
            cmd = "at+rawzcl:" + nodeId + "," + ep + "," + clusterId + ","+"05391000" + strPressCode + strButtonCode
            responseMsg = "OK"
            respState, _, respValue = AT.sendCommand(cmd, responseMsg, 1)

    return respState, respValue


def pressSLT4DeviceButton(nodeId, ep, strButtonName, strPressType, strHoldDuration="",doublehold=False):
    handleButtonPress(nodeId, ep, strButtonName, 'FD01', strPressType, strHoldDuration="",doublehold=False)

def rotateDial_SLT4(nodeId, ep, strDirection, intUnits):
    strPressCode = ""
    strButtonCode = "20"
    if str(strDirection).upper() == "CLOCKWISE":
        strPressCode = "03"
    elif str(strDirection).upper() == "ANTICLOCKWISE":
        strPressCode = "04"
    for intCounter in range(0, int(intUnits)):
        cmd = "at+rawzcl:" + nodeId + "," + ep + ",FD01,05391000" + strPressCode + strButtonCode
        AT.sendCommand(cmd, "OK", 1)
        time.sleep(3)


def changePlugState(context, oRow, strDeviceType):
    """

    :param context:
    :param oRow:
    :param strDeviceType:
    :return:
    """
    try:
        strOppText = ""
        if str(strDeviceType).upper() == "GENERIC":
            DeviceName = utils.getAttribute("COMMON", "mainClient")
            oJson = getDeviceNode(DeviceName)
            MAcID = oJson['macID']
            myNodeId = oJson['nodeID']
            context.nodeId = myNodeId
            myEp = oJson["endPoints"][0]
        elif str(strDeviceType).upper() == "SIREN001":
            MAcID = getDeviceMACWithModel(strDeviceType)
            myNodeId = getDeviceNodeWithMAC(MAcID)
            myEp = getDeviceEPWithModel(strDeviceType)[1]
        else:
            MAcID = getDeviceMACWithModel(strDeviceType)
            myNodeId = getDeviceNodeWithMAC(MAcID)
            myEp = getDeviceEPWithModel(strDeviceType)[0]
        print(strDeviceType, myNodeId, MAcID, "\n")
        strExp = ""
        if str(oRow['State']).upper() == "OFF":
            strExp = "00"
            strOppText = "ON"
        elif str(oRow['State']).upper() == "ON":
            strExp = "01"
            strOppText = "OFF"
        else:
            context.report().ReportEvent("Test Validation", "Invalid State", "FAIL")
            exit()
        utils.setSPOnOff(myNodeId,myEp, oRow['State'], context, strDeviceType + " state is set to " + oRow['State'])
        intCounter = 0
        return intCounter, strExp, strOppText
    except Exception as e:
        print(e)

if __name__ == '__main__':
    '''create_android_device_json()
    install_app_android_device(strAndroidAppFilePath)'''
    pass
