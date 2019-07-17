#include <Wire.h>

#define SLAVE_ADDRESS 0x05

//char number[10];
//int state = 0;

String received_data = "";
String copy_data = "";
bool finish = false;
bool start = false;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  if (finish == true) {
    finish = false;
    String a_val = copy_data.substring(copy_data.indexOf('a') + 1, copy_data.indexOf('d'));
//    String t_val = copy_data.substring(copy_data.indexOf('t') + 1);
    String d_val = copy_data.substring(copy_data.indexOf('d') + 1, copy_data.indexOf('h'));
    String h_val = copy_data.substring(copy_data.indexOf('h') + 1);
    int a_val_int = a_val.toInt();
//    int t_val_int = t_val.toInt();
    int d_val_int = d_val.toInt();
    int h_val_int = h_val.toInt();
    Serial.println(a_val_int);
//    Serial.println(t_val_int);
    Serial.println(d_val_int);
    Serial.println(h_val_int);
  }
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
  union
  {
    uint8_t myByte[4];
    float link1EncoderPulse;
  } link1;
  
  link1.link1EncoderPulse = encoderValueLink1;
  
  Wire.write(link1.myByte, 4);
}