#include <Arduino.h>

void setup()
{
  Serial.begin(115200);
}
void loop()
{
  Serial.println(digitalRead(2)); // print the data from the sensor
  // delay(500);
}
