import os
import time
import datetime
import serial
from serial.tools import list_ports

def find_device():
    timeout = 10
    while timeout != 0:
        port = None
        for p in list_ports.comports():
#            print p[2]
#            if p[2].upper().startswith('USB VID:PID=2886:0004'):
            if p[2].upper().startswith('FTDIBUS\VID_0403+PID_6015'):
#            if p[2].upper().startswith('USB VID:PID=2341:0043'):
                port = p[0]
                print('find port: ' + port)
                return port

        time.sleep(0.1)
        timeout -= 1

    print('No FTDI chip found')
    return None

def UartTest():
    flag=0
    port=find_device()
    if port is None:
        return None
    time.sleep(0.1)
    serial1 = serial.Serial(port=port,
                            baudrate=115200,
                            bytesize=8,
                            stopbits=1,
                            timeout=1)
    
    time.sleep(1)
    n=0
    while(n<1):
        line=serial1.readline()
        if line:
            print("rx:" + line)
        time.sleep(0.1)
        n=n+1
    n=0 
#-----------------------get the first resut----------------------------#
    try:
        print("tx: P 50 1")
        serial1.write("P 50 1" + '\r\n')
    except IOError as e:
        print(e)
        serial1.close

    while(n<31):
        line=serial1.readline()
        if line:
            print("rx:" + line)
        time.sleep(0.01)
        n=n+1
#-----------------------get the second resut----------------------------#
    raw_input("Enter Key to continue...")       #press the swith and press enter key
    try:
        print("tx: P 50 2")
        serial1.write("P 50 2" + '\r\n')
    except IOError as e:
        print(e)
        serial1.close
    n=0
    while(n<31):
        line=serial1.readline()
        if line:
            print("rx:" + line)
        time.sleep(0.01)
        n=n+1
#-----------------------get the test resut----------------------------#
    try:
        print("tx: P 60")
        serial1.write("P 60" + '\r\n')
    except IOError as e:
        print(e)
        serial1.close
    n=0
    while(n<5):
        line=serial1.readline()
        if line:
            print("rx:" + line)
        time.sleep(0.01)
        n=n+1
    serial1.close
'''
    n=0
    while(n<10):
        line=serial1.readline()
        if line:
            print("rx:" + line)
            if ("IO FAIL" in line):
                print "IO Test Fail"
                error_flag=False
                return None
            else:
                print "IO Test OK"
        time.sleep(0.1)
        n=n+1
    serial1.close()
    return "OK"
'''
#-------------------------------------------------------------#

while True:
    result=UartTest()
    raw_input("Enter to Test Next")



