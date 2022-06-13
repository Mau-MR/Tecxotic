let camera__one = document.getElementById("camera__one");
let camera__two = document.getElementById("camera__two");
let camera__container = document.getElementById("camera__container");
let camera__line = document.getElementById("camera__line");

var mousePosition;
var offset = [0,0];
var isDown = false;


var minWidth = "36rem";
var minHeight = "24rem";

var normalHeight = (camera__container.offsetHeight-10)/2;
var normalWidth = (normalHeight * 16) /9;

camera__line.style.position = "absolute";

// Set default values to start 
camera__one.style.width =  normalWidth + "px";
camera__one.style.height = normalHeight +"px";
camera__two.style.width =  normalWidth + "px";
camera__two.style.height = normalHeight +"px";
camera__line.style.top = camera__one.offsetTop + camera__one.offsetHeight + "px"; // default en la mitad


camera__line.addEventListener('mousedown', function(e) {
    isDown = true;
    offset = [camera__line.offsetLeft - e.clientX, camera__line.offsetTop - e.clientY];    
}, true);

document.addEventListener('mouseup', function() {
    isDown = false;
}, true);

document.addEventListener('mousemove', function(event) {
  event.preventDefault();
  if (isDown) {
      mousePosition = { y : event.clientY };
      camera__line.style.top  = (mousePosition.y + offset[1]) + 'px';
  }
}, true);



