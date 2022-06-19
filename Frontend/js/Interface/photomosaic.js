import {flask_address} from "../Constants.js";
import {requestWithBLOB} from "../Connection/Requests";


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
document.getElementById("photomosaic_button").addEventListener("click", photomosaic)
document.getElementById("photo_button").addEventListener("click", takePhoto)
