"""
File: radiobuttondemo2.py

Demonstrates radio button capabilities.
"""

from breezypythongui import EasyFrame
from tkinter import HORIZONTAL

class RadiobuttonDemo(EasyFrame):
    """When the Display button is pressed, shows the label of
    the selected radio button.  The button group has a 
    horizontal alignment."""
    
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, "Radio Button Demo")
        
        # Add the button group
        self.group = self.addRadiobuttonGroup(row = 1, column = 0,
                                              columnspan = 4,
                                              orient = HORIZONTAL)

        # Add the radio buttons to the group
        self.group.addRadiobutton("Freshman")
        self.group.addRadiobutton("Sophomore")
        self.group.addRadiobutton("Junior")
        defaultRB = self.group.addRadiobutton("Senior")

        # Select one of the buttons in the group
        self.group.setSelectedButton(defaultRB)
        
        # Output field and command button for the results
        self.output = self.addTextField("", row = 0, column = 1)
        self.addButton("Display", row = 0, column = 0,
                       command = self.display)

    # Event handler method

    def display(self):
        """Displays the selected button's label in the text field."""
        self.output.setText(self.group.getSelectedButton()["value"])
                
# Instantiate and pop up the window.
RadiobuttonDemo().mainloop()
