import {commands_instance} from "./Message.js";
import {socket_address} from "../Constants.js";

const wsAddress = "ws://" + socket_address;
var web_socket

let instantiateWebSocket = async () => {
    console.log("Websocket trying to connect to: " + socket_address)
    // since flask-socket-io runs on http, we directly connect to this ws endpoint since this build-in client doestn allo to connect to http
    web_socket = await new WebSocket(wsAddress)
    webSocketConnection(web_socket)
}
instantiateWebSocket()


let rov_status = document.getElementById("rov_status");
let pixhawk_status = document.getElementById("pixhawk_status");

rov_status.addEventListener("click", async () => {
    await instantiateWebSocket()
});

const mode_status = document.getElementById("mode_status")
mode_status.style.color = "#e5ee78"
const setupMode = (mode) =>{
    if(mode === 'MANUAL')
        mode_status.style.color = "#525e78"
    if(mode === 'STABILIZE')
        mode_status.style.color = "#e5ee78"
    if(mode === 'ACRO')
        mode_status.style.color = "#321123"
}
const arm_disarm_status = document.getElementById("arm_disarm_status")
arm_disarm_status.style.color= "#FF0000"
let isArmed = (status) => {
    if(status){
        arm_disarm_status.style.color = "#00FF00";
        return
    }
    arm_disarm_status.style.color = "#FF0000"
}
var received_message_from_ROV
let webSocketConnection = (web_socket) => {
    web_socket.onopen = () => {
        console.log("Connection stablished...")
        web_socket.send(JSON.stringify(commands_instance));
        rov_status.style.color = "#00FF00"
    };

    var attitude = $.flightIndicator('#attitudeNavigation', 'attitude', {size: 400, roll: 0, pitch: 0, showBox: true});
    const radiansToDegrees = (radian) => {
        return radian * (180 / Math.PI);
    }
    web_socket.onmessage = (event) => {
        if (event.data instanceof Blob) {
            const reader = new FileReader();
            reader.onload = () => {
                received_message_from_ROV = JSON.parse(reader.result)
                try {
                    const {roll, pitch} = received_message_from_ROV.imu
                    attitude.setRoll(radiansToDegrees(roll)); // Sets the roll to 30 degrees
                    attitude.setPitch(radiansToDegrees(pitch))
                    const {is_armed, mode} = received_message_from_ROV.pix_info
                    isArmed(is_armed);
                    setupMode(mode)
                } catch (error) {
                }
            };
            reader.readAsText(event.data);
        }
        web_socket.send(JSON.stringify(commands_instance))
    }
    web_socket.onclose = () => {
        rov_status.style.color = "#FF0000"
    };
    web_socket.onerror = (error) => {
        alert(`[error] ${error.message}`);
    };
    rov_status.style.color = "#FF0000"
}

