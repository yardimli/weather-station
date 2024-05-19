#!/usr/bin/python3
import MySQLdb, datetime, http.client, json, os
import io


class mysql_database:
    def __init__(self):
        credentials_file = os.path.join(os.path.dirname(__file__), "weather-config.json")
        f = open(credentials_file, "r")
        credentials = json.load(f)
        f.close()
        for key, value in credentials.items():  # remove whitespace
            credentials[key] = value.strip()
            print(key)
            print(value)

        self.connection = MySQLdb.connect(user=credentials["USERNAME"], password=credentials["PASSWORD"],
                                          database=credentials["DATABASE"])
        self.cursor = self.connection.cursor()

    def execute(self, query, params=[]):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


class weather_database:
    def __init__(self):
        self.db = mysql_database()
        self.insert_template = "INSERT INTO WEATHER_MEASUREMENT (AMBIENT_TEMPERATURE, GROUND_TEMPERATURE, AIR_QUALITY, AIR_PRESSURE, HUMIDITY, WIND_DIRECTION, WIND_SPEED, WIND_GUST_SPEED, RAINFALL, CREATED) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.update_template = "UPDATE WEATHER_MEASUREMENT SET REMOTE_ID=%s WHERE ID=%s;"
        self.upload_select_template = "SELECT * FROM WEATHER_MEASUREMENT WHERE REMOTE_ID IS NULL;"

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_none(self, val):
        return val if val != None else "NULL"

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

    def upload(self):
        # Endpoint of the PHP script
        credentials_file = os.path.join(os.path.dirname(__file__), "weather-config.json")
        f = open(credentials_file, "r")
        credentials = json.load(f)
        f.close()
        for key, value in credentials.items():  # remove whitespace
            credentials[key] = value.strip()

        php_endpoint = 'http://yourserver.com/path_to_your_php_script.php'

        results = self.db.query(self.upload_select_template)
        rows_count = len(results)
        if rows_count > 0:
            print("%d rows to send..." % rows_count)
            for row in results:
                data = {
                    "id": row["ID"],
                    "ambient_temperature": row["AMBIENT_TEMPERATURE"],
                    "ground_temperature": row["GROUND_TEMPERATURE"],
                    "air_quality": row["AIR_QUALITY"],
                    "air_pressure": row["AIR_PRESSURE"],
                    "humidity": row["HUMIDITY"],
                    "wind_direction": row["WIND_DIRECTION"],
                    "wind_speed": row["WIND_SPEED"],
                    "wind_gust_speed": row["WIND_GUST_SPEED"],
                    "rainfall": row["RAINFALL"],
                    "created": row["CREATED"].strftime("%Y-%m-%dT%H:%M:%S")
                }

                try:
                    response = requests.post(php_endpoint, data=data)
                    response_data = response.json()  # Assuming your PHP script returns JSON

                    if response.status_code == 200 and response_data.get('save_id') is not None:
                        local_id = str(row["ID"])
                        response_data_id = response_data['save_id']
                        self.db.execute(self.update_template, (response_data_id, local_id))
                        print("ID: %s updated with REMOTE_ID = %s" % (local_id, response_data_id))
                    else:
                        print("Bad response from Server: ", response_data)

                except Exception as e:
                    print("Error during HTTP request: ", e)
        else:
            print("Nothing to upload")
