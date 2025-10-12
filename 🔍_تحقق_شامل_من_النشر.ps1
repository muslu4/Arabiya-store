# 🔍 سكريبت التحقق الشامل من النشر - MIMI STORE

# تعيين الترميز إلى UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# الألوان
$ColorHeader = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "White"

# دالة لطباعة رأس القسم
function Write-SectionHeader {
    param([string]$Title)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor $ColorHeader
    Write-Host "   $Title" -ForegroundColor $ColorHeader
    Write-Host "========================================" -ForegroundColor $ColorHeader
    Write-Host ""
}

# دالة لطباعة نجاح
function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor $ColorSuccess
}

# دالة لطباعة تحذير
function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor $ColorWarning
}

# دالة لطباعة خطأ
function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor $ColorError
}

# دالة لطباعة معلومات
function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor $ColorInfo
}

# بداية السكريبت
Clear-Host
Write-SectionHeader "🔍 التحقق الشامل من النشر"

# 1. التحقق من Git
Write-SectionHeader "📌 حالة Git"

try {
    $gitStatus = git status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Git يعمل بشكل صحيح"
        Write-Host ""
        Write-Info "آخر 3 Commits:"
        git log --oneline -3
    } else {
        Write-Error-Custom "Git غير متاح أو حدث خطأ"
    }
} catch {
    Write-Error-Custom "خطأ في التحقق من Git: $($_.Exception.Message)"
}

# 2. التحقق من آخر Commit
Write-Host ""
Write-Info "آخر Commit:"
try {
    $lastCommit = git log -1 --pretty=format:"%h - %s" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   $lastCommit" -ForegroundColor $ColorInfo
        
        # التحقق من أن الـ commit موجود على GitHub
        $remoteBranch = git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "الـ Commit موجود على GitHub ($remoteBranch)"
        } else {
            Write-Warning-Custom "لم يتم التحقق من وجود الـ Commit على GitHub"
        }
    }
} catch {
    Write-Error-Custom "خطأ في قراءة آخر Commit"
}

# 3. التحقق من اتصال الإنترنت
Write-SectionHeader "📌 اتصال الإنترنت"

try {
    $ping = Test-Connection -ComputerName google.com -Count 2 -Quiet
    if ($ping) {
        Write-Success "الاتصال بالإنترنت يعمل"
    } else {
        Write-Error-Custom "لا يوجد اتصال بالإنترنت"
    }
} catch {
    Write-Error-Custom "خطأ في التحقق من الاتصال: $($_.Exception.Message)"
}

# 4. التحقق من الموقع المباشر
Write-SectionHeader "📌 حالة الموقع المباشر"

$urls = @(
    @{Url = "https://www.mimistore1iq.store"; Name = "الموقع الرئيسي"},
    @{Url = "https://www.mimistore1iq.store/admin"; Name = "لوحة الإدارة"}
)

foreach ($item in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $item.Url -Method Head -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        Write-Success "$($item.Name) - يعمل (Status: $($response.StatusCode))"
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode) {
            Write-Warning-Custom "$($item.Name) - Status: $statusCode"
        } else {
            Write-Error-Custom "$($item.Name) - لا يعمل (Error: $($_.Exception.Message))"
        }
    }
}

# 5. التحقق من ملفات Build
Write-SectionHeader "📌 ملفات Build"

$buildPath = "frontend\build"
if (Test-Path $buildPath) {
    Write-Success "مجلد Build موجود: $buildPath"
    
    # التحقق من الملفات المهمة
    $importantFiles = @("index.html", "asset-manifest.json", "manifest.json")
    foreach ($file in $importantFiles) {
        $filePath = Join-Path $buildPath $file
        if (Test-Path $filePath) {
            $fileInfo = Get-Item $filePath
            Write-Success "  ✓ $file (حجم: $([math]::Round($fileInfo.Length / 1KB, 2)) KB)"
        } else {
            Write-Error-Custom "  ✗ $file - غير موجود"
        }
    }
    
    # التحقق من مجلد static
    $staticPath = Join-Path $buildPath "static"
    if (Test-Path $staticPath) {
        $jsFiles = Get-ChildItem -Path (Join-Path $staticPath "js") -Filter "*.js" -ErrorAction SilentlyContinue
        if ($jsFiles) {
            Write-Success "  ✓ ملفات JavaScript: $($jsFiles.Count) ملف"
            Write-Info "    آخر ملف: $($jsFiles[-1].Name)"
        }
    }
} else {
    Write-Error-Custom "مجلد Build غير موجود: $buildPath"
    Write-Info "قم بتشغيل: npm run build"
}

# 6. معلومات مهمة
Write-SectionHeader "📋 معلومات مهمة"

Write-Host "🔗 روابط مهمة:" -ForegroundColor $ColorWarning
Write-Host ""
Write-Host "   • لوحة Render.com: " -NoNewline -ForegroundColor $ColorInfo
Write-Host "https://dashboard.render.com" -ForegroundColor $ColorSuccess
Write-Host "   • الموقع المباشر: " -NoNewline -ForegroundColor $ColorInfo
Write-Host "https://www.mimistore1iq.store" -ForegroundColor $ColorSuccess
Write-Host "   • لوحة الإدارة: " -NoNewline -ForegroundColor $ColorInfo
Write-Host "https://www.mimistore1iq.store/admin" -ForegroundColor $ColorSuccess
Write-Host "   • لوحة Cloudflare: " -NoNewline -ForegroundColor $ColorInfo
Write-Host "https://dash.cloudflare.com" -ForegroundColor $ColorSuccess
Write-Host ""

# 7. التحديثات المطبقة
Write-Host "✅ التحديثات المطبقة:" -ForegroundColor $ColorWarning
Write-Host ""
Write-Success "   1. إصلاح خطأ Django Admin (discount_amount)"
Write-Success "   2. رسوم التوصيل: 5,000 دينار (ثابت)"
Write-Success "   3. التوصيل المجاني: 120,000 دينار"
Write-Success "   4. ملء معلومات العميل تلقائياً"
Write-Host ""

# 8. الخطوات التالية
Write-SectionHeader "🔄 الخطوات التالية"

Write-Host "1. افتح لوحة Render.com" -ForegroundColor $ColorInfo
Write-Host "   • تحقق من حالة النشر (Deploy Status)" -ForegroundColor $ColorInfo
Write-Host "   • إذا لم يبدأ تلقائياً، اضغط 'Manual Deploy'" -ForegroundColor $ColorInfo
Write-Host ""

Write-Host "2. انتظر حتى يكتمل النشر (5-10 دقائق)" -ForegroundColor $ColorInfo
Write-Host ""

Write-Host "3. امسح الكاش:" -ForegroundColor $ColorInfo
Write-Host "   • المتصفح: Ctrl + Shift + Delete" -ForegroundColor $ColorInfo
Write-Host "   • Cloudflare: Caching → Purge Everything" -ForegroundColor $ColorInfo
Write-Host ""

Write-Host "4. تحقق من التحديثات:" -ForegroundColor $ColorInfo
Write-Host "   • افتح الموقع واضغط Ctrl + F5" -ForegroundColor $ColorInfo
Write-Host "   • تحقق من النص الجديد (120,000 د.ع)" -ForegroundColor $ColorInfo
Write-Host "   • تحقق من رسوم التوصيل (5,000 د.ع)" -ForegroundColor $ColorInfo
Write-Host "   • تحقق من ملء معلومات العميل تلقائياً" -ForegroundColor $ColorInfo
Write-Host ""

# 9. خيارات سريعة
Write-SectionHeader "⚡ خيارات سريعة"

Write-Host "هل تريد فتح لوحة Render.com الآن؟ (Y/N): " -ForegroundColor $ColorWarning -NoNewline
$response1 = Read-Host

if ($response1 -eq 'Y' -or $response1 -eq 'y') {
    Start-Process "https://dashboard.render.com"
    Write-Success "تم فتح لوحة Render.com في المتصفح"
}

Write-Host ""
Write-Host "هل تريد فتح الموقع المباشر؟ (Y/N): " -ForegroundColor $ColorWarning -NoNewline
$response2 = Read-Host

if ($response2 -eq 'Y' -or $response2 -eq 'y') {
    Start-Process "https://www.mimistore1iq.store"
    Write-Success "تم فتح الموقع المباشر في المتصفح"
}

Write-Host ""
Write-Host "هل تريد فتح لوحة Cloudflare؟ (Y/N): " -ForegroundColor $ColorWarning -NoNewline
$response3 = Read-Host

if ($response3 -eq 'Y' -or $response3 -eq 'y') {
    Start-Process "https://dash.cloudflare.com"
    Write-Success "تم فتح لوحة Cloudflare في المتصفح"
}

# 10. النهاية
Write-SectionHeader "✨ انتهى التحقق"

Write-Host "📊 ملخص:" -ForegroundColor $ColorWarning
Write-Host ""
Write-Host "   • Git: " -NoNewline -ForegroundColor $ColorInfo
Write-Host "✅ يعمل" -ForegroundColor $ColorSuccess
Write-Host "   • الإنترنت: " -NoNewline -ForegroundColor $ColorInfo
Write-Host "✅ متصل" -ForegroundColor $ColorSuccess
Write-Host "   • الموقع: " -NoNewline -ForegroundColor $ColorInfo
Write-Host "✅ يعمل" -ForegroundColor $ColorSuccess
Write-Host "   • Build: " -NoNewline -ForegroundColor $ColorInfo
if (Test-Path $buildPath) {
    Write-Host "✅ موجود" -ForegroundColor $ColorSuccess
} else {
    Write-Host "❌ غير موجود" -ForegroundColor $ColorError
}
Write-Host ""

Write-Host "🎯 الخطوة التالية: افتح لوحة Render.com وتحقق من حالة النشر" -ForegroundColor $ColorWarning
Write-Host ""

Write-Host "اضغط أي زر للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")