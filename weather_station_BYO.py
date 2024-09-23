from gpiozero import Button
import time
import math
import bme280_sensor
import wind_direction_byo
import statistics
import ds18b20_therm
import random
import os
import json

import database

wind_count = 0  # Counts how many half-rotations
radius_cm = 9.0  # Radius of your anemometer
wind_interval = 5  # How often (secs) to sample speed
interval = 5  # measurements recorded every 5 minutes
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
ADJUSTMENT = 1.18
BUCKET_SIZE = 0.2794
gust = 0
store_speeds = []
store_directions = []

credentials_file = os.path.join(os.path.dirname(__file__), "weather-config.json")
f = open(credentials_file, "r")
credentials = json.load(f)
f.close()

# Remove whitespace from strings in credentials
for key, value in credentials.items():
    if isinstance(value, str):
        credentials[key] = value.strip()

number_of_readings_to_take = credentials['READINGS_EACH_RUN']
use_real_data = credentials.get('USE_REAL_DATA', False)

readings_counter = 0

# Every half-rotation, add 1 to count
def spin():
    global wind_count
    wind_count = wind_count + 1
    # print( wind_count )


def calculate_speed(time_sec):
    global wind_count
    global gust
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    # Calculate distance travelled by a cup in km
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM

    # Speed = distance / time
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR

    # Calculate speed
    final_speed = km_per_hour * ADJUSTMENT

    return final_speed

def reset_wind():
    global wind_count
    wind_count = 0


def reset_gust():
    global gust
    gust = 0


def simulate_wind():
    global wind_count
    wind_count += random.randint(1, 15)

print('begin')

if use_real_data:
    wind_speed_sensor = Button(5)
    wind_speed_sensor.when_activated = spin
    temp_probe = ds18b20_therm.DS18B20()

db = database.weather_database()

while readings_counter < number_of_readings_to_take:

    readings_counter += 1

    start_time = time.time()
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()

        if use_real_data:
            time.sleep(wind_interval)
        else:
            simulate_wind()
            time.sleep(wind_interval)


        # time.sleep(wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            if use_real_data:
                store_directions.append(wind_direction_byo.get_value())
            else:
                store_directions.append(random.uniform(0, 360))

        final_speed = calculate_speed(wind_interval)  # Add this speed to the list
        store_speeds.append(final_speed)

    wind_average = wind_direction_byo.get_average(store_directions)
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)

    store_speeds = []
    store_directions = []
    rainfall = 0

    if use_real_data:
        try:
            ground_temp = temp_probe.read_temp()
            humidity, pressure, ambient_temp = bme280_sensor.read_all()
        except Exception as e:
            print(f"Error reading sensors: {e}")
            ground_temp = 0
            humidity = 0
            pressure = 1000
            ambient_temp = 0
    else:
        # Use random data
        humidity = random.uniform(0, 100)
        pressure = random.uniform(980, 1050)
        ambient_temp = random.uniform(-10, 35)
        ground_temp = random.uniform(-10, 35)

    print('Wind Dir:', round(wind_average, 1), 'Wind Speed:', round(wind_speed, 1), 'Wind Gust:', round(wind_gust, 1),
          'Humidity:', round(humidity, 1), 'Pressure:', round(pressure, 1),
          'Ambient Temp:', round(ambient_temp, 1), 'Ground Temp:', round(ground_temp, 1))

    db.insert(ambient_temp, ground_temp, 0, pressure, humidity, wind_average, wind_speed, wind_gust, rainfall)
