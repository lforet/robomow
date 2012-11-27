
#include <SoftwareSerial.h>

// Labels for use with the Sabertooth 2x5 motor controller

// Digital pin 13 is the serial transmit pin to the
// Sabertooth 2x5
#define SABER_TX_PIN 13
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

int rc1_fwrv = 8; //channel 2 on rc
int rc2_rtlf = 9; //channel 1 on rc
int rc3_kill = 10; //channel 5 on rc

int rc1_val;
int rc2_val;
int rc3_val;

SoftwareSerial SaberSerial = SoftwareSerial( SABER_RX_PIN, SABER_TX_PIN );

//global variables
boolean isConnectedPC = false;
boolean isConnectedRC = false;
int motor1_spd;
int motor2_spd;

void initSabertooth()
{
  // Init software UART to communicate
  // with the Sabertooth 2x5
  pinMode( SABER_TX_PIN, OUTPUT );

  SaberSerial.begin( SABER_BAUDRATE );
  Serial.begin( SABER_BAUDRATE );
  
  //establish contact with main pc
  //establishContact();
  
  // 2 second time delay for the Sabertooth to init
  delay( 2000 );
  // Send full stop command
  //setEngineSpeed( SABER_ALL_STOP );
  pinMode(rc1_fwrv, INPUT);
  pinMode(rc2_rtlf, INPUT);
  pinMode(rc3_kill, INPUT);
}

void establishContact() {
  Serial.println("establishContact: ");
  Serial.println(Serial.available());
  byte incomingByte = 0;
  while (Serial.available() <= 0) {
    Serial.println('mmd'); //mobot motor driver
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

String pc_commands(){
  byte incomingByte;
  String cmd = "";
  String confirm_cmd = "";
  char incoming_character;
  
  while (Serial.available() <= 0) {
    Serial.println ("m1:");
    delay(100);
  }
  while(Serial.available()) {
      incoming_character = Serial.read();
      cmd.concat(incoming_character);
  }
  if (cmd != "") {
    //Serial.println(content);
    //Serial.println(content.substring(0,2));
    if (cmd.substring(0,2) == "FW"){
      //Serial.println(cmd);
      int speed_cmd = cmd.substring(2,5).toInt();
      return cmd;
    }
    if (cmd.substring(0,2) == "RV"){
      //Serial.println(cmd);
      int speed_cmd = cmd.substring(2,5).toInt();
      return cmd;
    }
    if (cmd.substring(0,2) == "LT"){
      //Serial.println(cmd);
      int speed_cmd = cmd.substring(2,5).toInt();
      return cmd;
    }
    if (cmd.substring(0,2) == "RT"){
      //Serial.println(cmd);
      int speed_cmd = cmd.substring(2,5).toInt();
      return cmd;
    }
    if (cmd.substring(0,2) == "ST"){
      //Serial.println(cmd);
      int speed_cmd = cmd.substring(2,5).toInt();
      return cmd;
    }
    if (cmd.substring(0,2) == "SP"){
      //Serial.println(cmd);
      return cmd;
    }    
  }
  delay(200);
}

void loop(){
  String cmd = "";
  //forward(50);
  //delay (2000);
  //Serial.println("loop");
  //SaberSerial.write("loop2");
  //establishContact();
  //cmd = pc_commands();
  rc_commands();
  //serial_print_stuff();
  //send_cmd_to_robot(cmd);
  //Serial.println(");
  // if (SaberSerial.available()){
  //  Serial.write(SaberSerial.read());
  //}
  //if (Serial.available()){
  //  SaberSerial.write(Serial.read());
  //}
  //SaberSerial.println("hello")
  delay (10);
}

void rc_commands(){
  String cmd = "";
  rc3_val = pulseIn(rc3_kill, HIGH, 20000);//channel 5 on rc
  if (rc3_val > 1400){
    
    rc1_val = pulseIn(rc1_fwrv, HIGH, 20000);
    //Serial.print(rc1_val);
    if (rc1_val > 1000 && rc1_val < 2000){
      rc1_val = map(rc1_val, 1030, 1860, 1, 127);
      if (rc1_val < 1){
        rc1_val = 1;
      }
      if (rc1_val > 127){
        rc1_val = 127;
      }
    }
    else{
      rc1_val = 64;
    }
    // ******************************************************
    rc2_val = pulseIn(rc2_rtlf, HIGH, 20000);//channel 1 on rc
    if (rc2_val > 1000 && rc2_val < 2000){
      rc2_val = map(rc2_val, 1070, 1890, 128, 255); 
      if (rc2_val < 128){
        rc2_val = 128;
      }
      if (rc2_val > 255){
       rc2_val = 255;
      }
      //Serial.println(rc2_val);
    }
    else{
      rc2_val = 192;
    }
    
    rc_motor_drive();
  }
   // ******************************************************
  if (rc3_val < 1400){
    Serial.println("kill switch activated");
    stop_motors();
  }
}

void rc_motor_drive(){
  //Serial.write(rc1_val);
  //Serial.write(rc2_val);
  SaberSerial.write(rc1_val);
  SaberSerial.write(rc2_val);
  
}


void send_cmd_to_robot(String cmd){
  if (cmd != "") {
    if (cmd.substring(0,2) == "FW"){
      int speed_cmd = cmd.substring(2,5).toInt();
      forward(speed_cmd);
    }
    if (cmd.substring(0,2) == "RV"){
      int speed_cmd = cmd.substring(2,5).toInt();
      reverse(speed_cmd);
    }
    if (cmd.substring(0,2) == "LT"){
      int speed_cmd = cmd.substring(2,5).toInt();
      left(speed_cmd);
    }
    if (cmd.substring(0,2) == "RT"){
      int speed_cmd = cmd.substring(2,5).toInt();
      right(speed_cmd);
    }
    if (cmd.substring(0,2) == "ST"){
      int speed_cmd = cmd.substring(2,5).toInt();
      stop_motors();
    }
    if (cmd.substring(0,2) == "SP"){
      stats();
    }    
  }
  Serial.print("cmd send to robot");
  Serial.println(cmd);
}


void m1_drive(int speed_val){
  int val = map(speed_val, -100, 100, 1, 127);
  if (val > 127){
    val = 127;
  }
  else if (val < 1){
    val = 1;
  }
  //Serial.print("m1:");
  //Serial.println(val);
  //Serial.write(val);
  motor1_spd = speed_val;
}

void m2_drive(int speed_val){
  int val = map(speed_val, -100, 100, 128, 255);
  if (val < 128){
    val = 128;
  }
  else if (val > 255){
    val = 255;
  }
  if (val == 191){
    val = 192;
  }
  //Serial.write(val);
  //Serial.print("m2:");
  //Serial.println(val);
  motor2_spd = speed_val;
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

void stop_motors(){
  int speed_val = 0;
  rc1_val = 64;
  rc2_val = 192;
  m1_drive(speed_val);
  m2_drive(speed_val);
}

void stats(){
  Serial.print(motor1_spd);
  Serial.print(",");
  Serial.println(motor2_spd);
}


void serial_print_stuff(){
  Serial.print("rc1: ");
  Serial.print(rc1_val);
  Serial.print("  rc2: ");
  Serial.print(rc2_val);
  Serial.print("  rc3: ");
  Serial.println(rc3_val);
}
