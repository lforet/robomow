#!/usr/bin/python

#sudo apt-get install gpsd gpsd-clients
#gpsd /dev/ttyUSB0 -b -n
#The gpsd server reads NMEA sentences from the gps unit and is accessed on port 2947. You can test if everything is working by running a pre-built gpsd client such as xgps.

#sudo easy_install geopy
from geopy import distance
import geopy
from geopy.distance import VincentyDistance
from math import *
import gps, os, time
#from future import division
from math import sin, cos, radians, sqrt, atan2, asin, sqrt, pi
from subprocess import call
from identify_device_on_ttyport import *
from threading import *
import random

rEarth = 6371.01 # Earth's average radius in km
epsilon = 0.000001 # threshold for floating-point equality


#             model             major (km)   minor (km)     flattening  
ELLIPSOIDS = {'WGS-84':        (6378.137,    6356.7523142,  1 / 298.257223563),  
              'GRS-80':        (6378.137,    6356.7523141,  1 / 298.257222101),  
              'Airy (1830)':   (6377.563396, 6356.256909,   1 / 299.3249646),  
              'Intl 1924':     (6378.388,    6356.911946,   1 / 297.0),  
              'Clarke (1880)': (6378.249145, 6356.51486955, 1 / 293.465),  
              'GRS-67':        (6378.1600,   6356.774719,   1 / 298.25),  
              } 
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
			#time.sleep(1)
						
		while True :
			avg_latitude = 0.0
			avg_longitude = 0.0
			avg_altitude = 0.0
			avg_satellites = 0
			avg_active_satellites = 0
			try:
				for n in range(len(all_gps_list)):
					for x in xrange(1, self.samples):
						os.system("clear")
						while ActiveSatelliteCount(gpss[n].satellites) < 4:
							print "Acquiring at least 6 GPS Satellites..."
							print 'Satellites (total of', len(gpss[n].satellites) , ' in view)'
							print "Number of acquired satellites: ", ActiveSatelliteCount(gpss[n].satellites)
							time.sleep(1)
							os.system("clear")
							gpss[n].next()
							gpss[n].stream()
						gpss[n].next()
						#test data	
						#gpss[n].fix.latitude = 53.32055555555556 + (random.random() * 0.00005)
						#gpss[n].fix.longitude =-1.7297222222222221 + (random.random() * 0.00005)
						
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
											
						avg_latitude =  (avg_latitude + gpss[n].fix.latitude)  
						avg_longitude = (avg_longitude + gpss[n].fix.longitude)
						#if (x > 0):
						#	print 'Avg latitude : ' , self.latitude / x
						#	print 'Avg longitude: ' , self.longitude / x
							#time.sleep(10)
						avg_active_satellites = (avg_active_satellites + ActiveSatelliteCount(gpss[n].satellites))				
						time.sleep(.2)
						
				#print "Averaging....", (x*len(all_gps_list))
				self.latitude = (avg_latitude / (x*len(all_gps_list)))
				self.longitude = (avg_longitude / (x*len(all_gps_list)))
				#print "total sats:", self.active_satellites
				self.active_satellites = ( avg_active_satellites / (x*len(all_gps_list)))
				#time.sleep(1)
			   	print 'Avg latitude : ' , self.latitude, "   ", abs(self.latitude - gpss[n].fix.latitude)
			   	print 'Avg longitude: ' , self.longitude, "    ", abs(self.longitude - gpss[n].fix.longitude) 				
				print 'Avg Active Satellites: ' , self.active_satellites
			
				print "Distance: ", round((lldistance((self.latitude, self.longitude), (gpss[n].fix.latitude, gpss[n].fix.longitude)) * 3.28084), 4), " feet"
				time.sleep(5)


			except:
				#time.sleep(1)
				pass
			#os.system("clear")

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
		time.sleep(4)
		#print returncode

def start_a_gps(gps_to_start):
	start_gps = "gpsd "+gps_to_start+" -S " + str(2947+n) + " -n -b"
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

def geopyDistance(lat1, lon1, lat2, lon2):
	x = distance.distance((lat1, lon1), (lat2,lon2)).meters	
	return x

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km 

def calcBearing(lat1, lon1, lat2, lon2):
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dLon = lon2 - lon1
	y = sin(dLon) * cos(lat2)
	x = cos(lat1) * sin(lat2) \
		- sin(lat1) * cos(lat2) * cos(dLon)
	return atan2(y, x)


#def vertical_angle():

def bearing2(lat1, lon1, lat2, lon2):
	startLat = math.radians(lat1)
	startLong = math.radians(lon1)
	endLat = math.radians(lat2)
	endLong = math.radians(lon2)

	dLong = endLong - startLong

	dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
	if abs(dLong) > math.pi:
		 if dLong > 0.0:
		     dLong = -(2.0 * math.pi - dLong)
		 else:
		     dLong = (2.0 * math.pi + dLong)

	bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;

	return bearing

def calculate_distance(lat1, lon1, lat2, lon2):
        '''
        * Calculates the distance between two points given their (lat, lon) co-ordinates.
        * It uses the Spherical Law Of Cosines (http://en.wikipedia.org/wiki/Spherical_law_of_cosines):
        *
        * cos(c) = cos(a) * cos(b) + sin(a) * sin(b) * cos(C)                        (1)
        *
        * In this case:
        * a = lat1 in radians, b = lat2 in radians, C = (lon2 - lon1) in radians
        * and because the latitude range is  [-pie/2, pie/2] instead of [0, pie]
        * and the longitude range is [-pie, pie] instead of [0, 2pie]
        * (1) transforms into:
        *
        * x = cos(c) = sin(a) * sin(b) + cos(a) * cos(b) * cos(C)
        *
        * Finally the distance is arccos(x)
        '''

        if ((lat1 == lat2) and (lon1 == lon2)):
            return 0

        try:
            delta = lon2 - lon1
            a = math.radians(lat1)
            b = math.radians(lat2)
            C = math.radians(delta)
            x = math.sin(a) * math.sin(b) + math.cos(a) * math.cos(b) * math.cos(C)
            distance = math.acos(x) # in radians
            distance  = math.degrees(distance) # in degrees
            distance  = distance * 60 # 60 nautical miles / lat degree
            distance = distance * 1852 # conversion to meters
            #distance  = round(distance)
            return distance;
        except:
            return 0


def deg2rad(angle):
    return angle*pi/180


def rad2deg(angle):
    return angle*180/pi


def pointRadialDistance(lat1, lon1, bearing, distance):
    """
    Return final coordinates (lat2,lon2) [in degrees] given initial coordinates
    (lat1,lon1) [in degrees] and a bearing [in degrees] and distance [in km]
    """
    rlat1 = deg2rad(lat1)
    rlon1 = deg2rad(lon1)
    rbearing = deg2rad(bearing)
    rdistance = distance / rEarth # normalize linear distance to radian angle

    rlat = asin( sin(rlat1) * cos(rdistance) + cos(rlat1) * sin(rdistance) * cos(rbearing) )

    if cos(rlat) == 0 or abs(cos(rlat)) < epsilon: # Endpoint a pole
        rlon=rlon1
    else:
        rlon = ( (rlon1 - asin( sin(rbearing)* sin(rdistance) / cos(rlat) ) + pi ) % (2*pi) ) - pi

    lat = rad2deg(rlat)
    lon = rad2deg(rlon)
    return (lat, lon)

def recalculate_coordinate(val,  _as=None):
  """
    Accepts a coordinate as a tuple (degree, minutes, seconds)
    You can give only one of them (e.g. only minutes as a floating point number) 
    and it will be duly recalculated into degrees, minutes and seconds.
    Return value can be specified as 'deg', 'min' or 'sec'; default return value is 
    a proper coordinate tuple.
This formula is only an approximation when applied to the Earth, because the Earth is not a perfect sphere: the Earth radius R varies from 6356.78 km at the poles to 6378.14 km at the equator. There are small corrections, typically on the order of 0.1% (assuming the geometric mean R = 6367.45 km is used everywhere, for example), because of this slight ellipticity  of the planet. A more accurate method, which takes into account the Earth's ellipticity, is given by Vincenty's formulae.
  """
  deg,  min,  sec = val
  # pass outstanding values from right to left
  min = (min or 0) + int(sec) / 60
  sec = sec % 60
  deg = (deg or 0) + int(min) / 60
  min = min % 60
  # pass decimal part from left to right
  dfrac,  dint = math.modf(deg)
  min = min + dfrac * 60
  deg = dint
  mfrac,  mint = math.modf(min)
  sec = sec + mfrac * 60
  min = mint
  if _as:
    sec = sec + min * 60 + deg * 3600
    if _as == 'sec': return sec
    if _as == 'min': return sec / 60
    if _as == 'deg': return sec / 3600
  return deg,  min,  sec
      

def points2distance(start,  end):
  """
    Calculate distance (in kilometers) between two points given as (long, latt) pairs
    based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
    Implementation inspired by JavaScript implementation from 
    http://www.movable-type.co.uk/scripts/latlong.html
    Accepts coordinates as tuples (deg, min, sec), but coordinates can be given 
    in any form - e.g. can specify only minutes:
    (0, 3133.9333, 0) 
    is interpreted as 
    (52.0, 13.0, 55.998000000008687)
    which, not accidentally, is the lattitude of Warsaw, Poland.
  """
  start_long = math.radians(recalculate_coordinate(start[0],  'deg'))
  start_latt = math.radians(recalculate_coordinate(start[1],  'deg'))
  end_long = math.radians(recalculate_coordinate(end[0],  'deg'))
  end_latt = math.radians(recalculate_coordinate(end[1],  'deg'))
  d_latt = end_latt - start_latt
  d_long = end_long - start_long
  a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
  c = 2 * math.atan2(math.sqrt(a),  math.sqrt(1-a))
  return rEarth * c

def meters_to_feet(meters):
	print "metters", meters
	return (meters*3.28084)

def destination_coordinates(lat1, lon1, bearing_in_degrees, distance_to_travel_in_meters):
# given: lat1, lon1,  bearing = bearing to travel in degrees, distance_to_travel = distance to travel in meters
	distance_to_travel_in_meters = float(distance_to_travel_in_meters) / 1000
	print distance_to_travel_in_meters
	origin = geopy.Point(lat1, lon1)
	destination = VincentyDistance(kilometers=distance_to_travel_in_meters).destination(origin, bearing_in_degrees)
	lat2, lon2 = destination.latitude, destination.longitude
	return lat2,lon2


def distance_and_bearings(lat1, lon1, lat2, lon2, start_altitude=0, dest_altitude=0):
	#GPS distance and bearing between two GPS points (Python recipe)
	#This code outputs the distance between 2 GPS points showing also the vertical and horizontal bearing between them. 
	#Haversine Formuala to find vertical angle and distance
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	#convert to meters
	#Base = Base * 1000 6367442.5
	Base = 6367442.5 * c # average earth radius in m
	Bearing = calcBearing(lat1, lon1, lat2, lon2)
	Bearing = round(degrees(Bearing), 2)
	distance = Base * 2 + dest_altitude * 2 / 2
	Caltitude = dest_altitude - start_altitude

	#Convertion from radians to decimals
	a = dest_altitude/Base
	b = atan(a)
	c = degrees(b)
	#Convert meters into Kilometers
	#distance = distance / 1000
	Base = round(Base,2)
	return Base, distance, c, Bearing

#Horisontal Bearing
def calcBearing(lat1, lon1, lat2, lon2):
    dLon = lon2 - lon1
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) \
        - sin(lat1) * cos(lat2) * cos(dLon)
    return atan2(y, x)

def get_dest_gps_cood(lat1, lon1, bearing, distance_in_meters):
	# given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
	#returns new lat long
	#lat1 = 53.32055555555556
	#lat2 = 53.31861111111111
	#lon1 = -1.7297222222222221
	#lon2 = -1.6997222222222223
	d = distance_in_meters / 1000.0
	b = bearing
	print d, b
	origin = geopy.Point(lat1, lon1)
	destination = VincentyDistance(kilometers=d).destination(origin, b)
	lat2, lon2 = destination.latitude, destination.longitude
	return lat2, lon2
