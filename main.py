import asyncio
import cv2
import websockets
import json
from ConnectionPixhawk import *
from ManualControl import *
import Agent1Manager
import CamServer
from time import sleep
from Constants import *
from GripperManager import gripperManager

indicator_pixhawk = False
master = None
target_square = None


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
            send = {
                "message_received": True,
                "connection_pixhawk": indicator_pixhawk,
                "target_square": target_square,
                "gripper_state": gripperManager(commands['gripper'])
            }
            send = str(json.dumps(send))
            await websocket.send(bytearray(send, 'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    except Exception as e:
        print("ERROR in main.py: " + str(e))
    finally:
        client.remove(websocket)


if __name__ == "__main__":
    try:
        print("Running...")
        # CamServer.run()
        start_server = websockets.serve(echo, IP_ADDRESS, PORT)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

    # GIT PUSH TESTING
