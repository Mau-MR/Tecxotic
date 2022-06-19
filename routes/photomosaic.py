from flask import request, Blueprint
from Photomosaic import photomosaic as take_photo
from CamServer import  cap

photomos = Blueprint('photomos', __name__)

@photomos.route('/photomosaic', methods=['GET'])
def photomosaic_photo():
    take_photo()


@photomos.route('/photomosaicChange',methods=['POST'])#take and change a photo with the number of the photo
def photomosaic_change():
    json_dict = request.get_json()
    currentPhoto = json_dict["currentPhoto"]
    os.chdir(photosDir)
    Photomosaic.takePhoto(currentPhoto, cap)
    os.chdir(mainDir)
    return send_file("photos\photo" + str(currentPhoto) + ".jpg", mimetype='image/jpg')