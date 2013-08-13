"""
File: scaledemo1.py

Displays the area of a circle whose radius is input from a sliding scale.
"""

from breezypythongui import EasyFrame
import math

class CircleArea(EasyFrame):

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Circle Area")

        # Label and field for the area
        self.addLabel(text = "Area",
                      row = 0, column = 0)
        self.areaField = self.addFloatField(value = 0.0,
                                            row = 0,
                                            column = 1,
                                            width = 20)

        # Sliding scale for the radius
        self.radiusScale = self.addScale(label = "Radius",
                                         row = 1, column = 0,
                                         columnspan = 2,
                                         from_ = 0, to = 100,
                                         length = 300,
                                         tickinterval = 10,
                                         command = self.computeArea)


    # The event handler method for the sliding scale
    def computeArea(self, radius):
        """Inputs the radius, computes the area,
        and outputs the area."""
        # radius is the current value of the scale, as a string.
        area = float(radius) ** 2 * math.pi
        self.areaField.setNumber(area)

# Instantiate and pop up the window."""
CircleArea().mainloop()
