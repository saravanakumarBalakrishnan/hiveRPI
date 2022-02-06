import FF_zigbeeToolsConfig as config
import threading
import serial
import queue
import datetime
import os
import sys

sys.path.append("steps")
sys.path.append("steps/PageObjects")
sys.path.append("steps/Locators")
sys.path.append("steps/Function_Libraries")
debug = True
rxQueue = queue.Queue(maxsize=1000)
txQueue = queue.Queue(maxsize=1000)
listenerQueue = queue.Queue(maxsize=1000)

stopThread = threading.Event()
threadPool = []
ser=None

class serials:

    def startSerialThreads(self,port, baud, printStatus=False, rxQ=False, listenerQ=False):
        """
            rxQ and listenerQ are flags to switch on/off the appropriate Q
            defaults are off.

        """
        if config.PORT == "COM1":
            print('Error opening port.')
            strJson = open(os.path.abspath("__file__") + "/../../../../../TGStickstatus.txt", mode='w')
            strJson.write("Error opening port. ")
            strJson.close()
            exit()
        try:
            serial_port = serial.Serial(port, baud, timeout=1)
            global ser
            ser=serial_port
        except IOError as e:
            print('Error opening port.',e)
            strJson = open(os.path.abspath("__file__") + "/../../../../../TGStickstatus.txt", mode='w')
            strJson.write("Error opening port. "+str(e))
            strJson.close()            
            exit()
        if printStatus: print("Serial port opened...{0}".format(port))
        strJson = open(os.path.abspath("__file___") + "/../../../../../TGStickstatus.txt", mode='w')
        strJson.write("TG Stick connected properly,"+port)
        # Make sure the stopThread event is not set
        stopThread.clear()

        # Start the serial port handler thread
        readThread = threading.Thread(target=self.serialReadHandler, args=(serial_port,rxQ,listenerQ))
        readThread.daemon = True # This kills the thread when main program exits
        readThread.start()
        readThread.name = 'readThread'
        threadPool.append(readThread)
        if printStatus: print('Serial port read handler thread started.')

        writeThread = threading.Thread(target=self.serialWriteHandler, args=(serial_port,))
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
        self.stopThreads()
        exit()
        return


    """ Serial Port methods """
    def serialReadHandler(self,ser,rxQ=False,listenerQ=False):
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

    def stopThreads(self):
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

    def serialWriteHandler(self,ser):
        """ Serial port write handler

            Get from a queue blocks if queue is empty so we just loop
            and wait for items

        """
        while not stopThread.isSet():
            try:
                myMessage = txQueue.get(timeout=1)
                #myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
                #if debug: print("DEBUG Tx: {},  {}".format(myTime,myMessage))
                if type(myMessage) is str:
                    ser.write(bytearray(myMessage + '\r\n','ascii'))
                else:
                    ser.write(myMessage)
            except queue.Empty:
                pass
        print('Serial write thread exit')
        return 0

serials().startSerialThreads(config.PORT,config.BAUD,True,True,False)