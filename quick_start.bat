@echo off
chcp 65001 >nul
echo 🚀 تشغيل سريع لـ MIMI STORE Backend...

REM Activate virtual environment and start server
call backend\env\Scripts\activate
echo 🖥️ تشغيل الخادم...
python manage.py runserver

pause