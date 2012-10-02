import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from datetime import datetime
#from ThreadedBeatServer import *
import socket 

sock = None
conn = None

def com_loop(IP, PORT):
	global sock, conn
	#print "sock, conn", sock, conn
	if conn == None:	
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "binding port...."
			sock.bind((IP, PORT))
			conn = None
			print "listening..."
			sock.listen(1)
			sock.settimeout(1)
			print "waiting to accept.."
			conn, addr = sock.accept()
			print "accepted connection from client..", conn, addr
			return True 
		except IOError as detail:
			print "communication to basestation: NOT ACTIVE"
			conn = None
			time.sleep(.1)
			return False
	else:
		try:
			if conn != None:
				data = conn.recv(1024)
				#if not data: break
				print 'Received from remote: ', data
				time.sleep(.1)	
				if len(data) > 0:
					print "communication to basestation: ACTIVE"		
					#time.sleep(.5)
					return True
				else:
					print "communication to basestation: NOT ACTIVE"
					conn = None
					time.sleep(.1)
					return False
		except socket.error, e:
			print "communication to basestation: NOT ACTIVE", e
			#sock = None
			time.sleep(.5)
			return False


image = Image.open("temp.jpg")

top = Tkinter.Tk()
text1 = Tkinter.StringVar()
text1.set('Text')
heartbeat = Tkinter.StringVar()
heartbeat.set('NO HEARTBEAT')

i = 0
button_txt = i

def helloCallBack():
	global i
   	#tkMessageBox.showinfo( "Hello Python", "Hello World")
   	print "do some stuff"
   	i = i + 1
	B["text"]=i
   	#text1.set("New Text!")

	
def update_display():
		IP = "192.168.1.87"
		PORT = 50005
		text1.set( str(datetime.now()) )
		print "update called", i
		if com_loop(IP,PORT) == True:
			#time.sleep(.5) 
			#com_status.set('COM ACTIVE')
			heartbeat.set('COM ACTIVE')
			#send_heartbeat()
			#show_buttons()
			#update_images()
		else:
			heartbeat.set('COM NOT ACTIVE')
			#Button_Com_Status.configure(bg = "red")
			#hide_buttons()
		#	time.sleep(.01)
		#com_loop(IP, PORT)
		#time.sleep(.1)
		top.update()
		top.after(50, update_display)

if __name__== "__main__":
	IP = "192.168.1.87"
	PORT = 50005
	B = Tkinter.Button(top, text=button_txt, command = helloCallBack)
	B2 = Tkinter.Button(top, text=button_txt, command = helloCallBack)
	L1 = Tkinter.Label(top, textvariable=text1).pack()
	Label_HeartBeat = Tkinter.Label(top, textvariable=heartbeat).pack()

	photo = ImageTk.PhotoImage(image)
	label = Tkinter.Label(image=photo)
	label.image = photo # keep a reference!
	label.pack()
	B.pack()
	B2.pack()

	
	update_display()
	#time.sleep(.01)
	print "hi"
	top.mainloop()
	print "out"

