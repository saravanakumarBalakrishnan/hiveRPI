import sys
sys.path.append("../../01_BDD_Tier/features/steps")
sys.path.append("../../01_BDD_Tier/features/steps/PageObjects")
sys.path.append("../../01_BDD_Tier/features/steps/Locators")
sys.path.append("../../01_BDD_Tier/features/steps/Function_Libraries")
import FF_threadedSerial as AT
import FF_zigbeeToolsConfig as config
AT.debug = False
AT.nodeId, AT.nodeEp, AT.port = AT.readArguments()

if AT.nodeId == '':
    AT.nodeId = config.NODE_ID
if AT.port == '': AT.port = config.PORT
AT.baud = config.BAUD

AT.startSerialThreads(AT.port, AT.baud, printStatus=True, rxQ=True, listenerQ=False)

""" Get initial data - may have to set fp=True here for some devices """
AT.fp = False
# params = getInitialData(nodeId, nodeEp, fastPoll=fp, printStatus=True)
AT.params = AT.getInitialData(AT.nodeId, fastPoll=AT.fp, printStatus=True)

""" Iterate through all endpoints, clusters and attributes and bindings """
AT.getAllAttributes(AT.nodeId)

if AT.fp: AT.resetSedAttrs(AT.params)

AT.getAllBindings()

# Turn off the serial port worker thread
print()
AT.stopThreads()
AT.ser.close()

print('\nAll Done')