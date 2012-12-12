import cv2, cv
import time



webcam1 = cv2.VideoCapture(0)
cv2.namedWindow('Front Camera', cv.CV_WINDOW_AUTOSIZE)	
while True:
	#for i in range (5):
	ret, frame = webcam1.read()
	cv2.imshow('Front Camera', frame)
	cv.WaitKey(5)
	time.sleep(.1)


