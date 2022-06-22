import cv2
from flask import Response, Blueprint, request
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
    cap1.release()


# Inserts new photo for the photomosaic
images = []


@camServer.route('/photomosaic', methods=['POST'])
def photo():
    body = request.json
    capture = body['capture']
    _, frame = cap1.get_frame()  # todo: handle posible error
    if capture == 2:
        _, frame = cap2.get_frame()
    (flag, encodedImage) = cv2.imencode(".jpg", frame)
    if not flag:
        return "Error decoding image taken"
    # appeding the pic to the array of fotomosaic
    images.append(frame)
    return Response(
        encodedImage.tobytes(),
        status=200,
        mimetype='img/jpeg')


# Generates the fotomosaic with the photos at the images array
@camServer.route('/photomosaic', methods=['GET'])
def photomosaic():
    if len(images) < 8:
        return "Not enough photos taken";  # not enough images
    for index, val in enumerate(images):  #
        images[index] = cv2.resize(val, (200, 200))
    stack1 = cv2.hconcat([images[0], images[1], images[2], images[3]])
    stack2 = cv2.hconcat([images[4], images[5], images[6], images[7]])
    stack3 = cv2.vconcat([stack1, stack2])
    (flag, encodedImage) = cv2.imencode(".jpg", stack3)
    if not flag:
        return "Error converting the photo to jpg";
    return Response(
        encodedImage.tobytes(),
        status=200,
        mimetype='img/jpeg')


# Update the foto of the photomosiac array with a screenshot of the given number of capture at the index wanted
@camServer.route('/photomosaic', methods=['PUT'])
def photomosaic_change():
    body = request.json
    _, frame = cap1.get_frame()
    if body['capture'] == 2:
        _, frame = cap2.get_frame()

    try:
        images[body['index']] = frame
    except Exception as e:
        return "Index out of range"

    (flag, encodedImage) = cv2.imencode(".jpg", frame)
    if not flag:
        return "Error decoding image taken"
    return Response(
        encodedImage.tobytes(),
        status=200,
        mimetype='img/jpeg')


# Returns screenshot for the measurements tasks
@camServer.route('/screenshot/<capture>', methods=['GET'])
def screenshot(capture):
    _, frame = cap1.get_frame()
    if capture == 2:
        _, frame = cap2.get_frame()
    (flag, encodedImage) = cv2.imencode(".jpg", frame)
    return Response(
        encodedImage.tobytes(),
        status=200,
        mimetype='img/jpeg'
    )
