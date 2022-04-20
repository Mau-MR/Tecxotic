let address_camera1 = document.getElementById("address_camera1")
let address_camera2 = document.getElementById("address_camera2")
let address_camera3 = document.getElementById("address_camera3")
let address_camera4 = document.getElementById("address_camera4")

let view_main_camera = document.getElementById("view_main_camera")
let view_camera1 = document.getElementById("view_camera1")
let view_camera2 = document.getElementById("view_camera2")
let view_camera3 = document.getElementById("view_camera3")
let view_camera4 = document.getElementById("view_camera4")

let view_main_camera_context = view_main_camera.getContext('2d')
let view_camera1_context = view_camera1.getContext('2d')
let view_camera2_context = view_camera2.getContext('2d')
let view_camera3_context = view_camera3.getContext('2d')
let view_camera4_context = view_camera4.getContext('2d')

var view_main_camera_image = new Image();
view_main_camera_image.crossOrigin = "Anonymous"
var view_camera1_image = new Image();
view_camera1_image.crossOrigin = "Anonymous"
var view_camera2_image = new Image();
view_camera2_image.crossOrigin = "Anonymous"
var view_camera3_image = new Image();
view_camera3_image.crossOrigin = "Anonymous"
var view_camera4_image = new Image();
view_camera4_image.crossOrigin = "Anonymous"

view_main_camera_image.onload = () =>{
    setInterval(() => {try{view_main_camera_context.drawImage(view_main_camera_image, 0, 0)}catch(error){}
    if(agent1_button.getAttribute("class") == "btn btn-success"){
        refreshMarker(view_main_camera_context)
    }
}, FPS_video)
}
view_camera1_image.onload = () =>{
    setInterval(() => {try{view_camera1_context.drawImage(view_camera1_image, 0, 0)}catch(error){}}, FPS_video)
}
view_camera2_image.onload = () =>{
    setInterval(() => {try{view_camera2_context.drawImage(view_camera2_image, 0, 0)}catch(error){}}, FPS_video)
}
view_camera3_image.onload = () =>{
    setInterval(() => {try{view_camera3_context.drawImage(view_camera3_image, 0, 0)}catch(error){}}, FPS_video)
}
view_camera4_image.onload = () =>{
    setInterval(() => {try{view_camera4_context.drawImage(view_camera4_image, 0, 0)}catch(error){}}, FPS_video)
}
let loadCameraConnection = () => {
    return fetch("./services/read_config.php")
    .then(response => response.json())
    .then(
      data => {
            view_main_camera_image.src  = data["address_camera1"]
            view_camera1_image.src = data["address_camera1"]
            view_camera2_image.src = data["address_camera2"]
            view_camera3_image.src = data["address_camera3"]
            view_camera4_image.src = data["address_camera4"]

            address_camera1.value = data["address_camera1"]
            address_camera2.value = data["address_camera2"]
            address_camera3.value = data["address_camera3"]
            address_camera4.value = data["address_camera4"]
      }
    )
    .catch(error => console.log(error))
}
loadCameraConnection()
let saveCameraConnection = (address_camera1,address_camera2,address_camera3,address_camera4) => {
    return fetch("./services/save_config.php?address_camera1="+address_camera1+"&address_camera2="+address_camera2+"&address_camera3="+address_camera3+"&address_camera4="+address_camera4)
    .then(response => {} )
    .then( data => {loadCameraConnection() })
    .catch(error => console.log(error))

}
let reconnect_button = document.getElementById("reconnectButtonCam")
reconnect_button.addEventListener("click", () => {
    saveCameraConnection(address_camera1.value, address_camera2.value, address_camera3.value, address_camera4.value)
}
);
var camera_selector = 0
let cameras = {
    0 : view_camera1_image,
    1 : view_camera2_image,
    2 : view_camera3_image,
    3 : view_camera4_image,
}
let border_cameras = {
    0 : view_camera1,
    1 : view_camera2,
    2 : view_camera3,
    3 : view_camera4,
}
let putMainCameraView = (cam_sel) =>{
    view_main_camera_image.src = cameras[cam_sel].src
    for(var key in cameras) {
        if(key == cam_sel){
            border_cameras[cam_sel].style.borderColor = "#00FF00"
        }else{
            border_cameras[key].style.borderColor = "#000000"
        }
    }
}
putMainCameraView(0)
var left_camera_pressed,right_camera_pressed

