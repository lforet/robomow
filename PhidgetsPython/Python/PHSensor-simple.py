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
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, PHChangeEventArgs
from Phidgets.Devices.PHSensor import PHSensor

#Create an PHSensor object
try:
    phSensor = PHSensor()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (phSensor.isAttached(), phSensor.getDeviceName(), phSensor.getSerialNum(), phSensor.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("PH Sensitivity: %f" % (phSensor.getPHChangeTrigger()))
    print("Current Potential: %f" % (phSensor.getPotential()))

#Event Handler Callback Functions
def phSensorAttached(e):
    attached = e.device
    print("PHSensor %i Attached!" % (attached.getSerialNum()))

def phSensorDetached(e):
    detached = e.device
    print("PHSensor %i Detached!" % (detached.getSerialNum()))

def phSensorError(e):
    try:
        source = e.device
        print("PHSensor %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def phSensorPHChanged(e):
    source = e.device
    potential = phSensor.getPotential()
    print("PHSensor %i: PH: %f -- Potential: %f" % (source.getSerialNum(), e.PH, potential))

#Main Program Code
try:
    phSensor.setOnAttachHandler(phSensorAttached)
    phSensor.setOnDetachHandler(phSensorDetached)
    phSensor.setOnErrorhandler(phSensorError)
    phSensor.setOnPHChangeHandler(phSensorPHChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    phSensor.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    phSensor.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        phSensor.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Increasing sensitivity to 10.00")
phSensor.setPHChangeTrigger(10.00)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    phSensor.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)