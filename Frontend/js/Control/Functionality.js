import {commands_instance} from "../Connection/Message.js";
import {controller} from "./Control.js";
import {webRequest} from '../Connection/Requests.js'

let RANGE=1000, NEUTRAL = 0
let THROTTLE_RANGE=500, NEUTRAL_THROTTLE = 500

let pixhawk_on = false, pixhawk_pressed = false;
let arm_disarm_on, arm_disarm_pressed;

let arm_disarm_status = document.getElementById("arm_disarm_status")
arm_disarm_status.style.color= "#FF0000"

const calculatePotency = (joystick) =>{
   return parseInt((joystick * RANGE) + NEUTRAL)
}
//EventListener to detect pressed keys to control tools
document.addEventListener('keypress', async (event) => {
    var name = event.key;

    //                0   1   2   3   4
    const letters = ['y','u','i','o','p',
    //                5   6   7   8   9
                     'h','j','k','l',';'] 
    // letters is a hashmap that return the index of the element pressed if is in the list
    // these numbers can be then programmed to perfom different actions (these actions need to be programmed in back/arduino)
    let number = letters.indexOf(name)
    let body = {
        actions: number
    }
    let url= 'http://192.168.2.2:8000'
    if (number >= 0) {
        let response =await webRequest('POST',url,body)
        // console.log('Response from flask server', response)
    }
  }, false);

let powerLimit = document.getElementById("powerLimitSlider").value // Get the value from slider
document.getElementById('powerLimitSlider_value').innerHTML = powerLimit; // Put the value in screen 
powerLimit /= 100 

function JoystickFunctionality(){

    let safeZone = 0.1;
    let {lx, ly, rx, ry} = controller.joystick

    lx *= powerLimit
    ly *= powerLimit

    rx *= powerLimit
    ry *= powerLimit

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
        arm_disarm_status.style.color = "#00FF00"
        commands_instance.arm_disarm = true
    }else{
        commands_instance.arm_disarm = false
        arm_disarm_status.style.color = "#FF0000"
    }
}



export function ControlFunctionality(){
    JoystickFunctionality()
    PixhawkFunctionality()
}