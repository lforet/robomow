
#this function will find and start all gps devices connected to linux computer

from subprocess import call
from identify_device_on_ttyport import *
import time
from threading import *
import gps
import random
import os



class mobot_gps( Thread ):

	def __init__(self, port): 
		Thread.__init__( self )	
		#self.gps = gps_to_start
		self.port = port
		self._gps = None
		self.satellites = 0
		self.active_satellites = 0
		self.lat = 0.0
		self.long = 0.0
		print self.port

	#def __del__(self):
	#	del(self)
	
	def run(self):
		self.process()

	def process( self ):
		print "startup"
		print self.port
		self._gps = gps.gps(host="localhost", port=self.port)
		print self._gps
		print "hi"
		self._gps.next()
		self._gps.stream()
		while True:
			try:
				self._gps.next()
				self._gps.stream()
				self.satellites = self._gps.satellites
				self.active_satellites = ActiveSatelliteCount(self._gps.satellites)
				self.lat = self._gps.fix.latitude
				self.long = self._gps.fix.longitude
				time.sleep(1)
			except:
				pass


def ActiveSatelliteCount(session):
   count = 0
   for i in range(len(session)):
      s = str(session[i])
      if s[-1] == "y":
			count = count + 1
   return count


def start_all_gps():

	all_gps_list = gps_list()

	#gps_list = ["/dev/ttyUSB0", "/dev/ttyUSB1"]
	#print "gps_list:", gps_list
	#print len(gps_list)
	for n in range(len(all_gps_list)):
		start_gps = "gpsd "+all_gps_list[0]+" -S " + str(2947+n)
		print "start_gps:", start_gps
		returncode = call(start_gps, shell=True)
		time.sleep(2)
		#print returncode

def start_a_gps(gps_to_start):
	start_gps = "gpsd "+gps_to_start+" -S " + str(2947+n)
	print "start_gps:", start_gps
	returncode = call(start_gps, shell=True)
	time.sleep(2)
	#print returncode


def gps_list():
	gps_list = find_usb_tty("067b","2303")
	return gps_list

def decdeg2dms(dd):
   mnt,sec = divmod(dd*3600,60)
   deg,mnt = divmod(mnt,60)
   return deg,mnt,sec

if __name__ == "__main__":
	gpslist = gps_list()
	print gpslist
	gps2 = mobot_gps("2947")
	#gps2.daemon=True
	gps2.start()
	print gps2._gps
	while 1:
		if (gps2.satellites > 0):
			print 'Satellites (total of', len(gps2.satellites) , ' in view)'
			print "Active satellites used:", gps2.active_satellites
			for i in gps2.satellites:
				print '\t', i
			print "lat: ", gps2.lat
			print "long:", gps2.long
		time.sleep(random.randint(1, 3))	
		os.system("clear")	
