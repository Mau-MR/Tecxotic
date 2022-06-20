from flask import Flask
from flask_cors import CORS
from threading import Thread
# Flask routes
from routes.CamServer import camServer, cap1, cap2
from routes.floatGrid import floatGrid
#from routes.photomosaic import photomos
from routes.ButtonsFunctionality import buttons_functionality
#from core.Server import run as websocket_server



app = Flask(__name__)
CORS(app)
app.register_blueprint(camServer)
app.register_blueprint(floatGrid)
app.register_blueprint(buttons_functionality)
#app.register_blueprint(photomos)



if __name__ == '__main__':
    try:
        # Running the server that delivers video and the task, each request runs on diferent thread
        Thread(
            target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)).start()
        # Running the websocket server that manage the manual control of the ROV
        #websocket_server()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Releasing video") #TODO: CHECK WHETHER THIS CODE IS TRULY EXECUTING
        cap1.release()
        cap2.release()
        pass
