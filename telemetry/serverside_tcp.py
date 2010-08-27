# Echo server program
import socket
import time

HOST = ''                 # Symbolic name meaning the local host
PORT = 50008              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) 
#next line spcifies how long in seconds to wait for a connection
#s.settimeout(5.0)



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
