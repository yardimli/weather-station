import bme280
import smbus2
from time import sleep
import random

port = 1
address = 0x77  # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)

# bme280.load_calibration_params(bus, address)

# while True:
    # bme280_data = bme280.sample(bus,address)
    # humidity  = bme280_data.humidity
    # pressure  = bme280_data.pressure
    # ambient_temperature = bme280_data.temperature

    # Simulate random sensor data within plausible ranges
    # ##humidity = random.uniform(0, 100)  # Random humidity percentage between 0% and 100%
    # ##pressure = random.uniform(980, 1050)  # Random pressure in hPa between 980 and 1050
    # ##ambient_temperature = random.uniform(-10, 35)  # Random temperature in °C between -10 and 35

    # ##print(humidity, pressure, ambient_temperature)
    # ##sleep(1)
