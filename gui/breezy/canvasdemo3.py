"""
File: canvasdemo3.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame, EasyCanvas
import tkinter.colorchooser

class CanvasDemo(EasyFrame):
    """Draws ovals, rectangles, or line segments."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Canvas Demo 3")

        # Specialized canvas for drawing shapes
        self.shapeCanvas = ShapeCanvas(self)
        self.addCanvas(self.shapeCanvas, row = 0, column = 2,
                       rowspan = 8, width = 200)

        # Radio buttons, labels, fields, and color canvas
        self.shapeGroup = self.addRadiobuttonGroup(row = 5,
                                                   column = 0,
                                                   rowspan = 3)
        defaultRB = self.shapeGroup.addRadiobutton(
                                        text = "Line segment",
                                        command = self.chooseShape)
        self.shapeGroup.setSelectedButton(defaultRB)
        self.shapeGroup.addRadiobutton(text = "Rectangle",
                                       command = self.chooseShape)
        self.shapeGroup.addRadiobutton(text = "Oval",
                                       command = self.chooseShape)
        self.addLabel(text = "x0", row = 0, column = 0)
        self.addLabel(text = "y0", row = 1, column = 0)
        self.addLabel(text = "x1", row = 2, column = 0)
        self.addLabel(text = "y1", row = 3, column = 0)
        self.addLabel(text = "Color", row = 4, column = 0)
        self.x0Field = self.addIntegerField(0, row = 0, column = 1)
        self.y0Field = self.addIntegerField(0, row = 1, column = 1)
        self.x1Field = self.addIntegerField(0, row = 2, column = 1)
        self.y1Field = self.addIntegerField(0, row = 3, column = 1)
        self.colorCanvas = self.addCanvas(row = 4, column = 1,
                                          width = 45, height = 20,
                                          background = "black")
        
        
        # Command buttons
        self.addButton(text = "Choose color", row = 5, column = 1,
                       command = self.chooseColor)
        self.addButton(text = "Draw", row = 6, column = 1,
                       command = self.draw)
        self.addButton(text = "Erase all",
                       row = 7, column = 1,
                       command = self.eraseAll)

    # Event handling methods in the main window class

    def chooseShape(self):
        """Responds to a radio button click by updating the
        shape canvas with the selected shape type."""
        shapeType = self.shapeGroup.getSelectedButton()["text"]
        self.shapeCanvas.setShapeType(shapeType)

    def chooseColor(self):
        """Pops up a color chooser, outputs the result,
        and updates the two canvases."""
        colorTuple = tkinter.colorchooser.askcolor()
        if not colorTuple[0]: return
        hexString = colorTuple[1]
        self.colorCanvas["background"] = hexString
        self.shapeCanvas.setColor(hexString)

    def draw(self):
        """Draws a shape of the current type at the current position
        and in the current color."""
        x0 = self.x0Field.getNumber()
        y0 = self.y0Field.getNumber()
        x1 = self.x1Field.getNumber()
        y1 = self.y1Field.getNumber()
        self.shapeCanvas.draw(x0, y0, x1, y1)

    def eraseAll(self):
        """Deletes all shapes from the canvas."""
        self.shapeCanvas.eraseAll()

    
class ShapeCanvas(EasyCanvas):
    """Supports the drawing of different types of shapes."""

    def __init__(self, parent):
        """Sets up the canvas."""
        EasyCanvas.__init__(self, parent, background = "gray")
        self.shapeType = "Line segment"
        self.color = "black"
        self.shapes = list()

    def setColor(self, color):
        """Resets the color to the given color."""
        self.color = color

    def setShapeType(self, shapeType):
        """Resets the shape type to the given shape type."""
        self.shapeType = shapeType

    def draw(self, x0, y0, x1, y1):
        """Draws the shape at the given coordinates."""
        if self.shapeType == "Line segment":
            shape = self.drawLine(x0, y0, x1, y1, self.color)
        elif self.shapeType == "Rectangle":
            shape = self.drawRectangle(x0, y0, x1, y1, self.color)
        else:
            shape = self.drawOval(x0, y0, x1, y1, self.color)
        self.shapes.append(shape)

    def eraseAll(self):
        """Deletes all shapes from the canvas."""
        for shape in self.shapes:
            self.delete(shape)
        self.shapes = list()


# Instantiate and pop up the window."""
if __name__ == "__main__":
    CanvasDemo().mainloop()
