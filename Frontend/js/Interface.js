import {commands_instance} from "./Connection/Message.js";
import {FPS_controller} from "./Constants.js";
import {controller} from "./Control/Control.js";


//##################################################CAMERA CONFIGURATION#####################################################
//##################################################PID CONFIGURATION################################################
let pid = {
    0 : document.getElementById("roll_p"),
    1 : document.getElementById("roll_i"),
    2 : document.getElementById("roll_d"),
    3 : document.getElementById("pitch_p"),
    4 : document.getElementById("pitch_i"),
    5 : document.getElementById("pitch_d"),
    6 : document.getElementById("yaw_p"),
    7 : document.getElementById("yaw_i"),
    8 : document.getElementById("yaw_d"),
    9 : document.getElementById("throttle_p"),
    10 : document.getElementById("throttle_i"),
    11 : document.getElementById("throttle_d")
}
for (const [key, value] of Object.entries(pid)) {
    value.addEventListener("input", (event) => {
        updatePID(value.id, value.value)
    })
}

let updatePID = (key, value) =>{
    return fetch("./services/save_config.php?"+key+"="+value)
    .then(response => {} )
    .then( data => { 
        sendPIDToROV()
    })
    .catch(error => console.log(error))
}
let loadPID = () =>{
    return fetch("./services/read_config.php")
    .then(response => response.json())
    .then( data => {
        for (const [key, value] of Object.entries(pid)) {
            value.value = data[value.id]
            sendPIDToROV()
        }
    })
    .catch(error => console.log(error))
}
loadPID()

let sendPIDToROV = () =>{
    fetch("http://"+server_connection_on_ROV+"/TecXotic2022/services/updateRollPID.php?p="+pid[0].value+"&i="+pid[1].value+"&d="+pid[2].value)
    .then(response => {} )
    .then( data => {})
    .catch(error => console.log(error))
    fetch("http://"+server_connection_on_ROV+"/TecXotic2022/services/updatePitchPID.php?p="+pid[3].value+"&i="+pid[4].value+"&d="+pid[5].value)
    .then(response => {} )
    .then( data => {})
    .catch(error => console.log(error))
    fetch("http://"+server_connection_on_ROV+"/TecXotic2022/services/updateYawPID.php?p="+pid[6].value+"&i="+pid[7].value+"&d="+pid[8].value)
    .then(response => {} )
    .then( data => {})
    .catch(error => console.log(error))
    fetch("http://"+server_connection_on_ROV+"/TecXotic2022/services/updateThrottlePID.php?p="+pid[9].value+"&i="+pid[10].value+"&d="+pid[11].value)
    .then(response => {} )
    .then( data => {})
    .catch(error => console.log(error))
}
//##################################################OPENCV AGENT1 ADJUSTMENT#####################################
let AI1_button = document.getElementById("AI1_button")
let src_image_AI1 = document.getElementById("camera_IA1")
let result_image_AI1 = document.getElementById("result_IA1")
let AI1_modal = new bootstrap.Modal(document.getElementById('modalAI1'))

var interval_refresh
AI1_modal._element.addEventListener("hidden.bs.modal",()=>{
    clearInterval(interval_refresh)
})
var input_AI1_image = new Image();
var src_image_AI1_context = src_image_AI1.getContext('2d');
AI1_button.addEventListener("click", ()=>{
    loadFilterValues()
    input_AI1_image.crossOrigin = 'Anonymous';
    input_AI1_image.src = view_main_camera_image.src;
    input_AI1_image.onload = function(){
        interval_refresh = setInterval(imageProcessing, FPS_video  );
    }

});

let first_slider_low = document.getElementById("first_slider_low")
let first_slider_low_text = document.getElementById("first_slider_low_text")
let first_slider_high = document.getElementById("first_slider_high")
let first_slider_high_text = document.getElementById("first_slider_high_text")

let second_slider_low = document.getElementById("second_slider_low")
let second_slider_low_text = document.getElementById("second_slider_low_text")
let second_slider_high = document.getElementById("second_slider_high")
let second_slider_high_text = document.getElementById("second_slider_high_text")

let third_slider_low = document.getElementById("third_slider_low")
let third_slider_low_text = document.getElementById("third_slider_low_text")
let third_slider_high = document.getElementById("third_slider_high")
let third_slider_high_text = document.getElementById("third_slider_high_text")

let size_slider_min = document.getElementById("size_slider_min")
let size_slider_min_text = document.getElementById("size_slider_min_text")
let percentage_slider_min = document.getElementById("percentage_slider_min")
let percentage_slider_min_text = document.getElementById("percentage_slider_min_text")


var [first_value_low  , second_value_low  , third_value_low] = [0,0,0]
var [first_value_high , second_value_high , third_value_high] = [180,255,255]
var [size_value_min, size_value_max] = [0,30000]
var [percentage_value_min, percentage_value_max] = [0,100]

let sliderAI1Change = () => {
    first_slider_low_text.innerHTML = "H:"+first_slider_low.value
    first_slider_high_text.innerHTML = "H:"+first_slider_high.value
    second_slider_low_text.innerHTML = "S:"+second_slider_low.value
    second_slider_high_text.innerHTML = "S:"+second_slider_high.value
    third_slider_low_text.innerHTML = "V:"+third_slider_low.value
    third_slider_high_text.innerHTML = "V:"+third_slider_high.value
    size_slider_min_text.innerHTML = "S:"+size_slider_min.value
    size_slider_max_text.innerHTML = "S:"+size_slider_max.value
    percentage_slider_min_text.innerHTML = "P:"+percentage_slider_min.value
    percentage_slider_max_text.innerHTML = "P:"+percentage_slider_max.value

    first_value_low = parseInt(first_slider_low.value)
    first_value_high = parseInt(first_slider_high.value)
    second_value_low = parseInt(second_slider_low.value)
    second_value_high = parseInt(second_slider_high.value)
    third_value_low = parseInt(third_slider_low.value)
    third_value_high = parseInt(third_slider_high.value)
    size_value_min = parseInt(size_slider_min.value)
    size_value_max = parseInt(size_slider_max.value)
    percentage_value_min = parseInt(percentage_slider_min.value)
    percentage_value_max = parseInt(percentage_slider_max.value)

    updateFilterValues(first_value_low, first_value_high, second_value_low, second_value_high, third_value_low, third_value_high, size_value_min, size_value_max, percentage_value_min, percentage_value_max)
}

first_slider_low.addEventListener("input", sliderAI1Change)
first_slider_high.addEventListener("input", sliderAI1Change)
second_slider_low.addEventListener("input", sliderAI1Change)
second_slider_high.addEventListener("input", sliderAI1Change)
third_slider_low.addEventListener("input", sliderAI1Change)
third_slider_high.addEventListener("input", sliderAI1Change)
size_slider_min.addEventListener("input", sliderAI1Change)
size_slider_max.addEventListener("input", sliderAI1Change)
percentage_slider_min.addEventListener("input", sliderAI1Change)
percentage_slider_max.addEventListener("input", sliderAI1Change)

var src, dst, hsv
let imageProcessing = () => {
    src_image_AI1_context.drawImage(input_AI1_image, 0, 0);
    refreshMarker(src_image_AI1_context)
    src = cv.imread(input_AI1_image);
    hsv = new cv.Mat();
    cv.cvtColor(src, hsv, cv.COLOR_RGB2HSV);
    var lower_val = [first_value_low, second_value_low, third_value_low, 0]
    var upper_val = [first_value_high, second_value_high, third_value_high, 255]
    var low = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), lower_val);
    var high = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), upper_val);
    dst = new cv.Mat();
    cv.inRange(hsv, low, high, dst);
    cv.imshow(result_image_AI1, dst);
    src.delete()
    hsv.delete()
    dst.delete()
    low.delete()
    high.delete()
    // console.log("Doing image processing AI1")
}
let putMarker = (object, target) =>{
    object.beginPath()
    object.strokeStyle = "#FF0000";
    object.lineWidth = "2";
    object.rect(target[0], target[1], target[2], target[3])
    object.stroke()
}
let refreshMarker = (context) =>{
    try{
        var x,y,w,h = received_message_from_ROV["target_square"][0]
        putMarker(context,(x,y,w,h))
    }
    catch(error){}
}
let loadFilterValues = () =>{
    return fetch("./services/read_AI1_config.php")
    .then(response => response.json())
    .then(
      data => {
            first_slider_low.value = data["first_value_low"]
            first_slider_high.value = data["first_value_high"]
            second_slider_low.value = data["second_value_low"]
            second_slider_high.value = data["second_value_high"]
            third_slider_low.value = data["third_value_low"]
            third_slider_high.value = data["third_value_high"]
            size_slider_min.value = data["size_value_min"]
            size_slider_max.value = data["size_value_max"]
            percentage_slider_min.value = data["percentage_value_min"]
            percentage_slider_max.value = data["percentage_value_max"]

            first_slider_low_text.innerHTML = "H:"+first_slider_low.value
            first_slider_high_text.innerHTML = "H:"+first_slider_high.value
            second_slider_low_text.innerHTML = "S:"+second_slider_low.value
            second_slider_high_text.innerHTML = "S:"+second_slider_high.value
            third_slider_low_text.innerHTML = "V:"+third_slider_low.value
            third_slider_high_text.innerHTML = "V:"+third_slider_high.value
            size_slider_min_text.innerHTML = "S:"+size_slider_min.value
            size_slider_max_text.innerHTML = "S:"+size_slider_max.value
            percentage_slider_min_text.innerHTML = "P:"+percentage_slider_min.value
            percentage_slider_max_text.innerHTML = "P:"+percentage_slider_max.value

            first_value_low = parseInt(first_slider_low.value)
            first_value_high = parseInt(first_slider_high.value)
            second_value_low = parseInt(second_slider_low.value)
            second_value_high = parseInt(second_slider_high.value)
            third_value_low = parseInt(third_slider_low.value)
            third_value_high = parseInt(third_slider_high.value)
            size_value_min = parseInt(size_slider_min.value)
            size_value_max = parseInt(size_slider_max.value)
            percentage_value_min = parseInt(percentage_slider_min.value)
            percentage_value_max = parseInt(percentage_slider_max.value)
      }
    )
    .catch(error => console.log(error))
}
let updateFilterValues = (fl,fh,sl,sh,tl,th,smin,smax,pmin,pmax) =>{
    fetch("./services/save_AI1_config.php?first_value_low="+fl+"&first_value_high="+fh+"&second_value_low="+sl+"&second_value_high="+sh+"&third_value_low="+tl+"&third_value_high="+th+"&size_value_min="+smin+"&size_value_max="+smax+"&percentage_value_min="+pmin+"&percentage_value_max="+pmax)
    .then(response => {} )
    .then( data => {loadCameraConnection() })
    .catch(error => console.log(error))

    fetch("http://"+server_connection_on_ROV+"/TecXotic2022/services/updateAgent1.php?first_value_low="+fl+"&first_value_high="+fh+"&second_value_low="+sl+"&second_value_high="+sh+"&third_value_low="+tl+"&third_value_high="+th+"&size_value_min="+smin+"&size_value_max="+smax+"&percentage_value_min="+pmin+"&percentage_value_max="+pmax)
    .then(response => {} )
    .then( data => { })
    .catch(error => console.log(error))
}


//##################################################AGENT ACTIVATION##############################################
let agent1_button = document.getElementById("agent1_button")
let agent2_button = document.getElementById("agent2_button")
let agent3_button = document.getElementById("agent3_button")

var agent1_on = false
agent1_button.addEventListener("click", ()=>{
    agent1_on = !agent1_on;
    if(agent1_on){
        commands_instance.agent1 = true
        agent1_button.className = "btn btn-success"
    }else{
        commands_instance.agent1 = false
        agent1_button.className = "btn btn-primary"
    }
})






var agent2_on = false
agent2_button.addEventListener("click", ()=>{
    agent2_on = !agent2_on;
    if(agent2_on){
        commands_instance.agent1 = true
        agent2_button.className = "btn btn-success"
    }else{
        commands_instance.agent1 = false
        agent2_button.className = "btn btn-primary"
    }
})

var agent3_on = false
agent3_button.addEventListener("click", ()=>{
    agent3_on = !agent3_on;
    if(agent3_on){
        commands_instance.agent1 = true
        agent3_button.className = "btn btn-success"
    }else{
        commands_instance.agent1 = false
        agent3_button.className = "btn btn-primary"
    }
})


let gamepadRefresh = () =>{
    const {left_dpad, right_dpad} = controller.buttons
    if(left_dpad){
        if(!left_camera_pressed){
            left_camera_pressed = true;
            camera_selector--
            if(camera_selector < 0){
                camera_selector = 3
            }
            putMainCameraView(camera_selector)
        }
    }else{
        left_camera_pressed = false;
    }

    if(right_dpad){
        if(!right_camera_pressed){
            right_camera_pressed = true;
            camera_selector++
            if(camera_selector > 3){
                camera_selector = 0
            }
            putMainCameraView(camera_selector)
        }
    }else{
        right_camera_pressed = false;
    }
}

setInterval(gamepadRefresh, FPS_controller)































