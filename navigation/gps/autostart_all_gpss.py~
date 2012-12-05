
#this function will find and start all gps devices connected to linux computer

from subprocess import call
from identify_device_on_ttyport import *
import time
from threading import *
import gps
import random
import os
from math import sin, cos, radians, sqrt, atan2, asin, sqrt, pi


class mobot_gps( Thread ):

	def __init__(self): 
		Thread.__init__( self )	
		self.latitude = 0.0
		self.longitude = 0.0
		self.altitude = 0.0
		self.satellites = 0
		self.active_satellites = 0
		self.samples = 10

	def __del__(self):
		del(self)
	
	def run(self):
		self.process()

	def process( self ):
		gpss = []
		#get list of all attached gps units
		all_gps_list = gps_list()
		print "Total # GPS Units Found:", len (all_gps_list)
		#start all gps units
		start_all_gps()
		#connect via python
		for n in range(len(all_gps_list)):
			port = str(2947+n)
			print "port", port
			gpss.append(gps.gps(host="localhost", port=port))
			print "starting_gps:", gpss[n]
			#returncode = call(start_gps, shell=True)
			time.sleep(1)	
			gpss[n].next()
			gpss[n].stream()
			#print 'Satellites (total of', len(gpss[n].satellites) , ' in view)'
			time.sleep(1)
						
		while True :
			self.latitude = 0.0
			self.longitude = 0.0
			self.altitude = 0.0
			self.satellites = 0
			self.active_satellites = 0
			try:
				for n in range(len(all_gps_list)):
					for x in xrange(1, self.samples):
						os.system("clear")
						while ActiveSatelliteCount(gpss[n].satellites) < 6:
							print "Acquiring at least 6 GPS Satellites..."
							print "Number of acquired satellites: ", ActiveSatelliteCount(gpss[n].satellites)
							time.sleep(1)
							#os.system("clear")
							gpss[n].next()
							gpss[n].stream()
						gpss[n].next()
					   	print "READING GPS:", n, "  ", x
					   	print "-------------"
					   	print 'latitude ' , gpss[n].fix.latitude
					   	print 'longitude ' , gpss[n].fix.longitude
					   	print 'time utc ' , gpss[n].utc, gpss[n].fix.time
					   	print 'altitude ' , gpss[n].fix.altitude
					   	print 'epx ', gpss[n].fix.epx
					   	print 'epv ', gpss[n].fix.epv
					   	print 'ept ', gpss[n].fix.ept
					   	print "speed ", gpss[n].fix.speed
					   	print "climb " , gpss[n].fix.climb
					   	#print
					   	print 'Satellites (total of', len(gpss[n].satellites) , ' in view)'
					   	for i in gpss[n].satellites:
						 	print '\t', i
					   	print "Active satellites used: ", ActiveSatelliteCount(gpss[n].satellites)
						self.latitude =  (self.latitude + gpss[n].fix.latitude)  
						self.longitude = (self.longitude + gpss[n].fix.longitude)
						if (x > 0):
							print 'Avg latitude : ' , self.latitude / x
							print 'Avg longitude: ' , self.longitude / x
							#time.sleep(10)
						self.active_satellites = (self.active_satellites + ActiveSatelliteCount(gpss[n].satellites))				
						time.sleep(.5)
						
				print "Averaging....", x+1
				self.latitude = (self.latitude / x)
				self.longitude = (self.longitude / x)
				print "total sats:", self.active_satellites
				self.active_satellites = ( self.active_satellites / x)
				time.sleep(1)
			   	print 'Avg latitude : ' , self.latitude, "   ", abs(self.latitude - gpss[n].fix.latitude)
			   	print 'Avg longitude: ' , self.longitude, "    ", abs(self.longitude - gpss[n].fix.longitude) 				
				print 'Avg Active Satellites: ' , self.active_satellites
			
				print "Distance: ", round((lldistance((self.latitude, self.longitude), (gpss[n].fix.latitude, gpss[n].fix.longitude)) * 3.28084), 4), " feet"
				time.sleep(8)


			except:
				#time.sleep(1)
				pass
			os.system("clear")

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
	print "gps_list:", all_gps_list
	print len(all_gps_list)
	for n in range(len(all_gps_list)):
		start_gps = "gpsd "+all_gps_list[n]+" -S " + str(2947+n) + " -n -b"
		print "start_gps:", start_gps
		returncode = call(start_gps, shell=True)
		time.sleep(2)
		#print returncode

def start_a_gps(gps_to_start):
	start_gps = "gpsd "+gps_to_start+" -S " + str(2947+n) + "-n -b"
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


def lldistance(a, b):
   """
   Calculates the distance between two GPS points (decimal)
   @param a: 2-tuple of point A
   @param b: 2-tuple of point B
   @return: distance in m
   """
   r = 6367442.5             # average earth radius in m
   dLat = radians(a[0]-b[0])
   dLon = radians(a[1]-b[1])
   x = sin(dLat/2) ** 2 + \
       cos(radians(a[0])) * cos(radians(b[0])) *\
       sin(dLon/2) ** 2
   #original# y = 2 * atan2(sqrt(x), sqrt(1-x))
   y = 2 * asin(sqrt(x))
   d = r * y

   return d

if __name__ == "__main__":
	#print "startup all gps"
	#start_all_gps()
	#gpslist = gps_list()
	#print gpslist
	gps2 = mobot_gps()
	gps2.daemon=True
	gps2.start()
	gps2.join()
	'''
	print gps2._gps
	while 1:
		print gps2._gps
		print "# of GPS Units:", len(gpslist)
		if (gps2.satellites > 0):
			print 'Satellites (total of', len(gps2.satellites) , ' in view)'
			print "Active satellites used:", gps2.active_satellites
			for i in gps2.satellites:
				print '\t', i
			print "lat: ", gps2.lat
			print "long:", gps2.long
		time.sleep(random.randint(1, 3))	
		os.system("clear")
	'''	
