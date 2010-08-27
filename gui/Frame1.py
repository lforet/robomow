#Boa:Frame:Frame1

import wx
import socket
import time


#Variables
HOST = '127.0.0.1'        # Symbolic name meaning the local host
HBPORT = 12340            # HeartBeat Port Arbitrary non-privileged port




def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1PANEL1, wxID_FRAME1STTXTHRTBEAT, 
 wxID_FRAME1TEXTCTRL1, wxID_FRAME1TXTSTATUS, 
] = [wx.NewId() for _init_ctrls in range(6)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(649, 219), size=wx.Size(946, 673),
              style=wx.DEFAULT_FRAME_STYLE, title=u'RoboMower DashBoard')
        self.SetClientSize(wx.Size(930, 635))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(930, 635),
              style=wx.TAB_TRAVERSAL)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1,
              label=u'Connect To Robot', name='button1', parent=self.panel1,
              pos=wx.Point(8, 8), size=wx.Size(104, 32), style=0)
        self.button1.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.NORMAL, False,
              u'Serif'))
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(288, 40), size=wx.Size(88, 24),
              style=0, value='textCtrl1')

        self.stTxtHrtBeat = wx.StaticText(id=wxID_FRAME1STTXTHRTBEAT,
              label=u'HeartBeat', name=u'stTxtHrtBeat', parent=self.panel1,
              pos=wx.Point(282, 16), size=wx.Size(108, 16), style=0)
        self.stTxtHrtBeat.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Terminal'))

        self.txtStatus = wx.TextCtrl(id=wxID_FRAME1TXTSTATUS, name=u'txtStatus',
              parent=self.panel1, pos=wx.Point(120, 8), size=wx.Size(144, 600),
              style=wx.TE_MULTILINE, value=u'')

    def __init__(self, parent):
        self._init_ctrls(parent)



    def Initialize_HeartBeat():
        HB_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global HOST
        global HBPORT
        HB_TCP.bind((HOST, HBPORT)) 
        print "listening for robot on port: ", HBPORT
        hhh = self.txtStatus.GetValue()
        hhh = hhh + "listening for robot on port: " + HBPORT + "\n"
        self.txtStatus.SetValue(hhh)
        HB_TCP.listen(1)
        try:
            print "waiting to accept.."
            conn, addr = HB_TCP.accept()
            print "accepted connection from client.."
            while conn <> "":
                HB_TCP.listen(1)
                #print time.time()
                #print s.gettimeout()
                print 'Connected by', addr
                data = conn.recv(1024)
                if not data: break
                print 'Received from remote: ', data 
                conn.send("ACK") 
        except IOError as detail:
            print "connection lost", detail    
 
    def OnButton1Button(self, event):
        ggg = self.stTxtHrtBeat.GetLabel()
        #self.textCtrl1.SetValue("New Text")
        self.textCtrl1.SetValue(ggg)
        hhh = self.txtStatus.GetValue()
        hhh = hhh + "jjj" + "\n"
        self.txtStatus.SetValue(hhh)
        Initialize_HeartBeat()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
