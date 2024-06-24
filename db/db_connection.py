import mysql.connector
from mysql.connector import Error
from utils.logger import get_logger

logger = get_logger(__name__)

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='mbna',
            user='yourusername',
            password='yourpassword'
        )
        if connection.is_connected():
            logger.info("Connected to MySQL database")
        return connection
    except Error as e:
        logger.error(f"Error while connecting to MySQL: {e}")
        return None
