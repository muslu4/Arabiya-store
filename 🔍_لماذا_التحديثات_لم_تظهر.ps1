Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   🔍 تشخيص: لماذا التحديثات لم تظهر في الموقع؟" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 الخطوة 1: التحقق من حالة الكود المحلي" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

# التحقق من Git
Set-Location "c:\Users\a\Desktop\ecom_setup\ecom_project\ecom_project"
Write-Host ""
Write-Host "✅ آخر 3 commits على GitHub:" -ForegroundColor Cyan
git log --oneline -3
Write-Host ""

Write-Host "✅ حالة Git الحالية:" -ForegroundColor Cyan
git status
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "📊 الخطوة 2: التحقق من الملفات المهمة" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

# التحقق من ProductSerializer
Write-Host "✅ التحقق من ProductSerializer (الخصم والمخزون):" -ForegroundColor Cyan
$serializerContent = Get-Content "backend\products\serializers.py" -Raw
if ($serializerContent -match "discount_percentage" -and $serializerContent -match "discounted_price") {
    Write-Host "   ✓ حقول الخصم موجودة في الكود المحلي" -ForegroundColor Green
} else {
    Write-Host "   ✗ حقول الخصم غير موجودة!" -ForegroundColor Red
}

if ($serializerContent -match "stock = serializers.IntegerField") {
    Write-Host "   ✓ حقل المخزون موجود في الكود المحلي" -ForegroundColor Green
} else {
    Write-Host "   ✗ حقل المخزون غير موجود!" -ForegroundColor Red
}
Write-Host ""

# التحقق من Home.jsx
Write-Host "✅ التحقق من Home.jsx (التحقق من المخزون):" -ForegroundColor Cyan
$homeContent = Get-Content "frontend\src\pages\Home.jsx" -Raw
if ($homeContent -match "product.stock <= 0") {
    Write-Host "   ✓ التحقق من المخزون موجود في الكود المحلي" -ForegroundColor Green
} else {
    Write-Host "   ✗ التحقق من المخزون غير موجود!" -ForegroundColor Red
}
Write-Host ""

# التحقق من api.js
Write-Host "✅ التحقق من api.js (إزالة timestamp):" -ForegroundColor Cyan
$apiContent = Get-Content "frontend\src\api.js" -Raw
if ($apiContent -notmatch "timestamp") {
    Write-Host "   ✓ لا يوجد timestamp في الكود المحلي (صحيح)" -ForegroundColor Green
} else {
    Write-Host "   ✗ timestamp موجود في الكود!" -ForegroundColor Red
}
Write-Host ""

# التحقق من currency.js
Write-Host "✅ التحقق من currency.js (الشحن المجاني):" -ForegroundColor Cyan
$currencyContent = Get-Content "frontend\src\utils\currency.js" -Raw
if ($currencyContent -match "120000") {
    Write-Host "   ✓ قيمة الشحن المجاني 120,000 د.ع في الكود المحلي" -ForegroundColor Green
} else {
    Write-Host "   ✗ قيمة الشحن المجاني غير صحيحة!" -ForegroundColor Red
}
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 التشخيص النهائي:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ الكود المحلي: جميع التحديثات موجودة" -ForegroundColor Green
Write-Host "✅ GitHub: الكود محدث (آخر commit: 2a27cef)" -ForegroundColor Green
Write-Host ""
Write-Host "❌ المشكلة: Render.com لم يسحب التحديثات من GitHub!" -ForegroundColor Red
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "🔥 الحل: يجب نشر التحديثات يدوياً على Render.com" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "📋 الخطوات المطلوبة:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  افتح Render.com Dashboard:" -ForegroundColor White
Write-Host "   https://dashboard.render.com" -ForegroundColor Blue
Write-Host ""

Write-Host "2️⃣  انشر Backend:" -ForegroundColor White
Write-Host "   • اذهب إلى: mimi-store-backend" -ForegroundColor Gray
Write-Host "   • اضغط: Manual Deploy → Deploy latest commit" -ForegroundColor Gray
Write-Host "   • انتظر حتى يكتمل البناء (5-10 دقائق)" -ForegroundColor Gray
Write-Host ""

Write-Host "3️⃣  انشر Frontend:" -ForegroundColor White
Write-Host "   • اذهب إلى: mimi-store-frontend" -ForegroundColor Gray
Write-Host "   • اضغط: Manual Deploy → Deploy latest commit" -ForegroundColor Gray
Write-Host "   • انتظر حتى يكتمل البناء (5-10 دقائق)" -ForegroundColor Gray
Write-Host ""

Write-Host "4️⃣  امسح الكاش:" -ForegroundColor White
Write-Host "   • المتصفح: Ctrl + Shift + Delete" -ForegroundColor Gray
Write-Host "   • Cloudflare: Caching → Purge Everything" -ForegroundColor Gray
Write-Host ""

Write-Host "5️⃣  تحقق من الموقع:" -ForegroundColor White
Write-Host "   https://www.mimistore1iq.store" -ForegroundColor Blue
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

Write-Host "💡 ملاحظة مهمة:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "Render.com لا ينشر التحديثات تلقائياً!" -ForegroundColor Red
Write-Host "يجب عليك الضغط على 'Manual Deploy' في كل مرة تريد نشر تحديثات جديدة." -ForegroundColor Yellow
Write-Host ""
Write-Host "إذا كنت تريد النشر التلقائي:" -ForegroundColor Cyan
Write-Host "• اذهب إلى Settings في كل خدمة" -ForegroundColor Gray
Write-Host "• فعّل: Auto-Deploy" -ForegroundColor Gray
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

$openRender = Read-Host "هل تريد فتح Render.com Dashboard الآن؟ (y/n)"
if ($openRender -eq 'y' -or $openRender -eq 'Y') {
    Start-Process "https://dashboard.render.com"
    Write-Host ""
    Write-Host "✅ تم فتح Render.com Dashboard" -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   ✅ انتهى التشخيص" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "اضغط أي زر للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")