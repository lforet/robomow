

import random
import thread
import time 

class lidar_faker():
	def __init__(self):
		self.x_degree = 0
		self.y_degree = 0
		self.dist = 0
		self.quality = 0
		self.rpm = 0
		self.th = thread.start_new_thread(self.run, ())
	
	def run(self):
		while True:
			time.sleep(.05)
			self.read_lidar()
			
	def read_lidar(self):
		self.y_degree += 1
		if self.y_degree > 360:
			self.y_degree = 0
			self.x_degree += 1
			if self.x_degree > 360: self.x_degree = 0	
		self.dist = random.randint(0,4000)
		self.quality = random.randint(0,100)
		self.rpm = random.randint(281 ,295)
