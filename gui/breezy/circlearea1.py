"""
File: circlearea1.py

Inputs a radius of a circle and outputs its area.
"""

from breezypythongui import EasyFrame
import math

class CircleArea(EasyFrame):

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Circle Area")

        # Label and field for the radius
        self.addLabel(text = "Radius",
                      row = 0, column = 0)
        self.radiusField = self.addFloatField(value = 0.0,
                                              row = 0,
                                              column = 1,
                                              width = 10)

        # Label and field for the area
        self.addLabel(text = "Area",
                      row = 1, column = 0)
        self.areaField = self.addFloatField(value = 0.0,
                                            row = 1,
                                            column = 1)

        # The command button
        self.button = self.addButton(text = "Compute",
                                     row = 2, column = 0,
                                     columnspan = 2,
                                     command = self.computeArea)

    # The event handler method for the button
    def computeArea(self):
        """Inputs the radius, computes the area,
        and outputs the area."""
        radius = self.radiusField.getNumber()
        area = radius ** 2 * math.pi
        self.areaField.setNumber(area)

#Instantiate and pop up the window."""
CircleArea().mainloop()
