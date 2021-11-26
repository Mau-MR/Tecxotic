import asyncio
import websockets
import json
import ConnectionArduino

indicator_pixhawk = False
pixhawk_status = False
master = None


def Control(roll, pitch, yaw, throttle):
    send_arduino = " "+str(roll)+" "+str(pitch)+" "+str(yaw)+" "+str(throttle)
  
    #print(send_arduino)
    ConnectionArduino.send(json.dumps(send_arduino))
    print(ConnectionArduino.receive())
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
            Control(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'])
            # print(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'])
            send = {
                   "message_received":True
                }
            send = json.dumps(send)
            send = str(send)
            await websocket.send(bytearray(send,'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    finally:
        client.remove(websocket)




if __name__ == "__main__":
    try:
        print("Running...")
        start_server = websockets.serve(echo, "127.0.0.1", 55000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

      