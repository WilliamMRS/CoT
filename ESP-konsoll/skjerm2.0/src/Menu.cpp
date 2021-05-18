#include <Menu.h>

/*void Menu::draw_menu(TFT_eSPI tft){//, int cursor){ // tegner menyen til skjermen
    tft.println(header);
    tft.println("");
} */

void Main_menu::draw_menu(TFT_eSPI tft){//, int cursor){ // tegner menyen til skjermen
    tft.println(header); // tegner overskrift

    for(auto option : options){ // setter default farge til alle valg
        option->set_color(TFT_WHITE, TFT_BLACK);
    }
    options[prev_cursor]->set_color(TFT_WHITE, TFT_BLACK);
    options[cursor]->set_color(TFT_BLACK, TFT_WHITE); // setter invers farge på valgt valg

    for(auto option : options){ // tegner options
        option->draw(tft);
        tft.println("");
    }
    prev_cursor = cursor; 
} 

void Booking_menu::draw_menu(TFT_eSPI tft){//, int cursor){ // tegner menyen til skjermen
    tft.println(header); // tegner overskrift

    for(auto option : options){ // setter default farge til alle valg
        option->set_color(TFT_WHITE, TFT_BLACK);
    }

    options[prev_cursor]->set_color(TFT_WHITE, TFT_BLACK);
    options[cursor]->set_color(TFT_BLACK, TFT_WHITE); // setter invers farge på valgt valg
    
    for(auto option : options){ // tegner options
        option->draw(tft);
        tft.println("");
    }
    prev_cursor = cursor;
} 

void Main_menu::increment_cursor(){
    if(cursor < sizeof(options)/sizeof(options[0]) - 1){
        cursor += 1;
    }
    else{
        cursor = 0;
    }
    
}

void Booking_menu::increment_cursor(){
    if(cursor < sizeof(options)/sizeof(options[0]) - 1){
        cursor += 1;
    }
    else{
        cursor = 0;
    }

}

void Main_menu::select_option(int& menu_value){
    //int link = options[cursor].get_link();
    options[cursor]->action(menu_value);
}

void Booking_menu::select_option(int& menu_value){
    //int link = options[cursor].get_link();
    options[cursor]->action(menu_value);
}

void Room_booking_menu::draw_menu(TFT_eSPI tft){
    tft.println(header); // tegner overskrift

    for(auto option : options){ // setter default farge til alle valg
        option->set_color(TFT_WHITE, TFT_BLACK);
    }

    options[prev_cursor]->set_color(TFT_WHITE, TFT_BLACK);
    options[cursor]->set_color(TFT_BLACK, TFT_WHITE); // setter invers farge på valgt valg
    if(time_selected != 0 || dur_selected){
        options[cursor]->set_color(TFT_WHITE, TFT_BLACK);
    }
   
    for(auto option : options){ // tegner options
        option->draw(tft);
        tft.println();
    }
    prev_cursor = cursor;
}

void Room_booking_menu::increment_cursor(){
    if(time_selected == 1){
        if(start_hour < 23){
            start_hour ++;
        }
        else{
            start_hour = 0;
        }
        
        time_opt.set_hour(start_hour);
    }
    else if(time_selected == 2){
        if(start_minute < 55){
            start_minute += 5;
        }
        else{
            start_minute = 0;
        }
        time_opt.set_minute(start_minute);
    }
    else if(dur_selected){
        if(duration < 120){
            duration += 5;
        }
        else{
            duration = 0;
        }
        
        dur_opt.set_duration(duration);
    }
    else{
        if(cursor < sizeof(options)/sizeof(options[0]) - 1){
            cursor += 1;
        }
        else{
            cursor = 0;
        }
    }

}

void Room_booking_menu::select_option(int& menu_value){
    //int link = options[cursor].get_link();
    if(cursor == 0){
        if(time_selected < 2){
            time_selected++;
        }
        else{
            time_selected = 0;
        }
    }
    else if(cursor == 1){
        dur_selected = !dur_selected;
    }
    else if(cursor == 2){
        signal_opt.set_signal(resident, selected_room, start_hour, start_minute, duration);
        start_hour = 0;
        start_minute = 0;
        duration = 0;
        time_opt.set_hour(start_hour);
        time_opt.set_minute(start_minute);
        dur_opt.set_duration(duration);
        //signal_opt.send_signal(CircusESP32Lib circusESP32, key, token);
    }

    options[cursor]->action(menu_value);
}


