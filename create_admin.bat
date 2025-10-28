@echo off
chcp 65001 >nul
echo 👤 إنشاء المستخدم الإداري لـ العربية فون...

REM Activate virtual environment
call backend\env\Scripts\activate

REM Create admin user
python create_admin_user.py

echo.
echo ✅ تم الانتهاء!
pause