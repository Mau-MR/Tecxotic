const flask_address = "http://localhost:8080"
var photoImages = [];

/*photoImages.push("https://www.comedera.com/wp-content/uploads/2017/08/tacos-al-pastor-receta.jpg");
photoImages.push("https://mexico.didiglobal.com/wp-content/uploads/sites/5/2022/02/tacos-de-carnitas.jpg.jpg");
photoImages.push("https://www.travelreport.mx/mexico/tacos-tradicionales-de-mexico/attachment/tacos-tradicionales-de-mexico-pastor/");*/

var photoIndex = 0;
2
function blobToBase64(blob) {
  return new Promise((resolve, _) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
}
const fethImg = async (id) => {
    const response = await fetch(flask_address+'/screenshot/'+id, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'GET',
    })
    const blob = await response.blob()
    const base64 = await blobToBase64(blob)
    return base64;
}

async function createPhoto(){
    const base64 = await fethImg("1");
    photoImages.push(base64);
    let img = document.createElement('img');
    img.src = photoImages[photoIndex];
    img.id = 'photomosaic/' + photoIndex.toString();
    img.style = "width: 720px; height: 420px;";
    document.getElementById("fotomosaico").appendChild(img);
    document.getElementById("imageIndex").innerHTML = "Image number: " + (photoIndex+1).toString();
    photoIndex++;
}

function photomosaic(){

}

async function replaceImg(indice){
    const base64 = await fethImg("1");
    document.getElementById("photomosaic/"+ indice.toString()).src = base64;
    //document.getElementById("photomosaic/"+ indice.toString()).src = "https://www.goya.com/media/7912/birria-tacos.jpg?quality=80";
}

document.body.addEventListener('click',function(e){
    for (let i = 0; i < photoIndex; i++){
        if(e.target.id == 'photomosaic/'+ i.toString()){
            replaceImg(i);
       }
    }
 });

document.getElementById("photomosaic").addEventListener("click", photomosaic)
document.getElementById("take_photo").addEventListener("click", createPhoto)
