"""
File: checkbuttondemo.py

Demonstrates check button capabilities.
"""

from breezypythongui import EasyFrame

class CheckbuttonDemo(EasyFrame):
    """When the display button is pressed, shows the label of
    the selected radio button.  The button group has a default
    vertical alignment."""
    
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, "Check Button Demo")
        
        # Add two check buttons
        self.firstCB = self.addCheckbutton(text = "First",
                                           row = 0, column = 0,
                                           command = self.first)

        self.secondCB = self.addCheckbutton(text = "Second",
                                            row = 1, column = 0,
                                            command = self.second)

    # Event handler methods

    def first(self):
        """Display a message box with the state of the check button."""
        if self.firstCB.isChecked():
            message = "First has been checked"
        else:
            message = "First has been unchecked"
        self.messageBox(title = "State of First", message = message)
                
    def second(self):
        """Display a message box with the state of the check button."""
        if self.secondCB.isChecked():
            message = "Second has been checked"
        else:
            message = "Second has been unchecked"
        self.messageBox(title = "State of Second", message = message)


# Instantiate and pop up the window."""
CheckbuttonDemo().mainloop()
