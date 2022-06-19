import {webRequest} from '../Connection/Requests.js'
let points = [];
let measurements = [];
var img;
var myCanvas;
var biomass;
var calculado;
var promedio;

const REFERENCIA = 9;

let pixel_2_cm_ratio;
let longitud_calculada;
let flask_address = 'http://192.168.2.2:8080'
function setup() {

    myCanvas = createCanvas(470, 295);
    myCanvas.parent("prueba");
    myCanvas.position(0,0);

    if(camera == 1) { // camera comes from toggle_task_one.js
        img = createImg(flask_address+'/video1'); //Aquí va el url de las cámaras
    } else if (camera == 2) {
        img = createImg(flask_address+'/video2'); //Aquí va el url de las cámaras
    }
    img.hide();

    image(img, 0, 0, 470, 275);

    calculado = false;
}


function draw() {
    image(img, 0, 0, width, height);
    if (points.length % 2 == 0 && points.length >= 2) {
        for (let i = 0; i < points.length; i = i + 2) {
            strokeWeight(6);
            stroke(255,0,0);
            point(points[i], points[i + 1]);
        }
    }
    if (points.length % 2 == 0 && points.length >= 4) {
        for (let i = 0; i < points.length; i = i + 4) {
            strokeWeight(3);
            stroke(0);
            line(points[i], points[i + 1], points[i + 2], points[i + 3]);
        }
    }
}
document.getElementById("screenshot").addEventListener("click",screenshot);
document.getElementById("reset").addEventListener("click",reiniciar);
document.getElementById("calculate").addEventListener("click",calcula);
document.getElementById("correct").addEventListener("click",guarda);
document.getElementById("biomass").addEventListener("click",biomasa);
document.getElementById("float_grid_button").addEventListener("click", getGridMeasurment)
document.getElementById("photomosaic_button").addEventListener("click", photomosaic)


function reiniciar() {
    points = [];
    document.getElementById("measurement-text").innerHTML = "Waiting for measurement...";
    if(camera == 1) { // camera comes from toggle_task_one.js
        img = createImg(flask_address+'/video1'); //Aquí va el url de las cámaras
    } else if (camera == 2) {
        img = createImg(flask_address+'/video2'); //Aquí va el url de las cámaras
    }
    img.hide();
    calculado = false;
    promedio = null;
}


function screenshot(){
    img = myCanvas.get();
}

function guarda(){
    if(longitud_calculada != 0 && calculado == true){
    append(measurements, longitud_calculada);
    document.getElementById("measurement-text").innerHTML = "Measurement has been saved correctly.";
    calculado = false;
    }
    if (measurements.length == 3){
        promedio = measurements[0]+measurements[1]+measurements[2];
        promedio = promedio/3;
        document.getElementById("length-mean").innerHTML = "Calculated mean length = "  + str(promedio.toFixed(4));
    }
}

function calcula() {
    if (points.length % 2 == 0 && points.length >= 8) {
        pixel_2_cm_ratio = Math.sqrt(Math.pow(points[2] - points[0], 2) + Math.pow(points[3] - points[1], 2)) / float(REFERENCIA);
        longitud_calculada = Math.sqrt(Math.pow(points[6] - points[4], 2) + Math.pow(points[7] - points[5], 2)) / float(pixel_2_cm_ratio);
        document.getElementById("measurement-text").innerHTML = "Measurement: " + str(longitud_calculada.toFixed(4)) + " cm.";
        calculado = true;
    }
}

function mouseClicked() {
    if (points.length < 8 && mouseY <= height && mouseY > 0 && mouseX <= width && mouseX >= 0) {
        append(points, mouseX);
        append(points, mouseY);
    }
}

function biomasa(){
    let N = document.getElementById("n-data").value;
    let a = document.getElementById("a-data").value;
    let b = document.getElementById("b-data").value;
    
    let l = document.getElementById("l-data").value;
    if (l == "" && promedio != null){
        l = promedio;
    }   

    N = float(N);
    N = N/1000;
    a = float(a);
    b = float(b);
    l = float(l);
    biomass = N*a*(Math.pow(l,b))
    document.getElementById("measurement-text").innerHTML = "Calculated Biomass = "  + str(biomass.toFixed(4));
}

async function getGridMeasurment() {
    let requestData = {
        grid_speed: document.getElementById("grid_speed").value,
        grid_angle: document.getElementById("grid_angle").value,
        grid_time: document.getElementById("grid_time").value,
        grid_x: document.getElementById("grid_x").value,
        grid_y: document.getElementById("grid_x").value
    }

    let res =await webRequest('POST',flask_address+'/floatgrid',requestData)
    console.log(requestData, response)
    document.getElementById("grid-answer").innerHTML = "Calculated position = "  + str(res);
}

var URL_array = []
async function photomosaic () {
    let init = {
        method: 'GET',
        mode: 'cors'
    };
    let response = await fetch(flask_address+'/photomosaicPhoto', init)
    let blob = await response.blob();
    let url = window.URL.createObjectURL(blob);
    URL_array.push(url)
    return URL_array
}
