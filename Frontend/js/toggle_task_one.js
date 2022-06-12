let radio_1 = document.getElementById('radio-1');
let radio_2 = document.getElementById('radio-2');
let camera = 1; // camera default

radio_1.addEventListener("click",radio);
radio_2.addEventListener("click",radio);

function radio() {
    if(radio_1.checked) {
        //I am checked
        camera = 1;
        reiniciar();  // calls function in sketch.js 
    } 
    else if(radio_2.checked) {
        //I am checked
        camera = 2;
        reiniciar();  // calls function in sketch.js 
    } 
}