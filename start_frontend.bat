@echo off
chcp 65001 >nul
echo 🎨 تشغيل واجهة MIMI STORE...

REM Check if backend is running
echo 🔍 فحص حالة Backend...
curl -s http://localhost:8000/api/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend غير متصل!
    echo 🚀 يرجى تشغيل Backend أولاً باستخدام:
    echo    quick_start.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Backend متصل بنجاح!
echo.

REM Try to open with different browsers
echo 🌐 فتح الواجهة في المتصفح...

REM Try Chrome first
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "MIMI STORE Frontend" "C:\Program Files\Google\Chrome\Application\chrome.exe" "file:///%~dp0frontend\index.html"
    goto :opened
)

REM Try Chrome (x86)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "MIMI STORE Frontend" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "file:///%~dp0frontend\index.html"
    goto :opened
)

REM Try Edge
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "MIMI STORE Frontend" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "file:///%~dp0frontend\index.html"
    goto :opened
)

REM Try Firefox
if exist "C:\Program Files\Mozilla Firefox\firefox.exe" (
    start "MIMI STORE Frontend" "C:\Program Files\Mozilla Firefox\firefox.exe" "file:///%~dp0frontend\index.html"
    goto :opened
)

REM Default browser
start "MIMI STORE Frontend" "file:///%~dp0frontend\index.html"

:opened
echo.
echo ✅ تم فتح واجهة MIMI STORE!
echo.
echo 🔗 الروابط:
echo    الواجهة الأمامية: file:///%~dp0frontend\index.html
echo    Backend API: http://localhost:8000/api
echo    Django Admin: http://localhost:8000/admin
echo.
echo 👤 بيانات المشرف:
echo    الهاتف: admin
echo    كلمة المرور: admin123
echo.
echo 💡 نصائح:
echo    - استخدم Developer Tools (F12) لمراقبة الأخطاء
echo    - تأكد من تشغيل Backend قبل استخدام الواجهة
echo    - يمكنك استخدام Live Server في VS Code للتطوير
echo.
echo 📱 المميزات المتاحة:
echo    ✅ عرض المنتجات والأقسام
echo    ✅ البحث في المنتجات
echo    ✅ تسجيل الدخول
echo    ✅ سلة التسوق
echo    ✅ تفاصيل المنتجات
echo    ✅ تصميم متجاوب
echo.
pause