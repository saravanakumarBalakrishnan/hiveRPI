"""
Created on 2 Sep 2016

@author: keith
"""

import FF_zigbeeToolsConfig as config
import datetime, time
import queue
import threading
import serial
import sys
from getopt import getopt

debug = False
rxQueue = queue.Queue(maxsize=1000)
txQueue = queue.Queue(maxsize=1000)
listenerQueue = queue.Queue(maxsize=1000)

stopThread = threading.Event()
threadPool = []
ser=None
debug=True

GET_COMMANDS=['dev','ver','stk','eui','tmp','vcc','lux']
SET_COMMANDS=['led']
TEST_COMMANDS=['zig','rad','mem','btn','pir','mag']

""" Serial Port methods """
def serialReadHandler(ser,rxQ=False,listenerQ=False):
    """ Serial port read thread handler
        If serial timeout=None then this thread blocks until a new line is available
     
    """
    while not stopThread.isSet():
        reading = ser.readline().decode(errors='replace').strip()
        if reading!='':
            # Make sure Qs are not full and blocking
            if rxQ:
                if rxQueue.full():
                    print("*** DEBUG: rxQueue is full.  Dumping oldest message")
                    rxQueue.get()
                rxQueue.put(reading)
            
            # Deal with listerQueue if it is switched on
            if listenerQ:
                if listenerQueue.full():
                    print("*** DEBUG: listenerQueue is full.  Dumping oldest message")
                    listenerQueue.get()
                listenerQueue.put(reading)          
                
            myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
            if debug: print("DEBUG RX: {},  {}".format(myTime,reading))
    print('Serial read thread exit')
    return 0
# def serialWriteHandler_old(ser):
#     """ Serial port write handler
#     
#         Get from a queue blocks if queue is empty so we just loop
#         and wait for items
#     
#     """
#     while not stopThread.isSet():
#         try:
#             myMessage = txQueue.get(timeout=1)
#             #myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
#             #if debug: print("DEBUG Tx: {},  {}".format(myTime,myMessage))
#             if type(myMessage) is str:
#                 ser.write(bytearray(myMessage + '\r\n','ascii'))
#             else:
#                 ser.write(myMessage)
#         except queue.Empty:
#             pass
#     print('Serial write thread exit')
#     return 0
def serialWriteHandler(ser,interCharDelay=0):
    """ Serial port write handler
    
        Get from a queue blocks if queue is empty so we just loop
        and wait for items
    
    """
    while not stopThread.isSet():
        try:
            myMessage = txQueue.get(timeout=1)
            #myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
            #if debug: print("DEBUG Tx: {},  {}".format(myTime,myMessage))
            myMessage=myMessage +'\r\n'
            for c in myMessage:
                ser.write(bytearray(c,'ascii'))
                time.sleep(interCharDelay)

        except queue.Empty:
            pass
    print('Serial write thread exit')
    return 0
def startSerialThreads(port, baud, printStatus=False, rxQ=False, listenerQ=False):
    """ 
        rxQ and listenerQ are flags to switch on/off the appropriate Q
        defaults are off.
        
    """
    try:
        #serial_port = serial.Serial(port, baud, timeout=1, rtscts=True,dsrdtr=True)
        serial_port = serial.Serial(port, baud, bytesize=8, timeout=1)
        global ser
        ser=serial_port
    except IOError as e:
        print('Error opening port.',e)
        exit()
    if printStatus: print("Serial port opened...{0}".format(port))

    # Make sure the stopThread event is not set
    stopThread.clear()

    # Start the serial port handler thread    
    readThread = threading.Thread(target=serialReadHandler, args=(serial_port,rxQ,listenerQ))
    readThread.daemon = True # This kills the thread when main program exits
    readThread.start()
    readThread.name = 'readThread'
    threadPool.append(readThread)
    if printStatus: print('Serial port read handler thread started.')
    
    interCharDelay=0.01
    writeThread = threading.Thread(target=serialWriteHandler, args=(serial_port,interCharDelay))
    writeThread.daemon = True # This kills the thread when main program exits
    writeThread.start()
    writeThread.name = 'writeThread'
    threadPool.append(writeThread)
    if printStatus: print('Serial port write handler thread started.')
    
    if printStatus:
        if rxQ:
            print('rxQueue is ON')
        else:
            print('rxQueue is OFF')
            
        if listenerQ:
            print('listenerQueue is ON')
        else:
            print('listenerQueue is OFF')
    print()
    return
def stopThreads():
    """ Set the stop event and wait for all threads to exit
        Close the serial port
    
    """
    stopThread.set()
    for t in threadPool:
        t.join()

    # Close the serial port
    global ser
    ser.close()
    return
def printAllResponses():
    """
    """
    while True:
        if not rxQueue.empty():
            item = rxQueue.get()  # Pop first item from the Queue
            myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
            print("RX: {},  {}".format(myTime,item))
    return 0
def flushRxQ():
    """
    """
    while not rxQueue.empty():
        rxQueue.get()    
    return
# def matchResponse(myResp, myExpectedResponses):
#     """ Returns a match if the given response matches one of the given expected responses.
#     
#         Expected responses should be in the form:
#             READRPTCFGRSP:F14D,05,FC00,(..),00,0002
#         The parameter in the curved brackets is the ZigBee response code.  We use regex to match against the
#         string and extract the response code.
#         
#         Returns True if a match is found, else False
#         Returns the 
#     """    
#     for er in myExpectedResponses:
#         matchPattern = re.compile(er)
#         match = matchPattern.search(myResp)
#         if match:
#             # If there is a response code then extract it
#             if len(match.regs)>1:
#                 respCode = match.group(1)
#             else:
#                 respCode = None
#             return True, respCode
#     return False, None
def sendCommand(cmd,myExpectedResponses,maxAttempts=2,timeout=10):
    """ Sends a command and reads the rxQueue looking for a matching echo back from the DUT
    
    """
    flushRxQ()

    myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
    if debug: print("DEBUG Tx: {},  {},Expected Response={}".format(myTime,cmd,cmd))
    
    # Loop until all retries done
    respValue = None
    respState = False
    attemptCount=0
    strResponse = ""
    while attemptCount<maxAttempts:
        txQueue.put(cmd)
        attemptCount+=1
        
        attemptTimeout=time.time()+timeout
        while time.time()<attemptTimeout:
            # Some message received so do something with it
            if not rxQueue.empty():
                resp = rxQueue.get()
                strResponse = strResponse + "<BR>" +  resp
                print("Response =====" + str(resp).upper() + " ********* Value="+str(resp).upper())
                if str(myExpectedResponses).upper() in str(resp).upper():
                    # If it's what we want the exit 
                    respState=True
                    respValue = resp
                    #return respState, respValue
                    break
        if respState:
            break
                
        respValue="Timeout ~" + strResponse
        myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
        if debug: print("DEBUG Tx: {},  {}".format(myTime,"Timeout for {} command".format(cmd)))    
                
    return respState, respValue

""" Command line argument methods """
def readArguments():
    """ Read command line parameters 
        Use them if provided.
    """
    helpString = "\n*** threadedSerial Module\n\n" +\
                 "Use these command line options to select the node and firmware file:\n\n" +\
                 "-h Print this help\n" +\
                 "-p port        /dev/portId"

    myPort = None
    myBaud = None

    opts = getopt(sys.argv[1:], "hp:b:")[0]
    
    for opt, arg in opts:
        #print(opt, arg)
        if opt == '-h':
            print(helpString)
            exit()
        elif opt == '-p':
            myPort = arg
        elif opt == '-b':
            myBaud = arg
        else:
            print("Invalid argument: {},{}".format(opt,arg))
            print(helpString)
            exit()

    return myPort,myBaud

""" Test Command Methods """
def runTest(coreCmd):
    """ core command is one of: zig, mag, tmp etc.
        We add the additional chars to buld a full command e.g. 'test Tzig'
         
        We expect a response value and a pass fail e.g.
        Izig11    - Info response (network found on ch11)
        RzigP     - Result for zig test. P=Pass, F=Fail
    """
    # Check we have a supported command
    if not coreCmd in TEST_COMMANDS:
        print("Command {} is not listed in TEST_COMMANDS.  Please add it.".format(coreCmd))
        exit()
    
    # Send the command and wait for the echo back
    testCmd="test T{}".format(coreCmd)
    respState,respValue=sendCommand(testCmd,[testCmd],timeout=10)
    if not respState:
        respValue="No command echo received"
        return respState,respValue
    
    # Once we have the echo then read multiple lines until we
    # we get a pass, a fail or we timeout
    passStatus="R{}P".format(coreCmd)
    failStatus="R{}F".format(coreCmd)
    resultHeader="I{}".format(coreCmd)
    respState=False
    respValue=None
    
    timeout=time.time()+10
    while time.time()<timeout and result is None:
        line = rxQueue.get()
        if line.startswith(passStatus):
            respState=True
        elif line.startswith(failStatus):
            respState=False
        elif line.startswith(resultHeader):
            respValue=line[len(resultHeader):]
        else:
            pass
    
    return respState, respValue

def getValue(coreCmd):
    """ coreCmd is one of ver, stk etc.
        We add additional characters to buld the full command e.g. 'test Gver'
        
        We expect the command to be echo'd back by the device followed by another
        line with the result string.
    """
    # Check we have a supported command
    if not coreCmd in GET_COMMANDS:
        print("Command {} is not listed in GET_COMMANDS.  Please add it.".format(coreCmd))
        exit()
    
    # Send the command and wait for the echo back
    testCmd="test G{}".format(coreCmd)
    respState,respValue=sendCommand(testCmd,[testCmd],timeout=10)
    if not respState:
        respValue="No command echo received"
        return respState,respValue
    
    respState=False
    respHeader="I{}".format(coreCmd)
    
    timeout=time.time()+10
    while time.time()<timeout:
        line=rxQueue.get()
        if line.startswith(respHeader):
            respValue=line[len(respHeader):]
            respState=True
    
    return respState,respValue

def zigBeeTest():
    """
    """
    respState,respValue=sendCommand("test Tzig", "Izig",timeout=10)
    result=None
    if respState:
        result=rxQueue.get()
        if result not in ['RzigP',['RzigF']]:
            print("Problem with Tzig result")
            print("    {},{}".format(respState,respValue))
            print("    {}".format(result))
            exit()
    return respState,respValue,result
        
if __name__=="__main__":
    # Check if any command line arguments provided
    #port,baud = readArguments()
    
    #if port==None: port=cfg.port
    #if baud==None: baud=cfg.baud

    port = config.BUTTON_PORT
    baud = config.BAUD
    
    startSerialThreads(port, baud, printStatus=True, rxQ=True, listenerQ=False)

    '''respState,respValue = sendCommand("reset", ["IceOS"])
    if not respState:
        print("Initial reset did not succeed. {}".format(respValue))
    else:
        print("Reset to enter test mode")
'''
    # Give device a couple of seconds to reboot
    time.sleep(2)

    # Send a Gver command to start production test mode
    respState,respValue = sendCommand("test Gver",'IverIceOS',maxAttempts=100,timeout=1)
    print(respState,respValue)
    
    print(zigBeeTest())

    #timeout=time.time()+60
    #while time.time()<timeout:
    #    respState,respValue = sendCommand("test Gver",['Iver'])
    #    print(respState,respValue)

    c=0
    for i in range(0,1):
        #time.sleep(0.1)
        respState,respValue,result = zigBeeTest()
        #respState,respValue = sendCommand("test Gver", ["Iver"])
        if respState: c+=1
        print(respState)

    print("COUNT={}".format(c))

    #sendCommand("reset",["IceOS"])
    print()
    stopThreads()
    ser.close()    
    print('All done')