#!/usr/bin/python

import sys
from opencv import cv
from opencv import highgui

hmin = 4
hmax = 18

highgui.cvNamedWindow('Camera', highgui.CV_WINDOW_AUTOSIZE)
highgui.cvNamedWindow('Hue', highgui.CV_WINDOW_AUTOSIZE)
highgui.cvCreateTrackbar("hmin Trackbar","Hue",hmin,180, change_hmin);
highgui.cvCreateTrackbar("hmax Trackbar","Hue",hmax,180, change_hmax);

print "grabbing camera"
capture = highgui.cvCreateCameraCapture(0)
print "found camera"
highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_WIDTH, 320)
highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_HEIGHT, 240)

frame = highgui.cvQueryFrame(capture)
frameSize = cv.cvGetSize(frame)

hue = cv.cvCreateImage(frameSize,8,1)


print frameSize

while 1:
   frame = highgui.cvQueryFrame(capture)

   cv.cvCvtColor(frame, hsv, cv.CV_BGR2HSV)        
   #cv.cvInRangeS(hsv,hsv_min,hsv_max,mask)
   cv.cvSplit(hsv,hue,satuation,value,None)

   cv.cvInRangeS(hue,hmin,hmax,hue)
   highgui.cvShowImage('Camera',frame)
   highgui.cvShowImage('Hue',hue)

   highgui.cvWaitKey(10)

