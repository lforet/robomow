#!/usr/bin/python

from PIL import Image, ImageTk
import time
from datetime import datetime
import socket 
import cv2
import cv
from threading import *
import sys
from maxsonar_class import *
import random
from robomow_motor_class_arduino import *
from gps_functions import *
from math import *
import easygui as eg
import sonar_functions as sf
from img_processing_tools import *

def snap_shot(filename):
	#capture from camera at location 0
	now = time.time()
	global webcam1
	try:
		#have to capture a few frames as it buffers a few frames..
		for i in range (5):
			ret, img = webcam1.read()		 
		#print "time to capture 5 frames:", (time.time()) - now
		cv2.imwrite(filename, img)
		img1 = Image.open(filename)
		img1.thumbnail((320,240))
		img1.save(filename)
		#print (time.time()) - now
	except:
		print "could not grab webcam"
	return 

def send_file(host, cport, mport, filetosend):
	#global file_lock
	file_lock = True
	#print "file_lock", file_lock
	try:       
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((host, cport))
		cs.send("SEND " + filetosend)
		print "sending file", filetosend
		cs.close()
	except:
		#print "cs failed"
		pass
	time.sleep(0.1)
	try:
		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ms.connect((host, mport))
		f = open(filetosend, "rb")
		data = f.read()
		f.close()
		ms.send(data)
		ms.close()
	except:
		#print "ms failed"
		pass
	#file_lock = False
	#print "file_lock", file_lock
		
		
'''
def send_data(host="u1204vm.local", cport=9091, mport=9090, datatosend=""):
	try:       
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((host, cport))
		cs.send("SEND " + filetosend)
		cs.close()
	except:
		pass
	time.sleep(0.05)
	try:
		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ms.connect((host, mport))
		f = open(filetosend, "rb")
		data = f.read()
		f.close()
		ms.send(data)
		ms.close()
	except:
		pass
'''	
class send_video(Thread):
	def __init__(self, filetosend):   
		self.filetosend = filetosend     
		Thread.__init__(self)

	def run(self):
			#global file_lock, hhh
			print self.filetosend
			while True:
				snap_shot(self.filetosend)	
				send_file(host="u1204vm.local", cport=9090, mport=9091,filetosend=self.filetosend)
				time.sleep(.01)
							
class send_sonar_data(Thread):
	def __init__(self, filetosend):   
		self.filetosend = filetosend
		self.sonar_data = "" 
		self.max_dist = -1
		self.min_dist = -1   
		self.min_sensor = -1
		self.max_sensor = -1 
		self.right_sensor = -1
		self.left_sensor = -1
		self.forwardl_sensor = -1
		self.fowardr_sensor = -1
		Thread.__init__(self)

	def run(self):
			#global file_lock, hhh
			sonar = MaxSonar()
			while True:
				self.sonar_data = ""
				self.max_dist = -1
				self.min_dist = -1 
				self.min_sensor = -1
				self.max_sensor = -1
				self.right_sensor = -1
				self.left_sensor = -1
				self.forwardl_sensor = -1
				self.fowardr_sensor = -1
				#
				#below 2 lines are for test purposes when actual US arent sending data
				#for i in range(1,6):
				#	sonar_data = sonar_data + "s"+str(i)+":"+ str(random.randint(28, 91))

				data = str(sonar.distances_cm())
				self.sonar_data = []
				sonar_data_str1 = ""
				try:
					if len(data) > 1:
						self.sonar_data.append(int(data[(data.find('s1:')+3):(data.find('s2:'))]))
						self.sonar_data.append(int(data[(data.find('s2:')+3):(data.find('s3:'))]))
						self.sonar_data.append(int(data[(data.find('s3:')+3):(data.find('s4:'))]))
						self.sonar_data.append(int(data[(data.find('s4:')+3):(data.find('s5:'))]))
						#self.sonar_data.append(int(data[(data.find('s5:')+3):(len(data)-1)]))
						self.max_dist = max(self.sonar_data)
						self.min_dist = min(self.sonar_data)
						self.min_sensor = self.sonar_data.index(self.min_dist)
						self.max_sensor = self.sonar_data.index(self.max_dist)
						#sonar_data_str1 = "".join(str(x) for x in self.sonar_data)
						self.frontl_sensor = self.sonar_data[0]
						self.frontr_sensor = self.sonar_data[1]
						self.right_sensor = self.sonar_data[2]
						self.left_sensor = self.sonar_data[3]

						#print sonar_data_str1
						#print data
						#
						#f = open("sonar_data.txt", "w")
						#f.write(data)
						#f.close()
						#send_file(host="u1204vm.local", cport=9092, mport=9093,filetosend=self.filetosend)
				except:
					pass
				try:
					time.sleep(.02)
				except:
					pass
			print "out of while in sonar"


def move_mobot(motor, themove, speed):
	print "moving:", themove, "  speed:", speed
	if (themove == "f"):
		motor.forward(speed)
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed
	if (themove == "b"):
		motor.reverse(speed)
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed
	if (themove == "l"):
		motor.left(speed)
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed
	if (themove == "r"):
		motor.right(speed)
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed
	if (themove == "s"):
		motor.stop()
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed


def enable_video():
	video1 = send_video("snap_shot.jpg")
	video1.daemon=True
	video1.start()
	#video1.join()
	
def enable_sonar():
	sonar = send_sonar_data("sonar_data.txt")
	sonar.daemon=True
	sonar.start()
	#sonar.join()


def test_gps():
	#print "startup all gps"
	#start_all_gps()
	gpslist = gps_list()
	#print gpslist
	gps2 = mobot_gps()
	gps2.daemon=True
	gps2.start()
	#gps2.join()
	while 1:
		print "# of GPS Units:", len(gpslist)
		if (gps2.satellites > 0):
			print 'Satellites (total of', len(gps2.satellites) , ' in view)'
			print "Active satellites used:", gps2.active_satellites
			for i in gps2.satellites:
				print '\t', i
		print "lat: ", gps2.latitude
		print "long:", gps2.longitude
		time.sleep(random.randint(1, 3))	
		#os.system("clear")



class display_sonar(Thread):
	def __init__(self, sonar):
		self.sonar = sonar  
		Thread.__init__(self)

class mobot_display(Thread):
	def __init__(self, camID, sonar):
		self.camID = camID 
		self.sonar = sonar   
		Thread.__init__(self)

	def run(self):
		cv2.namedWindow('Sonar Data', cv.CV_WINDOW_AUTOSIZE)
		cv2.namedWindow('Front Camera', cv.CV_WINDOW_AUTOSIZE)
		cv.MoveWindow('Front Camera', 373, 24)
		camera =  cv.CreateCameraCapture(self.camID)
		while True:
			#time.sleep(1)
			try:
				#print "raw sonar data", self.sonar.sonar_data
				sonar_img = sf.sonar_graph(self.sonar.sonar_data)
				cv.ShowImage('Sonar Data', PILtoCV(sonar_img, 4))
				cv.WaitKey(40)
				frame = cv.QueryFrame(camera)
				frame = resize_img(frame, 0.60)
				cv.ShowImage('Front Camera', frame)
				cv.WaitKey(40)
			except:
				print "display failure"
				pass

class sonar_prevent_hit(Thread):
	def __init__(self, motor, sonar, threshold):
		self.sonar = sonar  
		self.motor = motor
		self.threshold = threshold
		Thread.__init__(self)

	def run(self):
		while True:
			#time.sleep(.12)
			try:
				#print "self.sonar.min_dist:", self.sonar.min_dist
				if (self.sonar.min_dist < self.threshold):
					print "auto hit prevent activated: " ,self.sonar.sonar_data
					time.sleep(1)
				evasive_maneuver(self.motor, self.sonar, self.threshold)
			except:
				print "sonar auto hit prevent failure"
				pass

def evasive_maneuver(motor, sonar, threshold):
	#wait to confirm 
	move_mobot(motor, 's', 0)
	time.sleep(.5)
	while (sonar.min_dist < threshold ):
		print "..........evasive maneuver............."
		print "sonar_data: ", sonar.sonar_data
		move_mobot(motor, 's', 0)
		time.sleep(.5)
		move_mobot(motor, 'b', 28)
		time.sleep(1)
		move_mobot(motor, 's', 0)
		time.sleep(.5)
		if (sonar.right_sensor > sonar.left_sensor):
			motor.spin_right(25)
			time.sleep(random.randint(100, 250)/100)	
		else:
			motor.spin_left(25)
			time.sleep(random.randint(100, 250)/100)
		#move_mobot(motor, 'f', 25)
		#time.sleep(.2)


def auto_move(motor, sonar, threshold):

	print "..........autopilot............."
	print "sonar_data: ", sonar.sonar_data
	now =  datetime.now()
	while  (sonar.min_dist < threshold):
		evasive_maneuver(motor, sonar, threshold)
	#time.sleep(.5)
	#if (sonar.min_dist > threshold):
		#move_mobot(motor, 'f', 20)
	#print "sonar_data: ", sonar.sonar_data
	#print "loop time:",  datetime.now() - now


def wallfollow(motor, sonar, threshold):
	rm_spd = 16
	lm_spd = 16

	spd = 14
	while True:
		print "..........wallfollow............."
		print "sonar_data: ", sonar.sonar_data
		print "sonar_right:", sonar.right_sensor, "   sonar_left:", sonar.left_sensor,
		print "RMotor: ", rm_spd, "  LMotor: ", lm_spd
		while (sonar.min_dist < threshold):
			rm_spd = spd
			lm_spd = spd
			evasive_maneuver(motor, sonar, threshold)
		else:
			if sonar.right_sensor < 56:
					lm_spd = spd - 4 #decrease left motor speed
					rm_spd = spd + 1 
			if sonar.right_sensor > 57:
					lm_spd = spd + 2 #increase left motor speed
					rm_spd = spd
					#rm_spd = rm_spd -1
			#if sonar.right_sensor  > 48 and sonar.right_sensor < 52:
			#		rm_spd = spd
			#		lm_spd = spd

		#adjust for max/min
		if lm_spd > 28: lm_spd = 28
		if rm_spd > 28: rm_spd = 28
		if lm_spd < 6: lm_spd = 6
		if rm_spd < 6: rm_spd = 6

		#send cmds to motors
		motor.right(rm_spd)
		motor.left(lm_spd)
		time.sleep(.03)
		#move_mobot(motor, 's', 0)
		

if __name__== "__main__":
	testmode = False
	if len(sys.argv) > 1:
		if sys.argv[1] == 'testmode':
				print 'starting in testing mode'
				testmode= True

	sonar = None
	motor = None
	reply =""
	movetime = 0.25
	while sonar == None or motor == None:
		if sonar == None: # or len(sonar.sonar_data) < 1:
			sonar = send_sonar_data("sonar_data.txt")
			sonar.daemon=True
			sonar.start()
		if motor == None:
			motor = robomow_motor()
			print "motor.isConnected:", motor.isConnected
		time.sleep(2)

	#wallfollow(motor, sonar)

	#start front navigation cam
	mobot_disp = mobot_display(0, sonar)
	mobot_disp.daemon=True
	mobot_disp.start()
	time.sleep(2)

	#start sonar_hit_preventer
	#sonar_hit_preventer = sonar_prevent_hit(motor, sonar, 38)
	#sonar_hit_preventer.daemon=True
	#sonar_hit_preventer.start()
	#sonar_hit_preventer.join()
	#time.sleep(2)

	while True:
		auto_move(motor, sonar, 38)
		time.sleep(.03)
	#wallfollow(motor, sonar, 40)



'''
	eg.rootWindowPosition = "+60+375"
	while True:
		
		if reply == 'AutoPilot':
			auto_move(sonar, motor)
	
		if reply == 'F':
			move_mobot(motor, 'f', 25)
			#time.sleep(movetime)
		if reply == 'B':
			move_mobot(motor, 'b', 25)
			#time.sleep(movetime)
		if reply == 'R':
			move_mobot(motor, 'r', 25)
			time.sleep(movetime)
			move_mobot(motor, 's', 0)
		if reply == 'L':
			move_mobot(motor, 'l', 25)
			time.sleep(movetime)
			move_mobot(motor, 's', 0)
		if reply == 'STOP':
			move_mobot(motor, 's', 0)
		if reply == "Quit":
			print "stopping mobot..."
			move_mobot(motor, 's', 0)
			time.sleep(movetime)
			print "Quitting...."
			sys.exit(-1)
		reply =	eg.buttonbox(title='Mobot Drive', choices=('AutoPilot', 'F', 'B', 'L', 'R', 'STOP', 'Quit'), root=None)



#############################################################
#start gps
#get current gps postiion
#get bearing to target position 
# turn toward target bearing
######################################################
gps1 = gps.gps(host="localhost", port="2947")
gps2 = gps.gps(host="localhost", port="2948")
gps3 = gps.gps(host="localhost", port="2949")
gps4 = gps.gps(host="localhost", port="2950")

'''

