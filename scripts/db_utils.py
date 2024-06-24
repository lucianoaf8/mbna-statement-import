# scripts/db_utils.py
import mysql.connector
from mysql.connector import Error
import os

def connect():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='mbna',
            user='root',
            password='password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def check_file_imported(connection, file_name):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS count FROM mbna_file_tracker WHERE file_name = %s", (file_name,))
    result = cursor.fetchone()
    return result['count'] > 0
