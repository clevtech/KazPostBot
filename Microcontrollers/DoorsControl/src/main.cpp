#include <Arduino.h>
#define interval 10000

void setup() {
  int incomingByte = 0;
  int ledPins2[] = {23, 25, 27, 29, 33, 31, 37, 35}; // LED pins
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
  while(!Serial.available() ){
    delay(10);
    }
  if (Serial.available() > 0) {
                // read the incoming byte:
                char incomingByte = Serial.read();
                // say what you got:
                Serial.println("Box");
        }
  for(int p=0; p<8; p++)
   {
       pinMode(ledPins2[p], OUTPUT); // Set the mode to OUTPUT
       digitalWrite(ledPins2[p], HIGH);
   }
}

void loop()
{
  if (Serial.available() > 0) {
    int Value = Serial.read();
    if (Value == 63){
      Serial.println("Box");
    }
    else{
                // read the incoming byte:
                int incomingByte = Value - 48;

                // say what you got:
//                int ledPins[] = {23, 25, 27, 29, 31, 33, 35, 37}; // LED pins
                int ledPins[] = {31, 33, 35, 37, 29, 27, 25, 23};
                Serial.println(ledPins[incomingByte]);
                digitalWrite(ledPins[incomingByte], LOW);
                delay(interval);
                digitalWrite(ledPins[incomingByte], HIGH);
  }
        }
}
