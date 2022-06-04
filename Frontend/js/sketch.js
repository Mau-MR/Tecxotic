points = [];
measurements = [];
var img;

var myCanvas;

const REFERENCIA = 9;
const DIVWIDTH = document.querySelector('#prueba').offsetWidth;

let pixel_2_cm_ratio;
let longitud_calculada;

function setup() {
    img = createCapture(VIDEO);
    img.hide();
    myCanvas = createCanvas(DIVWIDTH, DIVWIDTH*0.6);
    myCanvas.parent("prueba");
    myCanvas.position(0,0);
    
    image(img, 0, 0, width, height);
}

function draw() {

    image(img, 0, 0, width, height);
    if (points.length % 2 == 0 && points.length >= 2) {
        for (let i = 0; i < points.length; i = i + 2) {
            strokeWeight(2);
            stroke(0,0,255);
            point(points[i], points[i + 1]);
        }
    }
    if (points.length % 2 == 0 && points.length >= 4) {
        for (let i = 0; i < points.length; i = i + 4) {
            strokeWeight(1);
            stroke(0);
            line(points[i], points[i + 1], points[i + 2], points[i + 3]);
        }
    }
}
document.getElementById("screenshot").addEventListener("click",screenshot);
document.getElementById("reset").addEventListener("click",reiniciar);
document.getElementById("calculate").addEventListener("click",calcula);
document.getElementById("correct").addEventListener("click",guarda);

function reiniciar() {
    points = [];
    document.getElementById("measurement-text").innerHTML = "Waiting for measurement...";
    img = createCapture(VIDEO);
    img.hide();
}


function screenshot(){
    img = myCanvas.get();
}

function guarda(){
    if(longitud_calculada != 0){
    append(measurements, longitud_calculada);
    document.getElementById("measurement-text").innerHTML = "Measurement has been saved correctly.";
    }
}

function calcula() {
    if (points.length % 2 == 0 && points.length >= 8) {
        pixel_2_cm_ratio = Math.sqrt(Math.pow(points[2] - points[0], 2) + Math.pow(points[3] - points[1], 2)) / float(REFERENCIA);
        longitud_calculada = Math.sqrt(Math.pow(points[6] - points[4], 2) + Math.pow(points[7] - points[5], 2)) / float(pixel_2_cm_ratio);
        document.getElementById("measurement-text").innerHTML = "Measurement: " + str(longitud_calculada.toFixed(4)) + " cm";
    }
}

function mouseClicked() {
    if (points.length < 8 && mouseY <= height && mouseX <= width) {
        append(points, mouseX);
        append(points, mouseY);
    }
}