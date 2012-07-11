#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'July 14 2010'

#Basic imports
from ctypes import *
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import ErrorEventArgs, KeyChangeEventArgs, ServerConnectArgs, ServerDisconnectArgs
from Phidgets.Dictionary import Dictionary, DictionaryKeyChangeReason, KeyListener

#Create a Dictionary object and a key listener object
try:
    dictionary = Dictionary()
    keyListener = KeyListener(dictionary, ".*")
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Event Handler Callback Functions
def DictionaryError(e):
    print("Dictionary Error %i: %s" % (e.eCode, e.description))
    return 0

def DictionaryServerConnected(e):
    print("Dictionary connected to server %s" % (e.device.getServerAddress()))
    try:
        keyListener.start()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
    return 0

def DictionaryServerDisconnected(e):
    print("Dictionary disconnected from server")
    try:
        keyListener.stop()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
    return 0

def KeyChanged(e):
    if e.reason == DictionaryKeyChangeReason.PHIDGET_DICTIONARY_VALUE_CHANGED:
        reason = "Value Changed"
    elif e.reason == DictionaryKeyChangeReason.PHIDGET_DICTIONARY_ENTRY_ADDED:
        reason = "Entry Added"
    elif e.reason == DictionaryKeyChangeReason.PHIDGET_DICTIONARY_ENTRY_REMOVING:
        reason = "Entry Removed"
    elif e.reason == DictionaryKeyChangeReason.PHIDGET_DICTIONARY_CURRENT_VALUE:
        reason = "Current Value"
    
    print("%s -- Key: %s -- Value: %s" % (reason, e.key, e.value))
    return 0

def KeyRemoved(e):
    if e.reason == DictionaryKeyChangeReason.PHIDGET_DICTIONARY_VALUE_CHANGED:
        reason = "Value Changed"
    elif e.reason == DictionaryKeyChangeReason.PHIDGET_DICTIONARY_ENTRY_ADDED:
        reason = "Entry Added"
    elif e.reason == DictionaryKeyChangeReason.PHIDGET_DICTIONARY_ENTRY_REMOVING:
        reason = "Entry Removed"
    elif e.reason == DictionaryKeyChangeReason.PHIDGET_DICTIONARY_CURRENT_VALUE:
        reason = "Current Value"
    
    print("%s -- Key: %s -- Value: %s" % (reason, e.key, e.value))
    return 0

#Main Program Code
try:
    dictionary.setErrorHandler(DictionaryError)
    dictionary.setServerConnectHandler(DictionaryServerConnected)
    dictionary.setServerDisconnectHandler(DictionaryServerDisconnected)
    
    keyListener.setKeyChangeHandler(KeyChanged)
    keyListener.setKeyRemovalListener(KeyRemoved)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening Dictionary object....")

try:
    dictionary.openRemoteIP("adam.local", 5001)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

try:
    while dictionary.isAttachedToServer() == False:
        pass
    else:
        print("Connected: %s" % (dictionary.isAttachedToServer()))
        print("Server: %s:%s" % (dictionary.getServerAddress(), dictionary.getServerPort()))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

try:
    print("Now we'll add some keys...")
    sleep(1)
    
    dictionary.addKey("test1", "ok")
    dictionary.addKey("test2", "ok", True)
    dictionary.addKey("test3", "ok", False)
    dictionary.addKey("test4", "ok", True)
    sleep(2)
    
    print("Now we will test for key 'test2' being in the dictionary.")
    sleep(1)
    
    value = dictionary.getKey("test2")
    print("Key: test2  Value: %s" % (value))
    
    print("Now we will remove one of the keys...")
    sleep(1)
    
    dictionary.removeKey("test4")
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    keyListener.stop()
    dictionary.closeDictionary()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)