const flask_address = "http://localhost:8080"

function blobToBase64(blob) {
  return new Promise((resolve, _) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
}
const fethImg = async ({method, body}) => {
    const response = await fetch(flask_address+'/photomosaic', {
        headers: {
            'Content-Type': 'application/json'
        },
        method,
        body
    })
    const blob = await response.blob()
    const base64 = await blobToBase64(blob)
    return base64;
}

var photoImages = [];
async function createPhoto(){
    const request = {method: "POST", body: JSON.stringify({
            capture: 1 //change the capture if the photos taken are from another camera
    })}
    const base64 = await fethImg(request);
    photoImages.push(base64);
    let img = document.createElement('img');
    img.src = photoImages[photoIndex];
    img.id = 'photomosaic/' + photoIndex.toString();
    img.style = "width: 720px; height: 420px;";
    document.getElementById("fotomosaico").appendChild(img);
    document.getElementById("imageIndex").innerHTML = "Image number: " + (photoIndex+1).toString();
    photoIndex++;
}

async function photomosaic() {
    const request = {method: "GET"}
    const base64 = await fethImg(request)
    document.getElementById('mosaic').src = base64;
}

async function replaceImg(index, capture){
    const request = {
        method: "PUT",
        body: JSON.stringify({index, capture})
    }
    const base64 = await fethImg(request);
    document.getElementById("photomosaic/"+ index.toString()).src = base64;
    //document.getElementById("photomosaic/"+ indice.toString()).src = "https://www.goya.com/media/7912/birria-tacos.jpg?quality=80";
}

var photoIndex = 0;
document.body.addEventListener('click',function(e){
    for (let i = 0; i < photoIndex; i++){
        if(e.target.id == 'photomosaic/'+ i.toString()){
            replaceImg(i, 1);
       }
    }
 });

document.getElementById("photomosaic").addEventListener("click", photomosaic)
document.getElementById("take_photo").addEventListener("click", createPhoto)
