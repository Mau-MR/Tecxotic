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

indicator_pixhawk = False
master = None

def Control(roll, pitch, yaw, throttle, connect_pixhawk, arm_disarm):
    global master, indicator_pixhawk
    if master != None:
        master = ConnectDisconnectPixhawk(connect_pixhawk)
        Arm_Disarm(master, arm_disarm)
        Move(master, roll, pitch, yaw, throttle, 0)

        if (indicator_pixhawk == False):
            indicator_pixhawk = True
    else:
        master = ConnectDisconnectPixhawk(connect_pixhawk)
        indicator_pixhawk = False
    # print(f"roll:{roll} pitch:{pitch} yaw:{yaw} throttle:{throttle} pixhawk:{connect_pixhawk}")
        
def UtilityControl(agent1, agent2, agent3):
    if agent1 == True:
        roll, pitch, yaw, throttle, target_square = Agent1Manager.run()
        # print(f"{roll}   {pitch}   {yaw}   {throttle}")
        return  target_square
    return (-1,-1,-1,-1)

def CameraControl():
    pass


client = set()
async def echo(websocket,path):
    print("Client connected...")
    client.add(websocket)
    try:
        async for commands in websocket:
            # print (commands)
            commands = json.loads(commands)
            Control(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'], commands['connect_pixhawk'], commands['arm_disarm'])
            target_square = UtilityControl(commands['agent1'],commands['agent2'],commands['agent3'])
            send = {
                "message_received":True,
                "connection_pixhawk" : indicator_pixhawk,
                "target_square" : (target_square)
            }
            send = str(json.dumps(send))
            #print(bytearray(send,'utf-8'))
            await websocket.send(bytearray(send,'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    except Exception as e:
        print("ERROR in main.py: "+str(e))
    finally:
        client.remove(websocket)




if __name__ == "__main__":
    try:
        print("Running...")
        CamServer.run()
        start_server = websockets.serve(echo, IP_ADDRESS, PORT)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

     #GIT PUSH TESTING 
