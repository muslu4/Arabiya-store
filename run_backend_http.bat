@echo off
chcp 65001 >nul
echo 🚀 بدء تشغيل Backend مع HTTP فقط...

cd backend
call env\Scripts\activate

echo 🖥️ تشغيل Backend server على HTTP...
python manage.py runserver 127.0.0.1:8000 --insecure

pause
