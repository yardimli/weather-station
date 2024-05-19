#!/usr/bin/python3
import os
import sys
import logging
from pathlib import Path

# Insert the path to the weather_station directory to the system path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from database import weather_database  # Import the class from your database.py file

# Configure logging
logging.basicConfig(filename='upload_to_php.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Instantiate your weather_database class
        weather_db = weather_database()

        # Perform the upload
        weather_db.upload()

        # Log success
        logging.info('Weather data upload successfully completed.')

    except Exception as e:
        # Log any errors
        logging.error('Error during weather data upload: %s', str(e))


if __name__ == "__main__":
    main()