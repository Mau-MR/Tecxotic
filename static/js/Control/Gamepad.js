let controller_status = document.getElementById("controller_status")

/**
 * Maps the connected control and retrieves the position of the joysticks and the pressed buttons
 * @returns {{movedJoystick: (*|ReadonlyArray<number>|[]), pressedButtons}}
 */
export function getGamepadState() {
    const gamepads = navigator.getGamepads();
    const gamepad = gamepads[0];

    if (!gamepad) {
        controller_status.style.backgroundColor = "#FF0000"
        throw("Not gamepad")
    }
    controller_status.style.backgroundColor = "#00FF00"
    const pressedButtons = gamepad.buttons.map((button, id) => ({id, button})).filter(isPressed);
    const movedJoystick = gamepad.axes

    return {movedJoystick, pressedButtons}
}

/**
 * checks whether if the gamepad button has been pressed
 * @param pressed
 * @returns {boolean}
 */
function isPressed({button: {pressed}}) {
    return !!pressed;
}


/*
class ToggleButton{
    constructor(){
        this.toggleOn = false
        this.togglePressed = false
    }
    UpdateToggle(button)
    {
        if(button){
            if(!(this.togglePressed)){
                this.toggleOn = !(this.toggleOn);
                this.togglePressed = true;
            }
        }else{
            this.togglePressed = false;
        }
        if(this.toggleOn){
            return true
        }else{
            return false
        }
    }
}
const connect_pixhawk_instruction = new ToggleButton()
const arm_disarm_instruction = new ToggleButton()

*/
