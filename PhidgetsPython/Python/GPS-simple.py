#! /usr/bin/python

"""Copyright 2011 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__="Adam Stelmack"
__version__="2.1.8"
__date__ ="14-Jan-2011 3:01:06 PM"

#Basic imports
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS

#Create an accelerometer object
try:
    gps = GPS()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (gps.isAttached(), gps.getDeviceName(), gps.getSerialNum(), gps.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")

#Event Handler Callback Functions
def GPSAttached(e):
    attached = e.device
    print("GPS %i Attached!" % (attached.getSerialNum()))

def GPSDetached(e):
    detached = e.device
    print("GPS %i Detached!" % (detached.getSerialNum()))

def GPSError(e):
    try:
        source = e.device
        print("GPS %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def GPSPositionChanged(e):
    source = e.device
    print("GPS %i: Latitude: %F, Longitude: %F, Altitude: %F" % (source.getSerialNum(), e.latitude, e.longitude, e.altitude))

def GPSPositionFixStatusChanged(e):
    source = e.device
    if e.positionFixStatus:
        status = "FIXED"
    else:
        status = "NOT FIXED"
    print("GPS %i: Position Fix Status: %s" % (source.getSerialNum(), status))

#Main Program Code
try:
    gps.setOnAttachHandler(GPSAttached)
    gps.setOnDetachHandler(GPSDetached)
    gps.setOnErrorhandler(GPSError)
    gps.setOnPositionChangeHandler(GPSPositionChanged)
    gps.setOnPositionFixStatusChangeHandler(GPSPositionFixStatusChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    gps.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        gps.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Press Enter to quit....")

try:
    print("GPS Current Time: %s" %(gps.getTime().toString()))
    print("GPS Current Date: %s" %(gps.getDate().toString()))
    print("GPS Current Latitude: %F" %(gps.getLatitude()))
    print("GPS Current Longitude: %F" %(gps.getLongitude()))
    print("GPS Current Altitude: %F" %(gps.getAltitude()))
    print("GPS Current Heading: %F" %(gps.getHeading()))
    print("GPS Current Velocity: %F" % (gps.getVelocity()))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

chr = sys.stdin.read(1)

print("Closing...")

try:
    gps.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)