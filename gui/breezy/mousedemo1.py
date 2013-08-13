"""
File: mousedemo1.py
uthor: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame, EasyCanvas

class MouseDemo(EasyFrame):
    """Draws coordinates of mouse presses on a canvas."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Mouse Demo 1")

        # Canvas
        self.shapeCanvas = ShapeCanvas(self)
        self.addCanvas(self.shapeCanvas, row = 0, column = 0,
                       width = 300, height = 150)


class ShapeCanvas(EasyCanvas):
    """Displays the coordinates of the point where the mouse is pressed."""

    def __init__(self, parent):
        """Background is gray."""
        EasyCanvas.__init__(self, parent, background = "gray") 

    def mousePressed(self, event):
        """Draws the coordinates of the mouse press."""
        coordString = "(" + str(event.x) + "," + str(event.y) + ")"
        self.drawText(coordString, event.x, event.y)


# Instantiate and pop up the window."""
if __name__ == "__main__":
    MouseDemo().mainloop()
