"""
File: calculatordemo.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame

class CalculatorDemo(EasyFrame):
    """Illustrates command buttons and user events."""

    def __init__(self):
        """Sets up the window, label, and buttons."""
        EasyFrame.__init__(self, "Calculator")
        self.digits = self.addLabel("", row = 0, column = 0,
                                    columnspan = 3, sticky = "NSEW")
        digit = 9
        for row in range(1, 4):
            for column in range(0, 3):
                button = self.addButton(str(digit), row, column)
                button["command"] = self.makeCommand(button)
                digit -= 1
        
    # Event handling method
    def makeCommand(self, button):
        """Define and return the event handler for the button."""
        def addDigit():
            self.digits["text"] = self.digits["text"] + button["text"]
        return addDigit

# Instantiates and pops up the window.
if __name__ == "__main__":
    CalculatorDemo().mainloop()
