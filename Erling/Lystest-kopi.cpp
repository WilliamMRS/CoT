//snakke til raspberry eller arduino?
#include <CircusESP32lib.h>

char ssid[] = "";
char password[] = "";
char token[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjA5In0.5a3-vboGDDnRC6akHjKlbSWLz6PM1uQPgts2WxzRGXc";
char server[] = "www.circusofthings.com";
char LightKey[] = "23790";

int TXPinToESP01 = 2;
int RXPinToESP01 = 3;
int esp01BaudRate = 9600;
int debugLevel = DEBUG_YES;
int LightPin = 4;

CircusESP32lib circusESP32(server, ssid, password);

void setup() {
    Serial.begin(115200);
    circusESP32.begin();
    PinMode(LightPin, OUTPUT);
    Serial.println("Klar");
}

void loop() {
    int Lightstate = circusESP32.read(LightKey, token);
    digitalWrite(LightPin, Lightstate);
    Serial.print("Lyset er: ");
    Serial.println(Lightstate);
    delay(1000);
}