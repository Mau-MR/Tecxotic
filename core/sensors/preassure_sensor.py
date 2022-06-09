import ms5837

sensor = ms5837.MS5837_30BA()  # Default I2C bus is 1 (Raspberry Pi 3)

# We must initialize the sensor before reading it
if not sensor.init():
    print("Sensor could not be initialized")
    exit(1)


# Print readings
def read_altitude():
    if sensor.read():
        return sensor.pressure(ms5837.UNITS_psi) / 1422
    print('Some error with the preasure read')
    return 0
