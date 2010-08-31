##
## Based on camshiftdemo.c
##

import sys
from opencv import cv
from opencv import highgui
import opencv

from myro import *

go = False

image = None
hsv = None
hue = None
mask = None
backproject = None
ist = None

backproject_mode = 0
select_object = 0
track_object = 0

origin = cv.CvPoint()
selection = cv.CvRect()
track_window = cv.CvRect()
track_box = cv.CvBox2D()
track_comp = cv.CvConnectedComp()

hdims = 16
hranges = [[0, 180]]
vmin = 60
vmax = 256
smin = 65

def on_mouse(event, x, y, flags, param):

    global select_object, selection, image, origin, select_object, track_object

    if image is None:
        return

    if image.origin:
        y = image.height - y

    if select_object:
        selection.x = min(x,origin.x)
        selection.y = min(y,origin.y)
        selection.width = selection.x + cv.CV_IABS(x - origin.x)
        selection.height = selection.y + cv.CV_IABS(y - origin.y)
        
        selection.x = max( selection.x, 0 )
        selection.y = max( selection.y, 0 )
        selection.width = min( selection.width, image.width )
        selection.height = min( selection.height, image.height )
        selection.width -= selection.x
        selection.height -= selection.y

    if event == highgui.CV_EVENT_LBUTTONDOWN:
        origin = cv.cvPoint(x,y)
        selection = cv.cvRect(x,y,0,0)
        select_object = 1
    elif event == highgui.CV_EVENT_LBUTTONUP:
        select_object = 0
        if( selection.width > 0 and selection.height > 0 ):
            track_object = -1

def out_values():
    print "vmin =", vmin, "vmax =", vmax, "smin =", smin

def set_vmin(value):
    global vmin
    vmin = value
    out_values()

def set_vmax(value):
    global vmax
    vmax = value
    out_values()
    
def set_smin(value):
    global smin
    smin = value
    out_values()


def hsv2rgb (hue):
    # convert the hue value to the corresponding rgb value

    sector_data = [[0, 2, 1],
                   [1, 2, 0],
                   [1, 0, 2],
                   [2, 0, 1],
                   [2, 1, 0],
                   [0, 1, 2]]
    hue *= 0.1 / 3
    sector = cv.cvFloor (hue)
    p = cv.cvRound (255 * (hue - sector))
    if sector & 1:
        p ^= 255

    rgb = {}
    rgb [sector_data [sector][0]] = 255
    rgb [sector_data [sector][1]] = 0
    rgb [sector_data [sector][2]] = p

    return cv.cvScalar (rgb [2], rgb [1], rgb [0], 0)


if __name__ == '__main__':

    # use the webcam
    capture = highgui.cvCreateCameraCapture (0)

    # check that capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit (1)
        
    # display a small howto use it
    print  "Hot keys: \n"
    print "\tESC - quit the program\n"
    print "\tc - stop the tracking\n"
    print "\tb - switch to/from backprojection view\n"
    print "To initialize tracking, select the object with mouse\n"

    # first, create the necessary windows
    highgui.cvNamedWindow ('VisualJoystick', highgui.CV_WINDOW_AUTOSIZE)

    # register the mouse callback
    highgui.cvSetMouseCallback ('VisualJoystick', on_mouse, None)
    
    highgui.cvCreateTrackbar( "Vmin", "VisualJoystick", vmin, 256, set_vmin)
    highgui.cvCreateTrackbar( "Vmax", "VisualJoystick", vmax, 256, set_vmax)
    highgui.cvCreateTrackbar( "Smin", "VisualJoystick", smin, 256, set_smin)


    if go:
        init()
        print getBattery()

    while True:

        frame = highgui.cvQueryFrame (capture)
            
        if frame is None:
            # no image captured... end the processing
            break

        if image is None:
            # create the images we need
            image = cv.cvCreateImage (cv.cvGetSize (frame), 8, 3)
            image.origin = frame.origin            
            hsv = cv.cvCreateImage( cv.cvGetSize(frame), 8, 3 )
            hue = cv.cvCreateImage( cv.cvGetSize(frame), 8, 1 )
            mask = cv.cvCreateImage( cv.cvGetSize(frame), 8, 1 )
            backproject = cv.cvCreateImage( cv.cvGetSize(frame), 8, 1 )
            hist = cv.cvCreateHist( [hdims], cv.CV_HIST_ARRAY, hranges, 1 )

        # flip the image
        cv.cvFlip (frame, image, 1)
        
        cv.cvCvtColor( image, hsv, cv.CV_BGR2HSV)

        cv.cvLine(image, cv.cvPoint(0, image.height/2), cv.cvPoint(image.width, image.height/2),
                  cv.CV_RGB(0,255,0), 2, 8, 0 )
        
        cv.cvLine(image, cv.cvPoint(image.width/2, 0), cv.cvPoint(image.width/2, image.height),
                  cv.CV_RGB(0,255,0), 2, 8, 0 )
        
        if track_object:
            _vmin = vmin
            _vmax = vmax

            cv.cvInRangeS( hsv,
                           cv.cvScalar(  0, smin,min(_vmin,_vmax),0),
                           cv.cvScalar(180, 256, max(_vmin,_vmax),0),
                           mask );

            cv.cvSplit( hsv, hue, None, None, None)

            if track_object < 0:
                max_val = 0.0                
                subhue = cv.cvGetSubRect(hue, selection)
                submask = cv.cvGetSubRect(mask, selection)
                cv.cvCalcHist( subhue, hist, 0, submask )
                
                # extract the min and max value of the histogram
                min_val, max_val, min_idx, max_idx = cv.cvGetMinMaxHistValue (hist)
                
                if (max_val):
                    cv.cvConvertScale( hist.bins, hist.bins, 255.0 / max_val, 0)
                else:
                    cv.cvConvertScale( hist.bins, hist.bins, 0.0, 0 )

                track_window = selection
                track_object = 1


            cv.cvCalcArrBackProject( hue, backproject, hist )
            
            cv.cvAnd( backproject, mask, backproject, 0 )
            cv.cvCamShift( backproject, track_window,
                           cv.cvTermCriteria( cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, 10, 1 ),
                           track_comp, track_box )
            track_window = track_comp.rect
            
            if backproject_mode:
                cv.cvCvtColor( backproject, image, cv.CV_GRAY2BGR )
            if not image.origin:
                track_box.angle = -track_box.angle

            cv.cvEllipseBox(image, track_box, cv.CV_RGB(255,0,0), 3, cv.CV_AA, 0)
            
            if (track_box.size.width > 10 or track_box.size.height  > 10):

                rotate = ( (image.width/2.0) - track_box.center.x) / (image.width/2.0)
                translate = ((image.height/2.0) - track_box.center.y) / (image.height/2.0)
                
                #print "rotate =", rotate, "translate =", translate
                
                if go:
                    move(translate, rotate)
        
        if select_object and selection.width > 0 and selection.height > 0:
            subimg = cv.cvGetSubRect(image, selection)
            cv.cvXorS( subimage, cv.cvScalarAll(255), subimage, 0 )

        highgui.cvShowImage( "VisualJoystick", image )

        c = highgui.cvWaitKey(10)
        if c == '\x1b':
            break        
        elif c == 'b':
            backproject_mode ^= 1
        elif c == 'c':
            track_object = 0
            cv.cvZero( histimg )
            if go:
                stop()

if go:
    stop()

