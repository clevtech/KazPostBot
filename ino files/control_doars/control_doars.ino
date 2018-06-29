#define interval 300
void setup() {
  int incomingByte = 0;
  int ledPins[] = {0, 1, 2, 3, 4, 5, 6, 7}; // LED pins
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
       pinMode(ledPins[p], OUTPUT); // Set the mode to OUTPUT
   }
}

void loop()
{
  if (Serial.available() > 0) {
                // read the incoming byte:
                int incomingByte = Serial.read() - 48;
                // say what you got:
                
                digitalWrite(incomingByte, HIGH);
                delay(interval);
                digitalWrite(incomingByte, LOW);
                Serial.println(incomingByte);
        }
}
