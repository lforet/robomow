#!/usr/bin/python


import thread, time, sys
import pika 


class publish_heartbeat():
	def __init__(self):
		self.heartbeat_signal = "X"
		#-------------connection variables
		self.channel_name = 'heartbeat.1'
		self.connection = None
		self.channel = None
		#----------------------RUN
		self.run()


	def connect(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='mobot_data_feed',type='topic')	
	
	def publish(self, data):
			self.channel.basic_publish(exchange='mobot_data_feed', 
								routing_key=self.channel_name, body=data)
	
	def run(self):
		self.connect()
		self.th = thread.start_new_thread(self.send_heartbeat, ())
		
	def send_heartbeat(self):
		while True:	
			time.sleep(0.1) # send 10 times per second
			self.publish(self.heartbeat_signal)


if __name__== "__main__":

	heartbeat = publish_lidar():
	while True:
		time.sleep(0.00001)
