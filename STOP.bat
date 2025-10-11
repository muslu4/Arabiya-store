@echo off
chcp 65001 >nul
title MIMI STORE - إيقاف الخوادم

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║            🛑 MIMI STORE - إيقاف الخوادم 🛑               ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.

echo 🔍 البحث عن الخوادم النشطة...
echo.

REM ═══════════════════════════════════════════════════════════
REM  إيقاف Backend (Django - Port 8000)
REM ═══════════════════════════════════════════════════════════
echo [1/2] 🔧 إيقاف Backend Server (Port 8000)...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo    • إيقاف العملية: %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo ✅ تم إيقاف Backend
echo.

REM ═══════════════════════════════════════════════════════════
REM  إيقاف Frontend (React - Port 3002)
REM ═══════════════════════════════════════════════════════════
echo [2/2] 🎨 إيقاف Frontend Server (Port 3002)...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3002 ^| findstr LISTENING') do (
    echo    • إيقاف العملية: %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo ✅ تم إيقاف Frontend
echo.

REM ═══════════════════════════════════════════════════════════
REM  إيقاف عمليات Python و Node إضافية (اختياري)
REM ═══════════════════════════════════════════════════════════
echo 🧹 تنظيف العمليات الإضافية...
echo.

REM إيقاف عمليات Python المتعلقة بـ manage.py
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "python.exe"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /i "manage.py" >nul
    if not errorlevel 1 (
        echo    • إيقاف Python: %%a
        taskkill /PID %%a /F >nul 2>&1
    )
)

REM إيقاف عمليات Node المتعلقة بـ react-scripts
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "node.exe"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /i "react-scripts" >nul
    if not errorlevel 1 (
        echo    • إيقاف Node: %%a
        taskkill /PID %%a /F >nul 2>&1
    )
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✅ تم إيقاف جميع الخوادم! ✅                 ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 💡 يمكنك الآن:
echo    • إعادة تشغيل المشروع باستخدام START.bat
echo    • إغلاق هذه النافذة
echo.
echo ═══════════════════════════════════════════════════════════
pause