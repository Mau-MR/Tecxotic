import websockets
import asyncio
import json
from tests.ConnectionPixhawk import Pixhawk

px = Pixhawk('COM7')  # TODO: ADD LATER
client = set()


async def echo(websocket, path):
    client.add(websocket)
    try:
        async for commands in websocket:
            print(commands)
            commands = json.loads(commands)
            px.drive_manual(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'],0)
            imuVal = px.get_msg('')
            imu = {
                "roll": imuVal['roll'],
                "yaw": imuVal['yaw'],
                "pitch": imuVal['pitch']
            }
            send = {
                "message_received": True,
                "imu": imu
            }
            send = str(json.dumps(send))
            await websocket.send(bytearray(send, 'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    except Exception as e:
        print("ERROR in main.py: " + str(e))
    finally:
        client.remove(websocket)


def run():
    start_server = websockets.serve(echo, '0.0.0.0', 55000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
