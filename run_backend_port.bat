@echo off
chcp 65001 >nul
echo 🚀 بدء تشغيل Backend على منفذ مختلف...

cd backend
call env\Scripts\activate

echo 🖥️ تشغيل Backend server على منفذ 8080...
python manage.py runserver 127.0.0.1:8080 --insecure

pause
