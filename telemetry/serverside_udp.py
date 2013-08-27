import socket
import time
import thread
import datetime

class Heartbeat():
	def __init__(self, robot_IP, basestation_IP):
		#-------------connection variables
		self.SOCKET = None
		self.SOCKET2 = None
		self.UDP_IP="127.0.0.1"
		self.UDP_PORT=5005
		self.MESSAGE= "X" #str(time.time())
		self.ACTIVE = False
		#----------------------RUN
		self.run()

	def connect(self):
		self.SOCKET = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
		self.SOCKET2 = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
		#host= '0.0.0.0'
		self.SOCKET2.bind( (self.UDP_IP, self.UDP_PORT) )
		

	def run(self):
		self.connect()
		self.th = thread.start_new_thread(self.send_heartbeat, ())
		self.th2 = thread.start_new_thread(self.receive_heartbeat, ())
		
	def send_heartbeat(self):
		while True:	
			time.sleep(.499) # send 10 times per second
			#self.MESSAGE = str(time.time())
			#print "sending heartbeat", self.MESSAGE
			self.SOCKET.sendto( self.MESSAGE, (self.UDP_IP, self.UDP_PORT) )

	def receive_heartbeat(self):
		count = 0
		while True:
			now = time.time()
			count = count + 1
			print count
			data, addr = self.SOCKET2.recvfrom( 128 ) # buffer size is X bytes
			beat_time = (time.time()-now)
			#self.SOCKET2.flush()
			#print "received message:", data,  "   time:", beat_time 
			data = None
			if beat_time < 0.5:
				self.ACTIVE = True
			if beat_time > 0.5:
				self.ACTIVE = False
			#print "heartbeat Active:", self.ACTIVE

if __name__== "__main__":

	heartbeat = Heartbeat('localhost', 'localhost') # (robot_IP, basestation_IP)
	while True:
		time.sleep(1)
		print heartbeat.ACTIVE
