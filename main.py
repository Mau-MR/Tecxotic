from flask import Flask
from flask_cors import CORS
from threading import Thread
import os
# Flask routes
from routes.CamServer import camServer
from routes.floatGrid import floatGrid
from routes.photomosaic import photomos
from routes.ButtonsFunctionality import buttons_functionality
from core.Server import run as websocket_server


mainDir = os.getcwd()
photosDir = mainDir + "\photos" #windows


app = Flask(__name__)
CORS(app)
app.register_blueprint(camServer)
app.register_blueprint(photomos)
app.register_blueprint(floatGrid)
app.register_blueprint(buttons_functionality)



if __name__ == '__main__':
    try:
        # Running the server that delivers video and the task, each request runs on diferent thread
        Thread(
            target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)).start()
        # Running the websocket server that manage the manual control of the ROV
        websocket_server()
    except KeyboardInterrupt:
        for f in os.listdir(photosDir):
            os.remove(os.path.join(photosDir, f))
        pass
    except Exception as e:
        for f in os.listdir(photosDir):
            os.remove(os.path.join(photosDir, f))
        print(e)
        pass
