"""
auth_utils.py
--------------------------------------------------
Authentication utility functions for
Client Query Management System (CQMS)

Features:
- Password hashing (SHA-256)
- Register user
- Login using username OR email OR mobile number
- Role-based validation

Tech:
- Python
- hashlib
- mysql-connector-python
--------------------------------------------------
"""

import hashlib
from services.db_connection import get_db_connection, close_db_connection


# --------------------------------------------------
# PASSWORD HASHING
# --------------------------------------------------
def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using SHA-256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# --------------------------------------------------
# REGISTER USER
# --------------------------------------------------
def register_user(username, email, mobile, password, role):
    """
    Registers a new user (Client or Support).
    Returns (success, message).
    """
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed."

    cursor = conn.cursor()

    try:
        hashed_pwd = hash_password(password)

        query = """
            INSERT INTO users
            (username, email, mobile_number, hashed_password, role)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (username, email, mobile, hashed_pwd, role))
        conn.commit()
        return True, "User registered successfully."

    except Exception as e:
        return False, str(e)

    finally:
        close_db_connection(conn, cursor)


# --------------------------------------------------
# LOGIN USER
# --------------------------------------------------
def login_user(identifier, password, role):
    """
    Logs in user using:
    - Username OR
    - Email OR
    - Mobile number

    Role must match (Client / Support).
    Returns (success, user_data or error_message).
    """
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed."

    cursor = conn.cursor(dictionary=True)

    try:
        hashed_pwd = hash_password(password)

        query = """
            SELECT user_id, username, email, mobile_number, role
            FROM users
            WHERE (username = %s OR email = %s OR mobile_number = %s)
              AND hashed_password = %s
              AND role = %s
        """

        cursor.execute(query, (
            identifier,
            identifier,
            identifier,
            hashed_pwd,
            role
        ))

        user = cursor.fetchone()

        if user:
            return True, user
        else:
            return False, "Invalid credentials."

    except Exception as e:
        return False, str(e)

    finally:
        close_db_connection(conn, cursor)
