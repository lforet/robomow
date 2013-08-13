"""
File: songbrowser1.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame
from tkinter import END, NORMAL, DISABLED
import tkinter.filedialog
from song import SongDatabase, Song

class SongBrowser(EasyFrame):
    """Allows the user to browse songs in a database file, delete them,
    and save the database to a file."""

    def __init__(self):
        """Sets up the window and the widgets."""
        EasyFrame.__init__(self, title = "Song Browser",
                           width = 300, height = 150)

        # Create a model
        self.database = SongDatabase()
        self.selectedTitle = None

        # Set up the menus
        menuBar = self.addMenuBar(row = 0, column = 0, columnspan = 2)
        fileMenu = menuBar.addMenu("File")
        fileMenu.addMenuItem("Open", self.openFile)
        fileMenu.addMenuItem("Save", self.saveFile)
        fileMenu.addMenuItem("Save As...", self.saveFileAs)
        
        self.editMenu = menuBar.addMenu("Edit", state = DISABLED)
        self.editMenu.addMenuItem("Find", self.findSong)
        self.editMenu.addMenuItem("Delete", self.deleteSong)

        # Set up the list box
        self.listBox = self.addListbox(row = 1, column = 0, width = 20,
                                       listItemSelected = self.listItemSelected)

        # Set the text area
        self.outputArea = self.addTextArea("", row = 1, column = 1,
                                           width = 30, height = 4)


    # Event handling methods
    def listItemSelected(self, index):
        """Responds to the selection of an item in the list box.
        Updates the selected title and the text area with the
        current song's info."""
        self.selectedTitle = self.listBox.getSelectedItem()
        if self.selectedTitle == "":
            self.outputArea.setText("")
        else:
            self.outputArea.setText(str(self.database[self.selectedTitle]))

    def openFile(self):
        """Pops up an open file dialog.  Updates the view if
        a file is opened."""
        filetypes = [("Database files", "*.dat")]
        fileName = tkinter.filedialog.askopenfilename(parent = self,
                                                      filetypes = filetypes)
        if fileName == "": return
        self.database = SongDatabase(fileName)
        self.listBox.clear()
        for title in self.database.getTitles():
            self.listBox.insert(END, title)
        self.listBox.setSelectedIndex(0)
        self.listItemSelected(0)
        if self.listBox.size() > 0:
            self.editMenu["state"] = NORMAL
        else:
            self.editMenu["state"] = DISABLED

    def saveFile(self):
        """If the database has a file name, saves it to the file.
        Otherwise, calls saveFileAs to prompt the user for a file
        name."""
        if self.database.fileName != "":
            self.database.save()
        else:
            self.saveFileAs()

    def saveFileAs(self):
        """Pops up a dialog to save the database to a file."""
        fileName = tkinter.filedialog.asksaveasfilename(parent = self)
        if fileName != "":
            self.database.save(fileName)

    def findSong(self):
        """Prompts the user for a title and searches for the song.
        Selects and updates if found."""
        title = self.prompterBox(title = "Find",
                                 promptString = "Enter a song's title")
        if title == "": return
        song = self.database[title]
        if not song:
            self.messageBox(message = title + " was not found")
        else:
            index = self.listBox.getIndex(title)
            self.listBox.setSelectedIndex(index)            
            self.listItemSelected(index)

    def deleteSong(self):
        """Deletes the selected song from the database and updates the view."""
        if self.selectedTitle:
            self.database.pop(self.selectedTitle)
            index = self.listBox.getSelectedIndex()
            self.listBox.delete(index)
            if self.listBox.size() > 0:
                if index > 0:
                    index -= 1
                self.listBox.setSelectedIndex(index)
                self.listItemSelected(index)
            else:
                self.listItemSelected(-1)
                self.editMenu["state"] = DISABLED


# Instantiate and pop up the window."""
if __name__ == "__main__":
    SongBrowser().mainloop()
