#include <Arduino.h>
#include <Ultrasonic.h>

#define SONAR_NUM 3      // Number of sensors.
#define MAX_DISTANCE 160 // Maximum distance (in cm) to ping.

int OBSTACLE = 0;

// Sonar values
Ultrasonic ultrasonicR(13, 12);
Ultrasonic ultrasonicC(11, 10);
Ultrasonic ultrasonicL(24, 25);

void STOP(){
  Serial.print("1st One: ");
  delay(50);
  Serial.print(ultrasonicC.distanceRead(CM));
  Serial.print(" | 2nd One: ");
  delay(50);
  Serial.print(ultrasonicL.distanceRead(CM));
  Serial.print(" | 3rd One: ");
  delay(50);
  Serial.print(ultrasonicR.distanceRead(CM));
  Serial.println("");
  // Serial.println("FUCK!");
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
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
  while(!Serial.available() ){
    delay(10);
    }
  if (Serial.available() > 0) {
                // read the incoming byte:
                char incomingByte = Serial.read();
                // say what you got:
                Serial.println("Sonar");
        }
}

void loop() {


  if (Serial.available() > 0){
    Serial.read();
    tackle();
  }
}
