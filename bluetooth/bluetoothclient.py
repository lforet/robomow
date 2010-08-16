# file: rfcomm-client.py
# original code auth: Albert Huang <albert@csail.mit.edu>
# modified multithreaded client/server auth: andrew blaich <ablaich@cse.nd.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py,v 1.3 2006/02/24 19:42:34 albert Exp $

from bluetooth import *
from select import *
import sys
import threading
import thread
import time


class ClientThreadRecv(threading.Thread):
    def __init__(self, sock):
        self.sock = sock;
        threading.Thread.__init__(self);
	
    def run(self):
        #try:
        while True:
            for s in can_rd:
                threadLock.acquire(0);
                try:
                    data = self.sock.recv(1024)
                    print "Server sends:", " [%s]" % data
                finally:
                    if threadLock.locked==True:						
                        threadLock.release();

class ClientThreadSend(threading.Thread):
    def __init__(self, sock):
        self.sock = sock;
        threading.Thread.__init__(self);
        
    def run(self):
        while True:
            for s1 in can_wr:
                threadLock.acquire(0);
                try: 
                    data = time.ctime();    		
                    if len(data) == 0: break
                    print "Client is sending: "+data;
                    self.sock.send(data)
                    data="";
                finally:
                    if threadLock.locked==True:						
                        threadLock.release();
                time.sleep(5);
			
###########################################################
addr = None

if len(sys.argv) < 2:
    print "no device specified.  Searching all nearby bluetooth devices for"
    print "the bt serve"
else:
    addr = sys.argv[1]
    print "Searching for bt serve on %s" % addr

# search for the FooBar service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print "couldn't find the FooBar service =("
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print "connecting to \"%s\" on %s" % (name, host)

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))
sock.setblocking(True);

print "Connected:"

global can_rd
global can_wr
global has_exc

can_rd = 0

print "can_rd %s" % can_rd

global threadLock
threadLock=threading.Lock();	

print "Starting Receiving Thread";
ClientThreadRecv(sock).start();	
print "Starting Sending Thread (a time stamp is sent at 5 second intervals to the server)"; 
ClientThreadSend(sock).start();

print "Setup Complete, Client is running..."

while True:
	can_rd, can_wr, has_exc = select( [sock], [sock], [], 2 )

sock.close();

