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

#define d 300

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
      del = d;
    }
    else{
      del = 2*d;
    }
    digitalWrite(L, LOW);
    int i = 0;
    while(i < del){
      delay(1);
      i = i + 1;
    }
    digitalWrite(L, HIGH);
    //Serial.println(i);
    turn = 0;
  }
}

// Done
void turn_right() {
  int del = 0;
  if(turn != 2){
    if(turn == 1){
      del = d;
    }
    else{
      del = 2*d;
    }
    digitalWrite(R, LOW);
    int i = 0;
    while(i < del){
      delay(1);
      i = i + 1;
    }
    digitalWrite(R, HIGH);
    //Serial.println(i);
    turn = 2;
  }
}

// Done
void turn_center() {
  analogWrite(RS, 1024);
  int i = 0;
  if(turn == 0){
    digitalWrite(R, LOW);
    while(analogRead(RS) > 24 and i < d){
      delay(1);
      i = i + 1;
      analogWrite(RS, 1024);
    }
    digitalWrite(R, HIGH);
    //Serial.println(i);
    turn = 1;
  }
  else if(turn == 2){
    digitalWrite(L, LOW);
    while(analogRead(RS) > 25 and i < d){
      delay(1);
      i = i + 1;
      analogWrite(RS, 1024);
    }
    digitalWrite(L, HIGH);
    //Serial.println(i);
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
  int UR1 = ultrasonicC.distanceRead(CM);
  delay(50);
  int UR2 = ultrasonicR.distanceRead(CM);
  delay(50);
  int UR3 = ultrasonicL.distanceRead(CM);
  if(UR1<40 and UR1>0 or
      UR2<40 and UR2>0 or
        UR3<40 and UR3>0){
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
  tackle();
  if (Serial.available() > 0) {
    int Value = Serial.read();
    if (Value == 63){
      Serial.println("MOT");
      analogWrite(RS, 1024);

    }
    else{
                tackle();
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

                tackle();
              }
      }
      else{
        STOP();
        turn_center();
      }
}
