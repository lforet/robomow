#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'May 11 2010'

#Basic imports
from ctypes import *
import sys
import math
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, IRCodeEventArgs, IRLearnEventArgs, IRRawDataEventArgs
from Phidgets.Devices.IR import IR, IRCode, IRCodeInfo, IRCodeLength, IREncoding

#Create an RFID object
try:
    ir = IR()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (ir.isAttached(), ir.getDeviceName(), ir.getSerialNum(), ir.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")

def displayCodeInfo(codeInfo):
    print("----------------------------------------------------")
    print("Bit Count: %d\nEncoding: %s\nLength: %s\nGap: %d\nTrail: %d" % (codeInfo.BitCount, IREncoding.toString(codeInfo.Encoding), IRCodeLength.toString(codeInfo.Length), codeInfo.Gap, codeInfo.Trail))
    if codeInfo.Header != None:
        print("Header: { %d, %d }" % (codeInfo.Header[0], codeInfo.Header[1]))
    else:
        print("Header: Null")
    print("One: { %d, %d }\nZero: { %d, %d }" % (codeInfo.One[0], codeInfo.One[1], codeInfo.Zero[0], codeInfo.Zero[1]))
    
    if codeInfo.Repeat != None:
        printStr = "{ "
        for i in range(len(codeInfo.Repeat)):
            if i > 0:
                printStr += ", "
            printStr += str(codeInfo.Repeat[i])
        printStr += " }"
        
        print("Repeat: %s" % (printStr))
    else:
        print("Repeat: None")
    
    print("MinRepeat: %d\nToggle Mask: %s\nCarrier Frequency: %d\nDuty Cycle: %d" % (codeInfo.MinRepeat, codeInfo.ToggleMask.toString(), codeInfo.CarrierFrequency, codeInfo.DutyCycle))
    print("----------------------------------------------------")

def displayRawData(data):
    print("----------------------------------------------------")
    outStr = "Raw Data:"
    for i in range(len(data)):
        if (i % 8) == 0: outStr += "\n"
        if data[i] == IR.RAWDATA_LONGSPACE:
            outStr += "LONG"
        else:
            outStr += str(data[i])
        if ((i + 1) % 8) != 0: outStr += ", "
    print("%s" % (outStr))
    print("----------------------------------------------------")

#Event Handler Callback Functions
def irAttached(e):
    attached = e.device
    print("PhidgetIR %i Attached!" % (attached.getSerialNum()))

def irDetached(e):
    detached = e.device
    print("PhidgetIR %i Detached!" % (detached.getSerialNum()))

def irError(e):
    try:
        source = e.device
        print("PhidgetIR %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def irCodeRecv(e):
    print("Phiget IR Code Receive")
    source = e.device
    if e.repeat:
        repeat = "true"
    else:
        repeat = "false"
    print("PhidgetIR %i Code Receive: Code: %s Repeat: %s" % (source.getSerialNum(), e.code.toString(), repeat))

def irLearnRecv(e):
    source = e.device
    print("PhidgetIR %i Learn Receive: Code: %s -- Code Info:" % (source.getSerialNum(), e.code.toString()))
    displayCodeInfo(e.codeInfo)

def irRawDataRecv(e):
    source = e.device
    print("PhidgetIR %i Raw Data Received:" % (source.getSerialNum()))
    displayRawData(e.rawData)

#Main Program Code
try:
    ir.setOnAttachHandler(irAttached)
    ir.setOnDetachHandler(irDetached)
    ir.setOnErrorhandler(irError)
    ir.setOnIRCodeHandler(irCodeRecv)
    ir.setOnIRLearnHandler(irLearnRecv)
    ir.setOnIRRawDataHandler(irRawDataRecv)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    ir.openPhidget(114101)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    ir.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        ir.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Press enter to transmit a code....")

chr = sys.stdin.read(1)

#send the code for Apple remote Volume UP (Standard NEC encoding)
codeInfo = IRCodeInfo()
codeInfo.Encoding = IREncoding.Space
codeInfo.BitCount = 32
codeInfo.Header = [9078, 4610]
codeInfo.Zero = [593, 581]
codeInfo.One = [593, 1701]
codeInfo.Trail = 593
codeInfo.Gap = 108729
codeInfo.Repeat = [9078, 2345, 593]

try:
    ir.transmit(IRCode("0x77e1d0f0", 32), codeInfo)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

print("Press enter to transmit RAW data....")

chr = sys.stdin.read(1)

#example of sending RAW Data - this was captured from an Apple remote Volume UP command
rawData = (c_int * 67)(9040,   4590,    540,    630,    550,   1740,    550,   1750,    550,   1740,
                       550,    620,    550,   1750,    550,   1740,    550,   1750,    550,   1740,
                       550,   1740,    560,   1740,    540,    630,    550,    620,    550,    620,
                       540,    630,    550,   1750,    550,   1740,    560,   1740,    550,    620,
                       550,   1740,    550,    620,    550,    620,    560,    610,    550,    620,
                       550,   1750,    550,   1740,    550,    620,    550,   1740,    550,   1750,
                       550,    620,    550,    620,    550,    620,    540)

try:
    ir.transmitRaw(rawData, 108729)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

print("Press Enter to quit....")

chr = sys.stdin.read(1)

try:
    lastCode = ir.getLastCode()
    print("Last Code: %s" % (lastCode.toString()))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

try:
    lastLearnedCode = ir.getLastLearnedCode()
    print("Last Learned Code: %s -- Last Learned Code Info:" % (lastLearnedCode.Code.toString()))
    displayCodeInfo(lastLearnedCode.CodeInfo)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

print("Closing...")

try:
    ir.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)