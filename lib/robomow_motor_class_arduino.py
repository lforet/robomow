#!/usr/bin/env python

import serial
import time
import os
from serial.tools import list_ports

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
			for i in range(len(list_serial_ports())):
				com = "/dev/ttyACM"
				com = com[0:11] + str(i)
				print "class robomow_motor: searching on COM:", com
				time.sleep(.5)
				try:				
					ser = serial.Serial(com, 57600, timeout=0.2)
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
		#self.com.flushInput()
		command_str = ("FW"+str(speed))
		#validate_command(self, command_str)
		send_command(self, command_str)		
		#self.motor_stats()


	def reverse(self,speed):
		##takes desired speed as percentage
		#self.com.flushInput()
		command_str = ("RV"+str(speed))
		#validate_command(self, command_str)
		send_command(self, command_str)			
		#self.motor_stats()

	def stop(self):
		##takes desired speed as percentage
		command_str = ("FW"+str(0))
		#validate_command(self, command_str)
		send_command(self, command_str)	
		#self.motor_stats()

	def spin_left(self, speed):
		##takes desired speed as percentage
		command_str = ("SL"+str(speed))
		#validate_command(self, command_str)
		send_command(self, command_str)	
		#self.motor_stats()

	def spin_right(self, speed):
		##takes desired speed as percentage
		command_str = ("SR"+str(speed))
		#validate_command(self, command_str)
		send_command(self, command_str)	
		#self.motor_stats()

	def right(self, speed):
		##takes desired speed as percentage
		command_str = ("M2"+str(speed))
		#validate_command(self, command_str)
		send_command(self, command_str)	
		#self.motor_stats()

	def left(self, speed):
		##takes desired speed as percentage
		command_str = ("M1"+str(speed))
		#validate_command(self, command_str)
		send_command(self, command_str)	
		#self.motor_stats()

	def motor_stats(self):
		##takes desired speed as percentage
		cmd = ("SP")
		successful = False
		for n in range (5):
			time.sleep(0.05)
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
			try:
				if (len(received) > 0 and len(received) < 9):	
					#print "successful: sending to motor arduino"
					received = received.strip("SP")
					#print "received now:", received
					spd_list = received.split(',')
					print "spd_list", spd_list
					successful = True
					self.motor1_speed = int(spd_list[0])
					self.motor2_speed = int(spd_list[1])
					break
			except:
				pass
		if (successful == False):
				print "NOT successful: sending SP stats to motor arduino"

	def terminate(self):
		self.com.close()
		print "closing motor serial", self.com
		print self._should_stop.set()
		#self._read_thread.wait()
#############################################################

def validate_command(self, cmd):
		successful = False
		for n in range (5):
			time.sleep(0.05)
			#self.com.flushOutput()
			#print "sending to motor arduino:", cmd
			self.com.write (cmd)
			received = ""
			self.com.flushInput()
			#time.sleep(0.05)
			while (len(received) < 1):
				received = self.com.readline()
			print "received back from arduino:", received
			#print len(received)
			received = received.replace('\r\n', '')
			received = received.replace('m1:', '')
			received = received.replace('m', '')
			received = received.replace(':', '')
			print "stripped:", received, "  cmd:", cmd
			if (received == cmd):
				print "successful: sending to motor arduino"
				successful = True		 		
				break
		if (successful == False):
				print "NOT successful: sending to motor arduino"

def send_command(self, cmd):
	#successful = False
	received = ""
	for n in range (5):	
		self.com.flushOutput()
		self.com.flushInput()
		try:	
			received = self.com.readline()
		except SerialException as jj:
			print jj
		print "received back from arduino:", received
		received = received.replace("\r", "")
		received = received.replace("\n", "")
		if (received[0:3] == "m1:"): break
	if (len(received) > 0) and (received[0:3] == "m1:"):
		self.com.flushOutput()
		self.com.flushInput()
		print "sending command:", cmd
		self.com.write(cmd)
	else:
		try:
			print "closing port"
			#print self.com
			self.com.close()
			self.isConnected = False
			self.com = None
			print "reopening port"
			self.com = self.open_serial_port()			
		except:
			print "problem re-opening motor serial port"
			pass
		#except:
		#	print "motor driver problem"
		#	pass
		#try:
		#	received = ""
		#	self.com.flushInput()
		#	received = received + self.com.readline()
		#	print "received:", received
		#except:
		#	pass
		#time.sleep(5)

def list_serial_ports():
    # Windows
    if os.name == 'nt':
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append('COM'+str(i + 1))
                s.close()
            except serial.SerialException:
                pass
        return available
    else:
		# Mac / Linux
		ports_to_return = []
		for port in list_ports.comports():
			#print port[1]
			#[start:end:increment] 
			#print port[1][3:4:1]
			if port[1][3:4:1] == "A":ports_to_return.append(port)
		#print ports_to_return
		#raw_input ("press enter") 
		return ports_to_return

