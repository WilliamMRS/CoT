#include <Arduino.h>
#include <TFT_eSPI.h>
#include <CircusESP32Lib.h>
#include <Option.h>
#include <string>
#pragma once

class Menu{
    protected:
        String header; // overskriften til menyen
        int cursor = 0; // hvilken 'option' som er valgt (går fra 0 til sizeof(options) - 1) (starter på 0 ("toppen" av menyen))
        int prev_cursor = 0;
    public:
        Menu(String h): header{h}{}
        virtual void draw_menu(TFT_eSPI tft) = 0;//, int cursor) = 0; // tegner menyen til skjermen
        virtual void increment_cursor() = 0; // inkrementerer Cursor med 1 (eks: dersom man blar ett hakk ned på menyen -> neste valg skal "highlightes")
        virtual void select_option(int& menu_value) = 0; // aktiveres av å trykke på det valgte valget og utfører en handling som tilhører valget (varierer med forskjellige valgtyper)
        
        //virtual void decrement_cursor() = 0; // dekrementerer Cursor med 1
};

//Klassene under arver fra den virtuelle klassen "Menu"

class Main_menu : public Menu{
    private:
        //under er alle valgene som menyen består av
        Menu_option opt1{"Booking", 1};
        Menu_option opt2{"Option2", 0};
        Menu_option opt3{"Option3", 0};
        Option* options[3] = {&opt1, &opt2, &opt3};
    public:
        Main_menu(String h) : Menu(h){}
        void draw_menu(TFT_eSPI tft);//, int cursor);
        void increment_cursor();
        void select_option(int& menu_value);
        //void decrement_cursor();
};

class Booking_menu : public Menu{
    private:
        Menu_option opt1{"Bathroom", 2};
        Menu_option opt2{"Livingroom", 3};
        Menu_option opt3{"Kitchen", 4};
        Menu_option opt4{"<- Back", 0};
        Option* options[4] = {&opt1, &opt2, &opt3, &opt4};
    public:
        Booking_menu(String h) : Menu(h){}
        void draw_menu(TFT_eSPI tft);//, int cursor);
        void increment_cursor();
        void select_option(int& menu_value);
        //void decrement_cursor();
};

class Room_booking_menu : public Menu{
    private:
        //bool option_selected = false; // sjekker om et valg er valgt. Da skal ikke 'cursor' inkrementeres
        int resident; // ID som beskriver hvilken bruker som øsnker å booke rom
        int selected_room; // rom-nummeret som er valgt
        int start_hour; // tidspunktet man vil booke fra
        int start_minute; // ^^^^^^^^
        int duration; // hvor lenge man ønsker å booke
        int time_selected = 0;
        bool dur_selected = false;
        Time_option time_opt{"Start-time: "};
        //Hour_option opt2{""};
        Duration_option dur_opt{"Duration: "};
        Signal_option signal_opt{"Book room"};
        Menu_option opt4{"<- Back", 1};
        Option* options[4] = {&time_opt, &dur_opt, &signal_opt, &opt4};
    public:
        Room_booking_menu(String h, int res_num, int room_num) : Menu(h), resident{res_num}, selected_room{room_num}{}
        void draw_menu(TFT_eSPI tft);//, int cursor);
        void increment_cursor();
        void select_option(int& menu_value);
    
};

/*
rom-booking:
format på menyen:
    Booking:
        -rom1
        -rom2
        -rom3
        -> lagrer et tall som beskriver hvilket rom som er valgt.
        -> går så videre til neste meny hvor man kan velge:
            -starttidspunkt
            -varighet
            - person som booker er lagret i programmet som lastes opp til hver enkelt sin ESP-kontroll


*/


/*
skal ha en "run"-funskjon som kjører menyen. skjermen skal oppdateres når den får en input. skal printe alle valgene, og highlighte et valg. 
valg:
booking:
    -kjøkken
        -komfyr
        -hele rommet
    -bad
    -stue
    -vaskemaskin
innsjekking av gjest.
styre lys, temperatur etc. 
booke komfyr og dusj osv.

når man velger en option så skal man sendes til en ny meny.
*/
//void draw_menu(Option arr[], int length, TFT_eSPI tft);