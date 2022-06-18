import websockets
import asyncio
import json
from tests.ConnectionPixhawk import Pixhawk
# px = Pixhawk(direction='/dev/serial/by-id/usb-ArduPilot_Pixhawk1_380020000A51353338353732-if00')
px = Pixhawk(direction='COM7')

def handle_motors_arming(cmd):
    if cmd != px.get_pix_info()['is_armed']:
        px.arm_disarm()
def handle_pix_mode(mode):
    if mode != px.get_pix_info()['mode']:
        px.change_mode(mode)



client = set()
async def echo(websocket, path):
    client.add(websocket)
    try:
        async for commands in websocket:
            print(commands)
            commands = json.loads(commands)
            px.drive_manual(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'],0)
            imuVal = px.get_msg('AHRS2')
            imu = {
                "roll": imuVal['roll'],
                "yaw": imuVal['yaw'],
                "pitch": imuVal['pitch']
            }
            send = {
                "message_received": True,
                "imu": imu,
                "pix_info": px.get_pix_info()
            }
            send = str(json.dumps(send))
            await websocket.send(bytearray(send, 'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    except Exception as e:
        print("ERROR in main.py: " + str(e))
    finally:
        client.remove(websocket)
        px.disarm()


def run():
    start_server = websockets.serve(echo, '0.0.0.0', 55000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    run()