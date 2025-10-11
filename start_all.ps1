# MIMI STORE - Full Stack Startup Script
# تشغيل الواجهة الأمامية والخلفية معاً

# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Colors
$colors = @{
    Success = "Green"
    Error = "Red"
    Warning = "Yellow"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" $colors.Header
    Write-ColorOutput "║  $Text" $colors.Header
    Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" $colors.Header
    Write-Host ""
}

function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Clear screen
Clear-Host

Write-Header "🚀 تشغيل MIMI STORE - كامل المشروع 🚀"

# Get script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# ═══════════════════════════════════════════════════════════
# Check Prerequisites
# ═══════════════════════════════════════════════════════════
Write-ColorOutput "[0/3] 🔍 فحص المتطلبات..." $colors.Info

# Check Python
if (-not (Test-Command "python")) {
    Write-ColorOutput "❌ Python غير مثبت! يرجى تثبيت Python 3.8 أو أحدث" $colors.Error
    pause
    exit 1
}
Write-ColorOutput "✅ Python متوفر" $colors.Success

# Check Node.js
if (-not (Test-Command "node")) {
    Write-ColorOutput "❌ Node.js غير مثبت! يرجى تثبيت Node.js" $colors.Error
    pause
    exit 1
}
Write-ColorOutput "✅ Node.js متوفر" $colors.Success

# Check if ports are available
if (Test-Port 8000) {
    Write-ColorOutput "⚠️  المنفذ 8000 مستخدم بالفعل! سيتم استخدام Backend الحالي" $colors.Warning
    $backendRunning = $true
} else {
    $backendRunning = $false
}

if (Test-Port 3002) {
    Write-ColorOutput "⚠️  المنفذ 3002 مستخدم بالفعل! سيتم استخدام Frontend الحالي" $colors.Warning
    $frontendRunning = $true
} else {
    $frontendRunning = $false
}

Write-Host ""

# ═══════════════════════════════════════════════════════════
# 1. Start Backend (Django)
# ═══════════════════════════════════════════════════════════
if (-not $backendRunning) {
    Write-ColorOutput "[1/3] 🔧 تشغيل Backend Server..." $colors.Info
    Write-Host ""

    # Check if virtual environment exists
    if (-not (Test-Path "backend\env")) {
        Write-ColorOutput "📦 إنشاء البيئة الافتراضية..." $colors.Warning
        Set-Location backend
        python -m venv env
        Set-Location ..
        Write-ColorOutput "✅ تم إنشاء البيئة الافتراضية" $colors.Success
    }

    # Start Backend in new window
    $backendPath = Join-Path $scriptPath "backend"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\env\Scripts\Activate.ps1; python manage.py runserver 8000" -WindowStyle Normal

    Write-ColorOutput "✅ تم تشغيل Backend Server على المنفذ 8000" $colors.Success
    Write-Host ""

    # Wait for backend to start
    Write-ColorOutput "⏳ انتظار تشغيل Backend..." $colors.Info
    $timeout = 30
    $elapsed = 0
    while (-not (Test-Port 8000) -and $elapsed -lt $timeout) {
        Start-Sleep -Seconds 1
        $elapsed++
        Write-Host "." -NoNewline
    }
    Write-Host ""

    if (Test-Port 8000) {
        Write-ColorOutput "✅ Backend جاهز!" $colors.Success
    } else {
        Write-ColorOutput "⚠️  Backend قد يستغرق وقتاً أطول للتشغيل" $colors.Warning
    }
} else {
    Write-ColorOutput "[1/3] ✅ Backend يعمل بالفعل" $colors.Success
}

Write-Host ""

# ═══════════════════════════════════════════════════════════
# 2. Start Frontend (React)
# ═══════════════════════════════════════════════════════════
if (-not $frontendRunning) {
    Write-ColorOutput "[2/3] 🎨 تشغيل Frontend Server..." $colors.Info
    Write-Host ""

    # Check if node_modules exists
    if (-not (Test-Path "frontend\node_modules")) {
        Write-ColorOutput "📦 تثبيت حزم Node.js... (قد يستغرق بضع دقائق)" $colors.Warning
        Set-Location frontend
        npm install
        Set-Location ..
        Write-ColorOutput "✅ تم تثبيت الحزم" $colors.Success
        Write-Host ""
    }

    # Start Frontend in new window
    $frontendPath = Join-Path $scriptPath "frontend"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm start" -WindowStyle Normal

    Write-ColorOutput "✅ تم تشغيل Frontend Server على المنفذ 3002" $colors.Success
    Write-Host ""

    # Wait for frontend to start
    Write-ColorOutput "⏳ انتظار تشغيل Frontend..." $colors.Info
    $timeout = 60
    $elapsed = 0
    while (-not (Test-Port 3002) -and $elapsed -lt $timeout) {
        Start-Sleep -Seconds 1
        $elapsed++
        if ($elapsed % 5 -eq 0) {
            Write-Host "." -NoNewline
        }
    }
    Write-Host ""

    if (Test-Port 3002) {
        Write-ColorOutput "✅ Frontend جاهز!" $colors.Success
    } else {
        Write-ColorOutput "⚠️  Frontend قد يستغرق وقتاً أطول للتشغيل" $colors.Warning
    }
} else {
    Write-ColorOutput "[2/3] ✅ Frontend يعمل بالفعل" $colors.Success
}

Write-Host ""

# ═══════════════════════════════════════════════════════════
# 3. Open Browser
# ═══════════════════════════════════════════════════════════
Write-ColorOutput "[3/3] 🌐 فتح المتصفح..." $colors.Info
Start-Sleep -Seconds 2
Start-Process "http://localhost:3002"
Write-ColorOutput "✅ تم فتح المتصفح" $colors.Success

Write-Host ""

# ═══════════════════════════════════════════════════════════
# Display Information
# ═══════════════════════════════════════════════════════════
Write-Header "✅ تم تشغيل المشروع بنجاح! ✅"

Write-ColorOutput "🔗 الروابط المتاحة:" $colors.Header
Write-Host "   ┌─────────────────────────────────────────────────────────"
Write-ColorOutput "   │ 🌐 الواجهة الأمامية:  http://localhost:3002" $colors.Info
Write-ColorOutput "   │ 🔧 Backend API:        http://localhost:8000/api" $colors.Info
Write-ColorOutput "   │ 👤 لوحة الإدارة:       http://localhost:8000/admin" $colors.Info
Write-Host "   └─────────────────────────────────────────────────────────"
Write-Host ""

Write-ColorOutput "👤 بيانات تسجيل الدخول للإدارة:" $colors.Header
Write-Host "   ┌─────────────────────────────────────────────────────────"
Write-ColorOutput "   │ 📱 الهاتف:           admin" $colors.Success
Write-ColorOutput "   │ 🔑 كلمة المرور:      admin123" $colors.Success
Write-Host "   └─────────────────────────────────────────────────────────"
Write-Host ""

Write-ColorOutput "📊 اختبار API:" $colors.Header
Write-Host "   ┌─────────────────────────────────────────────────────────"
Write-ColorOutput "   │ المنتجات:    http://localhost:8000/api/products/" $colors.Info
Write-ColorOutput "   │ الأقسام:     http://localhost:8000/api/products/categories/" $colors.Info
Write-ColorOutput "   │ الطلبات:     http://localhost:8000/api/orders/" $colors.Info
Write-ColorOutput "   │ الكوبونات:   http://localhost:8000/api/coupons/" $colors.Info
Write-Host "   └─────────────────────────────────────────────────────────"
Write-Host ""

Write-ColorOutput "💡 ملاحظات مهمة:" $colors.Warning
Write-Host "   • لإيقاف الخوادم، أغلق نوافذ PowerShell الخاصة بها"
Write-Host "   • استخدم F12 في المتصفح لفتح Developer Tools"
Write-Host "   • تأكد من تشغيل كلا الخادمين قبل استخدام التطبيق"
Write-Host ""

Write-ColorOutput "🎯 المميزات المتاحة:" $colors.Success
Write-Host "   ✅ عرض المنتجات والأقسام"
Write-Host "   ✅ البحث والفلترة"
Write-Host "   ✅ سلة التسوق"
Write-Host "   ✅ نظام الكوبونات"
Write-Host "   ✅ إدارة الطلبات"
Write-Host "   ✅ تسجيل الدخول والتسجيل"
Write-Host "   ✅ تصميم متجاوب (Mobile-Friendly)"
Write-Host ""

Write-ColorOutput "═══════════════════════════════════════════════════════════" $colors.Header
Write-ColorOutput " اضغط أي زر لإغلاق هذه النافذة..." $colors.Info
Write-ColorOutput " (الخوادم ستستمر في العمل في النوافذ الأخرى)" $colors.Info
Write-ColorOutput "═══════════════════════════════════════════════════════════" $colors.Header

pause