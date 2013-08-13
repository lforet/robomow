"""
File: mousedemo2.py
uthor: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame, EasyCanvas
import random

class MouseDemo(EasyFrame):
    """Draws ovals in random colors."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Mouse Demo 2")

        # Canvas
        self.shapeCanvas = ShapeCanvas(self)
        self.addCanvas(self.shapeCanvas, row = 0, column = 0,
                       width = 300, height = 150)


class ShapeCanvas(EasyCanvas):
    """Draw an oval with a press, drag, and release of the mouse."""

    def __init__(self, parent):
        """Sets up the canvas."""
        EasyCanvas.__init__(self, parent, background = "gray")

    def mousePressed(self, event):
        """Sets the first corner of the oval's bounding rectangle."""
        self.x = event.x
        self.y = event.y

    def mouseReleased(self, event):
        """Sets the second corner of the oval's bounding rectangle.
        Draws an oval filled in a random color."""
        if self.x != event.x and self.y != event.y:
            color = self.getRandomColor()
            self.drawOval(self.x, self.y,
                          event.x, event.y, fill = color)

    def getRandomColor(self):
        """Returns a random RGB color."""
        hexR = hex(random.randint(0, 255))[2:]
        hexG = hex(random.randint(0, 255))[2:]
        hexB = hex(random.randint(0, 255))[2:]
        if len(hexR) == 1: hexR = "0" + hexR
        if len(hexG) == 1: hexG = "0" + hexG
        if len(hexB) == 1: hexB = "0" + hexB
        return "#" + hexR + hexG + hexB


# Instantiate and pop up the window."""
if __name__ == "__main__":
    MouseDemo().mainloop()
