#include <Button.h>

bool Button::pressed(){
    if(cur_val != prev_val && cur_val == 1){
        return true;
    }
    else{
        return false;
    }
}

void Button::setup(){
    pinMode(but_pin, INPUT);
}

void Button::update_cur_val(){
    cur_val = digitalRead(but_pin);
}

void Button::update_prev_val(){
    prev_val = cur_val;
}

