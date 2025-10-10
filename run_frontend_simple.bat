@echo off
chcp 65001 >nul
echo 🎨 تشغيل واجهة MIMI STORE...

cd frontend
echo 🚀 تثبيت الاعتماديات...
call npm install

echo 🖥️ تشغيل Frontend server على المنفذ 3002...
call npm start

pause
