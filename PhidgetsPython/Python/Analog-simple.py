#! /usr/bin/python

"""Copyright 2011 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__="Adam Stelmack"
__version__="2.1.8"
__date__ ="13-Jan-2011 4:28:27 PM"

#Basic imports
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Analog import Analog

#Create an accelerometer object
try:
    analog = Analog()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (analog.isAttached(), analog.getDeviceName(), analog.getSerialNum(), analog.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of analog outputs: %i" % (analog.getOutputCount()))
    print("Maximum output voltage: %d" % (analog.getVoltageMax(0)))
    print("Minimum output voltage: %d" % (analog.getVoltageMin(0)))

#Event Handler Callback Functions
def AnalogAttached(e):
    attached = e.device
    print("Analog %i Attached!" % (attached.getSerialNum()))

def AnalogDetached(e):
    detached = e.device
    print("Analog %i Detached!" % (detached.getSerialNum()))

def AnalogError(e):
    try:
        source = e.device
        print("Analog %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

#Main Program Code
try:
    analog.setOnAttachHandler(AnalogAttached)
    analog.setOnDetachHandler(AnalogDetached)
    analog.setOnErrorhandler(AnalogError)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    analog.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    analog.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        analog.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

try:
    print("Enabling Analog output channel 0...")
    analog.setEnabled(0, True)
    sleep(5)

    print("Set analog output voltage to +5.00V...")
    analog.setVoltage(0, 5.00)
    sleep(5)

    print("Set analog output voltage to -5.00V...")
    analog.setVoltage(0, -5.00)
    sleep(5)

    print("Set analog output voltage to +0.00V...")
    analog.setVoltage(0, 0.00)
    sleep(5)

    print("Disabling Analog output channel 0...")
    analog.setEnabled(0, False)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    analog.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)