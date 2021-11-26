#ifndef ESCController_h
#define ESCController_h
#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

class ESCController
{
    public:
        ESCController();
        /*
         * direction == false -> CCW
         * direction == true  -> CW
         */
        ESCController(byte _esc_pin, bool _direction); 
        void run();
        void setSpeed(int _speed);
        void setSpeed(int _speed, bool _direction);
        int getSpeed();
        bool getDirection();
    private:
        byte esc_pin; // 9  ex
        int pwm_val;
        bool direction;
        Adafruit_PWMServoDriver esc_thruster;

};

#endif
