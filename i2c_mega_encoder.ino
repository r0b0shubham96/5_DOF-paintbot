#include <Wire.h>

#define SLAVE_ADDRESS 0x04

String received_data = "";
String copy_data = "";
bool finish = false;
bool start = false;

int link2_encoder1 = 2;
int link2_encoder2 = 3;

int base_encoder1 = 18;
int base_encoder2 = 19;

int no_encoder_pulse = 360;

void setup() {
  // Setting pin modes for the encoder pin1 and pin2, that are interrupt pins and pullup these pins internally.
  pinMode(link2_encoder1, INPUT_PULLUP);
  pinMode(link2_encoder2, INPUT_PULLUP);

  pinMode(base_encoder1, INPUT_PULLUP);
  pinMode(base_encoder2, INPUT_PULLUP);

  // Interrupt for encoder pulses that are receiving as an input to the controller.
  attachInterrupt(digitalPinToInterrupt(link2_encoder1), updateLink2Encoder, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(link2_encoder2), updateLink2Encoder, CHANGE);

  attachInterrupt(digitalPinToInterrupt(base_encoder1), updateBaseEncoder, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(base_encoder2), updateBaseEncoder, CHANGE);
  
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

volatile int lastEncodedLink2 = 0;  
volatile long encoderValueLink2 = 0;

volatile int lastEncodedBase = 0;  
volatile long encoderValueBase = 0; 
 
//int lastMSB = 0;                // variable for the most significant bit to measure the encoder value in different direction
//int lastLSB = 0;                // variable for the least significant bit to measure the encoder value in different direction

void loop() {
  if (finish == true) {
  }
}

void updateLink2Encoder(){
  int MSB = digitalRead(link2_encoder1); //MSB = most significant bit
  int LSB = digitalRead(link2_encoder2); //LSB = least significant bit
 
  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncodedLink2 << 2) | encoded; //adding it to the previous encoded value
 
  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValueLink2 ++;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValueLink2 --;
 
  lastEncodedLink2 = encoded; //store this value for next time
}

void updateBaseEncoder(){
  int MSB = digitalRead(base_encoder1); //MSB = most significant bit
  int LSB = digitalRead(base_encoder2); //LSB = least significant bit
 
  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncodedBase << 2) | encoded; //adding it to the previous encoded value
 
  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValueBase ++;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValueBase --;
 
  lastEncodedBase = encoded; //store this value for next time
}

void receiveData(int byteCount) {
  char data = char(Wire.read());
  if (start == false) {
    if (data == '<') {
      start = true;
    }
  } else {
    if (data == '>') {
      copy_data = received_data;
      received_data = "";
      finish = true;
      start = false;
    } else {
      received_data += data;
    }
  }
}

void sendData() {
  //union
  //{
  //  uint8_t baseByte[4];
  //  float baseEncoderPulse;
  //} base;

  //union
  //{
  // uint8_t link2Byte[4];
  //  float link2EncoderPulse;
  //} link2;
  
  //link2.link2EncoderPulse = encoderValueLink2;
  //base.baseEncoderPulse = encoderValueBase;
  
  //Wire.write(link1.myByte, 4);

  union
  {
    uint8_t myByte[8];
    float link2EncoderPulse;
    float baseEncoderPulse;
  } link;

  link.link2EncoderPulse = encoderValueLink2;
  link.baseEncoderPulse = encoderValueBase;

  Wire.write(link.myByte, 8);
}