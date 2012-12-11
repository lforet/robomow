#!/usr/bin/env python

import easygui as eg
import sys
from img_processing_tools import *
#from PIL import Image
from PIL import ImageStat
import cv2 
import time
import mahotas
import Image


def snap_shot(filename):
	#capture from camera at location 0
	now = time.time()
	global webcam1
	try:
		#have to capture a few frames as it buffers a few frames..
		for i in range (5):
			ret, img = webcam1.read()		 
		print "time to capture 5 frames:", (time.time()) - now
		cv2.imwrite(filename, img)
		#img1 = Image.open(filename)
		#img1.thumbnail((320,240))
		#img1.save(filename)
		#print (time.time()) - now
	except:
		print "could not grab webcam"
	return img


if __name__=="__main__":
	loop = 1
	reply =""

	webcam1 = cv2.VideoCapture(0)

	while True:

		# data file schema
		# classID, next 256 integers are I3 greenband histogram, I3 sum, I3 sum2, I3 median, I3 mean, 
		# I3 variance, I3 Standard Deviation, I3 root mean square
		if reply == "":
			image = snap_shot('temp.png')

		if reply == "Mowable":
			#eg.msgbox("Going to mow....:")
			classID = "1"
			print "calling i3"
			I3image = rgb2I3(image)
			WriteMeterics(I3image, classID)
			
		if reply == "Non-Mowable":
			classID = "2"
			print "calling i3"
			I3image = rgb2I3(image)
			WriteMeterics(I3image, classID)

		if reply == "Test Img":	
			#im = Image.fromarray(image)
			#im.save("new.png")
			img1 = Image.open('temp.png')
			#img1.thumbnail((320,240))
			img1.save('new.png')

		if reply == "Quit":
			print "Quitting...."
			sys.exit(-1)

		if reply == "New Image":
			print "Acquiring new image.."
			image = snap_shot('temp.png')
			#print np.array(image)
			#print PIL2array(image)
			#lbp1 = mahotas.features.lbp(image , 1, 8, ignore_zeros=False)
			#print lbp1

		reply =	eg.buttonbox(msg='Classify Image', title='Robomow GUI', choices=('Mowable', 'Non-Mowable', 'Test Img', 'New Image', 'Quit'), image='temp.png', root=None)



