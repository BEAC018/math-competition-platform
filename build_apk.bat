@echo off
REM سكريپت بناء APK للتطبيق - Windows

echo 📱 بناء تطبيق المسابقات الرياضية APK
echo ========================================

REM التحقق من وجود Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت أو غير موجود في PATH
    pause
    exit /b 1
)

REM التحقق من وجود buildozer
pip show buildozer >nul 2>&1
if errorlevel 1 (
    echo ❌ Buildozer غير مثبت. يرجى تثبيته أولاً:
    echo pip install buildozer
    pause
    exit /b 1
)

REM التحقق من وجود الملفات المطلوبة
if not exist "main.py" (
    echo ❌ ملف main.py غير موجود
    pause
    exit /b 1
)

if not exist "buildozer.spec" (
    echo ❌ ملف buildozer.spec غير موجود
    pause
    exit /b 1
)

echo ✅ جميع الملفات المطلوبة موجودة

REM تنظيف البناء السابق
echo 🧹 تنظيف البناء السابق...
buildozer android clean

REM بناء APK
echo 🏗️ بناء APK...
buildozer android debug

REM التحقق من نجاح البناء
if exist "bin\*.apk" (
    echo ✅ تم بناء APK بنجاح!
    for %%f in (bin\*.apk) do (
        echo 📁 الملف: %%f
        copy "%%f" "math-competition-app.apk"
        echo 📱 تم نسخ APK إلى: math-competition-app.apk
    )
) else (
    echo ❌ فشل في بناء APK
    pause
    exit /b 1
)

echo 🎉 اكتمل البناء بنجاح!
pause
