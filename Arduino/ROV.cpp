#include "Arduino.h"
#include "ROV.h"

ROV::ROV(String _rov, int _pin[], bool _direction[]){
    rov = _rov;
    direction = _direction;
    //for(int x : enumerate(_pin)){
    //    thruster[x.index] = new ESCController(_pin[x.index],_direction[x.index]);
    //}

}
ROV::drive(int _roll, int _pitch, int _yaw, int _throttle){
    roll_rov = _roll;
    pitch_rov = _pitch;
    yaw_rov = _yaw;
    throttle_rov = _throttle;

    if(rov == "ROV6"){
        ROV6();
    }
    else if (rov == "ROV8"){
        ROV8();
    }
}

ROV::ROV6(){
    roll();
    pitch();
    yaw();
    throttle();
}
ROV::ROV8(){
    roll();
    pitch();
    yaw();
    throttle();
}



ROV::roll(){
    thruster[0]->setSpeed(roll_rov, direction[0]);
    thruster[0]->run();
    thruster[1]->setSpeed(roll_rov, !direction[1]);
    thruster[1]->run();

    thruster[2]->setSpeed(roll_rov, direction[2]);
    thruster[2]->run();
    thruster[3]->setSpeed(roll_rov, !direction[3]);
    thruster[3]->run();

}
ROV::pitch(){
    thruster[0]->setSpeed(pitch_rov, direction[0]);
    thruster[0]->run();
    thruster[1]->setSpeed(pitch_rov, direction[1]);
    thruster[1]->run();
    
    thruster[2]->setSpeed(pitch_rov, direction[2]);
    thruster[2]->run();
    thruster[3]->setSpeed(pitch_rov, direction[3]);
    thruster[4]->run();
}

ROV::yaw(){
    thruster[0]->setSpeed(yaw_rov, !direction[0]);
    thruster[0]->run();
    thruster[1]->setSpeed(yaw_rov, direction[1]);
    thruster[1]->run();
    
    thruster[2]->setSpeed(yaw_rov, !direction[2]);
    thruster[2]->run();
    thruster[3]->setSpeed(yaw_rov, direction[3]);
    thruster[3]->run();
}

ROV::throttle(){
    if(rov=="ROV6"){
        thruster[4]->setSpeed(throttle_rov, direction[4]);
        thruster[4]->run();
        thruster[5]->setSpeed(throttle_rov, direction[5]);
        thruster[5]->run();
    }
    else if(rov == "ROV8"){
        thruster[4]->setSpeed(throttle_rov, direction[4]);
        thruster[4]->run();
        thruster[5]->setSpeed(throttle_rov, direction[5]);
        thruster[5]->run();
        thruster[6]->setSpeed(throttle_rov, direction[6]);
        thruster[6]->run();
        thruster[7]->setSpeed(throttle_rov, direction[7]);
        thruster[8]->run();
    }
   
}
