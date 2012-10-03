import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from PIL import ImageFile
from datetime import datetime
#from ThreadedBeatServer import *
import socket 

sock = None

def com_loop(address, port):
	global sock
	#print "sock:", sock
	if sock == None:
		try:
			print "Attempting to connect to %s on port %s" % (address, port)	
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((address, port))
			print "Connected to %s on port %s" % (address, port)
			return True
		except socket.error, e:
			print "Connection to %s on port %s failed: %s" % (address, port, e)
			return False
	else:
		try:
			sock.send("PING\n")
			print "communication to robot: ACTIVE"
			#sock.settimeout(.5)
			#data = sock.recv(1)	
			#print "recieved from robot: ", data	
			time.sleep(.1)
			return True
		except socket.error, e:
			print "communication to robot: NOT ACTIVE"
			sock = None
			time.sleep(.1)
			return False

def move(direction):
	print "move called"
	#time.sleep(1)
	IP="192.168.1.87"
	PORT=5005
	MESSAGE=direction
	print "target IP:", IP
	print "target port:", PORT
	print "moving:", MESSAGE
	sock = socket.socket( socket.AF_INET, # Internet
		            socket.SOCK_DGRAM ) # UDP
					#socket.SOCK_STREAM)  #TCP
	#while 1:
	sock.sendto( MESSAGE, (IP, PORT) )
	#time.sleep(1)


def send_command_to_robot(command):
	global sock
	IP="192.168.1.87"
	PORT=50005
	print "target IP:", IP
	print "target port:", PORT
	print "Command:", command
	try:
		sock.send(command)
		print "Command Sent to Robot:", command
		time.sleep(.1)
		return True
	except socket.error, e:
		print "communication to robot: NOT ACTIVE"
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
		#send_command_to_robot("edm")
		Button_Enable_Motors.configure(bg = "green")
		MF.pack()
		MB.pack()
		ML.pack()
		MR.pack()

def show_buttons():	
		Button_Enable_Motors.pack()
		Button_Update_Image.pack()
		camera_1.pack()

def update_images():
	IP = '192.168.1.43'
	PORT = 12345
	try:
		sock.send("IU")
		tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#tcp.connect(('192.168.1.87', 12345))
		#tcp.send("1000 4")	
		tcp.bind((IP,PORT))
		print "listening..."
		tcp.listen(1)
		tcp.settimeout(1)
		print "waiting for data connection.."
		conn, addr = tcp.accept()
		print "accepted connection from client.."	
		file = open("rec_image.jpg", "w")
		parser = ImageFile.Parser()
		print time.time()
		#temp = conn.recv(1024)
		#print temp

		while 1:
			print "receiving image data..."
			jpgdata = conn.recv(65536)
			#print jpgdata
			if not jpgdata:
			#sock.close()
				print "no more data"
				break
			parser.feed(jpgdata)
			file.write(jpgdata)

		print time.time()
		print "data received.."
		file.close()
		image = parser.close()
		image.show()
		image = Image.open("rec_image.jpg")
		photo = ImageTk.PhotoImage(image)
	 	camera_1 = Tkinter.Label(image=photo); camera_1.pack()

	except IOError as detail:
		print "connection lost", detail

def update_display():
		#global heartbeat_enabled
		IP = "192.168.1.87"
		PORT = 50005
		print "update called"
		if com_loop(IP,PORT) == True:
		#if 1 == 1: 
			com_status.set('COM ACTIVE')
			Button_Com_Status.configure(bg = "green")
			#send_heartbeat()
			show_buttons()
			#update_images()
		else:
			com_status.set('COM NOT ACTIVE')
			Button_Com_Status.configure(bg = "red")
			hide_buttons()
		main_gui.update()	
		main_gui.after(100, update_display)

if __name__== "__main__":
	main_gui = Tkinter.Tk()
	main_gui.geometry("640x480")
	image = Image.open("temp.jpg")
	IP = "192.168.1.87"
	PORT = 50005
	com_status = Tkinter.StringVar()
	com_status.set('COM INACTIVE')

	#Label_Com_Status = Tkinter.Label(main_gui, text="Helvetica", font=("Helvetica", 16),  textvariable=com_status, bg=com_status_color.get()).pack()
	Button_Com_Status = Tkinter.Button(main_gui, textvariable=com_status);Button_Com_Status.pack();
	Button_Enable_Motors = Tkinter.Button(main_gui, text="Enable Drive Motors", command= enable_drive_motors); Button_Enable_Motors.pack();
	MF = Tkinter.Button(main_gui, text="Forward", command=lambda: send_command_to_robot('f')); MF.pack();
	MB = Tkinter.Button(main_gui, text="Reverse", command=lambda: send_command_to_robot('b')); MB.pack();
	ML = Tkinter.Button(main_gui, text="Left", command=lambda: send_command_to_robot('l')); ML.pack();
	MR = Tkinter.Button(main_gui, text="Right", command=lambda: send_command_to_robot('r')); MR.pack();
	Button_Update_Image = Tkinter.Button(main_gui, text="Grab Images", command=update_images); Button_Update_Image.pack();
	

	photo = ImageTk.PhotoImage(image)
	camera_1 = Tkinter.Label(image=photo); camera_1.pack()

	update_display()
	#time.sleep(.01)
	print "hi"
	main_gui.mainloop()
	print "out"
