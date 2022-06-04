# INTERFACE OF MPU9250 WITH RASPEBERRY PI
# https://medium.com/@niru5/hands-on-with-rpi-and-mpu9250-part-3-232378fa6dbc
# https://www.luisllamas.es/medir-la-inclinacion-imu-arduino-filtro-complementario/

import time
import smbus

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman

# initializing publisher
kalman_filter = kalman.Kalman()
address = 0x68
bus = smbus.SMBus(0)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
imu.caliberateAccelerometer()
print("Acceleration calib successful")
imu.caliberateMag()
print("Mag calib successful")

imu.readSensor()
imu.computeOrientation()
kalman_filter.roll = imu.roll
kalman_filter.pitch = imu.pitch
kalman_filter.yaw = imu.yaw

currTime = time.time()
kal_currTime = time.time()
imu.readSensor()
kal_currTime = time.time()


def read_IMU():
    global kal_currTime

    imu.readSensor()
    imu.computeOrientation()

    kal_newTime = time.time()
    kal_dt = kal_newTime - kal_currTime
    kal_currTime = kal_newTime

    kalman_filter.computeAndUpdateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0],
                                               imu.GyroVals[1], imu.GyroVals[2],
                                               imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], kal_dt)

    calibkalman = {
        'roll': kalman_filter.roll,
        'pitch': kalman_filter.pitch,
        'yaw': kalman_filter.yaw,
    }

    return calibkalman
