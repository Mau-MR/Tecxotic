points = [];
measurements = [];
var img;

var referencia;
var myImg;
var calcular;
var ss;
var correcto;
var reset;
var paragraph;
var myCanvas;

let pixel_2_cm_ratio;
let longitud_calculada;



//function imgSize(){
//       myImg = document.querySelector("#caradelmau");
//        var currWidth = myImg.clientWidth;
//        var currHeight = myImg.clientHeight;
//00        return [currWidth, currHeight]
//}

function setup() {
    img = createCapture(VIDEO);
    img.hide();
    //const [ancho, alto] = imgSize();
    myCanvas = createCanvas(293, 180);
    myCanvas.parent("prueba");
    myCanvas.position(0,0);
    
    image(img, 0, 0, width, height);
    
    referencia = createInput("9");
    referencia.parent("prueba");
    referencia.position(0,190);
    
    ss = createButton("Take Photo");
    ss.parent("prueba");
    ss.mousePressed(screenshot);
    ss.position(0,220);

    calcular = createButton("Calcular");
    calcular.parent("prueba");
    calcular.mousePressed(calcula);
    calcular.position(0,250);

    reset = createButton("Reiniciar");
    reset.parent("prueba");
    reset.mousePressed(reiniciar);
    reset.position(0,280);

    correcto = createButton("Correcto");
    correcto.parent("prueba");
    correcto.mousePressed(guarda);
    correcto.position(0,310);

    paragraph = createP("Waiting for measurement...").position(0,350);
    paragraph.style("font-size","25px");
    paragraph.parent("prueba");
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

function reiniciar() {
    points = [];
    paragraph.html("Waiting for measurement...");
    img = createCapture(VIDEO);
    img.hide();
}
function screenshot(){
    img = myCanvas.get();

}

function guarda(){
    if(longitud_calculada != 0){
    append(measurements, longitud_calculada);
    paragraph.html("Measurement has been saved correctly.");
    }
}

function calcula() {
    if (points.length % 2 == 0 && points.length >= 8 && referencia.value() != "") {
        pixel_2_cm_ratio = Math.sqrt(Math.pow(points[2] - points[0], 2) + Math.pow(points[3] - points[1], 2)) / float(referencia.value());
        longitud_calculada = Math.sqrt(Math.pow(points[6] - points[4], 2) + Math.pow(points[7] - points[5], 2)) / float(pixel_2_cm_ratio);
        //createP("La longitud Calculada es:" + str(longitud_calculada) + "cm");
        paragraph.html("La longitud Calculada es: " + str(longitud_calculada.toFixed(4)) + " cm");
    }
}

function mouseClicked() {
    if (points.length < 8 && mouseY <= height && mouseX <= width) {
        append(points, mouseX);
        append(points, mouseY);
    }
}