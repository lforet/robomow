from opencv.cv import *
from opencv.highgui import *


def DoCanny(img, lowThresh, highThresh, aperature):
    gray = cvCreateImage(cvSize(cvGetSize(img).width, cvGetSize(img).height), IPL_DEPTH_8U, 1)
    cvCvtColor(img,gray,CV_BGR2GRAY)
    
    if (gray.nChannels != 1):
        return False
    
    out = cvCreateImage(cvSize(cvGetSize(gray).width, cvGetSize(gray).height), IPL_DEPTH_8U, 1)
    cvCanny(gray, out, lowThresh, highThresh, aperature)
    return out


if __name__ == '__main__':

    cvNamedWindow("Example5-Canny", CV_WINDOW_AUTOSIZE)

    
    cvNamedWindow("Example5", CV_WINDOW_AUTOSIZE)
    g_capture = cvCreateFileCapture('C:\python26\sample.avi')
    frames = long(cvGetCaptureProperty(g_capture, CV_CAP_PROP_FRAME_COUNT))
      
    loop = True
    
    while(loop):

        frame = cvQueryFrame(g_capture)
        if (frame == None):
            break
        cvShowImage("Example5", frame)
        outCan = DoCanny(frame, 70.0, 140.0, 3)
        cvShowImage("Example5-Canny", outCan)
        
        char = cvWaitKey(0)
        if (char != -1):
            if (ord(char) == 27):
                loop = False

    cvDestroyWindow("Example5")
    cvDestroyWindow("Example5-Canny")