#!/usr/bin/env python
import sys
sys.path.append( "../lib/" )

import pika
from pylab import imread
import Image
import time
import cv, cv2
import cPickle as pickle	
from img_processing_tools import *
import numpy

count = 0
recovery_count = 0

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

'''
 queue_declare(callback, queue='', passive=False, durable=False, exclusive=False, auto_delete=False, nowait=False, arguments=None)[source]

    Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.

    Leave the queue name empty for a auto-named queue in RabbitMQ
    Parameters:	

        callback (method) - The method to call on Queue.DeclareOk
        queue (str or unicode) - The queue name
        passive (bool) - Only check to see if the queue exists
        durable (bool)- Survive reboots of the broker
        exclusive (bool)- Only allow access by the current connection
        auto_delete (bool) - Delete after consumer cancels or disconnects
        nowait (bool) - Do not wait for a Queue.DeclareOk
        arguments (dict) - Custom key/value arguments for the queue

'''
channel.queue_declare(queue='mobot_video1', auto_delete=True, arguments={'x-message-ttl':1000})

cv2.namedWindow('Front Camera', cv.CV_WINDOW_AUTOSIZE)
#webcam1 =  cv.CreateCameraCapture(1)
webcam1 = cv2.VideoCapture(1)
#webcam1.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320) 
#webcam1.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240) 
#webcam1.set(cv2.cv.CV_CAP_PROP_FPS, 10)

while True:
	frame1 = None
	now = time.time()
	count = count + 1
	time.sleep(0.001)
	try:
		#frame1 = cv.QueryFrame(camera)
		ret, frame1 = webcam1.read()
	except:
		pass
	capture_time = (time.time()-now)
	print 'frames:', count , "   capture time:", capture_time, "   recovery_count:", recovery_count 
	if capture_time > 0.9 or frame1 == None:
		frame1 = None
		while frame1 == None:
			recovery_count = recovery_count + 1
			try:
				webcam1.release				
				webcam1 = cv2.VideoCapture(1)
				ret, frame1 = webcam1.read()
			except:
				time.sleep(.1)
				pass
	#print frame1, type(frame1)#, dir (frame1)
	#cv.ShowImage('Front Camera', frame1)
	cv2.imshow('Front Camera', frame1)
	#cv.WaitKey(30)	
	cv2.waitKey(30)
	img = pickle.dumps(frame1,-1)
	channel.basic_publish(exchange='', routing_key='mobot_video1', body=img)

connection.close()

