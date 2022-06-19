import {commands_instance} from "../Connection/Message.js";
import {controller} from "./Control.js";
import {webRequest} from '../Connection/Requests.js'
import{flask_address} from "../Constants.js";

let RANGE=1000, NEUTRAL = 0
let THROTTLE_RANGE=500, NEUTRAL_THROTTLE = 500


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
    if (number >= 0) {
        let response =await webRequest('POST',flask_address+'/actuators',body)
        // console.log('Response from flask server', response)
    }
  }, false);

let limitSlider = document.getElementById("powerLimitSlider")
let powerTag = document.getElementById('powerLimitSlider_value');

function JoystickFunctionality(){

    let safeZone = 0.1;
    let {lx, ly, rx, ry} = controller.joystick
    let powerLimit = limitSlider.value;
    powerTag.innerHTML = powerLimit
    powerLimit /= 100

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

let prevOptions = false;
function PixhawkFunctionality(){
    const {options} = controller.buttons
    if(options && !prevOptions)
        commands_instance.arm_disarm = !commands_instance.arm_disarm
    prevOptions = options
}
let prevShare = false;
export function ModeFunctionality(){
   const {share} = controller.buttons
    if(share && !prevShare)
        commands_instance.mode = (commands_instance.mode === 'MANUAL')? 'STABILIZED': 'MANUAL'
    prevShare = share
}

export function ControlFunctionality(){
    JoystickFunctionality()
    PixhawkFunctionality()
    ModeFunctionality()
}