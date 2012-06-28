import easygui as eg
import sys
from img_processing_tools import *
#from PIL import Image
from PIL import ImageStat



if __name__=="__main__":

	image   = "1.grass10.gif"
	msg     = "Is this mowable?"
	choices = ["Grab Frame","No"]
	reply   = eg.buttonbox(msg,image=image,choices=choices)
	cam_img = Image.open("1.grass10.jpg")
	#print cam_img
	#cam_img.show()
	#choice = choicebox(msg, title, choices)
	# note that we convert choice to string, in case
	# the user cancelled the choice, and we got None.
	#eg.msgbox("You chose: " + str(reply), "Result")

	# data file schema
	# classID, next 256 integers are I3 greenband histogram, I3 sum, I3 sum2, I3 median, I3 mean, 
	# I3 variance, I3 Standard Deviation, I3 root mean square


	if reply == "Grab Frame":
		try:
			#img1 = cv.LoadImage(sys.argv[1],cv.CV_LOAD_IMAGE_GRAYSCALE)
			frame = grab_frame(0)
			#img1 = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
			#img1 = CVtoGray(frame)
			#cv.WaitKey()
			#img1 = CV_enhance_edge(img1)
			#cv.WaitKey()
			#img2 = cv.LoadImage(sys.argv[1],cv.CV_LOAD_IMAGE_GRAYSCALE)
			#img3 = cv.LoadImage(sys.argv[2],cv.CV_LOAD_IMAGE_GRAYSCALE)
			print "frame=", frame
			cv.ShowImage("Frame1", frame)
			cv.MoveWindow ('Frame1',50 ,50 )
		except:
			print "******* Could not open image files *******"
			sys.exit(-1)




	if reply == "Yes":
		#eg.msgbox("Going to mow....:")
		print "calling i3"
	
		I3image = rgb2I3(cam_img)
	
		#calculate histogram
		print "Calculating Histogram for I3 pixels of image..."
		Red_Band, Green_Band, Blue_Band = I3image.split()
		Histogram = CalcHistogram(Green_Band)
		classid = "1"
		#save I3 Histogram to file in certain format
		f_handle = open('I3banddata.txt', 'a')
		f_handle.write(str(classid))
		f_handle.write(' ')
		f_handle.close()
		print "saving I3 histogram to dictionary..."
		f_handle = open("I3banddata.txt", 'a')
		for i in range(len(Histogram)):
			f_handle.write(str(Histogram[i]))
			f_handle.write(" ")
		#f_handle.write('\n')
		f_handle.close()

		I3_sum =    ImageStat.Stat(I3image).sum
		I3_sum2 =   ImageStat.Stat(I3image).sum2
		I3_median = ImageStat.Stat(I3image).median
		I3_mean =   ImageStat.Stat(I3image).mean
		I3_var =    ImageStat.Stat(I3image).var
		I3_stddev = ImageStat.Stat(I3image).stddev
		I3_rms =    ImageStat.Stat(I3image).rms
		print "saving I3 meterics to dictionary..."
		f_handle = open("I3banddata.txt", 'a')

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



	if reply == "No":
		eg.msgbox("NOT Going to mow....:")


