#include <Arduino.h>

int analogPin = 0;
int val = 0;

void setup()
{
  Serial.begin(115200);
  pinMode(2, INPUT);
}
void loop()
{
  val = analogRead(analogPin);     // read the input pin
  Serial.println(val);
  delay(100);
}
