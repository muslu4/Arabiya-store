@echo off
echo ========================================
echo Running Migrations on Render Database
echo ========================================
echo.

cd backend

set DATABASE_URL=postgresql://ecom_postgres_db_za4r_user:elNITLRgmSTvJ2mZG3MG3YcDkqD1q51E@dpg-d3khj849c44c73agblb0-a/ecom_postgres_db_za4r

echo Installing psycopg2 if needed...
pip install psycopg2-binary

echo.
echo Running migrations...
python manage.py migrate --noinput

echo.
echo Creating superuser...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('01234567890', password='admin123', first_name='Admin', last_name='User') if not User.objects.filter(phone='01234567890').exists() else print('Superuser already exists')"

echo.
echo Creating coupons...
python create_coupons.py

echo.
echo ========================================
echo Done!
echo ========================================
pause