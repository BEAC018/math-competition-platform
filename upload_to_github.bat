@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🚀 رفع مشروع منصة المسابقات إلى GitHub
echo ========================================
echo.

REM التحقق من وجود Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git غير مثبت!
    echo.
    echo 📥 يرجى تثبيت Git أولاً من:
    echo https://git-scm.com/download/win
    echo.
    echo أو راجع ملف MANUAL_GIT_SETUP.md للتعليمات التفصيلية
    echo.
    pause
    exit /b 1
)

echo ✅ Git مثبت ومتاح
echo.

REM التحقق من وجود مجلد .git
if exist ".git" (
    echo ⚠️  Repository موجود مسبقاً
    echo.
    set /p choice="هل تريد المتابعة؟ (y/n): "
    if /i not "%choice%"=="y" (
        echo عملية ملغاة
        pause
        exit /b 0
    )
) else (
    echo 🔧 تهيئة Git repository...
    git init
    if %errorlevel% neq 0 (
        echo ❌ فشل في تهيئة Git
        pause
        exit /b 1
    )
    echo ✅ تم تهيئة Git بنجاح
    echo.
)

REM إعداد Git إذا لم يكن معداً
for /f "tokens=*" %%i in ('git config --global user.name 2^>nul') do set username=%%i
if "%username%"=="" (
    echo 🔧 إعداد Git للمرة الأولى...
    git config --global user.name "BEAC1"
    git config --global user.email "beac1@example.com"
    git config --global init.defaultBranch main
    echo ✅ تم إعداد Git بنجاح
    echo.
)

echo 📁 إضافة جميع الملفات...
git add .
if %errorlevel% neq 0 (
    echo ❌ فشل في إضافة الملفات
    pause
    exit /b 1
)
echo ✅ تم إضافة جميع الملفات

echo.
echo 💾 إنشاء commit...
git commit -m "Initial commit: Math Competition Platform v2.0.0

- منصة تعليمية تفاعلية لمسابقات الحساب
- دعم 9 مستويات صعوبة متدرجة
- واجهة عربية جميلة ومتجاوبة
- نظام إدارة شامل للمعلمين
- إحصائيات وتقارير مفصلة
- تحسينات الأداء والأمان
- ملفات توثيق شاملة
- أدلة التثبيت والاستخدام"

if %errorlevel% neq 0 (
    echo ❌ فشل في إنشاء commit
    pause
    exit /b 1
)
echo ✅ تم إنشاء commit بنجاح

echo.
echo 🔗 ربط بـ GitHub repository...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/BEAC1/math-competition-platform.git
if %errorlevel% neq 0 (
    echo ❌ فشل في ربط Repository
    pause
    exit /b 1
)
echo ✅ تم ربط Repository بنجاح

echo.
echo 🌿 تعيين الفرع الرئيسي...
git branch -M main
if %errorlevel% neq 0 (
    echo ❌ فشل في تعيين الفرع
    pause
    exit /b 1
)
echo ✅ تم تعيين الفرع الرئيسي

echo.
echo ========================================
echo 🚀 رفع الملفات إلى GitHub...
echo ========================================
echo.
echo 🔐 ملاحظة مهمة:
echo عند طلب تسجيل الدخول:
echo Username: BEAC1
echo Password: استخدم Personal Access Token
echo.
echo إذا لم يكن لديك Token:
echo 1. اذهب إلى GitHub.com
echo 2. Settings ^> Developer settings
echo 3. Personal access tokens ^> Tokens (classic)
echo 4. Generate new token
echo 5. اختر صلاحيات: repo, workflow
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 🎉 تم رفع المشروع بنجاح!
    echo ========================================
    echo.
    echo ✅ Repository URL:
    echo https://github.com/BEAC1/math-competition-platform
    echo.
    echo 📋 الخطوات التالية:
    echo 1. اذهب إلى GitHub Repository
    echo 2. أضف وصف للمشروع
    echo 3. أضف Topics: django, python, education, math, arabic
    echo 4. تحقق من ظهور README بشكل صحيح
    echo.
    echo 🌟 مبروك! مشروعك الآن متاح للعالم!
) else (
    echo.
    echo ========================================
    echo ❌ فشل في رفع المشروع
    echo ========================================
    echo.
    echo 🔧 حلول مقترحة:
    echo 1. تأكد من اتصال الإنترنت
    echo 2. تأكد من صحة Personal Access Token
    echo 3. جرب الأوامر يدوياً:
    echo    git push -u origin main
    echo.
    echo 📖 راجع ملف MANUAL_GIT_SETUP.md للمساعدة
)

echo.
pause
