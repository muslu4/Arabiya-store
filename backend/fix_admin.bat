@echo off
chcp 65001 >nul
echo 🔧 Fixing admin login issue...

REM Activate virtual environment
call env\Scripts\activate

REM Run the fix script
echo 👤 Creating admin user...
python fix_admin.py

echo.
echo ✅ Issue fixed successfully!
echo.
echo 🔑 Login details:
echo    📱 Phone: admin
echo    🔑 Password: admin123
echo.
echo 🌐 Admin panel: http://localhost:8000/admin
echo.
pause
