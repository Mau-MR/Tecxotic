import {commands_instance} from "./Message.js";

var connection_address
var address_input = document.getElementById("connection_address")
var web_socket 

let loadAddressConnection =  () => {
  try{
    web_socket.close()
    console.log("Connection closed...")
  }
  catch(error){
  }
  return fetch("./services/read_config.php")
  .then(response => response.json())
  .then(
    data => {
      connection_address = data["address"]
      console.log("Trying to connect to: "+connection_address)
      web_socket = new WebSocket("ws://"+connection_address)
      address_input.value = connection_address
      webSocketConnection(web_socket)
    }
  )
  .catch(error => console.log(error))
}
loadAddressConnection()


let saveAddressConnection =  (address) => {
  return fetch("./services/save_config.php?address="+address)
  .then(response => {response} )
  .then( data => {loadAddressConnection() })
  .catch(error => console.log(error))
  
}

let reconnect_button = document.getElementById("reconnectButton")
reconnect_button.addEventListener("click", () => {
  saveAddressConnection(address_input.value)
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





