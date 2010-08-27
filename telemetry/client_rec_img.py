#!/usr/bin/python

import socket
from PIL import ImageFile

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(('127.0.0.1', 12345))
tcp.send("1000 4")

file = open("bar.jpg", "w")
parser = ImageFile.Parser()

while 1:
  jpgdata = tcp.recv(65536)
  if not jpgdata:
    tcp.close()
    break

  parser.feed(jpgdata)
  file.write(jpgdata)

file.close()
image = parser.close()
image.show()
