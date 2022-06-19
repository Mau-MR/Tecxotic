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


# Photomosaic logic
images=[]
@camServer.route('/photo', methods=['GET'])
def photo():
    _, frame = cap1.get_frame() #todo: handle posible error
    (flag, encodedImage) = cv2.imencode(".jpg", frame)
    if not flag:
        print("Error converting the photo from taking picture")
        return;
    images.append(frame)
    return Response(
        encodedImage.tobytes(),
        status=200,
        mimetype='img/jpeg')

@camServer.route('/photomosaic', methods=['GET'])
def photomosaic():
    if len(images) < 8:
        return "Not enough photos taken"; # not enough images
    for index, val in enumerate(images): #
        images[index] = cv2.resize(val, (200,200))
    stack1=cv2.hconcat([images[0],images[1],images[2],images[3]])
    stack2=cv2.hconcat([images[4],images[5],images[6],images[7]])
    stack3=cv2.vconcat([stack1,stack2])
    (flag, encodedImage) = cv2.imencode(".jpg", stack3)
    if not flag:
        return "Error converting the photo to jpg";
    return Response(
        encodedImage.tobytes(),
        status=200,
        mimetype='img/jpeg')

"""
@camServer.route('/photomosaicChange',methods=['POST'])#take and change a photo with the number of the photo
def photomosaic_change():
    json_dict = request.get_json()
    currentPhoto = json_dict["currentPhoto"]
    Photomosaic.takePhoto(currentPhoto, cap)
    os.chdir(mainDir)
    return send_file("photos\photo" + str(currentPhoto) + ".jpg", mimetype='image/jpg')

"""
