import pygame
import Image
import ImageDraw, time
from pygame.locals import *
import sys
from PIL import ImageEnhance
from opencv import cv
from opencv import highgui


import opencv
#this is important for capturing/displaying images
from opencv import highgui 

camera = highgui.cvCreateCameraCapture(0)
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im) 

res = (640,480)
pygame.init()
fps = 30.0
window = pygame.display.set_mode((res[0],res[1]))
#screen = pygame.display.set_mode((res[0],res[1]))
pygame.display.set_caption("WebCam Demo")
pygame.font.init()
font = pygame.font.SysFont("Courier",11)
screen = pygame.display.get_surface()

def disp(phrase,loc):
    s = font.render(phrase, True, (200,200,200))
    sh = font.render(phrase, True, (50,50,50))
    screen.blit(sh, (loc[0]+1,loc[1]+1))
    screen.blit(s, loc)
brightness = 1.0
contrast = 1.0
shots = 0

while True:
    #camshot = ImageEnhance.Brightness(camera.getImage()).enhance(brightness)
    #camshot = ImageEnhance.Contrast(camshot).enhance(contrast)
    camshot = get_image()
    for event in pygame.event.get():
        #if event.type == pygame.QUIT or event.type == KEYDOWN:
        if event.type == pygame.QUIT: sys.exit()
    keyinput = pygame.key.get_pressed()
    if keyinput[K_1]: brightness -= .1
    if keyinput[K_2]: brightness += .1
    if keyinput[K_3]: contrast -= .1
    if keyinput[K_4]: contrast += .1
    if keyinput[K_q]: camera.displayCapturePinProperties()
    if keyinput[K_w]: camera.displayCaptureFilterProperties()
    if keyinput[K_s]:
        filename = str(time.time()) + ".jpg"
        #camera.saveSnapshot(filename, quality=80, timestamp=0)
        cv.SaveImage("testcap.jpg", camshot)
        shots += 1 
    camshot = pygame.image.frombuffer(camshot.tostring(), res, "RGB")
    screen.blit(camshot, (0,0))
    disp("S:" + str(shots), (10,4))
    disp("B:" + str(brightness), (10,16))  
    disp("C:" + str(contrast), (10,28))
    pygame.display.flip()
            
    #im = get_image()
    #pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    #screen.blit(pg_img, (0,0))
    #pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))
