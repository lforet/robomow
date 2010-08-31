#!/usr/bin/python

import sys, time
from opencv import cv
from opencv import highgui

hmin = 4
hmax = 18

highgui.cvNamedWindow('Camera', highgui.CV_WINDOW_AUTOSIZE)
#highgui.cvNamedWindow('Hue', highgui.CV_WINDOW_AUTOSIZE)
#highgui.cvCreateTrackbar("hmin Trackbar","Hue",hmin,180, change_hmin);
#highgui.cvCreateTrackbar("hmax Trackbar","Hue",hmax,180, change_hmax);

print "grabbing camera"
capture = highgui.cvCreateCameraCapture(0)
print "found camera"
time.sleep(1)
frame = highgui.cvQueryFrame(capture)
frameSize = cv.cvGetSize(frame)
print "frameSize =", frameSize
time.sleep(1)
cam_width = highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_WIDTH)
cam_height = highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_HEIGHT)
print "camers cam_height =", cam_height
print "camers cam_width =", cam_width

highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_WIDTH, 320)
highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_HEIGHT, 240)
time.sleep(1)
cam_width = highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_WIDTH)
cam_height = highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_HEIGHT)
print "camers cam_height =", cam_height
print "camers cam_width =", cam_width
print highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_PROP_FPS)
print highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_PROP_BRIGHTNESS)
#print highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_CONTRAST )
print highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_PROP_SATURATION )
print highgui.cvGetCaptureProperty(capture,highgui.CV_CAP_PROP_HUE )



hue = cv.cvCreateImage(frameSize,8,1)


print frameSize

while 1:
   frame = highgui.cvQueryFrame(capture)

   #cv.cvCvtColor(frame, hsv, cv.CV_BGR2HSV)        
   #cv.cvInRangeS(hsv,hsv_min,hsv_max,mask)
   #cv.cvSplit(hsv,hue,satuation,value,None)

   #cv.cvInRangeS(hue,hmin,hmax,hue)
   highgui.cvShowImage('Camera',frame)
   #highgui.cvShowImage('Hue',hue)

   highgui.cvWaitKey(10)
"""
double cvGetCaptureProperty(CvCapture* capture, int property_id)

    Gets video capturing properties.
    Parameters:	
        * capture-video capturing structure.
        * property-id
          Property identifier. Can be one of the following:
              * CV_CAP_PROP_POS_MSEC - Film current position in milliseconds or video capture timestamp
              o CV_CAP_PROP_POS_FRAMES - 0-based index of the frame to be decoded/captured next
              o CV_CAP_PROP_POS_AVI_RATIO - Relative position of the video file (0 - start of the film, 1 - end of the film)
              o CV_CAP_PROP_FRAME_WIDTH - Width of the frames in the video stream
              o CV_CAP_PROP_FRAME_HEIGHT - Height of the frames in the video stream
              o CV_CAP_PROP_FPS - Frame rate
              o CV_CAP_PROP_FOURCC - 4-character code of codec
              o CV_CAP_PROP_FRAME_COUNT - Number of frames in the video file
              o CV_CAP_PROP_BRIGHTNESS - Brightness of the image (only for cameras)
              o CV_CAP_PROP_CONTRAST - Contrast of the image (only for cameras)
              o CV_CAP_PROP_SATURATION - Saturation of the image (only for cameras)
              o CV_CAP_PROP_HUE - Hue of the image (only for cameras)
"""
