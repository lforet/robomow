"""
File: thermometerview2.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame
from thermometer import Thermometer

class ThermometerView(EasyFrame):
    """A termperature conversion program.  Uses sliding scales."""

    def __init__(self, model):
        """Sets up the view.  The model comes in as an argument."""
        EasyFrame.__init__(self, title = "Temperature Converter")
        self.model = model

        # Sliding scale for Celsius
        self.celsiusScale = self.addScale(label = "Celsius",
                                          row = 0, column = 0,
                                          from_ = -273.15, to = 100.0,
                                          resolution = 0.01,
                                          length = 250,
                                          tickinterval = 0,
                                          command = self.computeFahr)
        self.celsiusScale.set(model.getCelsius())

        # Sliding scale for Celsius
        self.fahrScale = self.addScale(label = "Fahernheit",
                                       row = 1, column = 0,
                                       from_ = -459.67, to = 212.0,
                                       resolution = 0.01,
                                       length = 250,
                                       tickinterval = 0,
                                       command = self.computeCelsius)
        self.fahrScale.set(model.getFahrenheit())

    # The controller methods
    def computeFahr(self, degreesCelsius):
        """Inputs the Celsius degrees
        and outputs the Fahrenheit degrees."""
        degrees = float(degreesCelsius)
        self.model.setCelsius(degrees)
        self.fahrScale.set(self.model.getFahrenheit())

    def computeCelsius(self, degreesFahrenheit):
        """Inputs the Fahrenheit degrees
        and outputs the Celsius degrees."""
        degrees = float(degreesFahrenheit)
        self.model.setFahrenheit(degrees)
        self.celsiusScale.set(self.model.getCelsius())

# Instantiate the model, pass it to the view, and pop up the window.
if __name__ == "__main__":
    model = Thermometer()
    view = ThermometerView(model)
    view.mainloop()
