"""
File: canvasdemo2.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame
import random

class CanvasDemo(EasyFrame):
    """Draws filled ovals on a canvas, and allows the user to erase
    them all."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Canvas Demo 2")
        self.colors = ("blue", "green", "red", "yellow")
        self.shapes = list()

        # Canvas
        self.canvas = self.addCanvas(row = 0, column = 0,
                                     columnspan = 2,
                                     width = 300, height = 150,
                                     background = "gray")
        
        # Command buttons
        self.addButton(text = "Draw oval", row = 1, column = 0,
                       command = self.drawOval)
        self.addButton(text = "Erase all", row = 1, column = 1,
                       command = self.eraseAll)

    # Event handling method
    def drawOval(self):
        """Draws a filled oval at a random position."""
        x = random.randint(0, 300)
        y = random.randint(0, 150)
        color = random.choice(self.colors)
        shape = self.canvas.drawOval(x, y, x + 25, y + 25, fill = color)
        self.shapes.append(shape)

    def eraseAll(self):
        """Deletes all ovals from the canvas."""
        for shape in self.shapes:
            self.canvas.delete(shape)
        self.shapes = list()


# Instantiate and pop up the window."""
if __name__ == "__main__":
    CanvasDemo().mainloop()
