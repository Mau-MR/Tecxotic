import json
from flask import Flask, request, Blueprint


buttons_functionality = Blueprint('buttons_functionality', __name__)

@buttons_functionality.route('actuators', methods=['POST'])
def send_actions():
    json = request.get_json()
    print(json )