from PID import PID
import Agent1
import json
from Constants import *
roll_pid = PID(0, 0, 0, setpoint=0)
roll_pid.output_limits = (-1000,1000)
pitch_pid = PID(0, 0, 0, setpoint=0)
pitch_pid.output_limits = (-1000,1000)
yaw_pid = PID(0, 0, 0, setpoint=0)
yaw_pid.output_limits = (-1000,1000)
throttle_pid = PID(0, 0, 0, setpoint=0)
throttle_pid.output_limit = (0,1000)


        
def run():
    values_roll_json = open(JSON_ROLL_FILE, "r")
    values_pitch_json = open(JSON_PITCH_FILE, "r")
    values_yaw_json = open(JSON_YAW_FILE, "r")
    values_throttle_json = open(JSON_THROTTLE_FILE, "r")
    try:
        valuer = json.loads(values_roll_json.read())
        valuep = json.loads(values_pitch_json.read())
        valuey = json.loads(values_yaw_json.read())
        valuet = json.loads(values_throttle_json.read())
        roll_pid.tunings = (valuer['p'], valuer['i'],valuer['d'])
        pitch_pid.tunings = (valuep['p'], valuep['i'], valuep['d'])
        yaw_pid.tunings = (valuey['p'], valuey['i'], valuey['d'])
        throttle_pid.tunings = (valuet['p'], valuet['i'], valuet['d'])
        
        roll_diff, throttle_diff, target_square = Agent1.run()
        
        output_roll = roll_pid(roll_diff)
        value_pitch = 0
        output_pitch = pitch_pid(value_pitch)
        value_yaw = 0
        output_yaw = yaw_pid(value_yaw)
        output_throttle = throttle_pid(throttle_diff)
        return output_roll, output_pitch, output_yaw, output_throttle, target_square
    except Exception as e:
        print(e)
        values_roll_json.close()
        values_pitch_json.close()
        values_yaw_json.close()
        values_throttle_json.close()
        return -1,-1,-1,-1, -1
        
if __name__ == "__main__":
    from Constants import *
    import CamServer
    import cv2
    CamServer.run()
    while True:
        print(run())














