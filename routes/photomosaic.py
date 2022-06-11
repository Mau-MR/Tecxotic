#Photomosaic utilities----------
from flask import send_file, request, Blueprint
import os
import Photomosaic

import cv2
currPhoto = 0
cap = cv2.VideoCapture(0)
mainDir = os.getcwd()
photosDir = mainDir + "\photos" #windows
#photosDir = mainDir + "/photos" #macos
#--------------

photomos = Blueprint('camServer', __name__)

@photomos.route('/photomosaicPhoto')#Take photo one by one
def photomosaic_photo():
    global currPhoto
    currPhoto +=1
    if currPhoto > 8:
        currPhoto = 1
        for f in os.listdir(photosDir):
            os.remove(os.path.join(photosDir, f))
    os.chdir(photosDir)
    Photomosaic.takePhoto(currPhoto, cap)
    os.chdir(mainDir)
    return send_file("photos\photo" + str(currPhoto) + ".jpg", mimetype='image/jpg')


@photomos.route('/photomosaicChange',methods=['POST'])#take and change a photo with the number of the photo
def photomosaic_change():
    json_dict = request.get_json()
    currentPhoto = json_dict["currentPhoto"]
    os.chdir(photosDir)
    Photomosaic.takePhoto(currentPhoto, cap)
    os.chdir(mainDir)
    return send_file("photos\photo" + str(currentPhoto) + ".jpg", mimetype='image/jpg')