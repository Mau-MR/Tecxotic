import sys
import time

from pymavlink import mavutil


# class pixhawk to handle ROV movement and communication
class Pixhawk:
    def __init__(self, direction='COM3'):
        self.px_conn = mavutil.mavlink_connection(direction)
        self.px_conn.wait_heartbeat()
        self.boot_time = time.time()
        self.disarm()
        self.change_mode('STABILIZE')
        print(self.get_msg('SYS_STATUS'))

    def get_msg(self, command):
        msg = self.px_conn.recv_match(type=command, blocking=True, timeout=1)
        if not msg:
            return
        if msg.get_type() == "BAD_DATA":
            print('Error receiving %s' % command)
            return;
        return msg.to_dict()

    def arm(self):
        self.px_conn.arducopter_arm()
        self.px_conn.motors_armed_wait()
        print("Motors armed successfully")

    def disarm(self):
        self.px_conn.arducopter_disarm()
        self.px_conn.motors_disarmed_wait()
        print("Motors disarmed successfully")


    def change_mode(self, mode):
        current_mode = self.px_conn.flightmode
        print("Changing mode from", current_mode, "to", mode)
        if mode not in self.px_conn.mode_mapping():
            print('Unknown mode : {}'.format(mode))
            print('Try:', list(self.px_conn.mode_mapping().keys()))
            sys.exit(1)
        mode_id = self.px_conn.mode_mapping()[mode]
        self.px_conn.mav.set_mode_send(
            self.px_conn.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id
        )
        while self.px_conn.flightmode != mode:
            print('Waiting to change mode')
        print("Got mode:", mode)

    def drive_manual(self, roll, pitch, yaw, throttle, buttons = 0):
        self.px_conn.mav.manual_control_send(
            self.px_conn.target_system,
            pitch,  # -1000 to 1000
            roll,  # -1000 to 1000
            throttle,  # 0 to 1000  ==  500 means neutral throttle
            yaw,  # -1000 to 1000
            buttons
        )

    def rc_verification(self):
        #TODO
        rc = self.get_msg('RC_CHANNELS')





def test_imu(px):
    while True:
        dict = px.get_msg('AHRS2')
        print(dict['roll'], dict['pitch'], dict['yaw'])



if __name__ == "__main__":
    px = Pixhawk()
    test_imu(px)