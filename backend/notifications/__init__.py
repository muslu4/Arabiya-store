# notifications/__init__.py
import os
from django.db import connection
from django.db.utils import ProgrammingError

def create_notifications_tables():
    """
    Create notifications tables if they don't exist
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications_notification (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    is_read BOOLEAN NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """)
        print("Notifications tables created successfully!")
    except ProgrammingError as e:
        print(f"Error creating notifications tables: {e}")
    except Exception as e:
        print(f"Unexpected error creating notifications tables: {e}")

# Create tables when the app is imported
create_notifications_tables()