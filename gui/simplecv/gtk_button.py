from SimpleCV import *
from imagegtk import DisplayImage

im = Image("Lenna")
image = im.toRGB.getBitmap()

d = DisplayImage(title="iamgegtk")

label = gtk.Label("Lenna")
d.box.pack_start(label,False,False,0)

but1 = gtk.Button("Quit")
but1.connect("clicked",d.leave_app)
d.box.pack_end(but1,False,False,2)

d.show(image)
