#include "Wire.h"
#include "Adafruit_ADS1X15.h"

Adafruit_ADS1115 ads1, ads2;
int adc0, adc1, adc2, adc3, adc4;
char check;

void setup(){
  Serial.begin(115200);
  ads1.begin(0x48);
  ads2.begin(0x49);
  ads1.setGain(GAIN_FOUR);
  ads2.setGain(GAIN_FOUR);
//                                              S                  ADS1015  ADS1115
//                                                                -------  -------
// ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
// ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
// ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
// ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
// ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
// ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV
  Serial.println("connected");
}

void loop(){  
  if (Serial.available()){
    while (Serial.available()) {Serial.read();}
    check = Serial.read();
    if (check = 'a'){
        adc0 = ads1.readADC_SingleEnded(0);
        adc1 = ads1.readADC_SingleEnded(1);
        adc2 = ads1.readADC_SingleEnded(2);
        adc3 = ads1.readADC_SingleEnded(3);
        adc4 = ads2.readADC_SingleEnded(0);
        
        Serial.print(adc0); Serial.print(", ");
        Serial.print(adc1); Serial.print(", ");
        Serial.print(adc2); Serial.print(", ");
        Serial.print(adc3); Serial.print(", ");
        Serial.print(adc4); Serial.println();
        
    }
    }
}
