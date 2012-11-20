#!/usr/bin/env python
import serial
import sys, time
from threading import Thread
import numpy as np
import matplotlib.cm as cm
from matplotlib.pyplot import figure, show, rc
import matplotlib.pyplot as P
from pylab import *
import Image
import cv
from maxsonar_class import *


###########################################################

def CVtoPIL_4Channel(CV_img):
	"""converts CV image to PIL image"""
	cv_img = cv.CreateMatHeader(cv.GetSize(img)[1], cv.GetSize(img)[0], cv.CV_8UC1)
	#cv.SetData(cv_img, pil_img.tostring())
	pil_img = Image.fromstring("L", cv.GetSize(img), img.tostring())
	return pil_img
###########################################################



###########################################################

def PILtoCV_4Channel(PIL_img):
	cv_img = cv.CreateImageHeader(PIL_img.size, cv.IPL_DEPTH_8U, 4)
	cv.SetData(cv_img, PIL_img.tostring())
	return cv_img

###########################################################

def fig2img ( fig ):
	# put the figure pixmap into a numpy array
	buf = fig2data ( fig )
	w, h, d = buf.shape
	fig_return = Image.fromstring( "RGBA", ( w ,h ), buf.tostring( ) )
	buf = 0
	return fig_return

###########################################################

def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf
###########################################################


def process_sonar_data(sonar_data):
	#global sensor1
	#data  = str(sensor1.distances_cm())
	data = sonar_data
	print "sonar data from inside sonar_functions", sonar_data
	if len(data) > 1:
		#print "data=", data
		#s1_data = re.search('s1', data)
		#print s1_data.span()
		s1_data = int(data[(data.find('s1:')+3):(data.find('s2:'))])
		s2_data = int(data[(data.find('s2:')+3):(data.find('s3:'))])
		s3_data = int(data[(data.find('s3:')+3):(data.find('s4:'))])
		s4_data = int(data[(data.find('s4:')+3):(data.find('s5:'))])
		s5_data = int(data[(data.find('s5:')+3):(len(data))])
		print s1_data, s2_data, s3_data, s4_data, s5_data 
		data2 = []
		data2.append(s1_data)
		data2.append(s2_data)
		data2.append(s3_data)
		data2.append(s4_data)
		data2.append(s5_data)
		#s1_data = int(s1_data)
		#if s1_data > 91: s1_data = 91
		#if s1_data < 0: s1_data = 0
		#print "s1:", s1_data
		#sonar_img = sonar_graph(data2)
		return data2
		#time.sleep(.01)


if __name__== "__main__":

	#t = Thread(target=sonar_display)
	#t.start()

	sensor1 = MaxSonar()
	time.sleep(1)
	sonar_display(sensor1)
	time.sleep(1)

	for i in range(1000):
		sonar_display(sensor1)
		time.sleep(0.01)

