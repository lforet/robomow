from img_processing_tools import *
from PIL import Image
from PIL import ImageStat
import sys

if __name__=="__main__":

	if len(sys.argv) < 1:
		#print "******* Requires an image files of the same size."
		#print "This program will return the angle at which the second is in relation to the first. ***"
		sys.exit(-1)

	try:
		img1 = Image.open(sys.argv[1])
		#img2 = cv.LoadImage(sys.argv[2],cv.CV_LOAD_IMAGE_GRAYSCALE)
	except:
		print "******* Could not open image files *******"
		sys.exit(-1)

	img1.show()
	img1_I3 = rgb2I3(img1)
	img1_I3.show()
	print "sum img1: ", ImageStat.Stat(img1).sum
	print "sum img1_I3: ", ImageStat.Stat(img1_I3).sum
	print "sum2 img1_I3: ", ImageStat.Stat(img1_I3).sum2
	print "median img1_I3: ", ImageStat.Stat(img1_I3).median
	print "avg img1_I3: ", ImageStat.Stat(img1_I3).mean
	print "var img1_I3: ", ImageStat.Stat(img1_I3).var
	print "stddev img1_I3: ", ImageStat.Stat(img1_I3).stddev
	print "rms img1_I3: ", ImageStat.Stat(img1_I3).rms
	print "extrema img1_I3: ", ImageStat.Stat(img1_I3).extrema
	print "histogram I3: ", len(img1_I3.histogram())
