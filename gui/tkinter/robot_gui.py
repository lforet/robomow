import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from datetime import datetime
#from ThreadedBeatServer import *
import socket 
import os, random
import cv2
from maxsonar_class import *
from threading import *
import sys

sock = None
conn = None
basestation = None
cap = cv2.VideoCapture(0)

def com_loop(ip, port):
	global sock, conn, basestation
	#print "sock, conn", sock, conn
	if conn == None:	
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "binding: ", ip, " on port....", port
			sock.bind((ip, port))
			conn = None
			print "listening..."
			sock.listen(1)
			sock.settimeout(1)
			print "waiting to accept.."
			conn, basestation = sock.accept()
			print "accepted connection from client..", conn, basestation
			return 'com with basestation established'
		except IOError as detail:
			print detail
			conn = None
			#time.sleep(.1)
			return False
	else:
		try:
			if conn != None:
				data = conn.recv(1024)
				#if not data: break
				#print 'Received from remote: ', data
				#time.sleep(.1)	
				if len(data) > 0:
					#print "communication to basestation: ACTIVE"		
					#time.sleep(.5)
					return data
				else:
					#print "communication to basestation: NOT ACTIVE"
					conn = None
					#time.sleep(.1)
					return False
		except socket.error, e:
			#print "communication to basestation: NOT ACTIVE", e
			#sock = None
			#time.sleep(.5)
			return False


image = Image.open("temp.jpg")

top = Tkinter.Tk()
text1 = Tkinter.StringVar()
text1.set('Text')
heartbeat = Tkinter.StringVar()
heartbeat.set('NO HEARTBEAT')

i = 0
button_txt = i

def snap_shot():
	#capture from camera at location 0
	now = time.time()
	#cap = cv2.VideoCapture(0)
	global cap
	global photo
	print 'cap=', cap
	try:
		#have to capture a few frames as it buffers a few frames..
		for i in range (5):
			ret, img = cap.read()		 
		print (time.time()) - now
		#img.save('temp.png')
		#cv2.imshow('grab',img)
		#cv2.waitKey()
		cv2.imwrite('temp.jpg', img)
		img1 = Image.open('temp.jpg')
		img1.thumbnail((320,240))
		#if img1.size[0] <> 320 or img1.size[1] <> 240:
		#	print "Image is not right size. Resizing image...."
		#	img1 = img1.resize((320, 240))
		#	print "Resized to 320, 340"
	
		#img1 = Image.open(filename).convert('RGB').save('temp.gif')
		img1.save('temp.jpg')
		#img1.show()
		#update display
		#image = Image.open("temp.jpg")
		#image.thumbnail((320,240))
		photo = ImageTk.PhotoImage(img1)
		label.config(image=photo)	
		#label.pack()
		print (time.time()) - now
	except:
		print "could not grab webcam"
	#cap.release()
	#cap = cv2.VideoCapture(0)
	return img


def Send_Image():
	vf = send_video('u1204vm.local', 9091, 9090, 'temp.jpg')
	vf.daemon=True
	vf.start()

'''
	#temparaily just send random image
	
	#use folder to send images
	#image =  random.choice(os.listdir("/home/mobot/projects/robomow/images"))
	#FILE = "/home/mobot/projects/robomow/images/" + image
	####
	#grab image from webcam
	now = time.time()
	snap_shot()
	print "time to execute:", (time.time()) - now
	time.sleep(.3)
	FILE = "temp.jpg"
	print 'ip , port = ', ip, port
	try:
		data_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		data_tcp.connect((ip, port))
		print "data port connected..."
		f = open(FILE, "rb")
		print "sending image:", FILE
		data = f.read()
		f.close()
		data_tcp.send(data)
		data_tcp.close()
		print "bytes of image date sent:", len(data)
	except:
		print 'no data sent'
'''

class send_video(Thread):
	def __init__(self, host, cport, mport, filetosend):        
		self.host = host
		self.cport = cport
		self.mport = mport
		self.filetosend = filetosend
		Thread.__init__(self)

	def run(self):
			while True:
				snap_shot()
				#time.sleep(.05)

				#HOST = 'u1204vm.local'
				#CPORT = 9091
				#MPORT = 9090
				#FILE = sys.argv[1]
				print "sending image"
				cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				cs.connect((self.host, self.cport))
				cs.send("SEND " + self.filetosend)
				cs.close()

				time.sleep(0.05)

				ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				ms.connect((self.host, self.mport))

				f = open(self.filetosend, "rb")
				data = f.read()
				f.close()

				ms.send(data)
				ms.close()
				print "waiting one second before sending another image"
				#time.sleep(.1)

def Send_Sonar_Data(ip,port):
	global sonar
	#now = time.time()
	sonar_data  = str(sonar.distances_cm())
	print "sonar_data:", sonar_data
	#print "time to execute:", (time.time()) - now
	#time.sleep(.1)
	#print 'ip , port = ', ip, port
	try:
		data_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		data_tcp.connect((ip, port))
		print "data port connected..."
		data_tcp.send(sonar_data)
		data_tcp.close()
		print "bytes of sonar data sent:", len(sonar_data)
	except:
		print 'no data sent'



def update_display():
		global IP, PORT, testmode
		text1.set( str(datetime.now()) )
		#print "update called", i
		if (testmode == False):
			com_response = com_loop(IP,PORT)
			if  com_response != False:
				#time.sleep(.5) 
				#com_status.set('COM ACTIVE')
				heartbeat.set('COM ACTIVE')
				if com_response != "PING\n":
					print "COM ACTIVE at time: ", str(datetime.now())
					print "Response from Basestation: ", com_response
					#echo the command received
					#sock.send(com_response)
				
					#if com_response == "IU": Send_Image(basestation[0], 12345)
					if com_response == "IU": Send_Image()
					if com_response == "US": Send_Sonar_Data(basestation[0], 12345)
			else:
				heartbeat.set('COM NOT ACTIVE')
				print "COM NOT ACTIVE at time: ", str(datetime.now())
				#sock = None
				conn = None
				#sock.close()
				#basestation = None
				time.sleep(.5)
		#com_loop(IP, PORT)
		#time.sleep(.1)
		top.update()
		top.after(50, update_display)

def gethostaddress(): 
	os.system("ifconfig > temp.txt")
	f=open('temp.txt', 'r')
	for line in f:
		#print line
		where = line.find('192.168')
		if where > -1:
			my_ip = line[where:where+13]
	print 'my_ip=', my_ip
	return my_ip


if __name__== "__main__":
	testmode = False

	if len(sys.argv) > 1:
		if sys.argv[1] == 'testmode':
				print 'starting in testing mode'
				testmode= True

	#IP = gethostaddress()
	IP = ''
	PORT = 50005
	#B = Tkinter.Button(top, text=button_txt, command = helloCallBack)
	#B2 = Tkinter.Button(top, text=button_txt, command = helloCallBack)
	L1 = Tkinter.Label(top, textvariable=text1).pack()
	Label_HeartBeat = Tkinter.Label(top, textvariable=heartbeat).pack()

	photo = ImageTk.PhotoImage(image)
	label = Tkinter.Label(image=photo); label.pack()
	#label.image = photo # keep a reference!
	
	#B.pack()
	#B2.pack()
	Send_Image()
	##start sonar
	if (testmode == False):
		sonar= MaxSonar()


	update_display()
	#time.sleep(.01)
	top.mainloop()

