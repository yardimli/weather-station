# Raspberry Pi PHP Server Weather Station

## Installation

Follow the guides and tutorials at [https://github.com/raspberrypilearning/weather\_station\_guide](https://github.com/raspberrypilearning/weather_station_guide) (published at [www.raspberrypi.org/weather-station](https://www.raspberrypi.org/weather-station/))

## Version

This repo contains the updated version of the software, re-engineered for the [Stretch version of Raspbian](https://www.raspberrypi.org/blog/raspbian-stretch/). If you are an existing Weather Station owner and are using a Pi running the Jessie version of Raspbian, then this code will not work without modification. You should flash your SD card with the [latest Raspbian image](https://www.raspberrypi.org/downloads/raspbian/) and perform a fresh install of this software (you may wish to take a copy of your local MYSQL database first).

----------

## The Reporting is Done to a LAMP server

### Screenshots

![Simple View](https://github.com/yardimli/weather-station/blob/main/images/logo.jpg?raw=true)


## Installation

use putty ssh to user@raspberrypi.local

or hover over wifi on raspberry pi desktop to see ip address

if (forgot username and password when creating the sd card)
can find username from terminal on the pi
can set password from the config utility again

### Install the software

```bash
git clone https://github.com/yardimli/weather-station.git

sudo pip3 install RPi.bme280 --break-system-packages
# need to add the extra parameter  --break-system-packages

sudo apt-get install -y mariadb-server mariadb-client libmariadbclient-dev
# if the above fails use
sudo apt-get install -y mariadb-server mariadb-client libmariadb-dev

sudo pip3 install mysqlclient --break-system-packages
```

#### enable i2c from pi desktop config

quick test with random data
```bash
python bme280_sensor.py

# then open config.txt
sudo nano /boot/firmware/config.txt
# and add
dtoverlay=w1-gpio
# bellow the line with
dtparam=audio=on

sudo nano /etc/modules
# at the bottom add:
w1-gpio
w1-therm

# reboot the pi
# after reboot test

python ds18b20_therm.py
# and
python wind.py

# use rasberry pi config utility and make sure
spi, i2c and 1-wire 
# are enabled

# create the database
sudo mysql
create user pi IDENTIFIED by 'my_weather_station_123';
grant all privileges on *.* to 'pi' with grant option;
create database weather;
use weather;

# run the create.sql file or create the table manually
CREATE TABLE WEATHER_MEASUREMENT(
ID BIGINT NOT NULL AUTO_INCREMENT,
REMOTE_ID BIGINT,
AMBIENT_TEMPERATURE DECIMAL(6,2) NOT NULL,
GROUND_TEMPERATURE DECIMAL(6,2) NOT NULL,
AIR_QUALITY DECIMAL(6,2) NOT NULL,
AIR_PRESSURE DECIMAL(6,2) NOT NULL,
HUMIDITY DECIMAL(6,2) NOT NULL,
WIND_DIRECTION DECIMAL(6,2) NULL,
WIND_SPEED DECIMAL(6,2) NOT NULL,
WIND_GUST_SPEED DECIMAL(6,2) NOT NULL,
RAINFALL DECIMAL (6,2) NOT NULL,
CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY ( ID )
);

# exit mysql with Ctrl-D

# lest test the full weather station
python weather_station_BYO.py

# ...run for a while and then check the database

sudo mysql
use weather;
select count(*) from WEATHER_MEASUREMENT;
select * from WEATHER_MEASUREMENT;

# --------------------------------------------------
# use SSH to connect to the EC2 instance
# or can also use phpmyadmin from the browser

# RUN the create.sql file on the REMOTE servers database

# in the /var/www/weather-station folder
# edit config.php file
# and add the database credentials

# On the Raspberry Pi add cronjob to get the data and another to upload data to the remote server

0 */2 * * * ~/weather-station/python weather_station_BYO.py
0 */5 * * * ~/weather-station/upload_to_php.py
