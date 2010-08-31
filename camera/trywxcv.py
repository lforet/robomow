import wx
from CVtypes import cv
import time

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Try CV')
        self.SetClientSize((320,240))

        # setup capture
        self.cap = cv.CreateCameraCapture(0)
        self.Bind(wx.EVT_IDLE, self.onIdle)

        # infrastructure for timing
        self.frames = 0
        self.starttime = time.clock()

    def onIdle(self, event):
        img = cv.QueryFrame(self.cap)
        self.displayImage(img)
        event.RequestMore()

        # timing stuff
        self.frames += 1
        interval = time.clock() - self.starttime
        if interval > 5:
            print 'rate = %.1f frames/second' % (self.frames / interval)
            self.frames = 0
            self.starttime = time.clock()

    def displayImage(self, img, offset=(0,0)):
        bitmap = cv.ImageAsBitmap(img)
        dc = wx.ClientDC(self)
        dc.DrawBitmap(bitmap, offset[0], offset[1], False)

class myApp(wx.App):
    def OnInit(self):
        self.frame = myFrame()
        self.frame.Show(True)
        return True
    
app = myApp(0)
app.MainLoop()
