#include <Arduino.h>
#include <Ultrasonic.h>
#include <MotorDriver.h>

/*
0 - STOP
1 - FWD
2 - BWD
3 - turn_center
4 - turn_right
5 - turn_left
*/

// Turning sensor outputs
int LS = 39;
int RS = 37;
int CS = 35;

// Sonar values
Ultrasonic ultrasonicR(47, 46);
Ultrasonic ultrasonicC(49, 48);
Ultrasonic ultrasonicL(51, 50);

// Turn motor values
int L = 30;
int R = 28;

// Turning last point: 1 = center, 0 = left, 2 = right
int turn = 1;

// Motor shield
MotorDriver m;

// Done
void turn_left() {
  digitalWrite(L, HIGH);
  while(digitalRead(LS) > 0){
    delay(1);
  }
  digitalWrite(L, LOW);
  turn = 0;
}

// Done
void turn_right() {
  digitalWrite(R, HIGH);
  while(digitalRead(RS) > 0){
    delay(1);
  }
  digitalWrite(R, LOW);
  turn = 2;
}

// Done
void turn_center() {
  if(turn == 0){
    digitalWrite(R, HIGH);
    while(digitalRead(CS) > 0){
      delay(1);
    }
    digitalWrite(R, LOW);
    turn = 1;
  }
  else if(turn == 2){
    digitalWrite(L, HIGH);
    while(digitalRead(CS) > 0){
      delay(1);
    }
    digitalWrite(L, LOW);
    turn = 1;
  }
  else if(turn == 1){
    turn = 1;
  }
}

// Done
void FWD() {
  m.motor(1,FORWARD,0);
}

// Done
void BWD() {
  m.motor(2,FORWARD,0);
}

// Done
void STOP() {
  m.motor(1,FORWARD,255);
  m.motor(2,FORWARD,255);
}

// Done
void tackle() {
  if(ultrasonicC.distanceRead(CM)<30 or
      ultrasonicR.distanceRead(CM)<30 or
        ultrasonicL.distanceRead(CM)<30){
          STOP();
  }
}

void calibrate() {
  STOP();
  Serial.println("Turning right");
  turn_right();
  Serial.println("Turning right is done");
  delay(1000);
  Serial.println("Turning left");
  turn_left();
  Serial.println("Turning left is done");
  delay(1000);
  Serial.println("Turning center");
  turn_center();
  Serial.println("Turning center is done");
  delay(1000);
  Serial.println("Moving forward");
  FWD();
  delay(100);
  Serial.println("Stop");
  STOP();
  Serial.println("Moving backward");
  BWD();
  delay(100);
  Serial.println("Stop");
  STOP();
}

void setup() {
  STOP();
  Serial.begin(115200);
  delay(20000);
  Serial.println("Calibration is began");
  pinMode(L, OUTPUT);
  pinMode(R, OUTPUT);
  pinMode(LS, INPUT);
  pinMode(CS, INPUT);
  pinMode(RS, INPUT);
  calibrate();
  Serial.println("Calibration is done");
}

void loop() {
  calibrate();
}
