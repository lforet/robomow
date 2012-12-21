#!/usr/bin/env python


import serial
import time
import math
#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan



sp = Spatial()
print("Opening phidget object....")

try:
    sp.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    sp.waitForAttach(6000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        sp.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    sp.setDataRate(16)

#print sp.spatialData()
print ("zeroing gyro...")

sp.zeroGyro()
time.sleep(2.2)

north = 0
for i in range (10000):
	try:
		print
		gravity = sp.getAngularRate([0][0]), sp.getAngularRate([1][0]), sp.getAngularRate([2][0])
		print "acc:", gravity
		print "AngularRate:", sp.getAngularRate([0][0]), sp.getAngularRate([1][0]), sp.getAngularRate([2][0])
		magField = sp.getMagneticField([0][0]), sp.getMagneticField([1][0]), sp.getMagneticField([2][0])
		print "MagneticField:", magField
		#print "compass = ", compass
		#if compass <  0:		
		#	compass = compass + 360
			#print "north: ", north, (north / i) , i
		#compassBearing = compass* (180.0 / math.pi);
		#if (compassBearing > 360): compassBearing -= 360;
		#if (compassBearing < 0): compassBearing += 360;
		#print "compass: ", compass

	except:
		print ('..................')
	time.sleep(.1)
	#chr = sys.stdin.read(1)
sp.closePhidget()


