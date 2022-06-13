let camera__one = document.getElementById("camera__one");
let camera__two = document.getElementById("camera__two");
let camera__container = document.getElementById("camera__container");
let camera__line = document.getElementById("camera__line");

var mousePosition;
var offset = [0,0];
var isDown = false;

var normalHeight = (camera__container.offsetHeight-10)/2;
var normalWidth = (normalHeight * 16) /9;
camera__line.style.position = "absolute";


// Set default values to start 
camera__one.style.width =  normalWidth + "px";
camera__one.style.height = normalHeight +"px";

camera__two.style.width = normalWidth + "px"; 
camera__two.style.height = normalHeight +"px"; 

camera__line.style.top = camera__one.offsetTop + camera__one.offsetHeight + "px"; // default en la mitad

$(window).resize(function() { // Resize just happened, pixels changed
  normalHeight = (camera__container.offsetHeight-10)/2;
  normalWidth = (normalHeight * 16) /9;
  camera__one.style.width =  normalWidth + "px";
  camera__one.style.height = normalHeight +"px";
  camera__two.style.width =  normalWidth + "px";
  camera__two.style.height = normalHeight +"px";
  camera__line.style.top = camera__one.offsetTop + camera__one.offsetHeight + "px"; // default en la mitad
});

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
    moveLine();  
  }
}, true);

var mytext = document.getElementById('mytext');

function moveLine() {
  var defaultMiddle = (camera__container.offsetHeight / 2);
  var index = ((mousePosition.y + offset[1]) - defaultMiddle) ; //  - defaultMiddle 

  var heightOne = normalHeight + index;
  var heightTwo = normalHeight - index;

  camera__line.style.top = camera__one.offsetTop + camera__one.offsetHeight + "px"; // default en la mitad

  if(camera__container.offsetWidth > getWidth(heightTwo) && camera__container.offsetWidth > getWidth(heightOne)) {

    camera__line.style.top  = (mousePosition.y + offset[1]) + 'px';
    //camera__line.style.top = camera__one.offsetTop + camera__one.offsetHeight + "px"; // default en la mitad


    mytext.innerText = camera__container.offsetWidth + " ... " + getWidth(heightTwo);

    camera__one.style.height = heightOne + "px";
    camera__one.style.width = getWidth(heightOne) + "px";

    camera__two.style.height = heightTwo + "px"; 
    camera__two.style.width = getWidth(heightTwo) + "px";  
    camera__line.style.top = camera__one.offsetTop + camera__one.offsetHeight + "px"; // default en la mitad
  
  }  
}

function getWidth(current_hight) {
  var new_width;
  new_width =  ((current_hight * 16) / 9);
  
  return new_width;

}

