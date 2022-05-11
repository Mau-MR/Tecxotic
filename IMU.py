# INTERFACE OF MPU9250 WITH RASPEBERRY PI
# https://medium.com/@niru5/hands-on-with-rpi-and-mpu9250-part-3-232378fa6dbc
# https://www.luisllamas.es/medir-la-inclinacion-imu-arduino-filtro-complementario/

# Before we run the code we need to enable I2C communications on rpi and install smbus library

import os
import sys
import time
import smbus
import numpy as np #

from imusensor.MPU9250 import MPU9250

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
imu.caliberateAccelerometer() #
print ("Acceleration calib successful") #
imu.caliberateMag() #
print ("Mag calib successful") #

accelscale = imu.Accels #
accelBias = imu.AccelBias #
gyroBias = imu.GyroBias #
mags = imu.Mags  #
magBias = imu.MagBias #

imu.saveCalibDataToFile("/home/pi/MPU9250-rpi/data/calib.json") #
print ("calib data saved") #

imu.loadCalibDataFromFile("/home/pi/MPU9250-rpi/data/calib.json") #

if np.array_equal(accelscale, imu.Accels) & np.array_equal(accelBias, imu.AccelBias) & \ #
    np.array_equal(mags, imu.Mags) & np.array_equal(magBias, imu.MagBias) & \ #
    np.array_equal(gyroBias, imu.GyroBias): #
    print ("calib loaded properly") #


while True:
    imu.readSensor()
    imu.computeOrientation()

    print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
    print ("Gyro x: {0} ; Gyro y : {1} ; Gyro z : {2}".format(imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2]))
    print ("Mag x: {0} ; Mag y : {1} ; Mag z : {2}".format(imu.MagVals[0], imu.MagVals[1], imu.MagVals[2]))
    print ("roll: {0} ; pitch : {1} ; yaw : {2}".format(imu.roll, imu.pitch, imu.yaw))
    time.sleep(0.1)