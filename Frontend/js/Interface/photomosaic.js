import {flask_address} from "../Constants.js";
import {requestWithBLOB} from "../Connection/Requests";


var photoImages = [];
append(photoImages, "https://www.comedera.com/wp-content/uploads/2017/08/tacos-al-pastor-receta.jpg");
var photoIndex = 0;

export async function photomosaic () {
    console.log("photomosaic")
    const url = await requestWithBLOB('GET', flask_address+'/photomosaic')
    var a = document.createElement('a');
    a.href = url;
    a.download = "file.jpg";
    a.click();
    a.remove();  //afterwards we remove the element again
}

const URL_array = [];
export async function takePhoto(){
    console.log("photo")
    const url = await requestWithBLOB('GET', flask_address+'/photo')
    URL_array.push(url)
    var a = document.createElement('a');
    a.href = url;
    a.download = "file.jpg";
    a.click();
    a.remove();  //afterwards we remove the element again
}

function createPhoto(){
    console.log("Funcionando");
    document.createElement("img");
    img.src = photoImages[photoIndex];
    document.body.appendChild(img);

}

document.getElementById("photomosaic").addEventListener("click", photomosaic)

document.getElementById("take_photo").addEventListener("click", createPhoto)
