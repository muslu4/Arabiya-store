#!/usr/bin/env python
"""
Execute SQL script to create tables
"""
import os
import psycopg2
from django.conf import settings

def execute_sql_script():
    """
    Execute SQL script to create tables
    """
    print("Executing SQL script to create tables...")

    # Get database connection details from Django settings
    db_settings = settings.DATABASES['default']

    # Path to SQL script
    sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'create_tables.sql')

    if not os.path.exists(sql_path):
        print(f"SQL script not found at {sql_path}")
        return False

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=db_settings['HOST'],
            database=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            port=db_settings.get('PORT', 5432)
        )
        cursor = conn.cursor()

        # Read SQL script
        with open(sql_path, 'r') as f:
            sql_script = f.read()

        # Execute SQL script
        cursor.execute(sql_script)

        # Commit changes
        conn.commit()
        conn.close()

        print("SQL script executed successfully!")
        return True

    except Exception as e:
        print(f"Error executing SQL script: {e}")
        return False

if __name__ == '__main__':
    # Configure Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')
    import django
    django.setup()

    execute_sql_script()
