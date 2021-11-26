#include "Arduino.h"
#include "ESCController.h"

ESCController::ESCController(byte _esc_pin, bool _direction)
{
    esc_thruster = Adafruit_PWMServoDriver(0x40);
    esc_thruster.begin();
    esc_pin = _esc_pin;
    direction = _direction;
    esc_thruster.setPWMFreq(50);
    esc_thruster.writeMicroseconds(esc_pin,1500);
    delay(400); // delay to allow the ESC to recognize the stopped signal.
    //Serial.setTimeout(33);

}
void ESCController::setSpeed(int _speed, bool _direction)
{
    if (_direction){
      pwm_val = map(_speed, 1050, 1950, 1050, 1950);
    }
    else if (!_direction){
      pwm_val = map(_speed, 1050, 1950, 1950, 1050);
    }
}
void ESCController::setSpeed(int _speed)
{
    if (direction){
      pwm_val = map(_speed, 1050, 1950, 1050, 1950);
    }
    else if (!direction){
      pwm_val = map(_speed, 1050, 1950, 1950, 1050);
    }
}
int ESCController::getSpeed(){
  //Serial.println(pwm_val);
  return pwm_val;
}
bool ESCController::getDirection(){
  return direction;
}

void ESCController::run()
{
    esc_thruster.writeMicroseconds(esc_pin,pwm_val);

}
