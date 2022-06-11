from flask import Flask, send_file, request, Blueprint
import Floatgrid

floatGrid = Blueprint('floatGrid', __name__)

@floatGrid.route('/floatgrid',methods = ['POST'])#Task 3.1
def floatgrid():
    json_dict = request.get_json()
    speed = float(json_dict["grid_speed"])
    angle =  float(json_dict["grid_angle"])
    time =  float(json_dict["grid_time"])
    x = int(json_dict["grid_x"])
    y = int(json_dict["grid_y"])
    Floatgrid.main(speed, angle, time,x,y)
    return send_file('floatgrid.jpg', mimetype='image/jpg')