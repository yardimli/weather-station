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


# host = 'admin.cjp8hsqu4je0.us-east-2.rds.amazonaws.com'
# user = 'admin'
# password = '12345678'
# database = 'admin'
# connection = pymysql.connect(host, user, password, database)

with connection:
    cur = connection.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print("Database version: {} ".format(version[0]))
