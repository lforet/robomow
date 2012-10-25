//battery meter code for uno arduino
int interval = 1; //sample time interval (1000 (ms) = 1 second)
float bat1_high = 12.95;
float bat1_low = 11.10;
float bat2_high = 12.95;
float bat2_low = 11.10;
float bat3_high = 12.95;
float bat3_low = 11.10;
int samples = 10; //number of samples taken
int analog_read = 0; 
int bat1_pin_to_read = A0; 
int bat2_pin_to_read = A1; 
int bat3_pin_to_read = A2; 
long bat1_reading_sum_total = 0;
long bat2_reading_sum_total = 0;
long bat3_reading_sum_total = 0;
int bat1_reading_sum_avg = 0;
int bat2_reading_sum_avg = 0;
int bat3_reading_sum_avg = 0;
float bat1_volt = 0;
float bat2_volt = 0;
float bat3_volt = 0;
int bat1_lvl  = 0;
int bat2_lvl  = 0;
int bat3_lvl  = 0;
float calibration = 0.023941748; //voltage per reading
void setup()
{
  Serial.begin(9600);
   //pinMode(bat1_pin_to_read, INPUT);
   //digitalWrite(bat1_pin_to_read, HIGH);
  //pinMode(bat2_pin_to_read, INPUT);
  //digitalWrite(bat2_pin_to_read, HIGH);
  //pinMode(bat3_pin_to_read, INPUT);
  //digitalWrite(bat3_pin_to_read, HIGH);  
}
void loop()
{
	for(int i = 0; i < samples ; i++)
  	{	 
		bat1_reading_sum_total += analogRead(bat1_pin_to_read);
                delay(50);
		bat2_reading_sum_total += analogRead(bat2_pin_to_read);
                delay(50);
		bat3_reading_sum_total += analogRead(bat3_pin_to_read);
		delay(50);
        }
        //average out the readings
	bat1_reading_sum_avg = bat1_reading_sum_total / samples;
        bat2_reading_sum_avg = bat2_reading_sum_total / samples;
        bat3_reading_sum_avg = bat3_reading_sum_total / samples;
        //Serial.println (bat1_reading_sum_avg * (5.0 / 1023.0));
        Serial.println (bat1_reading_sum_avg );
        Serial.println (bat2_reading_sum_avg );
        Serial.println (bat3_reading_sum_avg ); 
        
        //calculate voltages
        bat1_volt = (bat1_reading_sum_avg * calibration );
        bat2_volt = (bat2_reading_sum_avg * calibration );
        bat3_volt = (bat3_reading_sum_avg * calibration );

        
        //calculate battery levels
        bat1_lvl = int(100 * ((bat1_volt - bat1_low) / (bat1_high - bat1_low)));
        bat2_lvl = int(100 * ((bat2_volt - bat2_low) / (bat2_high - bat2_low)));
        bat3_lvl = int(100 * ((bat3_volt - bat3_low) / (bat3_high - bat3_low)));
      
        //send data out  
        Serial.print ("bat bank,");
        Serial.print ("1,");
	Serial.print("voltage,");
	Serial.print (bat1_volt);
        Serial.print (","); 
        Serial.print ("battery lvl,");
        Serial.println (bat1_lvl);

        Serial.print ("bat bank,");
        Serial.print ("2,");
	Serial.print("voltage,");
	Serial.print (bat2_volt);
        Serial.print (","); 
        Serial.print ("battery lvl,");
        Serial.println (bat2_lvl);

        Serial.print ("bat bank,");
        Serial.print ("3,");
	Serial.print("voltage,");
	Serial.print (bat3_volt);
        Serial.print (","); 
        Serial.print ("battery lvl,");
        Serial.println (bat3_lvl);
        
        //reset for next loop	
        bat1_reading_sum_avg = 0;
        bat2_reading_sum_avg = 0;
        bat3_reading_sum_avg = 0;
        bat1_reading_sum_total = 0;
        bat2_reading_sum_total = 0;
        bat3_reading_sum_total = 0;
        delay(interval);
}


