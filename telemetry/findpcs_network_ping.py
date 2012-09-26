#!/usr/bin/env python

# this program pings all pcs and returns a list of names found


import socket

if hasattr(socket, 'setdefaulttimeout'):
	print 'Set the default timeout on sockets to 5 seconds'
	print socket.getdefaulttimeout()
	socket.setdefaulttimeout(.1)
	print socket.getdefaulttimeout()

for ip in range(87, 255):
	ip_to_ping = "192.168.1."+str(ip)
	print "PINGING:", ip_to_ping
	try:
		answer = socket.gethostbyaddr(ip_to_ping)
		print answer[0]
		if answer[0] == "mobot-2012.local":
			print "FOUND IT"
	except:
		print "Oops!  That was no valid number.  Try again..."



