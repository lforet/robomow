#!/usr/bin/python

import socket
from PIL import ImageFile
import time

HOST = '127.0.0.1'
CPORT = 12345
MPORT = 12346

data_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
filename_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#filename_tcp.connect(('127.0.0.1', 12345))
#data_tcp.connect(('127.0.0.1', 12346))
#tcp.send("1000 4")

filename_tcp.bind((HOST, CPORT))
data_tcp.bind((HOST, MPORT)) 
#next line spcifies how long in seconds to wait for a connection
#s.settimeout(5.0)

print "listening..."
filename_tcp.listen(1)
data_tcp.listen(1)

"""
#if want to recieve a file
try:
    print "waiting for filename connection.."
    conn, addr = filename_tcp.accept()
    print "accepted connection from client.."
    data = filename_tcp.recv(1024)
    if data <> "":
        print 'Received filename from server...', repr(data)
        filename = repr(data)
    else:
        print "filename not received from server"
        break
except IOError as detail:
    print "connection lost", detail
"""
#to receive and view pil image
try:
    print "waiting for data connection.."
    conn, addr = data_tcp.accept()
    print "accepted connection from client.."

    file = open("bar.jpg", "w")
    parser = ImageFile.Parser()
    print time.time()

    while 1:
        jpgdata = conn.recv(65536)
        if not jpgdata:
            data_tcp.close()
            print "no more data"
            break
        parser.feed(jpgdata)
        file.write(jpgdata)
    print time.time()
    print "data received.."
    file.close()
    image = parser.close()
    image.show()
except IOError as detail:
    print "connection lost", detail



