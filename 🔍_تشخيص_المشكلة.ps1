# ═══════════════════════════════════════════════════════════════
#  🔍 سكريبت تشخيص مشكلة عدم ظهور التحديثات
# ═══════════════════════════════════════════════════════════════

Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔍 تشخيص مشكلة عدم ظهور التحديثات على الموقع" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ─────────────────────────────────────────────────────────────────
# 1. التحقق من Git Repository
# ─────────────────────────────────────────────────────────────────
Write-Host "📌 الخطوة 1: التحقق من Git Repository" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

Set-Location "c:\Users\a\Desktop\ecom_setup\ecom_project\ecom_project"

Write-Host "`n✅ آخر 3 Commits:" -ForegroundColor Cyan
git log --oneline -3

$lastCommit = git log -1 --format="%h - %s (%ar)"
Write-Host "`n📍 آخر Commit: " -NoNewline -ForegroundColor Yellow
Write-Host "$lastCommit" -ForegroundColor White

# ─────────────────────────────────────────────────────────────────
# 2. التحقق من Build Files
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 2: التحقق من ملفات Build" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$buildFiles = Get-ChildItem "frontend\build\static\js\main.*.js" -ErrorAction SilentlyContinue

if ($buildFiles) {
    $buildFile = $buildFiles[0]
    $buildTime = $buildFile.LastWriteTime
    
    Write-Host "`n✅ ملف Build الرئيسي:" -ForegroundColor Cyan
    Write-Host "   📁 الاسم: $($buildFile.Name)" -ForegroundColor White
    Write-Host "   🕐 التاريخ: $($buildTime.ToString('dd/MM/yyyy hh:mm:ss tt'))" -ForegroundColor White
    
    # التحقق من المحتوى
    $content = Get-Content $buildFile.FullName -Raw
    
    Write-Host "`n🔍 فحص المحتوى:" -ForegroundColor Cyan
    
    if ($content -match "120000") {
        Write-Host "   ✅ يحتوي على: 120000 (صحيح)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ لا يحتوي على: 120000" -ForegroundColor Red
    }
    
    if ($content -match "200000") {
        Write-Host "   ❌ يحتوي على: 200000 (خطأ - قديم)" -ForegroundColor Red
    } else {
        Write-Host "   ✅ لا يحتوي على: 200000 (صحيح)" -ForegroundColor Green
    }
    
} else {
    Write-Host "`n❌ لم يتم العثور على ملفات Build!" -ForegroundColor Red
    Write-Host "   يجب تشغيل: npm run build" -ForegroundColor Yellow
}

# ─────────────────────────────────────────────────────────────────
# 3. التحقق من الكود المصدري
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 3: التحقق من الكود المصدري" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$currencyFile = "frontend\src\utils\currency.js"
if (Test-Path $currencyFile) {
    $currencyContent = Get-Content $currencyFile -Raw
    
    if ($currencyContent -match "FREE_SHIPPING_THRESHOLD.*?(\d+)") {
        $threshold = $matches[1]
        Write-Host "`n✅ قيمة FREE_SHIPPING_THRESHOLD في الكود:" -ForegroundColor Cyan
        Write-Host "   📊 القيمة: $threshold" -ForegroundColor White
        
        if ($threshold -eq "120000") {
            Write-Host "   ✅ صحيحة (120,000)" -ForegroundColor Green
        } else {
            Write-Host "   ❌ خاطئة (يجب أن تكون 120,000)" -ForegroundColor Red
        }
    }
}

# ─────────────────────────────────────────────────────────────────
# 4. مقارنة التواريخ
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 4: مقارنة التواريخ" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$lastCommitDate = git log -1 --format="%ai"
$commitDateTime = [DateTime]::Parse($lastCommitDate)

Write-Host "`n📅 تاريخ آخر Commit: $($commitDateTime.ToString('dd/MM/yyyy hh:mm:ss tt'))" -ForegroundColor Cyan

if ($buildFiles) {
    $buildDateTime = $buildFiles[0].LastWriteTime
    Write-Host "📅 تاريخ آخر Build:  $($buildDateTime.ToString('dd/MM/yyyy hh:mm:ss tt'))" -ForegroundColor Cyan
    
    $timeDiff = ($buildDateTime - $commitDateTime).TotalSeconds
    
    Write-Host "`n⏱️  الفرق الزمني: " -NoNewline -ForegroundColor Yellow
    
    if ($timeDiff -gt 0) {
        Write-Host "$([Math]::Abs($timeDiff)) ثانية (Build أحدث من Commit)" -ForegroundColor Green
        Write-Host "   ✅ Build تم بعد آخر تعديل - صحيح!" -ForegroundColor Green
    } elseif ($timeDiff -lt 0) {
        Write-Host "$([Math]::Abs($timeDiff)) ثانية (Build أقدم من Commit)" -ForegroundColor Red
        Write-Host "   ❌ Build قديم - يجب إعادة Build!" -ForegroundColor Red
    } else {
        Write-Host "نفس الوقت" -ForegroundColor Yellow
    }
}

# ─────────────────────────────────────────────────────────────────
# 5. التحقق من حالة Git
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 5: التحقق من حالة Git" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$gitStatus = git status --porcelain

if ($gitStatus) {
    Write-Host "`n⚠️  يوجد تغييرات غير محفوظة:" -ForegroundColor Yellow
    git status --short
    Write-Host "`n   💡 يجب تشغيل:" -ForegroundColor Cyan
    Write-Host "      git add ." -ForegroundColor White
    Write-Host "      git commit -m 'Update'" -ForegroundColor White
    Write-Host "      git push origin main" -ForegroundColor White
} else {
    Write-Host "`n✅ لا توجد تغييرات غير محفوظة" -ForegroundColor Green
    Write-Host "   كل شيء محفوظ على Git" -ForegroundColor White
}

# ─────────────────────────────────────────────────────────────────
# 6. اختبار الاتصال بالموقع
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 6: اختبار الاتصال بالموقع" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

try {
    $response = Invoke-WebRequest -Uri "https://www.mimistore1iq.store" -Method Head -TimeoutSec 10 -ErrorAction Stop
    Write-Host "`n✅ الموقع يعمل بشكل صحيح" -ForegroundColor Green
    Write-Host "   📊 Status Code: $($response.StatusCode)" -ForegroundColor White
} catch {
    Write-Host "`n❌ فشل الاتصال بالموقع" -ForegroundColor Red
    Write-Host "   الخطأ: $($_.Exception.Message)" -ForegroundColor Yellow
}

# ─────────────────────────────────────────────────────────────────
# 7. التوصيات
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 7: التوصيات" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

Write-Host "`n🎯 الخطوات التالية المطلوبة:" -ForegroundColor Yellow
Write-Host ""

# التحقق من Build
if ($buildFiles -and $buildDateTime -gt $commitDateTime) {
    Write-Host "✅ 1. Build محدث وصحيح" -ForegroundColor Green
} else {
    Write-Host "❌ 1. يجب إعادة Build:" -ForegroundColor Red
    Write-Host "      cd frontend" -ForegroundColor White
    Write-Host "      npm run build" -ForegroundColor White
    Write-Host "      cd .." -ForegroundColor White
}

# التحقق من Git
if (-not $gitStatus) {
    Write-Host "✅ 2. Git محدث" -ForegroundColor Green
} else {
    Write-Host "❌ 2. يجب رفع التغييرات على Git:" -ForegroundColor Red
    Write-Host "      git add ." -ForegroundColor White
    Write-Host "      git commit -m 'Rebuild with updates'" -ForegroundColor White
    Write-Host "      git push origin main" -ForegroundColor White
}

# Render.com
Write-Host "⚠️  3. يجب التحقق من Render.com:" -ForegroundColor Yellow
Write-Host "      • افتح: https://dashboard.render.com" -ForegroundColor White
Write-Host "      • تحقق من حالة النشر (Deploy Status)" -ForegroundColor White
Write-Host "      • إذا لم يبدأ تلقائياً، اضغط 'Manual Deploy'" -ForegroundColor White

# Cache
Write-Host "⚠️  4. يجب مسح الكاش:" -ForegroundColor Yellow
Write-Host "      • المتصفح: Ctrl + Shift + Delete" -ForegroundColor White
Write-Host "      • Cloudflare: Purge Everything" -ForegroundColor White
Write-Host "      • افتح الموقع في Incognito Mode" -ForegroundColor White

# ─────────────────────────────────────────────────────────────────
# 8. روابط سريعة
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 روابط سريعة" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host ""

$openLinks = Read-Host "هل تريد فتح الروابط المهمة؟ (y/n)"

if ($openLinks -eq 'y' -or $openLinks -eq 'Y') {
    Write-Host "`n🚀 فتح الروابط..." -ForegroundColor Cyan
    
    Start-Process "https://dashboard.render.com"
    Start-Sleep -Seconds 1
    
    Start-Process "https://www.mimistore1iq.store"
    Start-Sleep -Seconds 1
    
    $openCloudflare = Read-Host "`nهل تستخدم Cloudflare؟ (y/n)"
    if ($openCloudflare -eq 'y' -or $openCloudflare -eq 'Y') {
        Start-Process "https://dash.cloudflare.com"
    }
    
    Write-Host "`n✅ تم فتح الروابط!" -ForegroundColor Green
}

# ─────────────────────────────────────────────────────────────────
# النهاية
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ انتهى التشخيص" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 نصيحة: إذا كانت المشكلة مستمرة، تأكد من:" -ForegroundColor Yellow
Write-Host "   1. Render.com نشر آخر Commit" -ForegroundColor White
Write-Host "   2. مسح كاش Cloudflare (Purge Everything)" -ForegroundColor White
Write-Host "   3. فتح الموقع في Incognito Mode" -ForegroundColor White
Write-Host ""

Read-Host "اضغط Enter للخروج"