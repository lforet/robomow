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

def sonar_graph(ping_reading):

	# force square figure and square axes looks better for polar, IMO
	fig = figure(figsize=(6,6))
	#ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
	ax = P.subplot(1, 1, 1, projection='polar')
	#ax = fig.add_subplot(2, 2, 2, projection='radar')
	P.rgrids([28, 61, 91])
 	#circle = P.Circle((0, 0), 50)
	#ax.add_artist(circle)	

	ax.set_theta_zero_location('N')
	ax.set_theta_direction(-1)
	x = 1
	theta = 0
	angle = theta * np.pi / 180.0
	radii = [ping_reading]
	width = .15
	bars1 = ax.bar(0, 100, width=0.001, bottom=0.0)
	#print "theta, radii, width: ", theta, radii, width
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
	
	#for r,bar in zip(radii, bars):
#	bar.set_facecolor( cm.jet(r/10.))
#		bar.set_alpha(1)

	pil_img = fig2img(fig)
	#sonar_image = PILtoCV_4Channel(pil_img)
	sonar_image = pil_img 
	#print type(ax)
	#print type(fig)
	#print type(pil_img)
	#print type(sonar_image)

	#cv.ShowImage("Sonar", sonar_image )
	#cv.MoveWindow ('Sonar',50 ,50 )
	#time.sleep(.01)
	#cv.WaitKey(2)
	#print "finished graph"
	
	#garbage cleanup
	#fig.clf()
	#P.close()
	print sonar_image
	return sonar_image


def sonar_display(sonar_data):
	#global sensor1
	#data  = str(sensor1.distances_cm())
	data = sonar_data
	print "sonar data from inside sonar_functions", sonar_data
	if len(data) > 1:
		#print "data=", data
		#s1_data = re.search('s1', data)
		#print s1_data.span()
		s1_data = data[(data.find('s1:')+3):(data.find('s2:'))]
		s2_data = data[(data.find('s2:')+3):(data.find('s3:'))]
		s3_data = data[(data.find('s3:')+3):(data.find('s4:'))]
		s4_data = data[(data.find('s4:')+3):(data.find('s5:'))]
		s5_data = data[(data.find('s5:')+3):(len(data)-1)]
		#print s1_data, s2_data, s3_data, s4_data, s5_data 
		s1_data = int(s1_data)
		if s1_data > 91: s1_data = 91
		if s1_data < 0: s1_data = 0
		print "s1:", s1_data
		sonar_img = sonar_graph(s1_data)
		return sonar_img
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

