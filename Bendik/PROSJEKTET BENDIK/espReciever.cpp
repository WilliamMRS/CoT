
#include <CircusESP32lib.h>
#include key

char token = key ; 

char ssid[] = "";
char password[] = "";

char server[] = "www.circusofthings.com";
char consumerKey[] = "23790";

int TXPinToESP01 = 2;
int RXPinToESP01 = 3;
int esp01BaudRate = 9600;
int debugLevel = DEBUG_YES;
int powerPin = 4;

CircusESP32lib circusESP32(server, ssid, password);


void setup() {
    Serial.begin(115200);
    circusESP32.begin();
    PinMode(powerPin, OUTPUT);
    Serial.println("Initialized...");
}




void espID() {
    int n;
    cin << n;
    switch (n) {
        case 1 : 
            // Livingroom. Run functions for this room
        int livingroomLights = ; 
        int TV;
        int heatcables; 

        break;
        case 2 :
            // Kitchen. Run functions for this room 
        break; 
        case 3 :
            // bathroom. Run functions for this room 
        break; 
        case 4 :
            // bedroom 1. Run functions for this room 
        break; 
        case 5 :
            // bedroom 2. Run functions for this room 
        break; 
        case 6 :
            // bedroom 3. Run functions for this room 
        break; 
        case 7 :
            // bedroom 4. Run functions for this room 
        break;
        case 8 :
            // bedroom 5. Run functions for this room 
        break; 
        case 9 :
            // bedroom 6. Run functions for this room 
        break;  
    }
}



void loop() {
    int powerState = circusESP32.read(consumerKey, token);
    digitalWrite(powerPin, powerState);
    Serial.print("Status: " + powerState);
    delay(1000);
}




