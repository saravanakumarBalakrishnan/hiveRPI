import sys
sys.path.append("../../01_BDD_Tier/features/steps")
sys.path.append("../../01_BDD_Tier/features/steps/PageObjects")
sys.path.append("../../01_BDD_Tier/features/steps/Locators")
sys.path.append("../../01_BDD_Tier/features/steps/Function_Libraries")
import FF_zbOTA as OTA
import FF_threadedSerial as AT
import os
import FF_zigbeeToolsConfig as config
import time
import datetime

imageFile = ''
nodeId = '0380'
ep = '09'
zbType = 'FFD'

header = OTA.myOtaHeader(imageFile, printData=OTA.PRINT_DATA)

# Check the image file exists
if not os.path.isfile(imageFile):
    print("\nFile not found {}".format(imageFile))
    exit()
AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=False)
# Start the upgrades
result = OTA.firmwareUpgrade(nodeId, ep, zbType, imageFile, header, printData=OTA.PRINT_DATA)

if result.fileVersionCorrect and result.firstImageBlockRequest:
    upgradeDuration = result.fileVersionCorrect - result.firstImageBlockRequest
    durn = str(datetime.timedelta(seconds=upgradeDuration))
else:
    durn = None

print("Upgrade Duration={}".format(durn))

print('All Done. {}'.format(time.strftime("%H:%M:%S", time.gmtime())))