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
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.Stepper import Stepper

#Create a stepper object
try:
    stepper = Stepper()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (stepper.isAttached(), stepper.getDeviceName(), stepper.getSerialNum(), stepper.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Motors: %i" % (stepper.getMotorCount()))

#Event Handler Callback Functions
def StepperAttached(e):
    attached = e.device
    print("Stepper %i Attached!" % (attached.getSerialNum()))

def StepperDetached(e):
    detached = e.device
    print("Stepper %i Detached!" % (detached.getSerialNum()))

def StepperError(e):
    try:
        source = e.device
        print("Stepper %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def StepperCurrentChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Current Draw: %6f" % (source.getSerialNum(), e.index, e.current))

def StepperInputChanged(e):
    source = e.device
    print("Stepper %i: Input %i -- State: %s" % (source.getSerialNum(), e.index, e.state))

def StepperPositionChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Position: %f" % (source.getSerialNum(), e.index, e.position))

def StepperVelocityChanged(e):
    source = e.device
    print("Stepper %i: Motor %i -- Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))

#Main Program Code
try:
    stepper.setOnAttachHandler(StepperAttached)
    stepper.setOnDetachHandler(StepperDetached)
    stepper.setOnErrorhandler(StepperError)
    stepper.setOnCurrentChangeHandler(StepperCurrentChanged)
    stepper.setOnInputChangeHandler(StepperInputChanged)
    stepper.setOnPositionChangeHandler(StepperPositionChanged)
    stepper.setOnVelocityChangeHandler(StepperVelocityChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    stepper.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    stepper.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        stepper.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    print("Set the current position as start position...")
    stepper.setCurrentPosition(0, 0)
    sleep(1)
    
    print("Set the motor as engaged...")
    stepper.setEngaged(0, True)
    sleep(1)
    
    print("The motor will run until it reaches the set goal position...")
    
    stepper.setAcceleration(0, 87543)
    stepper.setVelocityLimit(0, 6200)
    stepper.setCurrentLimit(0, 0.26)
    sleep(2)
    
    print("Will now move to position 20000...")
    stepper.setTargetPosition(0, 20000)
    while stepper.getCurrentPosition(0) != 20000:
        pass
    
    sleep(2)
    
    print("Will now move back to positon 0...")
    stepper.setTargetPosition(0, 0)
    while stepper.getCurrentPosition(0) != 0:
        pass
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    stepper.setEngaged(0, False)
    sleep(1)
    stepper.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)