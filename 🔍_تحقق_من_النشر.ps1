# 🔍 سكريبت التحقق من حالة النشر على Render.com

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🔍 التحقق من حالة النشر" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. التحقق من آخر commit على GitHub
Write-Host "📌 آخر Commits على GitHub:" -ForegroundColor Yellow
Write-Host ""
git log --oneline -3
Write-Host ""

# 2. التحقق من حالة Git
Write-Host "📌 حالة Git الحالية:" -ForegroundColor Yellow
Write-Host ""
git status
Write-Host ""

# 3. التحقق من اتصال الإنترنت
Write-Host "📌 التحقق من اتصال الإنترنت:" -ForegroundColor Yellow
Write-Host ""
$ping = Test-Connection -ComputerName google.com -Count 2 -Quiet
if ($ping) {
    Write-Host "✅ الاتصال بالإنترنت يعمل" -ForegroundColor Green
} else {
    Write-Host "❌ لا يوجد اتصال بالإنترنت" -ForegroundColor Red
}
Write-Host ""

# 4. التحقق من الموقع المباشر
Write-Host "📌 التحقق من الموقع المباشر:" -ForegroundColor Yellow
Write-Host ""

$urls = @(
    "https://www.mimistore1iq.store",
    "https://mimistore1iq.store"
)

foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 10 -UseBasicParsing
        Write-Host "✅ $url - يعمل (Status: $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "❌ $url - لا يعمل (Error: $($_.Exception.Message))" -ForegroundColor Red
    }
}
Write-Host ""

# 5. معلومات مهمة
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   📋 معلومات مهمة" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔗 روابط مهمة:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   • لوحة Render.com: https://dashboard.render.com" -ForegroundColor White
Write-Host "   • الموقع المباشر: https://www.mimistore1iq.store" -ForegroundColor White
Write-Host "   • لوحة Cloudflare: https://dash.cloudflare.com" -ForegroundColor White
Write-Host ""

Write-Host "✅ التحديثات المطبقة:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1. ✅ إصلاح خطأ Django Admin (discount_amount)" -ForegroundColor Green
Write-Host "   2. ✅ رسوم التوصيل: 5,000 دينار (ثابت)" -ForegroundColor Green
Write-Host "   3. ✅ التوصيل المجاني: 120,000 دينار" -ForegroundColor Green
Write-Host "   4. ✅ ملء معلومات العميل تلقائياً" -ForegroundColor Green
Write-Host ""

Write-Host "🔄 الخطوات التالية:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1. افتح لوحة Render.com: https://dashboard.render.com" -ForegroundColor White
Write-Host "   2. تحقق من حالة النشر (Deploy Status)" -ForegroundColor White
Write-Host "   3. انتظر حتى يكتمل النشر (5-10 دقائق)" -ForegroundColor White
Write-Host "   4. امسح كاش المتصفح (Ctrl + Shift + Delete)" -ForegroundColor White
Write-Host "   5. امسح كاش Cloudflare (Purge Everything)" -ForegroundColor White
Write-Host "   6. افتح الموقع وتحقق من التحديثات" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ✨ انتهى التحقق" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# فتح لوحة Render.com في المتصفح
Write-Host "هل تريد فتح لوحة Render.com الآن؟ (Y/N): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Start-Process "https://dashboard.render.com"
    Write-Host "✅ تم فتح لوحة Render.com في المتصفح" -ForegroundColor Green
}

Write-Host ""
Write-Host "اضغط أي زر للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")