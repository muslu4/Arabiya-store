# products/__init__.py
import os
from django.db import connection
from django.db.utils import ProgrammingError

def create_products_tables():
    """
    Create products tables if they don't exist
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products_category (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    image VARCHAR(200),
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products_product (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL,
                    category_id INTEGER NOT NULL REFERENCES products_category(id),
                    image VARCHAR(200),
                    stock INTEGER NOT NULL,
                    is_available BOOLEAN NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """)
        print("Products tables created successfully!")
    except ProgrammingError as e:
        print(f"Error creating products tables: {e}")
    except Exception as e:
        print(f"Unexpected error creating products tables: {e}")

# Create tables when the app is imported
create_products_tables()
