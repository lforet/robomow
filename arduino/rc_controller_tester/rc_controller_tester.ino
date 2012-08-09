int rc1 = 7;
int rc2 = 8;
int rc3 = 4;

int rc1_val;
int rc2_val;
int rc3_val;

boolean kill_motors_flag;

void setup(){
  Serial.begin(9600);
  pinMode(rc1, INPUT);
  pinMode(rc2, INPUT);
  pinMode(rc3, INPUT);
}

void loop(){
  read_pulses();
  kill_switch();
  write_motors();
  serial_print_stuff();
}

void read_pulses(){
  // RC 1 value used to control motor 1 output
  rc1_val = pulseIn(rc1, HIGH, 20000);
  if (rc1_val > 1000 && rc1_val < 2000){
    rc1_val = map(rc1_val, 1000, 2000, 1, 127);
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
  // RC 2 value used to control motor 2 output
  rc2_val = pulseIn(rc2, HIGH, 20000);
  if (rc1_val > 1000 && rc1_val < 2000){
    rc2_val = map(rc2_val, 1000, 2000, 128, 255);
    if (rc2_val < 128){
      rc2_val = 128;
    }
    if (rc2_val > 255){
      rc2_val = 255;
    }
  }
  else{
    rc2_val = 192;
  }
  // RC 3 value from a toggle switch used to control motor output
  rc3_val = pulseIn(rc3, HIGH, 20000);
  if (rc3_val > 1000 && rc3_val < 2000){
    if (rc3_val < 1000){
      rc3_val = 1000;
    }
    if (rc3_val > 2000){
      rc3_val = 2000;
    }
  }
  else{
    rc3_val = 1000;
  }
}

void kill_switch(){
  if (rc3_val > 1700){
    kill_motors_flag = false;
  }
  else{
    kill_motors_flag = true;
  }
}

void write_motors(){
  if (kill_motors_flag == false){
    Serial.print(rc1_val);
    Serial.print(rc2_val);
  }
  else{
    Serial.print(0);
  }
}

void serial_print_stuff(){
  Serial.print("rc1: ");
  Serial.print(rc1_val);
  Serial.print("  rc2: ");
  Serial.print(rc2_val);
  Serial.print("  rc3: ");
  Serial.print(rc3_val);
  Serial.print("  flag: ");
  Serial.println(kill_motors_flag);
}
