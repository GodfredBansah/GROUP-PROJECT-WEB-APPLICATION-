import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='flask_auth',
            user='root',
            password='Godfred12345',  # Set your MySQL password here 
            port=3306
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def init_db():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS flask_auth")
            cursor.execute("USE flask_auth")
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
            connection.commit()
            print("Database and table initialized successfully")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def register_user(username, email, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Switch to the correct database
            cursor.execute("USE flask_auth")
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "Email already registered"
            
            # Hash password and insert user
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            connection.commit()
            return True, "Registration successful"
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return False, "Database connection failed"

def check_user(email, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # Switch to the correct database
            cursor.execute("USE flask_auth")
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                return True, user
            return False, "Invalid email or password"
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return False, "Database connection failed"