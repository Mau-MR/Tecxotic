import {commands_instance} from "./Message.js";
import {socket_address} from "../Constants.js";

var address_input = document.getElementById("connection_address")
var web_socket 

let instantiateWebSocket =  async () => {
    console.log("Websocket trying to connect to: " + socket_address)
    // since flask-socket-io runs on http, we directly connect to this ws endpoint since this build-in client doestn allo to connect to http
    web_socket = await new WebSocket("ws://" + socket_address)
    address_input.value = socket_address
    webSocketConnection(web_socket)
}
instantiateWebSocket()

//TODO HANDLE RECONECTION WITH THE BUTTON
let reconnect_button = document.getElementById("reconnectButton")
reconnect_button.addEventListener("click", () => {
  instantiateWebSocket(address_input.value)
});


let rov_status = document.getElementById("rov_status");
let pixhawk_status = document.getElementById("pixhawk_status");

var received_message_from_ROV
let webSocketConnection = (web_socket) => {
  web_socket.onopen = () => {
    console.log("Connection stablished...")
    web_socket.send(JSON.stringify(commands_instance));
    rov_status.style.backgroundColor = "#00FF00"
  }; 

  web_socket.onmessage = (event) => {
    if (event.data instanceof Blob) {
      const reader = new FileReader();
      reader.onload = () => {
          received_message_from_ROV = JSON.parse(reader.result)
          try{
            pixhawkStatus(received_message_from_ROV["connection_pixhawk"])
            // console.log(received_message_from_ROV)  //PRINTS RECEIVED MESSAGES
          }
          catch(error){
          }
      };
      reader.readAsText(event.data);
    }
    web_socket.send(JSON.stringify(commands_instance))
  }
  web_socket.onclose = () => {
    rov_status.style.backgroundColor = "#FF0000"
  };
  web_socket.onerror = (error) => {
    alert(`[error] ${error.message}`);
  };
  rov_status.style.backgroundColor = "#FF0000"
}

let pixhawkStatus = (status) => {
  if(status){
    pixhawk_status.style.backgroundColor = "#00FF00"
  }
  else{
    pixhawk_status.style.backgroundColor = "#FF0000"
  }
}
pixhawk_status.style.backgroundColor = "#FF0000"





