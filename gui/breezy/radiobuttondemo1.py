"""
File: radiobuttondemo1.py

Demonstrates radio button capabilities.
"""

from breezypythongui import EasyFrame

class RadiobuttonDemo(EasyFrame):
    """When the Display button is pressed, shows the label of
    the selected radio button.  The button group has a default
    vertical alignment."""
    
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, "Radio Button Demo")
        
        # Add the button group
        self.group = self.addRadiobuttonGroup(row = 0, column = 0, rowspan = 4)

        # Add the radio buttons to the group
        self.group.addRadiobutton("Freshman")
        self.group.addRadiobutton("Sophomore")
        self.group.addRadiobutton("Junior")
        defaultRB = self.group.addRadiobutton("Senior")

        # Select one of the buttons in the group
        self.group.setSelectedButton(defaultRB)
        
        # Output field and command button for the results
        self.output = self.addTextField("", row = 0, column = 1)
        self.addButton("Display", row = 1, column = 1,
                       command = self.displayButton)

    # Event handler method

    def displayButton(self):
        """Display the label of the selected button."""
        selectedButton = self.group.getSelectedButton()
        self.output.setText(selectedButton["text"])
                
# Instantiate and pop up the window."""
RadiobuttonDemo().mainloop()
