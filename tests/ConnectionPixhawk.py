import time

from pymavlink import mavutil


# class pixhawk to handle ROV movement and communication
class Pixhawk:
    def __init__(self, direction='COM7'):
        self.px_conn = mavutil.mavlink_connection(direction)
        self.px_conn.wait_heartbeat()
        print(self.get_msg('SYS_STATUS'))

    def get_msg(self, command):
        msg = self.px_conn.recv_match(type=command, blocking=True)
        if not msg:
            return
        if msg.get_type() == "BAD_DATA":
            print('Error receiving %s' % command)
            return;
        return msg.to_dict()

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


if __name__ == "__main__":
    px = Pixhawk()
    test_imu(px)
