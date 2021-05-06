#include <Arduino.h>
#include <TFT_eSPI.h>
#include <CircusESP32Lib.h>
#pragma once

class Option{
    protected:
        String n; 
        uint16_t textcolor;
        uint16_t textbgcolor;
        //int action; // Dersom man trykker på valget -> videre til en annen meny
        
    public:
        Option(String name, uint16_t color = TFT_WHITE, uint16_t bgcolor = TFT_BLACK); // konstruktør
        virtual void set_color(uint16_t color, uint16_t bgcolor) = 0; // setter fargen på valget (selected == true -> txt-black & bg-white, else -> txt-white & bg-black)
        virtual void draw(TFT_eSPI tft) = 0; //skal tegne valget på skjermen
        virtual void action(int& menu_value) = 0;
        //int selected(); // dersom man trykker på valget --> videre til neste meny
}; 

class Menu_option : public Option{ // dette valget vil sende deg videre til en annen meny dersom man velger det (eks: trykk på Menu_option -> videre til meny 2)
    private:
        int linked_menu; // beskriver hvilken meny man skal sendes til dersom man trykker på valget
    public:
        Menu_option(String name, int link, uint16_t color = TFT_WHITE, uint16_t bgcolor = TFT_BLACK);
        void set_color(uint16_t color, uint16_t bgcolor);
        void draw(TFT_eSPI tft);
        void action(int& menu_value); // dersom valget trykkes på så endres menu_value (verdien som angir hvilken meny som vises) til linked_menu
        //int get_link(); // returnerer 'linked_menu' variabelen
};

class Time_option : public Option{
    private:
        int hour;
        int minute;
        int selected = 0; // går fra 0-2, (0 => ikke valgt, 1 => 'hour' valgt, 2 => 'minute' valgt)

        uint16_t hour_color = textcolor;
        uint16_t hour_bgcolor = textbgcolor;
        uint16_t minute_color = textcolor;
        uint16_t minute_bgcolor = textbgcolor;
        
    public:
        
        Time_option(String name, uint16_t color = TFT_WHITE, uint16_t bgcolor = TFT_BLACK);
        void draw(TFT_eSPI tft);
        void set_color(uint16_t color, uint16_t bgcolor);
        void action(int& menu_value);// override;
        void set_hour(int h);
        void set_minute(int m);
};

/*class Hour_option : public Option{
    private:
        int hour = 0;
    public:
        //int selected = 0; // går fra 0-2, (0 => ikke valgt, 1 => 'hour' valgt, 2 => 'minute' valgt)
        Hour_option(String name, uint16_t color = TFT_WHITE, uint16_t bgcolor = TFT_BLACK);
        void draw(TFT_eSPI tft);
        void set_color(uint16_t color, uint16_t bgcolor);
        void action(int& menu_value);// override;

};*/

class Duration_option : public Option{
    private:
        int duration = 0;
        bool selected = false;
        uint16_t dur_color = textcolor;
        uint16_t dur_bgcolor = textbgcolor;
    public:
        Duration_option(String name, uint16_t color = TFT_WHITE, uint16_t bgcolor = TFT_BLACK);
        void draw(TFT_eSPI tft);
        void set_color(uint16_t color, uint16_t bgcolor);
        void action(int& menu_value);// override;
        void set_duration(int dur);
};

class Signal_option : public Option{
    private:
        long signal;
        uint16_t dur_color = textcolor;
        uint16_t dur_bgcolor = textbgcolor;
    public:
        Signal_option(String name, uint16_t color = TFT_WHITE, uint16_t bgcolor = TFT_BLACK);
        void draw(TFT_eSPI tft);
        void set_color(uint16_t color, uint16_t bgcolor);
        void action(int& menu_value);// override;
        void set_signal(int resident_ID, int room_num, int starthour, int startminute, int duration);
        void print_message();
};

/*class Room_selection_option : public Option{
    private:
        int linked_menu; // beskriver hvilken meny man skal sendes til dersom man trykker på valget
        int selected_room; // beskriver hvilket rom man har valgt - viktig for å sende riktig signal til CoT
        String booking_header; // angir overskriften som skal vises på "neste" meny
    public:
        Room_selection_option(String name, int link, int room_num, String header, uint16_t color = TFT_WHITE, uint16_t bgcolor = TFT_BLACK);
        void set_color(uint16_t color, uint16_t bgcolor);
        void draw(TFT_eSPI tft);
        void action(int& menu_value);
};*/
