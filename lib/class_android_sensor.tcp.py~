from threading import Thread
import time
import sys 
import socket
import math

def read_line(s):
    ret = ''

    while True:
        c = s.recv(1)

        if c == '\n' or c == '':
            break
        else:
            ret += c

    return ret
    

class android_sensor_tcp(Thread):
	def __init__(self, port):
		self.host = ''  
		self.port = port  # Arbitrary non-privileged port
		self.socket = None   
		self.light = None
		self.accuracy = None
		self.xforce = None
		self.yforce = None
		self.zforce = None
		self.xMag = None
		self.yMag = None
		self.zMag = None
		self.pitch = None
		self.roll= None
		self.azimuth = None
		self.heading = None	
		Thread.__init__(self)
			
	def run(self):
		while True:
			try:
				self.close_com()
			except:	
				pass
			try:
				print "waiting to accept.."
				conn, addr = self.open_com()
				print "accepted connection from client.."
				while conn <> "":
					self.socket.listen(1)
					for i in range(5):
						data = read_line(conn)
						if len(data) > 0: break
					data1 = data.split(',')
					#print data1
					if len(data) > 1:
						try:
							self.light = float(data1[1])
							self.accuracy = float(data1[2])
							self.xforce = float(data1[3])
							self.yforce = float(data1[4])
							self.zforce = float(data1[5])
							self.xMag = float(data1[6])
							self.yMag = float(data1[7])
							self.zMag = float(data1[8])
							self.pitch = float(data1[9])
							self.roll = float(data1[10])
							self.azimuth = float(data1[11])
							self.heading = math.degrees(self.azimuth)
							if self.heading < 0: self.heading = self.heading + 360
							self.heading = round(self.heading, 2)
							#print "heading:", self.heading
						except:
							pass
					else:
						self.light = None
						self.accuracy = None
						self.xforce = None
						self.yforce = None
						self.zforce = None
						self.xMag = None
						self.yMag = None
						self.zMag = None
						self.pitch = None
						self.roll= None
						self.azimuth = None
						self.heading = None	
						conn = ""	
						time.sleep(.5)	
				time.sleep(1) 
			except IOError as detail:
				print "connection lost", detail



	def open_com(self):
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.bind((self.host, self.port))
			#print "listening..."
			self.socket.listen(1)
			try:
				print "waiting to accept.."
				conn, addr = self.socket.accept()
				return conn, addr	
			except IOError as detail:
				print "connection lost", detail

	def close_com(self):
		try:
			print "closing Socket"
			self.socket.close()
		except NameError as detail:
			print "No socket to close", detail


if __name__== "__main__":

	android_sensor = android_sensor_tcp(8095)
	android_sensor.daemon=True
	android_sensor.start()
	while True:
		while android_sensor.heading == None:
			time.sleep(.1)
		print android_sensor.heading
		#time.sleep(.1)
	del android_sensor

