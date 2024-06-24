# scripts/db_utils.py
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Set up logging for db_utils.py
log_file = 'logs/db_utils.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

dbconfig = {
    "host": urlparse(MYSQL_URL).hostname,
    "port": urlparse(MYSQL_URL).port if urlparse(MYSQL_URL).port else 3306,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "database": urlparse(MYSQL_URL).path.lstrip('/')
}

def connect():
    try:
        connection = mysql.connector.connect(**dbconfig)
        if connection.is_connected():
            logging.info("Database connection successful.")
            return connection
    except Error as e:
        logging.error(f"Error while connecting to MySQL: {e}")
        return None

def check_file_imported(connection, file_name):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS count FROM mbna_file_tracker WHERE file_name = %s", (file_name,))
    result = cursor.fetchone()
    return result['count'] > 0
