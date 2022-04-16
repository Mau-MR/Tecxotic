from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit

import photomosaic

#imports del código anterior
#import asyncio
import cv2
import json
from ConnectionPixhawk import *
from ManualControl import *
import Agent1Manager
import CamServer
from time import sleep
from Constants import *
from GripperManager import gripperManager, clearPort

#--------------------------

#maindir = r"C:\Users\PC\OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey\Universidad TEC21\TECXOTIC\Software\Photomosaic"


indicator_pixhawk = False
master = None
target_square = None

#Submarine control
def Control(roll, pitch, yaw, throttle, connect_pixhawk, arm_disarm, agent1, agent2, agent3):
    global master, indicator_pixhawk, target_square
    target_square = (-1, -1, -1, -1)
    if master != None:
        master = ConnectDisconnectPixhawk(connect_pixhawk)
        Arm_Disarm(master, arm_disarm)
        if agent1 == False and agent2 == False and agent3 == False:
            Move(master, roll, pitch, yaw, throttle, 0)
        elif agent1 == True and agent2 == False and agent3 == False:
            roll, pitch, yaw, throttle, target_square = Agent1Manager.run()
            Move(master, int(roll), int(pitch), int(yaw), int(throttle), 0)
        elif agent1 == False and agent2 == True and agent3 == False:
            pass
        elif agent1 == False and agent2 == False and agent3 == True:
            pass

        if (indicator_pixhawk == False):
            indicator_pixhawk = True
    else:
        master = ConnectDisconnectPixhawk(connect_pixhawk)
        indicator_pixhawk = False
    # print(f"roll:{roll} pitch:{pitch} yaw:{yaw} throttle:{throttle} pixhawk:{connect_pixhawk}")

#------------------------------------------------------

def CameraControl():
    pass







#Use of Flask_Socketio


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
name_space = '/tecxotic' # espacio de nombres
event_name = 'mensaje de devolución de llamada' # Objeto receptor de mensaje
client_query = []






@app.route('/photomosaic')
def photomosaicfunc():
    photomosaic.main()
    return 'Done!'


 # on ('objeto de suscripción de mensaje', 'distinción de espacio de nombres')
@socketio.on('message', namespace=name_space)
def receive_message(commands):
    #El servidor recibe el mensaje
    #print('recevice message', commands)
    commands = json.loads(commands)
    Control(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'],
                    commands['connect_pixhawk'], commands['arm_disarm'], commands['agent1'], commands['agent2'],
                    commands['agent3'])
         #Envíe el mensaje al cliente o puede optar por no devolverlo.
    send = {
                "message_received": True, 
                "connection_pixhawk": indicator_pixhawk,
                "target_square": target_square,
                "gripper_state": gripperManager(commands['gripper'])
            }
    send = str(json.dumps(send))
    emit('callback message', send, broadcast=True, namespace=name_space)
 
'''
@socketio.on('my broadcast event', namespace=name_space)
def send_message(message):
    print("my response===>", message)
    emit('my response', {'data': message}, broadcast=True)
'''

@socketio.on('connect', namespace=name_space)
def client_connect():
     # Establecer conexión sid: ID de objeto de conexión
    client_id = request.sid
    print('1 connected ==> ', client_id)
    client_query.append(client_id)
    emit('connect', '%s connect successful!' % client_id, broadcast=True)


@socketio.on('disconnect', namespace=name_space)
def client_disconnect():
    client_query.remove(request.sid)
    print('0 Client disconnected==> ', request.sid)





if __name__ == '__main__':
    try:
        print("Running...")
        # CamServer.run()
        socketio.run(app, host='0.0.0.0', port= PORT, debug =True) 
    except KeyboardInterrupt:
        clearPort()
    except Exception as e:
        print(e)

