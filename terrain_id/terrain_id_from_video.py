#!/usr/bin/env python

import os
from img_processing_tools import *
import Image, ImageDraw
import time
import sys
import cv, cv2
from PIL import ImageStat
import numpy as np


def grab_frame_from_video(video):
	frame = video.read()
	
	#counter = 0
	#while video.grab():
	#	    counter += 1
	#	    flag, frame = video.retrieve()
	#	    if flag:
		            #gray_frm = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		            #cv2.imwrite('frame_'+str(counter)+'.png',gray_frm)
					#cv.ShowImage("Video",frame)
					#cv2.imshow("Video",frame)
					#cv.WaitKey(1000/fps)
	return frame
				


def classifiy_section(img):
	#class_ID: 1=grass, 2=non-mowable, 3=unknown
	class_ID = 2
	#print img[0], img[1], img[2]
	#print "class_ID", class_ID
	#if (img[0] > 65 and img[0] < 115) and (img[1] > 70 and img[1] < 135) and (img[2] < 85):	class_ID = 1
	#if img[0] > 82 and img[1] > 85 and img[2] > 72:	class_ID = 2	
	
	rb_sum = img[0] + img[2]
	g_sum = img[1]
	if img[1] > 26: class_ID=1

	#if img[1] < 15 and img[2] > 5 : class_ID=2
	#print "rgb: ", img, "class_ID: ", class_ID
	return class_ID


def rgb2I3 (img):
	"""Convert RGB color space to I3 color space
	@param r: Red
	@param g: Green
	@param b: Blue
	return (I3) integer 
	"""
	img_width, img_height = img.size
	#make a copy to return
	returnimage = Image.new("RGB", (img_width, img_height))
	imagearray = img.load()
	for y in range(0, img_height, 1):					
		for x in range(0, img_width, 1):
			rgb = imagearray[x, y]
			i3 = ((2*rgb[1])-rgb[0]-rgb[2]) / 2
			#print rgb, i3
			returnimage.putpixel((x,y), (0,i3,0))
	return returnimage



def subsection_image(pil_img, sections, visual):
	sections = sections /4
	#print "sections= ", sections
	fingerprint = []

	# - -----accepts image and  number of sections to divide the image into (resolution of fingerprint)
	# ---------- returns a subsectioned image classified by terrain type
	img_width, img_height = pil_img.size
	#print "image size = img_wdith= ", img_width, "  img_height=", img_height, "  sections=", sections
	if visual == True:
		cv_original_img1 = PILtoCV(pil_img)
		cv.ShowImage("Original",cv_original_img1 )
		cv.MoveWindow("Original", ((img_width)+100),50)
	pil_img = rgb2I3 (pil_img)
	#cv.WaitKey()
	temp_img = pil_img.copy()
	xsegs = img_width  / sections
	ysegs = img_height / sections
	#print "xsegs, ysegs = ", xsegs, ysegs 
	for yy in range(0, img_height-ysegs+1 , ysegs):
		for xx in range(0, img_width-xsegs+1, xsegs):
			#print "Processing section =", xx, yy, xx+xsegs, yy+ysegs
			box = (xx, yy, xx+xsegs, yy+ysegs)
			#print "box = ", box
			cropped_img1 = pil_img.crop(box)
			I3_mean =   ImageStat.Stat(cropped_img1).mean
			I3_mean_rgb = (int(I3_mean[0]), int(I3_mean[1]), int(I3_mean[2]))
			#print "I3_mean: ", I3_mean
			sub_ID = classifiy_section(I3_mean_rgb)
			fingerprint.append(sub_ID)
			if visual == True:
				cv_cropped_img1 = PILtoCV(cropped_img1)
				cv.ShowImage("Fingerprint",cv_cropped_img1 )
				cv.MoveWindow("Fingerprint", (img_width+100),50)
				if sub_ID == 1: I3_mean_rgb = (50,150,50)
				if sub_ID == 2: I3_mean_rgb = (150,150,150)
				if sub_ID == 3: I3_mean_rgb = (0,0,200)
				ImageDraw.Draw(pil_img).rectangle(box, (I3_mean_rgb))
				cv_img = PILtoCV(pil_img)
				cv.ShowImage("Image",cv_img)
				cv.MoveWindow("Image", 50,50)
				cv.WaitKey(10)
				#print xx*yy
				#time.sleep(.05)
	
	#print "FINGERPRINT: ", fingerprint
	#cv.WaitKey()
	return fingerprint

###########################################################

def direction_I3_sum(pil_img):
	pil_img = rgb2I3 (pil_img)
	center_size = .20	
	
	#returns which direction based on sum of I3 total per side (L or R)
	img_width, img_height = pil_img.size
	left_box = (0, 0, img_width/2, img_height )
	right_box = (img_width/2, 0, img_width, img_height )
	center_box = (int( (img_width/2) - (img_width*(center_size/2))), 0, int( (img_width/2) + (img_width*(center_size/2))), img_height ) 
	#print 'center_box'  , center_box
	#print "box1, box2, center_box ", box1, box2, center_box
	cropped_left_img = pil_img.crop(left_box)
	cropped_right_img = pil_img.crop(right_box) 
	cropped_center_img = pil_img.crop(center_box) 

	c_img_width, c_img_height = cropped_center_img.size
	center_left_box = (0, 0, c_img_width/2, c_img_height )
	center_right_box = (c_img_width/2, 0, c_img_width, c_img_height )

	l_center_img = cropped_center_img.crop(center_left_box) 
	r_center_img = cropped_center_img.crop(center_right_box) 
	#print l_center_img, r_center_img , cropped_center_img
	cv_img = PILtoCV(cropped_left_img)
	cv.ShowImage("Left",cv_img)
	cv.MoveWindow("Left", 2*(img_width)+60,0)
	#cv.WaitKey(25)
	cv_img = PILtoCV(cropped_right_img)
	cv.ShowImage("Right",cv_img)
	cv.MoveWindow("Right", 2*(img_width)+60+img_width/2,0)
	#cv.WaitKey(25)
	cv_img = PILtoCV(cropped_center_img)
	cv.ShowImage("Center",cv_img)
	cv.MoveWindow("Center", 2*(img_width)+60+img_width,0)
	#cv.WaitKey()
	cv_img = PILtoCV(l_center_img)
	cv.ShowImage("LCenter",cv_img)
	cv.MoveWindow("LCenter",2*(img_width)+60+img_width+c_img_width,0)
	cv_img = PILtoCV(r_center_img)
	cv.ShowImage("RCenter",cv_img)
	cv.MoveWindow("RCenter",2*(img_width)+60+img_width+(c_img_width)+c_img_width/2,0)

	I3_sum = ImageStat.Stat(pil_img).sum[1]	
	I3_sum_left = ImageStat.Stat(cropped_left_img ).sum[1]	
	I3_sum_right =ImageStat.Stat(cropped_right_img ).sum[1]	
	I3_center_sum = ImageStat.Stat(cropped_center_img).sum[1]
	I3_sum_cleft_g =   ImageStat.Stat(l_center_img).sum[1]
	I3_sum_cright_g =  ImageStat.Stat(r_center_img).sum[1]

	print 'I3_sum_left, I3_sum_right, I3_center_sum : ' , I3_sum_cleft_g , I3_sum_cright_g,I3_center_sum 
	#percent =  int(I3_sum_left_g/(I3_sum_left_g+I3_sum_right_g ) * 100)
	l_percent = I3_sum_cleft_g / I3_center_sum
	r_percent = I3_sum_cright_g / I3_center_sum 
	print 'l_percent, r_percent, I3_center_sum: ', l_percent, r_percent, I3_center_sum
	#cv.WaitKey()
	
	thres1=.55
	if I3_center_sum > 50000 and ( l_percent > thres1 or r_percent > thres1):
		
		print "................ ON EDGE ..............."
		cv.WaitKey(250)
		thres1 = .50
		thres2 = .90
		thres3 = .96
		print 'I3_sum_cleft_g , (I3_center_sum * thres1):',I3_sum_cleft_g , (I3_center_sum * thres1)
		if I3_sum_cleft_g  > (I3_center_sum * thres1) and I3_sum_cleft_g  < (I3_center_sum * thres2): 
			print '.............turn right -> 50%-90%.............'
			cv.WaitKey()
			#side = "L"
		#if within 90-95 %continue forward
		if I3_sum_cleft_g  > (I3_center_sum * thres2) and I3_sum_cleft_g  < (I3_center_sum * thres3):
			print '.............continue foward -> within 90-95 %.............'
			cv.WaitKey()
		# if over 96% turn towards grass
		if  I3_sum_cleft_g  > (I3_center_sum * thres3):
			print '.............turn left -> over 96%.............'
			cv.WaitKey()
		# if over 96% turn towards grass
		if  I3_sum_cright_g  > (I3_center_sum * thres3):
			print '.............turn right -> over 96%.............'
			cv.WaitKey()
		#if I3_sum_cright_g  > (I3_center_sum * thres2):
		#	print '.............turn left.............edge on left'
		#	cv.WaitKey()
		#side = "R"
	else:

		print "................ NOT ON EDGE so ????????????????"
	'''
	#is there enough data
	if I3_center_sum > 100000:
		print "continue foward"
	else:
		if I3_sum_cleft_g > I3_sum_cright_g:
			print "turn left"
			cv.WaitKey(1000)
		if I3_sum_cleft_g < I3_sum_cright_g:
			print "turn right"
			cv.WaitKey(1000)
	'''	
	

	#i think this!!
	thres2 = .55
	print I3_sum_cleft_g , (I3_center_sum * thres2)/2
	if l_percent < thres2 and r_percent < thres2:
		print "too much grass...maybe in a field away from edge"

		if I3_sum_left < I3_sum_right:
			print "turn left toward edge"
		else:
			print "turn right toward edge"
		cv.WaitKey(10)

	thres3 = 150000
	print I3_sum_cleft_g
	if I3_center_sum < thres3:
		print "too much non-grass...maybe on non-mowing suface"

		if I3_sum_left > I3_sum_right:
			print "turn left toward grass"
		else:
			print "turn right toward grass"
		cv.WaitKey(10)
	print
	cv.WaitKey(5)


if __name__=="__main__":
	video = cv2.VideoCapture(sys.argv[1])
	while 1:
	 	 
	#	if len(sys.argv) < 4:
	#		print "******* Requires 3 image files of the same size."
	#		print "This program will return the angle at which the second is in relation to the first. ***"
	#		sys.exit(-1)

		try:
			#img1 = cv.LoadImage(sys.argv[1])
			#frame = grab_frame(1)
			
			img1 = np.array(grab_frame_from_video(video)[1])
			cv.NamedWindow("Video",cv.CV_WINDOW_AUTOSIZE)
			cv2.imshow("Video",img1)
		except:
			print "******* Could not open image/video file *******"
			sys.exit(-1)
		#print len (sys.argv)

		if len(sys.argv) == 2:
			resolution = 32
		else:
			resolution = int(sys.argv[2])

		img1 = array2image(img1)
		img1 = img1.resize((320,240))
		direction_I3_sum(img1)

		"""
		image_fingerprint = np.array(subsection_image(img1, resolution, False))
		#print "FINGERPRINT: ",image_fingerprint
		#print 'len(image_fingerprint):', len(image_fingerprint)
		#image_fingerprint.reshape(((image_fingerprint/2), 2))
		#print image_fingerprint 
		step = len(image_fingerprint)/ (resolution/4)
		#print "step =", step
		a = []
		b = []
		for x in range (0, len(image_fingerprint), step):
			#print x
			for y in range(0, step/2):
				#print x,y
				a.append(image_fingerprint[(x+y)])
				b.append(image_fingerprint[(x+(step/2)+y)])
				#print a
				#print b

		direction = sum(a)-sum(b)
		total_sum = sum(a)+sum(b)
		limit = int(2*(len(image_fingerprint) * .95))
		print "leftside-rightside:", direction , '  total sum:', total_sum, '  limit: ', limit
		#if direction > -5 :
		#	print "turn right"
		#	cv.WaitKey(600)
		#if direction < -55: 
		#	print "turn left"
		#	cv.WaitKey(500)
		if direction < -55: 
		#	print "turn left"
		#	cv.WaitKey(500)	
		if total_sum > limit:
			print "not enough data to continue mowing"
			cv.WaitKey()
		cv.WaitKey(20)
		"""
