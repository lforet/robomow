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
from Phidgets.Phidget import PhidgetID
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.TextLCD import TextLCD, TextLCD_ScreenSize

#Create an TextLCD object
try:
    textLCD = TextLCD()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    try:
        isAttached = textLCD.isAttached()
        name = textLCD.getDeviceName()
        serialNo = textLCD.getSerialNum()
        version = textLCD.getDeviceVersion()
        rowCount = textLCD.getRowCount()
        columnCount = textLCD.getColumnCount()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        return 1
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (isAttached, name, serialNo, version))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Rows: %i -- Number of Columns: %i" % (rowCount, columnCount))

#Event Handler Callback Functions
def TextLCDAttached(e):
    attached = e.device
    print("TextLCD %i Attached!" % (attached.getSerialNum()))

def TextLCDDetached(e):
    detached = e.device
    print("TextLCD %i Detached!" % (detached.getSerialNum()))

def TextLCDError(e):
    try:
        source = e.device
        print("TextLCD %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

#Main Program Code
try:
    textLCD.setOnAttachHandler(TextLCDAttached)
    textLCD.setOnDetachHandler(TextLCDDetached)
    textLCD.setOnErrorhandler(TextLCDError)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    textLCD.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    textLCD.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        textLCD.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    if textLCD.getDeviceID()==PhidgetID.PHIDID_TEXTLCD_ADAPTER:
        textLCD.setScreenIndex(0)
        textLCD.setScreenSize(TextLCD_ScreenSize.PHIDGET_TEXTLCD_SCREEN_2x8)
    
    print("Writing to first row....")
    textLCD.setDisplayString(0, "Row 1")
    sleep(2)
    
    print("Writing to second row....")
    textLCD.setDisplayString(1, "Row 2")
    sleep(2)
    
    print("Adjusting contrast up....")
    textLCD.setContrast(255)
    sleep(2)
    
    print("Adjusting contrast down....")
    textLCD.setContrast(110)
    sleep(2)
    
    print("Turn on cursor....")
    textLCD.setCursor(True)
    sleep(2)
    
    print("Turn on cursor blink....")
    textLCD.setCursor(False)
    textLCD.setCursorBlink(True)
    sleep(2)
    
    print("Clear the screen...")
    textLCD.setCursorBlink(False)
    textLCD.setDisplayString(0, "")
    textLCD.setDisplayString(1, "")
    sleep(2)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

try:
    print("Display some custom characters...")
    print("Set the custom chars....")
    textLCD.setCustomCharacter(0, 949247, 536)
    textLCD.setCustomCharacter(1, 1015791, 17180)
    textLCD.setCustomCharacter(2, 1048039, 549790)
    textLCD.setCustomCharacter(3, 1031395, 816095)
    textLCD.setCustomCharacter(4, 498785, 949247)
    textLCD.setCustomCharacter(5, 232480, 1015791)
    textLCD.setCustomCharacter(6, 99328, 1048039)
    print("Display the custom chars....")
    textLCD.setDisplayString(0, "Custom..")
    customString = textLCD.getCustomCharacter(0)
    customString += textLCD.getCustomCharacter(1)
    customString += textLCD.getCustomCharacter(2)
    customString += textLCD.getCustomCharacter(3)
    customString += textLCD.getCustomCharacter(4)
    customString += textLCD.getCustomCharacter(5)
    customString += textLCD.getCustomCharacter(6)
    textLCD.setDisplayString(1, customString)
    sleep(2)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

textLCD.setDisplayString(0, "")
textLCD.setDisplayString(1, "")

try:
    textLCD.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)