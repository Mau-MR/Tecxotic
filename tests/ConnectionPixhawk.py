import sys

from pymavlink import mavutil


# class pixhawk to handle ROV movement and communication
class Pixhawk:
    def __init__(self, direction='COM7'):
        self.px_conn = mavutil.mavlink_connection(direction)
        self.px_conn.wait_heartbeat()
        self.arm_disarm()
        print(self.get_msg('SYS_STATUS'))
        px.change_mode('STABILIZE')

    def get_msg(self, command):
        msg = self.px_conn.recv_match(type=command, blocking=True)
        if not msg:
            return
        if msg.get_type() == "BAD_DATA":
            print('Error receiving %s' % command)
            return;
        return msg.to_dict()

    def arm_disarm(self):
        if self.px_conn.motors_armed():
            self.px_conn.arducopter_disarm()
            self.px_conn.motors_disarmed_wait()
            print("Motors disarmed successfully")
        else:
            self.px_conn.arducopter_arm()
            self.px_conn.motors_armed_wait()
            print("Motors armed successfully")

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


    # Print all the received packages from the pix
    def test_msg_reception(self):
        while True:
            try:
                print(self.px_conn.recv_match().to_dict())
            except:
                pass


def test_imu(px):
    while True:
        dict = px.get_msg('AHRS2')
        print(dict['roll'], dict['pitch'], dict['yaw'])
def test_arm_disarm(px):
     px.arm_disarm()
     px.arm_disarm()



if __name__ == "__main__":
    px = Pixhawk()