import asyncio
import websockets
import json
from ConnectionPixhawk import *
from PID import PID
roll_pid = PID(0, 0, 0, setpoint=0)
roll_pid.output_limits = (-1000,1000)
pitch_pid = PID(0, 0, 0, setpoint=0)
pitch_pid.output_limits = (-1000,1000)
yaw_pid = PID(0, 0, 0, setpoint=0)
yaw_pid.output_limits = (-1000,1000)
throttle_pid = PID(0, 0, 0, setpoint=0)
throttle_pid.output_limit = (0,1000)

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
        
def UtilityControl(agent1, agent2, agent3,pid_values):
    roll_pid.tunings = (pid_values['roll_p'], pid_values['roll_i'],pid_values['roll_d'])
    pitch_pid.tunings = (pid_values['pitch_p'], pid_values['pitch_i'], pid_values['pitch_d'])
    yaw_pid.tunings = (pid_values['yaw_p'], pid_values['yaw_i'], pid_values['yaw_d'])
    throttle_pid.tunings = (pid_values['throttle_p'], pid_values['throttle_i'], pid_values['throttle_d'])
    if agent1:
        value_roll = 3
        output_roll = roll_pid(value_roll)
        value_pitch = 5
        output_pitch = pitch_pid(value_pitch)
        value_yaw = 9
        output_yaw = yaw_pid(value_yaw)
        value_throttle = 7
        output_throttle = throttle_pid(value_throttle)
        print(f"{output_roll}   {output_pitch}   {output_yaw}   {output_throttle}")



client = set()
async def echo(websocket,path):
    print("Client connected...")
    client.add(websocket)
    try:
        async for commands in websocket:
            #print (commands)
            commands = json.loads(commands)
            Control(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'], commands['connect_pixhawk'])
            UtilityControl(commands['agent1'],commands['agent2'],commands['agent3'],commands['pid'])
            send = {
                "message_received":True,
                "connection_pixhawk" : indicator_pixhawk
            }
            send = str(json.dumps(send))
            #print(bytearray(send,'utf-8'))
            await websocket.send(bytearray(send,'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    finally:
        client.remove(websocket)




if __name__ == "__main__":
    try:
        print("Running...")
        start_server = websockets.serve(echo, "192.168.2.2", 55000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

      
