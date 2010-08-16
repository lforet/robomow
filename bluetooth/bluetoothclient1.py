# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py,v 1.3 2006/02/24 19:42:34 albert Exp $

from bluetooth import *
import sys

addr = None

if len(sys.argv) < 2:
    print "no device specified.  Searching all nearby bluetooth devices for"
    print "the FooBar service"
else:
    addr = sys.argv[1]
    print "Searching for FooBar on %s" % addr

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

print "connected.  type stuff"
while True:
    data = raw_input('from client:')
    if not data: break
    sock.send(data)
    data = sock.recv(1024)
    print 'Received from server: ', `data`
sock.close()
