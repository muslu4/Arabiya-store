# ═══════════════════════════════════════════════════════════════
#  🚀 سكريبت إصلاح ونشر التحديثات تلقائياً
# ═══════════════════════════════════════════════════════════════

Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🚀 إصلاح ونشر التحديثات تلقائياً" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Set-Location "c:\Users\a\Desktop\ecom_setup\ecom_project\ecom_project"

# ─────────────────────────────────────────────────────────────────
# 1. التحقق من الوضع الحالي
# ─────────────────────────────────────────────────────────────────
Write-Host "📌 الخطوة 1: التحقق من الوضع الحالي" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$lastCommit = git log -1 --format="%h - %s"
Write-Host "`n✅ آخر Commit: $lastCommit" -ForegroundColor Cyan

$buildFile = Get-ChildItem "frontend\build\static\js\main.*.js" -ErrorAction SilentlyContinue | Select-Object -First 1

if ($buildFile) {
    $buildTime = $buildFile.LastWriteTime
    Write-Host "✅ آخر Build: $($buildTime.ToString('dd/MM/yyyy hh:mm:ss tt'))" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  لا يوجد Build" -ForegroundColor Yellow
}

# ─────────────────────────────────────────────────────────────────
# 2. إعادة Build
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 2: إعادة Build للـ Frontend" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$rebuild = Read-Host "`nهل تريد إعادة Build الآن؟ (y/n)"

if ($rebuild -eq 'y' -or $rebuild -eq 'Y') {
    Write-Host "`n🔨 جاري إعادة Build..." -ForegroundColor Cyan
    Write-Host "   (قد يستغرق 1-2 دقيقة)" -ForegroundColor Yellow
    
    Set-Location "frontend"
    
    # تشغيل npm run build
    $buildProcess = Start-Process -FilePath "npm" -ArgumentList "run", "build" -NoNewWindow -Wait -PassThru
    
    if ($buildProcess.ExitCode -eq 0) {
        Write-Host "`n✅ Build نجح!" -ForegroundColor Green
        
        # التحقق من Build الجديد
        Set-Location ".."
        $newBuildFile = Get-ChildItem "frontend\build\static\js\main.*.js" -ErrorAction SilentlyContinue | Select-Object -First 1
        
        if ($newBuildFile) {
            $newBuildTime = $newBuildFile.LastWriteTime
            Write-Host "   📅 Build الجديد: $($newBuildTime.ToString('dd/MM/yyyy hh:mm:ss tt'))" -ForegroundColor Cyan
            
            # التحقق من المحتوى
            $content = Get-Content $newBuildFile.FullName -Raw
            
            if ($content -match "120000" -and $content -notmatch "200000") {
                Write-Host "   ✅ Build يحتوي على القيمة الصحيحة (120,000)" -ForegroundColor Green
            } else {
                Write-Host "   ⚠️  تحذير: قد يكون Build لا يحتوي على التحديثات الصحيحة" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "`n❌ فشل Build!" -ForegroundColor Red
        Write-Host "   تحقق من الأخطاء أعلاه" -ForegroundColor Yellow
        Set-Location ".."
        Read-Host "`nاضغط Enter للخروج"
        exit
    }
    
    Set-Location ".."
} else {
    Write-Host "`n⏭️  تخطي إعادة Build" -ForegroundColor Yellow
}

# ─────────────────────────────────────────────────────────────────
# 3. رفع التغييرات على Git
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 3: رفع التغييرات على Git" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$gitStatus = git status --porcelain

if ($gitStatus) {
    Write-Host "`n⚠️  يوجد تغييرات غير محفوظة:" -ForegroundColor Yellow
    git status --short
    
    $pushGit = Read-Host "`nهل تريد رفع التغييرات على Git؟ (y/n)"
    
    if ($pushGit -eq 'y' -or $pushGit -eq 'Y') {
        Write-Host "`n📤 جاري رفع التغييرات..." -ForegroundColor Cyan
        
        # إضافة جميع التغييرات
        git add .
        Write-Host "   ✅ تم إضافة التغييرات" -ForegroundColor Green
        
        # Commit
        $commitMsg = Read-Host "`nأدخل رسالة Commit (اضغط Enter للرسالة الافتراضية)"
        if ([string]::IsNullOrWhiteSpace($commitMsg)) {
            $commitMsg = "Rebuild frontend with updated shipping policy (120,000 IQD)"
        }
        
        git commit -m "$commitMsg"
        Write-Host "   ✅ تم Commit" -ForegroundColor Green
        
        # Push
        Write-Host "`n   📤 جاري Push إلى GitHub..." -ForegroundColor Cyan
        git push origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ تم Push بنجاح!" -ForegroundColor Green
            
            $newCommit = git log -1 --format="%h - %s"
            Write-Host "`n   📍 Commit الجديد: $newCommit" -ForegroundColor Cyan
        } else {
            Write-Host "   ❌ فشل Push!" -ForegroundColor Red
            Write-Host "   تحقق من اتصال الإنترنت وصلاحيات Git" -ForegroundColor Yellow
        }
    } else {
        Write-Host "`n⏭️  تخطي رفع التغييرات" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n✅ لا توجد تغييرات جديدة للرفع" -ForegroundColor Green
}

# ─────────────────────────────────────────────────────────────────
# 4. فتح Render Dashboard
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 4: فتح Render Dashboard" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$openRender = Read-Host "`nهل تريد فتح Render Dashboard؟ (y/n)"

if ($openRender -eq 'y' -or $openRender -eq 'Y') {
    Write-Host "`n🚀 فتح Render Dashboard..." -ForegroundColor Cyan
    Start-Process "https://dashboard.render.com"
    
    Write-Host "`n📋 في Render Dashboard:" -ForegroundColor Yellow
    Write-Host "   1. ابحث عن: mimi-store-frontend" -ForegroundColor White
    Write-Host "   2. تحقق من حالة النشر (Deploy Status)" -ForegroundColor White
    Write-Host "   3. إذا لم يبدأ تلقائياً:" -ForegroundColor White
    Write-Host "      • اضغط 'Manual Deploy'" -ForegroundColor Cyan
    Write-Host "      • اختر 'Deploy latest commit'" -ForegroundColor Cyan
    Write-Host "   4. انتظر 5-10 دقائق حتى يكتمل النشر" -ForegroundColor White
}

# ─────────────────────────────────────────────────────────────────
# 5. مسح الكاش
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 5: مسح الكاش" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

Write-Host "`n⚠️  مهم جداً: يجب مسح الكاش!" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  كاش المتصفح:" -ForegroundColor Cyan
Write-Host "   • اضغط: Ctrl + Shift + Delete" -ForegroundColor White
Write-Host "   • اختر: Cached images and files" -ForegroundColor White
Write-Host "   • اختر: All time" -ForegroundColor White
Write-Host "   • اضغط: Clear data" -ForegroundColor White

Write-Host "`n2️⃣  Cloudflare Cache:" -ForegroundColor Cyan
$openCloudflare = Read-Host "   هل تستخدم Cloudflare؟ (y/n)"

if ($openCloudflare -eq 'y' -or $openCloudflare -eq 'Y') {
    Write-Host "`n   🚀 فتح Cloudflare Dashboard..." -ForegroundColor Cyan
    Start-Process "https://dash.cloudflare.com"
    
    Write-Host "`n   📋 في Cloudflare Dashboard:" -ForegroundColor Yellow
    Write-Host "      1. اختر: mimistore1iq.store" -ForegroundColor White
    Write-Host "      2. اذهب إلى: Caching" -ForegroundColor White
    Write-Host "      3. اضغط: Purge Everything" -ForegroundColor White
    Write-Host "      4. أكد العملية" -ForegroundColor White
}

Write-Host "`n3️⃣  Hard Refresh:" -ForegroundColor Cyan
Write-Host "   • افتح الموقع" -ForegroundColor White
Write-Host "   • اضغط: Ctrl + F5" -ForegroundColor White

# ─────────────────────────────────────────────────────────────────
# 6. فتح الموقع للتحقق
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n📌 الخطوة 6: التحقق من التحديثات" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$openSite = Read-Host "`nهل تريد فتح الموقع للتحقق؟ (y/n)"

if ($openSite -eq 'y' -or $openSite -eq 'Y') {
    Write-Host "`n🌐 فتح الموقع..." -ForegroundColor Cyan
    
    # فتح في نافذة عادية
    Start-Process "https://www.mimistore1iq.store"
    Start-Sleep -Seconds 1
    
    # فتح في Incognito (Chrome)
    $openIncognito = Read-Host "`nهل تريد فتح الموقع في Incognito Mode؟ (y/n)"
    if ($openIncognito -eq 'y' -or $openIncognito -eq 'Y') {
        Start-Process "chrome.exe" -ArgumentList "--incognito", "https://www.mimistore1iq.store"
    }
    
    Write-Host "`n✅ تحقق من:" -ForegroundColor Yellow
    Write-Host "   • صفحة المنتج: يجب أن يظهر '120,000 د.ع'" -ForegroundColor White
    Write-Host "   • صفحة الطلب: رسوم التوصيل 5,000 د.ع" -ForegroundColor White
    Write-Host "   • التوصيل المجاني عند 120,000 د.ع أو أكثر" -ForegroundColor White
}

# ─────────────────────────────────────────────────────────────────
# 7. ملخص نهائي
# ─────────────────────────────────────────────────────────────────
Write-Host "`n`n═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ انتهت العملية" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 ملخص ما تم:" -ForegroundColor Green
if ($rebuild -eq 'y' -or $rebuild -eq 'Y') {
    Write-Host "   ✅ إعادة Build للـ Frontend" -ForegroundColor White
}
if ($pushGit -eq 'y' -or $pushGit -eq 'Y') {
    Write-Host "   ✅ رفع التغييرات على Git" -ForegroundColor White
}
if ($openRender -eq 'y' -or $openRender -eq 'Y') {
    Write-Host "   ✅ فتح Render Dashboard" -ForegroundColor White
}

Write-Host "`n⏳ الخطوات المتبقية:" -ForegroundColor Yellow
Write-Host "   1. انتظر اكتمال النشر على Render (5-10 دقائق)" -ForegroundColor White
Write-Host "   2. امسح كاش المتصفح (Ctrl + Shift + Delete)" -ForegroundColor White
if ($openCloudflare -eq 'y' -or $openCloudflare -eq 'Y') {
    Write-Host "   3. امسح كاش Cloudflare (Purge Everything)" -ForegroundColor White
}
Write-Host "   4. افتح الموقع في Incognito Mode للتحقق" -ForegroundColor White

Write-Host "`n💡 إذا لم تظهر التحديثات:" -ForegroundColor Cyan
Write-Host "   • تأكد من اكتمال النشر على Render" -ForegroundColor White
Write-Host "   • امسح الكاش مرة أخرى" -ForegroundColor White
Write-Host "   • جرب متصفح آخر" -ForegroundColor White
Write-Host "   • انتظر 5-10 دقائق إضافية" -ForegroundColor White

Write-Host ""
Read-Host "اضغط Enter للخروج"