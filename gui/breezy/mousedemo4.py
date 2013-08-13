"""
File: mousedemo4.py
uthor: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame, EasyCanvas
import random

class MouseDemo(EasyFrame):
    """Draws ovals in random colors, erases them, or moves them."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Mouse Demo 4")

        # Canvas
        self.shapeCanvas = ShapeCanvas(self)
        self.addCanvas(self.shapeCanvas, row = 0, column = 0,
                       columnspan = 2, width = 300, height = 150)
        
        # Radio buttons
        self.commandGroup = self.addRadiobuttonGroup(row = 1,
                                                     column = 0,
                                                     rowspan = 2,
                                                     orient = "horizontal")
        defaultRB = self.commandGroup.addRadiobutton(text = "Draw",
                                                     command = self.chooseCommand)
        self.commandGroup.setSelectedButton(defaultRB)
        self.commandGroup.addRadiobutton(text = "Move",
                                         command = self.chooseCommand)
        self.commandGroup.addRadiobutton(text = "Erase",
                                         command = self.chooseCommand)

    # Event handling method in the main window class
    def chooseCommand(self):
        """Responds to a radio button click by updating the
        shape canvas with the selected command."""
        command = self.commandGroup.getSelectedButton()["text"]
        self.shapeCanvas.setCommand(command)


class ShapeCanvas(EasyCanvas):
    """Draw an oval with a press, drag, and release of the mouse, when
    Draw is selected.  Erase with a mouse press when Erase is selected.
    Move with a press and drag when Move is selected."""

    def __init__(self, parent):
        """Sets up the canvas."""
        EasyCanvas.__init__(self, parent, background = "gray")
        self.command = "Draw"
        self.items = list()
        self.selectedItem = None

    def setCommand(self, command):
        """Resets the command."""
        self.command = command

    def mousePressed(self, event):
        """Sets the first corner of the oval's bounding rectangle.
        If the command is Erase, erases the oval.  Otherwise, if
        the command is Move, sets the selected shape."""
        self.x = event.x
        self.y = event.y
        if self.command == "Erase":
            selectedItem = self.findItemId(self.x, self.y)
            if selectedItem:
                self.items.remove(selectedItem)
                self.delete(selectedItem)
        elif self.command == "Move":
            self.selectedItem = self.findItemId(self.x, self.y)


    def mouseReleased(self, event):
        """If the command is draw, sets the second corner of the
        oval's bounding rectangle. Draws an oval filled in a
        random color and saves its item ID.  Otherwise, if the
        command is Move, deselects the selected shape."""
        if self.command == "Draw":
            if self.x != event.x and self.y != event.y:
                color = self.getRandomColor()
                itemId = self.drawOval(self.x, self.y,
                                       event.x, event.y, fill = color)
                self.items.append(itemId)
        elif self.command == "Move":
            self.selectedItem = None

    def mouseDragged(self, event):
        """If the command is Move, moves the selected shape to the new
        location."""
        if self.command == "Move" and self.selectedItem:
            xDistance = event.x - self.x
            yDistance = event.y - self.y
            self.move(self.selectedItem, xDistance, yDistance)
            self.x = event.x
            self.y = event.y

    def findItemId(self, x, y):
        """If the coordinates are in a shape's bounding rectangle,
        returns its item ID; otherwise, returns None."""
        for itemId in self.items:
            coords = self.coords(itemId)
            if self.containsPoint(coords, x, y):
                return itemId
        return None

    def containsPoint(self, coords, x, y):
        """Returns True if (x, y) is contained in the rectangle
        defined by coords, or False otherwise."""
        [x0, y0, x1, y1] = coords
        return x >= min(x0, x1) and x <= max(x0, x1) \
               and y >= min(y0, y1) and y <= max (y0, y1)        

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
