#include <NewPing.h>

#define SONAR_NUM 3      // Number of sensors.
#define MAX_DISTANCE 200 // Maximum distance (in cm) to ping.

NewPing sonar[SONAR_NUM] = {   // Sensor object array.
  NewPing(4, 5, MAX_DISTANCE), // Each sensor's trigger pin, echo pin, and max distance to ping.
  NewPing(6, 7, MAX_DISTANCE),
  NewPing(8, 9, MAX_DISTANCE)
};

void setup() {
  int incomingByte = 0;
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
  int OBSTACLE = 0;
  for (uint8_t i = 0; i < SONAR_NUM; i++) {
    delay(30); // Min wait is 29
    int pings = sonar[i].ping_cm();
    if ((pings < 100) && (pings > 0)){
      OBSTACLE = 1;
    }
  }
  if (OBSTACLE == 1) {
    Serial.println("1");
  }
  else {
    Serial.println("0");
  }
}

