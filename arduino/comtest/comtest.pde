int incomingByte = 0;	// for incoming serial data
int var = 0;
int sum = 0;

void setup() {
	Serial.begin(9600);	// opens serial port, sets data rate to 9600 bps
        establishContact();  // send a byte to establish contact until receiver responds 
}

void loop() {

	// send data only when you receive data:
	if (Serial.available() > 0) {
		// read the incoming byte:
		incomingByte = Serial.read();

		// say what you got:
		Serial.print("I received: ");
		Serial.println(incomingByte, DEC);
                while(var < 100){
                // do something repetitive 200 times
                      var++;
                      Serial.print("Hey Andrea Count: ");
                      Serial.println(var, DEC);
                      delay(10); 
                      //sum = sum + var^2;
                      //Serial.print("Sum: ");
                      //Serial.println(sum, DEC);      
                }
                var = 0;
	}
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A', BYTE);   // send a capital A
    delay(1000);
  }
}


