@echo off
chcp 65001 >nul
echo 🔧 إصلاح مشكلة تسجيل الدخول للمدير...

REM Activate virtual environment
call backend\env\Scripts\activate

REM Create/fix admin user
echo 👤 إنشاء المستخدم الإداري...
python create_admin_simple.py

echo.
echo ✅ تم إصلاح المشكلة بنجاح!
echo.
echo 🔑 بيانات تسجيل الدخول:
echo    📱 الهاتف: admin
echo    🔑 كلمة المرور: admin123
echo.
echo 🌐 لوحة الإدارة: http://localhost:8000/admin
echo.
echo 💡 إذا لم يكن الخادم يعمل، استخدم: quick_start.bat
echo.
pause