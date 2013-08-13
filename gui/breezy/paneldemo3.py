"""
File: paneldemo3.py

Calculates the attributes of a sphere.  Uses a panel to organize the
data labels and fields.
"""

from breezypythongui import EasyFrame
import math

class PanelDemo(EasyFrame):

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Sphere Attributes")

        # Panel for the labels and fields
        dataPanel = self.addPanel(row = 0, column = 0,
                                  columnspan = 3)

        # Label and field for the radius
        dataPanel.addLabel(text = "Radius",
                           row = 0, column = 0)
        self.radiusField = dataPanel.addFloatField(value = 0.0,
                                                   row = 0,
                                                   column = 1)

        # Label and field for the output
        self.outputLabel = dataPanel.addLabel(text = "Diameter",
                                              row = 1, column = 0)
        self.outputField = dataPanel.addFloatField(value = 0.0,
                                                   row = 1,
                                                   column = 1)
        # The command buttons
        self.addButton(text = "Diameter",
                              row = 1, column = 0,
                              command = self.computeDiameter)
        self.addButton(text = "Area",
                       row = 1, column = 1,
                       command = self.computeArea)
        self.addButton(text = "Volume",
                       row = 1, column = 2,
                       command = self.computeVolume)
        
    # The event handler methods for the buttons
    def computeDiameter(self):
        """Inputs the radius, computes the diameter,
        and outputs the result."""
        radius = self.radiusField.getNumber()
        diameter = radius * 2
        self.outputField.setNumber(diameter)
        self.outputLabel["text"] = "Diameter"

    def computeArea(self):
        """Inputs the radius, computes the area,
        and outputs the result."""
        radius = self.radiusField.getNumber()
        area = 4 * radius ** 2 * math.pi
        self.outputField.setNumber(area)
        self.outputLabel["text"] = "Area"

    def computeVolume(self):
        """Inputs the radius, computes the volume,
        and outputs the result."""
        radius = self.radiusField.getNumber()
        volume = 4/3 * radius ** 3 * math.pi
        self.outputField.setNumber(volume)
        self.outputLabel["text"] = "Volume"

#Instantiate and pop up the window."""
PanelDemo().mainloop()
