#!/usr/bin/env python

import serial
import time
from struct import *
#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan


def log(*msgline):
	for msg in msgline:
		print msg,
	print



class robomow_spatial(object):
	def __init__(self): 
		############################
		# lets introduce and init the main variables
		#self.com = None
		self.isInitialized = False 
		#Create an accelerometer object
		try:
			self = Spatial()
		except RuntimeError as e:
			print("Runtime Exception: %s" % e.details)
			print("Exiting....")
			exit(1)
		try:
			self.openPhidget()
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting....")
			exit(1)
		print("Waiting for attach....")

		try:
			self.waitForAttach(4000)
			print "is attached = ", self.isAttached()
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			try:
				self.closePhidget()
			except PhidgetException as e:
				print("Phidget Exception %i: %s" % (e.code, e.details))
				print("Exiting....")
				exit(1)
			print("Exiting....")
			exit(1)
		else:
			self.setDataRate(1000)
			
	
		

