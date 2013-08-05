#!/usr/bin/env python
#!/usr/bin/python

import sys
sys.path.append( "../lib/" )

import easygui as eg
from img_processing_tools import *
#from PIL import Image
from PIL import ImageStat, Image, ImageDraw
import cv, cv2 
import time
import mahotas
import numpy as np
import pickle
import csv
import milk
from threading import *

def snap_shot():
	#capture from camera at location 0
	now = time.time()
	webcam1 = None
	try:
		while webcam1 == None:
			webcam1 = cv2.VideoCapture(1)
			time.sleep(.1)
			#webcam1 = cv.CreateCameraCapture(1)
	except:
		print "******* Could not open WEBCAM *******"
		print "Unexpected error:", sys.exc_info()[0]
		#raise		
		#sys.exit(-1)
	try:
		#have to capture a few frames as it buffers a few frames..
		for i in range (5):
			ret, img = webcam1.read()
			#img = cv.QueryFrame(webcam1)		 
		#print "time to capture 5 frames:", (time.time()) - now
		#cv2.imwrite(filename, img)
		#img1 = Image.open(filename)
		#img1.thumbnail((320,240))
		#img1.save(filename)
		#print (time.time()) - now
		webcam1.release()
		return img
	except:
		print "could not grab webcam" 


def find_features(img):
	#print type(img), img.size, img.shape

	#gray scale the image if neccessary
	#if img.shape[2] == 3:
	#	img = img.mean(2)

	#img = mahotas.imread(imname, as_grey=True)
	features = mahotas.features.haralick(img).mean(0)
	#features = mahotas.features.lbp(img, 1, 8)
	#features = mahotas.features.tas(img)
	#features = mahotas.features.zernike_moments(img, 2, degree=8)
	print 'features:', features, len(features), type(features[0])
	return features

def classify(model, features):
     return model.apply(features)

def grab_frame_from_video(video):
	frame = video.read()
	return frame
				

def predict_class(img):
	#try:
	model = pickle.load( open( "robomow_ai_model.mdl", "rb" ) )
	features = find_features(img)
	classID = classify(model, features)	
	if classID == 1: answer = "Mowable"
	if classID == 2: answer = "Non-Mowable"
	print "predicted classID:", answer
	eg.msgbox("predicted classID:"+answer)
	return classID
	#except:
	print "could not predict...bad data"
		

def save_data(features, classID):
	data_filename = 'robomow_feature_data.csv'
	###########################
	print 'writing image features to file: ', data_filename
	# delete data file and write header
	#f_handle = open(data_filename, 'w')
	#f_handle.write(str("classid, lbp, i3_histogram, rgb_histogram, sum_I3, sum2_I3, median_I3, avg_I3, var_I3, stddev_I3, rms_I3"))
	#f_handle.write('\n')
	#f_handle.close()

	#write class data to file
	f_handle = open(data_filename, 'a')
	f_handle.write(str(classID))
	f_handle.write(', ')
	f_handle.close()

	f_handle = open(data_filename, 'a')
	for i in range(len(features)):
		f_handle.write(str(features[i]))
		f_handle.write(" ")
	f_handle.write('\n')
	f_handle.close()
	
def train_ai():
		data = []
		classID = []
		features = []
		features_temp_array = []
		try: 
			data_filename = 'robomow_feature_data.csv'
			print 'readind features and classID: ', data_filename
			f_handle = open(data_filename, 'r')
			reader = csv.reader(f_handle)
			#read data from file into arrays
			for row in reader:
				data.append(row)

			for row in range(0, len(data)):
				#print features[row][1]
				classID.append(int(data[row][0]))
				features_temp_array.append(data[row][1].split(" "))

			#removes ending element which is a space
			for x in range(len(features_temp_array)):
				features_temp_array[x].pop()
				features_temp_array[x].pop(0)

			#convert all strings in array to numbers
			temp_array = []
			for x in range(len(features_temp_array)):
				temp_array = [ float(s) for s in features_temp_array[x] ]
				features.append(temp_array)

			#make numpy arrays
			#features = np.asarray(features)
			print classID, features 

			learner = milk.defaultclassifier()
			model = learner.train(features, classID)
			pickle.dump( model, open( "robomow_ai_model.mdl", "wb" ) )
		except:
			print "could not retrain.. bad file"
			return 


def subsection_image(pil_img, sections, visual):
	sections = sections / 4
	#print "sections= ", sections
	fingerprint = []

	# - -----accepts image and  number of sections to divide the image into (resolution of fingerprint)
	# ---------- returns a subsectioned image classified by terrain type
	img_width, img_height = pil_img.size
	#print "image size = img_wdith= ", img_width, "  img_height=", img_height, "  sections=", sections
	#cv.DestroyAllWindows()
	#time.sleep(2)
	if visual == True:
		cv_original_img1 = PILtoCV(pil_img,3)
		#cv.NamedWindow('Original', cv.CV_WINDOW_AUTOSIZE)
		cv.ShowImage("Original",cv_original_img1 )
		#cv_original_img1_ary = np.array(PIL2array(pil_img))
		#print cv_original_img1_ary
		#cv2.imshow("Original",cv_original_img1_ary) 
		cv.MoveWindow("Original", ((img_width)+100),50)
	#pil_img = rgb2I3 (pil_img)
	#cv.WaitKey()
	#cv.DestroyWindow("Original")
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
			print "I3_mean: ", I3_mean
			sub_ID = predict_class(image2array(cropped_img1))
			print "sub_ID:", sub_ID
			#fingerprint.append(sub_ID)
			if visual == True:
				cv_cropped_img1 = PILtoCV(cropped_img1,3)
				cv.ShowImage("Fingerprint",cv_cropped_img1 )
				cv.MoveWindow("Fingerprint", (img_width+100),50)
				if sub_ID == 1: I3_mean_rgb = (50,150,50)
				if sub_ID == 2: I3_mean_rgb = (150,150,150)
				if sub_ID == 3: I3_mean_rgb = (0,0,200)
				ImageDraw.Draw(pil_img).rectangle(box, (I3_mean_rgb))
				cv_img = PILtoCV(pil_img,3)
				cv.ShowImage("Image",cv_img)
				cv.MoveWindow("Image", 50,50)
				cv.WaitKey(20)
				time.sleep(.1)
				#print xx*yy
				#time.sleep(.05)
	#cv.DestroyAllWindows()
	cv.DestroyWindow("Fingerprint")
	cv.WaitKey(100)
	cv.DestroyWindow("Image")
	cv.WaitKey(100)
	cv.DestroyWindow("Original")
	cv.WaitKey(100)
	cv.DestroyWindow("Image")
	cv.WaitKey()
	time.sleep(2)
	#print "FINGERPRINT: ", fingerprint
	#cv.WaitKey()
	#return fingerprint
	return 9


if __name__=="__main__":
	
	print "********************************************************************"
	print "*   if 1 argument: video file to process otherwise uses webcam     *"
	print "********************************************************************"
	video = None
	webcam1 = None
	img1 = None

	if len(sys.argv) > 1:
		try:
			video = cv2.VideoCapture(sys.argv[1])
			print video, sys.argv[1]
		except:
			print "******* Could not open image/video file *******"
			print "Unexpected error:", sys.exc_info()[0]
			#raise		
			sys.exit(-1)
	reply =""
	#eg.rootWindowPosition = "+100+100"
	while True:
		#eg.rootWindowPosition = eg.rootWindowPosition
		print 'reply=', reply		

		#if reply == "": reply = "Next Frame"

		if reply == "Mowable":
			classID = "1"
			if img1 != None:
				features = find_features(img1)
				save_data(features, classID)
			else:
				if video != None: 
					img1 = np.array(grab_frame_from_video(video)[1])
				else:
					img1 = snap_shot()
				img1 = array2image(img1)
				img1 = img1.resize((320,240))
				img1 = image2array(img1)
				cv2.imwrite('temp.png', img1)

		if reply == "Non-Mowable":
			classID = "2"
			if img1 != None:
				features = find_features(img1)
				save_data(features, classID)
			else:
				if video != None: 
					img1 = np.array(grab_frame_from_video(video)[1])
				else:
					img1 = snap_shot()
				img1 = array2image(img1)
				img1 = img1.resize((320,240))
				img1 = image2array(img1)
				cv2.imwrite('temp.png', img1)

		if reply == "Quit":
			print "Quitting...."
			sys.exit(-1)

		if reply == "Predict":
			print "AI predicting"
			if img1 != None:
				predict_class(img1)
			else:
				if video != None: 
					img1 = np.array(grab_frame_from_video(video)[1])
				else:
					img1 = snap_shot()
				img1 = array2image(img1)
				img1 = img1.resize((320,240))
				img1 = image2array(img1)
				cv2.imwrite('temp.png', img1)

		if reply == "Subsection":
			img1 = Image.open('temp.png')
			print img1
			xx = subsection_image(img1, 16,True)
			print xx
			#while (xx != 9):
			#	time.sleep(1)

		if reply == "Retrain AI":
			print "Retraining AI"
			train_ai()

		if reply == "Next Frame":
			print "Acquiring new image.."
			if video != None: 
				img1 = np.array(grab_frame_from_video(video)[1])
			else:
				img1 = snap_shot()
			img1 = array2image(img1)
			img1 = img1.resize((320,240))
			img1 = image2array(img1)
			cv2.imwrite('temp.png', img1)
			#print type(img1)
			#img1.save()

		if reply == "Fwd 10 Frames":
			print "Forward 10 frames..."
			for i in range(10):
				img1 = np.array(grab_frame_from_video(video)[1])
			img1 = array2image(img1)
			img1 = img1.resize((320,240))
			img1 = image2array(img1)
			cv2.imwrite('temp.png', img1)

		if reply == "Del AI File":
			data_filename = 'robomow_feature_data.csv'
			f_handle = open(data_filename, 'w')
			f_handle.write('')
			f_handle.close()

		if reply == "Test Img":	
			#im = Image.fromarray(image)
			#im.save("new.png")
			img1 = Image.open('temp.png')
			#img1.thumbnail((320,240))
			path = "../../../../mobot_data/images/test_images/"
			filename = str(time.time()) + ".jpg"
			img1.save(path+filename)	
		try:
			print "trying"
			if video != None: 
				reply =	eg.buttonbox(msg='Classify Image', title='Robomow GUI', choices=('Mowable', 'Non-Mowable', 'Test Img', 'Next Frame', 'Fwd 10 Frames', 'Predict', 'Subsection', 'Retrain AI' , 'Del AI File', 'Quit'), image='temp.png', root=None)
			else:
				reply =	eg.buttonbox(msg='Classify Image', title='Robomow GUI', choices=('Mowable', 'Non-Mowable', 'Test Img','Next Frame',  'Predict', 'Retrain AI' , 'Del AI File', 'Quit'), image='temp.png', root=None)
		except:
			pass



