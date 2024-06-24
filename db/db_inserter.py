from db.db_connection import create_connection
from utils.logger import get_logger

logger = get_logger(__name__)

def insert_data(query, data):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.executemany(query, data)
            connection.commit()
            logger.info(f"Inserted {cursor.rowcount} records into the database")
        except mysql.connector.Error as error:
            logger.error(f"Failed to insert record into table: {error}")
        finally:
            cursor.close()
            connection.close()
