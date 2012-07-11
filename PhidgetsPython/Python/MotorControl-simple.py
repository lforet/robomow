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
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, InputChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.MotorControl import MotorControl
#import methods for sleeping thread
from time import sleep

#Create an motorcontrol object
try:
    motorControl = MotorControl()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (motorControl.isAttached(), motorControl.getDeviceName(), motorControl.getSerialNum(), motorControl.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")

#Event Handler Callback Functions
def motorControlAttached(e):
    attached = e.device
    print("MotorControl %i Attached!" % (attached.getSerialNum()))

def motorControlDetached(e):
    detached = e.device
    print("MotorControl %i Detached!" % (detached.getSerialNum()))

def motorControlError(e):
    try:
        source = e.device
        print("Motor Control %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def motorControlCurrentChanged(e):
    source = e.device
    print("Motor Control %i: Motor %i Current Draw: %f" % (source.getSerialNum(), e.index, e.current))

def motorControlInputChanged(e):
    source = e.device
    print("Motor Control %i: Input %i State: %s" % (source.getSerialNum(), e.index, e.state))

def motorControlVelocityChanged(e):
    source = e.device
    print("Motor Control %i: Motor %i Current Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))

#Main Program Code
try:
    motorControl.setOnAttachHandler(motorControlAttached)
    motorControl.setOnDetachHandler(motorControlDetached)
    motorControl.setOnErrorhandler(motorControlError)
    motorControl.setOnCurrentChangeHandler(motorControlCurrentChanged)
    motorControl.setOnInputChangeHandler(motorControlInputChanged)
    motorControl.setOnVelocityChangeHandler(motorControlVelocityChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    motorControl.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    motorControl.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        motorControl.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

#Control the motor a bit.
print("Will now simulate motor operation....")
print("Step 1: increase acceleration to 50, set target speed at 100")
try:
    motorControl.setAcceleration(0, 50.00)
    motorControl.setVelocity(0, 100.00)
    sleep(5) #sleep for 5 seconds
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

print("Step 2: Set acceleration to 100, decrease target speed to 75")
try:
    motorControl.setAcceleration(0, 100.00)
    motorControl.setVelocity(0, 75.00)
    sleep(5) #sleep for 5 seconds
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

print("Step 3: Stop the motor by decreasing speed to 0 at 50 acceleration")
try:
    motorControl.setAcceleration(0, 50.00)
    motorControl.setVelocity(0, 0.00)
    sleep(5) #sleep for 5 seconds
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
else:
    try:
        motorControl.setAcceleration(0, 1.00)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    motorControl.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
