#!/bin/bash

# Get database connection details from environment variables
DB_HOST=${DB_HOST:-localhost}
DB_NAME=${DB_NAME:-ecom_db}
DB_USER=${DB_USER:-ecom_user}
DB_PASSWORD=${DB_PASSWORD:-password}
DB_PORT=${DB_PORT:-5432}

# Path to SQL script
SQL_PATH="$(dirname "$0")/create_tables.sql"

echo "Creating tables in database..."

# Execute SQL script
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $SQL_PATH

if [ $? -eq 0 ]; then
    echo "Tables created successfully!"
else
    echo "Error creating tables!"
    exit 1
fi
