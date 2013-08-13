"""
File: layoutdemo.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame

class LayoutDemo(EasyFrame):
    """Displays label in the quadrants."""

    def __init__(self):
        """Sets up the window and the labels."""
        EasyFrame.__init__(self)
        self.addLabel(text = "(0, 0)", row = 0, column = 0)
        self.addLabel(text = "(0, 1)", row = 0, column = 1)
        self.addLabel(text = "(1, 0)", row = 1, column = 0)
        self.addLabel(text = "(1, 1)", row = 1, column = 1)

# Instantiates and pops up the window.
if __name__ == "__main__":
    LayoutDemo().mainloop()
