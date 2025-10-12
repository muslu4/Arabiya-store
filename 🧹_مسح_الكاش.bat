@echo off
chcp 65001 >nul
color 0B

echo ========================================
echo    🧹 مسح الكاش - MIMI STORE
echo ========================================
echo.

echo 📋 خطوات مسح الكاش:
echo.

echo 1️⃣  مسح كاش المتصفح (Chrome/Edge):
echo    ----------------------------------------
echo    • اضغط: Ctrl + Shift + Delete
echo    • اختر: "Cached images and files"
echo    • اختر: "All time"
echo    • اضغط: "Clear data"
echo.

echo 2️⃣  Hard Refresh للموقع:
echo    ----------------------------------------
echo    • افتح: https://www.mimistore1iq.store
echo    • اضغط: Ctrl + F5
echo    • أو: Ctrl + Shift + R
echo.

echo 3️⃣  مسح كاش Cloudflare:
echo    ----------------------------------------
echo    • افتح: https://dash.cloudflare.com
echo    • اختر: mimistore1iq.store
echo    • اذهب إلى: Caching
echo    • اضغط: Purge Everything
echo.

echo 4️⃣  التحقق من التحديثات:
echo    ----------------------------------------
echo    • افتح الموقع في نافذة خاصة (Incognito)
echo    • تحقق من النص الجديد في صفحة المنتج
echo    • تحقق من رسوم التوصيل (5,000 دينار)
echo    • تحقق من ملء معلومات العميل تلقائياً
echo.

echo ========================================
echo.

echo هل تريد فتح الموقع الآن؟ (Y/N): 
set /p choice=

if /i "%choice%"=="Y" (
    start https://www.mimistore1iq.store
    echo ✅ تم فتح الموقع في المتصفح
) else (
    echo ℹ️  يمكنك فتح الموقع يدوياً: https://www.mimistore1iq.store
)

echo.
echo هل تريد فتح لوحة Cloudflare؟ (Y/N): 
set /p choice2=

if /i "%choice2%"=="Y" (
    start https://dash.cloudflare.com
    echo ✅ تم فتح لوحة Cloudflare في المتصفح
)

echo.
echo ========================================
echo    ✨ انتهى
echo ========================================
echo.

pause