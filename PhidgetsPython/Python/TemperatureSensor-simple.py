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
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, TemperatureChangeEventArgs
from Phidgets.Devices.TemperatureSensor import TemperatureSensor, ThermocoupleType
#import methods for sleeping thread
from time import sleep

#Create an temperaturesensor object
try:
    temperatureSensor = TemperatureSensor()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    inputCount = temperatureSensor.getTemperatureInputCount()
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (temperatureSensor.isAttached(), temperatureSensor.getDeviceName(), temperatureSensor.getSerialNum(), temperatureSensor.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Temperature Inputs: %i" % (inputCount))
    for i in range(inputCount):
        print("Input %i Sensitivity: %f" % (i, temperatureSensor.getTemperatureChangeTrigger(i)))

#Event Handler Callback Functions
def TemperatureSensorAttached(e):
    attached = e.device
    print("TemperatureSensor %i Attached!" % (attached.getSerialNum()))

def TemperatureSensorDetached(e):
    detached = e.device
    print("TemperatureSensor %i Detached!" % (detached.getSerialNum()))

def TemperatureSensorError(e):
    try:
        source = e.device
        if source.isAttached():
            print("TemperatureSensor %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def TemperatureSensorTemperatureChanged(e):
    try:
        ambient = temperatureSensor.getAmbientTemperature()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        ambient = 0.00
    
    source = e.device
    print("TemperatureSensor %i: Ambient Temp: %f -- Thermocouple %i temperature: %f -- Potential: %f" % (source.getSerialNum(), ambient, e.index, e.temperature, e.potential))

#Main Program Code
try:
    temperatureSensor.setOnAttachHandler(TemperatureSensorAttached)
    temperatureSensor.setOnDetachHandler(TemperatureSensorDetached)
    temperatureSensor.setOnErrorhandler(TemperatureSensorError)
    temperatureSensor.setOnTemperatureChangeHandler(TemperatureSensorTemperatureChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    temperatureSensor.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    temperatureSensor.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        temperatureSensor.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

print("Setting Thermocouple type...")
temperatureSensor.setThermocoupleType(0, ThermocoupleType.PHIDGET_TEMPERATURE_SENSOR_K_TYPE)

print("Setting sensitivity of the thermocouple....")
temperatureSensor.setTemperatureChangeTrigger(0, 0.10)
sleep(5) #sleep for 5 seconds
print("Sensitivity of thermocouple index 0 is now %f" % (temperatureSensor.getTemperatureChangeTrigger(0)))

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    temperatureSensor.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)