// Struct for the management of the actuators
struct Actuator{
    int rightMovementPin;
    int leftMovementPin;
    int timePerAction;
    Actuator(int left, int right, int miliseconds){
        pinMode(left, OUTPUT);
        pinMode(right, OUTPUT);
        rightMovementPin = left;
        leftMovementPin = right;
        //Setting the value to read 0 on first try
        timePerAction = miliseconds;
    }
    Actuator* stop(){
        delay(timePerAction);
        digitalWrite(rightMovementPin, LOW);
        digitalWrite(leftMovementPin, LOW);
        return this;
    }
    Actuator* rightRotation(){
        digitalWrite(rightMovementPin, LOW);
        digitalWrite(leftMovementPin, HIGH);
        return this;
    }
    Actuator* leftRotation(){
        digitalWrite(rightMovementPin, HIGH);
        digitalWrite(leftMovementPin, LOW);
        return this;
    }
};

Actuator *fishGripper; //The motor that open/close The downside gripper that grabs the fish
Actuator *pinMotor; //The motor that moves the pinmotor
Actuator * rotationMotor; //The motor that ratates the ratationalGripper
Actuator * rotationalGripper; // The motor that open/close the ratationalGripper
Actuator * flexGripper; //The motor that open/close the multiporpuse gripper

void setup() {
    Serial.begin(115200);
    Serial.setTimeout(1);
    fishGripper = new Actuator(6, 7, 100);
    pinMotor = new Actuator(8,9, 0);
    rotationMotor = new Actuator(4,5, 0);
    rotationalGripper = new Actuator(2,3,0);
    flexGripper = new Actuator(10,11,0);
}

int command;
//Commands for moving the fish gripper
const int OPEN_GRIPPER = 1;
const int CLOSE_GRIPPER = 2;
//commands for moving the pin motor
const int RUN_PIN_MOTOR = 3;
const int STOP_PIN_MOTOR = 4;
//commands for moving the flexible gripper
const int OPEN_FLEX_GRIPPER = 5;
const int CLOSE_FLEX_GRIPPER = 6;
//commands for moving the rotational gripper
const int LEFT_FLIP = 7;
const int RIGHT_FLIP = 8;
const int OPEN_ROTATIONAL_GRIPPER = 9;
const int CLOSE_ROTATIONAL_GRIPPER = 10;

void loop() {
    while (!Serial.available());
    command = Serial.readString().toInt();
    switch(command){
        case OPEN_GRIPPER:
            fishGripper->rightRotation()->stop();
            break;
        case CLOSE_GRIPPER:
            fishGripper->leftRotation(); //This keeps sending the signal to hold the fish
            break;
        case RUN_PIN_MOTOR:
            pinMotor->rightRotation();
            break;
        case STOP_PIN_MOTOR:
            pinMotor->stop();
            break;
        case OPEN_FLEX_GRIPPER:
            flexGripper->rightRotation();
            break;
        case CLOSE_FLEX_GRIPPER:
            flexGripper->leftRotation();
            break;
        case LEFT_FLIP:
            rotationMotor->leftRotation();
            break;
        case RIGHT_FLIP:
            rotationMotor->rightRotation();
            break;
        case OPEN_ROTATIONAL_GRIPPER:
            rotationalGripper->rightRotation();
            break;
        case CLOSE_ROTATIONAL_GRIPPER:
            rotationalGripper->leftRotation();
            break;
    }
}