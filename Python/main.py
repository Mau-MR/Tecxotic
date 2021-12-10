import asyncio
import websockets
import json
from ConnectionPixhawk import *

indicator_pixhawk = False
master = None

master = None
def Control(roll, pitch, yaw, throttle, connect_pixhawk):
    global master, indicator_pixhawk
    if master != None:
        master = ConnectDisconnectPixhawk(connect_pixhawk)
        if (indicator_pixhawk == False):
            indicator_pixhawk = True
    else:
        master = ConnectDisconnectPixhawk(connect_pixhawk)
        indicator_pixhawk = False
    # print(f"roll:{roll} pitch:{pitch} yaw:{yaw} throttle:{throttle} pixhawk:{connect_pixhawk}")
        
def UtilityControl():
	pass
	


client = set()
async def echo(websocket,path):
    print("Client connected...")
    client.add(websocket)
    try:
        async for commands in websocket:
            # print ("client say -> "+commands)
            commands = json.loads(commands)
            Control(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'], commands['connect_pixhawk'])
            send = {
                "message_received":True,
                "connection_pixhawk" : indicator_pixhawk
            }
            send = str(json.dumps(send))
            print(bytearray(send,'utf-8'))
            await websocket.send(bytearray(send,'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    finally:
        client.remove(websocket)




if __name__ == "__main__":
    try:
        print("Running...")
        start_server = websockets.serve(echo, "10.49.182.166", 55000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

      