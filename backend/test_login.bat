@echo off
echo ============================================================
echo Testing Admin Login Fix
echo ============================================================
echo.

echo Running system check...
python manage.py check
echo.

echo ============================================================
echo Starting Django development server...
echo ============================================================
echo.
echo Once the server starts, open your browser and go to:
echo http://127.0.0.1:8000/admin/
echo.
echo Login credentials:
echo   Username: admin (or phone: 01234567890)
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python manage.py runserver