#ifndef ROV_h
#define ROV_h
#include "Arduino.h"
#include "ESCController.h"

class ROV
{
    public:
        ROV();
        ROV(String _rov, int _pin[], bool _direction[8]); 
        drive(int _roll, int _pitch, int _yaw, int _throttle);

        
    private:
        ESCController *thruster[8];
        ROV6();
        ROV8();
        String rov;
        int roll_rov, pitch_rov, yaw_rov, throttle_rov;
        bool *direction[];
        roll();
        pitch();
        yaw();
        throttle();
     

};

#endif
