#!/usr/bin/env python

from PIL import Image
import numpy as np
from PIL import ImageStat

def image2array(img):
	"""given an image, returns an array. i.e. create array of image using numpy """
	return np.asarray(img)

###########################################################

def array2image(arry):
	"""given an array, returns an image. i.e. create image using numpy array """
	#Create image from array
	return Image.fromarray(arry)

###########################################################

def PILtoCV(PIL_img):
	cv_img = cv.CreateImageHeader(PIL_img.size, cv.IPL_DEPTH_8U, 1)
	cv.SetData(cv_img, PIL_img.tostring())
	return cv_img

###########################################################

def CVtoPIL(img):
	"""converts CV image to PIL image"""
	cv_img = cv.CreateMatHeader(cv.GetSize(img)[1], cv.GetSize(img)[0], cv.CV_8UC1)
	#cv.SetData(cv_img, pil_img.tostring())
	pil_img = Image.fromstring("L", cv.GetSize(img), img.tostring())
	return pil_img
###########################################################

def CalcHistogram(img):
	#calc histogram of green band
	bins = np.arange(0,256)
	hist1 = image2array(img)
	H, xedges = np.histogram(np.ravel(hist1), bins=bins, normed=False)
	return H	

def WriteMeterics(image, classID):
	#calculate histogram
	print "Calculating Histogram for I3 pixels of image..."
	Red_Band, Green_Band, Blue_Band = image.split()
	Histogram = CalcHistogram(Green_Band)
	#save I3 Histogram to file in certain format
	f_handle = open('I3banddata.csv', 'a')
	f_handle.write(str(classID))
	f_handle.write(' ')
	f_handle.close()
	print "saving I3 histogram to dictionary..."
	f_handle = open("I3banddata.csv", 'a')
	for i in range(len(Histogram)):
		f_handle.write(str(Histogram[i]))
		f_handle.write(" ")
	#f_handle.write('\n')
	f_handle.close()

	I3_sum =    ImageStat.Stat(image).sum
	I3_sum2 =   ImageStat.Stat(image).sum2
	I3_median = ImageStat.Stat(image).median
	I3_mean =   ImageStat.Stat(image).mean
	I3_var =    ImageStat.Stat(image).var
	I3_stddev = ImageStat.Stat(image).stddev
	I3_rms =    ImageStat.Stat(image).rms
	print "saving I3 meterics to dictionary..."
	f_handle = open("I3banddata.csv", 'a')

	print "sum img1_I3: ",    I3_sum[1]
	print "sum2 img1_I3: ",   I3_sum2[1]
	print "median img1_I3: ", I3_median[1]
	print "avg img1_I3: ",    I3_mean[1]
	print "var img1_I3: ",    I3_var[1]
	print "stddev img1_I3: ", I3_stddev[1]
	print "rms img1_I3: ",    I3_rms[1]
	#print "extrema img1_I3: ", ImageStat.Stat(img1_I3).extrema
	#print "histogram I3: ", len(img1_I3.histogram())

	f_handle.write(str(I3_sum[1]))
	f_handle.write(" ")
	f_handle.write(str(I3_sum2[1]))
	f_handle.write(" ")
	f_handle.write(str(I3_median[1]))
	f_handle.write(" ")
	f_handle.write(str(I3_mean[1]))
	f_handle.write(" ")
	f_handle.write(str(I3_var[1]))
	f_handle.write(" ")
	f_handle.write(str(I3_stddev[1]))
	f_handle.write(" ")
	f_handle.write(str(I3_rms[1]))
	f_handle.write(" ")
	f_handle.write('\n')
	f_handle.close()
	return

def rgbToI3(r, g, b):
	"""Convert RGB color space to I3 color space
	@param r: Red
	@param g: Green
	@param b: Blue
	return (I3) integer 
	"""
	i3 = ((2*g)-r-b)/2	 
	return i3

def rgb2I3 (img):
	"""Convert RGB color space to I3 color space
	@param r: Red
	@param g: Green
	@param b: Blue
	return (I3) integer 
	"""
	xmax = img.size[0]
	ymax = img.size[1]
	#make a copy to return
	returnimage = Image.new("RGB", (xmax,ymax))
	imagearray = img.load()
	for y in range(0, ymax, 1):					
		for x in range(0, xmax, 1):
			rgb = imagearray[x, y]
			i3 = ((2*rgb[1])-rgb[0]-rgb[2]) / 2
			#print rgb, i3
			returnimage.putpixel((x,y), (0,i3,0))
	return returnimage
