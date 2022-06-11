
document.getElementById('fotoBtn').addEventListener("click",async function () {
    console.log("Clciekckdkdd")
    const body = {
        grid_speed: 0.143,
        grid_angle: 103,
        grid_time: 144,
        grid_x: 6,
        grid_y: 15
    }
    let init = {
        method: 'GET',
        mode: 'cors'
    };
    const response = await fetch("http://localhost:8080/photomosaicPhoto", init)
    console.log(response.body)
    const blob = await response.blob();
    console.log(blob)
    const url = window.URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = "file.jpg";
    a.click();
    a.remove();  //afterwards we remove the element again
})