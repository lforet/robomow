import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from datetime import datetime
#from ThreadedBeatServer import *
import socket 

def check_heartbeat():

	HOST = '192.168.1.87'                 # Symbolic name meaning the local host
	PORT = 50005             # Arbitrary non-privileged port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT)) 
	#next line spcifies how long in seconds to wait for a connection
	s.settimeout(1.0)

	print "listening..."
	s.listen(1)
	print "made connection..."

	try:
	    print "waiting to accept.."
	    conn, addr = s.accept()
	    print "accepted connection from client.."
	    while conn <> "":
		s.listen(1)
		#print time.time()
		#print s.gettimeout()
		print 'Connected by', addr
		data = conn.recv(1024)
		if not data: break
		print 'Received from remote: ', data 
		conn.send("ACK") 
	except IOError as detail:
	    print "connection lost", detail

	try:
	    print "closing Socket"
	    s.close()
	except NameError as detail:
	    print "No socket to close", detail


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
		#global i
		text1.set( str(datetime.now()) )
		#top.update_idletasks()
		print "update called", i
		print "check heartbeat"
		#if check_heartbeat() == True: Label_HeartBeat["text"]='HEARTBEAT' 
		heart_check = check_heartbeat()
		if heart_check == True: heartbeat.set('HEARTBEAT')
		if heart_check == False: heartbeat.set('NO HEARTBEAT')
		top.update()

		top.after(50, update_display)


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
#first_run = False
if __name__== "__main__":
	update_display()
	#time.sleep(.01)
	print "hi"
	top.mainloop()
	print "out"

