#include "ROV.h"
ROV *rov;
void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(33);
  int pins[8] = {1,2,3,4,5,6,7,8};
  bool directions[] = {0,0,1,1,0,1};
  rov = new ROV("ROV8",pins,directions);

}

void loop()
{
  if ( Serial.available()) {
    char *str[10];
    int counter = 0;
    String serialResponse = Serial.readStringUntil('\n');
    char buf[256];
    serialResponse.toCharArray(buf, sizeof(buf));
    char *p = buf;
    while ((str[counter] = strtok_r(p, " ", &p)) != NULL){
      //Serial.println(str[counter]);
      counter++;
    }

    int roll = atoi(str[1]);
    int pitch = atoi(str[2]);
    int yaw = atoi(str[3]);
    int throttle = atoi(str[4]);
    rov->drive(roll, pitch, yaw, throttle);

   
    //Serial.print(String(roll)+" "+String(pitch)+" "+String(yaw)+" "+String(throttle)+"\n");
    //Serial.print(thruster->getSpeed());
  }
}
