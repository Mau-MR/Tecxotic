import json
from flask import Flask, request, Blueprint
import serial

arduino = serial.Serial(port='usb-1a86_USB_Serial-if00-port0', baudrate=115200, timeout=1)


def send(message):
    arduino.write(bytes(message, 'UTF-8'))


buttons_functionality = Blueprint('buttons_functionality', __name__)

@buttons_functionality.route('actuators', methods=['POST'])
def send_actions():
    json = request.get_json()
    send(json.actions)
    # print(json )