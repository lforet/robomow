from Tkinter import *
import tkMessageBox
from PIL import Image, ImageTk
import time
from PIL import ImageFile
from datetime import datetime
#from ThreadedBeatServer import *
import socket 
import sonar_functions as sf
from FileReceiver import *
from threading import *
import matplotlib.pyplot as P
import matplotlib.cm as cm
from matplotlib.pyplot import figure, show, rc
import pylab as pl
import numpy as np
<<<<<<< HEAD
import gc
=======
>>>>>>> e0d260f296db2ad7fde958de126416ea81ad932d

sock = None
ROBOT_IP = None
PORT = 50005

def TextOut(text):
	if (paused.get() != 'UN-PAUSE'):
		Textbox1.insert(END, str(datetime.now()) + ':' + text +'\n') #print new line in textbox
		Textbox1.yview(END) 			#autoscroll

def Search_For_Robot():
	global ROBOT_IP
	#first try by dns lookup
	#robot_name = 'mobot-2012'
	try:
		answer = None
		print "Searching for Robot using DNS..."
		TextOut("Searching for Robot using DNS...")
		time.sleep(.1)		
		answer = socket.gethostbyname('mobot-2012.local')
		print "Robot found on IP: ", answer
		TextOut("Robot found on IP: " + answer)
		ROBOT_IP = answer
		return answer
	except:
		if answer == None:
			print "failed DNS Search...trying PING method...", answer
		
			for ip in xrange(30, 150, 1):
				ip_to_ping = "192.168.1."+str(ip)
				print "Searching for Robot on IP:", ip_to_ping,
				TextOut("Searching for Robot on IP:" + ip_to_ping)
				try:
					answer = socket.gethostbyaddr(ip_to_ping)
					print ": Found Device: ",answer[0]
					temp = answer[0][:10]
					#print "temp=", temp
					#Textout(": Found Device: " + temp)
					if temp == 'mobot-2012':
						print "Robot found on IP: ", ip_to_ping
						TextOut("Robot found on IP: " + ip_to_ping)
						ROBOT_IP = ip_to_ping
						return ip_to_ping
						break
				except:
					print ": No response....."
					TextOut(": No response.....")
			return False
		else:
			return answer

<<<<<<< HEAD
=======
def sonar_graph(ping_readings):
	print "ping reading:", ping_readings
	print type(ping_readings[1])
	# force square figure and square axes looks better for polar, IMO
	fig = pl.figure(figsize=(6,6))
	ax = P.subplot(1, 1, 1, projection='polar')
	P.rgrids([28, 61, 91])
	ax.set_theta_zero_location('N')
	ax.set_theta_direction(-1)
	theta = 356
	angle = theta * np.pi / 180.0
	radii = [ping_readings[0]]
	width = .15
	bars1 = ax.bar(0, 100, width=0.001, bottom=0.0)
	#print "theta, radii, width: ", theta, radii, width
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
	theta = 86
	angle = theta * np.pi / 180.0
	radii = [ping_readings[1]]
	width = .15
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')	
	theta = 176
	angle = theta * np.pi / 180.0
	radii = [ping_readings[2]]
	width = .15
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
	theta = 266
	angle = theta * np.pi / 180.0
	radii = [ping_readings[3]]
	width = .15
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
	#print "finshed graph"
	#pil_img = fig2img(fig)
	#sonar_image = pil_img
	#print type(pil_img), pil_img
	#sonar_image = PILtoCV_4Channel(pil_img)
	#cv.ShowImage("Sonar", sonar_image )
	#cv.MoveWindow ('Sonar',50 ,50 )
	time.sleep(.01)
	#cv.WaitKey(10)
	fig.savefig('sonar_image.png')
	Image.open('sonar_image.png').save('sonar_image.jpg','JPEG')
	#stop
	#garbage cleanup
	#fig.clf()
	#P.close()
	return

>>>>>>> e0d260f296db2ad7fde958de126416ea81ad932d

def com_loop(address, port):
	global sock
	#print "sock:", sock
	if sock == None:
		try:
			print "Attempting to connect: %s port %s" % (address, port)
			TextOut("Attempting to connect: %s port %s" % (address, port))	
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(.1)
			sock.connect((address, port))
			print "Connected to %s on port %s" % (address, port)
			TextOut("Connected to %s on port %s" % (address, port))
			return True
		except socket.error, e:
			print "Connection to: %s port %s failed: %s" % (address, port, e)
			TextOut("Connection to: %s port %s failed: %s" % (address, port, e))
			return False
	else:
		try:
			sock.send("PING\n")
			#print "communication to robot: ACTIVE"
			#TextOut("communication to robot: ACTIVE")
			#data = sock.recv(1)	
			#print "recieved from robot: ", data	
			time.sleep(.1)
			return True
		except socket.error, e:
			print "communication to robot: NOT ACTIVE"
			TextOut("communication to robot: NOT ACTIVE")
			sock = None
			time.sleep(.5)
			return False

def toggle_button_pause():
	'''
	use
	t_btn.config('text')[-1]
	to get the present state of the toggle button
	'''
	if button_pause.config('text')[-1] == 'UN-PAUSE':
		#button_pause.config(text='PAUSE')
		paused.set('PAUSE')
	else:
		#button_pause.config(text='UN-PAUSE')
		paused.set('UN-PAUSE')


def send_command_to_robot(command, ip, port):
	global sock
	#IP="192.168.1.87"
	#PORT=50005
	#print "target IP:", IP
	#print "target port:", PORT
	#print "Command:", command
	if sock != None:
		try:
			sock.send(command)
			print "Command Sent to Robot:", command
			TextOut("Command Sent to Robot:" + command)
			reply = sock.recv(1024)
			TextOut("Echoed from Robot:" + reply)
			time.sleep(.1)
			return True
		except socket.error, e:
			print "Send Command Failed"
			TextOut("Send Command Failed")
			print "com to robot: NOT ACTIVE"
			TextOut("communication to robot: NOT ACTIVE")
			sock = None
			time.sleep(.5)
			return False
	else:
		print "Send Command Failed"
		TextOut("Send Command Failed")
		print "com to robot: NOT ACTIVE"
		TextOut("communication to robot: NOT ACTIVE")
		sock = None
		time.sleep(.5)
		return False

def hide_buttons():
		Button_Enable_Motors.pack_forget()
		MF.pack_forget()
		MB.pack_forget()
		ML.pack_forget()
		MR.pack_forget()
		Button_Update_Image.pack_forget()
		camera_1.pack_forget()
		

def enable_drive_motors():
	print Button_Enable_Motors.configure('text')[-1][0]
	if Button_Enable_Motors.configure('text')[-1][0] == 'Disable':
		#button_pause.config(text='PAUSE')
		#paused.set('PAUSE')
		Button_Enable_Motors.configure(text='Enable Drive Motors', bg = "red")	
		MF.configure(state=DISABLED, background='red')
		MB.configure(state=DISABLED, background='red')
		ML.configure(state=DISABLED, background='red')
		MR.configure(state=DISABLED, background='red')

	else:
		#button_pause.config(text='UN-PAUSE')
		#paused.set('UN-PAUSE')
		Button_Enable_Motors.configure(text='Disable Drive Motors', bg = "green")
		MF.configure(state=NORMAL, background='green')
		MB.configure(state=NORMAL, background='green')
		ML.configure(state=NORMAL, background='green')
		MR.configure(state=NORMAL, background='green')
	#send_command_to_robot("edm")

def show_buttons():	
		Button_Enable_Motors.pack()
		Button_Update_Image.pack()
		camera_1.pack()


def update_sonar(ip, port):
	#s = FileReceiver()
	#line below stops thread when main program stops
	#s.daemon = True
	#s.start()
	sonarfeed = sonar_feed()
	sonarfeed.daemon=True
	sonarfeed.start()
<<<<<<< HEAD
	#sonarfeed.join()
=======
	sonarfeed.join()
>>>>>>> e0d260f296db2ad7fde958de126416ea81ad932d

def update_images(ip, port):
	s = FileReceiver()
	#line below stops thread when main program stops
	s.daemon = True
	s.start()
	videofeed = video_feed()
	videofeed.daemon=True
	videofeed.start()

class video_feed(Thread):
<<<<<<< HEAD
	def run(self):
		while True:
			try:
				image = Image.open("snap_shot.jpg")
				image.thumbnail((320,240))
				photo1 = ImageTk.PhotoImage(image)
				camera_1.config(image=photo1)
				time.sleep(.1)
			except:
				pass
			

class sonar_feed(Thread):
	def run(self):
		while True:
			try:
=======
	def run(self):
		while True:
			try:
				image = Image.open("snap_shot.jpg")
				image.thumbnail((320,240))
				photo1 = ImageTk.PhotoImage(image)
				camera_1.config(image=photo1)
				time.sleep(.3)
			except:
				pass
			

class sonar_feed(Thread):
	def run(self):
		while True:
			try:
>>>>>>> e0d260f296db2ad7fde958de126416ea81ad932d
				f = open("sonar_data.txt", "r")
				sonar_data = f.readline()
				f.close()
				processed_sonar_data = []
				print "calling sonar_display"
				#sonar_image  = sf.sonar_display(sonar_data)
				processed_sonar_data = sf.process_sonar_data(sonar_data)
				print "processed_sonar_data ", processed_sonar_data 
<<<<<<< HEAD
				sf.sonar_graph(processed_sonar_data)
=======
				sonar_graph(processed_sonar_data)
>>>>>>> e0d260f296db2ad7fde958de126416ea81ad932d
				#print "saving sonar image"
				#sonar_image.save("sonar_image.jpg")
				#print "returning"
				#refresh with new somar image
<<<<<<< HEAD
				image = Image.open("sonar_image.png")
				#image.thumbnail((320,240))
				sonar_img = ImageTk.PhotoImage(image)
				sonar_display.config(image=sonar_img)
				time.sleep(.2)
				#gc.collect()
			except:
				pass
=======
				image = Image.open("sonar_image.jpg")
				image.thumbnail((320,240))
				sonar_img = ImageTk.PhotoImage(image)
				sonar_display.config(image=sonar_img)
				time.sleep(1)
			except:
				pass


>>>>>>> e0d260f296db2ad7fde958de126416ea81ad932d

def update_display():
		global ROBOT_IP
		#global heartbeat_enabled
		#IP = "192.168.1.44"
		PORT = 50005
		#print "update called"
		#print "paused:", paused.get()
		if (testmode == False):
			if ROBOT_IP != None:
				if com_loop(ROBOT_IP,PORT) == True:
				#if 1 == 1: 
					com_status.set('COM ACTIVE ON IP: '  + ROBOT_IP)
					Button_Com_Status.configure(bg = "green")
					#update_sonar()
					#show_buttons()
					#update_images()
				else:
					com_status.set('COM NOT ACTIVE' )
					Button_Com_Status.configure(bg = "red")
					#hide_buttons()
			else:
				 Search_For_Robot()
		#main_gui.update()	
		main_gui.after(100, update_display)

if __name__== "__main__":

	testmode = False

	if len(sys.argv) > 1:
		if sys.argv[1] == 'testmode':
				print 'starting in testing mode'
				testmode= True

	main_gui = Tk()
	main_gui.geometry("1150x840")

	com_status = StringVar()
	com_status.set('COM INACTIVE')
	
	frame1=Frame(main_gui,  bd=1, relief=SUNKEN)
	frame2=Frame(main_gui,  bd=1, relief=SUNKEN)
	frame3=Frame(main_gui,  bd=1, relief=SUNKEN)

	Button_Com_Status = Button(main_gui, textvariable=com_status);Button_Com_Status.pack();

	button_search_for_bot = Button(frame2, text="Find Bot", command=lambda: Search_For_Robot());
	#button_search_for_bot.grid(row=0, column=1, sticky=W)
	button_search_for_bot.pack()
	frame2.pack()

	Button_Enable_Motors = Button(main_gui, text="Enable Drive Motors", command=enable_drive_motors)
	Button_Enable_Motors.pack()
	MF = Button(frame1, text="Forward", command=lambda: send_command_to_robot('f', ROBOT_IP, PORT));
	#MF.grid(row=0, column=1, sticky=W)
 	MB = Button(frame1, text="Reverse", command=lambda: send_command_to_robot('b', ROBOT_IP, PORT))
	#MB.grid(row=0, column=2, sticky=W)
	ML = Button(frame1, text="Left", command=lambda: send_command_to_robot('l', ROBOT_IP, PORT))
	#ML.grid(row=1, column=1, sticky=W)
	MR = Button(frame1, text="Right", command=lambda: send_command_to_robot('r', ROBOT_IP, PORT))
	#MR.grid(row=1, column=2, sticky=W)
	MF.pack(side=LEFT)
	MB.pack(side=LEFT)
	ML.pack(side=LEFT)
	MR.pack(side=LEFT)
	frame1.pack( padx=5, pady=5)
	Button_Enable_Motors.configure(background='green')
	MF.configure(state=DISABLED, background='red')
	MB.configure(state=DISABLED, background='red')
	ML.configure(state=DISABLED, background='red')
	MR.configure(state=DISABLED, background='red')

	Button_Update_Image = Button(frame3, text="Grab Images", command=lambda: update_images(ROBOT_IP, 12345)); 
	Button_Update_Image.pack(side=LEFT);
	button_toggle_sonar = Button(frame3, text="Update Sonar", command=lambda: update_sonar(ROBOT_IP, 12345));
	button_toggle_sonar.pack()
	#frame3.pack(anchor=NW)
	frame3.pack()
#
	paused = StringVar()
	paused.set('PAUSE')
	button_pause = Button(main_gui, textvariable=paused, command=toggle_button_pause);button_pause.pack();

	#Button_show_Image = Button(main_gui, text="Load Image", command=random_image).pack(); 
	
	s = Scrollbar(main_gui)
	Textbox1 = Text(main_gui)
	Textbox1.focus_set()
	s.pack(side=RIGHT, fill=Y)
	Textbox1.pack(side=RIGHT)#, fill=Tkinter.Y)
	s.config(command=Textbox1.yview)
	Textbox1.config(yscrollcommand=s.set, width=90)#, height=50)

	var_IP_of_bot = StringVar(None)
	IP_of_bot = Entry(main_gui, textvariable=var_IP_of_bot)
	IP_of_bot.pack()

	image = Image.open("temp.jpg")
	sonar = Image.open('sonar_image.png')
	#sonar.thumbnail((440,440))
	photo1 = ImageTk.PhotoImage(image)
	camera_1 = Label(image=photo1, bd=1, relief=SUNKEN); camera_1.pack(padx=5, pady=5)
	

	sonar_img = ImageTk.PhotoImage(sonar)
	sonar_display = Label(image=sonar_img, bd=1, relief=SUNKEN); sonar_display.pack(padx=5, pady=5)
	
	#frame1.pack_forget()
	update_display()
	main_gui.mainloop()
	
