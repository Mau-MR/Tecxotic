import {FPS_video, flask_address} from '../Constants.js'

// Code for rendering the video from the server
const camera1 = document.getElementById('view_camera1');
const context1 = camera1.getContext('2d');
//Setting the image
const image1 = new Image();
image1.src = flask_address + '/video1';
image1.onload = () => {
    //Updating the frames every FPS_video
    setInterval(() => {
        context1.drawImage(image1, 0, 0);
    }, FPS_video)
};
// Code for rendering the video from the server
const camera2 = document.getElementById('view_camera2');
const context2 = camera2.getContext('2d');
//Setting the image
const image2 = new Image();
image2.src = flask_address+'/video2';
image2.onload = () => {
    //Updating the frames every FPS_video
    setInterval(() => {
        context2.drawImage(image2, 0, 0);
    }, FPS_video)
};
