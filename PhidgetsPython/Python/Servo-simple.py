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
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Servo import Servo, ServoTypes

#Create an servo object
try:
    servo = Servo()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (servo.isAttached(), servo.getDeviceName(), servo.getSerialNum(), servo.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of motors: %i" % (servo.getMotorCount()))

#Event Handler Callback Functions
def ServoAttached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))

def ServoDetached(e):
    detached = e.device
    print("Servo %i Detached!" % (detached.getSerialNum()))

def ServoError(e):
    try:
        source = e.device
        print("Servo %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def ServoPositionChanged(e):
    source = e.device
    print("Servo %i: Motor %i Current Position: %f" % (source.getSerialNum(), e.index, e.position))

#Main Program Code
try:
    servo.setOnAttachHandler(ServoAttached)
    servo.setOnDetachHandler(ServoDetached)
    servo.setOnErrorhandler(ServoError)
    servo.setOnPositionChangeHandler(ServoPositionChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    servo.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    servo.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        servo.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    print("Setting the servo type for motor 0 to HITEC_HS322HD")
    servo.setServoType(0, ServoTypes.PHIDGET_SERVO_HITEC_HS322HD)
    #Setting custom servo parameters example - 600us-2000us == 120 degrees
    #servo.setServoParameters(0, 600, 2000, 120)
    print("Move to position 10.00")
    servo.setPosition(0, 10.00)
    sleep(5)
    
    print("Move to position 50.00")
    servo.setPosition(0, 50.00)
    sleep(5)
    
    print("Move to position 100.00")
    servo.setPosition(0, 100.00)
    sleep(5)
    
    print("Move to position 150.00")
    servo.setPosition(0, 150.00)
    sleep(5)
    
    print("Move to position PositionMax")
    servo.setPosition(0, servo.getPositionMax(0))
    sleep(5)
    
    print("Move to position PositionMin")
    servo.setPosition(0, servo.getPositionMin(0))
    sleep(5)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    servo.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)