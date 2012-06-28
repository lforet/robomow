

import Image
from numpy import *
from PIL import Image
import ImageFilter
import ImageOps
import ImageStat

#load image
im = Image.open("images/1.grass11.jpg")
print "image loaded", im
print "image is in mode = " , im.mode
print "image size = ", im.size
#print "image info = ", im.info
im.show()


#image resize
# adjust width and height to your needs
#
#idth = 500
#eight = 420
#
# use one of these filter options to resize the image
#
#m2 = im1.resize((width, height), Image.NEAREST) # use nearest neighbour
#m3 = im1.resize((width, height), Image.BILINEAR) # linear interpolation in a 2x2 environment
#m4 = im1.resize((width, height), Image.BICUBIC) # cubic spline interpolation in a 4x4 environment
#m5 = im1.resize((width, height), Image.ANTIALIAS) # best down-sizing filter

#convert an image to different format
im6 = im.convert("L")
im6.save("greyscale.jpg")

#print bands of color
print "bands of color = ", im6.getbands()

#print list of colors
#print im6.getcolors() 

#print number of colors
print "number of unique colors = " , len(im6.getcolors())

#print pixel values colors
#print list(im6.getdata())

#create histogram of greyscale image
image_histogram = im6.histogram()
print image_histogram 
print "image_histogram size = ", len(image_histogram)
im6.show()

#split image into color bands (RGB)
kkk = im.split()
print kkk[1]

#kkk[0].show()
#kkk[1].show()
#kkk[2].show()
#/Parse An Image

#import ImageFile

#fp = open("lena.pgm", "rb")

#p = ImageFile.Parser()

#while 1:
#    s = fp.read(1024)
#    if not s:
#        break
#    p.feed(s)

#im = p.close()

#im.save("copy.jpg")
#

#median filter
#im8 = im.filter(ImageFilter.MedianFilter(size=3))
#im8.show()

#mode filter
#im8 = im.filter(ImageFilter.ModeFilter(size=3))
#im8.show()

#EDGE_ENHANCEfilter
#im8 = im.filter(ImageFilter.EDGE_ENHANCE)
#im8.show()
#greyscale the image
im8 = ImageOps.grayscale(im) 
im8.show()

#equalize the image
im8 = ImageOps.equalize(im6)
im8.show()

#get image stats
im_stat = ImageStat.Stat(im)

print "stat.extrema  = ", im_stat.extrema
print "stat.count  = ", im_stat.count
print "stat.sum  = ", im_stat.sum
print "stat.sum2  = ", im_stat.sum2
print "stat.mean  = ", im_stat.mean
print "stat.median  = ", im_stat.median
print "stat.rms  = ", im_stat.rms
print "stat.var  = ", im_stat.var
print "stat.stddev  = ", im_stat.stddev

