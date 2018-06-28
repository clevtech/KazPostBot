#include "Arduino.h"
#include "digitalWriteFast.h"
#define c_LeftEncoderInterruptA 0
#define c_LeftEncoderInterruptB 1
#define c_LeftEncoderPinA 2
#define c_LeftEncoderPinB 3
#define LeftEncoderIsReversed

int leftPosition;
int rightPosition;
int middlePosition;

volatile bool _LeftEncoderASet;
volatile bool _LeftEncoderBSet;
volatile bool _LeftEncoderAPrev;
volatile bool _LeftEncoderBPrev;
volatile long _LeftEncoderTicks = 0.0;
volatile long _LeftEncoderTicksPast = 0.0;
float pos = 0.0;
void setup()
{
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  Serial.begin (9600);
  pinMode(c_LeftEncoderPinA, INPUT);      // sets pin A as input
  digitalWrite(c_LeftEncoderPinA, LOW);  // turn on pullup resistors
  pinMode(c_LeftEncoderPinB, INPUT);      // sets pin B as input
  digitalWrite(c_LeftEncoderPinB, LOW);  // turn on pullup resistors
  attachInterrupt(c_LeftEncoderInterruptA, HandleLeftMotorInterruptA, CHANGE);
  attachInterrupt(c_LeftEncoderInterruptB, HandleLeftMotorInterruptB, CHANGE);
//  left
//  digitalWrite(12, LOW);
//  digitalWrite(13, HIGH);
//  delay(1000);
//  digitalWrite(12, LOW);
//  digitalWrite(13, LOW);
//  leftPosition = pos;
//  digitalWrite(12, HIGH);
//  digitalWrite(13, LOW);
}

int counter = 0;
int thresh = 7;
int goal;

void loop()
{
if (counter > 100 && counter < 200){
    digitalWrite(12, LOW);
    digitalWrite(13, HIGH);
    leftPosition = pos;
    Serial.print("Left:");
    Serial.println(leftPosition);
  }else if(counter > 200 && counter < 300){
    digitalWrite(12, HIGH);
    digitalWrite(13, LOW);
    rightPosition = pos;
    Serial.print("Right:");
    Serial.println(rightPosition);
  }
//  else{
//    if (pos < goal - thresh){
//      digitalWrite(12, HIGH);
//      digitalWrite(13, LOW);
//    }else if(pos > goal + thresh){
//      digitalWrite(12, LOW);
//      digitalWrite(13, HIGH);
//    }else{
//      digitalWrite(12, LOW);
//      digitalWrite(13, LOW);
//    }
//  }
  delay(1);
  pos = (_LeftEncoderTicks);
  Serial.println(pos);
//  if(Serial.available()) {
//    Serial.read();
//    Serial.println(pos);
//  }
  counter++;
}

void calibrate(){
  
}

// Interrupt service routines for the left motor's quadrature encoder
void HandleLeftMotorInterruptA(){
  _LeftEncoderBSet = digitalReadFast(c_LeftEncoderPinB);
  _LeftEncoderASet = digitalReadFast(c_LeftEncoderPinA);
  
  _LeftEncoderTicks+=ParseEncoder();
  
  _LeftEncoderAPrev = _LeftEncoderASet;
  _LeftEncoderBPrev = _LeftEncoderBSet;
}

// Interrupt service routines for the right motor's quadrature encoder
void HandleLeftMotorInterruptB(){
  // Test transition;
  _LeftEncoderBSet = digitalReadFast(c_LeftEncoderPinB);
  _LeftEncoderASet = digitalReadFast(c_LeftEncoderPinA);
  
  _LeftEncoderTicks+=ParseEncoder();
  
  _LeftEncoderAPrev = _LeftEncoderASet;
  _LeftEncoderBPrev = _LeftEncoderBSet;
}

int ParseEncoder(){
  if(_LeftEncoderAPrev && _LeftEncoderBPrev){
    if(!_LeftEncoderASet && _LeftEncoderBSet) return 1;
    if(_LeftEncoderASet && !_LeftEncoderBSet) return -1;
  }else if(!_LeftEncoderAPrev && _LeftEncoderBPrev){
    if(!_LeftEncoderASet && !_LeftEncoderBSet) return 1;
    if(_LeftEncoderASet && _LeftEncoderBSet) return -1;
  }else if(!_LeftEncoderAPrev && !_LeftEncoderBPrev){
    if(_LeftEncoderASet && !_LeftEncoderBSet) return 1;
    if(!_LeftEncoderASet && _LeftEncoderBSet) return -1;
  }else if(_LeftEncoderAPrev && !_LeftEncoderBPrev){
    if(_LeftEncoderASet && _LeftEncoderBSet) return 1;
    if(!_LeftEncoderASet && !_LeftEncoderBSet) return -1;
  }
}
