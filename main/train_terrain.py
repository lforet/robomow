#!/usr/bin/env python

import easygui as eg
import sys
from img_processing_tools import *
#from PIL import Image
from PIL import ImageStat
import cv, cv2 
import time
import mahotas
import numpy as np
import pickle
import csv
import milk
from threading import *
import gc


class front_camera(Thread):
	def __init__(self, camID):
		self.camID = camID   
		#self.camera = cv2.VideoCapture(camID)  
		#self.camera = cv.CreateCameraCapture(camID)  
		Thread.__init__(self)

	def run(self):
		cv2.namedWindow('Front Camera', cv.CV_WINDOW_AUTOSIZE)
		#gc.enable()
		camera =  cv.CreateCameraCapture(self.camID)
		while True:
			time.sleep(.1)
			#camera = cv2.VideoCapture(self.camID)
			#ret, frame = camera.read()
			frame = cv.QueryFrame(camera)
			#cv2.imshow('Front Camera', frame)
			cv.ShowImage('Front Camera', frame)
			cv.WaitKey(50)
			#camera.release()
			#frame = None
			#ret = None
			#camera = None
			#gc.collect()
					

def snap_shot():
	#capture from camera at location 0
	now = time.time()
	webcam1 = None
	try:
		while webcam1 == None:
			webcam1 = cv2.VideoCapture(0)
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
	try:
		model = pickle.load( open( "robomow_ai_model.mdl", "rb" ) )
		features = find_features(img)
		classID = classify(model, features)
		if classID == 1: answer = "Mowable"
		if classID == 2: answer = "Non-Mowable"
		print "predicted classID:", answer
		eg.msgbox("predicted classID:"+answer)
	except:
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
	#try: 
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
	#except:
		print "could not retrain.. bad file"
		return 

if __name__=="__main__":
	
	print "********************************************************************"
	print "*   if 1 argument: video file to process otherwise uses webcam     *"
	print "********************************************************************"
	video = None
	webcam1 = None
	front_cam = front_camera(1)
	front_cam.daemon=True
	front_cam.start()
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
	eg.rootWindowPosition = "+100+100"
	while True:
		eg.rootWindowPosition = eg.rootWindowPosition
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
	
		if video != None: 
			reply =	eg.buttonbox(msg='Classify Image', title='Robomow GUI', choices=('Mowable', 'Non-Mowable', 'Test Img', 'Next Frame', 'Fwd 10 Frames', 'Predict', 'Retrain AI' , 'Del AI File', 'Quit'), image='temp.png', root=None)
		else:
			reply =	eg.buttonbox(msg='Classify Image', title='Robomow GUI', choices=('Mowable', 'Non-Mowable', 'Test Img','Next Frame',  'Predict', 'Retrain AI' , 'Del AI File', 'Quit'), image='temp.png', root=None)


