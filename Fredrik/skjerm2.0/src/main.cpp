
#include <Option.h>
#include <Menu.h>
#include <Button.h>

#include <Arduino.h>
#include <SPI.h>
#include <TFT_eSPI.h>       // Hardware-specific library
#include <string>
#include <CircusESP32Lib.h>

int resident_ID = 1; // ID som beskriver hvilken bruker ESP-kontrollen tilhører (må endres for hver enkelt ESP-kontroll) PS: ikke nullindeksert!

//#include "soc/soc.h"
//#include "soc/rtc_cntl_reg.h"

// ------------------------------------------------
// These are the CircusESP32Lib related declarations
// ------------------------------------------------

char ssid[] = "Fredrik"; // Place your wifi SSID here
char password[] =  "yesyesyes"; // Place your wifi password here
char token[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjI4In0.K58Zp9kRjEWJdlIkNRhD2yrV5EB6DcbDRnHsIVRspps"; // Place your token, find it in 'account' at Circus. It will identify you.
char server[] = "www.circusofthings.com";
char key[] = "9940"; // Type the Key of the Circus Signal you want the ESP32 listen to. 
CircusESP32Lib circusESP32(server,ssid,password); // The object representing an ESP32 to whom you can order to Write or Read


TFT_eSPI tft = TFT_eSPI();  // Invoke custom library

Main_menu main_menu{"HOVEDMENY:"}; // meny nr. 0
Booking_menu booking_menu{"BOOKING:"}; // meny nr. 1
Room_booking_menu room0_booking_menu{"BOOK BATHROOM:", resident_ID, 0}; // meny nr. 2
Room_booking_menu room1_booking_menu{"BOOK LIVINGROOM:", resident_ID, 1}; // meny nr. 3
Room_booking_menu room2_booking_menu{"BOOK KITCHEN:", resident_ID, 2}; // meny nr. 4

Menu* menus[5] = {&main_menu, &booking_menu, &room0_booking_menu, &room1_booking_menu, &room2_booking_menu};



//int prev_but_val = 0;

int cur_menu = 0; // (current_menu) beskriver hvilken meny man er innpå (eks: cur_menu == 0 => man ser på main_menu)


Button down_but(25); // knapp til pin 25
Button select_but(26); // knapp til pin 26

void setup(void) {
// Let the Circus object set up itself for an SSL/Secure connection
  circusESP32.begin(); 

  // kjører setup for knappene
  down_but.setup();
  select_but.setup();

  tft.init();
  
  tft.invertDisplay( true ); // for å få riktige farger
 
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(0, 0, 4); // setter riktig skrift-font 

  Serial.begin(115200);
}



void loop() {
  //circusESP32.write(key,13, token);

  // buttons:
  down_but.update_cur_val();
  select_but.update_cur_val();

  menus[cur_menu]->draw_menu(tft);
  if(down_but.pressed()){
    menus[cur_menu]->increment_cursor();
  }
  if(select_but.pressed()){
    menus[cur_menu]->select_option(cur_menu);
    tft.fillScreen(TFT_BLACK);
  }

  down_but.update_prev_val();
  select_but.update_prev_val();
}


