from VideoCapture import Device
import ImageDraw, sys, pygame, time
from pygame.locals import *
from PIL import ImageEnhance
res = (640,480)
pygame.init()
cam = Device()
cam.setResolution(res[0],res[1])
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('Webcam')
pygame.font.init()
font = pygame.font.SysFont("Courier",11)

def disp(phrase,loc):
    s = font.render(phrase, True, (200,200,200))
    sh = font.render(phrase, True, (50,50,50))
    screen.blit(sh, (loc[0]+1,loc[1]+1))
    screen.blit(s, loc)
brightness = 1.0
contrast = 1.0
shots = 0

while 1:
    camshot = ImageEnhance.Brightness(cam.getImage()).enhance(brightness)
    camshot = ImageEnhance.Contrast(camshot).enhance(contrast)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    keyinput = pygame.key.get_pressed()
    if keyinput[K_1]: brightness -= .1
    if keyinput[K_2]: brightness += .1
    if keyinput[K_3]: contrast -= .1
    if keyinput[K_4]: contrast += .1
    if keyinput[K_q]: cam.displayCapturePinProperties()
    if keyinput[K_w]: cam.displayCaptureFilterProperties()
    if keyinput[K_s]:
        filename = str(time.time()) + ".jpg"
        cam.saveSnapshot(filename, quality=80, timestamp=0)
        shots += 1 
    camshot = pygame.image.frombuffer(camshot.tostring(), res, "RGB")
    screen.blit(camshot, (0,0))
    disp("S:" + str(shots), (10,4))
    disp("B:" + str(brightness), (10,16))  
    disp("C:" + str(contrast), (10,28))
    pygame.display.flip()

