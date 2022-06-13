let camera__one = document.getElementById("camera__one");
let camera__two = document.getElementById("camera__two");
let camera__container = document.getElementById("camera__container");
let camera__line = document.getElementById("camera__line");

var mousePosition;
var offset = [0,0];
var isDown = false;

camera__line.style.position = "absolute";
camera__line.style.top = camera__one.offsetHeight + "px"; // default en la mitad

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



