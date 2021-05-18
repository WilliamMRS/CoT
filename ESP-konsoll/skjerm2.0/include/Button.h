#include <Arduino.h>

class Button{
    private:
        int prev_val = 0;
        int cur_val = 0;
        int but_pin;
    public:
        Button(int pin): but_pin{pin}{} // konstruktør
        bool pressed();
        void setup();
        void update_cur_val();
        void update_prev_val();

};

