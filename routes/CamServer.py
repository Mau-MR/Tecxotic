import cv2
from flask import Response, Blueprint
from Capture import Capture
camServer = Blueprint('camServer', __name__)

cap1 = Capture(0)
cap2 = Capture(1)

def generate(capture):
    while True:
        ret, frame = capture.get_frame()
        if ret:
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')



@camServer.route("/video1")
def video1():
    return Response(generate(cap1),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
@camServer.route("/video2")
def video2():
    return Response(generate(cap2),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def release_video():
    # Releasing video
    cap2.release()

