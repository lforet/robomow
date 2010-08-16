#! /usr/bin/env python

import sys
import functools
# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

#############################################################################
# definition of some constants

# how many bins we want for the histogram, and their ranges
hdims = 16
hranges = [[0, 180]]

# ranges for the limitation of the histogram
vmin = 10
vmax = 256
smin = 30

# the range we want to monitor
hsv_min = cv.cvScalar (0, smin, vmin, 0)
hsv_max = cv.cvScalar (180, 256, vmax, 0)

#############################################################################
# some useful functions

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

       
def on_mouse( event, x, y, flags, param = [] ):
    global mouse_selection
    global mouse_origin
    global mouse_select_object
    if event == highgui.CV_EVENT_LBUTTONDOWN:
        print("Mouse down at (%i, %i)" % (x,y))
        mouse_origin = cv.cvPoint(x,y)

        mouse_selection = cv.cvRect(x,y,0,0)
        mouse_select_object = True
        return
    if event == highgui.CV_EVENT_LBUTTONUP:
        print("Mouse up at (%i,%i)" % (x,y))
        mouse_select_object = False
        if( mouse_selection.width > 0 and mouse_selection.height > 0 ):
            global track_object
            track_object = -1
        return
    if mouse_select_object:
        mouse_selection.x = min(x,mouse_origin.x)
        mouse_selection.y = min(y,mouse_origin.y)
        mouse_selection.width = mouse_selection.x + cv.CV_IABS(x - mouse_origin.x)
        mouse_selection.height = mouse_selection.y + cv.CV_IABS(y - mouse_origin.y)
        mouse_selection.x = max( mouse_selection.x, 0 )
        mouse_selection.y = max( mouse_selection.y, 0 )
        mouse_selection.width = min( mouse_selection.width, frame.width )
        mouse_selection.height = min( mouse_selection.height, frame.height )
        mouse_selection.width -= mouse_selection.x
        mouse_selection.height -= mouse_selection.y
   

#############################################################################
# so, here is the main part of the program

if __name__ == '__main__':

    print "OpenCV Python wrapper test"
    #print "OpenCV version: %s (%d, %d, %d)" % (cv.CV_VERSION,
    #                                           cv.CV_MAJOR_VERSION,
    #                                           cv.CV_MINOR_VERSION,
    #                                           cv.CV_SUBMINOR_VERSION)

    # first, create the necessary windows
    highgui.cvNamedWindow ('Camera', highgui.CV_WINDOW_AUTOSIZE)
    highgui.cvNamedWindow ('Histogram', highgui.CV_WINDOW_AUTOSIZE)

    # move the new window to a better place
    highgui.cvMoveWindow ('Camera', 10, 40)
    highgui.cvMoveWindow ('Histogram', 10, 270)


    global mouse_origin
    global mouse_selection
    global mouse_select_object
    mouse_select_object = False
    global track_object
    track_object = 0
   
    global track_comp
    global track_box
   
    track_comp = cv.CvConnectedComp()
    track_box = cv.CvBox2D()
           
    highgui.cvSetMouseCallback( "Camera", on_mouse, 0 )
   
   
    try:
        # try to get the device number from the command line
        device = int (sys.argv [1])

        # got it ! so remove it from the arguments
        del sys.argv [1]
    except (IndexError, ValueError):
        # no device number on the command line, assume we want the 1st device
        device = 0

    if len (sys.argv) == 1:
        # no argument on the command line, try to use the camera
        capture = highgui.cvCreateCameraCapture (device)

        # set the wanted image size from the camera
        highgui.cvSetCaptureProperty (capture,
                                      highgui.CV_CAP_PROP_FRAME_WIDTH, 1600)
        highgui.cvSetCaptureProperty (capture,
                                      highgui.CV_CAP_PROP_FRAME_HEIGHT, 1200)
    else:
        # we have an argument on the command line,
        # we can assume this is a file name, so open it
        capture = highgui.cvCreateFileCapture (sys.argv [1])            

    # check that capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit (1)
       
    # create an image to put in the histogram
    histimg = cv.cvCreateImage (cv.cvSize (320,240), 8, 3)

    # init the image of the histogram to black
    cv.cvSetZero (histimg)

    # capture the 1st frame to get some propertie on it
    frame = highgui.cvQueryFrame (capture)
   

   
    # get some properties of the frame
    frame_size = cv.cvGetSize (frame)

    # compute which selection of the frame we want to monitor
    selection = cv.cvRect (0, 0, frame.width, frame.height)

    # create some images usefull later
    hue = cv.cvCreateImage (frame_size, 8, 1)
    mask = cv.cvCreateImage (frame_size, 8, 1)
    hsv = cv.cvCreateImage (frame_size, 8, 3 )
    backproject = cv.cvCreateImage( frame_size, 8, 1 )

    # create the histogram
    hist = cv.cvCreateHist ([hdims], cv.CV_HIST_ARRAY, hranges, 1)
    obj_hist = cv.cvCreateHist ([hdims], cv.CV_HIST_ARRAY, hranges, 1)
    while 1:
        # do forever

        # 1. capture the current image
        frame = highgui.cvQueryFrame (capture)
        if frame is None:
            # no image captured... end the processing
            break

        # mirror the captured image
        #cv.cvFlip (frame, None, 1)

        # compute the hsv version of the image
        cv.cvCvtColor (frame, hsv, cv.CV_BGR2HSV)

        # compute which pixels are in the wanted range
        cv.cvInRangeS (hsv, hsv_min, hsv_max, mask)

        # extract the hue from the hsv array
        cv.cvSplit (hsv, hue, None, None, None)

        # select the rectangle of interest in the hue/mask arrays
        hue_roi = cv.cvGetSubRect (hue, selection)
        mask_roi = cv.cvGetSubRect (mask, selection)

        # it's time to compute the histogram
        cv.cvCalcHist (hue_roi, hist, 0, mask_roi)

        # extract the min and max value of the histogram
        min_val, max_val, min_idx, max_idx = cv.cvGetMinMaxHistValue (hist)


        # compute the scale factor
        if max_val > 0:
            scale = 255. / max_val
        else:
            scale = 0.

        # scale the histograms
        cv.cvConvertScale (hist.bins, hist.bins, scale, 0)

        # clear the histogram image
        cv.cvSetZero (histimg)

        # compute the width for each bin do display
        bin_w = histimg.width / hdims
       
        for  i in range (hdims):
            # for all the bins

            # get the value, and scale to the size of the hist image
            val = cv.cvRound (cv.cvGetReal1D (hist.bins, i)
                              * histimg.height / 255)

            # compute the color
            color = hsv2rgb (i * 180. / hdims)

            # draw the rectangle in the wanted color
            cv.cvRectangle (histimg,
                            cv.cvPoint (i * bin_w, histimg.height),
                            cv.cvPoint ((i + 1) * bin_w, histimg.height - val),
                            color, -1, 8, 0)
        # Make the sweet negative selection box
        if mouse_select_object and mouse_selection.width > 0 and mouse_selection.height > 0:
            a = cv.cvGetSubRect(frame,mouse_selection)
            cv.cvXorS(a,cv.cvScalarAll(255), a)   # Take the negative of the image..
            del a

        # Carry out the histogram tracking...
        if track_object != 0:            
            cv.cvInRangeS( hsv, cv.cvScalar(0,smin ,min(vmin, vmax), 0), cv.cvScalar(180, 256, max(vmin,vmax), 0), mask )
            cv.cvSplit(hsv, hue, None, None, None)
           
            if track_object < 0:
                # Calculate the histogram for the mouse_selection box
                hue_roi_rect = cv.cvGetSubRect( hue, mouse_selection )
                mask_roi_rect = cv.cvGetSubRect( mask, mouse_selection )
                cv.cvCalcHist (hue_roi_rect, obj_hist, 0, mask_roi_rect)
                min_val, max_val, min_idx, max_idx = cv.cvGetMinMaxHistValue (obj_hist)
               
                track_window = mouse_selection
                track_object = 1
               
            cv.cvCalcBackProject( hue, backproject, obj_hist )
            cv.cvAnd(backproject, mask, backproject)

            #niter, track_comp, track_box =
            cv.cvCamShift( backproject, track_window,
                    cv.cvTermCriteria( cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, 10, 1 ), track_comp, track_box)
            track_window = track_comp.rect
           
            #if backproject_mode:
            #    cvCvtColor( backproject, image, CV_GRAY2BGR )
           
            if not frame.origin:
                track_box.angle = -track_box.angle
            cv.cvEllipseBox( frame, track_box, cv.CV_RGB(255,0,0), 3, cv.CV_AA, 0 )

       
        # we can now display the images
        highgui.cvShowImage ('Camera', frame)
        highgui.cvShowImage ('Histogram', histimg)

        # handle events
        k = highgui.cvWaitKey (10)

        if k == '\x1b':
            # user has press the ESC key, so exit
            break
    highgui.cvReleaseCapture(capture)

