@echo off
chcp 65001 >nul
echo 🌐 تشغيل خادم الواجهة الأمامية...

REM Check if backend is running
echo 🔍 فحص حالة Backend...
curl -s http://localhost:8000/api/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend غير متصل!
    echo 🚀 يرجى تشغيل Backend أولاً:
    echo    quick_start.bat
    echo.
    echo ⚠️  هل تريد المتابعة بدون Backend؟ (y/n)
    set /p continue=
    if /i not "%continue%"=="y" (
        pause
        exit /b 1
    )
)

echo ✅ بدء تشغيل خادم الواجهة الأمامية...

REM Activate virtual environment
call backend\env\Scripts\activate

REM Start frontend server
python serve_frontend.py

pause