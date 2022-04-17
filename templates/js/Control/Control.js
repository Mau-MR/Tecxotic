//Module in charge of handling the functionality of the controller and the iteractions
import {FPS_controller} from "../Constants.js";
import {getGamepadState} from "./Gamepad.js";
import {PS4Controller} from "./types/PS4Controller.js";
import {ControlFunctionality} from "./Functionality.js";
//Iterates every fpsController to update controller state
setInterval(ControllerLoop, FPS_controller);
export const controller = new PS4Controller()

function ControllerLoop(){
    try{
        const {movedJoystick, pressedButtons} = getGamepadState()
        controller.UpdateControllerJoystick(movedJoystick)
        controller.UpdateControllerButton(pressedButtons)
        ControlFunctionality()
        controller.ResetPressedButtons()
    }catch (e){
        console.log(e)
    }
}
