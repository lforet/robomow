"""
File: thermometer.py
Author: Kenneth A. Lambert
"""

class Thermometer(object):
    """Models temperature conversion between degrees Fahrenheit
    and degrees Celsius."""

    def __init__(self):
        """Sets up the model."""
        # Celsius is the standard
        self._degreesCelsius = 0.0

    def getCelsius(self):
        """Returns the Celsius temperature."""
        return self._degreesCelsius

    def setCelsius(self, degrees):
        """Sets the thermometer to degrees in Celsius."""
        self._degreesCelsius = degrees

    def getFahrenheit(self):
        """Returns the Fahrenheit temperature."""
        return self._degreesCelsius * 9 / 5 + 32

    def setFahrenheit(self, degrees):
        """Sets the thermometer to degrees in Fahrenheit."""
        self._degreesCelsius = (degrees - 32) * 5 / 9
