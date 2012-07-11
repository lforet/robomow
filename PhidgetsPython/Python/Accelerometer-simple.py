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
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AccelerationChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Accelerometer import Accelerometer

#Create an accelerometer object
try:
    accelerometer = Accelerometer()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (accelerometer.isAttached(), accelerometer.getDeviceName(), accelerometer.getSerialNum(), accelerometer.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Axes: %i" % (accelerometer.getAxisCount()))

#Event Handler Callback Functions
def AccelerometerAttached(e):
    attached = e.device
    print("Accelerometer %i Attached!" % (attached.getSerialNum()))

def AccelerometerDetached(e):
    detached = e.device
    print("Accelerometer %i Detached!" % (detached.getSerialNum()))

def AccelerometerError(e):
    try:
        source = e.device
        print("Accelerometer %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def AccelerometerAccelerationChanged(e):
    source = e.device
    print("Accelerometer %i: Axis %i: %6f" % (source.getSerialNum(), e.index, e.acceleration))

#Main Program Code
try:
    accelerometer.setOnAttachHandler(AccelerometerAttached)
    accelerometer.setOnDetachHandler(AccelerometerDetached)
    accelerometer.setOnErrorhandler(AccelerometerError)
    accelerometer.setOnAccelerationChangeHandler(AccelerometerAccelerationChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    accelerometer.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    accelerometer.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        accelerometer.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    try:
        numAxis = accelerometer.getAxisCount()
        accelerometer.setAccelChangeTrigger(0, 0.500)
        accelerometer.setAccelChangeTrigger(1, 0.500)
        if numAxis > 2:
            accelerometer.setAccelChangeTrigger(2, 0.500)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
    
    DisplayDeviceInfo()

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    accelerometer.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)