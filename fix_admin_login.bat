@echo off
chcp 65001 >nul
echo 🔧 حل مشكلة تسجيل الدخول للمشرف...

REM Activate virtual environment
call backend\env\Scripts\activate

REM Create/Update admin user
echo 👤 إنشاء/تحديث المستخدم الإداري...
python create_admin_user.py

echo.
echo ✅ تم حل المشكلة!
echo.
echo 🔑 بيانات الدخول:
echo    📱 الهاتف: admin
echo    🔑 كلمة المرور: admin123
echo.
echo 🌐 لوحة الإدارة: http://localhost:8000/admin
echo.
pause