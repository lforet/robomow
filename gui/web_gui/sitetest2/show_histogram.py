# RGB Hitogram
# This script will create a histogram image based on the RGB content of
# an image. It uses PIL to do most of the donkey work but then we just
# draw a pretty graph out of it.
#
# May 2009,  Scott McDonough, www.scottmcdonough.co.uk
#

import Image, ImageDraw
import sys

import numpy as np
import matplotlib.pyplot as plt
import pylab as P



if __name__=="__main__":

	if len(sys.argv) < 1:
		#print "******* Requires an image files of the same size."
		#print "This program will return the angle at which the second is in relation to the first. ***"
		sys.exit(-1)

	try:
		imagepath = sys.argv[1] # The image to build the histogram of
		#img2 = cv.LoadImage(sys.argv[2],cv.CV_LOAD_IMAGE_GRAYSCALE)
	except:
		print "******* Could not open image files *******"
		sys.exit(-1)
	


	histHeight = 120            # Height of the histogram
	histWidth = 256             # Width of the histogram
	multiplerValue = 1.5        # The multiplier value basically increases
		                        # the histogram height so that love values
		                        # are easier to see, this in effect chops off
		                        # the top of the histogram.
	showFstopLines = True       # True/False to hide outline
	fStopLines = 5


	# Colours to be used
	backgroundColor = (51,51,51)    # Background color
	lineColor = (102,102,102)       # Line color of fStop Markers 
	red = (255,60,60)               # Color for the red lines
	green = (51,204,51)             # Color for the green lines
	blue = (0,102,255)              # Color for the blue lines

	##################################################################################


	img = Image.open(imagepath)
	hist = img.histogram()
	histMax = max(hist)                                     #comon color
	xScale = float(histWidth)/len(hist)                     # xScaling
	yScale = float((histHeight)*multiplerValue)/histMax     # yScaling 


	im = Image.new("RGBA", (histWidth, histHeight), backgroundColor)   
	draw = ImageDraw.Draw(im)


	# Draw Outline is required
	if showFstopLines:    
		xmarker = histWidth/fStopLines
		x =0
		for i in range(1,fStopLines+1):
		    draw.line((x, 0, x, histHeight), fill=lineColor)
		    x+=xmarker
		draw.line((histWidth-1, 0, histWidth-1, 200), fill=lineColor)
		draw.line((0, 0, 0, histHeight), fill=lineColor)


	# Draw the RGB histogram lines
	x=0; c=0;
	for i in hist:
		if int(i)==0: pass
		else:
		    color = red
		    if c>255: color = green
		    if c>511: color = blue
		    draw.line((x, histHeight, x, histHeight-(i*yScale)), fill=color)        
		if x>255: x=0
		else: x+=1
		c+=1

	# Now save and show the histogram    
	im.save('histogram.png', 'PNG')
	im.show()
	#!/usr/bin/env python

	#
	# The hist() function now has a lot more options
	#

	#
	# first create a single histogram
	#
	mu, sigma = 200, 25
	x = mu + sigma*P.randn(10000)

	# the histogram of the data with histtype='step'
	n, bins, patches = P.hist(x, 50, normed=1, histtype='stepfilled')
	P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)

	# add a line showing the expected distribution
	y = P.normpdf( bins, mu, sigma)
	l = P.plot(bins, y, 'k--', linewidth=1.5)


	#
	# create a histogram by providing the bin edges (unequally spaced)
	#
	P.figure()

	bins = [100,125,150,160,170,180,190,200,210,220,230,240,250,275,300]
	# the histogram of the data with histtype='step'
	n, bins, patches = P.hist(x, bins, normed=1, histtype='bar', rwidth=0.8)

	#
	# now we create a cumulative histogram of the data
	#
	P.figure()

	n, bins, patches = P.hist(x, 50, normed=1, histtype='step', cumulative=True)

	# add a line showing the expected distribution
	y = P.normpdf( bins, mu, sigma).cumsum()
	y /= y[-1]
	l = P.plot(bins, y, 'k--', linewidth=1.5)

	# create a second data-set with a smaller standard deviation
	sigma2 = 15.
	x = mu + sigma2*P.randn(10000)

	n, bins, patches = P.hist(x, bins=bins, normed=1, histtype='step', cumulative=True)

	# add a line showing the expected distribution
	y = P.normpdf( bins, mu, sigma2).cumsum()
	y /= y[-1]
	l = P.plot(bins, y, 'r--', linewidth=1.5)

	# finally overplot a reverted cumulative histogram
	n, bins, patches = P.hist(x, bins=bins, normed=1,
		histtype='step', cumulative=-1)


	P.grid(True)
	P.ylim(0, 1.05)


	#
	# histogram has the ability to plot multiple data in parallel ...
	# Note the new color kwarg, used to override the default, which
	# uses the line color cycle.
	#
	P.figure()

	# create a new data-set
	x = mu + sigma*P.randn(1000,3)

	n, bins, patches = P.hist(x, 10, normed=1, histtype='bar',
		                        color=['crimson', 'burlywood', 'chartreuse'],
		                        label=['Crimson', 'Burlywood', 'Chartreuse'])
	P.legend()

	#
	# ... or we can stack the data
	#
	P.figure()

	n, bins, patches = P.hist(x, 10, normed=1, histtype='barstacked')

	#
	# finally: make a multiple-histogram of data-sets with different length
	#
	x0 = mu + sigma*P.randn(10000)
	x1 = mu + sigma*P.randn(7000)
	x2 = mu + sigma*P.randn(3000)

	# and exercise the weights option by arbitrarily giving the first half
	# of each series only half the weight of the others:

	w0 = np.ones_like(x0)
	w0[:len(x0)/2] = 0.5
	w1 = np.ones_like(x1)
	w1[:len(x1)/2] = 0.5
	w2 = np.ones_like(x2)
	w0[:len(x2)/2] = 0.5



	P.figure()

	n, bins, patches = P.hist( [x0,x1,x2], 10, weights=[w0, w1, w2], histtype='bar')

	P.show()



