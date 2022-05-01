import json
from flask import Flask, request, Blueprint

FishLength = Blueprint('fishLength', __name__)

@fishLength.route('/fishLength', methods=['POST'])
def process_json():
    json = request.get_json()

    x1 = float(json["x1"])
    y1 = float(json["y1"])
    x2 = float(json["x2"])
    y2 = float(json["y2"])
    x3 = float(json["x3"])
    y3 = float(json["y3"])
    x4 = float(json["x4"])
    y4 = float(json["y4"])
    reference = float(json["referencia"])

    pixel_2_cm_ratio = (((x2-x1)**2+(y2-y1)**2)**(1/2))/reference
    
    measurement = (((x4-x3)**2+(y4-y3)**2)**(1/2))/pixel_2_cm_ratio

    return str(round(measurement,4))