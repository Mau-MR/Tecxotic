import sys
import time

from pymavlink import mavutil


# class pixhawk to handle ROV movement and communication
class Pixhawk:
    def __init__(self, direction='COM3', mode='MANUAL'):
        try:
            self.px_conn = mavutil.mavlink_connection(direction)
        except Exception as e:
            print("Error in ConnectionPixhawk.py:", "Could not connect to:", direction)
            sys.exit(1)
        self.px_conn.wait_heartbeat()
        self.boot_time = time.time()
        self.is_armed = False
        self.mode = mode
        self.disarm()
        self.change_mode(mode)
        print(self.get_msg('SYS_STATUS'))

    def get_pix_info(self):
        return {
            "is_armed":  self.is_armed,
            "mode": self.mode
        }

    def get_msg(self, command, timeout = 0.1):
        msg = self.px_conn.recv_match(type=command, blocking=True, timeout=timeout)
        if not msg:
            return
        if msg.get_type() == "BAD_DATA":
            print('Error receiving %s' % command)
            return
        return msg.to_dict()

    def arm(self):
        print("Arming motors")
        self.px_conn.arducopter_arm()
        self.px_conn.motors_armed_wait()
        self.is_armed = True
        print("Motors armed successfully")

    def disarm(self):
        print("Disarming motors")
        self.px_conn.arducopter_disarm()
        self.px_conn.motors_disarmed_wait()
        self.is_armed = False
        print("Motors disarmed successfully")

    def arm_disarm(self):
        if self.px_conn.motors_armed():
            self.disarm()
        else:
            self.arm()


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
        # TODO: HANDLE THE VERIFICATION OF THE MODE
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




if __name__ == "__main__":
    px = Pixhawk()