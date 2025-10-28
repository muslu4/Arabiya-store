# Create Desktop Shortcut for العربية فون
# إنشاء اختصار على سطح المكتب

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "║         🔗 إنشاء اختصار العربية فون على سطح المكتب 🔗      ║" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

# Get script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$startBatPath = Join-Path $scriptPath "START.bat"

# Get desktop path
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "العربية فون.lnk"

# Check if START.bat exists
if (-not (Test-Path $startBatPath)) {
    Write-Host "❌ خطأ: ملف START.bat غير موجود!" -ForegroundColor Red
    Write-Host "   المسار المتوقع: $startBatPath" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "📁 مسار المشروع: $scriptPath" -ForegroundColor Cyan
Write-Host "🖥️  مسار سطح المكتب: $desktopPath" -ForegroundColor Cyan
Write-Host ""

try {
    # Create WScript Shell object
    $WScriptShell = New-Object -ComObject WScript.Shell
    
    # Create shortcut
    $Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $startBatPath
    $Shortcut.WorkingDirectory = $scriptPath
    $Shortcut.Description = "تشغيل العربية فون - متجر إلكتروني"
    $Shortcut.IconLocation = "shell32.dll,43"  # Shopping cart icon
    $Shortcut.Save()
    
    Write-Host "✅ تم إنشاء الاختصار بنجاح!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 موقع الاختصار: $shortcutPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 يمكنك الآن:" -ForegroundColor Cyan
    Write-Host "   • النقر نقراً مزدوجاً على الاختصار لتشغيل المشروع" -ForegroundColor White
    Write-Host "   • سحب الاختصار إلى شريط المهام للوصول السريع" -ForegroundColor White
    Write-Host ""
    
    # Ask if user wants to open desktop
    $response = Read-Host "هل تريد فتح سطح المكتب الآن؟ (Y/N)"
    if ($response -eq "Y" -or $response -eq "y" -or $response -eq "نعم") {
        Start-Process explorer.exe $desktopPath
    }
    
} catch {
    Write-Host "❌ خطأ في إنشاء الاختصار: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 حل بديل:" -ForegroundColor Yellow
    Write-Host "   1. انقر بزر الماوس الأيمن على START.bat" -ForegroundColor White
    Write-Host "   2. اختر 'إرسال إلى' > 'سطح المكتب (إنشاء اختصار)'" -ForegroundColor White
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Magenta
pause