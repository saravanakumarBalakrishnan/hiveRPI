'''
Created on 26 Feb 2018

@author: Keith.Gough

1. Manually join a bulb to the network
2. Put network into pairing.
3. Power up bulb via plug
4. Put network into pairing.
5. Find FFD device(bulb)
6. Read binding table - if len != 0 then stop.
7. If len=0 then set a binding.
8. Factory restore the bulb
   off (2s)
   on (0.5)
   x6 (one more than required?)
9. Go back to 4

    1       2       3       4       5       6
____|¯¯|____|¯¯|____|¯¯|____|¯¯|____|¯¯|____|¯|____|¯¯¯¯¯¯¯¯¯¯¯¯¯

Pulses 1-5 = 1s off, 0.5s on
Pulse 6    = 1s off, 0.4s on

Assumption:

Reset sequence during pulse 6 is truncated by premature power down of the bulb. Reset does not fully occur and binding
table is left populated.  Perhaps due to incorrect sequencing (e.g. reset count should not be cleared until all other
functions have completed, therefore if final pulse is too short then bulb resets again on next power up)



'''
import FF_threadedSerial as AT
import FF_zigbeeToolsConfig as config
import time

PORT = config.PORT
BAUD = config.BAUD
PLUG_NODE_ID = "F6C0"
PLUG_EP_ID = "09"

OFF_TIME = 2
ON_TIME = 0.1
myEui = ''

def plugOn(plugNodeId=PLUG_NODE_ID, plugEpId=PLUG_EP_ID):
    mySendMode = '0'  # Unicast
    myState = '1'  #  On
    AT.onOff(plugNodeId, plugEpId, mySendMode, myState)
    return


def plugOff(plugNodeId=PLUG_NODE_ID, plugEpId=PLUG_EP_ID):
    mySendMode = '0'  # Unicast
    myState = '0'  #  Off
    AT.onOff(plugNodeId, plugEpId, mySendMode, myState)
    return


def checkNoBindings(nodeId):
    """
    """
    _, _, rows = AT.getBindings(nodeId)
    if rows[1] == "Length:00":
        return True
    elif int(rows[1].split(':')[1]) > 0:
        return False
    else:
        print('Binding table decode error')
        exit()

    return


def onePulse(offTime, onTime):
    """
    """
    plugOff(PLUG_NODE_ID, PLUG_EP_ID)
    time.sleep(offTime)
    plugOn(PLUG_NODE_ID, PLUG_EP_ID)
    time.sleep(onTime)
    return


def resetBulb():
    """
    """
    # 5x standard pulses
    for _ in range(5):
        onePulse(1, 0.45)

    # Extra short pulse.  We want this to be the one where the reset is done.
    onePulse(1, 0.45)
    plugOff()

    # Finally turn the bulb on
    time.sleep(1)
    plugOn()
    return


def pairBulb(timeout):
    """ Turn on pairing
        Wait for FFD:

    """
    # Put co-ordinator into pairing mode
    AT.pjoin(250)

    ### Wait for FFD
    shortId = None
    print("Pairing", end='')
    timeout = time.time() + timeout
    while time.time() < timeout and shortId == None:
        while not AT.rxQueue.empty():
            msg = AT.rxQueue.get()
            if msg.startswith("FFD:"):
                shortId = msg.split(',')[1]

        time.sleep(0.1)

    AT.pjoin(0)
    print("")
    return shortId


def bindingsClearedTest(reporter=None):
    """
    """
    bulbNodeId = None

    #  Reset and pair the bulb
    while not bulbNodeId:

        # Reset the bulb
        print("Reset the bulb...")
        if reporter is not None:
            reporter.ReportEvent("Test log","Resetting the bulb","Done")
        resetBulb()

        # Pair the bulb
        bulbNodeId = pairBulb(timeout=30)
        if not bulbNodeId:
            print("Device did not pair. Retry")
            if reporter is not None:
                reporter.ReportEvent("Test Validation", "Device did not pair. Retry", "Fail")

    print("Bulb joins as = {}".format(bulbNodeId))
    if reporter is not None:
        reporter.ReportEvent("Test Validation", "Bulb joins as = {}".format(bulbNodeId), "Pass")
    _, _, bulbEui = AT.getEUI(bulbNodeId, bulbNodeId)

    btableEmpty = checkNoBindings(bulbNodeId)
    print('Binding table empty = {}'.format(btableEmpty))
    if reporter is not None:
        reporter.ReportEvent("Test Validation", "Binding table empty = {}".format(btableEmpty), "Pass")
    if not btableEmpty:
        print("Binding table not cleared")
        if reporter is not None:
            reporter.ReportEvent("Test Validation", "Binding table not cleared", "Fail")
        exit()

    # Set a binding
    AT.setBinding(bulbNodeId, bulbEui, '01', '0000', myEui, '01')
    btableEmpty = checkNoBindings(bulbNodeId)
    print('Binding table empty = {}'.format(btableEmpty))
    if reporter is not None:
        reporter.ReportEvent("Test Validation", "Binding table empty = {}".format(btableEmpty), "Pass")

    return


if __name__ == "__main__":

    AT.startSerialThreads(PORT, BAUD, printStatus=True, rxQ=True, listenerQ=False)
    AT.debug = False
    _, _, myEui = AT.getEUI('0000', '0000')
    for i in range(100):
        bindingsClearedTest()
        print()

    print('\nAll done')

