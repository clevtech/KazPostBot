#include <Arduino.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>


static const int RXPin = 8, TXPin = 9;
static const uint32_t GPSBaud = 9600;
float headingDegrees = 0;
float LNG = 0;
float LAT = 0;

// Assign a Uniquej ID to the HMC5883 Compass Sensor
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the NEO-6m GPS module
SoftwareSerial ss(RXPin, TXPin);


void displayCompassInfo()
{
  sensors_event_t event;
  delay(100);
  mag.begin();
  mag.getEvent(&event);
  delay(100);
  float heading = atan2(event.magnetic.y, event.magnetic.x);
  float declinationAngle = 0.22;
  heading += declinationAngle;
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;

  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;

  // Convert radians to degrees for readability.
  headingDegrees = heading * 180/M_PI;
}

void displayGpsInfo()
{
  if (gps.location.isValid())
  {
    LAT = gps.location.lat();
    LNG = gps.location.lng();
  }
  // prints invalid if no information was recieved in regards to location.
  else
  {
    LAT = 0;
    LNG = 0;
  }
}

void setup()
{
  sensor_t sensor;
  mag.getSensor(&sensor);
  Serial.begin(115200);
  delay(3000);
  ss.begin(GPSBaud);
  delay(3000);
}

void loop()
{
  if(Serial.available()){
    int Value = Serial.read();
    if (Value==103){
      if(ss.available()){
        delay(100);
        while(gps.encode(ss.read()))
          delay(100);
          displayGpsInfo();
          delay(100);
          displayCompassInfo();
          // delay(100);
    }
    else{
      Serial.println("GPS sensor is not available");
    }
        Serial.println(String(LAT) + ";" + String(LNG) + ";" + String(headingDegrees));
    }
    else{
      Serial.println("GPS");
    }
}
}
