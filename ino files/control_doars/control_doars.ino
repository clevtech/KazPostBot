#define interval 3
void setup() {
  int incomingByte = 0;
  int ledPins[] = {23, 25, 27, 29, 31, 33, 35, 37}; // LED pins
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
       digitalWrite(ledPins[p], HIGH);
   }
}

void loop()
{
  if (Serial.available() > 0) {
                // read the incoming byte:
                int incomingByte = Serial.read() - 48;
         
                // say what you got:
                int ledPins[] = {23, 25, 27, 29, 31, 33, 35, 37}; // LED pins
                Serial.println(ledPins[incomingByte]);
                digitalWrite(ledPins[incomingByte], LOW);
                delay(interval);
//                digitalWrite(ledPins[incomingByte], LOW);
                
        }
}
