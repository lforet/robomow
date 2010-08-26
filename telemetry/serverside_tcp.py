# Echo server program
import socket
import time

HOST = ''                 # Symbolic name meaning the local host
PORT = 50008              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except IOError as detail:
    print "no connection", detail

#next line spcifies how long in seconds to wait for a connection
s.settimeout(10.0)

s.listen(1)

try:
    conn, addr = s.accept()
    while 1:
        print time.time()
        s.listen(1)
        #print s.gettimeout()
        print 'Connected by', addr
        data = conn.recv(1024)
        if not data: break
        print 'Received from remote: ', data 
        #time.sleep(3)
        conn.send(data) 

except IOError as detail:
    print "no connection", detail

try:
    print "closing Socket"
    s.close()
except NameError as detail:
    print "No socket to close", detail
