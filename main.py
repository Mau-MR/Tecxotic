from flask import Flask
from routes.CamServer import camServer
from routes.Biomass import biomass

import websockets
import asyncio
from threading import Thread
import json

from ConnectionPixhawk import *
from ManualControl import *
import Agent1Manager
from GripperManager import openGripper,closeGripper, clearPort, stopMotor, runMotor

app = Flask(__name__)
app.register_blueprint(camServer)
app.register_blueprint(biomass)

indicator_pixhawk = False
master = None
target_square = None


# Submarine control
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


def CameraControl():
    pass


client = set()


async def echo(websocket, path):
    print("Client connected...")
    client.add(websocket)
    try:
        async for commands in websocket:
            # print (commands)
            commands = json.loads(commands)
            Control(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'],
                    commands['connect_pixhawk'], commands['arm_disarm'], commands['agent1'], commands['agent2'],
                    commands['agent3'])
            openGripper(commands['openGripper'])
            closeGripper(commands['closeGripper'])
            runMotor(commands['runMotor'])
            stopMotor(commands['stopMotor'])
            send = {
                "message_received": True,
                "connection_pixhawk": indicator_pixhawk,
                "target_square": target_square,
            }
            send = str(json.dumps(send))
            await websocket.send(bytearray(send, 'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    except Exception as e:
        print("ERROR in main.py: " + str(e))
    finally:
        client.remove(websocket)
        clearPort()


app.config['CORS_HEADERS'] = 'Content-Type'
name_space = '/tecxotic'  # espacio de nombres
client_query = []



if __name__ == '__main__':
    try:
        print("Running...")
        calibrateIMU()
        # Running the server that delivers video and the task, each request runs on diferent thread
        Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)).start()
        # Running the websocket server that manage the manual control of the ROV
        start_server = websockets.serve(echo, '0.0.0.0', 55000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        clearPort()
    except Exception as e:
        print(e)
