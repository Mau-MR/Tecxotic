
class ControllerValues{
    constructor(){
        this.throttle = 500
        this.roll = 0
        this.pitch = 0
        this.yaw = 0
        this.connect_pixhawk = false
        this.arm_disarm = false
    }
}
export const commands_instance = new ControllerValues();


