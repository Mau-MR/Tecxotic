import json
from flask import Flask, request, Blueprint
import serial
buttons_functionality = Blueprint('buttons_functionality', __name__)
try:
    arduino = serial.Serial(port='/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0', baudrate=115200, timeout=1)
except Exception as e:
    print("ERROR in ButtonsFunctionality.py, serial route not founded: " + str(e))
# arduino = serial.Serial(port='COM3', baudrate=115200, timeout=1) #for testing in local


def send(message):
    arduino.write(bytes(message, 'UTF-8'))

@buttons_functionality.route('/actuators', methods=['POST'])
def send_actions():
    json = request.get_json()
    print('json_respone: ', int(json["actions"]))

    send(str(json["actions"]))
    return ""