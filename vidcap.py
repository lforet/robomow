"""
Sometimes we may have (or want) to use the pygame interface to the camera, sometimes opencv, to avoid changing lots of code this camera class is a wrapper around the opencv code - making it look like pygames camera.
Brian Thorne - OLPC Hitlab Project 2009
"""

import opencv
import opencv.cv as cv
import opencv.highgui as hg
import conversionUtils

import pygame
from pygame.locals import QUIT, K_ESCAPE, KEYDOWN
from pygame import surfarray

opencv_camera = True

class Camera():
    """
    Simulate the pygame camera class using opencv for capturing.
    Takes one additional parameter than a pygame.camera.Camera object
    the imageType which is the return type required for any image requests.
    imagetype can be set as:
         'opencv' - this returns an opencv.CvMat object
         'pygame' - returns a pygame surface, if surface is passed in - it will try blit directly to it.
    """
    def __init__(self, device, size, mode, imageType='opencv'):
        self.imageType = imageType
        self.size = self.width, self.height = size
        self.device = device
  
        # todo: would be nice if this didn't make a whole lot of noise about firewire...
        self.capture = hg.cvCreateCameraCapture(self.device)

        # set the wanted image size from the camera
        hg.cvSetCaptureProperty (self.capture, hg.CV_CAP_PROP_FRAME_WIDTH, self.width)
        hg.cvSetCaptureProperty (self.capture, hg.CV_CAP_PROP_FRAME_HEIGHT, self.height)
    
    def get_image(self,surface=None,*argv,**argd):
        """
        Since we are using opencv there are some differences here.
        This function will return a cvmat by default (the quickest route from camera to your code)
        Or if pygame was specified a 3dpixel array
          - this can be blitted directly to a pygame surface
          - or can be converted to a surface array and returned to your pygame code.
        
        """
        if self.imageType == "pygame":
            try:
                surfarray.blit_array(surface,conversionUtils.cv2SurfArray(hg.cvQueryFrame(self.capture)))
                return surface
            except:
                return surfarray.make_surface(conversionUtils.cv2SurfArray(hg.cvQueryFrame(self.capture))).convert()
        return hg.cvQueryFrame(self.capture)

    def start(self):
        pass
        
    def stop(self):
        return hg.cvReleaseCapture(self.capture)
    
    def query_image(self):
        return True
    
def list_cameras():
    #return [0]  # Just use this line if errors occur
    cams = []
    for i in range(3):
        try:
            capture = hg.cvCreateCameraCapture( i )  # Must be a better way of doing this...
            if capture is not None:
                cams.append(i)
        except Exception, e:
            pass
        finally:
            hg.cvReleaseCapture(capture)
    return cams
       
        
def init():
    """
    Work out at this point what we will use...
    """
    pass

def opencvSnap(dev,size):
    """
    An example use of the "camera" taking a single picture frame using opencv's cvMat as the return method.
    """
    # First lets take a picture using opencv, and display it using opencv...
    cvWin = hg.cvNamedWindow( "Opencv Rendering and Capture", 0 )

    print("Opening device %s, with video size (%s,%s)" % (dev,size[0],size[1]))
    
    # creates the camera of the specified size and in RGB colorspace
    cam = Camera(dev, size, "RGB")
    a = cam.get_image()
    hg.cvShowImage ('Opencv Rendering and Capture', a)
    
    # close the capture stream to avoid problems later, should see the camera turn off
    hg.cvReleaseCapture(cam.capture)
    del cam
    
    # Wait for any key then clean up
    print("Press any key to continue")
    k = hg.cvWaitKey()
    hg.cvDestroyWindow("Opencv Rendering and Capture")
    
    
 
def pygameSnap(dev,size):
    """
    Another use, taking a single from the "camera" (ie using opencv) 
    and return the image as a pygame surface. Then we display it in pygame.
    """
    print("Opening device %s, with video size (%s,%s), in pygame mode (returns pygame surface)" % (dev,size[0],size[1]))
    
    # creates the camera of the specified size in pygame mode
    cam = Camera(dev, size, "RGB", imageType='pygame')

    display = pygame.display.set_mode( size, 0 )
    pygame.display.set_caption("Pygame Render, Opencv Capture")
    snapshot = cam.get_image()
    
    display.blit(snapshot, (0,0))
    cam.stop()
    del cam # Turn off the camera
        
    print("Press escape to continue")
    while(True):
        pygame.display.flip()
        e = pygame.event.poll()
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            break
    pygame.quit()

def pygameSnap2(dev,size):
    """
    This time we get the image blitted directly to an existing surface.
    """
    print("Opening device %s, with video size (%s,%s), in pygame mode (returns pygame surface)" % (dev,size[0],size[1]))
    
    # creates the camera of the specified size in pygame mode
    cam = Camera(dev, size, "RGB", imageType='pygame')

    display = pygame.display.set_mode( size, 0 )
    pygame.display.set_caption("Pygame Render, Opencv Capture, Direct Blit")
    snapshot = cam.get_image()  # We will get a first frame to use as our surface to direct blit to.

    
    snapshot = cam.get_image(snapshot)  # This time it should have blitted direct to snapshot
    display.blit(snapshot, (0,0))
    cam.stop()
    del cam # Turn off the camera
        
    print("Press escape to continue")
    while(True):
        pygame.display.flip()
        e = pygame.event.poll()
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            break
    pygame.quit()
    

if __name__ == "__main__":
    init()
    print("""
    Running some opencv camera tests. You should see 3 seperate images, one after the other.
    Press any key after each image.
    """)
    clist = list_cameras()
    if not clist:
        raise ValueError("Sorry, no cameras detected.")
    
    dev = clist[0]
    size = (640,480)
    
    opencvSnap(dev,size)
    
    pygameSnap(dev,size)

    pygameSnap2(dev,size)

