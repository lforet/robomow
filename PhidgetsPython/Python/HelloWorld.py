#! /usr/env/python

'''
# 
# Phidget Hello World program for all devices
# (c) Phidgets 2012
#
'''

from ctypes import *
import sys

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Manager import Manager
from Phidgets.Devices import *

# ========== Event Handling Functions ==========

def AttachHandler(event):
    attachedDevice = event.device
    serialNumber = attachedDevice.getSerialNum()
    deviceName = attachedDevice.getDeviceName()
    print("Hello to Device " + str(deviceName) + ", Serial Number: " + str(serialNumber))

def DetachHandler(event):
    detachedDevice = event.device
    serialNumber = detachedDevice.getSerialNum()
    deviceName = detachedDevice.getDeviceName()
    print("Goodbye Device " + str(deviceName) + ", Serial Number: " + str(serialNumber))
    
def LibraryErrorHandler(event):
    try: 
        errorDevice = event.device
        serialNumber = errorDevice.getSerialNum()
        print("Error with Serial Number " + str(serialNumber))
    except PhidgetException as e: LocalErrorCatcher(e)

# =========== Python-specific Exception Handler ==========        
        
def LocalErrorCatcher(event):
    print("Phidget Exception: " + str(e.code) + " - " + str(e.details) + ", Exiting...")
    exit(1)

# ========= Main Code ==========        
        
try: manager = Manager()
except RuntimeError as e:
    print("Runtime Error " + e.details + ", Exiting...\n")
    exit(1)

try:
    manager.setOnAttachHandler(AttachHandler)
    manager.setOnDetachHandler(DetachHandler)
    manager.setOnErrorHandler(LibraryErrorHandler)
except PhidgetException as e: LocalErrorCatcher(e)

print("Opening....")
try:
    # This would be openPhidget for a specific device object
    manager.openManager()
except PhidgetException as e: LocalErrorCatcher(e)

print("Phidget Simple Playground (plug and unplug devices)");
print("Press Enter to end anytime...");
character = str(raw_input())

print("Closing...")
try:
    # This would be closePhidget() for a specific device object
    manager.closeManager()
except PhidgetException as e: LocalErrorCatcher(e)

exit(0)

