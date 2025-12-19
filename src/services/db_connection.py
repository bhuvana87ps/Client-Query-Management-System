"""
db_connection.py
--------------------------------------------------
Reusable MySQL database connection utility
for Client Query Management System (CQMS)

Tech:
- mysql-connector-python
--------------------------------------------------
"""

import mysql.connector
from mysql.connector import Error


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------
DB_CONFIG = {
    "host": "localhost", # Localhost for development
    "user": "root", # Default root user for local dev
    "password": "",   # cdefault no password for local dev
    "database": "client_query_db" # My project database name
}


# --------------------------------------------------
# GET DATABASE CONNECTION
# --------------------------------------------------
def get_db_connection(): # Returns database connection
    """
    Creates and returns a MySQL database connection.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except Error as e:
        print("❌ Database connection error:", e)
        return None


# --------------------------------------------------
# CLOSE DATABASE CONNECTION
# --------------------------------------------------
def close_db_connection(connection, cursor=None): # Closes connection and safety optional cursor

    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print("❌ Error while closing DB connection:", e)


# --------------------------------------------------
# TEST CONNECTION (OPTIONAL)
# --------------------------------------------------
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("✅ Database connection successful!")
        close_db_connection(conn)
