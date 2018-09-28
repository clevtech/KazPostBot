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
#define LS A7
#define RS A4
#define CS A5

// Sonar values
Ultrasonic ultrasonicR(13, 12);
Ultrasonic ultrasonicC(11, 10);
Ultrasonic ultrasonicL(24, 25);

// Turn motor values
#define L  29
#define R  31

// Motor values
#define FRW  53
#define BCW  51

// Turning last point: 1 = center, 0 = left, 2 = right
int turn = 1;

// Done
void turn_left() {
  int del = 0;
  if(turn != 0){
    if(turn == 1){
      del = 60;
    }
    else{
      del = 120;
    }
    digitalWrite(L, LOW);
    int i = 0;
    while(i < del){
      delay(1);
      i = i + 1;
    }
    digitalWrite(L, HIGH);
    Serial.println(i);
    turn = 0;
  }
}

// Done
void turn_right() {
  int del = 0;
  if(turn != 2){
    if(turn == 1){
      del = 60;
    }
    else{
      del = 120;
    }
    digitalWrite(R, LOW);
    int i = 0;
    while(i < del){
      delay(1);
      i = i + 1;
    }
    digitalWrite(R, HIGH);
    Serial.println(i);
    turn = 2;
  }
}

// Done
void turn_center() {
  int i = 0;
  if(turn == 0){
    digitalWrite(R, LOW);
    while(analogRead(CS) > 1 and i < 60){
      delay(1);
      i = i + 1;
    }
    digitalWrite(R, HIGH);
    Serial.println(i);
    turn = 1;
  }
  else if(turn == 2){
    digitalWrite(L, LOW);
    while(analogRead(CS) > 1 and i < 60){
      delay(1);
      i = i + 1;
    }
    digitalWrite(L, HIGH);
    Serial.println(i);
    turn = 1;
  }
  else if(turn == 1){
    turn = 1;
  }
}

// Done
void FWD() {
  digitalWrite(FRW, LOW);
  digitalWrite(BCW, HIGH);
}

// Done
void BWD() {
  digitalWrite(FRW, HIGH);
  digitalWrite(BCW, LOW);
}

// Done
void STOP() {
  digitalWrite(FRW, HIGH);
  digitalWrite(BCW, HIGH);
  digitalWrite(L, HIGH);
  digitalWrite(R, HIGH);
}

// Done
void tackle() {
  if(ultrasonicC.distanceRead(CM)<30 or
      ultrasonicR.distanceRead(CM)<30 or
        ultrasonicL.distanceRead(CM)<30){
          STOP();
  }
}


void setup() {
  Serial.begin(115200);
  pinMode(FRW, OUTPUT);
  pinMode(BCW, OUTPUT);
  pinMode(L, OUTPUT);
  pinMode(R, OUTPUT);
  STOP();
}

void loop() {
  if (Serial.available() > 0) {
    int Value = Serial.read();
    if (Value == 63){
      Serial.println("MOT");
    }
    else{
                //tackle();
                // read the incoming byte:
                int incomingByte = Value - 48;
                if(incomingByte == 0){
                  STOP();
                }
                else if(incomingByte == 1){
                  FWD();
                }
                else if(incomingByte == 2){
                  BWD();
                }
                else if(incomingByte == 3){
                  turn_center();
                }
                else if(incomingByte == 4){
                  turn_right();
                }
                else if(incomingByte == 5){
                  turn_left();
                }

                //tackle();
              }
      }
}
