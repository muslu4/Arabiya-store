@echo off
chcp 65001 >nul
echo 🚀 تشغيل سريع لـ MIMI STORE Backend...

cd /d "%~dp0"

REM Activate virtual environment and start server
call backend\env\Scripts\activate
echo 🖥️ تشغيل الخادم...
cd backend
start /b python manage.py runserver

pause