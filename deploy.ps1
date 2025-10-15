# ========================================
#   📤 سكريبت رفع التحديثات إلى Render.com
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   📤 رفع التحديثات إلى Render.com" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# التحقق من وجود Git
Write-Host "🔍 التحقق من Git..." -ForegroundColor Yellow
$gitCheck = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitCheck) {
    Write-Host "❌ Git غير مثبت! يرجى تثبيت Git أولاً." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Git موجود" -ForegroundColor Green
Write-Host ""

# التحقق من حالة Git
Write-Host "📊 حالة Git الحالية:" -ForegroundColor Yellow
git status
Write-Host ""

# سؤال المستخدم عن المتابعة
$continue = Read-Host "هل تريد المتابعة؟ (y/n)"
if ($continue -ne "y" -and $continue -ne "Y") {
    Write-Host "❌ تم الإلغاء" -ForegroundColor Red
    exit 0
}
Write-Host ""

# إضافة جميع التغييرات
Write-Host "📦 إضافة جميع التغييرات..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ فشل في إضافة التغييرات" -ForegroundColor Red
    exit 1
}
Write-Host "✅ تم إضافة التغييرات" -ForegroundColor Green
Write-Host ""

# طلب رسالة الـ commit
$commitMessage = Read-Host "أدخل رسالة الـ commit (اضغط Enter للرسالة الافتراضية)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "إصلاح حساب الخصم والسلة وفصل الطلبات الجديدة"
}

# عمل commit
Write-Host "💾 عمل commit..." -ForegroundColor Yellow
git commit -m "$commitMessage"
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ لا توجد تغييرات جديدة للـ commit" -ForegroundColor Yellow
}
Write-Host ""

# رفع التغييرات
Write-Host "🚀 رفع التغييرات إلى GitHub..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ فشل في رفع التغييرات" -ForegroundColor Red
    Write-Host "💡 جرب: git push origin master" -ForegroundColor Yellow
    git push origin master
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ فشل في رفع التغييرات" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ تم رفع التغييرات بنجاح!" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ✅ تم رفع التحديثات بنجاح!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 الخطوات التالية:" -ForegroundColor Yellow
Write-Host "1. اذهب إلى Render Dashboard: https://dashboard.render.com" -ForegroundColor White
Write-Host "2. انتظر حتى يكتمل النشر التلقائي (5-10 دقائق)" -ForegroundColor White
Write-Host "3. اختبر الموقع للتأكد من أن كل شيء يعمل" -ForegroundColor White
Write-Host ""
Write-Host "🔍 للتحقق من Logs:" -ForegroundColor Yellow
Write-Host "- افتح Render Dashboard" -ForegroundColor White
Write-Host "- اختر خدمة Backend أو Frontend" -ForegroundColor White
Write-Host "- اضغط على 'Logs' لمشاهدة السجلات" -ForegroundColor White
Write-Host ""

# فتح Render Dashboard
$openDashboard = Read-Host "هل تريد فتح Render Dashboard؟ (y/n)"
if ($openDashboard -eq "y" -or $openDashboard -eq "Y") {
    Start-Process "https://dashboard.render.com"
}

Write-Host ""
Write-Host "✅ انتهى!" -ForegroundColor Green