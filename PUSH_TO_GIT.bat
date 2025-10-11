@echo off
chcp 65001 >nul
echo ========================================
echo 📤 رفع التحديثات للمستودع
echo ========================================
echo.

REM الانتقال لمجلد المستودع
cd /d "%~dp0"

echo 📋 التحقق من الملفات المعدلة...
git status

echo.
echo 📦 إضافة جميع التغييرات...
git add .

echo.
set /p commit_msg="✍️ أدخل رسالة الـ commit (أو اضغط Enter للرسالة الافتراضية): "

if "%commit_msg%"=="" (
    set commit_msg=Fix: Register Coupons in custom admin site
)

echo.
echo 💾 حفظ التغييرات...
git commit -m "%commit_msg%"

echo.
echo 🚀 رفع التحديثات...
git push origin main

if errorlevel 1 (
    echo.
    echo ⚠️ فشل الرفع! جرب:
    echo    git push origin master
    git push origin master
)

echo.
echo ✅ تم رفع التحديثات بنجاح!
echo.
pause