import {flask_address} from "../Constants.js";
import {requestWithBLOB} from "../Connection/Requests.js";
document.getElementById("float_grid_button").addEventListener("click", getGridMeasurment)
let floatGridSrc = ''
export async function getGridMeasurment() {
    console.log("Grid measurement")
    let requestData = {
        grid_speed: document.getElementById("grid_speed").value,
        grid_angle: document.getElementById("grid_angle").value,
        grid_time: document.getElementById("grid_time").value,
        grid_x: document.getElementById("grid_x").value,
        grid_y: document.getElementById("grid_x").value
    }
    const url = await requestWithBLOB('POST', flask_address+'/floatgrid', requestData)
    var a = document.createElement('a');
    a.href = url;
    a.download = "file.jpg";
    a.click();
    a.remove();  //afterwards we remove the element again
    floatGridSrc = url
    // put here the src on specific id
}

