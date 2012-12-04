// This program written for Arduino UNO rv3. 
// for Maxbotix HRLV-Maxsonar MB1023
//Analog pin 0-4 for reading in the analog voltage from the MaxSonar device.

const int anPin0 = 0;
const int anPin1 = 1;
const int anPin2 = 2;
const int anPin3 = 3;
const int anPin4 = 4;

//variables needed to store values
long anVolt0;
long anVolt1;
long anVolt2;
long anVolt3;
long anVolt4;
long cm0;
long cm1;
long cm2;
long cm3;
long cm4;
int sum0=0;//Create sum variable so it can be averaged
int sum1=0;//Create sum variable so it can be averaged
int sum2=0;//Create sum variable so it can be averaged
int sum3=0;//Create sum variable so it can be averaged
int sum4=0;//Create sum variable so it can be averaged

int sum_mm = 0;
int avgrange=10;//Quantity of values to average (sample size)
int calibration_offset = 0;
float cm_to_inches = 0.393701;
void setup() {

  //This opens up a serial connection to shoot the results back to the PC console
  Serial.begin(9600);

}

void loop() {

  pinMode(anPin0, INPUT);
  pinMode(anPin1, INPUT);
  pinMode(anPin2, INPUT);
  pinMode(anPin3, INPUT);
  pinMode(anPin4, INPUT);
  //MaxSonar Analog reads are known to be very sensitive. See the Arduino forum for more information.
  //A simple fix is to average out a sample of n readings to get a more consistant reading.\\ 

  for(int i = 0; i < avgrange ; i++)
  {
    //Used to read in the analog voltage output that is being sent by the MaxSonar device.
    //Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/cm
    //Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual cm
    anVolt0 = analogRead(anPin0)/2;
    anVolt1 = analogRead(anPin1)/2;
    anVolt2 = analogRead(anPin2)/2;
    anVolt3 = analogRead(anPin3)/2;
    anVolt4 = analogRead(anPin4)/2;
    sum0 += anVolt0;
    sum1 += anVolt1;
    sum2 += anVolt2;
    sum3 += anVolt3;
    sum4 += anVolt4;
    delay(10);
  }  

  cm0 = sum0/avgrange;
  cm1 = sum1/avgrange;
  cm2 = sum2/avgrange;
  cm3 = sum3/avgrange;
  cm4 = sum4/avgrange;
  
  //inches = cm * cm_to_inches;
  //inches = cm * cm_to_inches;
  //inches = cm * cm_to_inches;
  //inches = cm * cm_to_inches;
  //inches = cm * cm_to_inches;
  
  //Serial.print(inches);
  //Serial.print("in, ");
  
  Serial.print("s1:");
  Serial.print(cm0);
  Serial.print("s2:");
  Serial.print(cm1);
  Serial.print("s3:");
  Serial.print(cm2);
  Serial.print("s4:");
  Serial.print(cm3);
  Serial.print("s5:");
  Serial.println(cm4);
  //Serial.println();

  //reset sample total
  sum0 = 0;
  sum1 = 0;
  sum2 = 0;
  sum3 = 0;
  sum4 = 0;

  delay(30);

} 
