Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   🚀 نشر التحديثات على Render.com" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 ملخص التحديثات الجاهزة للنشر:" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ 1. عرض الخصم على بطاقات المنتجات" -ForegroundColor White
Write-Host "   📁 backend/products/serializers.py" -ForegroundColor Gray
Write-Host "   • إضافة discount_percentage" -ForegroundColor Gray
Write-Host "   • إضافة discounted_price" -ForegroundColor Gray
Write-Host "   • إضافة is_on_sale" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ 2. التحقق من المخزون قبل الإضافة للسلة" -ForegroundColor White
Write-Host "   📁 frontend/src/pages/Home.jsx" -ForegroundColor Gray
Write-Host "   • التحقق من stock <= 0" -ForegroundColor Gray
Write-Host "   • التحقق من الكمية المتاحة" -ForegroundColor Gray
Write-Host "   • رسائل خطأ بالعربي" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ 3. إصلاح خطأ 405 في إرسال الطلبات" -ForegroundColor White
Write-Host "   📁 frontend/src/api.js" -ForegroundColor Gray
Write-Host "   • إزالة timestamp parameter" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ 4. تحديث قيمة الشحن المجاني" -ForegroundColor White
Write-Host "   📁 frontend/src/utils/currency.js" -ForegroundColor Gray
Write-Host "   • تغيير من 200,000 إلى 120,000 د.ع" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ 5. تحسين معالجة أخطاء تسجيل الدخول" -ForegroundColor White
Write-Host "   📁 frontend/src/pages/Login.jsx" -ForegroundColor Gray
Write-Host "   • عرض رسائل الخطأ بدلاً من 404" -ForegroundColor Gray
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "⚠️  ملاحظة مهمة:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "الكود موجود على GitHub ولكن Render.com لم يسحبه تلقائياً!" -ForegroundColor Red
Write-Host "يجب عليك نشر التحديثات يدوياً من لوحة التحكم." -ForegroundColor Yellow
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 خطوات النشر (اتبعها بالترتيب):" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "الخطوة 1: افتح Render.com Dashboard" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "🔗 https://dashboard.render.com" -ForegroundColor Blue
Write-Host ""
$openDashboard = Read-Host "اضغط Enter لفتح Dashboard..."
Start-Process "https://dashboard.render.com"
Write-Host "✅ تم فتح Dashboard" -ForegroundColor Green
Write-Host ""

Write-Host "الخطوة 2: انشر Backend" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "1. ابحث عن خدمة: mimi-store-backend" -ForegroundColor Yellow
Write-Host "2. اضغط على اسم الخدمة" -ForegroundColor Yellow
Write-Host "3. في الأعلى، اضغط على زر: Manual Deploy" -ForegroundColor Yellow
Write-Host "4. اختر: Deploy latest commit" -ForegroundColor Yellow
Write-Host "5. انتظر حتى يظهر: Live (5-10 دقائق)" -ForegroundColor Yellow
Write-Host ""
Write-Host "⏳ انتظر حتى يكتمل بناء Backend قبل المتابعة..." -ForegroundColor Cyan
Write-Host ""
$backendDone = Read-Host "هل اكتمل بناء Backend؟ (y/n)"
if ($backendDone -ne 'y' -and $backendDone -ne 'Y') {
    Write-Host ""
    Write-Host "⚠️  يجب انتظار اكتمال Backend قبل نشر Frontend!" -ForegroundColor Red
    Write-Host "اضغط Enter عندما يكتمل البناء..." -ForegroundColor Yellow
    Read-Host
}
Write-Host ""
Write-Host "✅ Backend تم نشره بنجاح" -ForegroundColor Green
Write-Host ""

Write-Host "الخطوة 3: انشر Frontend" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "1. ارجع إلى Dashboard" -ForegroundColor Yellow
Write-Host "2. ابحث عن خدمة: mimi-store-frontend" -ForegroundColor Yellow
Write-Host "3. اضغط على اسم الخدمة" -ForegroundColor Yellow
Write-Host "4. في الأعلى، اضغط على زر: Manual Deploy" -ForegroundColor Yellow
Write-Host "5. اختر: Deploy latest commit" -ForegroundColor Yellow
Write-Host "6. انتظر حتى يظهر: Live (5-10 دقائق)" -ForegroundColor Yellow
Write-Host ""
Write-Host "⏳ انتظر حتى يكتمل بناء Frontend..." -ForegroundColor Cyan
Write-Host ""
$frontendDone = Read-Host "هل اكتمل بناء Frontend؟ (y/n)"
if ($frontendDone -ne 'y' -and $frontendDone -ne 'Y') {
    Write-Host ""
    Write-Host "⚠️  انتظر حتى يكتمل البناء..." -ForegroundColor Yellow
    Write-Host "اضغط Enter عندما يكتمل البناء..." -ForegroundColor Yellow
    Read-Host
}
Write-Host ""
Write-Host "✅ Frontend تم نشره بنجاح" -ForegroundColor Green
Write-Host ""

Write-Host "الخطوة 4: امسح الكاش" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "أ) مسح كاش المتصفح:" -ForegroundColor Yellow
Write-Host "   1. اضغط: Ctrl + Shift + Delete" -ForegroundColor Gray
Write-Host "   2. اختر: All time" -ForegroundColor Gray
Write-Host "   3. اضغط: Clear data" -ForegroundColor Gray
Write-Host ""
$browserCacheDone = Read-Host "هل مسحت كاش المتصفح؟ (y/n)"
if ($browserCacheDone -eq 'y' -or $browserCacheDone -eq 'Y') {
    Write-Host "✅ تم مسح كاش المتصفح" -ForegroundColor Green
}
Write-Host ""

Write-Host "ب) مسح كاش Cloudflare:" -ForegroundColor Yellow
Write-Host "   🔗 https://dash.cloudflare.com" -ForegroundColor Blue
Write-Host ""
$openCloudflare = Read-Host "اضغط Enter لفتح Cloudflare..."
Start-Process "https://dash.cloudflare.com"
Write-Host ""
Write-Host "   1. اختر: mimistore1iq.store" -ForegroundColor Gray
Write-Host "   2. اذهب إلى: Caching" -ForegroundColor Gray
Write-Host "   3. اضغط: Purge Everything" -ForegroundColor Gray
Write-Host "   4. أكد الحذف" -ForegroundColor Gray
Write-Host ""
$cloudflareDone = Read-Host "هل مسحت كاش Cloudflare؟ (y/n)"
if ($cloudflareDone -eq 'y' -or $cloudflareDone -eq 'Y') {
    Write-Host "✅ تم مسح كاش Cloudflare" -ForegroundColor Green
}
Write-Host ""

Write-Host "الخطوة 5: تحقق من الموقع" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "🔗 https://www.mimistore1iq.store" -ForegroundColor Blue
Write-Host ""
$openSite = Read-Host "اضغط Enter لفتح الموقع..."
Start-Process "https://www.mimistore1iq.store"
Write-Host ""
Write-Host "✅ تم فتح الموقع" -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 ما يجب أن تراه الآن:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ السعر الأصلي مشطوب + نسبة الخصم على المنتجات" -ForegroundColor Green
Write-Host "✅ رسالة خطأ عند محاولة إضافة منتج غير متوفر" -ForegroundColor Green
Write-Host "✅ إرسال الطلبات يعمل بدون خطأ 405" -ForegroundColor Green
Write-Host "✅ نص الشحن المجاني: 120,000 د.ع" -ForegroundColor Green
Write-Host "✅ رسائل خطأ تسجيل الدخول تظهر بشكل صحيح" -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "❓ هل ظهرت التحديثات؟" -ForegroundColor Yellow
$updatesWorking = Read-Host "(y/n)"
Write-Host ""

if ($updatesWorking -eq 'y' -or $updatesWorking -eq 'Y') {
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "   🎉 مبروك! التحديثات تعمل بنجاح!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ تم حل 5 مشاكل من أصل 7" -ForegroundColor White
    Write-Host ""
    Write-Host "المشاكل المتبقية (متعلقة بالصور):" -ForegroundColor Yellow
    Write-Host "• الصور تختفي من ImgBB" -ForegroundColor Gray
    Write-Host "• الصور الإضافية (2-4) لا تظهر" -ForegroundColor Gray
    Write-Host ""
    Write-Host "الحل: راجع ملف 📋_حل_مشكلة_الصور_ImgBB.txt" -ForegroundColor Cyan
} else {
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host "   ⚠️  التحديثات لم تظهر بعد" -ForegroundColor Red
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔍 خطوات التشخيص:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. تأكد من اكتمال البناء في Render.com" -ForegroundColor White
    Write-Host "   • يجب أن يظهر 'Live' بجانب كل خدمة" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. تأكد من مسح الكاش بالكامل" -ForegroundColor White
    Write-Host "   • المتصفح: Ctrl + Shift + Delete" -ForegroundColor Gray
    Write-Host "   • Cloudflare: Purge Everything" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. جرب فتح الموقع في نافذة خاصة (Incognito)" -ForegroundColor White
    Write-Host "   • Ctrl + Shift + N (Chrome)" -ForegroundColor Gray
    Write-Host "   • Ctrl + Shift + P (Firefox)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. انتظر 5-10 دقائق ثم حاول مرة أخرى" -ForegroundColor White
    Write-Host "   • أحياناً يستغرق Cloudflare وقتاً لتحديث الكاش" -ForegroundColor Gray
    Write-Host ""
    Write-Host "5. تحقق من Logs في Render.com" -ForegroundColor White
    Write-Host "   • اذهب إلى كل خدمة → Logs" -ForegroundColor Gray
    Write-Host "   • ابحث عن أي أخطاء" -ForegroundColor Gray
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 نصيحة للمستقبل:" -ForegroundColor Cyan
Write-Host ""
Write-Host "لتفعيل النشر التلقائي في Render.com:" -ForegroundColor Yellow
Write-Host "1. اذهب إلى كل خدمة → Settings" -ForegroundColor Gray
Write-Host "2. ابحث عن: Auto-Deploy" -ForegroundColor Gray
Write-Host "3. فعّل: Yes" -ForegroundColor Gray
Write-Host ""
Write-Host "بهذا، كل push على GitHub سينشر تلقائياً!" -ForegroundColor Green
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   ✅ انتهى السكريبت" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "اضغط أي زر للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")