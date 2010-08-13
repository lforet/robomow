#!/usr/bin/env python

import os
from PIL import Image
from PIL import ImageOps
import sys, time
from optparse import OptionParser
import numpy as np
from numpy import *
import mlpy
import Numeric, Image
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import mlpy
import pylab
import matplotlib.numerix as nx
from numpy import array
from scipy.cluster.vq import vq, kmeans, kmeans2, whiten



def hsvToRGB(h, s, v):
    """Convert HSV color space to RGB color space
    @param h: Hue
    @param s: Saturation
    @param v: Value
    return (r, g, b)  
    """
    import math
    hi = math.floor(h / 60.0) % 6
    f =  (h / 60.0) - math.floor(h / 60.0)
    p = v * (1.0 - s)
    q = v * (1.0 - (f*s))
    t = v * (1.0 - ((1.0 - f) * s))
    return {
        0: (v, t, p),
        1: (q, v, p),
        2: (p, v, t),
        3: (p, q, v),
        4: (t, p, v),
        5: (v, p, q),
    }[hi]

def rgbToHSV(r, g, b):
    """Convert RGB color space to HSV color space
    @param r: Red
    @param g: Green
    @param b: Blue
    return (h, s, v)  
    """
    maxc = max(r, g, b)
    minc = min(r, g, b)
    colorMap = {
        id(r): 'r',
        id(g): 'g',
        id(b): 'b'
    }
    if colorMap[id(maxc)] == colorMap[id(minc)]:
        h = 0
    elif colorMap[id(maxc)] == 'r':
        h = 60.0 * ((g - b) / (maxc - minc)) % 360.0
    elif colorMap[id(maxc)] == 'g':
        h = 60.0 * ((b - r) / (maxc - minc)) + 120.0
    elif colorMap[id(maxc)] == 'b':
        h = 60.0 * ((r - g) / (maxc - minc)) + 240.0
    v = maxc
    if maxc == 0.0:
        s = 0.0
    else:
        s = 1.0 - (minc / maxc)
    return (h, s, v)

def rgbToI3(r, g, b):
	"""Convert RGB color space to I3 color space
	@param r: Red
	@param g: Green
	@param b: Blue
	return (I3) integer 
	"""
	i3 = ((2*g)-r-b)/2	 
	return i3

def image2array(im):
    if im.mode not in ("L", "F"):
        raise ValueError, "can only convert single-layer images"
    if im.mode == "L":
        a = Numeric.fromstring(im.tostring(), Numeric.UnsignedInt8)
		  #a = Numeric.fromstring(im.tostring(), Numeric.Int8)
    else:
        a = Numeric.fromstring(im.tostring(), Numeric.Float32)
    a.shape = im.size[1], im.size[0]
    return a

def array2image(a):
    if a.typecode() == Numeric.UnsignedInt8:
        mode = "L"
    elif a.typecode() == Numeric.Float32:
        mode = "F"
    else:
        raise ValueError, "unsupported image mode"
    return Image.fromstring(mode, (a.shape[1], a.shape[0]), a.tostring())

def CalcHistogram(img):
	#calc histogram of green band
	bins = nx.arange(0,256)
	hist1 = image2array(img)
	H, xedges = np.histogram(np.ravel(hist1), bins=bins, normed=False)
	return H				


def CalcLBP(img):
	#Function to calculate local binary pattern of an image 
	#pass in a img
	#returns an array???
	# Angle step.
	#PI = 3.14159265
	neighbors = 8
	#a = 2*PI/neighbors;
	#radius = 1
	#Increment = 1/neighbors
	xmax = img.size[0]
	ymax = img.size[1] 
	#convert image to grayscale
	grayimage = ImageOps.grayscale(img)
	#make a copy to return
	returnimage = Image.new("L", (xmax,ymax))
	neighborRGB = np.empty([8], dtype=int)
	meanRGB = 0
	imagearray = grayimage.load()
	for y in range(1, ymax-1, 1):				
		for x in range(1, xmax-1, 1):
			centerRGB = imagearray[x, y]
			meanRGB = centerRGB
			neighborRGB[4] = imagearray[x+1,y+1]
			neighborRGB[5] = imagearray[x,y+1]
			neighborRGB[6] = imagearray[x-1,y+1]
			neighborRGB[7] = imagearray[x-1,y]
			neighborRGB[0] = imagearray[x-1,y-1]
			neighborRGB[1] = imagearray[x,y-1]
			neighborRGB[2] = imagearray[x+1,y-1]
			neighborRGB[3] = imagearray[x+1,y]
			#comparing against mean adds a sec vs comparing against center pixel
			meanRGB= centerRGB + neighborRGB.sum()
			meanRGB = meanRGB / (neighbors+1)
			#compute Improved local binary pattern (center pixel vs the mean of neighbors)
			lbp = 0						
			for i in range(neighbors):
			#comparing against mean adds a sec vs comparing against center pixel
				if neighborRGB[i] >= meanRGB:
				#if neighborRGB[i] >= centerRGB:
					lbp = lbp + (2**i)
			#putpixel adds 1 second vs storing to array
			returnimage.putpixel((x,y), lbp)
	return returnimage


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

usage = "usage: %prog [options]"
parser = OptionParser(prog=sys.argv[0], usage=usage)

parser.add_option("-d", "--dir", dest="directory",
                  help="directory of images to process. example: /home/user/python/images...default = images", metavar="DIRECTORY")

#parser.add_option('-d', '--dir', dest='directory of images to process', action='store',
#    help='directory of images to process. example: /home/user/python/images')

#parser.add_option('-t', '--true', dest='true', action='store_true',
#    help='example of using store_true, default %default')

#parser.add_option('-v', '--value', dest='value', action='store',
#    help='example of using multiple arguments')
#
parser.set_defaults(true=False )

options, args = parser.parse_args()

#print 'OPTIONS::', options
#print 'ARGS::', args


if len(sys.argv) == 1:
		path='testimage'
		
if len(sys.argv) == 2:
		path= sys.argv[1]
print 
print "Attempting to process files in directory: ", os.getcwd()+"/"+ path
print 

count = 0
for subdir, dirs, files in os.walk(path):
	count = len(files)

if count == 0:
	print "No files in directory to process..."

if count > 0:
	#delete classid and classdata files to completely rebuild them 
	f_handle = open("greenbandclassid.txt", 'w')
	f_handle.close()
	f_handle = open("greenbanddata.txt", 'w')
	f_handle.close()
	print "Files to Process: ", count
	for subdir, dirs, files in os.walk(path):
		for file in files:
			filename1= os.path.join(path, file)
			im = Image.open(filename1)
			print
			print "Processing current image: " , filename1 
			#print im.format, im.size, im.mode
			if im.size[0] <> 320 or im.size[1] <> 240:
				print "Image is not right size. Resizing image...."
				im = im.resize((320, 240))
				print "Resized to 320, 340"
			if im.mode == "RGB":
				print "Image has multiple color bands...Splitting Bands...."
				Red_Band, Green_Band,Blue_Band = im.split()
				
				im.show()
				print Green_Band
				Green_Band.show()
				#print "Saving color bands...."
				#filename = filename1.rsplit('.')[0] + "_RedBand.bmp"
				#print filename1.rsplit('.')[0][-1]
				imageclassid = filename1.rsplit('.')[0][-1]
				classid = array(int(imageclassid[0]))
				if imageclassid.isdigit():
					print "Image class: ", imageclassid
					f_handle = open("greenbandclassid.txt", 'a')
					f_handle.write(str(classid))
					f_handle.write(' ')
					f_handle.close()
					
					#calculate histogram
					print "Calculating Histogram for the green pixels of image..."
					Histogram = CalcHistogram(Green_Band)
					#save Green Histogram to file in certain format
					print "saving histogram to dictionary..."
					f_handle = open("greenbanddata.txt", 'a')
					for i in range(len(Histogram)):
						f_handle.write(str(Histogram[i]))
						f_handle.write(" ")
					f_handle.write('\n')
					f_handle.close()
				#print "Saving.....", filename 
				#Red_Band.save(filename, "BMP")
				#filename = filename1.rsplit('.')[0] + "_GreenBand.bmp"
					print "calling i3"
					I3image = rgb2I3(im)
					#calculate histogram
					print "Calculating Histogram for I3 pixels of image..."
					Red_Band, Green_Band, Blue_Band = I3image.split()
					Histogram = CalcHistogram(Green_Band)
					#save I3 Histogram to file in certain format
					f_handle = open("I3bandclassid.txt", 'a')
					f_handle.write(str(classid))
					f_handle.write(' ')
					f_handle.close()
					print "saving I3 histogram to dictionary..."
					f_handle = open("I3banddata.txt", 'a')
					for i in range(len(Histogram)):
						f_handle.write(str(Histogram[i]))
						f_handle.write(" ")
					f_handle.write('\n')
					f_handle.close()
				
				"""
				#Local Binary Patterns
				inittime = time.time()
				print "Computing Local Binary Patterns....", inittime, time.ctime()
				neighborRGB = np.empty([8], dtype=int)
				
				for y in range(1, ymax-1, 1):	
					#print y				
					for x in range(1, xmax-1, 1):
						meanRGB = 0
						neighborRGB[0] = 0
						centerRGB = im2.getpixel((x, y))
						#im2.putpixel((x,y), (255,0,0))
						meanRGB = centerRGB
						#lbp = 0
						for i in range(neighbors):
							XPixel = around(-radius*sin((i-1)*a) )
							YPixel = around(radius*cos((i-1)*a) )
							#print  XPixel, YPixel,x+XPixel,y+YPixel
							if x+XPixel > -1 and y+YPixel > -1:
								neighborRGB[i] = im2.getpixel((x+XPixel,y+YPixel))
								meanRGB = meanRGB + neighborRGB[i]
								#if neighborRGB[i] >= centerRGB:
								#	lbp = lbp + (2**i)
								#print neighborRGB, meanRGB
						meanRGB = meanRGB / (neighbors+1)

						#print neighborRGB, meanRGB
						#im3.putpixel((x,y), lbp)
						
						
						#compute Improved local binary pattern (center pixel vs the mean of neighbors)
						lbp = 0						
						for i in range(neighbors):
							#print i, neighborRGB[i], meanRGB, (neighborRGB[i] >= meanRGB)
							if neighborRGB[i] >= meanRGB:
								lbp = lbp + (2**i)
						im3.putpixel((x,y), lbp)

						#Compute Uniform local binary pattern (center pixel vs the mean of neighbors)
						#im4.putpixel((x,y), 0)
						#if lbp == 1 or lbp == 3 or lbp == 7 or lbp == 15 or lbp == 31 or lbp == 127 or lbp == 255:
						#	im4.putpixel((x,y), lbp)

 				print "Completed Computing Local Binary Patterns....", (time.time()-inittime)
				"""
				I3image.show()
				#Local Binary Patterns
				inittime = time.time()
				print "Computing Local Binary Patterns....", inittime, time.ctime()				
				im6  = CalcLBP(im)
				im7 = CalcLBP(Green_Band)
				Red_Band, Green_Band, Blue_Band = im.split()


				print "Completed Computing Local Binary Patterns....", (time.time()-inittime)
				im6.show()
				im7.show()


#Compute Uniform local binary pattern (center pixel vs the mean of neighbors)
#im4.putpixel((x,y), 0)
#if lbp == 1 or lbp == 3 or lbp == 7 or lbp == 15 or lbp == 31 or lbp == 127 or lbp == 255:
#	im4.putpixel((x,y), lbp)

 				
				#
				#print im3.getcolors()
				#print im3.histogram()				
				#im3.show()
				#im5.show()
				#hist1 = CalcHistogram(im3)
				#print hist1
				#plt.plot(hist1)
				#plt.show()
				stop





