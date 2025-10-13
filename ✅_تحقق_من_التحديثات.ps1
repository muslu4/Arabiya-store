# سكريبت التحقق من التحديثات - MIMI Store
# يتحقق من حالة Git و Build و Render

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🔍 التحقق من حالة التحديثات - MIMI STORE            ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# التحقق من Git
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "📊 حالة Git:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow

Set-Location "c:\Users\a\Desktop\ecom_setup\ecom_project\ecom_project"

$lastCommit = git log -1 --format="%h - %s (%ar)"
Write-Host "✅ آخر Commit: $lastCommit" -ForegroundColor Green

$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  هناك تغييرات غير محفوظة!" -ForegroundColor Yellow
} else {
    Write-Host "✅ جميع التغييرات محفوظة على Git" -ForegroundColor Green
}

Write-Host ""

# التحقق من Build
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "🏗️  حالة Build:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow

$buildFile = Get-ChildItem "frontend\build\static\js\main.*.js" | Select-Object -First 1
if ($buildFile) {
    $buildTime = $buildFile.LastWriteTime
    Write-Host "✅ آخر Build: $buildTime" -ForegroundColor Green
    
    # مقارنة وقت Build مع آخر Commit
    $commitTime = git log -1 --format="%ai"
    $commitDateTime = [DateTime]::Parse($commitTime)
    
    if ($buildFile.LastWriteTime -gt $commitDateTime) {
        Write-Host "✅ Build أحدث من آخر Commit - جاهز للنشر!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Build أقدم من آخر Commit - يجب إعادة Build!" -ForegroundColor Red
        Write-Host "   شغّل: npm run build" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ لا يوجد Build! شغّل: npm run build" -ForegroundColor Red
}

Write-Host ""

# التحقق من الاتصال بالإنترنت
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "🌐 حالة الاتصال:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "https://www.mimistore1iq.store" -Method Head -TimeoutSec 10 -UseBasicParsing
    Write-Host "✅ الموقع يعمل - Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  لا يمكن الوصول للموقع" -ForegroundColor Yellow
}

Write-Host ""

# روابط مهمة
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "🔗 روابط سريعة:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host ""

Write-Host "1. Render Dashboard:" -ForegroundColor Cyan
Write-Host "   https://dashboard.render.com" -ForegroundColor White
Write-Host ""

Write-Host "2. الموقع المباشر:" -ForegroundColor Cyan
Write-Host "   https://www.mimistore1iq.store" -ForegroundColor White
Write-Host ""

Write-Host "3. لوحة الإدارة:" -ForegroundColor Cyan
Write-Host "   https://www.mimistore1iq.store/admin" -ForegroundColor White
Write-Host ""

Write-Host "4. Cloudflare:" -ForegroundColor Cyan
Write-Host "   https://dash.cloudflare.com" -ForegroundColor White
Write-Host ""

# خيارات
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "⚡ خيارات سريعة:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host ""

$choice = Read-Host "هل تريد فتح Render Dashboard؟ (y/n)"
if ($choice -eq 'y' -or $choice -eq 'Y') {
    Start-Process "https://dashboard.render.com"
    Write-Host "✅ تم فتح Render Dashboard" -ForegroundColor Green
}

Write-Host ""
$choice2 = Read-Host "هل تريد فتح الموقع المباشر؟ (y/n)"
if ($choice2 -eq 'y' -or $choice2 -eq 'Y') {
    Start-Process "https://www.mimistore1iq.store"
    Write-Host "✅ تم فتح الموقع" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   ✅ انتهى التحقق!                                       ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "اضغط أي زر للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")