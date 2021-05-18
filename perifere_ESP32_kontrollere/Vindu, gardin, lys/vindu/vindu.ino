#include <Arduino.h>
#include <CircusESP32Lib.h>
#include <ESP32Servo.h>

// lastes opp til hver enkelt ESP32 som styrer et vindu. CoT nækkelen må skiftes.
char token[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjI4In0.K58Zp9kRjEWJdlIkNRhD2yrV5EB6DcbDRnHsIVRspps";

char ssid[] = "Fredrik"; // Skriv inn navnet til ruteren din her.
char password[] = "yesyesyes"; // Skriv inn passordet til ruteren din her.
char server[] = "www.circusofthings.com"; // Her ligger serveren.
char key[] = "6488"; // Nøkkel-informasjon om konsollet for styring av vinduet
CircusESP32Lib circusESP32(server,ssid,password);// Her leses nettadressen til CoT, ssid, og
//... passord inn. Ikke gjør noen endringer her.

const int servoPin = 18;
const int t = 1000;
Servo servo;

int target_pos = 0; // posisjonen som servoen skal bevege seg til (mottas fra CoT)
int pos = 0; // Servoens posisjon
int dir = 1; // Retningen den beveger seg i

int windowState = 0;


void setup() {
  // put your setup code here, to run once:
  circusESP32.begin(); // Initialiserer oppkobling mot CoT
  servo.setPeriodHertz(50);
  servo.attach(servoPin, 1000,2000);
  
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(pos == 0 || pos == 180){ // dersom gardinen ikke beveger seg
    int CoT_signal = circusESP32.read(key,token);
    windowState = static_cast<int>(static_cast<String>(CoT_signal)[2] - 48); // leser fra CoT om gardinen er lukket "0" eller åpen "1"
    Serial.println(windowState);
  }
  
  if(windowState == 1){
    target_pos = 180;
  }
  else if(windowState == 0){
    target_pos = 0;
  }

  if(pos < target_pos){
    pos ++;
    delay(10);
  }
  else if(pos > target_pos){
    pos --;
    delay(10);
  }
  servo.write(pos);
  
}
