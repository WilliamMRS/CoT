#include <Option.h>

Option::Option(String name, uint16_t color, uint16_t bgcolor): n{name}, textcolor{color}, textbgcolor{bgcolor}{}
Menu_option::Menu_option(String name, int link, uint16_t color, uint16_t bgcolor) : Option(name, color, bgcolor), linked_menu{link}{}
Time_option::Time_option(String name, uint16_t color, uint16_t bgcolor) : Option(name, color, bgcolor){}
//Hour_option::Hour_option(String name, uint16_t color, uint16_t bgcolor) : Option(name, color, bgcolor){}
Duration_option::Duration_option(String name, uint16_t color, uint16_t bgcolor) : Option(name, color, bgcolor){}
//Room_selection_option::Room_selection_option(String name, int link, int room_num, String header, uint16_t color, uint16_t bgcolor) : Option(name, color, bgcolor), linked_menu{link}, selected_room{room_num}, booking_header{header}{}
Signal_option::Signal_option(String name, uint16_t color, uint16_t bgcolor) : Option(name, color, bgcolor){}

void Menu_option::set_color(uint16_t color, uint16_t bgcolor){ // setter fargen på valget
    textcolor = color;
    textbgcolor = bgcolor;
}

void Menu_option::draw(TFT_eSPI tft){ // tegner valget på skjermen
    tft.setTextColor(textcolor, textbgcolor);
    tft.println(n);
}

void Menu_option::action(int& menu_value){
    menu_value = linked_menu;
} 

void Time_option::draw(TFT_eSPI tft){
    String h;
    String m;
    if(hour < 10){
        h = "0" + static_cast<String>(hour);
    }
    else{
        h = static_cast<String>(hour);
    }
    if(minute < 10){
        m = "0" + static_cast<String>(minute);
    }
    else{
        m = static_cast<String>(minute);
    }

    tft.setTextColor(textcolor, textbgcolor);
    tft.print(n);
    tft.setTextColor(hour_color, hour_bgcolor);
    tft.print(h);
    tft.setTextColor(textcolor, textbgcolor);
    tft.print(":");
    tft.setTextColor(minute_color, minute_bgcolor);
    tft.print(m);
    tft.println();
    //tft.drawString(" " + h + ":" + m, 70, 105);
    //tft.print(" " + h + ":" + m);
    /*tft.print(hour);
    tft.print(minute);*/
}

void Time_option::set_color(uint16_t color, uint16_t bgcolor){ // setter fargen på valget
    textcolor = color;
    textbgcolor = bgcolor;
    if(selected == 0){
        hour_color = color;
        hour_bgcolor = bgcolor;
        minute_color = color;
        minute_bgcolor = bgcolor;
    }
    else if(selected == 1){
        hour_color = TFT_BLACK;
        hour_bgcolor = TFT_WHITE;
        minute_color = TFT_WHITE;
        minute_bgcolor = TFT_BLACK;
    }
    else if(selected == 2){
        hour_color = TFT_WHITE;
        hour_bgcolor = TFT_BLACK;
        minute_color = TFT_BLACK;
        minute_bgcolor = TFT_WHITE;
    }

}

void Time_option::action(int& menu_value){
    if(selected < 2){
        selected++;
    }
    else{
        selected = 0;
    }


    //this->set_color(TFT_WHITE, TFT_BLACK);
}

void Time_option::set_hour(int h){
    hour = h;
}

void Time_option::set_minute(int m){
    minute = m;
}


/*void Hour_option::draw(TFT_eSPI tft){
    tft.setTextColor(textcolor, textbgcolor);
    String h;
    if(hour < 10){
        h = "0" + static_cast<String>(hour);
    }
    else{
        h = static_cast<String>(hour);
    }
    tft.print(h);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print(":");
}

void Hour_option::set_color(uint16_t color, uint16_t bgcolor){ // setter fargen på valget
    textcolor = color;
    textbgcolor = bgcolor;
}

void Hour_option::action(int& menu_value){

    //this->set_color(TFT_WHITE, TFT_BLACK);
}*/

void Duration_option::draw(TFT_eSPI tft){
    String dur;
    if(duration < 10){
        dur = "   0" + static_cast<String>(duration);
    }
    else if(duration < 100){
        dur = "   " + static_cast<String>(duration); // for riktig formatering på skjermen
    }
    else{
        dur = static_cast<String>(duration);
    }

    tft.setTextColor(textcolor, textbgcolor);
    tft.print(n);
    tft.setTextColor(dur_color, dur_bgcolor);
    tft.print(dur);
    tft.setTextColor(textcolor,textbgcolor);
    tft.print(" min");
    tft.println();
    //tft.drawString(" " + h + ":" + m, 70, 105);
    //tft.print(" " + h + ":" + m);
    /*tft.print(hour);
    tft.print(minute);*/
}

void Duration_option::set_color(uint16_t color, uint16_t bgcolor){ // setter fargen på valget
    textcolor = color;
    textbgcolor = bgcolor;
    if(selected){
        dur_color = TFT_BLACK;
        dur_bgcolor =TFT_WHITE;
    }
    else{
        dur_color = color;
        dur_bgcolor = bgcolor;
    }
}

void Duration_option::action(int& menu_value){
    selected = !selected;
}

void Duration_option::set_duration(int dur){
    duration = dur;
}


void Signal_option::set_color(uint16_t color, uint16_t bgcolor){ // setter fargen på valget
    textcolor = color;
    textbgcolor = bgcolor;
}

void Signal_option::draw(TFT_eSPI tft){ // tegner valget på skjermen
    tft.setTextColor(textcolor, textbgcolor);
    tft.println(n);
}

void Signal_option::print_message(){
    extern TFT_eSPI tft;
    tft.fillScreen(TFT_BLACK);
    tft.print("Booking request");
    tft.print("delivered.");
    delay(2000);
    tft.fillScreen(TFT_BLACK);
}

void Signal_option::action(int& menu_value){
    // kommet så langt - skal nå sende 'signal' til CoT. Da kan man booke rom, men ikke motta error!
    extern CircusESP32Lib circusESP32;
    extern char key;
    extern char token;
    circusESP32.write(&key, signal, &token);

    this->print_message();
} 

void Signal_option::set_signal(int resident_ID, int room_num, int starthour, int startminute, int duration){
    String start_h;
    String start_m;
    String dur;
    String id = static_cast<String>(resident_ID);
    String room = static_cast<String>(room_num);
    if(starthour < 10){
        start_h = "0" + static_cast<String>(starthour);
    }
    else{
        start_h = static_cast<String>(starthour);
    }

    if(startminute < 10){
        start_m = "0" + static_cast<String>(startminute);
    }
    else{
        start_m = static_cast<String>(startminute);
    }
    if(duration < 10){
        dur = "00" + static_cast<String>(duration);
    }
    else if(duration < 100){
        dur = "0" + static_cast<String>(duration);
    }
    else{
        dur = static_cast<String>(duration);
    }
    String booking_signal = id + room + start_h + start_m + dur;

    signal = booking_signal.toInt();
}


/*void Room_selection_option::set_color(uint16_t color, uint16_t bgcolor){ // setter fargen på valget
    textcolor = color;
    textbgcolor = bgcolor;
}

void Room_selection_option::draw(TFT_eSPI tft){ // tegner valget på skjermen
    tft.setTextColor(textcolor, textbgcolor);
    tft.println(n);
}

void Room_selection_option::action(int& menu_value){
    menu_value = linked_menu;
    //menus[menu_value] -> set_header(booking_header);
}*/




/*bool Option::select(){

}*/