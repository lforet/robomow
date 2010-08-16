#!/usr/bin/python

# communicate.py

import wx
import os

ID_NEW = 1
ID_RENAME = 2
ID_CLEAR = 3
ID_DELETE = 4
ID_BROWSE = 5

class Communicate(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(480, 400))

        self.PhotoMaxSize = 240

        panel = wx.Panel(self, -1)
        #hbox = wx.BoxSizer(wx.HORIZONTAL)
        #hbox = wx.BoxSizer()
        self.listbox = wx.ListBox(panel, -1)
        #hbox.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 50)
        #hbox.Add(self.listbox, 1)
        instructions = 'Browse for an image'
        img = wx.EmptyImage(240,240)
        self.imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img))
 
        instructLbl = wx.StaticText(panel, label=instructions)
        self.photoTxt = wx.TextCtrl(panel, size=(200,-1))
        
     
        #hbox.Add(leftPanel, 1, wx.EXPAND | wx.ALL, 5)
        #hbox.Add(self.rightPanel, 1, wx.EXPAND | wx.ALL, 5)
        btnPanel = wx.Panel(panel, -1)
        #vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        new = wx.Button(btnPanel, ID_NEW, 'New', size=(90, 30))
        ren = wx.Button(btnPanel, ID_RENAME, 'Rename', size=(90, 30))
        dlt = wx.Button(btnPanel, ID_DELETE, 'Delete', size=(90, 30))
        clr = wx.Button(btnPanel, ID_CLEAR, 'Clear', size=(90, 30))
        #browseBtn = wx.Button(btnPanel, ID_BROWSE, 'Browse', size=(90,30))

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.OnRename, id=ID_RENAME)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=ID_CLEAR)
        #self.Bind(wx.EVT_BUTTON, self.onBrowse) 
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)



        vbox.Add((-1, 20))
        vbox.Add(new)
        vbox.Add(ren, 0, wx.TOP, 5)
        vbox.Add(dlt, 0, wx.TOP, 5)
        vbox.Add(clr, 0, wx.TOP, 5)
        #vbox.Add(browseBtn, 0, wx.TOP, 5)
        vbox.Add(self.photoTxt, 0, wx.TOP, 5)
        vbox.Add(self.imageCtrl, 0, wx.ALL, 5)
        vbox.Add(self.listbox, 1)

        btnPanel.SetSizer(vbox)
        #hbox.Add(btnPanel, .1, wx.EXPAND | wx.RIGHT, 120)
        panel.SetSizer(vbox)
        #self.createWidgets()
        #self.frame.Show()

 
        #self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        #self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        #vbox.Add(wx.StaticLine(panel, wx.ID_ANY),
        #                   0, wx.ALL|wx.EXPAND, 5)
        #self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        #
        #self.sizer.Add(self.photoTxt, 100, wx.ALL, 5)
        
        #self.sizer.Add(browseBtn, 0, wx.ALL, 5)
        #self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
 
        #panel.SetSizer(self.mainSizer)
        #self.mainSizer.Fit(self.frame)
 
        #self.panel.Layout()

        self.Centre()
        self.Show(True)

    def NewItem(self, event):
        text = wx.GetTextFromUser('Enter a new item', 'Insert dialog')
        if text != '':
            self.listbox.Append(text)

    def OnRename(self, event):
        sel = self.listbox.GetSelection()
        text = self.listbox.GetString(sel)
        renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)
        if renamed != '':
            self.listbox.Delete(sel)
            self.listbox.Insert(renamed, sel)


    def OnDelete(self, event):
        sel = self.listbox.GetSelection()
        if sel != -1:
            self.listbox.Delete(sel)

    def OnClear(self, event):
        self.listbox.Clear()

    def onBrowse(self, event):
        """
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())

            print "file name gotten from dialog"
            self.listbox.Append(dialog.GetPath())
        dialog.Destroy()
        self.onView()
 
    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        #self.panel.Refresh()

app = wx.App()
#ListBox(None, -1, 'ListBox')
Communicate(None, -1, 'widgets communicate')
app.MainLoop()

