# test_app/__init__.py
import os
from django.db import connection
from django.db.utils import ProgrammingError

def create_test_app_tables():
    """
    Create test_app tables if they don't exist
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_app_testmodel (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """)
        print("Test_app tables created successfully!")
    except ProgrammingError as e:
        print(f"Error creating test_app tables: {e}")
    except Exception as e:
        print(f"Unexpected error creating test_app tables: {e}")

# Create tables when the app is imported
create_test_app_tables()