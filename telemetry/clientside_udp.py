import socket, time

UDP_IP="127.0.0.1"
UDP_PORT=5005

sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock.bind( (UDP_IP,UDP_PORT) )

count = 0

while True:
	now = time.time()
	count = count + 1
	print count
	data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
	print "received message:", data,  "   time:", (now-(time.time()))

