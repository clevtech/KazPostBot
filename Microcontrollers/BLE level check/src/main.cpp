/*
   Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleScan.cpp
   Ported to Arduino ESP32 by Evandro Copercini
*/
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <WiFi.h>

WiFiServer server(80);
int scanTime = 1; //In seconds
const char* ssid = "CleverestTech";
const char* password =  "Robotics1sTheBest";

void setup() {
  Serial.begin(115200);
    WiFi.begin(ssid, password);

        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
    }
    Serial.println();
    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    server.begin();

}

void loop() {
  BLEDevice::init("");
  BLEScan* pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  WiFiClient client = server.available();   // listen for incoming clients
      if (client) {                             // if you get a client,
        String currentLine = "";                // make a String to hold incoming data from the client
        while (client.connected()) {            // loop while the client's connected
          if (client.available()) {             // if there's bytes to read from the client,
            char c = client.read();             // read a byte, then
            if (c == '\n') {                    // if the byte is a newline character
                BLEScanResults foundDevices = pBLEScan->start(scanTime);
                int count = foundDevices.getCount();
                client.println("HTTP/1.1 200 OK");
                client.println("Content-type:text/html");
                for (int i = 0; i < count; i++)
                {
                  BLEAdvertisedDevice d = foundDevices.getDevice(i);
                  client.printf("Signal from: %s, level is: ", d.getAddress().toString());
                  Serial.printf("Signal from: %s, level is: ", d.getAddress().toString());
                  client.print(d.getRSSI());
                  client.println();
                }
                break;
              }
        }
      }
        // close the connection:
        client.stop();
      }

}
