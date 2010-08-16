import os, sys
import Tkinter
import Image, ImageTk
import ImageEnhance

def enhance(eimage):
    enh = ImageEnhance.Contrast(eimage)
    enh.enhance(1.3).show("30% more contrast")
    
def win1():
    top = Tkinter.Tk()
    image1 = Image.open("C:\Python26\image.jpg")
    top.geometry('%dx%d' % (image1.size[0],image1.size[1]))
    tkpi = ImageTk.PhotoImage(image1)
    label_image1 = Tkinter.Label(top, image=tkpi)
    label_image1.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
    top.title("window 1")
    startButton = Tkinter.Button(top, text="Start", command=win2)
    startButton.grid(row=1, column=7)
    leaveButton = Tkinter.Button(top, text="Quit", command=top.destroy)
    leaveButton.grid(row=1, column=1, sticky='nw')
    #b1Var = Tkinter.StringVar()
    #b2Var = Tkinter.StringVar()
    #b1Var.set('b1')
    #b2Var.set('b2')
    #box1Label = Tkinter.Label(top,textvariable=b1Var,width=12)
    #box1Label.grid(row=3, column=2)
    #box2Label = Tkinter.Label(top,textvariable=b2Var,width=12)
    #box2Label.grid(row=3, column=3)
    top.mainloop()

def win2():
    board = Tkinter.Toplevel()
    image2 = Image.open("C:\Python26\image2.jpg")
    board.geometry('%dx%d' % (image2.size[0],image2.size[1]))
    tkpi2 = ImageTk.PhotoImage(image2)
    label_image2 = Tkinter.Label(board, image=tkpi2)
    label_image2.place(x=0,y=0,width=image2.size[0],height=image2.size[1])
    board.title("window 2")
    startButton = Tkinter.Button(board, text="Start", command=enhance(image2))
    startButton.grid(row=1, column=7)
    board.mainloop()

try:
    win1()
except Exception, e:
    # This is used to skip anything not an image.
    # Image.open will generate an exception if it cannot open a file.
    # Warning, this will hide other errors as well.
    print "didnt work"
    pass
