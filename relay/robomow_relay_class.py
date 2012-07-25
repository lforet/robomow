#!/usr/bin/env python

import serial
import time
from struct import *


def log(*msgline):
	for msg in msgline:
		print msg,
	print


class robomow_relay(object):
	def __init__(self,com_port="/dev/ttyUSB0"): 
		############################
		# lets introduce and init the main variables
		self.com = None
		self.isInitialized = False 

		self.commands = {
			'relay_1_on': 0x65,
			'relay_1_off': 0x6F,
			'relay_2_on': 0x66,
			'relay_2_off': 0x70,
			'info': 0x5A,
			'relay_states': 0x5B,
		}    
		###########################
		# lets connect the TTL Port
		try:
			self.com = serial.Serial(com_port, 9600, timeout=1)
			self.com.close()
			self.com.open()
			self.isInitialized = True
			self.relay1_state = 0
			self.relay2_state = 0
			log ("Link to relay driver -", com_port, "- successful")
			#log (self.com.portstr, self.com.baudrate,self.com.bytesize,self.com.parity,self.com.stopbits)

		except serial.serialutil.SerialException, e:
			print e
			log("Link to relay driver -", com_port, "- failed")

			
	def __del__(self):
		del(self)

	def stats(self):
		return (self.com.portstr, self.com.baudrate,self.com.bytesize,self.com.parity,self.com.stopbits)


	def send_command(self, cmd, read_response = False):
		#ser = serial.Serial('/dev/ttyACM0', 9600)
		#print "command", cmd
		self.com.write(chr(cmd)+'\n')
		#print "raw:", self.com.read()
		response = read_response and self.com.read() or None
		#print "response", response
		#self.com.close()
		return response

	def click_relay_1(self):
		print "indside clicking"
		self.send_command(self.commands['relay_1_on'])
		time.sleep(1)
		self.send_command(self.commands['relay_1_off'])

	def turn_relay_1_on(self):
		self.send_command(self.commands['relay_1_on'])

	def turn_relay_1_off(self):
		self.send_command(self.commands['relay_1_off'])

	def turn_relay_2_on(self):
		self.send_command(self.commands['relay_2_on'])

	def turn_relay_2_off(self):
		self.send_command(self.commands['relay_2_off'])

	def get_relay_states(self):
		states = self.send_command(self.commands['relay_states'], read_response=True)
		response = unpack('b',states)[0]
		states = {
				0: {'1': False, '2': False},
				1: {'1': True, '2': False},
				2: {'1': False, '2': True},
				3: {'1': True, '2': True},
		}
		if response == 0:
			self.relay1_state = 0
			self.relay2_state = 0
		if response == 1:
			self.relay1_state = 1
			self.relay2_state = 0
		if response == 2:
			self.relay1_state = 0
			self.relay2_state = 1
		if response == 3:
			self.relay1_state = 1
			self.relay2_state = 1
		return states[response]

