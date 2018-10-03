#include <Arduino.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

static const int RXPin = 8, TXPin = 9;
static const uint32_t GPSBaud = 9600;

// Assign a Uniquej ID to the HMC5883 Compass Sensor
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the NEO-6m GPS module
SoftwareSerial ss(RXPin, TXPin);


void displayCompassInfo()
{
  sensors_event_t event;
  mag.getEvent(&event);
  // Calculate heading when the magnetometer is level, then correct for signs of axis.
  float heading = atan2(event.magnetic.y, event.magnetic.x);
  float declinationAngle = 8;
  heading += declinationAngle;

  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;

  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;

  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI;

  Serial.println(headingDegrees);

  delay(500);
}



void displayGpsInfo()
{
  // Prints the location if lat-lng information was recieved
  if (gps.location.isValid())
  {
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6);
  }
  // prints invalid if no information was recieved in regards to location.
  else
  {
    Serial.print(F("INVALID"));
  }
  if(mag.begin())
  {
    Serial.print(",");
    displayCompassInfo();
  }
}



void setup()
{
  Serial.begin(115200);
  ss.begin(GPSBaud);
  Serial.read();
  Serial.println("GPS");
}

void loop()
{
  // This sketch displays information every time a new sentence is correctly encoded from the GPS Module.
  if (ss.available() > 0)
    if (gps.encode(ss.read()))
    if (Serial.read()=='g')
    displayGpsInfo();
}
