#!/usr/bin/env python

import os
from PIL import Image
import sys
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

usage = "usage: %prog [options]"

parser = OptionParser(prog=sys.argv[0], usage=usage)

parser.add_option("-d", "--dir", dest="directory",
                  help="directory of images to process. example: /home/user/python/images", metavar="DIRECTORY")

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
		path='/home/lforet/python/images'

if len(sys.argv) == 2:
		path= sys.argv[1]
print 
print "Attempting to process files in directory: ", path
print 




count = 0
for subdir, dirs, files in os.walk(path):
	count = len(files)

if count == 0:
	print "No files in directory to process..."

if count > 0:
	#del classid and classdata files
	f_handle = open("classidfile.txt", 'w')
	f_handle.close()
	#f_handle = open("classdatafile.txt", 'w')
	#f_handle.close()
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
			if im.mode == "RGB":
				print "Image has multiple color bands...Splitting Bands...."
				Red_Band, Green_Band,Blue_Band = im.split()
				print Green_Band
				#print "Saving color bands...."
				#filename = filename1.rsplit('.')[0] + "_RedBand.bmp"
				imageclassid = filename1.rsplit('.')[0][-1]
				classid = array(int(imageclassid[0]))
				if imageclassid.isdigit():
					print "hey this is a class 1 image"
					#if os.stat("classidfile.txt")[6] == 0:
					#	f_handle = open("classidfile.txt", 'a')
					#	classid.append(int(imageclassid[0]))
					#	savetxt("classidfile.txt", classid)
					#	f_handle.close()
					f_handle = open("classidfile.txt", 'a')
					f_handle.write(str(classid))
					f_handle.write(' ')
					f_handle.close()
					#testarray.fromfile(f_handle, 100)
					#classid.append(int(imageclassid[0]))
					#array.tofile(f)
					print imageclassid
					
					#calc histogram of green band
					bins = nx.arange(0,256)
					hist1 = image2array(Green_Band)
					H, xedges = np.histogram(np.ravel(hist1), bins=bins, normed=False)

					f_handle = open("classdatafile.txt", 'a')
					#savetxt(f_handle, H, fmt='%.f')
					for i in range(len(H)):
						f_handle.write(str(H[i]))
						f_handle.write(" ")
					f_handle.write('\n')
					f_handle.close()
					#break
					
					#f_handle = open("classdatafile.txt", 'r')
					#jjj = genfromtxt(f_handle, dtype = int)
					#print np.shape(jjj), jjj.ndim
					#break
				#fff[-1].isdigit()
				#print "Saving.....", filename 
				#Red_Band.save(filename, "BMP")
				#filename = filename1.rsplit('.')[0] + "_GreenBand.bmp"
				#print "Saving.....", filename 
				#Green_Band.save(filename, "BMP")
				#filename = filename1.rsplit('.')[0] + "_BlueBand.bmp"
				#print "Saving.....", filename 
				#Blue_Band.save(filename, "BMP")
				#ary = array([[47, 51, 65],[62, 70, 71], [80, 83, 78], [65, 34, 89]])
				

				print np.ndim(hist1)
				print np.size(hist1)
				print np.shape(hist1)
				#y = np.shape(ary)[0]
				#x = np.shape(ary)[1]
				#print ary[0].tolist()

				#hist1 = np.array([Green_Band.histogram()], dtype=int)
				#hist1 = np.array(ary, dtype=int)
				#hist1 = list(ary)
				#print hist1[0]
				#print type(hist1)
				#print list(np.ravel(hist1)).count(0)

				print np.size(H)
				print np.shape(H)

				ary = Green_Band.histogram()
				print np.size(ary)
				print np.shape(ary)
				#hist2d = np.array([hist], dtype=int)
				#print np.shape(hist2d)
				#print np.ndim(hist2d)
				#savetxt("test.txt", hist)
				#f_handle = open("test.txt", 'a')
				#savetxt(f_handle, hist2d)
				#f_handle.close()
				#f_handle = open("test.txt", 'a')
				#hist2 = genfromtxt("test.txt")
				#print hist2
				#print np.shape(hist2)
				#print np.ndim(hist2)
				#print hist2[0], hist2[1]
				#xtr = np.array([hist])
				#ytr = np.array([1])
				#print np.shape(xtr)
				#print np.shape(ytr)


				#Save and read data from disk
				#print mlpy.data_tofile('data_example.dat', xtr, ytr, sep='	')
				#x, y = mlpy.data_fromfile('data_example.dat')
				#print x
				#print y

				#plot the thing
				# the histogram of the data
				#pylab.hist(H, bins=32, facecolor='b', edgecolor='b' )
				#pylab.plot(ary)
				#pylab.plot(H)
				#pylab.show()

#				im = Image.open(filename1)
#				imbuf = im.tostring('raw','RGB',0,-1)
#				imnx = nx.fromstring(imbuf,nx.UInt8)
#				imnx.shape = im.size[1], im.size[0], 3

#				bins = nx.arange(0,256)
#				pylab.hist( nx.ravel(imnx[:,:,0]), bins=bins, facecolor='r', edgecolor='r' )
#				pylab.hist( nx.ravel(imnx[:,:,1]), bins=bins, facecolor='g', edgecolor='g' )
#				pylab.hist( nx.ravel(imnx[:,:,2]), bins=bins, facecolor='b', edgecolor='b' )
#				pylab.show()



				#n, bins, patches = plt.hist(hist1, 32, normed=0, facecolor='green', alpha=0.95)
				#plt.axis([0, 255, 0, 255])
				#print bins
				#plt.grid(True)
				#plt.show()

			   #print hist[0]
				xmax = im.size[0]
				ymax = im.size[1]
				#elementcount =  np.size(ary2)
				#print elementcount
				#meanvalue = np.mean(ary)
				#print "meanvalue = ", int(meanvalue)

				# Angle step.
				PI = 3.14159265
				neighbors = 8
				a = 2*PI/neighbors;
				radius = 2
				Increment = 1/neighbors 

				im2 = im.copy()
				im3 = im.copy()
	
				for y in range(0, ymax, 1):					
					for x in range(0, xmax, 1):
						rgb = im.getpixel((x, y))
						i3 = rgbToI3(rgb[0],rgb[1],rgb[2])
						im3.putpixel((x,y), (0,i3,0))
				im.show()
				im3.show()
										
				for y in range(0, ymax, 5):					
					for x in range(0, xmax, 5):
						rgb = im.getpixel((x, y))
						im2.putpixel((x,y), (255,0,0))
						for i in range(neighbors):
							XPixel = around(-radius*sin((i-1)*a) )
							YPixel = around(radius*cos((i-1)*a) )
						
							#print  XPixel, YPixel,x+XPixel,y+YPixel
							if x+XPixel > -1 and y+YPixel > -1:
								im2.putpixel((x+XPixel,y+YPixel), (0,255,0))
						#    
						#    #if sum(XPixel)+x > 0:
						#    print ary[x+XPixel][y+YPixel]
				im2.show()
			




