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
                    email VARCHAR(254),
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
                    is_customer BOOLEAN NOT NULL,
                    is_staff_member BOOLEAN NOT NULL,
                    phone VARCHAR(20) UNIQUE,
                    address TEXT
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
                    email VARCHAR(254),
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
                    is_customer BOOLEAN NOT NULL,
                    is_staff_member BOOLEAN NOT NULL,
                    phone VARCHAR(20) UNIQUE,
                    address TEXT
                )
            """)
        print("User tables created successfully!")
    except ProgrammingError as e:
        print(f"Error creating user tables: {e}")
    except Exception as e:
        print(f"Unexpected error creating user tables: {e}")

# تحديث الجداول لإضافة الأعمدة المفقودة
def update_user_tables():
    """
    Update user tables to add missing columns
    """
    try:
        with connection.cursor() as cursor:
            # قراءة ملف SQL
            sql_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'update_tables.sql')
            if os.path.exists(sql_path):
                with open(sql_path, 'r') as f:
                    sql_commands = f.read()

                # تنفيذ أوامر SQL
                cursor.execute(sql_commands)

            print("User tables updated successfully!")
    except ProgrammingError as e:
        print(f"Error updating user tables: {e}")
    except Exception as e:
        print(f"Unexpected error updating user tables: {e}")

# Create and update tables when the app is imported
create_user_table()
update_user_tables()