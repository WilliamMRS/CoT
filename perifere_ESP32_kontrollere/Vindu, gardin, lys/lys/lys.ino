#include <Arduino.h>
#include <CircusESP32Lib.h>

// lastes opp til hver enkelt ESP32 som styrer et lys. CoT nækkelen må skiftes.
char token[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjI4In0.K58Zp9kRjEWJdlIkNRhD2yrV5EB6DcbDRnHsIVRspps";

char ssid[] = "Fredrik"; // Skriv inn navnet til ruteren din her.
char password[] = "yesyesyes"; // Skriv inn passordet til ruteren din her.
char server[] = "www.circusofthings.com"; // Her ligger serveren.
char key[] = "27272"; // Nøkkel-informasjon om konsollet for styring av vinduet
CircusESP32Lib circusESP32(server,ssid,password);// Her leses nettadressen til CoT, ssid, og
//... passord inn. Ikke gjør noen endringer her.

int lightPin = 18;
void setup() {
  // put your setup code here, to run once:
  circusESP32.begin(); // Initialiserer oppkobling mot CoT
  pinMode(lightPin, OUTPUT); // kan kobles til en relay for å styre lys knyttet til strømnettet i et hus.
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  int CoT_signal = circusESP32.read(key,token);
  int lightState = static_cast<int>(static_cast<String>(CoT_signal)[1] - 48); // leser fra CoT om gardinen er lukket "0" eller åpen "1"
  Serial.println(lightState);
  digitalWrite(lightPin, lightState);
}
