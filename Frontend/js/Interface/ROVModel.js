import * as THREE from "../libraries/three.min.js";
import { MTLLoader } from '../libraries/MTLLoader.js';
import { OBJLoader } from '../libraries/OBJLoader.js';
import {commands_instance} from '../Connection/Message.js'
const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 100)
let ROV3D = document.getElementById("ROV3D")


const light = new THREE.PointLight()
light.position.set(0,0,0)
scene.add(light)


const renderer = new THREE.WebGLRenderer(
    {
        antialias:true,
        canvas: ROV3D,
        alpha: true
    })
renderer.setSize( window.innerWidth, window.innerHeight )

// ROV3D.appendChild(renderer.domElement)

camera.position.z = 0

var rov_model
var mtlLoader = new MTLLoader();
function loadModel() {
    mtlLoader.load('./assets/ROV.mtl',  function(materials) {
        materials.preload();
        var objLoader = new OBJLoader();
        objLoader.setMaterials(materials);
        objLoader.load('./assets/ROV.obj',  function (object) {
            rov_model = object
            rov_model.position.set(0,0,-4)
            // rov_model.rotation.x = 90 * Math.PI / 180
            rov_model.rotation.y = 180 * Math.PI / 180
            rov_model.scale.set(1.2,1,1)
            scene.add(rov_model);

        });
    });
}
loadModel()

let map = (X, A, B, C, D) =>{
    return (X-A)/(B-A) * (D-C) + C
}
var MIN_VEL=-1000, MAX_VEL = 1000
const animate = function () {
    requestAnimationFrame( animate )
    if(rov_model != null){
        rov_model.rotation.x = map(commands_instance['pitch'], MIN_VEL, MAX_VEL,  225 * Math.PI / 180, 135 * Math.PI / 180 )
        rov_model.rotation.y = map(commands_instance['roll'], MIN_VEL, MAX_VEL,   225 * Math.PI / 180, 135 * Math.PI / 180 )
        rov_model.rotation.z = map(commands_instance['yaw'], MIN_VEL, MAX_VEL,    225 * Math.PI / 180, 135 * Math.PI / 180 )
    }
    renderer.render( scene, camera )
}
animate()




