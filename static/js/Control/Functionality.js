import {commands_instance} from "../Connection/Message.js";
import {controller} from "./Control.js";

let RANGE=1000, NEUTRAL = 0
let THROTTLE_RANGE=500, NEUTRAL_THROTTLE = 500

let pixhawk_on = false, pixhawk_pressed = false;
let arm_disarm_on, arm_disarm_pressed;

let arm_disarm_status = document.getElementById("arm_disarm_status")
arm_disarm_status.style.backgroundColor = "#FF0000"

const calculatePotency = (joystick) =>{
   return parseInt((joystick * RANGE) + NEUTRAL)
}

function JoystickFunctionality(){
    // commands_instance.connect_pixhawk = connect_pixhawk_instruction.UpdateToggle(PS4Controller.share)
    // commands_instance.arm_disarm = arm_disarm_instruction.UpdateToggle(PS4Controller.options)

    //############################################ROLL PITCH YAW THROTTLE MOVEMENT#####################################
    //prevents the movement of the joystick
    let safeZone = 0.1;
    const {lx, ly, rx, ry} = controller.joystick

    //Populating the message that is going to be sended to the back if the joystick was moved
    if(ly > safeZone || ly < -safeZone){
        commands_instance.throttle = parseInt((-ly * THROTTLE_RANGE) + NEUTRAL_THROTTLE)
    }
    else{
        commands_instance.throttle = NEUTRAL_THROTTLE;
    }
    commands_instance.roll = (lx > safeZone || lx < -safeZone) ? calculatePotency(lx) : NEUTRAL
    commands_instance.pitch = ( ry > safeZone || ry < -safeZone) ? calculatePotency(-ry) : NEUTRAL
    commands_instance.yaw = ( rx > safeZone || rx < -safeZone) ? calculatePotency(rx) : NEUTRAL
}

function PixhawkFunctionality(){

    const {share, options} = controller.buttons

    //##################################### PIXHAWK CONNECT AND DISCONNECT ####################################
    if(share){
        if(!pixhawk_pressed){
            pixhawk_on = !pixhawk_on;
            pixhawk_pressed = true;
        }
    }else{
        pixhawk_pressed = false;
    }
    commands_instance.connect_pixhawk = pixhawk_on;
    //##################################### ARM AND DISARM MOTORS ####################################

    if(options){
        if(!arm_disarm_pressed){
            arm_disarm_on = !arm_disarm_on;
            arm_disarm_pressed = true;
        }
    }else{
        arm_disarm_pressed = false;
    }
    if(arm_disarm_on){
        arm_disarm_status.style.backgroundColor = "#00FF00"
        commands_instance.arm_disarm = true
    }else{
        commands_instance.arm_disarm = false
        arm_disarm_status.style.backgroundColor = "#FF0000"
    }
}


function OpenGripper(){
    const {cross} = controller.buttons
    if(cross)
        commands_instance.openGripper = true
    else
        commands_instance.openGripper = false
}
function CloseGripper(){
    const {circle} = controller.buttons
    if(circle)
        commands_instance.closeGripper = true
    else
        commands_instance.closeGripper = false
}

export function ControlFunctionality(){
    JoystickFunctionality()
    PixhawkFunctionality()
    OpenGripper()
    CloseGripper()
}