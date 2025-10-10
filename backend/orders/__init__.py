# orders/__init__.py
import os
from django.db import connection
from django.db.utils import ProgrammingError

def create_orders_tables():
    """
    Create orders tables if they don't exist
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders_order (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders_orderitem (
                    id SERIAL PRIMARY KEY,
                    order_id INTEGER NOT NULL REFERENCES orders_order(id),
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    price DECIMAL(10, 2) NOT NULL
                )
            """)
        print("Orders tables created successfully!")
    except ProgrammingError as e:
        print(f"Error creating orders tables: {e}")
    except Exception as e:
        print(f"Unexpected error creating orders tables: {e}")

# Create tables when the app is imported
create_orders_tables()