from CVtypes import cv

win = 'Show Cam'
cv.NamedWindow(win)
cap = cv.CreateCameraCapture(0)
while cv.WaitKey(1) != 27:
    img = cv.QueryFrame(cap)
    cv.ShowImage(win, img)
    
