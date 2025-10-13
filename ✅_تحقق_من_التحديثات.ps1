# ========================================
#    ✅ سكريبت التحقق من التحديثات
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ✅ التحقق من التحديثات" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# التحقق من Git Status
Write-Host "🔍 التحقق من حالة Git..." -ForegroundColor Yellow
Write-Host ""

$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  هناك تغييرات لم يتم رفعها:" -ForegroundColor Red
    Write-Host $gitStatus
    Write-Host ""
    Write-Host "❌ يجب رفع التغييرات أولاً!" -ForegroundColor Red
    Write-Host ""
    Write-Host "استخدم الأوامر التالية:" -ForegroundColor Yellow
    Write-Host "  git add ." -ForegroundColor White
    Write-Host "  git commit -m 'Your message'" -ForegroundColor White
    Write-Host "  git push origin main" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "✅ جميع التغييرات تم رفعها إلى GitHub" -ForegroundColor Green
    Write-Host ""
}

# عرض آخر commit
Write-Host "📝 آخر commit:" -ForegroundColor Yellow
Write-Host ""
git log -1 --oneline
Write-Host ""

# عرض الفرق بين Local و Remote
Write-Host "🔄 التحقق من الفرق بين Local و Remote..." -ForegroundColor Yellow
Write-Host ""

git fetch origin main 2>$null
$localCommit = git rev-parse main
$remoteCommit = git rev-parse origin/main

if ($localCommit -eq $remoteCommit) {
    Write-Host "✅ Local و Remote متطابقان" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "⚠️  Local و Remote غير متطابقين!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Local commit:  $localCommit" -ForegroundColor White
    Write-Host "Remote commit: $remoteCommit" -ForegroundColor White
    Write-Host ""
    Write-Host "❌ يجب عمل push أو pull!" -ForegroundColor Red
    Write-Host ""
}

# عرض الملفات المعدلة في آخر commit
Write-Host "📂 الملفات المعدلة في آخر commit:" -ForegroundColor Yellow
Write-Host ""
git diff-tree --no-commit-id --name-only -r HEAD
Write-Host ""

# التحقق من Backend files
Write-Host "🔍 التحقق من ملفات Backend..." -ForegroundColor Yellow
Write-Host ""

$backendFiles = @(
    "backend/products/serializers.py",
    "backend/orders/urls.py"
)

foreach ($file in $backendFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (غير موجود)" -ForegroundColor Red
    }
}
Write-Host ""

# التحقق من Frontend files
Write-Host "🔍 التحقق من ملفات Frontend..." -ForegroundColor Yellow
Write-Host ""

$frontendFiles = @(
    "frontend/src/api.js",
    "frontend/src/pages/Home.jsx",
    "frontend/src/pages/ProductDetail.jsx",
    "frontend/src/pages/Login.jsx",
    "frontend/src/components/CheckoutNew.jsx"
)

foreach ($file in $frontendFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (غير موجود)" -ForegroundColor Red
    }
}
Write-Host ""

# عرض ملخص
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   📊 ملخص" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not $gitStatus -and $localCommit -eq $remoteCommit) {
    Write-Host "✅ جميع التحديثات تم رفعها بنجاح!" -ForegroundColor Green
    Write-Host ""
    Write-Host "الخطوة التالية:" -ForegroundColor Yellow
    Write-Host "  1. اذهب إلى Render.com" -ForegroundColor White
    Write-Host "  2. انشر Backend و Frontend" -ForegroundColor White
    Write-Host "  3. امسح الكاش" -ForegroundColor White
    Write-Host ""
    Write-Host "📄 راجع ملف: ⚡_اقرأ_هذا_فوراً.txt" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "⚠️  هناك مشاكل يجب حلها!" -ForegroundColor Red
    Write-Host ""
    Write-Host "راجع الرسائل أعلاه لمعرفة المشكلة" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# انتظار ضغطة مفتاح
Write-Host "اضغط أي مفتاح للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")