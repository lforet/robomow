#!/usr/bin/python

import pika
import thread, time, sys, traceback	


''' USAGE:


	wifi = consume_wifi('wifi.1', 'localhost')
	while True:
		time.sleep(1)
		print 'signal strength:', wifi.signal_strength

	self.signal_strength:
		int > -1 = the wifi ssid signal strength
		-1 = connected to queue but ssid not found
		-2 = no connecntion to msg queue


'''

class consume_wifi():
	def __init__(self, channel_name, host_ip):
		self.signal_strength = None
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
		result = self.channel.queue_declare(exclusive=True, auto_delete=True, arguments={'x-message-ttl':100})
		self.queue_name = result.method.queue
		binding_keys = self.channel_name
		self.channel.queue_bind(exchange='mobot_data_feed', queue=self.queue_name, routing_key=binding_keys)

		
	def read_signal_strength(self):	
		while True:		
			if  self.connection == None or self.connection.is_open == False:
					self.connect()
			time.sleep(0.11) # do not hog the processor power
			#print "-" * 50
			method_frame, properties, body = self.channel.basic_get(self.queue_name)
			if method_frame:
				# Display the message parts
				#print method_frame
				#print properties
				#print body
				self.signal_strength = body
				#print "self.signal_strength:", self.signal_strength
				self.channel.basic_ack(method_frame.delivery_tag)
			else:
				#print "no msgs read"
				time.sleep(1)
				self.signal_strength = -2

	def run(self):
		self.th = thread.start_new_thread(self.read_signal_strength, ())
	

if __name__== "__main__":

	wifi = consume_wifi('wifi.1', '192.168.1.180')
	while True:
		time.sleep(1)
		print 'signal strength:', wifi.signal_strength

