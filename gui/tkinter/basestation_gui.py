import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from datetime import datetime
#from ThreadedBeatServer import *
import socket 

heartbeat_enabled = False
main_gui = Tkinter.Tk()

def send_heartbeat():
	UDP_IP="127.0.0.1"
	UDP_PORT=5005
	MESSAGE="ACK"
	print "UDP target IP:", UDP_IP
	print "UDP target port:", UDP_PORT
	print "message:", MESSAGE
	sock = socket.socket( socket.AF_INET, # Internet
		            socket.SOCK_DGRAM ) # UDP
	#while 1:
	sock.sendto( MESSAGE, (UDP_IP, UDP_PORT) )
	#time.sleep(.05)

def toggle_heartbeat():
	global heartbeat_enabled
	if heartbeat_enabled == True: 
		heartbeat_enabled = False 
	else:
		heartbeat_enabled = True

def update_display():
		global heartbeat_enabled

		#text1.set( str(datetime.now()) )
		#top.update_idletasks()
		print "update called"
		print "check heartbeat", heartbeat_enabled 
		#if check_heartbeat() == True: Label_HeartBeat["text"]='HEARTBEAT' 
		if heartbeat_enabled == True:
			B["text"]= "Stop Heartbeat"
			send_heartbeat()
		else:
			B["text"]= "Start Heartbeat"
		main_gui.update()
		main_gui.after(50, update_display)


B = Tkinter.Button(main_gui, text="Start Heartbeat", command = toggle_heartbeat)
#Label_HeartBeat = Tkinter.Label(top, textvariable=heartbeat).pack()

B.pack()



if __name__== "__main__":
	update_display()
	#time.sleep(.01)
	print "hi"
	main_gui.mainloop()
	print "out"
