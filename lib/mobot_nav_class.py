#!/usr/bin/python


import thread, time, sys, traceback
import serial
from math import *

class mobot_nav ():
	def __init__(self, lidar):
		self.lidar = lidar
	
	def angel_greatest_dist(self):
		min_dist_mm = 60
		greatest_dist_mm = 0
		#while True:
		for i in self.lidar.data:
			time.sleep(0.0001)
			angle = i[0]
			dist_mm = i[1]
			quality = i[2]	
			if dist_mm  > min_dist_mm and quality > 10:
				if dist_mm > greatest_dist_mm: 
						greatest_dist_mm = dist_mm 
						angle_to_return = angle
		return angle_to_return


	def turn_left_or_right(self):
		min_dist_mm = 60
		greatest_dist_mm = 0
		way_to_turn = "none"
		beam_width = 20
		left = 90
		right = 270
		for i in self.lidar.data:
			time.sleep(0.0001)
			angle = i[0]
			dist_mm = i[1]
			quality = i[2]	
			if dist_mm  > min_dist_mm and quality > 10:
				if (left-beam_width) <= angle <= (left+beam_width):
					if dist_mm > greatest_dist_mm: 
						greatest_dist_mm = dist_mm 
						way_to_turn = 'left'
				if (right-beam_width) <= angle <= (right+beam_width):
					if dist_mm > greatest_dist_mm: 
						greatest_dist_mm = dist_mm 
						way_to_turn = 'right'	
		print "greatest_dist_mm", greatest_dist_mm 
		return way_to_turn 
		
		
		
		
		
				
