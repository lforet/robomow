#!/usr/bin/python


import thread, time, sys, traceback
import serial
from math import *
import pika 
import cPickle as pickle

class publish_lidar():
	def __init__(self, com_port, baudrate):
		self.init_level = 0
		self.angle = 0
		self.index = 0
		self.speed_rpm = 0
		# serial port
		self.com_port = com_port
		self.baudrate = baudrate
		self.ser = serial.Serial(self.com_port, self.baudrate)
		self.data = []
		self.offset = 140
		#-------------connection variables
		self.feed_num = 'lidar.1'
		self.connection = None
		self.channel = None
		#----------------------RUN
		self.run()


	def connect(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		#channel.queue_declare(queue='mobot_video1', auto_delete=True, arguments={'x-message-ttl':1000})
		self.channel.exchange_declare(exchange='mobot_data_feed',type='topic')	
	
	def publish(self, data):
			self.channel.basic_publish(exchange='mobot_data_feed', 
								routing_key=self.feed_num, body=data)
	
	def run(self):
		self.connect()
		self.th = thread.start_new_thread(self.read_lidar, ())
		
	def read_lidar(self):
		nb_errors = 0
		while True:
			temp_data = []
			while len(temp_data) < 360:	
				try:
					time.sleep(0.00001) # do not hog the processor power
					#print "self.init_level", self.init_level
					if self.init_level == 0 :
						b = ord(self.ser.read(1))
						# start byte
						if b == 0xFA : 
							self.init_level = 1
						else:
							self.init_level = 0
					elif self.init_level == 1:
						# position index 
						b = ord(self.ser.read(1))
						if b >= 0xA0 and b <= 0xF9  : 
							self.index = b - 0xA0
							self.init_level = 2
						elif b != 0xFA:
							self.init_level = 0
					elif self.init_level == 2 :
						# speed
						b_speed = [ ord(b) for b in self.ser.read(2)]

						# data
						b_data0 = [ ord(b) for b in self.ser.read(4)]
						b_data1 = [ ord(b) for b in self.ser.read(4)]
						b_data2 = [ ord(b) for b in self.ser.read(4)]
						b_data3 = [ ord(b) for b in self.ser.read(4)]

						# for the checksum, we need all the data of the packet...
						# this could be collected in a more elegent fashion... 
						all_data = [ 0xFA, self.index+0xA0 ] + b_speed + b_data0 + b_data1 + b_data2 + b_data3 
						
						# checksum  
						b_checksum = [ ord(b) for b in self.ser.read(2) ]
						incoming_checksum = int(b_checksum[0]) + (int(b_checksum[1]) << 8)

						# verify that the received checksum is equal to the one computed from the data
						if checksum(all_data) == incoming_checksum:
							#pass
							self.speed_rpm = int(compute_speed(b_speed))
							#gui_update_speed(speed_rpm)

							#motor_control(speed_rpm)
		
							temp_data.append(convert_data(self.index * 4 + 0, b_data0, self.offset))
							temp_data.append(convert_data(self.index * 4 + 1, b_data1, self.offset))
							temp_data.append(convert_data(self.index * 4 + 2, b_data2, self.offset))
							temp_data.append(convert_data(self.index * 4 + 3, b_data3, self.offset))
						else:
							# the checksum does not match, something went wrong...
							nb_errors +=1
							print "errors found.....error count:", nb_errors
							#label_errors.text = "errors: "+str(nb_errors)
		
							# display the samples in an error state
							#update_view(index * 4 + 0, [0, 0x80, 0, 0])
							#update_view(index * 4 + 1, [0, 0x80, 0, 0])
							#update_view(index * 4 + 2, [0, 0x80, 0, 0])
							#update_view(index * 4 + 3, [0, 0x80, 0, 0])
				            
						self.init_level = 0 # reset and wait for the next packet
				        
					else: # default, should never happen...
						self.init_level = 0
				except :
					traceback.print_exc(file=sys.stdout)
				#print temp_data, i
				#raw_input("enter")
			if len (temp_data ) == 360:
				self.data = sorted(temp_data)
				self.data.append(self.speed_rpm)
				pickled_data = pickle.dumps(self.data,-1)
				self.publish(pickled_data)
			
			
def checksum(data):
	"""Compute and return the checksum as an int.

	data -- list of 20 bytes (as ints), in the order they arrived in.
	"""
	# group the data by word, little-endian
	data_list = []
	for t in range(10):
	    data_list.append( data[2*t] + (data[2*t+1]<<8) )
	
	# compute the checksum on 32 bits
	chk32 = 0
	for d in data_list:
	    chk32 = (chk32 << 1) + d

	# return a value wrapped around on 15bits, and truncated to still fit into 15 bits
	checksum = (chk32 & 0x7FFF) + ( chk32 >> 15 ) # wrap around to fit into 15 bits
	checksum = checksum & 0x7FFF # truncate to 15 bits
	return int( checksum )
	
	
	
def convert_data(angle, data, offset):
    """Updates the view of a sample.

    Takes the angle (an int, from 0 to 359) and the list of four bytes of data in the order they arrived.
    """
    #unpack data using the denomination used during the discussions
    x = data[0]
    x1= data[1]
    x2= data[2]
    x3= data[3]
    
    angle_rad = angle * pi / 180.0
    c = cos(angle_rad)
    s = -sin(angle_rad)

    dist_mm = x | (( x1 & 0x3f) << 8) # distance is coded on 13 bits ? 14 bits ?
    quality = x2 | (x3 << 8) # quality is on 16 bits

    dist_x = dist_mm*c
    dist_y = dist_mm*s
    
    #print "angle:", angle, "   dist_mm:", dist_mm, "   quality:",  quality 
    return angle, dist_mm, quality
    

def compute_speed(data):
    speed_rpm = float( data[0] | (data[1] << 8) ) / 64.0
    return speed_rpm
    

if __name__== "__main__":

	lidar = publish_lidar("/dev/ttyUSB0", 115200)
	while True:
		time.sleep(0.00001)


