#! /usr/bin/python

"""Copyright 2011 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__="Adam Stelmack"
__version__="2.1.8"
__date__ ="14-Jan-2011 2:29:14 PM"

#Basic imports
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Bridge import Bridge, BridgeGain

#Create an accelerometer object
try:
    bridge = Bridge()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (bridge.isAttached(), bridge.getDeviceName(), bridge.getSerialNum(), bridge.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of bridge inputs: %i" % (bridge.getInputCount()))
    print("Data Rate Max: %d" % (bridge.getDataRateMax()))
    print("Data Rate Min: %d" % (bridge.getDataRateMin()))
    print("Input Value Max: %d" % (bridge.getBridgeMax(0)))
    print("Input Value Min: %d" % (bridge.getBridgeMin(0)))

#Event Handler Callback Functions
def BridgeAttached(e):
    attached = e.device
    print("Bridge %i Attached!" % (attached.getSerialNum()))

def BridgeDetached(e):
    detached = e.device
    print("Bridge %i Detached!" % (detached.getSerialNum()))

def BridgeError(e):
    try:
        source = e.device
        print("Bridge %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def BridgeData(e):
    source = e.device
    print("Bridge %i: Input %i: %i" % (source.getSerialNum(), e.index, e.value))

#Main Program Code
try:
    bridge.setOnAttachHandler(BridgeAttached)
    bridge.setOnDetachHandler(BridgeDetached)
    bridge.setOnErrorhandler(BridgeError)
    bridge.setOnBridgeDataHandler(BridgeData)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    bridge.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    bridge.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

try:
    print("Set data rate to 8ms ...")
    bridge.setDataRate(16)
    sleep(2)

    print("Set Gain to 8...")
    bridge.setGain(0, BridgeGain.PHIDGET_BRIDGE_GAIN_8)
    sleep(2)

    print("Enable the Bridge input for reading data...")
    bridge.setEnabled(0, True)
    sleep(2)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    print("Disable the Bridge input for reading data...")
    bridge.setEnabled(0, False)
    sleep(2)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

try:
    bridge.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)