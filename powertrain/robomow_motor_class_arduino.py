#!/usr/bin/env python

import serial
import time


def log(*msgline):
	for msg in msgline:
		print msg,
	print

#!/usr/bin/env python

import serial
import threading
import time

# need to find best way to search seria ports for find device

class robomow_motor(object):
	def __init__(self):
		self._isConnected = False
		self._ser = self._open_serial_port()
		self._should_stop = threading.Event()
		self._start_reading()
		self._data = 0
		#self._port = port
		self.lmotor_speed = 0
		self.rmotor_speed = 0
		
    
	def _open_serial_port(self):
		while self._isConnected == False:
			print "class robomow_motor: searching serial ports for motor controller package..."
			for i in range(11):
				port = "/dev/ttyUSB"
				port = port[0:11] + str(i)
				print "class robomow_motor: searching on port:", port
				time.sleep(.2)
				try:				
					ser = serial.Serial(port, 9600, timeout=1)
					data = ser.readline()
					#print "data=", int(data[3:(len(data)-1)])
					if data[0:2] == "m1":
						#ser.write("a\n")      # write a string
						print "class robomow_motor: found motor controller package on serial port: ", port
						self._isConnected  = True
						#self._port = ser
						time.sleep(.35)
						break
				except:
					pass
			for i in range(11):
				port = "/dev/ttyACM"
				port = port[0:11] + str(i)
				print "class robomow_motor: searching on port:", port
				time.sleep(.2)
				try:				
					ser = serial.Serial(port, 9600, timeout=1)
					data = ser.readline()
					#print "data=", int(data[3:(len(data)-1)])
					if data[0:2] == "m1":
						#ser.write("a\n")      # write a string
						print "class robomow_motor: found robomow_motor package on serial port: ", port
						self._isConnected  = True
						#self._port = ser
						time.sleep(.35)
						break
				except:
					pass
			if self._isConnected == False:
				print "class robomow_motor: robomow_motor package not found!"
				time.sleep(1)
		#print "returning", ser
		return ser

	def __del__(self):
		del(self)

	def stats(self):
		return (self.com.portstr, self.com.baudrate,self.com.bytesize,self.com.parity,self.com.stopbits)

	def forward(self,speed):
		##takes desired speed as percentage, returns 2 ints indicating each current motor speed
		motor1_spd = int(63.0 * (float(speed)/100) + 65) 
		motor2_spd = int(63.0 * (float(speed)/100) + 193) 	
		if motor1_spd < 65: motor1_spd = 65
		if motor1_spd > 127: motor1_spd = 127
		if motor2_spd < 193: motor2_spd = 193
		if motor2_spd > 255: motor2_spd = 255
		#print motor1_spd, motor2_spd
		self.com.write (chr(int(hex(motor1_spd),16)))
		#time.sleep(.01)
		self.com.write (chr(int(hex(motor2_spd),16)))
		#print "sending command: ",  int(hex(speed),16)
		#print "sending command: ",  int(hex(speed+127),16)
		self.lmotor_speed = motor1_spd 
		self.rmotor_speed = motor2_spd 

	def reverse(self,speed):
		##takes desired speed as percentage, returns 2 ints indicating each current motor speed
		motor1_spd = 63 - int(63.0 * (float(speed)/100)) 
		motor2_spd = 191 - int(63.0 * (float(speed)/100)) 	
		if motor1_spd < 1: motor1_spd = 1
		if motor1_spd > 63: motor1_spd = 63
		if motor2_spd < 128: motor2_spd = 128
		if motor2_spd > 191: motor2_spd = 191
		#print motor1_spd, motor2_spd
		self.com.write (chr(int(hex(motor1_spd),16)))
		#time.sleep(.01)
		self.com.write (chr(int(hex(motor2_spd ),16)))
		#print "sending command: ",  int(hex(speed),16)
		#print "sending command: ",  int(hex(speed+127),16)
		self.lmotor_speed = motor1_spd 
		self.rmotor_speed = motor2_spd 

	def stop(self):
		self.com.write (chr(int(hex(64),16)))
		#time.sleep(.01)
		self.com.write (chr(int(hex(192),16)))
		self.lmotor_speed = 64 
		self.rmotor_speed = 192

	def left(self, degree):
		motor1_spd = motor1_spd - degree
		motor2_spd = motor2_spd + degree
		if motor1_spd < 1: motor1_spd = 1
		if motor1_spd > 127: motor1_spd = 127
		if motor2_spd < 128: motor1_spd = 128
		if motor2_spd > 255: motor1_spd = 255
		self.com.write (chr(int(hex(motor1_spd),16)))
		#time.sleep(.01)
		self.com.write (chr(int(hex(motor2_spd ),16)))
		self.lmotor_speed = motor1_spd 
		self.rmotor_speed = motor2_spd 

	def right(self, degree):
		motor1_spd = motor1_spd + degree
		motor2_spd = motor2_spd - degree
		if motor1_spd < 1: motor1_spd = 1
		if motor1_spd > 127: motor1_spd = 127
		if motor2_spd < 128: motor1_spd = 128
		if motor2_spd > 255: motor1_spd = 255
		self.com.write (chr(int(hex(motor1_spd),16)))
		#time.sleep(.01)
		self.com.write (chr(int(hex(motor2_spd ),16)))
		self.lmotor_speed = motor1_spd 
		self.rmotor_speed = motor2_spd 




