
class ControllerValues{
    constructor(){
        this.throttle = 500
        this.roll = 0
        this.pitch = 0
        this.yaw = 0
        this.arm_disarm = true
        // this.mode = 'STABILIZE'
        this.mode = 'MANUAL'

    }
}
export const commands_instance = new ControllerValues();


