from flask import request, Blueprint, Response
from routes.utils import Floatgrid
import cv2

floatGrid = Blueprint('floatGrid', __name__)

@floatGrid.route('/floatgrid',methods = ['POST'])#Task 3.1
def floatgrid():
    json_dict = request.get_json()
    speed = float(json_dict["grid_speed"])
    angle =  float(json_dict["grid_angle"])
    time =  float(json_dict["grid_time"])
    x = int(json_dict["grid_x"])
    y = int(json_dict["grid_y"])
    img = Floatgrid.main(speed, angle, time, x, y)
    (flag, encodedImage) = cv2.imencode(".jpg", img)
    if not flag:
        print("Error converting the photo from taking picture")
        return;
    print("Successfully saved image")
    return Response(
        encodedImage.tobytes(),
        status=200,
        mimetype='img/jpeg')