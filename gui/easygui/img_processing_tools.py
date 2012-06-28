from PIL import Image
#import matplotlib.numerix as nx
import numpy as np
import cv


###########################################################
def rgbToI3(r, g, b):
	"""Convert RGB color space to I3 color space
	@param r: Red
	@param g: Green
	@param b: Blue
	return (I3) integer 
	"""
	i3 = ((2*g)-r-b)/2	 
	return i3
###########################################################
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
###########################################################
def CalcHistogram(img):
	#calc histogram of green band
	bins = np.arange(0,256)
	hist1 = image2array(img)
	H, xedges = np.histogram(np.ravel(hist1), bins=bins, normed=False)
	return H
###########################################################
def image2array(img):
	"""given an image, returns an array. i.e. create array of image using numpy """
	return np.asarray(img)

###########################################################

def array2image(arry):
	"""given an array, returns an image. i.e. create image using numpy array """
	#Create image from array
	return Image.fromarray(arry)

###########################################################

def grab_frame(camera):
	capture =  cv.CreateCameraCapture(camera)
	print capture
	time.sleep(.1)
	frame = cv.QueryFrame(capture)
	time.sleep(.1)
	print frame
	temp = cv.CloneImage(frame)
	return temp





