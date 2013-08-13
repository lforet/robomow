"""
File: scaledemo1.py

Displays a color whose RGB values are input from sliding scales.
"""

from breezypythongui import EasyFrame
from tkinter import VERTICAL

class ColorMeter(EasyFrame):

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Color Meter")

        # Label to display the RGB value
        self.rgbLabel = self.addLabel(text = "RGB : x000000",
                                      row = 0, column = 0)

        # Canvas to display the color
        self.canvas = self.addCanvas(row = 1, column = 0)
        self.canvas["bg"] = "black"

        # Sliding scale for red
        self.redScale = self.addScale(label = "Red",
                                      row = 0, column = 1,
                                      orient = VERTICAL,
                                      from_ = 0, to = 255,
                                      length = 300,
                                      tickinterval = 15,
                                      command = self.setColor)


        # Sliding scale for green
        self.greenScale = self.addScale(label = "Green",
                                        row = 0, column = 2,
                                        orient = VERTICAL,
                                        from_ = 0, to = 255,
                                        length = 300,
                                        tickinterval = 15,
                                        command = self.setColor)

        # Sliding scale for blue
        self.blueScale = self.addScale(label = "Blue",
                                       row = 0, column = 3,
                                       orient = VERTICAL,
                                       from_ = 0, to = 255,
                                       length = 300,
                                       tickinterval = 15,
                                       command = self.setColor)


    # Event handler for the three sliding scales
    def setColor(self, value):
        """Gets the RGB values from the scales,
        converts them to hex, and builds a six-digit
        hex string to update the view."""
        red = hex(self.redScale.get())[2:]
        green = hex(self.greenScale.get())[2:]
        blue = hex(self.blueScale.get())[2:]
        if len(red) == 1:
            red = "0" + red
        if len(green) == 1:
            green = "0" + green
        if len(blue) == 1:
            blue = "0" + blue
        color = "#" + red + green + blue
        self.rgbLabel["text"] = "RGB: " + color
        self.canvas["bg"] = color
        

# Instantiate and pop up the window.
ColorMeter().mainloop()
