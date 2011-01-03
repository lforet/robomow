import cv

img = cv.LoadImageM("2005_Nickel_Proof_Obv.tif", cv.CV_LOAD_IMAGE_GRAYSCALE)
eig_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
temp_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)

# create the source image
canny_image = cv.CreateImage (cv.GetSize (img), 8, 1)


window_name = "Good Features To Track"
# create window and display the original picture in it
#cv.NamedWindow(window_name, 1)
#cv.SetZero(laplace)
#cv.ShowImage(window_name, img)

cv.Laplace(img, temp_image, 3)
cv.ShowImage("Laplace",temp_image)
#cv.SetZero(temp_image)
cv.Canny(img, canny_image , 50 , 150)
cv.ShowImage("Canny",canny_image )

for (x,y) in cv.GoodFeaturesToTrack(img, eig_image, temp_image, 20, 0.04, 1.0, useHarris = True):
	print "good feature at", x,y
	#Circle(img, center, radius, color, thickness=1, lineType=8, shift=0) 
	cv.Circle(img, (x,y), 6, (255,0,0),1, cv.CV_AA , 0)
	cv.ShowImage(window_name, img)
	cv.WaitKey(5)

img = cv.LoadImageM("/home/lforet/Downloads/photo.JPG")
tempimage = cv.LoadImageM("/home/lforet/Downloads/eye.JPG")	

size  = cv.GetSize(img)
size2 = cv.GetSize(tempimage)

width = (size[0] - size2[0]+1)
height = (size[1] - size2[1]+1)
resultimage = cv.CreateImage ((width,height), cv.IPL_DEPTH_32F, 1)	
cv.MatchTemplate(img, tempimage, resultimage, 1)
cv.ShowImage("result", resultimage)
cv.ShowImage("photo", img)
# wait some key to end

img = cv.LoadImageM("2005_Nickel_Proof_Obv.tif", cv.CV_LOAD_IMAGE_GRAYSCALE)
(keypoints, descriptors) = cv.ExtractSURF(img, None, cv.CreateMemStorage(), (0, 30000, 3, 1))
print len(keypoints), len(descriptors)

for ((x, y), laplacian, size, dir, hessian) in keypoints:
	print "x=%d y=%d laplacian=%d size=%d dir=%f hessian=%f" % (x, y, laplacian, size, dir, hessian)
	cv.Circle(img, (x,y), size, (255,0,0),1, cv.CV_AA , 0)

cv.ShowImage("SURF", img)


stor = cv.CreateMemStorage()
seq = cv.FindContours(canny_image, stor, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE)

cv.DrawContours(canny_image, seq, (255,0,0), (0,0,255), 20, thickness=1)
cv.ShowImage("Contours",canny_image )

original = cv.LoadImageM("2005_Nickel_Proof_Obv.tif", cv.CV_LOAD_IMAGE_GRAYSCALE)
print cv.GetHuMoments(cv.Moments(original))



cv.WaitKey(0)

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
