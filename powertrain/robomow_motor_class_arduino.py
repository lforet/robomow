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
		self.isConnected = False
		self._should_stop = threading.Event()
		self._data = 0
		self.port = None
		self.motor1_speed = 0
		self.motor2_speed = 0
		self.com = self.open_serial_port()

    
	def open_serial_port(self):
		while self.isConnected == False:
			print "class robomow_motor: searching serial ports for motor controller package..."
			for i in range(11):
				com = "/dev/ttyUSB"
				com = com[0:11] + str(i)
				print "class robomow_motor: searching on COM:", com
				time.sleep(.1)
				try:				
					ser = serial.Serial(com, 9600, timeout=1)
					data = ser.readline()
					#print "data=", int(data[3:(len(data)-1)])
					if data[0:2] == "m1":
						#ser.write("X")      # write a string
						print "class robomow_motor: found motor controller package on COM: ", com
						self.isConnected  = True
						time.sleep(.35)
						break
				except:
					pass
				com = "/dev/ttyACM"
				com = com[0:11] + str(i)
				print "class robomow_motor: searching on COM:", com
				time.sleep(.1)
				try:				
					ser = serial.Serial(com, 9600, timeout=1)
					data = ser.readline()
					#print "data=", int(data[3:(len(data)-1)])
					if data[0:2] == "m1":
						#ser.write("X\n")      # write a string
						print "class robomow_motor: found robomow_motor package on COM: ", com
						self.isConnected  = True
						time.sleep(.35)
						break
				except:
					pass
			if self.isConnected == False:
				print "class robomow_motor: robomow_motor package not found!"
				time.sleep(1)
		#print "returning", ser
		return ser

	def __del__(self):
		del(self)

	def com_stats(self):
		#print self.com
		return (self.com.port,self.com.baudrate,self.com.bytesize,self.com.parity,self.com.stopbits)

	def forward(self,speed):
		##takes desired speed as percentage
		self.com.flushInput()
		command_str = ("FW"+str(speed))
		validate_command(self, command_str)
		self.motor_stats()


	def reverse(self,speed):
		##takes desired speed as percentage
		self.com.flushInput()
		command_str = ("RV"+str(speed))
		validate_command(self, command_str)
		self.motor_stats()

	def stop(self):
		##takes desired speed as percentage
		command_str = ("ST")
		validate_command(self, command_str)
		self.motor_stats()

	def left(self, speed):
		##takes desired speed as percentage
		command_str = ("LF"+str(speed))
		validate_command(self, command_str)
		self.motor_stats()

	def right(self, speed):
		##takes desired speed as percentage
		command_str = ("RT"+str(speed))
		validate_command(self, command_str)
		self.motor_stats()

	def motor_stats(self):
		##takes desired speed as percentage
		cmd = ("SP")
		successful = False
		for n in range (5):
			time.sleep(0.01)
			self.com.flushOutput()
			#print "sending to motor arduino:", cmd
			self.com.write (cmd)
			received = ""
			self.com.flushInput()
			received = received + self.com.readline()
			received = received + self.com.readline()
			received = received + self.com.readline()
			#print "received back from arduino:", received
			#print len(received)
			received = received.replace('\r\n', '')
			received = received.replace('m1:', '')
			received = received.replace('m', '')
			received = received.replace(':', '')
			#print "stripped:", received, "  cmd:", cmd
			#cmd = cmd[0] + cmd[1]
			if (len(received) > 0):
				if (received[0]+received[1] == cmd[0]+cmd[1]):
					#print "successful: sending to motor arduino"
					received = received.strip("SP")
					#print "received now:", received
					spd_list = received.split(',')
					#print spd_list
					successful = True
					self.motor1_speed = spd_list[0]
					self.motor2_speed = spd_list[1] 	 		
					break
		if (successful == False):
				print "NOT successful: sending to motor arduino"

def validate_command(self, cmd):
		successful = False
		for n in range (5):
			time.sleep(0.01)
			self.com.flushOutput()
			#print "sending to motor arduino:", cmd
			self.com.write (cmd)
			received = ""
			self.com.flushInput()
			received = self.com.readline()
			#print "received back from arduino:", received
			#print len(received)
			received = received.replace('\r\n', '')
			received = received.replace('m1:', '')
			received = received.replace('m', '')
			received = received.replace(':', '')
			#print "stripped:", received, "  cmd:", cmd
			if (received == cmd):
				#print "successful: sending to motor arduino"
				successful = True		 		
				break
		if (successful == False):
				print "NOT successful: sending to motor arduino"


