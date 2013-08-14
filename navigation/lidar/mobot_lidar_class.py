#!/usr/bin/python

from threading import *
import os
import time
import serial
import math
import sys

class mobot_lidar (Thread):

	def __init__(self): 
		Thread.__init__( self )	
		self._isConnected = False
		self.visualization = False
		self.ser = self._open_serial_port()
		self.offset = 140
		self.init_level = 0 
		self.index = 0
		self.lidarData = [[] for i in range(360)] #A list of 360 elements Angle, Distance , quality
		#print self.lidarData

	def __del__(self):
		del(self)
	
	def run(self):
		print "hi:"
		self.read_Lidar()
        
	def _open_serial_port(self):
		while self._isConnected == False:
			print "class mobot_lidar: searching serial ports for lidar sensor package..."
			for i in range(1):
					port = "/dev/ttyUSB"
					port = port[0:11] + str(i)
					print "class mobot_lidar: searching on port:", port
					time.sleep(.2)
					try:				
						ser = serial.Serial(port, 115200, timeout=1)
						data = ser.readline()
						#print "data=", int(data[3:(len(data)-1)])
						if len(data) > 0:
							#ser.write("a\n")      # write a string
							print "class mobot_lidar: found lidar sensor package on serial port: ", port
							self._isConnected  = True
							#self._port = ser
							time.sleep(.35)
							break
					except:
						pass
			if self._isConnected == False:
				print "class mobot_lidar: lidar sensor package not found!"
				time.sleep(1)
			#print "returning", ser
		return ser
			
	def read_Lidar(self):
		nb_errors = 0
		while True:
			#try:
			time.sleep(0.00001) # do not hog the processor power
			if self.init_level == 0 :
				b = ord(self.ser.read(1))
				# start byte
				if b == 0xFA :
					self.init_level = 1
					#print lidarData
				else:
					self.init_level = 0
			elif self.init_level == 1:
				# position index
				b = ord(self.ser.read(1))
				if b >= 0xA0 and b <= 0xF9 :
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
					#if visualization:
					gui_update_speed(speed_rpm)
	                
					update_view(index * 4 + 0, b_data0)
					update_view(index * 4 + 1, b_data1)
					update_view(index * 4 + 2, b_data2)
					update_view(index * 4 + 3, b_data3)
				else:
				# the checksum does not match, something went wrong...
					nb_errors +=1
					#if visualization:
					#label_errors.text = "errors: "+str(nb_errors)
                
					# display the samples in an error state
					update_view(index * 4 + 0, [0, 0x80, 0, 0])
					update_view(index * 4 + 1, [0, 0x80, 0, 0])
					update_view(index * 4 + 2, [0, 0x80, 0, 0])
					update_view(index * 4 + 3, [0, 0x80, 0, 0])
	                
				self.init_level = 0 # reset and wait for the next packet

	            
			else: # default, should never happen...
				self.init_level = 0
			#except :
			#	traceback.print_exc(file=sys.stdout)




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

def gui_update_speed(speed_rpm):
    label_speed.text = "RPM : " + str(speed_rpm)

def compute_speed(data):
    speed_rpm = float( data[0] | (data[1] << 8) ) / 64.0
    return speed_rpm

def update_view( self, angle, data ):
    """Updates the view of a sample.

Takes the angle (an int, from 0 to 359) and the list of four bytes of data in the order they arrived.
"""
    #global offset, use_outer_line, use_line
    	
    #unpack data using the denomination used during the discussions
    x = data[0]
    x1= data[1]
    x2= data[2]
    x3= data[3]
    
    angle_rad = angle * math.pi / 180.0
    c = math.cos(angle_rad)
    s = -math.sin(angle_rad)

    dist_mm = x | (( x1 & 0x3f) << 8) # distance is coded on 13 bits ? 14 bits ?
    quality = x2 | (x3 << 8) # quality is on 16 bits
    self.lidarData[angle] = [dist_mm,quality]
    dist_x = dist_mm*c
    dist_y = dist_mm*s
    if visualization:
        #reset the point display
        point.pos[angle] = vector( 0, 0, 0 )
        pointb.pos[angle] = vector( 0, 0, 0 )
        point2.pos[angle] = vector( 0, 0, 0 )
        point2b.pos[angle] = vector( 0, 0, 0 )
        if not use_lines : lines[angle].pos[1]=(offset*c,0,offset*s)
        if not use_outer_line :
            outer_line.pos[angle]=(offset*c,0,offset*s)
            outer_line.color[angle] = (0.1, 0.1, 0.2)
        
        
        # display the sample
        if x1 & 0x80: # is the flag for "bad data" set?
            # yes it's bad data
            lines[angle].pos[1]=(offset*c,0,offset*s)
            outer_line.pos[angle]=(offset*c,0,offset*s)
            outer_line.color[angle] = (0.1, 0.1, 0.2)
        else:
            # no, it's cool
            if not x1 & 0x40:
                # X+1:6 not set : quality is OK
                if use_points : point.pos[angle] = vector( dist_x,0, dist_y)
                if use_intensity : point2.pos[angle] = vector( (quality + offset)*c,0, (quality + offset)*s)
                if use_lines : lines[angle].color[1] = (1,0,0)
                if use_outer_line : outer_line.color[angle] = (1,0,0)
            else:
                # X+1:6 set : Warning, the quality is not as good as expected
                if use_points : pointb.pos[angle] = vector( dist_x,0, dist_y)
                if use_intensity : point2b.pos[angle] = vector( (quality + offset)*c,0, (quality + offset)*s)
                if use_lines : lines[angle].color[1] = (0.4,0,0)
                if use_outer_line : outer_line.color[angle] = (0.4,0,0)
            if use_lines : lines[angle].pos[1]=( dist_x, 0, dist_y)
            if use_outer_line : outer_line.pos[angle]=( dist_x, 0, dist_y)




