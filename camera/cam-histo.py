#! /usr/bin/env python

import sys

# import the necessary things for OpenCV
from CVtypes import cv

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
hsv_min = cv.Scalar (0, smin, vmin, 0)
hsv_max = cv.Scalar (180, 256, vmax, 0)

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
    sector = int (hue)
    p = int(round (255 * (hue - sector)))
    if sector & 1:
        p ^= 255

    rgb = {}
    rgb [sector_data [sector][0]] = 255
    rgb [sector_data [sector][1]] = 0
    rgb [sector_data [sector][2]] = p

    return cv.Scalar (rgb [2], rgb [1], rgb [0], 0)

#############################################################################
# so, here is the main part of the program

if __name__ == '__main__':

    # a small welcome
    print "OpenCV Python wrapper test"
    print "OpenCV version: %s (%d, %d, %d)" % (cv.VERSION,
                                               cv.MAJOR_VERSION,
                                               cv.MINOR_VERSION,
                                               cv.SUBMINOR_VERSION)

    # first, create the necessary windows
    cv.NamedWindow ('Camera', cv.WINDOW_AUTOSIZE)
    cv.NamedWindow ('Histogram', cv.WINDOW_AUTOSIZE)

    # move the new window to a better place
    cv.MoveWindow ('Camera', 10, 40)
    cv.MoveWindow ('Histogram', 10, 270)

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
        capture = cv.CreateCameraCapture (device)

        # set the wanted image size from the camera
        cv.SetCaptureProperty (capture,
                                      cv.CAP_PROP_FRAME_WIDTH, 320)
        cv.SetCaptureProperty (capture,
                                      cv.CAP_PROP_FRAME_HEIGHT,240)
    else:
        # we have an argument on the command line,
        # we can assume this is a file name, so open it
        capture = cv.CreateFileCapture (sys.argv [1])            

    # check that capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit (1)
        
    # create an image to put in the histogram
    histimg = cv.CreateImage (cv.Size (320,240), 8, 3)

    # init the image of the histogram to black
    cv.SetZero (histimg)

    # capture the 1st frame to get some propertie on it
    frame = cv.QueryFrame (capture)

    # get some properties of the frame
    frame_size = cv.GetSize (frame)

    # compute which selection of the frame we want to monitor
    selection = cv.Rect (0, 0, frame_size.width, frame_size.height)

    # create some images usefull later
    hue = cv.CreateImage (frame_size, 8, 1)
    mask = cv.CreateImage (frame_size, 8, 1)
    hsv = cv.CreateImage (frame_size, 8, 3 )

    # create the histogram
    hist = cv.CreateHist (1, [hdims], cv.HIST_ARRAY, hranges, 1)

    while 1:
        # do forever

        # 1. capture the current image
        frame = cv.QueryFrame (capture)
        if frame is None:
            # no image captured... end the processing
            break

        # mirror the captured image
        cv.Flip (frame, None, 1)

        # compute the hsv version of the image 
        cv.CvtColor (frame, hsv, cv.BGR2HSV)

        # compute which pixels are in the wanted range
        cv.InRangeS (hsv, hsv_min, hsv_max, mask)

        # extract the hue from the hsv array
        cv.Split (hsv, hue, None, None, None)

        # select the rectangle of interest in the hue/mask arrays
        cv.SetImageROI(hue, selection)
        cv.SetImageROI(mask, selection)

        # it's time to compute the histogram
        cv.CalcHist ([hue], hist, 0, mask)

        # clear the ROIs
        cv.ResetImageROI(hue)
        cv.ResetImageROI(mask)

        # extract the min and max value of the histogram
        min_val, max_val, min_ndx, max_ndx = cv.GetMinMaxHistValue (hist)

        # compute the scale factor
        if max_val > 0:
            scale = 255. / max_val
        else:
            scale = 0.

        # scale the histograms
        cv.ConvertScale (hist[0].bins, hist[0].bins, scale, 0)

        # clear the histogram image
        cv.SetZero (histimg)

        # compute the width for each bin do display
        bin_w = histimg[0].width / hdims
        
        for  i in range (hdims):
            # for all the bins

            # get the value, and scale to the size of the hist image
            val = int(round (cv.GetReal1D (hist[0].bins, i)
                              * histimg[0].height / 255))

            # compute the color
            color = hsv2rgb (i * 180. / hdims)

            # draw the rectangle in the wanted color
            cv.Rectangle (histimg,
                            cv.Point (i * bin_w, histimg[0].height),
                            cv.Point ((i + 1) * bin_w, histimg[0].height - val),
                            color, -1, 8, 0)

        # we can now display the images
        cv.ShowImage ('Camera', frame)
        cv.ShowImage ('Histogram', histimg)

        # handle events
        k = cv.WaitKey (10)

        if k == 0x1b:
            # user has press the ESC key, so exit
            break
