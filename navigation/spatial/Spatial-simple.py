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
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan

#Create an accelerometer object
try:
    spatial = Spatial()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (spatial.isAttached(), spatial.getDeviceName(), spatial.getSerialNum(), spatial.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Acceleration Axes: %i" % (spatial.getAccelerationAxisCount()))
    print("Number of Gyro Axes: %i" % (spatial.getGyroAxisCount()))
    print("Number of Compass Axes: %i" % (spatial.getCompassAxisCount()))

#Event Handler Callback Functions
def SpatialAttached(e):
    attached = e.device
    print("Spatial %i Attached!" % (attached.getSerialNum()))

def SpatialDetached(e):
    detached = e.device
    print("Spatial %i Detached!" % (detached.getSerialNum()))

def SpatialError(e):
    try:
        source = e.device
        print("Spatial %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def SpatialData(e):
    source = e.device
    print("Spatial %i: Amount of data %i" % (source.getSerialNum(), len(e.spatialData)))
    for index, spatialData in enumerate(e.spatialData):
        print("=== Data Set: %i ===" % (index))
        if len(spatialData.Acceleration) > 0:
            print("Acceleration> x: %6f  y: %6f  z: %6f" % (spatialData.Acceleration[0], spatialData.Acceleration[1], spatialData.Acceleration[2]))
        if len(spatialData.AngularRate) > 0:
            print("Angular Rate> x: %6f  y: %6f  z: %6f" % (spatialData.AngularRate[0], spatialData.AngularRate[1], spatialData.AngularRate[2]))
        if len(spatialData.MagneticField) > 0:
            print("Magnetic Field> x: %6f  y: %6f  z: %6f" % (spatialData.MagneticField[0], spatialData.MagneticField[1], spatialData.MagneticField[2]))
        print("Time Span> Seconds Elapsed: %i  microseconds since last packet: %i" % (spatialData.Timestamp.seconds, spatialData.Timestamp.microSeconds))
    
    print("------------------------------------------")

#Main Program Code
try:
    spatial.setOnAttachHandler(SpatialAttached)
    spatial.setOnDetachHandler(SpatialDetached)
    spatial.setOnErrorhandler(SpatialError)
    spatial.setOnSpatialDataHandler(SpatialData)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    spatial.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    spatial.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        spatial.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    spatial.setDataRate(1000)
    DisplayDeviceInfo()

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    spatial.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
