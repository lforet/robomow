
#include <SoftwareSerial.h>

// Labels for use with the Sabertooth 2x5 motor controller

// Digital pin 13 is the serial transmit pin to the
// Sabertooth 2x5
#define SABER_TX_PIN 13

// NOT USED (but still init'd)
// Digital pin 12 is the serial receive pin from the
// Sabertooth 2x5
#define SABER_RX_PIN 12

// Set to 9600 through Sabertooth dip switches
#define SABER_BAUDRATE 9600

// Simplified serial Limits for each motor
#define SABER_MOTOR1_FULL_FORWARD 127
#define SABER_MOTOR1_FULL_REVERSE 1
#define SABER_MOTOR1_FULL_STOP 64


#define SABER_MOTOR2_FULL_FORWARD 255
#define SABER_MOTOR2_FULL_REVERSE 128
#define SABER_MOTOR2_FULL_STOP 192


// Motor level to send when issuing the full stop command
#define SABER_ALL_STOP 0


SoftwareSerial SaberSerial = SoftwareSerial( SABER_RX_PIN, SABER_TX_PIN );

void initSabertooth()
{
  // Init software UART to communicate
  // with the Sabertooth 2x5
  //pinMode( SABER_TX_PIN, OUTPUT );

  //SaberSerial.begin( SABER_BAUDRATE );
  Serial.begin( SABER_BAUDRATE );
  
  
  //establish contact with main pc
  establishContact();
  
  // 2 second time delay for the Sabertooth to init
  delay( 2000 );
  // Send full stop command
  //setEngineSpeed( SABER_ALL_STOP );
}

void establishContact() {
  byte incomingByte = 0;
  while (Serial.available() <= 0) {
    Serial.println('mobot motor driver');
    delay(100);
  }
  // read the incoming byte:
  incomingByte = Serial.read();
  // echo data received:
  Serial.print("I received: ");
  Serial.println(incomingByte);
}



void setup( )
{
  initSabertooth( );
}

void loop(){
  forward(50);
  delay (2000);
  reverse(50);
  delay (2000);
  stop_motors();
  delay (2000);
  right(50);
  delay (2000);
  left(50);
  delay (2000);
  Serial.println();
}

void m1_drive(int speed_val){
  int val = map(speed_val, -100, 100, 1, 127);
  if (val > 127){
    val = 127;
  }
  else if (val < 1){
    val = 1;
  }
  Serial.println(val);
  //Serial.write(val);
}

void m2_drive(int speed_val){
  int val = map(speed_val, -100, 100, 128, 255);
  if (val < 128){
    val = 128;
  }
  else if (val > 255){
    val = 255;
  }
  //Serial.write(val);
  Serial.println(val);
}

void stop_motors(){
  int val = 0;
  Serial.println(val);
  //Serial.write(val);
}

void forward(int speed_val){
  m1_drive(speed_val);
  m2_drive(speed_val);
}

void reverse(int speed_val){
  speed_val = speed_val * -1;
  m1_drive(speed_val);
  m2_drive(speed_val);
}

void right(int speed_val){
  m1_drive(speed_val);
  m2_drive(speed_val*-1);
}

void left(int speed_val){
  m1_drive(speed_val*-1);
  m2_drive(speed_val);
}
