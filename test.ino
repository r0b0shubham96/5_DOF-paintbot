int encoderPin3 = 2;
int encoderPin4 = 3;
int DIR=9;
int PWM=10;

volatile int lastEncodedInp = 0;  
volatile long encoderValueInp = 0; 
 
int lastMSB = 0;                
int lastLSB = 0;        
void setup() {
   pinMode(encoderPin3, INPUT_PULLUP);
  pinMode(encoderPin4, INPUT_PULLUP);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(encoderPin3), updateEncoderInp, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPin4), updateEncoderInp, CHANGE);
 
  Serial.begin(9600);
  while (!Serial) {
    ; 
  }
  
}            
void updateEncoderInp(){
  int MSB = digitalRead(encoderPin3); //MSB = most significant bit
  int LSB = digitalRead(encoderPin4); //LSB = least significant bit
 
  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncodedInp << 2) | encoded; //adding it to the previous encoded value
 
  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValueInp ++;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValueInp --;
 
  lastEncodedInp = encoded; //store this value for next time  
}
void loop() {
Serial.println(abs(encoderValueInp));
moveMotorForward(30);
delay(1000);
//moveMotorBackward(30);
//delay(1000);
Serial.println(abs(encoderValueInp));
//encoderValueInp=0;
 }
 void moveMotorForward( int x) {
//  int X = x * 28;

  digitalWrite(DIR,LOW);
  analogWrite(PWM,30);
  while (200 <abs(encoderValueInp) < 210) 
  {
   Serial.println("1");
    break;
  }
  if (abs(encoderValueInp) < 200)
  {
    digitalWrite(DIR, LOW);
    analogWrite(PWM, 30);
    Serial.println("2");
    }
    else if (abs(encoderValueInp) > 210) 
    {
    digitalWrite(DIR, HIGH);
    analogWrite(PWM, 30);
    Serial.println("3");
    }

}


void moveMotorBackward( int x) {
  int X = x * 28;
 
  digitalWrite(DIR,HIGH);
  analogWrite(PWM,50);
  while (200 <abs(encoderValueInp) < 210) 
  {
   Serial.println("1");
    break;
  }
  if (abs(encoderValueInp) < 200)
  {
    digitalWrite(DIR, HIGH);
    analogWrite(PWM, 50);
    Serial.println("2");
    }
    else if (abs(encoderValueInp) > 210) 
    {
    digitalWrite(DIR, LOW);
    analogWrite(PWM, 30);
    Serial.println("3");
    }

}



//void LaForward( int x, int d) {
//
//  digitalWrite(DIR, LOW);
//  analogWrite(PWM, 90);
//  delay(200);
//  
//}
//void LaBackward(int x,int d) { 
//  analogWrite(PWM, 100);
//  digitalWrite(DIR, HIGH);
//  delay(d*1000);
//  Serial.println("B");
//}
//
//void halt() {
//  digitalWrite(DIR, HIGH);
//  analogWrite(PWM, 0);
//  Serial.println("H");
//  Serial.println(encoderValueInp);
//
//}
