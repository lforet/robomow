#include <SoftwareSerial.h>

#define TX_PIN 13
#define RX_PIN 12

SoftwareSerial mySerial = SoftwareSerial( RX_PIN, TX_PIN );


void setup( )
{
  pinMode( RX_PIN, INPUT);
  pinMode( TX_PIN, INPUT);
  Serial.begin(9600);
  Serial.println("Goodnight moon!");

  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  //mySerial.println("Hello, world?");
}

void loop() // run over and over
{
  if (mySerial.available())
    Serial.write(mySerial.read());
  //if (Serial.available())
  //  mySerial.write(Serial.read());
}
