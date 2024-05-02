import json
import pymysql

with open('rds-config.json') as config_file:
    config = json.load(config_file)

connection = pymysql.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database']
)

insert_template = "INSERT INTO WEATHER_MEASUREMENT (AMBIENT_TEMPERATURE, GROUND_TEMPERATURE, AIR_QUALITY, AIR_PRESSURE, HUMIDITY, WIND_DIRECTION, WIND_SPEED, WIND_GUST_SPEED, RAINFALL, CREATED) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
update_template = "UPDATE WEATHER_MEASUREMENT SET REMOTE_ID=%s WHERE ID=%s;"
upload_select_template = "SELECT * FROM WEATHER_MEASUREMENT WHERE REMOTE_ID IS NULL;"


def insert(self, ambient_temperature, ground_temperature, air_quality, air_pressure, humidity, wind_direction,
           wind_speed, wind_gust_speed, rainfall, created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    params = (ambient_temperature,
              ground_temperature,
              air_quality,
              air_pressure,
              humidity,
              wind_direction,
              wind_speed,
              wind_gust_speed,
              rainfall,
              created)
    print(self.insert_template % params)
    self.db.execute(self.insert_template, params)


with connection:
    cur = connection.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print("Database version: {} ".format(version[0]))

