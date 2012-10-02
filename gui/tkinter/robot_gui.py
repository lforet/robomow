import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from datetime import datetime
#from ThreadedBeatServer import *
import socket 

sock = None

def com_loop(IP, PORT):
	global sock
	if sock == None:	
		try:
			print "binding port...."
			sock.bind((IP, PORT))
			print "waiting to accept.."
			conn, addr = s.accept()
			print "accepted connection from client..", conn, addr
			while conn <> "":
			s.listen(1)
			print 'Connected by', addr
			data = conn.recv(256)
			if not data: break
			print 'Received from remote: ', data
			time.sleep(.5)
			return True 
		except IOError as detail:
			print "connection lost", detail
			return False
	else:
		try:
			sock.send("PING")
			print "communication to basestation: ACTIVE"		
			time.sleep(.5)
			return True
		except socket.error, e:
			print "communication to basestation: NOT ACTIVE"
			sock = None
			time.sleep(.5)
			try:
				print "closing Socket"
				s.close()
			except NameError as detail:
				print "No socket to close", detail
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
		#top.update_idletasks()
		print "update called", i
		if com_loop(IP,PORT) == True: 
			#com_status.set('COM ACTIVE')
			#Button_Com_Status.configure(bg = "green")
			#send_heartbeat()
			#show_buttons()
			#update_images()
		else:
			#com_status.set('COM NOT ACTIVE')
			#Button_Com_Status.configure(bg = "red")
			#hide_buttons()
		time.sleep(.01)
		top.update()
		top.after(100, update_display)

if __name__== "__main__":
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

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((HOST, PORT)) 
	update_display()
	#time.sleep(.01)
	print "hi"
	top.mainloop()
	print "out"

