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
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Phidget import Phidget
from Phidgets.Manager import Manager

#Event Handler Callback Functions
def ManagerDeviceAttached(e):
    attached = e.device
    print("Manager - Device %i: %s Attached!" % (attached.getSerialNum(), attached.getDeviceName()))

def ManagerDeviceDetached(e):
    detached = e.device
    print("Manager - Device %i: %s Detached!" % (detached.getSerialNum(), detached.getDeviceName()))

def ManagerError(e):
    print("Manager Phidget Error %i: %s" % (e.eCode, e.description))

#Create an interfacekit object
try:
    mngr = Manager()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Main Program Code
try:
    mngr.setOnAttachHandler(ManagerDeviceAttached)
    mngr.setOnDetachHandler(ManagerDeviceDetached)
    mngr.setOnErrorHandler(ManagerError)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget manager....")

try:
    mngr.openManager()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

attachedDevices = mngr.getAttachedDevices()

print("|------------|----------------------------------|--------------|------------|")
print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
print("|------------|----------------------------------|--------------|------------|")
for attachedDevice in attachedDevices:
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (attachedDevice.isAttached(), attachedDevice.getDeviceName(), attachedDevice.getSerialNum(), attachedDevice.getDeviceVersion()))

print("|------------|----------------------------------|--------------|------------|")

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    mngr.closeManager()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)