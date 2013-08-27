#!/usr/bin/python

import pika
import thread, time, sys, traceback
import cPickle as pickle	
import cv, cv2


''' USAGE:

	lidar = consume_lidar('video.1', 'localhost')
	while True:
		time.sleep(1)
		print lidar.data[1]
		print 'rpm speed:', lidar.speed_rpm
'''

class consume_video():
	def __init__(self, channel_name, host_ip):
		self.frame = None
		#-------------connection variables
		self.channel_name = channel_name
		self.host_ip = host_ip
		self.queue_name =  None
		self.connection = None
		self.channel = None
		#----------------------RUN
		self.run()
	
	def connect(self):
		self.connection =  pika.BlockingConnection(pika.ConnectionParameters(host=self.host_ip))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='mobot_data_feed',type='topic')	
		result = self.channel.queue_declare(exclusive=True)
		self.queue_name = result.method.queue
		binding_keys = self.channel_name
		self.channel.queue_bind(exchange='mobot_data_feed', queue=self.queue_name, routing_key=self.channel_name)

		
	def grab_frames(self):	
		while True:
			time.sleep(0.0001) # do not hog the processor power
			self.connect()
			for method_frame, properties, body in self.channel.consume(self.queue_name):
				self.frame = pickle.loads(body)	
				# Acknowledge the message
				self.channel.basic_ack(method_frame.delivery_tag)
			
						
	def run(self):
		self.th = thread.start_new_thread(self.grab_frames, ())
	

if __name__== "__main__":
	cv2.namedWindow('Video', cv.CV_WINDOW_AUTOSIZE)
	camera = consume_video('video.0', 'localhost')
	while True:
		time.sleep(0.1)
		try:
			print "receiving video feed data: ", len(camera.frame)
			cv2.imshow('Video', camera.frame)
			cv.WaitKey(10)
		except:
			print "no video feed"
			pass


                   

