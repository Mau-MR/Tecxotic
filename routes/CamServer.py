import cv2
from flask import Response, Blueprint, request
from ColorFilter import processFilter
from RedDetection import processDetection
camServer = Blueprint('camServer', __name__)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 30)

cap2 = cv2.VideoCapture(1)
cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap2.set(cv2.CAP_PROP_FPS, 30)

def generate(capture):
    while True:
        ret, frame = capture.read()
        if ret:
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')


processImg = 0       # 0->NO    1->Filter    2->Detection
useFilter = False    # False->Normal cap with line detection    True->B&W cap with line detection
showDetection = True # False->Returns x_diff,y_diff    True->Returns cap with target detection
@camServer.route("/filterImg", methods=['POST'])
def filterImg():
    json = request.get_json()
    global processImg, useFilter, showDetection
    processImg = json["process"] 
    useFilter = json["filter"] 
    showDetection = json["detection"]  
@camServer.route("/video1")
def video1():
    if processImg == 1: 
        return Response(processFilter(cap, useFilter), mimetype="multipart/x-mixed-replace; boundary=frame")
    elif processImg == 2: 
        return Response(processDetection(cap, showDetection), mimetype="multipart/x-mixed-replace; boundary=frame")
    return Response(generate(cap),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
@camServer.route("/video2")
def video2():
    return Response(generate(cap2),
                    mimetype="multipart/x-mixed-replace; boundary=frame")



def release_video():
    # Releasing video
    cap2.release()

