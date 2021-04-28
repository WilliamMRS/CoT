//snakke til raspberry eller arduino?
#include <CircusESP32lib.h>

char ssid[] = "";
char password[] = "";
char token[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjA5In0.5a3-vboGDDnRC6akHjKlbSWLz6PM1uQPgts2WxzRGXc";
char server[] = "www.circusofthings.com";
char blinderkey[] = "9799";
char 

int TXPinToESP01 = 2;
int RXPinToESP01 = 3;
int esp01BaudRate = 9600;
int debugLevel = DEBUG_YES;
int 

CircusESP32lib circusESP32(server, ssid, password);

void setup() {
    serial.begin(115200);
    circusESP32.begin();
    serial.println("Klar");
}

void loop() {
    delay(5000);
    double d = circus.read(blinderkey, token);
    serial.print("Persiennene er: ");
    serial.println(d);
}