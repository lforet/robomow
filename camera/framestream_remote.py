# PURPOSE:
#open sockets between remote and station
#capture frame on remote
#send frame from remote to station

#import the necessary things for Socket
import sys, socket
# import the necessary things for OpenCV
import cv
#this is important for capturing/displaying images
from opencv import highgui
import pygame
import Image
from pygame.locals import *

#capture a frame
camera = highgui.cvCreateCameraCapture(0)

def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im)

fps = 30.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("WebCam Demo")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)
    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))



"""
#define variable
STATIONIP = '127.0.0.1'      #IP of the station's IP
CPORT = 12345                #port to handle commands           
DPORT = 12346                #port to handle data

#create socket
filename_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect to station
filename_tcp.connect((HOST, CPORT))
#send file name
filename_tcp.send("SEND " + FILE)
#close port
filename_tcp.close()

data_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_tcp .connect((HOST, MPORT))

print "data port connected..."

f = open(FILE, "rb")
data = f.read()
f.close()

data_tcp.send(data)
data_tcp.close()
"""
