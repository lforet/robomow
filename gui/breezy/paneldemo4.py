"""
File: paneldemo4.py

Calculates the attributes of a sphere.  Uses a panel to organize the
command buttons.
"""

from breezypythongui import EasyFrame, EasyDialog
import math

class PanelDemo(EasyFrame):

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self)

        self.addButton(text = "Press me", row = 0, column = 0,
                       command = self.modify)
        
    # Event handling method.
    def modify(self):
        """Pops up a dialog to edit the model."""
        dialog = PanelDialog(self)

class PanelDialog(EasyDialog):
    """Opens a dialog."""

    def __init__(self, parent):
        """Sets up the window."""
        EasyDialog.__init__(self, parent, "Sphere calculations")
    
    def body(self, master):
        """Sets up the widgets."""
        # Label and field for the radius
        self.addLabel(master, text = "Radius",
                      row = 0, column = 0)
        self.radiusField = self.addFloatField(master, value = 0.0,
                                              row = 0,
                                              column = 1)
        # Label and field for the output
        self.outputLabel = self.addLabel(master, text = "Diameter",
                                         row = 1, column = 0)
        self.outputField = self.addFloatField(master, value = 0.0,
                                              row = 1,
                                              column = 1)
        # Panel for the command buttons
        buttonPanel = self.addPanel(master, row = 2, column = 0,
                                    columnspan = 2)
        # The command buttons
        buttonPanel.addButton(text = "Diameter",
                              row = 0, column = 0,
                              command = self.computeDiameter)
        buttonPanel.addButton(text = "Area",
                              row = 0, column = 1,
                              command = self.computeArea)
        buttonPanel.addButton(text = "Volume",
                              row = 0, column = 2,
                              command = self.computeVolume)

    def apply(self):
        """Transfers data from the fields to the CD."""
        self.setModified()
        
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
