export class PS4Controller{
    //IMPORTANT: format this json in the gamepad order
    //DO NOT CHANGE ORDER OF THIS JSON OR THE BUTTONS ARE GOING TO BE MISMATCHED
    buttons = {
        cross : false, //cross
        circle : false, //circle
        square : false, //square
        triangle : false, //triangle
        l1 : false, //L1
        r1 : false, //R1
        l2 : false, //L2
        r2 : false, //R2
        share : false, //share
        options : false, //options
        l3 : false, //L3
        r3 : false, //R3
        up_dpad : false, //up_dpad
        down_dpad : false, //down_dpad
        left_dpad : false, //left_dpad
        right_dpad : false, //right_dpad
        PS : false, //PS
        touchpad : false, //touchpad
    }
    buttonArrayName = Object.keys(this.buttons)

    joystick = {
        lx : 0.0, //Left X
        ly : 0.0, //Left Y
        rx : 0.0, //Right X
        ry : 0.0, //Right Y
    }

    /**
     * Updates the pressed buttons
     * @param pressedButtons [array] - the pressed buttons from the gamepad
     * @void
     */
    UpdateControllerButton(pressedButtons) {
        for (const button of pressedButtons) {
            const buttonPressed = this.buttonArrayName[button.id]
            //the actual change of the state of the button
            this.buttons[buttonPressed] = true;
        }
    }

    /**
     * returns the buttons to the normal state
     * @void
     */
    ResetPressedButtons(){
        this.buttonArrayName.map((name)=>{
            this.buttons[name] = false
        })
    }

    /**
     * Updates the position of the joystick
     * @param movedJoystick [array] the moved joysticks from the gamepad
     * @void
     */
    UpdateControllerJoystick(movedJoystick){
        const joystick = this.joystick
        joystick.lx = movedJoystick[0].toFixed(2);
        joystick.ly = movedJoystick[1].toFixed(2);

        joystick.rx= movedJoystick[2].toFixed(2);
        joystick.ry= movedJoystick[3].toFixed(2);
    }
}
