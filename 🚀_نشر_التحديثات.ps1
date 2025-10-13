# ========================================
#    🚀 سكريبت نشر التحديثات
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🚀 سكريبت نشر التحديثات" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# التحقق من حالة Git
Write-Host "📋 التحقق من حالة Git..." -ForegroundColor Green
Write-Host ""

$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  هناك تغييرات غير محفوظة!" -ForegroundColor Yellow
    Write-Host ""
    git status
    Write-Host ""
    
    $response = Read-Host "هل تريد حفظ التغييرات ورفعها؟ (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host ""
        Write-Host "📦 حفظ التغييرات..." -ForegroundColor Green
        git add .
        
        $commitMessage = Read-Host "أدخل رسالة الـ commit"
        git commit -m "$commitMessage"
        
        Write-Host ""
        Write-Host "⬆️  رفع التحديثات إلى GitHub..." -ForegroundColor Green
        git push origin main
        
        Write-Host ""
        Write-Host "✅ تم رفع التحديثات بنجاح!" -ForegroundColor Green
    }
} else {
    Write-Host "✅ جميع التغييرات محفوظة ومرفوعة!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   📊 ملخص التحديثات" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ المشاكل المحلولة (جاهزة للنشر):" -ForegroundColor Green
Write-Host "   1. عرض الخصم في بطاقة المنتج" -ForegroundColor White
Write-Host "   2. التحقق من المخزون عند الإضافة للسلة" -ForegroundColor White
Write-Host "   3. خطأ 405 عند إرسال الطلب" -ForegroundColor White
Write-Host "   4. خطأ تسجيل الدخول (404 redirect)" -ForegroundColor White
Write-Host "   5. نص التوصيل المجاني (120,000 د.ع)" -ForegroundColor White
Write-Host ""

Write-Host "❌ المشاكل المتبقية:" -ForegroundColor Red
Write-Host "   6. الصور تختفي من ImgBB" -ForegroundColor White
Write-Host "   7. الصور الإضافية (2-4) لا تظهر" -ForegroundColor White
Write-Host ""

Write-Host "🔥 السبب: ImgBB يحذف الصور بعد فترة!" -ForegroundColor Yellow
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🎯 الخطوات التالية" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📌 الخطوة 1: انشر على Render.com" -ForegroundColor Green
Write-Host ""
Write-Host "   1. اذهب إلى: https://dashboard.render.com" -ForegroundColor White
Write-Host "   2. انشر Backend (mimi-store-backend)" -ForegroundColor White
Write-Host "      • اضغط 'Manual Deploy'" -ForegroundColor Gray
Write-Host "      • اختر 'Deploy latest commit'" -ForegroundColor Gray
Write-Host "      • انتظر 5-10 دقائق" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. انشر Frontend (mimi-store-frontend)" -ForegroundColor White
Write-Host "      • اضغط 'Manual Deploy'" -ForegroundColor Gray
Write-Host "      • اختر 'Deploy latest commit'" -ForegroundColor Gray
Write-Host "      • انتظر 5-10 دقائق" -ForegroundColor Gray
Write-Host ""

Write-Host "📌 الخطوة 2: امسح الكاش" -ForegroundColor Green
Write-Host ""
Write-Host "   1. المتصفح: Ctrl + Shift + Delete" -ForegroundColor White
Write-Host "   2. Cloudflare: Purge Everything" -ForegroundColor White
Write-Host "   3. Hard Refresh: Ctrl + F5" -ForegroundColor White
Write-Host ""

Write-Host "📌 الخطوة 3: تحقق من الموقع" -ForegroundColor Green
Write-Host ""
Write-Host "   • افتح: https://www.mimistore1iq.store" -ForegroundColor White
Write-Host "   • جرب الخصم ✅" -ForegroundColor White
Write-Host "   • جرب المخزون ✅" -ForegroundColor White
Write-Host "   • جرب الطلب ✅" -ForegroundColor White
Write-Host "   • جرب تسجيل الدخول ✅" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🖼️  حل مشكلة الصور" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  مشكلة الصور تحتاج حل منفصل!" -ForegroundColor Yellow
Write-Host ""
Write-Host "لديك 3 خيارات:" -ForegroundColor White
Write-Host ""
Write-Host "🎯 الخيار 1: Cloudinary (الأفضل ⭐)" -ForegroundColor Cyan
Write-Host "   • مجاني حتى 25GB" -ForegroundColor Gray
Write-Host "   • الصور لا تُحذف أبداً" -ForegroundColor Gray
Write-Host "   • سريع وموثوق" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 الخيار 2: Render Disk (الأسهل ⭐⭐)" -ForegroundColor Cyan
Write-Host "   • مجاني" -ForegroundColor Gray
Write-Host "   • الصور على السيرفر" -ForegroundColor Gray
Write-Host "   • لا يحتاج خدمة خارجية" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 الخيار 3: ImgBB Pro (غير موصى به)" -ForegroundColor Cyan
Write-Host "   • يحتاج اشتراك مدفوع" -ForegroundColor Gray
Write-Host "   • قد تستمر المشكلة" -ForegroundColor Gray
Write-Host ""

Write-Host "📖 التفاصيل الكاملة في:" -ForegroundColor White
Write-Host "   📋_الوضع_الحالي_والحلول.txt" -ForegroundColor Yellow
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🔗 روابط سريعة" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "• Render.com: https://dashboard.render.com" -ForegroundColor White
Write-Host "• الموقع: https://www.mimistore1iq.store" -ForegroundColor White
Write-Host "• Admin: https://www.mimistore1iq.store/admin" -ForegroundColor White
Write-Host "• Cloudflare: https://dash.cloudflare.com" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ✨ ملخص سريع" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ 5 مشاكل محلولة - جاهزة للنشر الآن!" -ForegroundColor Green
Write-Host "❌ 2 مشاكل متبقية - تحتاج حل الصور (ImgBB)" -ForegroundColor Red
Write-Host ""
Write-Host "🎯 الأولوية: انشر التحديثات الآن!" -ForegroundColor Yellow
Write-Host "⏱️  الوقت: 15-20 دقيقة فقط" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🎉 بالتوفيق!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "آخر تحديث: 13 يناير 2025" -ForegroundColor Gray
Write-Host "Commit: a739501" -ForegroundColor Gray
Write-Host ""

Write-Host "📞 إذا احتجت مساعدة، أنا هنا!" -ForegroundColor Cyan
Write-Host ""

# فتح Render.com في المتصفح
$response = Read-Host "هل تريد فتح Render.com الآن؟ (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Start-Process "https://dashboard.render.com"
    Write-Host ""
    Write-Host "✅ تم فتح Render.com في المتصفح!" -ForegroundColor Green
}

Write-Host ""
Write-Host "اضغط أي زر للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")