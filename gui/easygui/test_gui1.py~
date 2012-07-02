#!/usr/bin/env python

import easygui as eg
import sys
from img_processing_tools import *
#from PIL import Image
from PIL import ImageStat
import cv 
import time

if __name__=="__main__":
	loop = 1

	while loop == 1:
		#directory = eg.diropenbox(msg=None, title=None, default=None)
		#print directory
		filename = eg.fileopenbox(msg=None, title=None, default='*', filetypes=None)
		print filename	
		#img1 = cv.LoadImage(filename)
		img1 = Image.open(filename)
		if img1.size[0] <> 320 or img1.size[1] <> 240:
			print "Image is not right size. Resizing image...."
			img1 = img1.resize((320, 240))
			print "Resized to 320, 340"


		#img1 = Image.open(filename).convert('RGB').save('temp.gif')
		img1.save('temp.gif')
		print img1
		#cv.ShowImage("Frame1", img1)
		#time.sleep(1)
		#cv.WaitKey()
		#time.sleep(1)
		#cv.DestroyWindow("Frame1")
		#print "window destroyed"
		time.sleep(.5)
		#reply   = eg.buttonbox(msg,image=None,choices=choices)	
		reply =	eg.buttonbox(msg='Mow This?', title='Should I process ', choices=('Yes', 'No', 'Re-Snap', 'Quit'), image='temp.gif', root=None)
		#print "Press any key to continue....."
		print "calling i3"
		I3image = rgb2I3(img1)
		#cv.WaitKey()

	
		#print cam_img
		#cam_img.show()
		#choice = choicebox(msg, title, choices)
		# note that we convert choice to string, in case
		# the user cancelled the choice, and we got None.
		#eg.msgbox("You chose: " + str(reply), "Result")

		# data file schema
		# classID, next 256 integers are I3 greenband histogram, I3 sum, I3 sum2, I3 median, I3 mean, 
		# I3 variance, I3 Standard Deviation, I3 root mean square


		if reply == "Yes":
			#eg.msgbox("Going to mow....:")
			classID = "1"
			WriteMeterics(I3image, classID)
			

		if reply == "No":
			classID = "2"
			WriteMeterics(I3image, classID)

		if reply == "Quit":
			print "Quitting...."
			loop = 2

"""
	if reply == "Grab Frame":
		try:
			#img1 = cv.LoadImage(sys.argv[1],cv.CV_LOAD_IMAGE_GRAYSCALE)
			frame = grab_frame(0)
			#img1 = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
			#img1 = CVtoGray(frame)
			#cv.WaitKey()
			#img1 = CV_enhance_edge(img1)
			#cv.WaitKey()
			#img2 = cv.LoadImage(sys.argv[1],cv.CV_LOAD_IMAGE_GRAYSCALE)
			#img3 = cv.LoadImage(sys.argv[2],cv.CV_LOAD_IMAGE_GRAYSCALE)
			print "frame=", frame
			cv.ShowImage("Frame1", frame)
			cv.MoveWindow ('Frame1',50 ,50 )
		except:
			print "******* Could not open camera *******"
			frame = Image.open("1.grass10.jpg")
			#sys.exit(-1)
"""

