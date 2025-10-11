# MIMI STORE - Stop All Servers Script
# إيقاف جميع الخوادم

# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Colors
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Clear screen
Clear-Host

Write-Host ""
Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" "Magenta"
Write-ColorOutput "║                                                            ║" "Magenta"
Write-ColorOutput "║            🛑 MIMI STORE - إيقاف الخوادم 🛑               ║" "Magenta"
Write-ColorOutput "║                                                            ║" "Magenta"
Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" "Magenta"
Write-Host ""
Write-Host ""

Write-ColorOutput "🔍 البحث عن الخوادم النشطة..." "Cyan"
Write-Host ""

# ═══════════════════════════════════════════════════════════
# Stop Backend (Django - Port 8000)
# ═══════════════════════════════════════════════════════════
Write-ColorOutput "[1/2] 🔧 إيقاف Backend Server (Port 8000)..." "Yellow"

$backendProcesses = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique

if ($backendProcesses) {
    foreach ($pid in $backendProcesses) {
        try {
            $process = Get-Process -Id $pid -ErrorAction Stop
            Write-ColorOutput "   • إيقاف العملية: $($process.Name) (PID: $pid)" "Gray"
            Stop-Process -Id $pid -Force -ErrorAction Stop
        }
        catch {
            Write-ColorOutput "   ⚠️  تعذر إيقاف العملية: $pid" "Yellow"
        }
    }
    Write-ColorOutput "✅ تم إيقاف Backend" "Green"
} else {
    Write-ColorOutput "ℹ️  Backend غير نشط" "Gray"
}

Write-Host ""

# ═══════════════════════════════════════════════════════════
# Stop Frontend (React - Port 3002)
# ═══════════════════════════════════════════════════════════
Write-ColorOutput "[2/2] 🎨 إيقاف Frontend Server (Port 3002)..." "Yellow"

$frontendProcesses = Get-NetTCPConnection -LocalPort 3002 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique

if ($frontendProcesses) {
    foreach ($pid in $frontendProcesses) {
        try {
            $process = Get-Process -Id $pid -ErrorAction Stop
            Write-ColorOutput "   • إيقاف العملية: $($process.Name) (PID: $pid)" "Gray"
            Stop-Process -Id $pid -Force -ErrorAction Stop
        }
        catch {
            Write-ColorOutput "   ⚠️  تعذر إيقاف العملية: $pid" "Yellow"
        }
    }
    Write-ColorOutput "✅ تم إيقاف Frontend" "Green"
} else {
    Write-ColorOutput "ℹ️  Frontend غير نشط" "Gray"
}

Write-Host ""

# ═══════════════════════════════════════════════════════════
# Stop additional Python and Node processes (optional)
# ═══════════════════════════════════════════════════════════
Write-ColorOutput "🧹 تنظيف العمليات الإضافية..." "Cyan"
Write-Host ""

# Stop Python processes related to manage.py
$pythonProcesses = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*manage.py*"
}

if ($pythonProcesses) {
    foreach ($process in $pythonProcesses) {
        try {
            Write-ColorOutput "   • إيقاف Python: $($process.Name) (PID: $($process.Id))" "Gray"
            Stop-Process -Id $process.Id -Force -ErrorAction Stop
        }
        catch {
            Write-ColorOutput "   ⚠️  تعذر إيقاف العملية: $($process.Id)" "Yellow"
        }
    }
}

# Stop Node processes related to react-scripts
$nodeProcesses = Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*react-scripts*"
}

if ($nodeProcesses) {
    foreach ($process in $nodeProcesses) {
        try {
            Write-ColorOutput "   • إيقاف Node: $($process.Name) (PID: $($process.Id))" "Gray"
            Stop-Process -Id $process.Id -Force -ErrorAction Stop
        }
        catch {
            Write-ColorOutput "   ⚠️  تعذر إيقاف العملية: $($process.Id)" "Yellow"
        }
    }
}

Write-Host ""
Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" "Green"
Write-ColorOutput "║                                                            ║" "Green"
Write-ColorOutput "║              ✅ تم إيقاف جميع الخوادم! ✅                 ║" "Green"
Write-ColorOutput "║                                                            ║" "Green"
Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" "Green"
Write-Host ""

Write-ColorOutput "💡 يمكنك الآن:" "Cyan"
Write-Host "   • إعادة تشغيل المشروع باستخدام START.bat أو start_all.ps1"
Write-Host "   • إغلاق هذه النافذة"
Write-Host ""

Write-ColorOutput "═══════════════════════════════════════════════════════════" "Magenta"
pause