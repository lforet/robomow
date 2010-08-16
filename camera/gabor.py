from opencv.cv import *
from opencv.highgui import *
import math
import sys

src = 0
src_f = 0
image = 0
dest = 0
dest_mag = 0
kernelimg=0
big_kernelimg=0
kernel=0

kernel_size =21
pos_var = 50
pos_w = 5
pos_phase = 0
pos_psi = 90

def Process():
    var = pos_var/10.0
    w = pos_w/10.0
    phase = pos_phase*CV_PI/180.0
    psi = CV_PI*pos_psi/180.0

    cvZero(kernel)
    for x in range(-kernel_size/2+1,kernel_size/2+1):
        for y in range(-kernel_size/2+1,kernel_size/2+1):
            kernel_val = math.exp( -((x*x)+(y*y))/(2*var))*math.cos( w*x*math.cos(phase)+w*y*math.sin(phase)+psi)
            cvSet2D(kernel,y+kernel_size/2,x+kernel_size/2,cvScalar(kernel_val))
            cvSet2D(kernelimg,y+kernel_size/2,x+kernel_size/2,cvScalar(kernel_val/2+0.5))
    cvFilter2D(src_f, dest,kernel,cvPoint(-1,-1))
    cvShowImage("Process window",dest)
    cvResize(kernelimg,big_kernelimg)
    cvShowImage("Kernel",big_kernelimg)
    cvPow(dest,dest_mag,2)
    cvShowImage("Mag",dest_mag)

def cb_var(pos):
    global pos_var
    if pos > 0:
        pos_var = pos
    else:
        pos_var = 1
    Process()

def cb_w(pos):
    global pos_w
    pos_w = pos
    Process()

def cb_phase(pos):
    global pos_phase
    pos_phase = pos
    Process()

def cb_psi(pos):
    global pos_psi
    pos_psi = pos
    Process()

if __name__ == '__main__':
    image = cvLoadImage(sys.argv[1],1);
    print image.width
    
    if kernel_size%2==0:
        kernel_size += 1
    kernel = cvCreateMat(kernel_size,kernel_size,CV_32FC1)
    kernelimg = cvCreateImage(cvSize(kernel_size,kernel_size),IPL_DEPTH_32F,1)
    big_kernelimg = cvCreateImage(cvSize(kernel_size*20,kernel_size*20),IPL_DEPTH_32F,1)
    src = cvCreateImage(cvSize(image.width,image.height),IPL_DEPTH_8U,1)
    src_f = cvCreateImage(cvSize(image.width,image.height),IPL_DEPTH_32F,1)

    cvCvtColor(image,src,CV_BGR2GRAY)
    cvConvertScale(src,src_f,1.0/255,0)
    dest = cvCloneImage(src_f)
    dest_mag = cvCloneImage(src_f)

    cvNamedWindow("Process window",1)
    cvNamedWindow("Kernel",1)
    cvNamedWindow("Mag",1)
    cvCreateTrackbar("Variance","Process window", pos_var,100,cb_var)
    cvCreateTrackbar("Pulsation","Process window",pos_w ,30,cb_w)
    cvCreateTrackbar("Phase","Process window",pos_phase ,180,cb_phase)
    cvCreateTrackbar("Psi","Process window",pos_psi ,360,cb_psi)

    Process()
    cvWaitKey(0)
    cvDestroyAllWindows()
