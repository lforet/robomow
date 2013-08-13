"""
File: canvasdemo1.py
uthor: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame
import random

class CanvasDemo(EasyFrame):
    """Draws filled ovals on a canvas."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Canvas Demo 1")
        self.colors = ("blue", "green", "red", "yellow")

        # Canvas
        self.canvas = self.addCanvas(row = 0, column = 0,
                                     width = 300, height = 150,
                                     background = "gray")
        
        # Command button
        self.ovalButton = self.addButton(text = "Draw oval",
                                         row = 1, column = 0,
                                         command = self.drawOval)        

    # Event handling method
    def drawOval(self):
        """Draws a filled oval at a random position."""
        x = random.randint(0, 300)
        y = random.randint(0, 150)
        color = random.choice(self.colors)
        self.canvas.drawOval(x, y, x + 25, y + 25, fill = color)

# Instantiate and pop up the window."""
if __name__ == "__main__":
    CanvasDemo().mainloop()
