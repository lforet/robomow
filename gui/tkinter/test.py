import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from datetime import datetime



image = Image.open("temp.jpg")

top = Tkinter.Tk()
text1 = Tkinter.StringVar()
text1.set('Text')

i = 0

def helloCallBack():
	global i
   	#tkMessageBox.showinfo( "Hello Python", "Hello World")
   	print "do some stuff"
   	i = i + 1
   	#text1.set("New Text!")

	
def update_display():
		#global i
		text1.set( str(datetime.now()) )
		#top.update_idletasks()
		print "update called", i
		top.update()
		top.after(10, update_display)

B = Tkinter.Button(top, text="button1", command = helloCallBack)
L1 = Tkinter.Label(top, textvariable=text1).pack()


photo = ImageTk.PhotoImage(image)
label = Tkinter.Label(image=photo)
label.image = photo # keep a reference!
label.pack()
B.pack()
#first_run = False
if __name__== "__main__":
	update_display()
	#time.sleep(.01)
	print "hi"
	top.mainloop()
	print "out"
