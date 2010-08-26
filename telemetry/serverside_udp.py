   1 import socket
   2 
   3 UDP_IP="127.0.0.1"
   4 UDP_PORT=5005
   5 MESSAGE="Hello, World!"
   6 
   7 print "UDP target IP:", UDP_IP
   8 print "UDP target port:", UDP_PORT
   9 print "message:", MESSAGE
  10 
  11 sock = socket.socket( socket.AF_INET, # Internet
  12                       socket.SOCK_DGRAM ) # UDP
  13 sock.sendto( MESSAGE, (UDP_IP, UDP_PORT) )

