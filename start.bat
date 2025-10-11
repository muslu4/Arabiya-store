@echo off
chcp 65001 >nul
title MIMI STORE - تشغيل المشروع

REM ═══════════════════════════════════════════════════════════
REM  MIMI STORE - تشغيل سريع
REM ═══════════════════════════════════════════════════════════

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              🛍️  MIMI STORE - تشغيل المشروع 🛍️            ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.

cd /d "%~dp0"

REM ═══════════════════════════════════════════════════════════
REM  تشغيل Backend
REM ═══════════════════════════════════════════════════════════
echo [1/2] 🔧 تشغيل Backend...
echo.

if not exist "backend\env" (
    echo ⚠️  تحذير: البيئة الافتراضية غير موجودة!
    echo 📦 جاري الإنشاء...
    cd backend
    python -m venv env
    cd ..
)

start "MIMI Backend" cmd /k "cd /d "%~dp0backend" && env\Scripts\activate && python manage.py runserver 8000"
echo ✅ Backend يعمل على: http://localhost:8000
echo.

timeout /t 3 /nobreak >nul

REM ═══════════════════════════════════════════════════════════
REM  تشغيل Frontend
REM ═══════════════════════════════════════════════════════════
echo [2/2] 🎨 تشغيل Frontend...
echo.

if not exist "frontend\node_modules" (
    echo ⚠️  تحذير: حزم Node.js غير مثبتة!
    echo 📦 جاري التثبيت... (قد يستغرق دقائق)
    cd frontend
    call npm install
    cd ..
)

start "MIMI Frontend" cmd /k "cd /d "%~dp0frontend" && npm start"
echo ✅ Frontend يعمل على: http://localhost:3002
echo.

timeout /t 5 /nobreak >nul

REM ═══════════════════════════════════════════════════════════
REM  فتح المتصفح
REM ═══════════════════════════════════════════════════════════
echo 🌐 فتح المتصفح...
timeout /t 3 /nobreak >nul
start http://localhost:3002

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✅ تم تشغيل المشروع بنجاح! ✅                ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.
echo 🔗 الروابط:
echo    ┌────────────────────────────────────────────────────
echo    │ 🌐 المتجر:         http://localhost:3002
echo    │ 🔧 API:            http://localhost:8000/api
echo    │ 👤 لوحة الإدارة:   http://localhost:8000/admin
echo    └────────────────────────────────────────────────────
echo.
echo 👤 بيانات الدخول:
echo    ┌────────────────────────────────────────────────────
echo    │ الهاتف:          admin
echo    │ كلمة المرور:     admin123
echo    └────────────────────────────────────────────────────
echo.
echo 💡 ملاحظات:
echo    • لإيقاف الخوادم: أغلق نوافذ Backend و Frontend
echo    • للمساعدة: اقرأ ملف START_GUIDE_AR.md
echo.
echo ═══════════════════════════════════════════════════════════
pause