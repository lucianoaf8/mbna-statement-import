import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from utils.logger import get_logger

logger = get_logger(__name__)

# Load environment variables from .env file
load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Set up logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

dbconfig = {
    "host": urlparse(MYSQL_URL).hostname,
    "port": urlparse(MYSQL_URL).port if urlparse(MYSQL_URL).port else 3306,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "database": urlparse(MYSQL_URL).path.lstrip('/')
}

def create_connection():
    try:
        connection = mysql.connector.connect(**dbconfig)
        if connection.is_connected():
            logger.info("Connected to MySQL database")
        return connection
    except Error as e:
        logger.error(f"Error while connecting to MySQL: {e}")
        return None
