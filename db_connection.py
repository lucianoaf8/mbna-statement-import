import os
from mysql.connector import pooling
from dotenv import load_dotenv
from urllib.parse import urlparse
import logging

# Load environment variables
load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

dbconfig = {
    "host": urlparse(MYSQL_URL).hostname,
    "port": urlparse(MYSQL_URL).port if urlparse(MYSQL_URL).port else 3306,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "database": urlparse(MYSQL_URL).path.lstrip('/')
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)

def connect_to_db():
    try:
        connection = connection_pool.get_connection()
        logging.debug("Successfully connected to the database.")
        print("Successfully connected to the database.")
        return connection
    except Exception as err:
        logging.error(f"Database connection error: {err}")
        print(f"Database connection error: {err}")
        return None
