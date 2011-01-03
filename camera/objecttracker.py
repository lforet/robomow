#!/usr/bin/python
import urllib2
import cv
import sys



if __name__ == "__main__":
    laplace = None
    colorlaplace = None
    planes = [ None, None, None ]
    capture = None
    
    if len(sys.argv) == 1:
        capture = cv.CreateCameraCapture(0)
    elif len(sys.argv) == 2 and sys.argv[1].isdigit():
        capture = cv.CreateCameraCapture(int(sys.argv[1]))
    elif len(sys.argv) == 2:
        capture = cv.CreateFileCapture(sys.argv[1]) 

    if not capture:
        print "Could not initialize capturing..."
        sys.exit(-1)
        
    cv.NamedWindow("Good Features to Track", 1)

    while True:
        frame = cv.QueryFrame(capture)
	frame_size = cv.GetSize(frame)
	#print frame_size[1], frame_size[0]
	eig_image = cv.CreateMat(frame_size[1], frame_size[0], cv.CV_32FC1)
	temp_image = cv.CreateMat(frame_size[1], frame_size[0], cv.CV_32FC1)
	grayframe = cv.CreateImage (cv.GetSize (frame), 8, 1)
	cv.CvtColor(frame, grayframe, cv.CV_RGB2GRAY)

        if frame:
		for (x,y) in cv.GoodFeaturesToTrack(grayframe, eig_image, temp_image, 20, 0.08, 1.0, blockSize=6,useHarris = True):
			#print "good feature at", x,y
			#Circle(img, center, radius, color, thickness=1, lineType=8, shift=0) 
			cv.Circle(frame, (x,y), 6, (255,0,0),1, cv.CV_AA , 0)

		cv.ShowImage("Good Features to Track", frame)

        if cv.WaitKey(10) != -1:
            break

    cv.DestroyWindow("Laplacian")


"""
GoodFeaturesToTrack(image, eigImage, tempImage, cornerCount, qualityLevel, minDistance, mask=NULL, blockSize=3, useHarris=0, k=0.04)  corners

    Determines strong corners on an image.
    Parameters:	
        * image (CvArr)  The source 8-bit or floating-point 32-bit, single-channel image
        * eigImage (CvArr)  Temporary floating-point 32-bit image, the same size as image
        * tempImage (CvArr)  Another temporary image, the same size and format as eigImage
        * cornerCount (int)  number of corners to detect
        * qualityLevel (float)  Multiplier for the max/min eigenvalue; specifies the minimal accepted quality of image corners
        * minDistance (float) Limit, specifying the minimum possible distance between the returned corners; Euclidian distance is used
        * mask (CvArr)  Region of interest. The function selects points either in the specified region or in the whole image if the mask is NULL
        * blockSize (int)  Size of the averaging block, passed to the underlying CornerMinEigenVal or CornerHarris used by the function
        * useHarris (int)  If nonzero, Harris operator ( CornerHarris ) is used instead of default CornerMinEigenVal
        * k (float) Free parameter of Harris detector; used only if ( texttt{useHarris} != 0 )

The function finds the corners with big eigenvalues in the image. The function first calculates the minimal eigenvalue for every source image pixel using the CornerMinEigenVal function and stores them in eigImage . Then it performs non-maxima suppression (only the local maxima in 3times 3 neighborhood are retained). The next step rejects the corners with the minimal eigenvalue less than texttt{qualityLevel} \cdot max(texttt{eigImage}(x,y)) . Finally, the function ensures that the distance between any two corners is not smaller than minDistance . The weaker corners (with a smaller min eigenvalue) that are too close to the stronger corners are rejected.

Note that the if the function is called with different values A and B of the parameter qualityLevel , and A > {B}, the array of returned corners with qualityLevel=A will be the prefix of the output corners array with qualityLevel=B .
"""
