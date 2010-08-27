# Echo client program
import socket
import time


HOST = '192.168.1.118'    # The remote host
PORT = 50008              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for i in range(3):
   try:
      print  s.connect((HOST, PORT))
      break
   except IOError as detail:
      print "No server to connect to...retrying in 3 seconds", detail[0], detail [1]
      time.sleep(3)


for i in range(3):
   time.sleep(3)
   try:
      print "sending data...", i
      s.send('Hello, world')
      data = s.recv(1024)
      print 'Received', repr(data)
   except IOError as detail:
      print detail
      s.close()
      break
"""
time.sleep(6)
try:
   s.send('Hello, world')
   data = s.recv(1024)
   s.close()
   print 'Received', repr(data)
except IOError as detail:
   print detail
"""
