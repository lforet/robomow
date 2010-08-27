#Boa:Frame:Frame1

import wx
from wx.lib.anchors import LayoutAnchors

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1PANEL1, wxID_FRAME1STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(973, 359), size=wx.Size(593, 513),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(593, 513))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(8, 0), size=wx.Size(593, 513),
              style=wx.TAB_TRAVERSAL)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='button1',
              name='button1', parent=self.panel1, pos=wx.Point(20, 288),
              size=wx.Size(93, 45), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='staticText1', name='staticText1', parent=self.panel1,
              pos=wx.Point(48, 72), size=wx.Size(71, 17), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        self.staticText1.SetLabel("hello")

        


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
