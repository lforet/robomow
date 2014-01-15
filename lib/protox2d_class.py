#!/usr/bin/env python

"""

SUMMARY:
	This library allows interface to ProxoX2D LIDAR. 
	
	Call with the string ID of the device.
	
	Returns: array of 360 elements. The index is the angle, the array element value is distance in mm.
	

EXAMPLE USAGE:
	lidar = protox2d('A1')
	data = lidar.read_lidar()
	print data
"""

import serial
#import threading
import time
#import os
from serial.tools import list_ports

#import sys
#sys.path.append( "../../libs/" )
from identify_device_on_ttyport import *

NUMBER_READINGS = 2

class protox2d():
	def __init__(self, protox2dID):
		self.lidar_data = None
		self.id = protox2dID
		self.x_angle = 0
		self.y_angle = 0
		self.distance_mm = 0
		self.quality = 0
		self.rpm = 0
		# serial port
		self.com_port = None
		self.baudrate = 115200
		self.ser = None
		self._isConnected = False
		self.data = []
		#-------------connection variables
		self.feed_num = 'protox2d.1'
		self.connection = None
		self.channel = None
		#----------------------RUN
		self.run()

	def connect_to_lidar(self):
		while self._isConnected == False:
			print "protox2d: searching serial ports for protox2d..."
			ports =  find_usb_tty("10c4","ea60")
			if (len(ports) > 0):
				for port_to_try in ports:
					print "protox2d: attempting connection to port:", port_to_try
					try:				
						#could actually get serial number from device from list_serial _ports and look specifically for that one
						ser = serial.Serial(port_to_try, 115200)
						if (ser.isOpen() == True):
							print "Connected. Waiting 5 seconds for ProtoX2D to spin up."							
							time.sleep(5)
							temp_data = ser.readline()
							temp_data = temp_data.strip('\r\n')
							data = temp_data.split(',')
							print data
							if data[0] == self.id :
								#ser.write("a\n")      # write a string
								print "protox2d with id:", self.id, " connected to on serial port: ", port_to_try
								self._isConnected  = True
								self.ser = ser
								#time.sleep(.35)
								break
					except:
						pass
					time.sleep(.5)
			if self._isConnected == False:
				print "protox2d: protox2d sensor package not found!"
				time.sleep(.5)
		#print "returning", ser
		return ser

	def connect(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		#channel.queue_declare(queue='mobot_video1', auto_delete=True, arguments={'x-message-ttl':1000})
		self.channel.exchange_declare(exchange='mobot_data_feed',type='topic')	
	
	def publish(self, data):
			self.channel.basic_publish(exchange='mobot_data_feed', 
								routing_key=self.feed_num, body=data)
	
	def run(self):
		self.connect_to_lidar()
		#if self.ser != None:
		#	self.connect()
		#	self.th = thread.start_new_thread(self.read_lidar, ())
		

	def read_lidar(self):
			temp_array = [0] * 360
			num_of_readings = (360 * NUMBER_READINGS)
			for reading in range(num_of_readings):							
				temp_data = self.ser.readline()
				temp_data = temp_data.strip('\r\n')
				lidar_data = temp_data.split(',')
				try:
					#self.id = lidar_data[0]
					#self.x_angle = int(lidar_data[1])
					self.y_angle = int(lidar_data[2])
					self.distance_mm = int(lidar_data[3])
					self.quality = int(lidar_data[4])
					#self.rpm = int(lidar_data[5])
					if self.quality > 0:
						temp_array[self.y_angle] = self.distance_mm 
				except:
					pass
			#zero_distance = 0
			#for i in range(360):
			#	if temp_array[i] == 0: zero_distance = zero_distance + 1
				#print "angle: ", i, "  distance_mm: ", temp_array[i]
			#print "zero_distance:",zero_distance
			return temp_array

if __name__== "__main__":
	lidar = protox2d('A1')
	while True:
		#time.sleep(3)
		data = lidar.read_lidar()
		print data, len(data)

