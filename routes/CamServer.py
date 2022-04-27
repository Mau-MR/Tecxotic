import cv2
from flask import Response, Blueprint
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



@camServer.route("/video1")
def video1(id):
    return Response(generate(cap),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
@camServer.route("/video2")
def video2(id):
    return Response(generate(cap2),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def release_video():
    # Releasing video
    cap2.release()
