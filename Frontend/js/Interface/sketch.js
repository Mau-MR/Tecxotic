let points = [];
let measurements = [];
var img;
var myCanvas;
var biomass;
var calculado;
var promedio;

var images = [];

const REFERENCIA = 9;

let pixel_2_cm_ratio;
let imgIndex = 0;
let longitud_calculada;

const flask_address = "http://localhost:8080"
function blobToBase64(blob) {
  return new Promise((resolve, _) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
}
const fethImg = async (id) => {
    const response = await fetch(flask_address+'/screenshot/'+id, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'GET',
    })
    const blob = await response.blob()
    const base64 = await blobToBase64(blob)
    return base64;
}

function setup() {

    myCanvas = createCanvas(1280, 720);
    myCanvas.parent("prueba");
    myCanvas.position(50,500);

    calculado = false;
    append(images,"https://foodandtravel.mx/wp-content/uploads/2017/02/Tacos-tradicionales.jpg");
    append(images,"https://mexico.didiglobal.com/wp-content/uploads/sites/5/2022/02/tacos-de-carnitas.jpg.jpg");
    append(images, "https://cdn2.cocinadelirante.com/sites/default/files/styles/gallerie/public/images/2021/11/cuantas-calorias-tienen-los-tacos.jpg");
}


function draw() {
    background(230);
    img = createImg(images[imgIndex]);
    img.hide();

    image(img, 0, 0, width, height);
    if (points.length % 2 == 0 && points.length >= 2) {
        for (let i = 0; i < points.length; i = i + 2) {
            strokeWeight(10);
            stroke(255,0,0);
            point(points[i], points[i + 1]);
        }
    }
    if (points.length % 2 == 0 && points.length >= 4) {
        for (let i = 0; i < points.length; i = i + 4) {
            strokeWeight(5);
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

document.getElementById("prev").addEventListener("click",previa);
document.getElementById("next").addEventListener("click",siguiente);

function siguiente(){
    if (imgIndex == images.length-1){
        imgIndex = images.length-1;
    } else {   
        imgIndex += 1;
    }
}

function previa(){
    if (imgIndex == 0){
        imgIndex = 0;
    } else {   
        imgIndex -= 1;
    }
}

async function reiniciar() {
    points = [];
    calculado = false;
    promedio = null;
}


async function screenshot() {
    const base64 = await fethImg("1");
    append(images, base64);
    img = createImg(base64);
    img.hide()
    imgIndex++;
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
