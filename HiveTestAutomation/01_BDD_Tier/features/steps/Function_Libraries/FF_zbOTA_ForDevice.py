"""
Created on Apr 21, 2017

@author: Keith
"""
import binascii
import datetime
from getopt import getopt
import glob
import time
from tqdm import tqdm
import FF_utils as utils
import FF_zigbeeToolsConfig as config
import FF_threadedSerial as AT
import FF_zigbeeClusters as zcl
import FF_device_utils as deviceUtil

AT.debug = True
PRINT_DATA = True

deviceTypes = [{'type': 'SLR1', 'ep': '05', 'path': 'SLR1_SLR2', 'zbType': 'FFD'},
               {'type': 'SLR1b', 'ep': '05', 'path': 'SLR1b_SLR2b', 'zbType': 'FFD'},
               {'type': 'SLR2', 'ep': '05', 'path': 'SLR1_SLR2', 'zbType': 'FFD'},
               {'type': 'SLR2b', 'ep': '05', 'path': 'SLR1b_SLR2b', 'zbType': 'FFD'},
               {'type': 'SLT2', 'ep': '09', 'path': 'SLT2', 'zbType': 'SED'},
               {'type': 'SLT3', 'ep': '09', 'path': 'SLT3', 'zbType': 'SED'},
               {'type': 'SLT3b', 'ep': '09', 'path': 'SLT3b', 'zbType': 'SED'},
               {'type': 'SLT4', 'ep': '05', 'path': 'SLT4', 'zbType': 'FFD'},
               {'type': 'SLB1', 'ep': '09', 'path': 'SLB1', 'zbType': 'FFD'},
               {'type': 'SLB3', 'ep': '09', 'path': 'SLB3', 'zbType': 'FFD'},
               {'type': 'SLP2', 'ep': '09', 'path': 'SLP2', 'zbType': 'FFD'},
               {'type': 'SLP2b', 'ep': '09', 'path': 'SLP2b', 'zbType': 'FFD'},
               {'type': 'SLP2C', 'ep': '09', 'path': 'SLP2C', 'zbType': 'FFD'},
               {'type': 'CL01', 'ep': '01', 'path': 'CL01', 'zbType': 'FFD'},
               {'type': 'BUTTON01', 'ep': '01', 'path': 'BUTTON01', 'zbType': 'SED'},
               {'type': 'HAS01UK', 'ep': '01', 'path': 'HAS01UK', 'zbType': 'FFD'},
               {'type': 'MOT003', 'ep': '06', 'path': 'MOT003', 'zbType': 'SED'},
               {'type': 'DWS003', 'ep': '06', 'path': 'DWS003', 'zbType': 'SED'},
               {'type': 'FWBulb01', 'ep': '01', 'path': 'Aurora_FWBulb01UK', 'zbType': 'FFD'},
               {'type': 'FWBulb01US', 'ep': '01', 'path': 'Aurora_FWBulb01US', 'zbType': 'FFD'},
               {'type': 'TWBulb01UK', 'ep': '01', 'path': 'Aurora_TWBulb01UK', 'zbType': 'FFD'},
               {'type': 'TWBulb01US', 'ep': '01', 'path': 'Aurora_TWBulb01US', 'zbType': 'FFD'},
               {'type': 'RGBBulb01UK', 'ep': '01', 'path': 'Aurora_RGBBulb01UK', 'zbType': 'FFD'},
               {'type': 'RGBBulb01US', 'ep': '01', 'path': 'Aurora_RGBBulb01US', 'zbType': 'FFD'}]

zbType = None

otaHeader = [('upgradeFileIdentifier', 4),
             ('headerVersion', 2),
             ('headerLength', 2),
             ('headerFieldControl', 2),
             ('manufacturerCode', 2),
             ('imageType', 2),
             ('fileVersion', 4),
             ('zigbeeStackVersion', 2),
             ('headerString', 32),
             ('totalImageSize', 4),
             ('securityCredentialVersion', 1),
             ('upgradeFileDestination', 8),
             ('minHardwareVersion', 2),
             ('maxHardwareVersion', 2)]

HEADER_LENGTH_POSITION = 6

"""  Block Size 0x32 i.e. 50 Bytes
Needs to be small enough to prevent buffer overflow during multi-hop upgrades
Typical header = 64Bytes + 50 Payload = 114 Bytes total
Multi-hop header is 2 bytes larger (66 Bytes)
CT default for newer devices block size of 63 bytes
So for multi-hop header of 66 + 63 Payload = 129 Bytes (1 more than buffer length)

Update on 17th Feb 2016

It seems that the above calculations are not quite correct.  CT code for SLB1
is requesting 0x3F (63) bytes.  N2 code was failing upgrade so we investigated
further and found that max single hop upgrade payload was actually 58 Bytes.

I believe the breakdown is as follows...

                                        Bytes    Remaining
Max 802.15.4 Packet size                  133     133
PHY Hdr                                     6     127
MAC Hdr                                    11     116
NetWork Header (inc. relay count bytes)    28      88
APS Hdr                                     8      80
ZCL Hdr (for Image Block Response)         17      63
Radio Info                                  5      58
        
Need to also allow for 2 bytes for a routed upgrade.        
Therefore max payload is 56 Bytes        
My OTA code (and N2 code) will limit upgrades to 50Bytes.
Useful link...
http://community.silabs.com/t5/Wireless-Knowledge-Base/What-is-the-maximum-ZigBee-message-payload-length-in-secure-and/ta-p/113417        

"""
MAX_BLOCK_SIZE = 56
BLOCK_SIZE = "{:02x}".format(MAX_BLOCK_SIZE)
UPGRADE_DELAY = 0  # Delay in seconds before device is allowed to upgrade after the download

""" Helper Methods """


def getTimestamp():
    """
    """
    return round(time.time())


def stringFromDatetime(dt):
    """
    """
    return dt.strftime("%H:%M:%S.%f")


def swapEndian(myVal):
    myTemp = ''
    for i in range(len(myVal) - 2, -2, -2):
        myTemp += myVal[i:i + 2]
    return myTemp


def readFileByte(f, byteCount):
    myBytes = binascii.hexlify(f.read(byteCount)).decode('utf-8')
    return myBytes


def setPollControlBinding(nodeId, ep):
    """ Try for 5mins to set a binding
        Return True if binding set, False if it fails

    """
    #  Get the TG EUI
    respState, respCode, respValue = AT.getEUI('0000', '0000')
    if respState and respCode == zcl.statusCodes['SUCCESS']:
        myDstAddr = respValue
    else:
        print("ERROR: Unable to get EUI from telegesis device")
        exit()

    # Get the device EUI
    respState, respCode, respValue = AT.getEUI(nodeId, nodeId)
    if respState and respCode == zcl.statusCodes['SUCCESS']:
        mySrcAddr = respValue
    else:
        print("ERROR: Unable to get EUI from remote device")
        exit()

    myDstEp = '01'

    # Try for 5mins to set the binding.
    timeout = getTimestamp() + (5 * 60)
    while getTimestamp() < timeout:
        respState, respCode, respValue = AT.setBinding(nodeId, mySrcAddr, ep, '0020', myDstAddr, myDstEp)
        if respState and respCode == zcl.statusCodes['SUCCESS']:
            return True

    # Stop the serial threads
    # AT.stopThreads()

    return False


def selectDeviceAndFirmware():
    """ Get the user to enter nodeId, select the device type and select the
        firmware file.
    
    """
    print("*** Firmware Upgrade OTA Script\n")
    nodeId = input("Enter your NodeId = ")
    nodeId = nodeId.upper()

    # If the device is an SED it may not respond to commands (reliably)
    # So we get the user to tell us the device type then if it's an SED
    # we try to set a binding on the pollControl cluster so that it will 
    # send regular check-ins

    print('\nSelect your device type:')
    for i in range(0, len(deviceTypes)):
        print(i, deviceTypes[i])

    dt = input('> ')
    ep = deviceTypes[int(dt)]['ep']
    # dType = deviceTypes[int(dt)]['type']

    # If SED then we must try to set a binding on the pollControl cluster


    dPath = deviceTypes[int(dt)]['path']
    pathname = config.FIRMWARE_ROOT_FILE_PATH + dPath + "_Firmware/*.ota"

    print("DEBUG: {}".format(pathname))

    print('\nSelect your firmware image')
    fileList = glob.glob(pathname)
    for f in fileList:
        file = f.rpartition('/')[2]
        i = fileList.index(f)
        print("{0:>2}. {1}".format(i, file))
    i = input("> ")
    filename = fileList[int(i)]
    zbType = deviceTypes[int(dt)]['zbType']
    # Create header object (reads headers from the imageFile)
    header = myOtaHeader(filename, printData=PRINT_DATA)

    return nodeId, ep, filename, zbType, header


def readArguments():
    """ Read command line parameters 
        Use them if provided.
    """
    helpString = "\n*** OTA Module\n\n" + \
                 "Use these command line options to select the node and firmware file:\n\n" + \
                 "-h Print this help\n" + \
                 "-n node        Node ID of target node\n" + \
                 "-e endpoint    Endpoint for target node\n" + \
                 "-f firmware    Path to firmware file\n" + \
                 "-t type        S=SED, F=FFD" + \
                 "-p port        /dev/portId"

    cliArgs = {'nodeId': None,
               'ep': None,
               'imageFile': None,
               'port': None,
               'type': None,
               'baud': '115200'}

    argsGiven = False

    opts = getopt(sys.argv[1:], "hn:e:f:t:p:")[0]

    for opt, arg in opts:
        # print(opt, arg)
        argsGiven = True
        if opt == '-h':
            print(helpString)
            exit()
        if opt == '-n':
            cliArgs['nodeId'] = arg.upper()
        if opt == '-e':
            cliArgs['ep'] = arg
        if opt == '-f':
            cliArgs['imageFile'] = arg
            if not os.path.isfile(cliArgs['imageFile']):
                print('File not found: {}'.format(arg))
                exit()
        if opt == '-t':
            cliArgs['type'] = arg
            if not cliArgs['type'] in ['SED', 'FFD']:
                print("ERROR: -t option must be one of 'SED' or 'FFD'")
                exit()
        if opt == '-p':
            cliArgs['port'] = arg

    # If one argument was given on CLI then they all need to be given
    if argsGiven:
        for a in cliArgs:
            if a is None:
                print("You have given args on the command line but have not specifed {}.".format(a))
                exit()

    return argsGiven, cliArgs


class myOtaHeader(object):
    """ Header data object
    
    """

    def __init__(self, myFile, printData):
        self.upgradeFileIdentifier = ''
        self.headerVersion = ''
        self.headerLength = 0
        self.headerFieldControl = ''
        self.manufacturerCode = ''
        self.imageType = ''
        self.fileVersion = ''
        self.zigbeeStackVersion = ''
        self.headerString = ''
        self.totalImageSize = 0
        self.readHeader(myFile, printData)

    def readHeader(self, filename, printData):
        """ Read the header parameters from an OTA file and populate
            the header class instance.
            Print the header variables
            
        """
        with open(filename, mode='rb') as myFile:
            lengthCount = 0

            myFile.seek(HEADER_LENGTH_POSITION)
            self.headerLength = readFileByte(myFile, 2)
            headerLengthInt = int(self.headerLength, 16)
            myFile.seek(0)

            for item in otaHeader:
                lengthCount += item[1]
                myVal = readFileByte(myFile, item[1])
                myVal = swapEndian(myVal)

                if item[0] == 'headerString':
                    myVal = swapEndian(myVal)
                    # Convert hex to binary then decode that as UTF-8

                    # myVal = binascii.unhexlify(myVal).decode('utf-8')
                    # Alternative to above line which may work in older python versions
                    myVal = bytearray.fromhex(myVal).decode()

                setattr(self, item[0], myVal)

                if lengthCount >= headerLengthInt: break

        # Print the header fields
        if printData:
            print()
            for item in otaHeader:
                if hasattr(self, item[0]):
                    print('{0:26}= {1}'.format(item[0], getattr(self, item[0])))
            print()

        return


class results(object):
    def __init__(self):
        self.parms = ['initialVersion',
                      'finalVersion',
                      'imageNotifySent',
                      'firstImageBlockRequest',
                      'upgradeEndRequest',
                      'postUpgradeQni',
                      'postUpgradeQniVersion',
                      'fileVersionCorrect',
                      'error']

        for p in self.parms:
            setattr(self, p, None)

        self.header = ','.join(self.parms)

    def __str__(self):
        myString = ','.join([str(getattr(self, p)) for p in self.parms])
        return myString


def sedPostUpgradeChecks(result, header, timeout=30 * 60):
    """ Wait for QNI or checkIn
        When a checkIn is received then we know we will be in fastpoll mode
        so we can read the currentFileVersion attribute.
        When a QNI is received we can check the version is correct.
        When both of these are correct we can exit.

    """
    print("SED Post Upgrade Checks:")

    timeout = time.time() + timeout
    qniMsg = 'IMGQUERY:{0},{1}'.format(nodeId, ep)
    ciMsg = 'CHECKIN:{}'.format(nodeId)

    msgs = [qniMsg, ciMsg]

    while time.time() < timeout:
        msg = AT.waitForMessage(msgs, timeout=15 * 60)
        if msg is None:
            result.error = 'TIMEOUT: sedPostUpgradeChecks: No QNI or checkIn'
            return

        if msg.startswith(qniMsg):
            version = msg.split(',')[5]
            if version == header.fileVersion:
                result.postUpgradeQni = time.time()
                result.postUpgradeQniVersion = version

        if msg.startswith(ciMsg):
            # checkIn received.  Should be in fast poll mode now.
            # Read the currentFileVersion attribute from OTA cluster
            clust = '0019'
            attr = '0002'
            clustType = 'client'
            respState, respCode, respValue = AT.getAttribute(nodeId, ep, clust, attr, clustType)
            if not respState:
                result.error = 'ERROR: sedPostUpgradeChecks. currentFileVersion not received. {},{}'.format(
                    respCode, respValue)
                return
            else:
                if respValue == header.fileVersion:
                    result.fileVersionCorrect = getTimestamp()
                    result.finalVersion = respValue

        if result.finalVersion == header.fileVersion and result.postUpgradeQniVersion == header.fileVersion:
            return

    # Timeout. Set an error and return
    result.error = 'TIMEOUT: sedPostUpgradeChecks'

    return


def ffdPostUpgradeChecks(result, header, timeout=700):
    """ Send 2x imageNotify to provoke new QNIs. We need to send more than one just in case first
        response is a scheduled response rather than the provoked response. This confirms imageNotify
        works.  Check that also that QNI returns expected new version

        Then read OTA latestVersion attribute to confirm that version is correct:

        ImageNotify             >>
                                << QNI
        ImageNotify             >>
                                << QNI

        AT+readcatr             >>
                                << attributeResponse

    """
    # Long delay to allow reboot after flashing to complete.
    time.sleep(60)

    print("FFD Post Upgrade Checks:")

    timeout = time.time() + timeout
    state = 'checkImageNotify'
    doLoop = True

    while doLoop:
        if state == 'checkImageNotify':
            #  Send two imageNotify msgs to check QNI is generated
            for _ in range(2):
                # Short pause between IN attempts
                # Device should be rebooting on first pass so this is fine
                time.sleep(10)

                # Send IN
                respState, respCode, respValue = AT.imageNotify(nodeId, ep, header.manufacturerCode,
                                                                myImageType=header.imageType,
                                                                myFileVersion=header.fileVersion)
                if not respState:
                    result.error = 'ERROR: Image notify failed {},{}'.format(respCode, respValue)
                    return

                # WaitQNI
                resp = AT.waitForQNI(nodeId, ep, timeout=30)
                if resp['error'] is not None:
                    result.error = resp['error']
                    return
                result.postUpgradeQniVersion = resp['currentVersion']
                seqNum = resp['seqNum']

                # sendQNIR(no image avail)
                respState, respCode, respValue = AT.queryNextImageResponse(nodeId, ep, header.manufacturerCode,
                                                                           header.imageType,
                                                                           header.fileVersion,
                                                                           header.totalImageSize, seqNum)
                if not respState:
                    result.error = 'ERROR: QNI Response failed. {},{}'.format(respCode, respValue)
                    return

            if result.postUpgradeQniVersion == header.fileVersion:
                state = 'checkAttribute'
            elif time.time() > timeout:
                result.error = "TIMEOUT: FFD Post Upgrade Checks: QNI version is not correct"
                return
            else:
                state = 'checkImageNotify'

        elif state == 'checkAttribute':
            # Read the currentFileVersion attribute from OTA cluster
            clust = '0019'
            attr = '0002'
            clustType = 'client'
            respState, respCode, respValue = AT.getAttribute(nodeId, ep, clust, attr, clustType)
            if not respState:
                result.error = 'ERROR: Post upgrade currentFileVersion not received. {},{}'.format(respCode,
                                                                                                   respValue)
                return
            else:
                if respValue == header.fileVersion:
                    result.fileVersionCorrect = getTimestamp()
                    result.finalVersion = respValue
                    return
                elif time.time() > timeout:
                    result.error = "ERROR: FFD Post Upgrade Checks: currentFileVerison is not correct={}".format(
                        respValue)
                    return

        else:
            print("FFD Post Upgrade Checks: unknonwn state={}".format(state))
            exit()

    return


def firmwareUpgrade(nodeId, ep, zbType, imageFile, header, reboot, plugMacId, printData=PRINT_DATA):
    """ Execute the FW message exchanges
        Assumes the pollControl binding has been set for SEDs

        Expected message exchanges are:

        Co-ordinator      Device

        if SED we wait for a checkIN or a QNI
                    <<  checkIn or QNI

        if FFD (or SSD and we have received a CI) then start here:
        AT+IMGNOTIFY  >>


                      <<  IMGQuery (queryNextImage) - Device uses response to this to set it's FW server
        AT+QIMGRSP    >>  (queryNextImage Response)
                      <<  IMGBREQ = ImageBlock Request
        AT+IMGBRSP    >>  (ImageBlockRequest Response)
                      ..
                      <<  IMGBREQ = ImageBlock Request
        AT+IMGBRSP    >>  (ImageBlockRequest Response)
                      ..
                      <<  UPGRADEREQ = UpgradeEnd Request
        AT+UPGRADE    >>  UpgradeEnd Response (Upgrade with a time. Typically upgrade now)

        For SED we wait for a checkIn from the device before sending QNI.

        Post upgrade checks:

        For an FFD:
            Send double imageNotify messages to ensure that QNI response is generated.  We
            send two to be sure that one reply at least was as a reult of the IN message and
            not just a scheduled QNI.  Check the returned FW version in the QNI is correct.
            Read the currentFileVersion attribute to check the FW version is correct

        For an SED:
            Wait for a QNI and a checkIn.  Confirm the QNI version is correct.
            After the checkIn we can read the currentFileVersion attribute and confirm
            the file version is correct.


    """
    # If we are an SED then set a binding first.
    if zbType == 'SED':
        print("\nTrying to set pollControl binding.  Wake the device.. ")
        resp = setPollControlBinding(nodeId, ep)
        if not resp:
            print("ERROR: binding on pollControl has failed")
            exit()
        print('Binding set.')

    # Create header object (reads headers from the imageFile)
    # header = myOtaHeader(imageFile,printData)

    # Create a results object
    result = results()

    # Set fast poll so that we can talk quickly to SEDs
    AT.setFastPoll()

    # Connect to the serial port
    #     AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug,rxQ=True,listenerQ=False)
    # AT.initialiseSerialComms(config.PORT, config.BAUD)

    # In order to test imageNotify we wait for a QNI, then respond NO_IMAGE_AVAILABLE
    # then send imageNotify to trigger an immediate response.

    # Wait for a QNI


    if zbType == 'SED':

        state = 'waitQniOrCheckIn'

    else:
        state = 'sendIN'

    testInProgress = True
    seqNum = None
    maxDataSize = None
    offset = None
    downloadStarted = False
    if printData:
        pbar = tqdm(total=int(header.totalImageSize, 16))
        # Flush any garbage from the RxQueue
    AT.flushRxQ()
    CounterFlag = True
    while testInProgress:

        if state == 'waitQniOrCheckIn':
            print("Waiting for QNI or checkIn")
            timeout = time.time() + 630  # Bit more than 10mins.  Enough time for at least one QNI or checkIn
            qniMsg = 'IMGQUERY:{0},{1}'.format(nodeId, ep)
            ciMsg = 'CHECKIN:{}'.format(nodeId)
            msgs = [qniMsg, ciMsg]
            msg = AT.waitForMessage(msgs, timeout)
            if msg is None:
                result.error = 'TIMEOUT: sedPostUpgradeChecks: No QNI or checkIn'
                return

            if msg.startswith(qniMsg):
                resp = AT.parseQNI(msg)
                if resp['manufCode'] != header.manufacturerCode:
                    result.error = 'Error: Manufacturer code does not match ota file. Device code is {}, header code is{}'.format(
                        resp['maufacturerCode'], header.manufacturerCode)
                    state = 'exit'
                elif resp['imageType'] != header.imageType:
                    result.error = "Error: Image type does not match ota file. Device Type is {}, header type is {}".format(
                        resp['imageType'], header.imageType)
                    state = 'exit'
                else:
                    result.initialVersion = resp['currentVersion']
                    seqNum = resp['seqNum']
                    state = 'sendQNIR'

            elif msg.startswith(ciMsg):
                state = 'sendIN'

        elif state == 'sendIN':
            print('Sending imageNotify')
            respState, respCode, respValue = AT.imageNotify(nodeId, ep, header.manufacturerCode,
                                                            myImageType=header.imageType,
                                                            myFileVersion=header.fileVersion)
            if not respState:
                result.error = 'ERROR: Image notify failed {},{}'.format(respCode, respValue)
                state = 'exit'
            else:
                result.imageNotifySent = getTimestamp()
                state = 'waitQniOrCheckIn'

        elif state == 'sendQNIR':
            # Respond to QNI with valid image
            print('Sending QNIR')
            respState, respCode, respValue = AT.queryNextImageResponse(nodeId, ep, header.manufacturerCode,
                                                                       header.imageType,
                                                                       header.fileVersion, header.totalImageSize,
                                                                       seqNum, myStatus='00')
            if not respState:
                result.error = 'ERROR: QNI Response failed. {},{}'.format(respCode, respValue)
                state = 'exit'
            else:
                if printData:
                    pbar = tqdm(total=int(header.totalImageSize, 16))

                state = 'waitIBRequest'

        elif state == 'waitIBRequest':
            resp = AT.waitForImageBlockReqOrUpgradeEndReq(nodeId, ep, timeout=60)
            if resp['error']:
                result.error = resp['error']
                state = 'exit'
            else:
                # Save timestamp of first imageBlockRequest
                if not downloadStarted:
                    result.firstImageBlockRequest = getTimestamp()
                    downloadStarted = True
                    print('Download starting...')

                seqNum = resp['seqNum']
                offset = resp['offset']
                maxDataSize = resp['maxDataSize']

                if resp['upgradeEnd']:
                    maxDataSize = "30"
                    if int(maxDataSize, 16) > MAX_BLOCK_SIZE:
                        print("******** WARNING ******************************")
                        print("*** BLOCK SIZE REQUEST FROM DEVICE IS > {}".format(MAX_BLOCK_SIZE))
                        print("*** RAISE AN ERROR FOR THIS")
                        print("***********************************************")
                    state = 'sendUpgradeEndResp'
                else:
                    state = 'sendImageBlockResponse'
        elif state == 'sendImageBlockResponse':
            payload, payloadBytes = getBlockFromFile(header, offset, imageFile, maxDataSize)
            respState, respCode, respValue = AT.imageBlockResponse(nodeId, ep, header.manufacturerCode,
                                                                   header.imageType, header.fileVersion,
                                                                   offset, payloadBytes, payload, seqNum)
            if not respState:
                result.error = 'ERROR: imageBlockResponse has failed. {},{}'.format(respCode, respValue)
                state = 'exit'
            else:
                if printData: pbar.update(int(payloadBytes, 16))

                state = 'waitIBRequest'

                while CounterFlag:
                    if int(str(pbar).rsplit('%', 1)[0]) == 3:
                        if plugMacId:
                            print("node", deviceUtil.getDeviceNodeWithMAC(deviceUtil.getModelIdWithMAC(plugMacId, True),
                                                                          plugMacId))
                            utils.setSPOnOff(
                                deviceUtil.getDeviceNodeWithMAC(deviceUtil.getModelIdWithMAC(plugMacId, True),
                                                                plugMacId),
                                "OFF", None)

                            time.sleep(0.2)
                            utils.setSPOnOff(
                                deviceUtil.getDeviceNodeWithMAC(deviceUtil.getModelIdWithMAC(plugMacId, True),
                                                                plugMacId), "ON",
                                None)
                            print("Plug rebooting")
                        else:
                            deviceUtil.rebootDevice(nodeId, ep)
                            print("DeviceRebooting")

                        CounterFlag = False
                    break



        elif state == 'sendUpgradeEndResp':
            print('Sending upgradeEndResponse')

            nowTime = datetime.datetime.utcnow()
            upgradeTime = nowTime + datetime.timedelta(seconds=UPGRADE_DELAY)

            respState, respCode, respValue = AT.upgradeEndResponse(nodeId, ep, header.manufacturerCode,
                                                                   header.imageType,
                                                                   header.fileVersion, seqNum, nowTime, upgradeTime)
            if not respState:
                result.error = 'ERROR: upgradeEndResponse has failed.'
                state = 'exit'
            else:
                result.upgradeEndRequest = getTimestamp()
                if printData: pbar.close()
                state = 'postUpgradeChecks'

        elif state == 'postUpgradeChecks':
            if zbType == 'SED':
                sedPostUpgradeChecks(result, header)
            else:
                ffdPostUpgradeChecks(result, header)
                state = 'exit'

        elif state == 'exit':
            AT.clearFastPoll()

            return result
        else:
            print('Error: Unknown state machine state = {}'.format(state))
            exit()

    return result


def getBlockFromFile(header, offset, imageFile, maxDataSize):
    """ Get the wanted block from the image file.
        Final block gets shortened to match file size.
    
        We ignore the requested blocksize from the device and limit it to
        0x32 i.e. 50 bytes.  
    """
    if maxDataSize < BLOCK_SIZE:
        blockSize = maxDataSize
    else:
        blockSize = BLOCK_SIZE
    imageSizeInt = int(header.totalImageSize, 16)
    blockSizeInt = int(blockSize, 16)

    # Calculate the blocksize (note final block will be shorter than BLOCK_SIZE)
    chunkLeftInt = imageSizeInt - int(offset, 16)
    if chunkLeftInt < blockSizeInt:
        blockSize = "%02X" % chunkLeftInt

    # Read the block from the imageFile
    with open(imageFile, mode='rb') as f:
        f.seek(int(offset, 16))
        payload = readFileByte(f, blockSizeInt)

    return payload, blockSize


""" Code starts here """
if __name__ == "__main__":
    import sys

    print(sys.executable)
    import os

    print(os.getcwd())
    import sys

    print(sys.path)
    # Check if any command line arguments provided
    argsGiven, cliArgs = readArguments()
    if argsGiven:
        nodeId = cliArgs['nodeId']
        ep = cliArgs['ep']
        imageFile = cliArgs['imageFile']
        zbType = cliArgs['type']
        port = cliArgs['port']
        baud = cliArgs['baud']
        # Create header object (reads headers from the imageFile)
        header = myOtaHeader(imageFile, printData=PRINT_DATA)

    else:
        nodeId, ep, imageFile, zbType, header = selectDeviceAndFirmware()
        port = config.PORT
        baud = config.BAUD

    if PRINT_DATA or argsGiven:
        print()
        print("Node ID    : {}".format(nodeId))
        print("EP         : {}".format(ep))
        print("Image File : {}".format(imageFile))
        print("Type       : {}".format(zbType))
        print("Port       : {}".format(port))
        print("Baud       : {}".format(baud))

    # Check the image file exists
    if not os.path.isfile(imageFile):
        print("\nFile not found {}".format(imageFile))
        exit()
    try:
        AT.stopThreads()
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=False)
    except:
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=False)
    # AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
    # Start the upgrades
    reboot = False
    result = firmwareUpgrade(nodeId, ep, zbType, imageFile, header, reboot, '', printData=PRINT_DATA)

    if PRINT_DATA:
        print()
        for r in result.parms:
            print("{:23}, {}".format(r, getattr(result, r)))
        print()

    if result.fileVersionCorrect and result.firstImageBlockRequest:
        upgradeDuration = result.fileVersionCorrect - result.firstImageBlockRequest
        durn = str(datetime.timedelta(seconds=upgradeDuration))
    else:
        durn = None

    print("Upgrade Duration={}".format(durn))

    print('All Done. {}'.format(time.strftime("%H:%M:%S", time.gmtime())))
