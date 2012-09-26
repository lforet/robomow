import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from datetime import datetime
#from ThreadedBeatServer import *
import socket 

heartbeat_enabled = False


def send_heartbeat():
	IP="192.168.1.87"
	PORT=5005
	MESSAGE="ACK"
	print " target IP:", IP
	print " target port:", PORT
	print "message:", MESSAGE
	sock = socket.socket( socket.AF_INET, # Internet
		            socket.SOCK_DGRAM ) # UDP
					#socket.SOCK_STREAM)  #TCP
	#while 1:
	sock.sendto( MESSAGE, (IP, PORT) )
	#time.sleep(.05)

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


def toggle_heartbeat():
	global heartbeat_enabled
	if heartbeat_enabled == True: 
		heartbeat_enabled = False 
	else:
		heartbeat_enabled = True

def hide_buttons():
		MF.pack_forget()
		MB.pack_forget()
		ML.pack_forget()
		MR.pack_forget()
		camera_1.pack_forget()
		

def show_buttons():	
		MF.pack()
		MB.pack()
		ML.pack()
		MR.pack()
		camera_1.pack()

def update_images():
	HOST = "192.168.1.87"
	CPORT = 5006
	MPORT = 5007

	data_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	filename_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	filename_tcp.bind((HOST, CPORT))
	data_tcp.bind((HOST, MPORT)) 
	#next line spcifies how long in seconds to wait for a connection
	#s.settimeout(5.0)

	print "listening..."
	filename_tcp.listen(1)
	data_tcp.listen(1)

	#to receive and view pil image
	try:
		print "waiting for data connection.."
		conn, addr = data_tcp.accept()
		print "accepted connection from client.."

		file = open("rec_image.jpg", "w")
		parser = ImageFile.Parser()
		print time.time()

		while 1:
		    jpgdata = conn.recv(65536)
		    if not jpgdata:
		        data_tcp.close()
		        print "no more data"
		        break
		    parser.feed(jpgdata)
		    file.write(jpgdata)
		print time.time()
		print "data received.."
		file.close()
		image = parser.close()
		#image.show()
		image = Image.open("rec_image.jpg")
		photo = ImageTk.PhotoImage(image)
	 	camera_1 = Tkinter.Label(image=photo); camera_1.pack()

	except IOError as detail:
		print "connection lost", detail




def update_display():
		global heartbeat_enabled

		#text1.set( str(datetime.now()) )
		#top.update_idletasks()
		print "update called"
		print "check heartbeat", heartbeat_enabled 
		#if check_heartbeat() == True: Label_HeartBeat["text"]='HEARTBEAT' 
		if heartbeat_enabled == True: 
			HB["text"]= "Stop Heartbeat"
			send_heartbeat()
			show_buttons()
			#update_images()
		else:
			HB["text"]= "Start Heartbeat"
			hide_buttons()
		main_gui.update()	
		main_gui.after(50, update_display)


#Label_HeartBeat = Tkinter.Label(top, textvariable=heartbeat).pack()

if __name__== "__main__":
	main_gui = Tkinter.Tk()
	main_gui.geometry("640x480")
	image = Image.open("temp.jpg")

	HB = Tkinter.Button(main_gui, text="Start Heartbeat",command=toggle_heartbeat);HB.pack();
	MF = Tkinter.Button(main_gui, text="Forward", command=lambda: move('f')); MF.pack();
	MB = Tkinter.Button(main_gui, text="Reverse", command=lambda: move('b')); MB.pack();
	ML = Tkinter.Button(main_gui, text="Left", command=lambda: move('l')); ML.pack();
	MR = Tkinter.Button(main_gui, text="Right", command=lambda: move('r')); MR.pack();
	UI = Tkinter.Button(main_gui, text="Grab Images", command=update_images); UI.pack();
	photo = ImageTk.PhotoImage(image)
	camera_1 = Tkinter.Label(image=photo); camera_1.pack()

	update_display()
	#time.sleep(.01)
	print "hi"
	main_gui.mainloop()
	print "out"
