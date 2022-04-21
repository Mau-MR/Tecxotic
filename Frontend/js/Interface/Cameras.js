import {FPS_video, video_address} from '../Constants.js'

// Code for rendering the video from the server
const canvas = document.getElementById('view_main_camera');
const context = canvas.getContext('2d');
//Setting the image
const img = new Image();
img.src = video_address;
img.onload = () => {
    //Updating the frames every FPS_video
    setInterval(() => {
        context.drawImage(img, 0, 0);
    }, FPS_video)
};
