@echo off
chcp 65001 >nul
title 🌐 نشر منصة المسابقات الرياضية على الويب

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        🌐 نشر منصة المسابقات الرياضية على الويب           ║
echo ║                                                              ║
echo ║              🚀 نشر تلقائي وسريع وآمن                      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت
    echo 💡 يرجى تثبيت Python من: https://python.org
    pause
    exit /b 1
)
echo ✅ Python متوفر

echo.
echo 🚀 بدء عملية النشر التلقائي...
echo.

python deploy_to_web.py

echo.
echo 🎉 انتهت عملية النشر!
echo.
pause
