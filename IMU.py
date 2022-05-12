# INTERFACE OF MPU9250 WITH RASPEBERRY PI
# https://medium.com/@niru5/hands-on-with-rpi-and-mpu9250-part-3-232378fa6dbc
# https://www.luisllamas.es/medir-la-inclinacion-imu-arduino-filtro-complementario/

# Before we run the code we need to enable I2C communications on rpi and install smbus library

import os
import sys
import time
import smbus
import numpy as np
import zmq

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman

# initializing publisher
host = 'ip of rpi'
port = 8358
url = 'tcp://'+host+':'+str(port)
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(url)

kalman_filter = kalman.Kalman()

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

imu.calib()
print ("Calibration json saved.")

imu.loadCalibDataFromFile("place_your_calib_file_here.json")

imu.readSensor()
imu.computeOrientation()
kalman_filter.roll = imu.roll
kalman_filter.pitch = imu.pitch
kalman_filter.yaw = imu.yaw

print_count = 0
sensor_count = 0
currTime = time.time()
kal_currTime = time.time()
imu.readSensor()
while True:

    imu.readSensor()
    imu.computeOrientation()

    kal_newTime = time.time()
    kal_dt = kal_newTime - kal_currTime
    kal_currTime = kal_newTime

    kalman_filter.computeAndUpdateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2],\
                                                imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], kal_dt)

    if print_count == 5:
        print ("roll: {0} ; pitch : {1} ; yaw : {2}".format(imu.roll, imu.pitch, imu.yaw))
        print("Kalmanroll:{0} KalmanPitch:{1} KalmanYaw:{2} ".format(kalman_filter.roll, kalman_filter.pitch, kalman_filter.yaw))

        md = dict(topic = 'orientation', normal = str([imu.roll, imu.pitch, imu.yaw]), kalman = str([kalman_filter.roll, kalman_filter.pitch, kalman_filter.yaw]))
        socket.send_json(md)
        print_count = 0

    print_count = print_count + 1
    sensor_count = sensor_count + 1
    time.sleep(0.001)

'''

import os
import sys
import time
import smbus
import numpy as np
import zmq

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman


# initializing publisher
host = 'ip of rpi'
port = 8358
url = 'tcp://'+host+':'+str(port)
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(url)

kalman_filter = kalman.Kalman()

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)

imu.begin()
imu.caliberateAccelerometer()
print ("Acceleration calib successful")
imu.caliberateMag()
print ("Mag calib successful")

accelscale = imu.Accels
accelBias = imu.AccelBias
gyroBias = imu.GyroBias
mags = imu.Mags 
magBias = imu.MagBias

imu.saveCalibDataToFile("/home/pi/MPU9250-rpi/data/calib.json")
print ("calib data saved")

imu.loadCalibDataFromFile("/home/pi/MPU9250-rpi/data/calib.json")
if np.array_equal(accelscale, imu.Accels) & np.array_equal(accelBias, imu.AccelBias) & \
    np.array_equal(mags, imu.Mags) & np.array_equal(magBias, imu.MagBias) & \
    np.array_equal(gyroBias, imu.GyroBias):
    print ("calib loaded properly")
'''


'''
ONCE WE HAVE THE VALUES
import time
import smbus

from imusensor.MPU9250 import MPU9250

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
# imu.caliberateGyro()
# imu.caliberateAccelerometer()
# or load your own caliberation file
imu.loadCalibDataFromFile("/your_path/calib.json")

while True:
    imu.readSensor()
    imu.computeOrientation()

    print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
        print ("roll: {0} ; pitch : {1} ; yaw : {2}".format(imu.roll, imu.pitch, imu.yaw))
    time.sleep(0.1)

'''
