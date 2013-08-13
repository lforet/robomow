"""
File: filedialogdemo.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame
import tkinter.filedialog

class FileDialogDemo(EasyFrame):
    """Demonstrates a file dialog."""
    
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, "File Dialog Demo")
        self.outputArea = self.addTextArea("", row = 0, column = 0,
                                           columnspan = 2,
                                           width = 80, height = 15)
        self.addButton(text = "Open", row = 1, column = 0,
                       command = self.openFile)
        self.addButton(text = "Save As...", row = 1, column = 1,
                       command = self.saveFileAs)

    # Event handling methods
    def openFile(self):
        """Pops up an open file dialog, and if a file is selected,
        displays its text in the text area."""
        filetypes = [("Python files", "*.py"), ("Text files", "*.txt")]
        fileName = tkinter.filedialog.askopenfilename(parent = self,
                                                      filetypes = filetypes)
        if fileName != "":
            file = open(fileName, "r")
            text = file.read()
            file.close()
            self.outputArea.setText(text)
            self.setTitle(fileName)

    def saveFileAs(self):
        """Pops up a save file dialog, and if a file is selected,
        saves the contents of the text area to the file."""
        fileName = tkinter.filedialog.asksaveasfilename(parent = self)
        if fileName != "":
            text = self.outputArea.getText()
            file = open(fileName, "w")
            file.write(text)
            file.close()
            self.setTitle(fileName)

if __name__ == "__main__":
    FileDialogDemo().mainloop()
   
