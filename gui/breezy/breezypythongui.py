"""
File: breezypythongui.py
Version: 1.1
Copyright 2012, 2013 by Ken Lambert

Resources for easy Python GUIs.

LICENSE: This is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).  Its capabilities mirror those 
of BreezyGUI and BreezySwing, open-source frameworks for writing GUIs in Java,
written by Ken Lambert and Martin Osborne.

PLATFORMS: The package is a wrapper around Tkinter (Python 3.X) and should
run on any platform where Tkinter is available.

INSTALLATION: Put this file where Python can see it.

RELEASE NOTES: Version 1.1 now includes the class EasyPanel, for organizing
subpanes in windows and dialogs (updated 12-19-2012).  Version 1.1 now also
runs on either Python 3.x.x or Python 2.x.x (updated 2-4-2013).

"""

import sys
versionNumber = sys.version_info.major
if versionNumber == 3:
    import tkinter
    import tkinter.simpledialog
    Tkinter = tkinter
    tkSimpleDialog = tkinter.simpledialog
else:
    import Tkinter
    import tkSimpleDialog

N = Tkinter.N
S = Tkinter.S
E = Tkinter.E
W = Tkinter.W
CENTER = Tkinter.CENTER
END = Tkinter.END
NORMAL = Tkinter.NORMAL
DISABLED = Tkinter.DISABLED
NONE = Tkinter.NONE
WORD = Tkinter.WORD
VERTICAL = Tkinter.VERTICAL
HORIZONTAL = Tkinter.HORIZONTAL
RAISED = Tkinter.RAISED
SINGLE = Tkinter.SINGLE
ACTIVE = Tkinter.ACTIVE

class EasyFrame(Tkinter.Frame):
    """Represents an application window."""

    def __init__(self, title = "", width = None, height = None,
                 background = "white", resizable = True):
        """Will shrink wrap the window around the widgets if width
        and height are not provided."""
        Tkinter.Frame.__init__(self, borderwidth = 4, relief = "sunken")
        if width and height:
            self.setSize(width, height)
        self.master.title(title)
        self.grid()
        # Expand the frame within the window
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.grid(sticky = N+S+E+W)
        # Set the background color and resizability
        self.setBackground(background)
        self.setResizable(resizable)

    def setBackground(self, color):
        """Resets the window's background color to color."""
        self["background"] = color

    def setResizable(self, state):
        """Resets the window's resizable property to True
        or False."""
        self.master.resizable(state, state)

    def setSize(self, width, height):
        """Resets the window's width and height in pixels."""
        self.master.geometry(str(width)+ "x" + str(height))

    def setTitle(self, title):
        """Resets the window's title to title."""
        self.master.title(title)

    # Methods to add widgets to the window.  The row and column in
    # the grid are required arguments.

    def addLabel(self, text, row, column,
                 columnspan = 1, rowspan = 1,
                 sticky = N+W, font = None,
                 background = "white", foreground = "black"):
        """Creates and inserts a label at the row and column,
        and returns the label."""
        label = Tkinter.Label(self, text = text, font = font,
                              background = background,
                              foreground = foreground)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        label.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return label

    def addButton(self, text, row, column,
                  columnspan = 1, rowspan = 1,
                  command = lambda: None,
                  state = NORMAL):
        """Creates and inserts a button at the row and column,
        and returns the button."""
        button = Tkinter.Button(self, text = text,
                                command = command, state = state)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        button.grid(row = row, column = column,
                    columnspan = columnspan, rowspan = rowspan,
                    padx = 5, pady = 5)
        return button

    def addFloatField(self, value, row, column,
                      columnspan = 1, rowspan = 1,
                      width = 20, precision = None,
                      sticky = N+E, state = NORMAL):
        """Creates and inserts a float field at the row and column,
        and returns the float field."""
        field = FloatField(self, value, width, precision, state)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addIntegerField(self, value, row, column,
                        columnspan = 1, rowspan = 1,
                        width = 10, sticky = N+E, state = NORMAL):
        """Creates and inserts an integer field at the row and column,
        and returns the integer field."""
        field = IntegerField(self, value, width, state)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addTextField(self, text, row, column,
                     columnspan = 1, rowspan = 1,
                     width = 20, sticky = N+E, state = NORMAL):
        """Creates and inserts a text field at the row and column,
        and returns the text field."""
        field = TextField(self, text, width, state)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addTextArea(self, text, row, column, rowspan = 1, columnspan = 1,
                    width = 80, height = 5, wrap = NONE):
        """Creates and inserts a multiline text area at the row and column,
        and returns the text area.  Vertical and horizontal scrollbars are
        provided."""
        frame = Tkinter.Frame(self)
        frame.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   sticky = N+S+E+W)
        self.columnconfigure(column, weight = 1)
        self.rowconfigure(row, weight = 1)
        xScroll = Tkinter.Scrollbar(frame, orient = HORIZONTAL)
        xScroll.grid(row = 1, column = 0, sticky = E+W)
        yScroll = Tkinter.Scrollbar(frame, orient = VERTICAL)
        yScroll.grid(row = 0, column = 1, sticky = N+S)
        area = TextArea(frame, text, width, height,
                        xScroll.set, yScroll.set, wrap)
        area.grid(row = 0, column = 0,
                  padx = 5, pady = 5, sticky = N+S+E+W)
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        xScroll["command"] = area.xview
        yScroll["command"] = area.yview
        return area

    def addListbox(self, row, column, rowspan = 1, columnspan = 1,
                   width = 10, height = 5, listItemSelected = lambda index: index):
        """Creates and inserts a scrolling list box at the row and column, with a
        width and height in lines and columns of text, and a default item selection
        method, and returns the list box."""
        frame = Tkinter.Frame(self)
        frame.grid(row = row, column = column, columnspan = columnspan, rowspan = rowspan,
                   sticky = N+S+E+W)
        self.columnconfigure(column, weight = 1)
        self.rowconfigure(row, weight = 1)
        yScroll = Tkinter.Scrollbar(frame, orient = VERTICAL)
        yScroll.grid(row = 0, column = 1, sticky = N+S)
        listBox = EasyListbox(frame, width, height, yScroll.set, listItemSelected)
        listBox.grid(row = 0, column = 0, sticky = N+S+E+W)
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        yScroll["command"] = listBox.yview
        return listBox

    def addCanvas(self, canvas = None, row = 0, column = 0,
                  rowspan = 1, columnspan = 1, width = 200, height = 100,
                  background = "white"):
        """Creates and inserts a canvas at the row and column,
        and returns the canvas."""
        if not canvas:
            canvas = EasyCanvas(self, width = width, height = height,
                                background = background)
        canvas.grid(row = row, column = column,
                    rowspan = rowspan, columnspan = columnspan,
                    sticky = W+E+N+S)
        self.columnconfigure(column, weight = 10)
        self.rowconfigure(row, weight = 10)
        return canvas

    def addScale(self, row, column, rowspan = 1, columnspan = 1,
                 command = lambda value: value, from_ = 0, to = 0,
                 label = "", length = 100, orient = HORIZONTAL,
                 resolution = 1, tickinterval = 0):
        """Creates and inserts a scale at the row and column,
        and returns the scale."""
        scale = Tkinter.Scale(self, command = command, from_ = from_, to = to,
                              label = label, length = length,
                              orient = orient, resolution = resolution,
                              tickinterval = tickinterval, relief = "sunken",
                              borderwidth = 4)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        scale.grid(row = row, column = column, columnspan = columnspan,
                   rowspan = rowspan, sticky = N+S+E+W)
        return scale

    def addMenuBar(self, row, column, rowspan = 1, columnspan = 1,
                   orient = "horizontal"):
        """Creates and inserts a menu bar at the row and column,
        and returns the menu bar."""
        if not orient in ("horizontal", "vertical"):
            raise ValueError("orient must be horizontal or vertical")
        menuBar = EasyMenuBar(self, orient)
        menuBar.grid(row = row, column = column,
                     rowspan = rowspan, columnspan = columnspan,
                     sticky = N+W)
        return menuBar

    def addCheckbutton(self, text, row, column,
                       rowspan = 1, columnspan = 1,
                       sticky = N+S+E+W, command = lambda : 0):
        """Creates and inserts check button at the row and column,
        and returns the check button."""
        cb = EasyCheckbutton(self, text, command)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        cb.grid(row = row, column = column,
                columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return cb

    def addRadiobuttonGroup(self, row, column,
                            rowspan = 1, columnspan = 1, orient = VERTICAL):
        """Creates and returns a radio button group."""
        return EasyRadiobuttonGroup(self, row, column, rowspan, columnspan, orient)

    # Added 12-18-2012
    def addPanel(self, row, column,
                 rowspan = 1, columnspan = 1, background = "white"):
        """Creates and returns a panel."""
        return EasyPanel(self, row, column, rowspan, columnspan, background)

    # Method to pop up a message box from this window.

    def messageBox(self, title = "", message = "", width = 25, height = 5):
        """Creates and pops up a message box, with the given title,
        message, and width and height in rows and columns of text."""
        dlg = MessageBox(self, title, message, width, height)
        return dlg.modified()

    # Method to pop up a prompter box from this window.

    def prompterBox(self, title = "", promptString = "", inputText = "", fieldWidth = 20):
        """Creates and pops up a prompter box, with the given title, prompt,
        input text, and field width in columns of text.
        Returns the text entered at the prompt."""
        dlg = PrompterBox(self, title, promptString, inputText, fieldWidth)
        return dlg.getText()

# Classes for easy widgets

class AbstractField(Tkinter.Entry):
    """Represents common features of float fields, integer fields,
    and text fields."""

    def __init__(self, parent, value, width, state):
        self.var = Tkinter.StringVar()
        self.setValue(value)
        Tkinter.Entry.__init__(self, parent,
                               textvariable = self.var,
                               width = width, state = state)

    def setValue(self, value):
        self.var.set(value)

    def getValue(self):
        return self.var.get()


class FloatField(AbstractField):
    """Represents a single line box for I/O of floats."""

    def __init__(self, parent, value, width, precision, state):
        self.setPrecision(precision)
        AbstractField.__init__(self, parent, value, width, state)

    def getNumber(self):
        """Returns the float contained in the field.
        Raises: ValueError if number format is bad."""
        return float(self.getValue())

    def setNumber(self, number):
        """Replaces the float contained in the field."""
        self.setValue(self._precision % number)

    def setPrecision(self, precision):
        """Resets the precision for the display of a float."""
        if precision and precision >= 0:
            self._precision = "%0." + str(precision) + "f"
        else:
            self._precision = "%f"


class IntegerField(AbstractField):
    """Represents a single line box for I/O of integers."""

    def __init__(self, parent, value, width, state):
        AbstractField.__init__(self, parent, value, width, state)

    def getNumber(self):
        """Returns the integer contained in the field.
        Raises: ValueError if number format is bad."""
        return int(self.getValue())

    def setNumber(self, number):
        """Replaces the integer contained in the field."""
        self.setValue(str(number))


class TextField(AbstractField):
    """Represents a single line box for I/O of strings."""

    def __init__(self, parent, value, width, state):
        AbstractField.__init__(self, parent, value, width, state)

    def getText(self):
        """Returns the string contained in the field."""
        return self.getValue()

    def setText(self, text):
        """Replaces the string contained in the field."""
        self.setValue(text)

class TextArea(Tkinter.Text):
    """Represents a box for I/O of multiline text."""

    def __init__(self, parent, text, width, height,
                 xscrollcommand, yscrollcommand, wrap):
        Tkinter.Text.__init__(self, parent,
                              width = width,
                              height = height,
                              wrap = wrap,
                              xscrollcommand = xscrollcommand,
                              yscrollcommand = yscrollcommand)
        self.setText(text)

    def getText(self):
        """Returns the string contained in the text area."""
        return self.get("1.0", END)

    def setText(self, text):
        """Replaces the string contained in the text area."""
        self.delete("1.0", END)
        self.insert("1.0", text)
        
    def appendText(self, text):
        """Inserts the text after the string contained in
        the text area."""
        self.insert(END, text)

class EasyListbox(Tkinter.Listbox):
    """Represents a list box."""

    def __init__(self, parent, width, height, yscrollcommand, listItemSelected):
        self._listItemSelected = listItemSelected
        Tkinter.Listbox.__init__(self, parent,
                                 width = width, height = height,
                                 yscrollcommand = yscrollcommand,
                                 selectmode = SINGLE)
        self.bind("<<ListboxSelect>>", self.triggerListItemSelected)

    def triggerListItemSelected(self, event):
        """Strategy method to respond to an item selection in the list box.
        Runs the client's listItemSelected method with the selected index if
        there is one."""
        if self.size() == 0: return
        widget = event.widget
        index = widget.curselection()[0]
        self._listItemSelected(index)

    def getSelectedIndex(self):
        """Returns the index of the selected item or -1 if no item
        is selected."""
        tup = self.curselection()
        if len(tup) == 0:
            return -1
        else:
            return int(tup[0])

    def getSelectedItem(self):
        """Returns the selected item or the empty string if no item
        is selected."""
        index = self.getSelectedIndex()
        if index == -1:
            return ""
        else:
            return self.get(index)

    def setSelectedIndex(self, index):
        """Selects the item at the index if it's in the range."""
        if index < 0 or index >= self.size(): return
        self.selection_set(index, index)

    def clear(self):
        """Deletes all items from the list box."""
        while self.size() > 0:
            self.delete(0)

    def getIndex(self, item):
        """Returns the index of item if it's in the list box,
        or -1 otherwise."""
        tup = self.get(0, self.size() - 1)
        if item in tup:
            return tup.index(item)
        else:
            return -1
        
class EasyRadiobuttonGroup(Tkinter.Frame):
    """Represents a group of radio buttons, only one of which
    is selected at any given time."""

    def __init__(self, parent, row, column, rowspan, columnspan, orient):
        Tkinter.Frame.__init__(self, parent)
        self.grid(row = row, column = column,
                  rowspan = rowspan, columnspan = columnspan,
                  sticky = N+S+E+W)
        self._commonVar = Tkinter.StringVar("")
        self._buttons = dict()
        self._orient = orient
        self._buttonRow = self._buttonColumn = 0

    def addRadiobutton(self, text, command = lambda : 0):
        """Creates a button with the given text and command, adds it to the group,
        and returns the button."""
        if text in self._buttons:
            raise ValueError("Button with this label already in the group")
        button = Tkinter.Radiobutton(self, text = text, value = text,
                                     command = command,
                                     variable = self._commonVar)
        self._buttons[text] = button
        button.grid(row = self._buttonRow, column = self._buttonColumn, sticky = N+W)
        if self._orient == VERTICAL:
            self.rowconfigure(self._buttonRow, weight = 1)
            self._buttonRow += 1
        else:
            self.columnconfigure(self._buttonColumn, weight = 1)
            self._buttonColumn += 1
        return button

    def getSelectedButton(self):
        if not self._commonVar.get() in self._buttons:
            raise ValueError("No button has been selected yet.")
        return self._buttons[self._commonVar.get()]

    def setSelectedButton(self, button):
        self._commonVar.set(button["value"])
    

class EasyCheckbutton(Tkinter.Checkbutton):
    """Represents a check button."""

    def __init__(self, parent, text, command):
        self._variable = Tkinter.IntVar()
        Tkinter.Checkbutton.__init__(self, parent, text = text,
                                     variable = self._variable,
                                     command = command)

    def isChecked(self):
        """Returns True if the button is checked or
        False otherwise."""
        return self._variable.get() != 0

class EasyMenuBar(Tkinter.Frame):
    """Represents a menu bar."""

    def __init__(self, parent, orient):
        self._orient = orient
        self._row = self._column = 0
        Tkinter.Frame.__init__(self, parent, relief = RAISED, borderwidth = 1)

    def addMenu(self, text, state = NORMAL):
        """Creates and inserts a menu into the
        menubar, and returns the menu."""
        menu = EasyMenubutton(self, text, state = state)
        menu.grid(row = self._row, column = self._column)
        if self._orient == "horizontal":
            self._column += 1
        else:
            self._row += 1
        return menu


class EasyMenubutton(Tkinter.Menubutton):
    """Represents a menu button."""

    def __init__(self, menuBar, text, state):
        Tkinter.Menubutton.__init__(self, menuBar,
                                    text = text, state = state)
        self.menu = Tkinter.Menu(self)
        self["menu"] = self.menu
        self._currentIndex = -1
        
    def addMenuItem(self, text, command, state = NORMAL):
        """Inserts a menu option in the given menu."""
        self.menu.add_command(label = text, command = command, state = state)
        self._currentIndex += 1
        return EasyMenuItem(self, self._currentIndex)


class EasyMenuItem(object):
    """Represents an option in a drop-down menu."""

    def __init__(self, menu, index):
        self._menu = menu
        self._index = index

    def setState(self, state):
        """Sets the state of the item to state."""
        self._menu.menu.entryconfigure(self._index, state = state)
        

class EasyCanvas(Tkinter.Canvas):
    """Represents a rectangular area for interactive drawing of shapes.
    Supports simple commands for drawing lines, rectangles, and ovals,
    as well as methods for responding to mouse events in the canvas."""

    def __init__(self, parent, width = None, height = None,
                 background = "white"):
        Tkinter.Canvas.__init__(self, parent,
                                width = width, height = height,
                                background = background)
        self.bind("<Double-Button-1>", self.mouseDoubleClicked)
        self.bind("<ButtonPress-1>", self.mousePressed)
        self.bind("<ButtonRelease-1>", self.mouseReleased)
        self.bind("<B1-Motion>", self.mouseDragged)

    # Mouse event handling methods.  One or more of these methods can 
    # be overridden in the subclass to implement the required actions.
    
    # The event argument can be used to extract the current mouse
    # cursor coordinates (event.x and event.y).

    def mouseDoubleClicked(self, event):
        """Triggered when the mouse is
        double-clicked in the area of this canvas."""
        return

    def mousePressed(self, event):
        """Triggered when the mouse is
        pressed in the area of this canvas."""
        return
        
    def mouseReleased(self, event):
        """Triggered when the mouse is
        released in the area of this canvas."""
        return

    def mouseDragged(self, event):
        """Triggered when the mouse is
        dragged in the area of this canvas."""
        return

    def getWidth(self):
        """Returns the width of the canvas."""
        return self["width"]

    def getHeight(self):
        """Returns the height of the canvas."""
        return self["height"]

    def drawLine(self, x0, y0, x1, y1,
                 fill = "black", width = 1):
        item = self.create_line(x0, y0, x1, y1)
        self.itemconfig(item, fill = fill, width = width)
        return item

    def drawRectangle(self, x0, y0, x1, y1,
                      outline = "black", fill = None):
        """Draws a rectangle with the given corner points,
        outline color, and fill color."""
        item = self.create_rectangle(x0, y0, x1, y1)
        self.itemconfig(item, outline = outline, fill = fill)
        return item

    def drawOval(self, x0, y0, x1, y1,
                 outline = "black", fill = None):
        """Draws an ovel within the given corner points,
        with the given outline color and fill color."""
        item = self.create_oval(x0, y0, x1, y1)
        self.itemconfig(item, outline = outline, fill = fill)
        return item

    def drawText(self, text, x, y, fill = "black"):
        """Draws the given text (a string) at the given coordinates
        with the given fill color.  The string is centered vertically
        and horizontally at the given coordinates."""
        item = self.create_text(x, y)
        self.itemconfig(item, text = text, fill = fill)
        return item

    def drawImage(self, image, x, y, anchor = CENTER):
        """Draws the given image (a PhotoImage) at the given coordinates.
        The image is centered at the given coordinates by default."""
        item = self.create_image(x, y, image = image,
                                 anchor = anchor)
        self.itemconfig(item, image = image, anchor = anchor)
        return item

    def deleteItem(self, item):
        """Removes and erases the shape with the given item
        number from the canvas."""
        self.delete(item)

# Support classes for dialogs.

class MessageBox(tkSimpleDialog.Dialog):
    """Represents a message dialog with a scrollable text area."""

    @classmethod
    def message(cls, title = "", message = "", width = 25, height = 5):
        MessageBox(Tkinter.Frame(), title, message, width, height)

    def __init__(self, parent, title, message, width, height):
        """Set up the window and widgets."""
        self._message = message
        self._width = width
        self._height = height
        self._modified = False
        tkSimpleDialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        self.resizable(0, 0)
        yScroll = Tkinter.Scrollbar(master, orient = VERTICAL)
        yScroll.grid(row = 0, column = 1, sticky = N+S)
        output = Tkinter.Text(master, width = self._width, height = self._height,
                      padx = 5, pady = 5, wrap = WORD,
                      yscrollcommand = yScroll.set)
        output.grid(row = 0, column = 0, sticky = N+W+S+E)
        output.insert("1.0", self._message)
        output["state"] = DISABLED
        yScroll["command"] = output.yview
        return output

    def buttonbox(self):
        '''add standard button box.
        override if you do not want the standard buttons'''
        box = Tkinter.Frame(self)
        w = Tkinter.Button(box, text="OK", width = 10,
                           command = self.ok, default = ACTIVE)
        w.pack()
        self.bind("<Return>", self.ok)
        box.pack()

    def apply(self):
        """Quits the dialog."""
        self._modified = True

    def modified(self):
        return self._modified

class PrompterBox(tkSimpleDialog.Dialog):
    """Represents an input dialog with a text field."""

    @classmethod
    def prompt(cls, title = "", promptString = "", inputText = "", fieldWidth = 20):
        """Creates and pops up an input dialog."""
        dlg = PrompterBox(Tkinter.Frame(), title, promptString, inputText, fieldWidth)
        return dlg.getText()

    def __init__(self, parent, title, promptString, inputText, fieldWidth):
        """Set up the window and widgets."""
        self._prompt = promptString
        self._text = inputText
        self._width = fieldWidth
        self._modified = False
        tkSimpleDialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        self.resizable(0, 0)
        label = Tkinter.Label(master, text = self._prompt)
        label.grid(row = 0, column = 0, padx = 5, sticky = N+W+S+E)
        self._field = TextField(master, self._text, self._width, NORMAL)
        self._field.grid(row = 1, column = 0, padx = 5, sticky = N+W+S+E)
        return self._field

    def buttonbox(self):
        '''add standard button box.
        override if you do not want the standard buttons'''
        box = Tkinter.Frame(self)
        w = Tkinter.Button(box, text="OK", width = 10,
                           command = self.ok, default = ACTIVE)
        w.pack()
        self.bind("<Return>", self.ok)
        box.pack()

    def apply(self):
        """Quits the dialog."""
        self._modified = True

    def modified(self):
        return self._modified

    def getText(self):
        """Returns the text currently in the text field."""
        return self._field.getText()

class EasyDialog(tkSimpleDialog.Dialog):
    """Represents a general-purpose dialog.  Subclasses should include
    body and apply methods."""

    def __init__(self, parent, title = ""):
        """Set up the window and widgets."""
        self._modified = False
        tkSimpleDialog.Dialog.__init__(self, parent, title)

    def modified(self):
        """Returns the modified status of the dialog."""
        return self._modified

    def setModified(self):
        self._modified = True

    def addLabel(self, master, text, row, column,
                 columnspan = 1, rowspan = 1,
                 sticky = N+W, font = None):
        """Creates and inserts a label at the row and column,
        and returns the label."""
        label = Tkinter.Label(master, text = text, font = font)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        label.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return label

    def addButton(self, master, text, row, column,
                  columnspan = 1, rowspan = 1,
                  command = lambda: None,
                  state = NORMAL):
        """Creates and inserts a button at the row and column,
        and returns the button."""
        button = Tkinter.Button(master, text = text,
                                command = command, state = state)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        button.grid(row = row, column = column,
                    columnspan = columnspan, rowspan = rowspan,
                    padx = 5, pady = 5)
        return button

    def addFloatField(self, master, value, row, column,
                      columnspan = 1, rowspan = 1,
                      width = 20, precision = None,
                      sticky = N+E, state = NORMAL):
        """Creates and inserts a float field at the row and column,
        and returns the float field."""
        field = FloatField(master, value, width, precision, state)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addIntegerField(self, master, value, row, column,
                        columnspan = 1, rowspan = 1,
                        width = 10, sticky = N+E, state = NORMAL):
        """Creates and inserts an integer field at the row and column,
        and returns the integer field."""
        field = IntegerField(master, value, width, state)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addTextField(self, master, text, row, column,
                     columnspan = 1, rowspan = 1,
                     width = 20, sticky = N+E, state = NORMAL):
        """Creates and inserts a text field at the row and column,
        and returns the text field."""
        field = TextField(master, text, width, state)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addCheckbutton(self, master, text, row, column,
                       rowspan = 1, columnspan = 1,
                       sticky = N+S+E+W, command = lambda : 0):
        """Creates and inserts check button at the row and column,
        and returns the check button."""
        cb = EasyCheckbutton(master, text, command)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        cb.grid(row = row, column = column,
                columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return cb

    def addRadiobuttonGroup(self, master, row, column,
                            rowspan = 1, columnspan = 1, orient = VERTICAL):
        """Creates and returns a radio button group."""
        return EasyRadiobuttonGroup(master, row, column, rowspan, columnspan, orient)

    def addScale(self, master, row, column, rowspan = 1, columnspan = 1,
                 command = lambda value: value, from_ = 0, to = 0,
                 label = "", length = 100, orient = HORIZONTAL,
                 resolution = 1, tickinterval = 0):
        """Creates and inserts a scale at the row and column,
        and returns the scale."""
        scale = Tkinter.Scale(master, command = command, from_ = from_, to = to,
                              label = label, length = length,
                              orient = orient, resolution = resolution,
                              tickinterval = tickinterval, relief = "sunken",
                              borderwidth = 4)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        scale.grid(row = row, column = column, columnspan = columnspan,
                   rowspan = rowspan, sticky = N+S+E+W)
        return scale

    def addTextArea(self, master, text, row, column, rowspan = 1, columnspan = 1,
                    width = 80, height = 5, wrap = NONE):
        """Creates and inserts a multiline text area at the row and column,
        and returns the text area.  Vertical and horizontal scrollbars are
        provided."""
        frame = Tkinter.Frame(master)
        frame.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   sticky = N+S+E+W)
        master.columnconfigure(column, weight = 1)
        master.rowconfigure(row, weight = 1)
        xScroll = Tkinter.Scrollbar(frame, orient = HORIZONTAL)
        xScroll.grid(row = 1, column = 0, sticky = E+W)
        yScroll = Tkinter.Scrollbar(frame, orient = VERTICAL)
        yScroll.grid(row = 0, column = 1, sticky = N+S)
        area = TextArea(frame, text, width, height,
                        xScroll.set, yScroll.set, wrap)
        area.grid(row = 0, column = 0,
                  padx = 5, pady = 5, sticky = N+S+E+W)
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        xScroll["command"] = area.xview
        yScroll["command"] = area.yview
        return area

    def addListbox(self, master, row, column, rowspan = 1, columnspan = 1,
                   width = 10, height = 5, listItemSelected = lambda index: index):
        """Creates and inserts a scrolling list box at the row and column, with a
        width and height in lines and columns of text, and a default item selection
        method, and returns the list box."""
        frame = Tkinter.Frame(master)
        frame.grid(row = row, column = column, columnspan = columnspan, rowspan = rowspan,
                   sticky = N+S+E+W)
        master.columnconfigure(column, weight = 1)
        master.rowconfigure(row, weight = 1)
        yScroll = Tkinter.Scrollbar(frame, orient = VERTICAL)
        yScroll.grid(row = 0, column = 1, sticky = N+S)
        listBox = EasyListbox(frame, width, height, yScroll.set, listItemSelected)
        listBox.grid(row = 0, column = 0, sticky = N+S+E+W)
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        yScroll["command"] = listBox.yview
        return listBox

    def addCanvas(self, master, canvas = None, row = 0, column = 0,
                  rowspan = 1, columnspan = 1, width = 200, height = 100,
                  background = "white"):
        """Creates and inserts a canvas at the row and column,
        and returns the canvas."""
        if not canvas:
            canvas = EasyCanvas(master, width = width, height = height,
                                background = background)
        canvas.grid(row = row, column = column,
                    rowspan = rowspan, columnspan = columnspan,
                    sticky = W+E+N+S)
        master.columnconfigure(column, weight = 10)
        master.rowconfigure(row, weight = 10)
        return canvas

    def addMenuBar(self, master, row, column, rowspan = 1, columnspan = 1,
                   orient = "horizontal"):
        """Creates and inserts a menu bar at the row and column,
        and returns the menu bar."""
        if not orient in ("horizontal", "vertical"):
            raise ValueError("orient must be horizontal or vertical")
        menuBar = EasyMenuBar(master, orient)
        menuBar.grid(row = row, column = column,
                     rowspan = rowspan, columnspan = columnspan,
                     sticky = N+W)
        return menuBar

    def messageBox(self, title = "", message = "", width = 25, height = 5):
        """Creates and pops up a message box, with the given title,
        message, and width and height in rows and columns of text."""
        dlg = MessageBox(self, title, message, width, height)
        return dlg.modified()

        # Added 12-18-2012
    def addPanel(self, master, row, column,
                 rowspan = 1, columnspan = 1, background = "white"):
        """Creates and returns a panel."""
        return EasyPanel(master, row, column, rowspan, columnspan, background)


 
# Added 12-18-2012
class EasyPanel(Tkinter.Frame):
    """Organizes a group of widgets in a panel (nested frame)."""

    def __init__(self, parent, row, column, rowspan, columnspan, background):
        Tkinter.Frame.__init__(self, parent)
        parent.rowconfigure(row, weight = 1)
        parent.columnconfigure(column, weight = 1)
        self.grid(row = row, column = column,
                  rowspan = rowspan, columnspan = columnspan,
                  sticky = N+S+E+W)
        self.setBackground(background)

    def setBackground(self, color):
        """Resets the panel's background color to color."""
        self["background"] = color

    def addButton(self, text, row, column,
                  columnspan = 1, rowspan = 1,
                  command = lambda: None,
                  state = NORMAL):
        """Creates and inserts a button at the row and column,
        and returns the button."""
        button = Tkinter.Button(self, text = text,
                                command = command, state = state)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        button.grid(row = row, column = column,
                    columnspan = columnspan, rowspan = rowspan,
                    padx = 5, pady = 5)
        return button

    def addLabel(self, text, row, column,
                 columnspan = 1, rowspan = 1,
                 sticky = N+W, font = None,
                 background = "white", foreground = "black"):
        """Creates and inserts a label at the row and column,
        and returns the label."""
        label = Tkinter.Label(self, text = text, font = font,
                              background = background,
                              foreground = foreground)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        label.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return label

    def addFloatField(self, value, row, column,
                      columnspan = 1, rowspan = 1,
                      width = 20, precision = None,
                      sticky = N+E, state = NORMAL):
        """Creates and inserts a float field at the row and column,
        and returns the float field."""
        field = FloatField(self, value, width, precision, state)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addIntegerField(self, value, row, column,
                        columnspan = 1, rowspan = 1,
                        width = 10, sticky = N+E, state = NORMAL):
        """Creates and inserts an integer field at the row and column,
        and returns the integer field."""
        field = IntegerField(self, value, width, state)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addTextField(self, text, row, column,
                     columnspan = 1, rowspan = 1,
                     width = 20, sticky = N+E, state = NORMAL):
        """Creates and inserts a text field at the row and column,
        and returns the text field."""
        field = TextField(self, text, width, state)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return field

    def addTextArea(self, text, row, column, rowspan = 1, columnspan = 1,
                    width = 80, height = 5, wrap = NONE):
        """Creates and inserts a multiline text area at the row and column,
        and returns the text area.  Vertical and horizontal scrollbars are
        provided."""
        frame = Tkinter.Frame(self)
        frame.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   sticky = N+S+E+W)
        self.columnconfigure(column, weight = 1)
        self.rowconfigure(row, weight = 1)
        xScroll = Tkinter.Scrollbar(frame, orient = HORIZONTAL)
        xScroll.grid(row = 1, column = 0, sticky = E+W)
        yScroll = Tkinter.Scrollbar(frame, orient = VERTICAL)
        yScroll.grid(row = 0, column = 1, sticky = N+S)
        area = TextArea(frame, text, width, height,
                        xScroll.set, yScroll.set, wrap)
        area.grid(row = 0, column = 0,
                  padx = 5, pady = 5, sticky = N+S+E+W)
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        xScroll["command"] = area.xview
        yScroll["command"] = area.yview
        return area

    def addListbox(self, row, column, rowspan = 1, columnspan = 1,
                   width = 10, height = 5, listItemSelected = lambda index: index):
        """Creates and inserts a scrolling list box at the row and column, with a
        width and height in lines and columns of text, and a default item selection
        method, and returns the list box."""
        frame = Tkinter.Frame(self)
        frame.grid(row = row, column = column, columnspan = columnspan, rowspan = rowspan,
                   sticky = N+S+E+W)
        self.columnconfigure(column, weight = 1)
        self.rowconfigure(row, weight = 1)
        yScroll = Tkinter.Scrollbar(frame, orient = VERTICAL)
        yScroll.grid(row = 0, column = 1, sticky = N+S)
        listBox = EasyListbox(frame, width, height, yScroll.set, listItemSelected)
        listBox.grid(row = 0, column = 0, sticky = N+S+E+W)
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        yScroll["command"] = listBox.yview
        return listBox

    def addCanvas(self, canvas = None, row = 0, column = 0,
                  rowspan = 1, columnspan = 1, width = 200, height = 100,
                  background = "white"):
        """Creates and inserts a canvas at the row and column,
        and returns the canvas."""
        if not canvas:
            canvas = EasyCanvas(self, width = width, height = height,
                                background = background)
        canvas.grid(row = row, column = column,
                    rowspan = rowspan, columnspan = columnspan,
                    sticky = W+E+N+S)
        self.columnconfigure(column, weight = 10)
        self.rowconfigure(row, weight = 10)
        return canvas

    def addScale(self, row, column, rowspan = 1, columnspan = 1,
                 command = lambda value: value, from_ = 0, to = 0,
                 label = "", length = 100, orient = HORIZONTAL,
                 resolution = 1, tickinterval = 0):
        """Creates and inserts a scale at the row and column,
        and returns the scale."""
        scale = Tkinter.Scale(self, command = command, from_ = from_, to = to,
                              label = label, length = length,
                              orient = orient, resolution = resolution,
                              tickinterval = tickinterval, relief = "sunken",
                              borderwidth = 4)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        scale.grid(row = row, column = column, columnspan = columnspan,
                   rowspan = rowspan, sticky = N+S+E+W)
        return scale

    def addMenuBar(self, row, column, rowspan = 1, columnspan = 1,
                   orient = "horizontal"):
        """Creates and inserts a menu bar at the row and column,
        and returns the menu bar."""
        if not orient in ("horizontal", "vertical"):
            raise ValueError("orient must be horizontal or vertical")
        menuBar = EasyMenuBar(self, orient)
        menuBar.grid(row = row, column = column,
                     rowspan = rowspan, columnspan = columnspan,
                     sticky = N+W)
        return menuBar

    def addCheckbutton(self, text, row, column,
                       rowspan = 1, columnspan = 1,
                       sticky = N+S+E+W, command = lambda : 0):
        """Creates and inserts check button at the row and column,
        and returns the check button."""
        cb = EasyCheckbutton(self, text, command)
        self.rowconfigure(row, weight = 1)
        self.columnconfigure(column, weight = 1)
        cb.grid(row = row, column = column,
                columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        return cb

    def addRadiobuttonGroup(self, row, column,
                            rowspan = 1, columnspan = 1, orient = VERTICAL):
        """Creates and returns a radio button group."""
        return EasyRadiobuttonGroup(self, row, column, rowspan, columnspan, orient)
    
    def addPanel(self, row, column,
                 rowspan = 1, columnspan = 1, background = "white"):
        """Creates and returns a panel."""
        return EasyPanel(self, row, column, rowspan, columnspan, background)





    






    
        
