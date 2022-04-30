import json
from flask import Flask, request, Blueprint

biomass = Blueprint('biomass', __name__)

@biomass.route('/biomass', methods=['POST'])
def process_json():
    json = request.get_json()

    N = float( json["N"] )/1000
    a = float( json["a"] )
    b = float( json["b"] )
    L = float( json["L"] )

    M = N*a*(L**b)

    return str(round(M,2))