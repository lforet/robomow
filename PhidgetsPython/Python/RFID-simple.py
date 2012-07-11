#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'May 17 2010'

#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, OutputChangeEventArgs, TagEventArgs
from Phidgets.Devices.RFID import RFID

#Create an RFID object
try:
    rfid = RFID()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (rfid.isAttached(), rfid.getDeviceName(), rfid.getSerialNum(), rfid.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of outputs: %i -- Antenna Status: %s -- Onboard LED Status: %s" % (rfid.getOutputCount(), rfid.getAntennaOn(), rfid.getLEDOn()))

#Event Handler Callback Functions
def rfidAttached(e):
    attached = e.device
    print("RFID %i Attached!" % (attached.getSerialNum()))

def rfidDetached(e):
    detached = e.device
    print("RFID %i Detached!" % (detached.getSerialNum()))

def rfidError(e):
    try:
        source = e.device
        print("RFID %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def rfidOutputChanged(e):
    source = e.device
    print("RFID %i: Output %i State: %s" % (source.getSerialNum(), e.index, e.state))

def rfidTagGained(e):
    source = e.device
    rfid.setLEDOn(1)
    print("RFID %i: Tag Read: %s" % (source.getSerialNum(), e.tag))

def rfidTagLost(e):
    source = e.device
    rfid.setLEDOn(0)
    print("RFID %i: Tag Lost: %s" % (source.getSerialNum(), e.tag))

#Main Program Code
try:
    rfid.setOnAttachHandler(rfidAttached)
    rfid.setOnDetachHandler(rfidDetached)
    rfid.setOnErrorhandler(rfidError)
    rfid.setOnOutputChangeHandler(rfidOutputChanged)
    rfid.setOnTagHandler(rfidTagGained)
    rfid.setOnTagLostHandler(rfidTagLost)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    rfid.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    rfid.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        rfid.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Turning on the RFID antenna....")
rfid.setAntennaOn(True)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

try:
    lastTag = rfid.getLastTag()
    print("Last Tag: %s" % (lastTag))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

print("Closing...")

try:
    rfid.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)