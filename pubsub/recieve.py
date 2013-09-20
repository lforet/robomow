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

def callback(ch, method, properties, body):
	global count 
	count = count +1
	frame = pickle.loads(body)
	print count
	cv2.imshow('Video', frame)
	cv.WaitKey(10)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.39'))

channel = connection.channel()

channel.queue_declare(queue='mobot_video1', auto_delete=True, arguments={'x-message-ttl':1000}) 

print ' [*] Waiting for messages. To exit press CTRL+C'

cv2.namedWindow('Video', cv.CV_WINDOW_AUTOSIZE)

channel.basic_consume(callback, queue='mobot_video1', no_ack=True)

channel.start_consuming()
