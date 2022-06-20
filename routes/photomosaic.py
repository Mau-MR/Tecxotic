#Photomosaic utilities----------
from flask import send_file, request, Blueprint
import os
from routes.utils import Photomosaic

import cv2
currPhoto = 0
cap = cv2.VideoCapture(0)
mainDir = os.getcwd()
#photosDir = mainDir + "\photos" #windows
photosDir = mainDir + "/photos" #jetson
#--------------

photomos = Blueprint('photomos', __name__)

@photomos.route('/photomosaic')#Returns photomosaic
def photomosaico():
    os.chdir(photosDir)
    Photomosaic.photomosaic()
    os.chdir(mainDir)
    return send_file(photosDir+  "/photomosaic.jpg", mimetype='image/jpg')

@photomos.route('/photomosaicPhoto')#Take photo one by one
def photomosaic_photo():
    global currPhoto
    currPhoto +=1
    if currPhoto > 8:
        currPhoto = 1
    os.chdir(photosDir)
    Photomosaic.takePhoto(currPhoto, cap)
    os.chdir(mainDir)
    return send_file(photosDir+  "/photo"  + str(currPhoto) + ".jpg", mimetype='image/jpg')


@photomos.route('/photomosaicChange',methods=['POST'])#take and change a photo with the number of the photo
def photomosaic_change():
    json_dict = request.get_json()
    currentPhoto = json_dict["currentPhoto"]
    os.chdir(photosDir)
    Photomosaic.takePhoto(currentPhoto, cap)
    os.chdir(mainDir)
    return send_file(photosDir+  "photo"  + str(currentPhoto) + ".jpg", mimetype='image/jpg')