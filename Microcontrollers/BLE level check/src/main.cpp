/*
   Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleScan.cpp
   Ported to Arduino ESP32 by Evandro Copercini
*/
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>


int scanTime = 1; //In seconds


void setup() {
  Serial.begin(115200);
}


void loop() {
  if(Serial.available() > 0){
    int Value = Serial.read();
    if (Value == 63){
      Serial.println("R");
    }
    else{

      BLEDevice::init("");
      BLEScan* pBLEScan = BLEDevice::getScan(); //create new scan
      pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
      BLEScanResults foundDevices = pBLEScan->start(scanTime);
      int count = foundDevices.getCount();

      for (int i = 0; i < count; i++)
                {
                  BLEAdvertisedDevice d = foundDevices.getDevice(i);
                  char mac[18] = "24:0a:64:43:77:df";
                  for (int b = 0; b < 17; b++){
                    mac[b] = d.getAddress().toString()[b];
                  }
                  // client.printf("Signal from: %s, level is: ", d.getAddress().toString());
                  // Serial.printf("Signal from: %s, level is: ", d.getAddress().toString());
                  Serial.print("M:");Serial.print(mac);Serial.print(" S:");
                  Serial.print(d.getRSSI()); Serial.print(";");
                }
      Serial.println();
    }
    }
}
