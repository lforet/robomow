#! /usr/bin/python

"""Copyright 2011 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__="Adam Stelmack"
__version__="2.1.8"
__date__ ="14-Jan-2011 10:55:59 AM"

#Basic imports
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.FrequencyCounter import FrequencyCounter, FilterType

#Create an accelerometer object
try:
    freqCount = FrequencyCounter()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (freqCount.isAttached(), freqCount.getDeviceName(), freqCount.getSerialNum(), freqCount.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of frequency inputs: %i" % (freqCount.getFrequencyInputCount()))

#Event Handler Callback Functions
def FrequencyCounterAttached(e):
    attached = e.device
    print("Frequency Counter %i Attached!" % (attached.getSerialNum()))

def FrequencyCounterDetached(e):
    detached = e.device
    print("Frequency Counter %i Detached!" % (detached.getSerialNum()))

def FrequencyCounterError(e):
    try:
        source = e.device
        print("Frequency Counter %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def FrequencyCount(e):
    source = e.device
    print("Frequency Counter %i: Count Detected -- Index %i: Time %i -- Counts %i" % (source.getSerialNum(), e.index, e.time, e.counts))

#Main Program Code
try:
    freqCount.setOnAttachHandler(FrequencyCounterAttached)
    freqCount.setOnDetachHandler(FrequencyCounterDetached)
    freqCount.setOnErrorhandler(FrequencyCounterError)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    freqCount.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    freqCount.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        freqCount.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

try:
    print("Set timeout to be 10seconds (100,000 microseconds)...")
    freqCount.setTimeout(0, 100000)
    sleep(5)

    print("Set filter type to LOGIC_LEVEL...")
    freqCount.setFilter(0, FilterType.FILTERTYPE_LOGIC_LEVEL)
    
    print("Poll device for data")
    print("Enabling frequency input channel 0...")
    freqCount.setEnabled(0, True)
    sleep(5)

    print("Frequency Data -- Frequency: %d Hz  Total Time: %i ms  Total Counts: %i" % (freqCount.getFrequency(0), (freqCount.getTotalTime(0) / 100), freqCount.getTotalCount(0)))

    print("Disabling frequency input channel 0...")
    freqCount.setEnabled(0, False)
    sleep(5)

    print("Resetting frequency input channel 0...")
    freqCount.reset(0)
    sleep(5)

    print("Set up event handling...")
    freqCount.setOnFrequencyCountHandler(FrequencyCount)

    print("Enabling frequency input channel 0...")
    freqCount.setEnabled(0, True)
    sleep(5)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        freqCount.closePhidget()
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
    print("Disabling frequency input channel 0...")
    freqCount.setEnabled(0, False)
    sleep(5)

    print("Resetting frequency input channel 0...")
    freqCount.reset(0)
    sleep(5)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        freqCount.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

try:
    freqCount.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)