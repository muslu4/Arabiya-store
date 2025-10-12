@echo off
chcp 65001 >nul
color 0E

echo.
echo ╔════════════════════════════════════════╗
echo ║   ⚡ نشر التحديثات الآن - MIMI STORE  ║
echo ╚════════════════════════════════════════╝
echo.

echo ✅ التحديثات موجودة على GitHub!
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    🚀 سيتم فتح لوحات التحكم الآن
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo هل تريد المتابعة؟ (Y/N): 
set /p choice=

if /i "%choice%" NEQ "Y" (
    echo.
    echo ❌ تم الإلغاء
    echo.
    pause
    exit
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    📋 الخطوة 1: فتح لوحة Render.com
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo 🔗 فتح: https://dashboard.render.com
start https://dashboard.render.com
timeout /t 3 /nobreak >nul
echo ✅ تم

echo.
echo 📋 ماذا تفعل في Render.com:
echo.
echo    1. ابحث عن: mimi-store-frontend
echo    2. تحقق من حالة النشر (Deploy Status)
echo    3. إذا لم يبدأ تلقائياً:
echo       • اضغط "Manual Deploy"
echo       • اختر "Deploy latest commit"
echo.
echo    4. كرر نفس الخطوات لـ: mimi-store-backend
echo.

echo اضغط أي زر للمتابعة...
pause >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    📋 الخطوة 2: فتح الموقع المباشر
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo 🔗 فتح: https://www.mimistore1iq.store
start https://www.mimistore1iq.store
timeout /t 2 /nobreak >nul
echo ✅ تم

echo.
echo 📋 ماذا تفعل في الموقع:
echo.
echo    1. اضغط: Ctrl + Shift + Delete
echo    2. امسح: "Cached images and files"
echo    3. اختر: "All time"
echo    4. اضغط: "Clear data"
echo.
echo    5. ثم اضغط: Ctrl + F5 (Hard Refresh)
echo.

echo اضغط أي زر للمتابعة...
pause >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    📋 الخطوة 3: فتح لوحة Cloudflare
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo هل تستخدم Cloudflare؟ (Y/N): 
set /p cloudflare=

if /i "%cloudflare%"=="Y" (
    echo.
    echo 🔗 فتح: https://dash.cloudflare.com
    start https://dash.cloudflare.com
    timeout /t 2 /nobreak >nul
    echo ✅ تم
    echo.
    echo 📋 ماذا تفعل في Cloudflare:
    echo.
    echo    1. اختر: mimistore1iq.store
    echo    2. اذهب إلى: Caching
    echo    3. اضغط: Purge Everything
    echo    4. أكد العملية
    echo.
) else (
    echo.
    echo ℹ️  تم تخطي Cloudflare
    echo.
)

echo اضغط أي زر للمتابعة...
pause >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    ✅ التحقق من التحديثات
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo 📋 تحقق من التالي في الموقع:
echo.
echo    1. صفحة المنتج:
echo       ✓ النص: "توصيل مجاني... 120,000 د.ع"
echo       ✓ (بدلاً من 200,000)
echo.
echo    2. صفحة الطلب:
echo       ✓ رسوم التوصيل: 5,000 دينار
echo       ✓ التوصيل المجاني: 120,000 دينار
echo.
echo    3. ملء معلومات العميل:
echo       ✓ سجل الدخول
echo       ✓ اذهب لصفحة الطلب
echo       ✓ يجب أن تُملأ تلقائياً
echo.
echo    4. لوحة الإدارة:
echo       ✓ افتح: /admin
echo       ✓ جرب إضافة منتج
echo       ✓ يجب أن تعمل بدون أخطاء
echo.

echo هل تريد فتح لوحة الإدارة للتحقق؟ (Y/N): 
set /p admin=

if /i "%admin%"=="Y" (
    echo.
    echo 🔗 فتح: https://www.mimistore1iq.store/admin
    start https://www.mimistore1iq.store/admin
    timeout /t 2 /nobreak >nul
    echo ✅ تم
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    🐛 حل المشاكل
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo ❌ التحديثات لا تظهر؟
echo    1. تأكد من اكتمال النشر على Render
echo    2. امسح الكاش مرة أخرى
echo    3. افتح في نافذة خاصة (Incognito)
echo    4. جرب متصفح آخر
echo.

echo ❌ Render لا ينشر تلقائياً؟
echo    1. استخدم "Manual Deploy"
echo    2. تحقق من إعدادات Auto-Deploy
echo    3. تأكد من ربط GitHub
echo.

echo ❌ أخطاء في Build؟
echo    1. تحقق من Logs في Render
echo    2. ابحث عن الأخطاء الحمراء
echo    3. تواصل معي
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    📊 ملخص التحديثات
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Backend:
echo    ✅ إصلاح Django Admin
echo    ✅ رسوم توصيل: 5,000 د.ع
echo    ✅ توصيل مجاني: 120,000 د.ع
echo.

echo Frontend:
echo    ✅ نص جديد (120,000)
echo    ✅ حساب رسوم جديد
echo    ✅ ملء تلقائي للبيانات
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    ✨ انتهى!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo 🎯 الخطوات التالية:
echo.
echo    1. انتظر حتى يكتمل النشر على Render (5-10 دقائق)
echo    2. امسح الكاش من المتصفح و Cloudflare
echo    3. افتح الموقع وتحقق من التحديثات
echo    4. اختبر جميع الوظائف الجديدة
echo.

echo ╔════════════════════════════════════════╗
echo ║   ✅ بالتوفيق!                        ║
echo ╚════════════════════════════════════════╝
echo.

pause