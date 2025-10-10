# users/__init__.py
import os
from django.db import connection
from django.db.utils import ProgrammingError

def create_user_table():
    """
    Create user table if it doesn't exist
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_user (
                    id SERIAL PRIMARY KEY,
                    password VARCHAR(128) NOT NULL,
                    last_login TIMESTAMP WITH TIME ZONE,
                    is_superuser BOOLEAN NOT NULL,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
                    is_customer BOOLEAN NOT NULL,
                    is_staff_member BOOLEAN NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_customuser (
                    id SERIAL PRIMARY KEY,
                    password VARCHAR(128) NOT NULL,
                    last_login TIMESTAMP WITH TIME ZONE,
                    is_superuser BOOLEAN NOT NULL,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
                    is_customer BOOLEAN NOT NULL,
                    is_staff_member BOOLEAN NOT NULL
                )
            """)
        print("User tables created successfully!")
    except ProgrammingError as e:
        print(f"Error creating user tables: {e}")
    except Exception as e:
        print(f"Unexpected error creating user tables: {e}")

# Create tables when the app is imported
create_user_table()