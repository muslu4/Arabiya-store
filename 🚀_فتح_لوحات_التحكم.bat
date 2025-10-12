@echo off
chcp 65001 >nul
color 0A

echo ========================================
echo    🚀 فتح لوحات التحكم - MIMI STORE
echo ========================================
echo.

echo 📋 سيتم فتح الروابط التالية:
echo.
echo    1. لوحة Render.com (للنشر)
echo    2. الموقع المباشر (للتحقق)
echo    3. لوحة الإدارة (Django Admin)
echo    4. لوحة Cloudflare (لمسح الكاش)
echo.

echo هل تريد المتابعة؟ (Y/N): 
set /p choice=

if /i "%choice%" NEQ "Y" (
    echo ❌ تم الإلغاء
    pause
    exit
)

echo.
echo ========================================
echo    🔄 جاري فتح الروابط...
echo ========================================
echo.

echo 1️⃣  فتح لوحة Render.com...
start https://dashboard.render.com
timeout /t 2 /nobreak >nul
echo    ✅ تم

echo.
echo 2️⃣  فتح الموقع المباشر...
start https://www.mimistore1iq.store
timeout /t 2 /nobreak >nul
echo    ✅ تم

echo.
echo 3️⃣  فتح لوحة الإدارة...
start https://www.mimistore1iq.store/admin
timeout /t 2 /nobreak >nul
echo    ✅ تم

echo.
echo 4️⃣  فتح لوحة Cloudflare...
start https://dash.cloudflare.com
timeout /t 2 /nobreak >nul
echo    ✅ تم

echo.
echo ========================================
echo    ✅ تم فتح جميع الروابط
echo ========================================
echo.

echo 📋 الخطوات التالية:
echo.
echo    1. في لوحة Render.com:
echo       • تحقق من حالة النشر (Deploy Status)
echo       • إذا لم يبدأ تلقائياً، اضغط "Manual Deploy"
echo.
echo    2. انتظر حتى يكتمل النشر (5-10 دقائق)
echo.
echo    3. في لوحة Cloudflare:
echo       • اذهب إلى: Caching
echo       • اضغط: Purge Everything
echo.
echo    4. في المتصفح:
echo       • اضغط: Ctrl + Shift + Delete
echo       • امسح الكاش
echo.
echo    5. في الموقع المباشر:
echo       • اضغط: Ctrl + F5 (Hard Refresh)
echo       • تحقق من التحديثات
echo.

echo ========================================
echo.

pause