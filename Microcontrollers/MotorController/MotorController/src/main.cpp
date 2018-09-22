#include <Arduino.h>
#include <Ultrasonic.h>

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
#define L  A1
#define R  A0

// Motor values
#define FRW  A3
#define BCW  A2

// Turning last point: 1 = center, 0 = left, 2 = right
int turn = 1;

// Done
void turn_left() {
  digitalWrite(L, LOW);
  while(digitalRead(LS) > 0){
    delay(1);
  }
  digitalWrite(L, HIGH);
  turn = 0;
}

// Done
void turn_right() {
  digitalWrite(R, LOW);
  while(digitalRead(RS) > 0){
    delay(1);
  }
  digitalWrite(R, HIGH);
  turn = 2;
}

// Done
void turn_center() {
  if(turn == 0){
    digitalWrite(R, LOW);
    while(digitalRead(CS) > 0){
      delay(1);
    }
    digitalWrite(R, HIGH);
    turn = 1;
  }
  else if(turn == 2){
    digitalWrite(L, LOW);
    while(digitalRead(CS) > 0){
      delay(1);
    }
    digitalWrite(L, HIGH);
    turn = 1;
  }
  else if(turn == 1){
    turn = 1;
  }
}

// Done
void FWD() {
  digitalWrite(FRW, LOW);
}

// Done
void BWD() {
  digitalWrite(BCW, LOW);
}

// Done
void STOP() {
  digitalWrite(FRW, HIGH);
  digitalWrite(BCW, HIGH);
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
  digitalWrite(L, HIGH);
  digitalWrite(R, HIGH);
  STOP();
  // Serial.println("Turning right");
  // turn_right();
  // Serial.println("Turning right is done");
  // delay(1000);
  // Serial.println("Turning left");
  // turn_left();
  // Serial.println("Turning left is done");
  // delay(1000);
  // Serial.println("Turning center");
  // turn_center();
  // Serial.println("Turning center is done");
  // delay(1000);
  Serial.println("Turning right");
  digitalWrite(R, LOW);
  delay(100);
  digitalWrite(R, HIGH);
  Serial.println("Turned right");
  delay(1000);
  Serial.println("Turning left");
  digitalWrite(L, LOW);
  delay(100);
  digitalWrite(L, HIGH);
  Serial.println("Turned left");
  delay(1000);
  Serial.println("Moving forward");
  FWD();
  delay(1000);
  Serial.println("Stop");
  STOP();
  Serial.println("Moving backward");
  BWD();
  delay(1000);
  Serial.println("Stop");
  STOP();
  delay(1000);
}

void setup() {
  Serial.begin(115200);
  delay(20000);
  Serial.println("Calibration is began");
  pinMode(FRW, OUTPUT);
  pinMode(BCW, OUTPUT);
  pinMode(L, OUTPUT);
  pinMode(R, OUTPUT);
  pinMode(LS, INPUT);
  pinMode(CS, INPUT);
  pinMode(RS, INPUT);
  STOP();
  calibrate();
  Serial.println("Calibration is done");
}

void loop() {
  Serial.println("Turn right");
  while(digitalRead(RS) < 1){
    delay(1);
  }
  Serial.println("Turned right");
  delay(1000);
  Serial.println("Turn center");
  while(digitalRead(CS) < 1){
    delay(1);
  }
  Serial.println("Turned center");
  delay(1000);
  Serial.println("Turn left");
  while(digitalRead(LS) < 1){
    delay(1);
  }
  Serial.println("Turned left");
  delay(1000);
  // calibrate();
}
