"""
File: textfielddemo.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame

class TextFieldDemo(EasyFrame):
    """Converts an  input string to uppercase and displays the result."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self)

        # Label and field for the input
        self.addLabel(text = "Input",
                      row = 0, column = 0)
        self.inputField = self.addTextField(text = "",
                                            row = 0,
                                            column = 1)

        # Label and field for the output
        self.addLabel(text = "Output",
                      row = 1, column = 0)
        self.outputField = self.addTextField(text = "",
                                             row = 1,
                                             column = 1,
                                             state = "readonly")

        # The command button
        self.button = self.addButton(text = "Convert",
                                     row = 2, column = 0,
                                     columnspan = 2,
                                     command = self.convert)

    # The event handling method for the button
    def convert(self):
        """Inputs the string, converts it to uppercase,
        and outputs the result."""
        text = self.inputField.getText()
        result = text.upper()
        self.outputField.setText(result)

#Instantiate and pop up the window."""
if __name__ == "__main__":
    TextFieldDemo().mainloop()
