// Software Serial Sample
// Copyright (c) 2012 Dimension Engineering LLC
// See license.txt for license details.

#include <SoftwareSerial.h>
#include <SabertoothSimplified.h>

SoftwareSerial SWSerial(2, 3); // RX on pin 2 (unused), TX on pin 3 (to S1).
SabertoothSimplified ST(SWSerial); // Use SWSerial as the serial port.

void setup()
{
  SWSerial.begin(9600);
}

void loop()
{
  int power;
  
  // Ramp from -127 to 127 (full reverse to full forward), waiting 20 ms (1/50th of a second) per value.
  for (power = -127; power <= 127; power ++)
  {
    ST.motor(1, power);
    delay(20);
  }
  
  // Now go back the way we came.
  for (power = 127; power >= -127; power --)
  {
    ST.motor(1, power);
    delay(20);
  }
}

